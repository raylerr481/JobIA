from __future__ import annotations

import json
import os
import re
import sqlite3
import unicodedata
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.capability_contract import CONTRACT, DelegationRequest, handle_delegation

APP_VERSION = "1.4.1"
API_CONTRACT = CONTRACT
TRAINER_MODULE = "bitey-trainer"
PARENT_MODULE = "bitey"
HOST_CHANNEL = "bitey-web"
DB_PATH = Path(os.getenv("JOBIA_DB_PATH", "data/jobia.sqlite3"))

app = FastAPI(
    title="JobIA Backend",
    version=APP_VERSION,
    description="Employment intelligence module of Bitey IA, exposed through JobIA web and Android channels.",
)
cors_origins = [origin.strip() for origin in os.getenv("JOBIA_CORS_ORIGINS", "*").split(",") if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=False,
    allow_methods=["GET", "PUT", "POST", "OPTIONS"],
    allow_headers=["*"],
)


class Profile(BaseModel):
    email: str = ""
    profession: str = "IT / Computer Science"
    mode: str = "Remote"
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
    Job(id="jobia-1", title="AI Response Evaluator", company="JobIA Network", location="Brazil", modality="Remote", kind="Human-in-the-loop", match=94, summary="Evaluate AI responses using technical knowledge and quality criteria.", skills=["AI", "Evaluation", "Portuguese", "Critical thinking"]),
    Job(id="jobia-2", title="Remote Technical Support Specialist", company="JobIA Network", location="Brazil", modality="Remote", kind="Full-time", match=89, summary="Provide technical support and resolve issues for users and technology environments.", skills=["Support", "Windows", "Networking", "Customer service"]),
    Job(id="jobia-remote-python", title="Python Automation Developer", company="JobIA Network", location="Brazil", modality="Remote", kind="Contract", match=91, summary="Build Python automation, integrations, data workflows, and internal tools for remote teams.", skills=["Python", "Automation", "APIs", "Data analysis"]),
    Job(id="jobia-3", title="Junior Data Analyst", company="JobIA Network", location="Brazil", modality="Hybrid", kind="Contract", match=84, summary="Analyze, clean, and interpret data to support business decisions.", skills=["Python", "SQL", "Excel", "Data analysis"]),
]


def normalize(value: str) -> str:
    return "".join(ch for ch in unicodedata.normalize("NFD", value) if unicodedata.category(ch) != "Mn").lower().strip()


def overlaps(first: str, second: str) -> bool:
    a, b = normalize(first), normalize(second)
    if a == b or a in b or b in a:
        return True
    tokenize = lambda value: {token for token in value.replace("+", " + ").replace("#", " # ").replace(".", " . ").split() if len(token) > 2}
    return bool(tokenize(a) & tokenize(b))


def calculate_match(job: Job, profile: Profile):
    reasons = [MatchReason(skill=skill, matched=any(overlaps(owned, skill) for owned in profile.skills)) for skill in job.skills]
    strengths = [r.skill for r in reasons if r.matched]
    gaps = [r.skill for r in reasons if not r.matched]
    skill_score = (len(strengths) / len(job.skills)) * 70 if job.skills else 50
    modality_score = 15 if normalize(job.modality) == normalize(profile.mode) else 5
    profession = normalize(profile.profession.split("/")[0]) if profile.profession else ""
    profession_score = 15 if profession and profession in normalize(job.title + " " + job.summary) else 8
    return max(0, min(100, round(skill_score + modality_score + profession_score))), reasons, strengths, gaps


def enrich_job(job: Job, profile: Profile) -> Job:
    score, reasons, strengths, gaps = calculate_match(job, profile)
    return job.model_copy(update={"match": score, "match_reasons": reasons, "strengths": strengths, "gaps": gaps})


def get_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("CREATE TABLE IF NOT EXISTS profiles (email TEXT PRIMARY KEY, profession TEXT NOT NULL, mode TEXT NOT NULL, ai_opportunities INTEGER NOT NULL, skills TEXT NOT NULL)")
    return connection


