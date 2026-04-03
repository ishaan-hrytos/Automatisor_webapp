"""Supabase JWT auth dependency for FastAPI."""

from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt
from pydantic import BaseModel
from app.config import get_settings, Settings


class CurrentUser(BaseModel):
    user_id: str
    email: str | None = None
    account_id: str | None = None
    is_admin: bool = False


def _extract_token(request: Request) -> str:
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header",
        )
    return auth.removeprefix("Bearer ").strip()


def get_current_user(
    request: Request,
    settings: Settings = Depends(get_settings),
) -> CurrentUser:
    """Decode Supabase JWT and return the authenticated user."""
    token = _extract_token(request)
    try:
        payload = jwt.decode(
            token,
            settings.supabase_jwt_secret,
            algorithms=["HS256"],
            audience="authenticated",
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    app_metadata = payload.get("app_metadata", {})
    email = payload.get("email") or ""
    return CurrentUser(
        user_id=payload.get("sub", ""),
        email=email,
        account_id=app_metadata.get("account_id"),
        is_admin=email.lower().endswith("@hrytos.com"),
    )


def require_account(user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
    """Enforce that the user has an account_id assigned."""
    if not user.account_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No account associated with this user. Contact support.",
        )
    return user


def require_admin(user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
    """Enforce that the user is a Hrytos admin (@hrytos.com email)."""
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required.",
        )
    return user


def get_optional_user(
    request: Request,
    settings: Settings = Depends(get_settings),
) -> CurrentUser | None:
    """Try to decode the JWT if present; return None for unauthenticated requests."""
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        return None
    token = auth.removeprefix("Bearer ").strip()
    try:
        payload = jwt.decode(
            token,
            settings.supabase_jwt_secret,
            algorithms=["HS256"],
            audience="authenticated",
        )
    except JWTError:
        return None
    app_metadata = payload.get("app_metadata", {})
    email = payload.get("email") or ""
    return CurrentUser(
        user_id=payload.get("sub", ""),
        email=email,
        account_id=app_metadata.get("account_id"),
        is_admin=email.lower().endswith("@hrytos.com"),
    )
