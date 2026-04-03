"""
inspect_schema.py — Diagnostic script to inspect existing Supabase tables.

Fetches column definitions, sample rows, and RLS policies for all tables
to understand the existing schema before extending it.

Run with:  poetry run python inspect_schema.py
"""

import os
import json
import re
from pathlib import Path
import httpx


# ── Load .env manually (no extra dep needed) ─────────────────────────────────

def load_env(env_path: str = ".env") -> dict[str, str]:
    env: dict[str, str] = {}
    p = Path(env_path)
    if not p.exists():
        raise FileNotFoundError(f".env not found at {p.resolve()}")
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, _, val = line.partition("=")
            env[key.strip()] = val.strip().strip('"').strip("'")
    return env


env = load_env(Path(__file__).parent / ".env")

SUPABASE_URL = env.get("SUPABASE_URL", "").rstrip("/")
ANON_KEY     = env.get("SUPABASE_ANON_KEY", "")
SVC_KEY      = env.get("SUPABASE_SERVICE_ROLE_KEY", "")

# Prefer service role key; fall back to anon key if svc is still a placeholder
ACTIVE_KEY = SVC_KEY if (SVC_KEY and not SVC_KEY.startswith("your-")) else ANON_KEY

HEADERS = {
    "apikey": ACTIVE_KEY,
    "Authorization": f"Bearer {ACTIVE_KEY}",
    "Accept": "application/json",
    "Content-Type": "application/json",
}

DIVIDER = "─" * 60


# ── Helpers ───────────────────────────────────────────────────────────────────

def _hint_jwt_role(token: str) -> str:
    """Decode JWT payload (no verification) and return role claim."""
    try:
        import base64
        parts = token.split(".")
        if len(parts) != 3:
            return "unknown"
        padded = parts[1] + "=" * (-len(parts[1]) % 4)
        payload = json.loads(base64.urlsafe_b64decode(padded))
        return payload.get("role", "unknown")
    except Exception:
        return "unknown"


def rest_get(path: str, params: dict | None = None) -> httpx.Response:
    return httpx.get(
        f"{SUPABASE_URL}/rest/v1/{path}",
        headers=HEADERS,
        params=params or {},
        timeout=15,
    )


def rest_post_rpc(fn: str, args: dict) -> httpx.Response:
    return httpx.post(
        f"{SUPABASE_URL}/rest/v1/rpc/{fn}",
        headers=HEADERS,
        json=args,
        timeout=15,
    )


# ── Key sanity check ──────────────────────────────────────────────────────────

def check_keys():
    print(f"\n{'KEY DIAGNOSTIC':^60}")
    print(DIVIDER)

    anon_role = _hint_jwt_role(ANON_KEY)
    print(f"  SUPABASE_ANON_KEY role claim   : {anon_role}")
    if anon_role == "service_role":
        print("  ⚠️  WARNING: your SUPABASE_ANON_KEY contains the SERVICE ROLE key!")
        print("     This bypasses Row Level Security everywhere get_supabase() is called.")
        print("     Fix: swap key values so SUPABASE_ANON_KEY gets the anon/public key.")

    svc_role = _hint_jwt_role(SVC_KEY) if SVC_KEY and not SVC_KEY.startswith("your-") else "placeholder"
    print(f"  SUPABASE_SERVICE_ROLE_KEY role : {svc_role}")
    if svc_role == "placeholder":
        print("  ℹ️  SUPABASE_SERVICE_ROLE_KEY is still a placeholder.")

    print(f"  Active key used for this script: {_hint_jwt_role(ACTIVE_KEY)} ({ACTIVE_KEY[:24]}…)")


# ── Table introspection ───────────────────────────────────────────────────────

def describe_table(table: str):
    print(f"\n  TABLE: {table}")
    print(f"  {'─'*56}")

    # Fetch up to 3 rows to infer columns
    resp = rest_get(table, {"select": "*", "limit": "3"})

    if resp.status_code == 200:
        rows = resp.json()
        if rows:
            print(f"  Columns (inferred from live row):")
            for col, val in rows[0].items():
                type_hint = type(val).__name__ if val is not None else "null"
                sample = repr(val)
                if len(sample) > 60:
                    sample = sample[:57] + "…"
                print(f"    {col:<30} {type_hint:<12} {sample}")
            print(f"\n  Rows returned (sample ≤3): {len(rows)}")
            print(f"\n  Full first row (pretty):")
            print("    " + json.dumps(rows[0], indent=4, default=str).replace("\n", "\n    "))
        else:
            print("  Table exists but is empty — no rows to infer columns from.")
    elif resp.status_code == 404:
        print(f"  Table not found / not exposed via REST API.")
    elif resp.status_code in (401, 403):
        print(f"  HTTP {resp.status_code} Unauthorized — key may lack permissions.")
        print(f"  Response: {resp.text[:200]}")
    else:
        print(f"  HTTP {resp.status_code}")
        print(f"  Response: {resp.text[:300]}")


