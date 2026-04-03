"""Account endpoints — list accounts, sites, for authenticated users."""

from fastapi import APIRouter, Depends, HTTPException, status
from app.auth import CurrentUser, require_account, require_admin
from app.database import get_supabase_admin
from app.models.schemas import AccountOut, AdminAccountItem, AdminSiteItem

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("/me", response_model=AccountOut)
def get_my_account(user: CurrentUser = Depends(require_account)):
    """Get the current user's account details."""
    db = get_supabase_admin()
    result = (
        db.table("accounts")
        .select("*")
        .eq("id", user.account_id)
        .single()
        .execute()
    )
    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found",
        )
    return AccountOut(**result.data)


# ── Admin helpers ─────────────────────────────────────────────────────────────

@router.get("/admin/list", response_model=list[AdminAccountItem])
def admin_list_accounts(user: CurrentUser = Depends(require_admin)):
    """Admin — list accounts that have at least one row in account_sites_report."""
    db = get_supabase_admin()
    # Inner join: only accounts referenced in account_sites_report
    result = (
        db.table("accounts")
        .select("account_id, company_name, account_sites_report!inner(account_id)")
        .order("company_name")
        .execute()
    )
    seen = set()
    items = []
    for r in result.data:
        aid = r["account_id"]
        if aid not in seen:
            seen.add(aid)
            items.append(AdminAccountItem(account_id=aid, company_name=r["company_name"]))
    return items


@router.get("/admin/{account_id}/sites", response_model=list[AdminSiteItem])
def admin_list_sites(account_id: str, user: CurrentUser = Depends(require_admin)):
    """Admin — list sites from account_sites_report for this account.
    Only shows sites that already have a report row (existing or ready to link).
    """
    db = get_supabase_admin()
    result = (
        db.table("account_sites_report")
        .select("report_id, site_id, report_metadata, questionnaire_answers")
        .eq("account_id", account_id)
        .eq("is_archived", False)
        .execute()
    )
    items = []
    for r in result.data:
        meta = r.get("report_metadata") or {}
        address = (
            meta.get("site_location_full_address")
            or meta.get("site_location")
            or None
        )
        items.append(AdminSiteItem(
            site_id=r["site_id"],
            site_name=meta.get("site_name") or r["site_id"],
            site_address=address,
            report_id=r["report_id"],
            has_answers=bool(r.get("questionnaire_answers")),
        ))
    return items
