from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

APP_VERSION = "1.2.0"
API_CONTRACT = "jobia-v1"
TRAINER_MODULE = "bitey-trainer"
GENERAL_MODULE = "bitey-web"
DB_PATH = Path(os.getenv("JOBIA_DB_PATH", "data/jobia.sqlite3"))

app = FastAPI(
    title="JobIA Backend",
    version=APP_VERSION,
    description="Employment intelligence module of Bitey IA Web.",
)

cors_origins = [
    origin.strip()
    for origin in os.getenv("JOBIA_CORS_ORIGINS", "*").split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=False,
    allow_methods=["GET", "PUT", "POST", "OPTIONS"],
    allow_headers=["*"],
)


class Profile(BaseModel):
    email: str = ""
    profession: str = "Informática / IT"
    mode: str = "Remoto"
    aiOpportunities: bool = True
    skills: list[str] = Field(default_factory=list)


class Job(BaseModel):
    id: str
    title: str
    company: str
    location: str
    modality: str
    kind: str
    match: int = Field(ge=0, le=100)
    compensation: str | None = None
    summary: str
    url: str | None = None
    skills: list[str] = Field(default_factory=list)


JOBS: list[Job] = [
    Job(id="jobia-1", title="AI Response Evaluator", company="JobIA Network", location="Brasil", modality="Remoto", kind="Human-in-the-loop", match=94, summary="Evalúa respuestas de IA usando conocimiento técnico y criterios de calidad.", skills=["IA", "Evaluación", "Portugués", "Pensamiento crítico"]),
    Job(id="jobia-2", title="Soporte técnico remoto", company="JobIA Network", location="Brasil", modality="Remoto", kind="Tiempo completo", match=89, summary="Atención y resolución de problemas para usuarios y ambientes de tecnología.", skills=["Soporte", "Windows", "Redes", "Atención al cliente"]),
    Job(id="jobia-3", title="Analista de datos junior", company="JobIA Network", location="Brasil", modality="Híbrido", kind="Contrato", match=84, summary="Análisis, limpieza e interpretación de datos para apoyar decisiones de negocio.", skills=["Python", "SQL", "Excel", "Datos"]),
]