def profile_from_row(row):
    if row is None:
        return Profile()
    try:
        skills = json.loads(row["skills"])
        skills = skills if isinstance(skills, list) else []
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


def resolve_profile(request: DelegationRequest) -> Profile | None:
    candidates = []
    user_id = request.context.user_id.strip()
    if "@" in user_id:
        candidates.append(user_id)
    email_match = re.search(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", request.message, re.I)
    if email_match:
        candidates.append(email_match.group(0))
    for candidate in candidates:
        profile = load_profile(candidate)
        if profile.email and (profile.skills or profile.profession or profile.mode):
            return profile
    return None


def resolve_job_identifier(message: str) -> Job | None:
    text = normalize(message)
    for job in JOBS:
        if normalize(job.id) in text:
            return job
    numeric = re.search(r"\b(?:jobia[- ]?)?(\d+)\b", text)
    if numeric:
        candidate = f"jobia-{numeric.group(1)}"
        job = next((item for item in JOBS if item.id == candidate), None)
        if job:
            return job
    for job in JOBS:
        if normalize(job.title) in text:
            return job
    return None


def prepare_application(job: Job, profile: Profile) -> ApplicationDrafts:
    skills = [skill.strip() for skill in profile.skills if skill.strip()]
    skill_text = ", ".join(skills) if skills else "relevant technical and professional skills"
    profession = profile.profession or "professional"
    modality = profile.mode or "the specified work arrangement"
    matched = [required for required in job.skills if any(overlaps(owned, required) for owned in skills)]
    match_text = f" My strengths include {', '.join(matched)}." if matched else ""
    return ApplicationDrafts(
        cvSummary=f"{profession} with results-oriented experience and knowledge in {skill_text}. Interested in {modality.lower()} opportunities and applying technical skills, problem solving, and continuous learning.{match_text}",
        coverLetter=f"Hello,\n\nI am interested in the {job.title} opportunity at {job.company}. My profile as a {profession.lower()} and my knowledge of {skill_text} allow me to contribute technical capability, analysis, and results orientation.\n\nI would be glad to discuss my experience and how I can contribute to the team.\n\nRegards,\n{profile.email or 'Candidate'}",
        answers=f"Motivation: I am interested in {job.title} because it connects my experience as a {profession.lower()} with the opportunity to create value at {job.company}.\n\nRelevant strengths: {skill_text}." + (f"\n\nDirect matches: {', '.join(matched)}." if matched else "") + f"\n\nAvailability: {modality}.",
        notes="Draft generated by JobIA Backend. Review personal data, requirements, experience, and conditions before authorizing any external action.",
    )


def delegated_intent(message: str) -> str | None:
    text = normalize(message)
    if any(term in text for term in ("curriculum", "cv", "carta de presentacion", "postulacion", "aplicacion", "application")):
        return "application_preparation"
    if any(term in text for term in ("encaja conmigo", "mejor trabajo para mi", "mejores trabajos para mi", "matching", "match")):
        return "profile_matching"
    if any(term in text for term in ("buscame trabajo", "busca trabajo", "buscar trabajo", "vacante", "vacantes", "empleo", "trabajo remoto", "trabajos remotos", "oportunidades")):
        return "opportunity_search"
    return None


def delegated_filters(message: str) -> tuple[str, str, list[str]]:
    text = normalize(message)
    modality = "Remote" if any(term in text for term in ("remoto", "remota", "remote")) else ""
    known_skills = sorted({skill for job in JOBS for skill in job.skills}, key=len, reverse=True)
    requested_skills = [skill for skill in known_skills if normalize(skill) in text]
    removable = ("buscame", "busca", "buscar", "trabajo", "trabajos", "empleo", "empleos", "remoto", "remota", "remote", "vacante", "vacantes", "oportunidades", "por favor", "de", "para", "con")
    query = text
    for word in removable:
        query = query.replace(word, " ")
    for skill in requested_skills:
        query = query.replace(normalize(skill), " ")
    return " ".join(query.split()), modality, requested_skills


def execute_delegation(request: DelegationRequest) -> dict[str, Any]:
    intent = delegated_intent(request.message)
    base = handle_delegation(request)
    if intent == "opportunity_search":
        query, modality, requested_skills = delegated_filters(request.message)
        profile = resolve_profile(request) or Profile()
        def matches(job: Job) -> bool:
            if modality and normalize(job.modality) != normalize(modality):
                return False
            if requested_skills and not any(any(overlaps(requested, skill) for skill in job.skills) for requested in requested_skills):
                return False
            if query and query not in normalize(f"{job.title} {job.summary} {' '.join(job.skills)}"):
                return False
            return True
        result = sorted((enrich_job(job, profile) for job in JOBS if matches(job)), key=lambda job: job.match, reverse=True)
        return {**base, "execution_status": "completed", "result_type": "opportunities", "result": {"count": len(result), "filters": {"modality": modality or None, "skills": requested_skills, "query": query or None}, "jobs": [job.model_dump() for job in result]}, "answer": f"JobIA encontró {len(result)} oportunidades que coinciden con la solicitud."}
    if intent == "profile_matching":
        profile = resolve_profile(request)
        if profile is None:
            return {**base, "execution_status": "needs_input", "result_type": "matching", "result": {"required": ["persisted profile"], "hint": "Provide a registered user email or a saved JobIA profile."}, "answer": "No encontré un perfil laboral persistido para este usuario."}
        result = sorted((enrich_job(job, profile) for job in JOBS), key=lambda job: job.match, reverse=True)
        return {**base, "execution_status": "completed", "result_type": "matching", "result": {"profile": profile.model_dump(), "count": len(result), "jobs": [job.model_dump() for job in result]}, "answer": f"JobIA hizo el matching usando el perfil persistido y encontró {len(result)} oportunidades ordenadas por compatibilidad."}
    if intent == "application_preparation":
        job = resolve_job_identifier(request.message)
        if job is None:
            return {**base, "execution_status": "needs_input", "result_type": "application", "result": {"required": ["job_id"], "hint": "Specify a valid JobIA job ID or opportunity title."}, "answer": "Puedo preparar la postulación, pero necesito identificar una vacante válida."}
        profile = resolve_profile(request)
        if profile is None:
            return {**base, "execution_status": "needs_input", "result_type": "application", "result": {"required": ["persisted profile"], "job_id": job.id}, "answer": "La vacante está identificada; necesito el perfil laboral persistido para generar una postulación personalizada."}
        return {**base, "execution_status": "completed", "result_type": "application", "result": {"job_id": job.id, "profile_email": profile.email, "drafts": prepare_application(enrich_job(job, profile), profile).model_dump()}, "answer": f"Preparé una propuesta de candidatura para {job.title} usando el perfil persistido."}
    return {**base, "execution_status": "accepted", "result_type": "delegation", "result": None, "answer": "JobIA aceptó la solicitud. Necesito una intención laboral más específica para ejecutar una operación."}


@app.on_event("startup")
def initialize_database():
    connection = get_db()
    connection.close()


@app.get("/health")
def health():
    return {"status": "ok", "service": "jobia", "version": APP_VERSION, "contract": API_CONTRACT, "persistence": "sqlite"}


@app.get("/api/v1/capabilities")
def capabilities():
    return {"module": "jobia", "parent": PARENT_MODULE, "host_channel": HOST_CHANNEL, "capabilities": ["opportunities", "matching", "profiles", "applications", "alerts"], "api_version": API_CONTRACT, "trainer": TRAINER_MODULE}


@app.get("/api/v1/module/status")
def module_status():
    return {"module": "JobIA", "parent": "Bitey IA", "host_channel": "Bitey IA Web", "status": "ready", "contract": API_CONTRACT, "trainer": {"module": TRAINER_MODULE, "role": "training-and-validation"}}


@app.get("/api/v1/cognitive/status")
def cognitive_status():
    return {"status": "delegated", "owner": "Bitey IA", "host_channel": "Bitey IA Web", "module": "JobIA", "mode": "employment-intelligence", "bidirectional": True, "inbound": "Bitey IA may delegate employment capabilities to JobIA", "outbound": "JobIA may request general capabilities from Bitey IA"}


@app.get("/api/v1/integrations")
def integrations():
    return {"contract": API_CONTRACT, "general_intelligence": {"module": PARENT_MODULE, "host_channel": HOST_CHANNEL, "direction": "bidirectional", "purpose": "general reasoning, orchestration, tools, memory and policies"}, "trainer": {"module": TRAINER_MODULE, "direction": "trainer-to-jobia", "purpose": "validated employment capabilities, evaluation, regression and feedback", "public_client_api": False}, "clients": ["JobIA-Web", "JobIA-app"]}


@app.get("/api/v1/contract")
def contract():
    return {"name": API_CONTRACT, "module": "JobIA", "parent_system": "Bitey IA", "specialization": "employment-and-work", "host_channel": HOST_CHANNEL, "trainer": TRAINER_MODULE, "clients": ["JobIA-Web", "JobIA-app"], "principle": "Bitey IA coordinates; JobIA executes employment specialization; Bitey Trainer trains and validates."}


@app.get("/jobs")
def list_jobs(q: str = Query(default=""), modality: str = Query(default=""), location: str = Query(default=""), kind: str = Query(default=""), email: str = Query(default="")):
    profile = load_profile(email) if email.strip() else Profile()
    nq, nm, nl, nk = normalize(q), normalize(modality), normalize(location), normalize(kind)
    def matches(job: Job) -> bool:
        if nm and normalize(job.modality) != nm: return False
        if nl and nl not in normalize(job.location): return False
        if nk and nk not in normalize(job.kind): return False
        if nq and nq not in normalize(f"{job.title} {job.company} {job.location} {job.modality} {job.kind} {job.summary} {' '.join(job.skills)}"): return False
        return True
    result = sorted([enrich_job(job, profile) for job in JOBS if matches(job)], key=lambda job: job.match, reverse=True)
    return {"jobs": [job.model_dump() for job in result], "count": len(result)}


@app.get("/jobs/{job_id}")
def get_job(job_id: str, email: str = Query(default="")):
    job = next((item for item in JOBS if item.id == job_id), None)
    if job is None: raise HTTPException(status_code=404, detail="Job not found")
    profile = load_profile(email) if email.strip() else Profile()
    return enrich_job(job, profile)


@app.get("/profile")
def get_profile(email: str = Query(default="")):
    if not email.strip(): raise HTTPException(status_code=400, detail="email is required")
    return load_profile(email)


@app.put("/profile")
def put_profile(profile: Profile):
    normalized_email = profile.email.strip().lower()
    if not normalized_email: raise HTTPException(status_code=400, detail="email is required")
    stored = profile.model_copy(update={"email": normalized_email})
    connection = get_db()
    try:
        connection.execute("INSERT INTO profiles(email, profession, mode, ai_opportunities, skills) VALUES (?, ?, ?, ?, ?) ON CONFLICT(email) DO UPDATE SET profession=excluded.profession, mode=excluded.mode, ai_opportunities=excluded.ai_opportunities, skills=excluded.skills", (stored.email, stored.profession, stored.mode, 1 if stored.aiOpportunities else 0, json.dumps(stored.skills)))
        connection.commit()
    finally:
        connection.close()
    return stored


@app.post("/applications/prepare")
def prepare_application_endpoint(request: PreparationRequest):
    job = next((item for item in JOBS if item.id == request.job_id), None)
    if job is None: raise HTTPException(status_code=404, detail="Job not found")
    return prepare_application(enrich_job(job, request.profile), request.profile)


@app.post("/api/v1/capabilities/delegate")
def delegate(request: DelegationRequest):
    if request.contract != API_CONTRACT or request.capability != "jobia":
        raise HTTPException(status_code=400, detail="Invalid JobIA delegation contract")
    return execute_delegation(request)
