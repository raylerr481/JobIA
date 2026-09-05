from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

APP_VERSION = "1.3.0"
API_CONTRACT = "jobia-v1"
TRAINER_MODULE = "bitey-trainer"
GENERAL_MODULE = "bitey-web"
DB_PATH = Path(os.getenv("JOBIA_DB_PATH", "data/jobia.sqlite3"))

app = FastAPI(title="JobIA Backend", version=APP_VERSION, description="Employment intelligence module of Bitey IA Web.")

cors_origins = [origin.strip() for origin in os.getenv("JOBIA_CORS_ORIGINS", "*").split(",") if origin.strip()]
app.add_middleware(CORSMiddleware, allow_origins=cors_origins, allow_credentials=False, allow_methods=["GET", "PUT", "POST", "OPTIONS"], allow_headers=["*"])


class Profile(BaseModel):
    email: str = ""
    profession: str = "Informática / IT"
    mode: str = "Remoto"
    aiOpportunities: bool = True
    skills: list[str] = Field(default_factory=list)


class MatchReason(BaseModel):
    skill: str
    matched: bool


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
    match_reasons: list[MatchReason] = Field(default_factory=list)
    strengths: list[str] = Field(default_factory=list)
    gaps: list[str] = Field(default_factory=list)


class PreparationRequest(BaseModel):
    job_id: str
    profile: Profile


class ApplicationDrafts(BaseModel):
    cvSummary: str
    coverLetter: str
    answers: str
    notes: str


JOBS: list[Job] = [
    Job(id="jobia-1", title="AI Response Evaluator", company="JobIA Network", location="Brasil", modality="Remoto", kind="Human-in-the-loop", match=94, summary="Evalúa respuestas de IA usando conocimiento técnico y criterios de calidad.", skills=["IA", "Evaluación", "Portugués", "Pensamiento crítico"]),
    Job(id="jobia-2", title="Soporte técnico remoto", company="JobIA Network", location="Brasil", modality="Remoto", kind="Tiempo completo", match=89, summary="Atención y resolución de problemas para usuarios y ambientes de tecnología.", skills=["Soporte", "Windows", "Redes", "Atención al cliente"]),
    Job(id="jobia-3", title="Analista de datos junior", company="JobIA Network", location="Brasil", modality="Híbrido", kind="Contrato", match=84, summary="Análisis, limpieza e interpretación de datos para apoyar decisiones de negocio.", skills=["Python", "SQL", "Excel", "Datos"]),
]


def normalize(value: str) -> str:
    import unicodedata
    return "".join(ch for ch in unicodedata.normalize("NFD", value) if unicodedata.category(ch) != "Mn").lower().strip()


def overlaps(a: str, b: str) -> bool:
    aa, bb = normalize(a), normalize(b)
    if aa == bb or aa in bb or bb in aa:
        return True
    at = {x for x in aa.replace("+", " + ").replace("#", " # ").replace(".", " . ").split() if len(x) > 2}
    bt = {x for x in bb.replace("+", " + ").replace("#", " # ").replace(".", " . ").split() if len(x) > 2}
    return bool(at & bt)


def calculate_match(job: Job, profile: Profile) -> tuple[int, list[MatchReason], list[str], list[str]]:
    required = job.skills
    owned = profile.skills
    reasons = [MatchReason(skill=skill, matched=any(overlaps(item, skill) for item in owned)) for skill in required]
    strengths = [r.skill for r in reasons if r.matched]
    gaps = [r.skill for r in reasons if not r.matched]
    skill_score = (len(strengths) / len(required)) * 70 if required else 50
    modality_score = 15 if normalize(job.modality) == normalize(profile.mode) else 5
    profession = normalize(profile.profession.split("/")[0]) if profile.profession else ""
    profession_score = 15 if profession and profession in normalize(job.title + " " + job.summary) else 8
    score = max(0, min(100, round(skill_score + modality_score + profession_score)))
    return score, reasons, strengths, gaps


def enrich_job(job: Job, profile: Profile) -> Job:
    score, reasons, strengths, gaps = calculate_match(job, profile)
    return job.model_copy(update={"match": score, "match_reasons": reasons, "strengths": strengths, "gaps": gaps})


