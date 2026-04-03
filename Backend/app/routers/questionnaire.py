"""Questionnaire endpoints — public, no auth required."""

from fastapi import APIRouter, HTTPException, status
from app.database import get_supabase_admin
from app.models.schemas import QuestionnaireSubmission, QuestionnaireOut

router = APIRouter(prefix="/questionnaire", tags=["questionnaire"])


@router.post("/", response_model=QuestionnaireOut, status_code=status.HTTP_201_CREATED)
def submit_questionnaire(data: QuestionnaireSubmission):
    """
    Public endpoint — user fills out questionnaire from the webapp.
    No auth required. Data is saved for manual/automated report generation later.
    """
    db = get_supabase_admin()

    payload = {
        "email": data.email,
        "facility_name": data.facility_name,
        "location": data.location,
        "answers": data.model_dump(exclude={"email", "facility_name", "location"}),
        "status": "pending",
    }

    result = db.table("questionnaires").insert(payload).execute()

    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save questionnaire",
        )

    row = result.data[0]
    return QuestionnaireOut(
        id=row["id"],
        email=row["email"],
        facility_name=row["facility_name"],
        status=row["status"],
        created_at=row["created_at"],
    )


@router.get("/{questionnaire_id}", response_model=QuestionnaireOut)
def get_questionnaire_status(questionnaire_id: str):
    """Check the status of a submitted questionnaire (public, by ID)."""
    db = get_supabase_admin()
    result = (
        db.table("questionnaires")
        .select("id, email, facility_name, status, created_at")
        .eq("id", questionnaire_id)
        .single()
        .execute()
    )

    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Questionnaire not found",
        )

    return QuestionnaireOut(**result.data)