# ── RLS policies ──────────────────────────────────────────────────────────────

POLICY_SQL = """
select
  tablename,
  policyname,
  cmd,
  permissive,
  qual,
  with_check
from pg_policies
where schemaname = 'public'
order by tablename, policyname;
"""

def fetch_policies():
    """Try to get policies via a raw-SQL RPC function if one exists."""
    print(f"\n{'RLS POLICIES':^60}")
    print(DIVIDER)

    # Try via a commonly-available exec_sql RPC
    for fn_name in ("exec_sql", "run_sql", "execute_sql"):
        resp = rest_post_rpc(fn_name, {"query": POLICY_SQL})
        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data, list):
                for row in data:
                    t = row.get("tablename", "")
                    p = row.get("policyname", "")
                    cmd = row.get("cmd", "")
                    qual = row.get("qual", "")[:80]
                    wc  = row.get("with_check", "")[:80]
                    print(f"  [{t}] {p} — {cmd}")
                    if qual: print(f"    USING:      {qual}")
                    if wc:   print(f"    WITH CHECK: {wc}")
            return

    # No RPC available — print SQL for manual run
    print("  No exec_sql RPC found. Run this in Supabase SQL Editor:")
    print()
    print("  " + POLICY_SQL.strip().replace("\n", "\n  "))


# ── Column definitions via information_schema ─────────────────────────────────

COLUMNS_SQL = """
select
  table_name,
  column_name,
  data_type,
  is_nullable,
  column_default
from information_schema.columns
where table_schema = 'public'
order by table_name, ordinal_position;
"""

def fetch_column_definitions():
    print(f"\n{'COLUMN DEFINITIONS (information_schema)':^60}")
    print(DIVIDER)

    resp = rest_get("information_schema.columns", {
        "select": "table_name,column_name,data_type,is_nullable,column_default",
        "table_schema": "eq.public",
        "order": "table_name,ordinal_position",
    })

    if resp.status_code == 200:
        rows = resp.json()
        current_table = None
        for row in rows:
            if row["table_name"] != current_table:
                current_table = row["table_name"]
                print(f"\n  {current_table}")
            nullable = "NULL" if row["is_nullable"] == "YES" else "NOT NULL"
            default  = f"  DEFAULT {row['column_default']}" if row["column_default"] else ""
            print(f"    {row['column_name']:<30} {row['data_type']:<20} {nullable}{default}")
    else:
        print(f"  information_schema not accessible via REST ({resp.status_code}).")
        print("  Run this manually in Supabase SQL Editor:")
        print()
        print("  " + COLUMNS_SQL.strip().replace("\n", "\n  "))


# ── All public tables ─────────────────────────────────────────────────────────

def list_all_tables() -> list[str]:
    resp = rest_get("information_schema.tables", {
        "select": "table_name,table_type",
        "table_schema": "eq.public",
        "order": "table_name",
    })
    if resp.status_code == 200:
        return [r["table_name"] for r in resp.json()]
    # Fall back to known + guessed names
    return [
        "accounts",
        "account_sites",
        "reports",
        "questionnaires",
        "events",
        "site_events",
        "account_events",
        "account_sites_report",
    ]


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print(f"{'AutomatiSOR — Supabase Schema Inspector':^60}")
    print("=" * 60)
    print(f"  URL: {SUPABASE_URL}")

    check_keys()

    # 1. Discover all public tables
    print(f"\n{'PUBLIC TABLES':^60}")
    print(DIVIDER)
    tables = list_all_tables()
    for t in tables:
        print(f"  - {t}")

    # 2. Describe each table (sample rows)
    print(f"\n{'TABLE DETAILS (sample rows)':^60}")
    print(DIVIDER)
    for t in tables:
        describe_table(t)

    # 3. Column definitions via information_schema
    fetch_column_definitions()

    # 4. RLS policies
    fetch_policies()

    print(f"\n{'='*60}")
    print("  Done. Paste the output above when asking Copilot to")
    print("  design account_sites_report.")
    print("=" * 60)


if __name__ == "__main__":
    main()
