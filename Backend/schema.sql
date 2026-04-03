-- ============================================
-- AutomatiSOR — Supabase Schema
-- ============================================
-- NOTE: accounts and account_sites already exist in the DB.
--       Their definitions below are for reference only.
--       Run sections marked "NEW" to add the new table.
-- ============================================

-- 1. Accounts table (one per company)
-- EXISTING — already in DB. Columns confirmed from live inspection.
-- PK is account_id (not id). "is SME" has a space in the column name.
-- create table if not exists accounts (
--   account_id          uuid primary key default gen_random_uuid(),
--   company_name        text not null,
--   company_description text,
--   account_domain      text,
--   linkedin_url        text,
--   company_size        text,
--   company_type        text,
--   industry            text,
--   employee_count      int,
--   year_founded        int,
--   hq_city             text,
--   hq_region           text,
--   hq_country          text,
--   hq_country_code     text,
--   hq_postal_code      text,
--   hq_address_line_1   text,
--   annual_revenue      numeric,
--   metadata            jsonb,
--   created_at          timestamptz not null default now(),
--   updated_at          timestamptz not null default now(),
--   "is SME"            boolean not null default true,   -- false = not eligible for report
--   ignore              boolean not null default false   -- true  = excluded from processing
-- );

-- ============================================
-- NEW: account_sites_report
-- One report row per site.
-- Mirrors the is_archived pattern from account_sites:
--   archived when accounts.ignore = true  OR  accounts."is SME" = false
-- ============================================

-- 2. account_sites_report table
create table if not exists account_sites_report (
  report_id         uuid primary key default gen_random_uuid(),
  account_id        uuid not null references accounts(account_id) on delete cascade,
  site_id           uuid not null references account_sites(site_id) on delete cascade,
  report_metadata   jsonb not null default '{}',   -- full report JSON (sections, ofi_score, flags, etc.)
  created_at        timestamptz not null default now(),
  updated_at        timestamptz not null default now(),

  -- Archive fields — same pattern as account_sites
  is_archived       boolean not null default false,
  archived_at       timestamptz,
  archived_reason   text,

  -- One report per site
  constraint uq_account_sites_report_site unique (site_id)
);

-- Indexes for fast account-level lookups and archive filtering
create index if not exists idx_asr_account_id  on account_sites_report(account_id);
create index if not exists idx_asr_site_id     on account_sites_report(site_id);
create index if not exists idx_asr_is_archived on account_sites_report(is_archived);

-- Auto-update updated_at on every row change
create or replace function set_updated_at()
returns trigger language plpgsql as $$
begin
  new.updated_at := now();
  return new;
end;
$$;

create trigger trg_asr_updated_at
  before update on account_sites_report
  for each row execute function set_updated_at();


-- ============================================
-- Archive trigger:
-- When an account's ignore or "is SME" changes,
-- automatically archive / un-archive all its reports
-- to match the same logic already applied to account_sites.
-- ============================================

create or replace function sync_asr_archive_from_account()
returns trigger language plpgsql as $$
declare
  should_archive boolean;
begin
  -- Same rule as account_sites: ignore=true OR "is SME"=false
  should_archive := (new.ignore = true) or (new."is SME" = false);

  if should_archive then
    update account_sites_report
    set
      is_archived     = true,
      archived_at     = coalesce(archived_at, now()),   -- preserve original archive time if already set
      archived_reason = 'Account ineligible (ignore=true OR is SME=false).'
    where account_id  = new.account_id
      and is_archived = false;                          -- only touch currently active rows
  else
    -- Account became eligible again — un-archive its reports
    update account_sites_report
    set
      is_archived     = false,
      archived_at     = null,
      archived_reason = null
    where account_id  = new.account_id
      and is_archived = true
      and archived_reason = 'Account ineligible (ignore=true OR is SME=false).';
  end if;

  return new;
end;
$$;

create trigger trg_accounts_sync_asr
  after update of ignore, "is SME"
  on accounts
  for each row execute function sync_asr_archive_from_account();


-- ============================================
-- RLS
-- Service-role (backend API) bypasses RLS.
-- The webapp authenticated user sees only their
-- account's active reports (future, if exposed).
-- ============================================

alter table account_sites_report enable row level security;

-- Backend (service role) — full access, no policy needed (bypasses RLS).

-- Webapp authenticated users: read their own account's active reports only.
create policy "Users see own active reports"
  on account_sites_report
  for select
  using (
    account_id = (auth.jwt() -> 'app_metadata' ->> 'account_id')::uuid
    and is_archived = false
  );


-- ============================================
-- NEW: questionnaire_answers column
-- Stores the full 23-question answer set per report.
-- Populated with defaults on report creation;
-- overwritten when the user submits edits.
-- ============================================

alter table account_sites_report
  add column if not exists questionnaire_answers jsonb;


-- ============================================
-- NEW: account_report_access_log
-- One row per successful OTP verification.
-- Tracks every visitor (contact match or not).
-- ============================================

create table if not exists account_report_access_log (
  access_id        uuid        primary key default gen_random_uuid(),
  report_id        uuid        references account_sites_report(report_id) on delete set null,
  email            text        not null,
  contact_id       uuid        references contacts(id) on delete set null,  -- null = unknown visitor
  is_known_contact boolean     not null default false,
  accessed_at      timestamptz not null default now()
);

create index if not exists idx_ral_report_id  on account_report_access_log(report_id);
create index if not exists idx_ral_email      on account_report_access_log(email);
create index if not exists idx_ral_contact_id on account_report_access_log(contact_id);

