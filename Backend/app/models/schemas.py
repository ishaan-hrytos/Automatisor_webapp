"""Pydantic schemas for request/response validation."""

from __future__ import annotations
from datetime import datetime
from typing import Any
from pydantic import BaseModel, EmailStr, Field


# ── Accounts & Sites ──────────────────────────────────────

class AccountOut(BaseModel):
    id: str
    name: str
    domain: str | None = None
    created_at: datetime


class SiteOut(BaseModel):
    site_id: str
    site_name: str
    site_location: str
    report_id: str


# ── Report ────────────────────────────────────────────────

class ReportSection(BaseModel):
    id: str
    heading: str
    subheading: str
    body: str


class ReportSummary(BaseModel):
    """Lightweight listing — no section bodies."""
    report_id: str
    site_id: str
    site_name: str
    site_location: str
    report_type: str
    solution: str
    ofi_score: int
    ofi_tier: str
    ofi_tier_label: str
    generated_at: str


class ReportFull(BaseModel):
    """Full report with sections."""
    report_id: str
    report_type: str
    solution: str
    account_id: str | None = None
    site_id: str
    site_name: str
    site_location: str
    site_address: str | None = None
    generated_at: str
    ofi_score: int
    ofi_tier: str
    ofi_tier_label: str
    score_confidence: str
    caveat: str
    sections: list[ReportSection]


# ── Questionnaire ─────────────────────────────────────────

class QuestionnaireSubmission(BaseModel):
    """Public questionnaire — no auth required."""
    email: EmailStr
    facility_name: str
    location: str
    floor_area: int | None = None
    facility_type: str | None = None
    headcount: int | None = None
    shift_count: str | None = None
    primary_equipment: str | None = None
    sku_count: str | None = None
    wms_type: str | None = None
    wifi_status: str | None = None
    existing_automation: str | None = None
    biggest_challenge: str | None = None
    throughput_concern: str | None = None
    automation_interest: str | None = None


class QuestionnaireOut(BaseModel):
    id: str
    email: str
    facility_name: str
    status: str
    created_at: datetime


# ── Auth ──────────────────────────────────────────────────

class OTPRequest(BaseModel):
    email: EmailStr


class OTPVerify(BaseModel):
    email: EmailStr
    token: str
    report_id: str | None = None  # optional — logged with the access record


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    user_id: str
    account_id: str | None = None
    is_admin: bool = False


class QuestionnaireUpdate(BaseModel):
    """Payload for saving/updating questionnaire answers for a report."""
    answers: dict[str, Any]


class CreateReportRequest(BaseModel):
    """Admin-only — create a new report row with default questionnaire answers."""
    account_id: str
    site_id: str
    report_metadata: dict[str, Any] = Field(default_factory=dict)
    questionnaire_answers: dict[str, Any] = Field(default_factory=dict)


# ── Admin helpers ─────────────────────────────────────────

class AdminAccountItem(BaseModel):
    account_id: str
    company_name: str


class AdminSiteItem(BaseModel):
    site_id: str
    site_name: str
    site_address: str | None = None
    report_id: str | None = None
    has_answers: bool = False


class PrepareLinksRequest(BaseModel):
    report_ids: list[str]