def get_db() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("""CREATE TABLE IF NOT EXISTS profiles (email TEXT PRIMARY KEY, profession TEXT NOT NULL, mode TEXT NOT NULL, ai_opportunities INTEGER NOT NULL, skills TEXT NOT NULL)""")
    return connection


def profile_from_row(row: sqlite3.Row) -> Profile:
    try:
        skills = json.loads(row["skills"])
        if not isinstance(skills, list): skills = []
    except (TypeError, ValueError):
        skills = []
    return Profile(email=row["email"], profession=row["profession"], mode=row["mode"], aiOpportunities=bool(row["ai_opportunities"]), skills=[str(skill) for skill in skills])


def load_profile(email: str) -> Profile:
    normalized_email = email.strip().lower()
    if not normalized_email:
        return Profile()
    connection = get_db()
    try:
        row = connection.execute("SELECT * FROM profiles WHERE email = ?", (normalized_email,)).fetchone()
        return profile_from_row(row) if row else Profile(email=normalized_email)
    finally:
        connection.close()


def prepare_application(job: Job, profile: Profile) -> ApplicationDrafts:
    skills = [skill.strip() for skill in profile.skills if skill.strip()]
    skill_text = ", ".join(skills) if skills else "habilidades técnicas y profesionales relevantes"
    profession = profile.profession or "profesional"
    location = profile.mode or "la modalidad indicada"
    matched = [required for required in job.skills if any(overlaps(have, required) for have in skills)]
    match_text = f" Entre mis fortalezas destacan {', '.join(matched)}." if matched else ""
    return ApplicationDrafts(
        cvSummary=f"{profession} con experiencia orientada a resultados y conocimientos en {skill_text}. Interesado/a en oportunidades {location.lower()} y en aplicar capacidades técnicas, resolución de problemas y aprendizaje continuo.{match_text}",
        coverLetter=f"Hola,\n\nMe interesa la oportunidad de {job.title} en {job.company}. Mi perfil como {profession.lower()} y mis conocimientos en {skill_text} me permiten aportar una combinación de capacidad técnica, análisis y orientación a resultados.\n\nLa posición me resulta especialmente atractiva por su enfoque en {job.kind.lower()} y por la posibilidad de contribuir en un entorno donde pueda seguir desarrollando mis competencias.{match_text}\n\nQuedo disponible para conversar sobre mi experiencia y sobre cómo puedo contribuir al equipo.\n\nSaludos,\n{profile.email or 'Candidato/a'}",
        answers=f"Motivación: Me interesa {job.title} porque conecta mi experiencia como {profession.lower()} con la posibilidad de aportar valor en {job.company}.\n\nFortalezas relevantes: {skill_text}.{chr(10) + chr(10) + 'Coincidencias directas: ' + ', '.join(matched) + '.' if matched else ''}\n\nDisponibilidad: {location}.",
        notes="Borrador generado por JobIA Backend. Revisar datos, requisitos, experiencia y condiciones antes de autorizar cualquier acción externa.",
    )


@app.on_event("startup")
def initialize_database() -> None:
    connection = get_db()
    connection.close()


@app.get("/health")
def health() -> dict[str, Any]:
    return {"status": "ok", "service": "jobia", "version": APP_VERSION, "contract": API_CONTRACT, "persistence": "sqlite"}


@app.get("/api/v1/capabilities")
def capabilities() -> dict[str, Any]:
    return {"module": "jobia", "parent": GENERAL_MODULE, "capabilities": ["opportunities", "matching", "profiles", "applications", "alerts"], "api_version": API_CONTRACT, "trainer": TRAINER_MODULE}


@app.get("/api/v1/module/status")
def module_status() -> dict[str, Any]:
    return {"module": "JobIA", "parent": "Bitey IA Web", "status": "ready", "contract": API_CONTRACT, "trainer": {"module": TRAINER_MODULE, "role": "training-and-validation"}}


@app.get("/api/v1/cognitive/status")
def cognitive_status() -> dict[str, Any]:
    return {"status": "delegated", "owner": "Bitey IA Web", "module": "JobIA", "mode": "employment-intelligence", "bidirectional": True, "inbound": "Bitey IA Web may delegate employment capabilities to JobIA", "outbound": "JobIA may request general capabilities from Bitey IA Web"}


