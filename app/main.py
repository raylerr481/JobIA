from __future__ import annotations

from typing import Any
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

APP_VERSION = "1.0.0"

app = FastAPI(
    title="JobIA Backend",
    version=APP_VERSION,
    description="Employment intelligence module of Bitey IA Web.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
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

PROFILES: dict[str, Profile] = {}


@app.get("/health")
def health() -> dict[str, Any]:
    return {"status": "ok", "service": "jobia", "version": APP_VERSION}


@app.get("/api/v1/capabilities")
def capabilities() -> dict[str, Any]:
    return {
        "module": "jobia",
        "parent": "bitey-web",
        "capabilities": ["opportunities", "matching", "profiles", "applications", "alerts"],
        "api_version": "jobia-v1",
    }


@app.get("/api/v1/module/status")
def module_status() -> dict[str, Any]:
    return {"module": "JobIA", "parent": "Bitey IA Web", "status": "ready", "contract": "jobia-v1"}


@app.get("/api/v1/cognitive/status")
def cognitive_status() -> dict[str, Any]:
    return {"status": "delegated", "owner": "Bitey IA Web", "module": "JobIA", "mode": "employment-intelligence"}


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
    return PROFILES.get(email, Profile(email=email))


@app.put("/profile", response_model=Profile)
def save_profile(profile: Profile) -> Profile:
    if profile.email:
        PROFILES[profile.email] = profile
    return profile


@app.get("/api/v1/module/manifest")
def manifest() -> dict[str, Any]:
    return {
        "id": "jobia",
        "name": "JobIA",
        "parent_system": "bitey-web",
        "role": "specialized employment intelligence module",
        "clients": ["JobIA-Web", "JobIA-app"],
        "trainer": "bitey-trainer",
        "contract": "jobia-v1",
    }
