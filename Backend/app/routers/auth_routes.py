"""Auth endpoints — Supabase OTP flow."""

import logging
from fastapi import APIRouter, HTTPException, status
from app.database import get_supabase, get_supabase_admin
from app.models.schemas import OTPRequest, OTPVerify, AuthResponse

router = APIRouter(prefix="/auth", tags=["auth"])
logger = logging.getLogger(__name__)

ADMIN_DOMAIN = "hrytos.com"


@router.post("/otp/send")
def send_otp(data: OTPRequest):
    """Send OTP to the user's email via Supabase Auth. Open to any email."""
    db = get_supabase()
    try:
        db.auth.sign_in_with_otp({"email": data.email})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send OTP: {str(e)}",
        )
    return {"message": "OTP sent. Check your email."}


@router.post("/otp/verify", response_model=AuthResponse)
def verify_otp(data: OTPVerify):
    """Verify the OTP, return session tokens, and log the access."""
    db = get_supabase()
    try:
        result = db.auth.verify_otp({
            "email": data.email,
            "token": data.token,
            "type": "email",
        })
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"OTP verification failed: {str(e)}",
        )

    session = result.session
    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No session returned. Invalid or expired OTP.",
        )

    user_metadata = result.user.app_metadata if result.user else {}
    email = result.user.email if result.user else ""
    user_id = result.user.id if result.user else ""
    is_admin = (email or "").lower().endswith(f"@{ADMIN_DOMAIN}")

    # ── Account linking ───────────────────────────────────────────────────────
    # If the user arrived via a report link, resolve the account_id from the
    # report and persist it to the user's app_metadata so future logins work.
    account_id = user_metadata.get("account_id")
    if data.report_id and not account_id:
        try:
            admin_db = get_supabase_admin()
            report_row = (
                admin_db.table("account_sites_report")
                .select("account_id")
                .eq("report_id", data.report_id)
                .single()
                .execute()
            )
            if report_row.data and report_row.data.get("account_id"):
                account_id = report_row.data["account_id"]
                # Persist to Supabase auth so it's available on future logins via JWT
                admin_db.auth.admin.update_user_by_id(
                    user_id,
                    {"app_metadata": {"account_id": account_id}},
                )
        except Exception as exc:
            logger.warning("Account linking failed: %s", exc)

    # ── Access logging (non-blocking) ────────────────────────────────────────
    try:
        _log_access(email=email, report_id=data.report_id)
    except Exception as exc:
        # Never fail auth because of a logging error
        logger.warning("Access log insert failed: %s", exc)

    return AuthResponse(
        access_token=session.access_token,
        refresh_token=session.refresh_token,
        user_id=user_id,
        account_id=account_id,
        is_admin=is_admin,
    )


def _log_access(email: str, report_id: str | None) -> None:
    """Look up contact by email and insert a row into account_report_access_log."""
    admin_db = get_supabase_admin()

    # Check if this email belongs to a known contact
    contact_result = (
        admin_db.table("contacts")
        .select("id")
        .eq("email", email)
        .limit(1)
        .execute()
    )
    contact = contact_result.data[0] if contact_result.data else None

    admin_db.table("account_report_access_log").insert({
        "email": email,
        "report_id": report_id,           # None is fine — stored as NULL
        "contact_id": contact["id"] if contact else None,
        "is_known_contact": contact is not None,
    }).execute()
