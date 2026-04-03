from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.routers import reports, accounts, questionnaire, auth_routes

app = FastAPI(
    title="AutomatiSOR API",
    description="Backend API for warehouse automation assessment reports",
    version="0.1.0",
)

settings = get_settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(accounts.router)
app.include_router(reports.router)
app.include_router(questionnaire.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
