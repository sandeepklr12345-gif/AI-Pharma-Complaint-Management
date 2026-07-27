from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.routers import upload, analyze, complaints

# Creates tables on startup if they don't exist yet.
# Fine for a take-home; swap for Alembic migrations in a real production app.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AIVOA Complaint Management API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)
app.include_router(analyze.router)
app.include_router(complaints.router)


@app.get("/api/health")
def health_check():
    return {"status": "ok"}