def get_db() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS profiles (
            email TEXT PRIMARY KEY,
            profession TEXT NOT NULL,
            mode TEXT NOT NULL,
            ai_opportunities INTEGER NOT NULL,
            skills TEXT NOT NULL
        )
        """
    )
    return connection


def profile_from_row(row: sqlite3.Row) -> Profile:
    import json

    try:
        skills = json.loads(row["skills"])
        if not isinstance(skills, list):
            skills = []
    except (TypeError, ValueError):
        skills = []
    return Profile(
        email=row["email"],
        profession=row["profession"],
        mode=row["mode"],
        aiOpportunities=bool(row["ai_opportunities"]),
        skills=[str(skill) for skill in skills],
    )


@app.on_event("startup")
def initialize_database() -> None:
    connection = get_db()
    connection.close()


@app.get("/health")
def health() -> dict[str, Any]:
    return {
        "status": "ok",
        "service": "jobia",
        "version": APP_VERSION,
        "contract": API_CONTRACT,
        "persistence": "sqlite",
    }


@app.get("/api/v1/capabilities")
def capabilities() -> dict[str, Any]:
    return {
        "module": "jobia",
        "parent": GENERAL_MODULE,
        "capabilities": ["opportunities", "matching", "profiles", "applications", "alerts"],
        "api_version": API_CONTRACT,
        "trainer": TRAINER_MODULE,
    }


@app.get("/api/v1/module/status")
def module_status() -> dict[str, Any]:
    return {
        "module": "JobIA",
        "parent": "Bitey IA Web",
        "status": "ready",
        "contract": API_CONTRACT,
        "trainer": {"module": TRAINER_MODULE, "role": "training-and-validation"},
    }


@app.get("/api/v1/cognitive/status")
def cognitive_status() -> dict[str, Any]:
    return {
        "status": "delegated",
        "owner": "Bitey IA Web",
        "module": "JobIA",
        "mode": "employment-intelligence",
        "bidirectional": True,
        "inbound": "Bitey IA Web may delegate employment capabilities to JobIA",
        "outbound": "JobIA may request general capabilities from Bitey IA Web",
    }


@app.get("/api/v1/integrations")
def integrations() -> dict[str, Any]:
    return {
        "contract": API_CONTRACT,
        "general_intelligence": {
            "module": GENERAL_MODULE,
            "direction": "bidirectional",
            "purpose": "general reasoning, orchestration, tools, memory and policies",
        },
        "trainer": {
            "module": TRAINER_MODULE,
            "direction": "trainer-to-jobia",
            "purpose": "validated employment capabilities, evaluation, regression and feedback",
            "public_client_api": False,
        },
        "clients": ["JobIA-Web", "JobIA-app"],
    }


@app.get("/api/v1/contract")
def contract() -> dict[str, Any]:
    return {
        "name": API_CONTRACT,
        "module": "JobIA",
        "specialization": "employment-and-work",
        "orchestrator": "Bitey IA Web",
        "trainer": TRAINER_MODULE,
        "clients": ["JobIA-Web", "JobIA-app"],
        "principle": "Bitey IA Web coordinates; JobIA executes employment specialization; Bitey Trainer trains and validates.",
    }


@app.get("/jobs", response_model=list[Job])
def get_jobs(
    q: str = Query(default=""),
    modality: str = Query(default=""),
    location: str = Query(default=""),
    kind: str = Query(default=""),
) -> list[Job]:
    terms = q.strip().lower()
    result = JOBS
    if terms:
        result = [j for j in result if terms in f"{j.title} {j.company} {j.summary} {' '.join(j.skills)}".lower()]
    if modality:
        result = [j for j in result if j.modality.lower() == modality.lower()]
    if location:
        result = [j for j in result if location.lower() in j.location.lower()]
    if kind:
        result = [j for j in result if kind.lower() in j.kind.lower()]
    return result


@app.get("/jobs/{job_id}", response_model=Job)
def get_job(job_id: str) -> Job:
    for job in JOBS:
        if job.id == job_id:
            return job
    raise HTTPException(status_code=404, detail="Opportunity not found")


@app.get("/profile", response_model=Profile)
def get_profile(email: str = Query(default="")) -> Profile:
    normalized_email = email.strip().lower()
    if not normalized_email:
        return Profile()
    connection = get_db()
    try:
        row = connection.execute("SELECT * FROM profiles WHERE email = ?", (normalized_email,)).fetchone()
        return profile_from_row(row) if row else Profile(email=normalized_email)
    finally:
        connection.close()


@app.put("/profile", response_model=Profile)
def save_profile(profile: Profile) -> Profile:
    normalized_email = profile.email.strip().lower()
    if not normalized_email:
        raise HTTPException(status_code=400, detail="email is required")

    import json

    connection = get_db()
    try:
        connection.execute(
            """
            INSERT INTO profiles (email, profession, mode, ai_opportunities, skills)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(email) DO UPDATE SET
                profession = excluded.profession,
                mode = excluded.mode,
                ai_opportunities = excluded.ai_opportunities,
                skills = excluded.skills
            """,
            (
                normalized_email,
                profile.profession,
                profile.mode,
                int(profile.aiOpportunities),
                json.dumps(profile.skills, ensure_ascii=False),
            ),
        )
        connection.commit()
        return profile.model_copy(update={"email": normalized_email})
    finally:
        connection.close()


@app.get("/api/v1/module/manifest")
def manifest() -> dict[str, Any]:
    return {
        "id": "jobia",
        "name": "JobIA",
        "parent_system": GENERAL_MODULE,
        "role": "specialized employment intelligence module",
        "clients": ["JobIA-Web", "JobIA-app"],
        "trainer": TRAINER_MODULE,
        "contract": API_CONTRACT,
        "integration": "bidirectional-with-bitey-web",
        "persistence": "sqlite",
    }
