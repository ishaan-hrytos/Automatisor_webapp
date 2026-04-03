"""Reports endpoints — authenticated access to account reports."""

from fastapi import APIRouter, Depends, HTTPException, status
from app.auth import CurrentUser, get_current_user, get_optional_user, require_account, require_admin
from app.database import get_supabase_admin
from app.models.schemas import CreateReportRequest, PrepareLinksRequest, QuestionnaireUpdate, ReportFull, ReportSection, ReportSummary, SiteOut

router = APIRouter(prefix="/reports", tags=["reports"])

FREE_SECTION_IDS = {"operational_profile"}

# ── Default questionnaire answers (spec-compliant) ────────────────────────────
_DEFAULT_ANSWERS: dict = {
    "aisle_width": "10_15ft",
    "floor_condition": "mixed",
    "temp_exposure": "ambient_only",
    "travel_distance": "250_500ft",
    "load_format": "pallets",
    "load_weight": "220_660lbs",
    "wifi_state": "unknown",
    "deployment_constraints": [],
    "primary_mhe_type": "unknown",
    "route_count": "unknown",
    "ceiling_clearance": "unknown",
    "doorway_width": "unknown",
    "site_layout": "single_building",
    "charging_feasibility": "unknown",
    "payback_expectation": "unknown",
    # Fields with no default (absent = no signal):
    # transport_ftes, moves_per_shift, transport_overtime, transport_attrition,
    # lease_remaining, capex_cycle, competitor_automation, annual_transport_labour_cost
}


def _site_location(meta: dict) -> str:
    """Report metadata may use site_location or site_full_address."""
    return meta.get("site_location") or meta.get("site_full_address", "")


def _extract_report_summary(row: dict) -> ReportSummary:
    meta = row["report_metadata"]
    return ReportSummary(
        report_id=row["report_id"],
        site_id=row["site_id"],
        site_name=meta["site_name"],
        site_location=_site_location(meta),
        report_type=meta["report_type"],
        solution=meta["solution"],
        ofi_score=meta["ofi_score"],
        ofi_tier=meta["ofi_tier"],
        ofi_tier_label=meta["ofi_tier_label"],
        generated_at=meta["generated_at"],
    )


def _extract_report_full(row: dict, unlocked: bool = False) -> ReportFull:
    meta = row["report_metadata"]
    all_sections = [ReportSection(**s) for s in meta.get("sections", [])]

    if unlocked:
        sections = all_sections
    else:
        # Only return free sections fully, gated sections get heading/subheading only
        sections = []
        for s in all_sections:
            if s.id in FREE_SECTION_IDS:
                sections.append(s)
            else:
                sections.append(ReportSection(
                    id=s.id,
                    heading=s.heading,
                    subheading=s.subheading,
                    body="",  # gated — no body
                ))

    return ReportFull(
        report_id=row["report_id"],
        report_type=meta["report_type"],
        solution=meta["solution"],
        account_id=row.get("account_id"),
        site_id=row["site_id"],
        site_name=meta["site_name"],
        site_location=_site_location(meta),
        site_address=meta.get("site_location_full_address") or None,
        generated_at=meta["generated_at"],
        ofi_score=meta["ofi_score"],
        ofi_tier=meta["ofi_tier"],
        ofi_tier_label=meta["ofi_tier_label"],
        score_confidence=meta.get("score_confidence", ""),
        caveat=meta.get("caveat", ""),
        sections=sections,
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_report(
    body: CreateReportRequest,
    user: CurrentUser = Depends(require_admin),
):
    """Admin only — create a new report row with questionnaire_answers pre-filled."""
    db = get_supabase_admin()

    # Verify account exists
    acct = (
        db.table("accounts")
        .select("account_id")
        .eq("account_id", body.account_id)
        .single()
        .execute()
    )
    if not acct.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")

    # Verify site exists and belongs to the account
    site = (
        db.table("account_sites")
        .select("site_id")
        .eq("site_id", body.site_id)
        .eq("account_id", body.account_id)
        .single()
        .execute()
    )
    if not site.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site not found for this account")

    result = (
        db.table("account_sites_report")
        .insert({
            "account_id": body.account_id,
            "site_id": body.site_id,
            "report_metadata": body.report_metadata,
            "questionnaire_answers": body.questionnaire_answers,
        })
        .execute()
    )

    row = result.data[0] if result.data else {}
    return {"report_id": row.get("report_id"), "status": "created"}


@router.post("/prepare")
def prepare_report_links(
    body: PrepareLinksRequest,
    user: CurrentUser = Depends(require_admin),
):
    """Admin only — seed default questionnaire answers for reports that don't
    have any yet, then return the report details ready for link sharing."""
    db = get_supabase_admin()
    output = []
    for report_id in body.report_ids:
        row = (
            db.table("account_sites_report")
            .select("report_id, site_id, report_metadata, questionnaire_answers")
            .eq("report_id", report_id)
            .eq("is_archived", False)
            .single()
            .execute()
        )
        if not row.data:
            continue
        meta = row.data.get("report_metadata") or {}
        # Seed defaults if answers are absent
        if not row.data.get("questionnaire_answers"):
            answers = dict(_DEFAULT_ANSWERS)
            # Pre-fill site context fields from metadata
            answers["company_name"] = meta.get("site_name", "")
            answers["site_location"] = (
                meta.get("site_location_full_address")
                or meta.get("site_location", "")
            )
            db.table("account_sites_report").update(
                {"questionnaire_answers": answers}
            ).eq("report_id", report_id).execute()
        output.append({
            "report_id": report_id,
            "site_name": meta.get("site_name", ""),
            "site_address": (
                meta.get("site_location_full_address")
                or meta.get("site_location", "")
            ),
        })
    return output


@router.get("/", response_model=list[ReportSummary])
def list_reports(user: CurrentUser = Depends(get_current_user)):
    db = get_supabase_admin()
    query = (
        db.table("account_sites_report")
        .select("report_id, site_id, report_metadata")
        .eq("is_archived", False)
    )
    # Admins see all reports; regular users only see their account's reports
    if not user.is_admin:
        if not user.account_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No account associated with this user. Contact support.",
            )
        query = query.eq("account_id", user.account_id)
    result = query.execute()
    return [_extract_report_summary(r) for r in result.data]