@app.get("/api/v1/integrations")
def integrations() -> dict[str, Any]:
    return {"contract": API_CONTRACT, "general_intelligence": {"module": GENERAL_MODULE, "direction": "bidirectional", "purpose": "general reasoning, orchestration, tools, memory and policies"}, "trainer": {"module": TRAINER_MODULE, "direction": "trainer-to-jobia", "purpose": "validated employment capabilities, evaluation, regression and feedback", "public_client_api": False}, "clients": ["JobIA-Web", "JobIA-app"]}


@app.get("/api/v1/contract")
def contract() -> dict[str, Any]:
    return {"name": API_CONTRACT, "module": "JobIA", "specialization": "employment-and-work", "orchestrator": "Bitey IA Web", "trainer": TRAINER_MODULE, "clients": ["JobIA-Web", "JobIA-app"], "principle": "Bitey IA Web coordinates; JobIA executes employment specialization; Bitey Trainer trains and validates."}


@app.get("/jobs", response_model=list[Job])
def get_jobs(q: str = Query(default=""), modality: str = Query(default=""), location: str = Query(default=""), kind: str = Query(default=""), email: str = Query(default="")) -> list[Job]:
    terms = q.strip().lower()
    result = JOBS
    if terms: result = [j for j in result if terms in f"{j.title} {j.company} {j.summary} {' '.join(j.skills)}".lower()]
    if modality: result = [j for j in result if j.modality.lower() == modality.lower()]
    if location: result = [j for j in result if location.lower() in j.location.lower()]
    if kind: result = [j for j in result if kind.lower() in j.kind.lower()]
    profile = load_profile(email)
    return sorted((enrich_job(job, profile) for job in result), key=lambda job: job.match, reverse=True)


@app.get("/jobs/{job_id}", response_model=Job)
def get_job(job_id: str, email: str = Query(default="")) -> Job:
    for job in JOBS:
        if job.id == job_id: return enrich_job(job, load_profile(email))
    raise HTTPException(status_code=404, detail="Opportunity not found")


@app.get("/profile", response_model=Profile)
def get_profile(email: str = Query(default="")) -> Profile:
    normalized_email = email.strip().lower()
    if not normalized_email: return Profile()
    connection = get_db()
    try:
        row = connection.execute("SELECT * FROM profiles WHERE email = ?", (normalized_email,)).fetchone()
        if row is None: raise HTTPException(status_code=404, detail="Profile not found")
        return profile_from_row(row)
    finally:
        connection.close()


@app.put("/profile", response_model=Profile)
def save_profile(profile: Profile) -> Profile:
    normalized_email = profile.email.strip().lower()
    if not normalized_email: raise HTTPException(status_code=400, detail="email is required")
    connection = get_db()
    try:
        connection.execute("""INSERT INTO profiles (email, profession, mode, ai_opportunities, skills) VALUES (?, ?, ?, ?, ?) ON CONFLICT(email) DO UPDATE SET profession = excluded.profession, mode = excluded.mode, ai_opportunities = excluded.ai_opportunities, skills = excluded.skills""", (normalized_email, profile.profession, profile.mode, int(profile.aiOpportunities), json.dumps(profile.skills, ensure_ascii=False)))
        connection.commit()
        return profile.model_copy(update={"email": normalized_email})
    finally:
        connection.close()


@app.post("/applications/prepare", response_model=ApplicationDrafts)
def prepare_application_endpoint(request: PreparationRequest) -> ApplicationDrafts:
    job = next((item for item in JOBS if item.id == request.job_id), None)
    if job is None: raise HTTPException(status_code=404, detail="Opportunity not found")
    return prepare_application(job, request.profile)


@app.get("/api/v1/module/manifest")
def manifest() -> dict[str, Any]:
    return {"id": "jobia", "name": "JobIA", "parent_system": GENERAL_MODULE, "role": "specialized employment intelligence module", "clients": ["JobIA-Web", "JobIA-app"], "trainer": TRAINER_MODULE, "contract": API_CONTRACT, "integration": "bidirectional-with-bitey-web", "persistence": "sqlite"}
