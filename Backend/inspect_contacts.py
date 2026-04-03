"""Inspect contacts-related tables in Supabase."""
import httpx
from pathlib import Path


def load_env(p=".env"):
    env = {}
    for line in Path(p).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            k, _, v = line.partition("=")
            env[k.strip()] = v.strip().strip('"')
    return env


e = load_env(Path(__file__).parent / ".env")
URL = e["SUPABASE_URL"].rstrip("/")
KEY = e["SUPABASE_SERVICE_ROLE_KEY"]
H = {
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
    "Accept": "application/json",
}


def get(path, params=None):
    return httpx.get(
        f"{URL}/rest/v1/{path}",
        headers=H,
        params=params or {},
        timeout=15,
    )


# 1. List all public tables
print("=== ALL PUBLIC TABLES ===")
r = get(
    "information_schema/tables",
    {"table_schema": "eq.public", "select": "table_name", "limit": "100"},
)
print("Status:", r.status_code)
if r.status_code == 200:
    tables = sorted([t["table_name"] for t in r.json()])
    for t in tables:
        print(" ", t)
else:
    print(r.text[:500])

# 2. Try common contacts table names and inspect whichever exists
print("\n=== CONTACTS TABLE INSPECTION ===")
candidates = ["contacts", "account_contacts", "people", "leads", "crm_contacts"]
for name in candidates:
    r2 = get(name, {"select": "*", "limit": "2"})
    if r2.status_code == 200:
        rows = r2.json()
        print(f"\nFound table: {name}")
        if rows:
            print("  Columns:", list(rows[0].keys()))
            print("  Sample row (redacted):")
            for k, v in rows[0].items():
                # Redact email-like values partially
                if isinstance(v, str) and "@" in v:
                    v = v[:3] + "***" + v[v.index("@"):]
                print(f"    {k}: {v}")
        else:
            print("  Table exists but is empty.")
        # Also get total count
        r3 = get(name, {"select": "count", "limit": "1"})
        print(f"  Row count response: {r3.status_code}")
    elif r2.status_code != 404 and r2.status_code != 400:
        print(f"\n{name}: status {r2.status_code} — {r2.text[:200]}")