@router.get("/sites", response_model=list[SiteOut])
def list_sites(user: CurrentUser = Depends(require_account)):
    """List all sites (from reports) for the account — used for the dropdown."""
    db = get_supabase_admin()
    result = (
        db.table("account_sites_report")
        .select("report_id, site_id, report_metadata")
        .eq("account_id", user.account_id)
        .eq("is_archived", False)
        .execute()
    )
    return [
        SiteOut(
            site_id=r["site_id"],
            site_name=r["report_metadata"]["site_name"],
            site_location=_site_location(r["report_metadata"]),
            report_id=r["report_id"],
        )
        for r in result.data
    ]


@router.get("/by-account/{account_id}")
def list_reports_for_account(account_id: str, user: CurrentUser | None = Depends(get_optional_user)):
    """All reports for an account — used by the site-switcher dropdown.
    Public: anyone with the report link can see the site list for that account."""
    db = get_supabase_admin()
    # Authenticated non-admin users are still restricted to their own account
    if user and not user.is_admin and user.account_id and user.account_id != account_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    result = (
        db.table("account_sites_report")
        .select("report_id, site_id, report_metadata")
        .eq("account_id", account_id)
        .eq("is_archived", False)
        .execute()
    )
    return [
        {
            "report_id": r["report_id"],
            "site_id": r["site_id"],
            "site_name": r["report_metadata"].get("site_name", ""),
            "site_address": (
                r["report_metadata"].get("site_location_full_address")
                or r["report_metadata"].get("site_location", "")
            ),
        }
        for r in result.data
    ]


@router.get("/{report_id}", response_model=ReportFull)
def get_report(report_id: str, user: CurrentUser | None = Depends(get_optional_user)):
    """Get a report. Public endpoint — unauthenticated visitors get locked sections.
    Authenticated users who belong to the account (or admins) get fully unlocked content."""
    db = get_supabase_admin()
    result = (
        db.table("account_sites_report")
        .select("report_id, site_id, account_id, report_metadata")
        .eq("report_id", report_id)
        .eq("is_archived", False)
        .single()
        .execute()
    )
    if not result.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")

    # Unlock for any authenticated user — signing in is the gate.
    # Admins and account-matched users are always unlocked; any other
    # signed-in user (e.g. new sign-ups via the report page) also gets full access.
    unlocked = user is not None
    return _extract_report_full(result.data, unlocked=unlocked)


@router.get("/{report_id}/sections", response_model=list[ReportSection])
def get_report_sections(report_id: str, user: CurrentUser = Depends(get_current_user)):
    """Get all sections for a report."""
    db = get_supabase_admin()
    result = (
        db.table("account_sites_report")
        .select("report_id, account_id, report_metadata")
        .eq("report_id", report_id)
        .eq("is_archived", False)
        .single()
        .execute()
    )
    if not result.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")

    meta = result.data["report_metadata"]
    return [ReportSection(**s) for s in meta.get("sections", [])]


@router.get("/{report_id}/sections/{section_id}", response_model=ReportSection)
def get_report_section(
    report_id: str,
    section_id: str,
    user: CurrentUser = Depends(get_current_user),
):
    """Get a single section by ID."""
    db = get_supabase_admin()
    result = (
        db.table("account_sites_report")
        .select("report_id, account_id, report_metadata")
        .eq("report_id", report_id)
        .eq("is_archived", False)
        .single()
        .execute()
    )
    if not result.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")

    meta = result.data["report_metadata"]
    for s in meta.get("sections", []):
        if s["id"] == section_id:
            return ReportSection(**s)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Section not found")


@router.get("/{report_id}/questionnaire")
def get_questionnaire(report_id: str, user: CurrentUser = Depends(get_current_user)):
    """Return the current questionnaire answers for a report."""
    db = get_supabase_admin()
    result = (
        db.table("account_sites_report")
        .select("report_id, site_id, report_metadata, questionnaire_answers")
        .eq("report_id", report_id)
        .eq("is_archived", False)
        .single()
        .execute()
    )
    if not result.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")

    meta = result.data.get("report_metadata") or {}
    return {
        "report_id": report_id,
        "site_id": result.data.get("site_id"),
        "site_name": meta.get("site_name") or "",
        "site_location": _site_location(meta),
        "site_address": meta.get("site_location_full_address") or None,
        "answers": result.data.get("questionnaire_answers") or {},
    }


@router.patch("/{report_id}/questionnaire")
def update_questionnaire(
    report_id: str,
    body: QuestionnaireUpdate,
    user: CurrentUser = Depends(get_current_user),
):
    """Save or overwrite questionnaire answers for a report."""
    db = get_supabase_admin()

    # Verify report exists and is active
    check = (
        db.table("account_sites_report")
        .select("report_id")
        .eq("report_id", report_id)
        .eq("is_archived", False)
        .single()
        .execute()
    )
    if not check.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")

    db.table("account_sites_report").update(
        {"questionnaire_answers": body.answers}
    ).eq("report_id", report_id).execute()

    return {"report_id": report_id, "status": "saved"}
