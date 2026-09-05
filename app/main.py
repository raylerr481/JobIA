from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

APP_VERSION = "1.3.1"
API_CONTRACT = "jobia-v1"
TRAINER_MODULE = "bitey-trainer"
PARENT_MODULE = "bitey"
HOST_CHANNEL = "bitey-web"
DB_PATH = Path(os.getenv("JOBIA_DB_PATH", "data/jobia.sqlite3"))

app = FastAPI(
    title="JobIA Backend",
    version=APP_VERSION,
    description="Employment intelligence module of Bitey IA, exposed through JobIA web and Android channels.",
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
    Job(
        id="jobia-1",
        title="AI Response Evaluator",
        company="JobIA Network",
        location="Brazil",
        modality="Remote",
        kind="Human-in-the-loop",
        match=94,
        summary="Evaluate AI responses using technical knowledge and quality criteria.",
        skills=["AI", "Evaluation", "Portuguese", "Critical thinking"],
    ),
    Job(
        id="jobia-2",
        title="Remote Technical Support Specialist",
        company="JobIA Network",
        location="Brazil",
        modality="Remote",
        kind="Full-time",
        match=89,
        summary="Provide technical support and resolve issues for users and technology environments.",
        skills=["Support", "Windows", "Networking", "Customer service"],
    ),
    Job(
        id="jobia-3",
        title="Junior Data Analyst",
        company="JobIA Network",
        location="Brazil",
        modality="Hybrid",
        kind="Contract",
        match=84,
        summary="Analyze, clean, and interpret data to support business decisions.",
        skills=["Python", "SQL", "Excel", "Data analysis"],
    ),
]


def normalize(value: str) -> str:
    import unicodedata

    return "".join(
        ch
        for ch in unicodedata.normalize("NFD", value)
        if unicodedata.category(ch) != "Mn"
    ).lower().strip()


def overlaps(first: str, second: str) -> bool:
    normalized_first, normalized_second = normalize(first), normalize(second)
    if normalized_first == normalized_second:
        return True
    if normalized_first in normalized_second or normalized_second in normalized_first:
        return True
    first_tokens = {
        token
        for token in normalized_first.replace("+", " + ")
        .replace("#", " # ")
        .replace(".", " . ")
        .split()
        if len(token) > 2
    }
    second_tokens = {
        token
        for token in normalized_second.replace("+", " + ")
        .replace("#", " # ")
        .replace(".", " . ")
        .split()
        if len(token) > 2
    }
    return bool(first_tokens & second_tokens)


def calculate_match(
    job: Job, profile: Profile
) -> tuple[int, list[MatchReason], list[str], list[str]]:
    required_skills = job.skills
    owned_skills = profile.skills
    reasons = [
        MatchReason(
            skill=skill,
            matched=any(overlaps(owned_skill, skill) for owned_skill in owned_skills),
        )
        for skill in required_skills
    ]
    strengths = [reason.skill for reason in reasons if reason.matched]
    gaps = [reason.skill for reason in reasons if not reason.matched]
    skill_score = (len(strengths) / len(required_skills)) * 70 if required_skills else 50
    modality_score = 15 if normalize(job.modality) == normalize(profile.mode) else 5
    profession = normalize(profile.profession.split("/")[0]) if profile.profession else ""
    profession_score = (
        15 if profession and profession in normalize(job.title + " " + job.summary) else 8
    )
    score = max(0, min(100, round(skill_score + modality_score + profession_score)))
    return score, reasons, strengths, gaps


def enrich_job(job: Job, profile: Profile) -> Job:
    score, reasons, strengths, gaps = calculate_match(job, profile)
    return job.model_copy(
        update={
            "match": score,
            "match_reasons": reasons,
            "strengths": strengths,
            "gaps": gaps,
        }
    )


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


def load_profile(email: str) -> Profile:
    normalized_email = email.strip().lower()
    if not normalized_email:
        return Profile()
    connection = get_db()
    try:
        row = connection.execute(
            "SELECT * FROM profiles WHERE email = ?", (normalized_email,)
        ).fetchone()
        return profile_from_row(row) if row else Profile(email=normalized_email)
    finally:
        connection.close()


def prepare_application(job: Job, profile: Profile) -> ApplicationDrafts:
    skills = [skill.strip() for skill in profile.skills if skill.strip()]
    skill_text = ", ".join(skills) if skills else "relevant technical and professional skills"
    profession = profile.profession or "professional"
    modality = profile.mode or "the specified work arrangement"
    matched = [
        required
        for required in job.skills
        if any(overlaps(owned, required) for owned in skills)
    ]
    match_text = (
        f" My strengths include {', '.join(matched)}."
        if matched
        else ""
    )
    return ApplicationDrafts(
        cvSummary=(
            f"{profession} with results-oriented experience and knowledge in {skill_text}. "
            f"Interested in {modality.lower()} opportunities and applying technical skills, "
            f"problem solving, and continuous learning.{match_text}"
        ),
        coverLetter=(
            f"Hello,\n\nI am interested in the {job.title} opportunity at {job.company}. "
            f"My profile as a {profession.lower()} and my knowledge of {skill_text} allow me "
            "to contribute technical capability, analysis, and results orientation.\n\n"
            f"The position is particularly attractive to me because of its {job.kind.lower()} "
            f"focus and the opportunity to continue developing my skills.{match_text}\n\n"
            "I would be glad to discuss my experience and how I can contribute to the team.\n\n"
            f"Regards,\n{profile.email or 'Candidate'}"
        ),
        answers=(
            f"Motivation: I am interested in {job.title} because it connects my experience as a "
            f"{profession.lower()} with the opportunity to create value at {job.company}.\n\n"
            f"Relevant strengths: {skill_text}."
            + (
                f"\n\nDirect matches: {', '.join(matched)}."
                if matched
                else ""
            )
            + f"\n\nAvailability: {modality}."
        ),
        notes=(
            "Draft generated by JobIA Backend. Review personal data, requirements, experience, "
            "and conditions before authorizing any external action."
        ),
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
        "parent": PARENT_MODULE,
        "host_channel": HOST_CHANNEL,
        "capabilities": [
            "opportunities",
            "matching",
            "profiles",
            "applications",
            "alerts",
        ],
        "api_version": API_CONTRACT,
        "trainer": TRAINER_MODULE,
    }


@app.get("/api/v1/module/status")
def module_status() -> dict[str, Any]:
    return {
        "module": "JobIA",
        "parent": "Bitey IA",
        "host_channel": "Bitey IA Web",
        "status": "ready",
        "contract": API_CONTRACT,
        "trainer": {
            "module": TRAINER_MODULE,
            "role": "training-and-validation",
        },
    }


@app.get("/api/v1/cognitive/status")
def cognitive_status() -> dict[str, Any]:
    return {
        "status": "delegated",
        "owner": "Bitey IA",
        "host_channel": "Bitey IA Web",
        "module": "JobIA",
        "mode": "employment-intelligence",
        "bidirectional": True,
        "inbound": "Bitey IA may delegate employment capabilities to JobIA",
        "outbound": "JobIA may request general capabilities from Bitey IA",
    }


@app.get("/api/v1/integrations")
def integrations() -> dict[str, Any]:
    return {
        "contract": API_CONTRACT,
        "general_intelligence": {
            "module": PARENT_MODULE,
            "host_channel": HOST_CHANNEL,
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
        "parent_system": "Bitey IA",
        "specialization": "employment-and-work",
        "host_channel": "Bitey IA Web",
        "trainer": TRAINER_MODULE,
        "clients": ["JobIA-Web", "JobIA-app"],
        "principle": (
            "Bitey IA coordinates; JobIA executes employment specialization; "
            "Bitey Trainer trains and validates."
        ),
    }


@app.get("/jobs", response_model=list[Job])
def get_jobs(
    q: str = Query(default=""),
    modality: str = Query(default=""),
    location: str = Query(default=""),
    kind: str = Query(default=""),
    email: str = Query(default=""),
) -> list[Job]:
    search_term = q.strip().lower()
    result = JOBS
    if search_term:
        result = [
            job
            for job in result
            if search_term
            in f"{job.title} {job.company} {job.summary} {' '.join(job.skills)}".lower()
        ]
    if modality:
        result = [job for job in result if job.modality.lower() == modality.lower()]
    if location:
        result = [job for job in result if location.lower() in job.location.lower()]
    if kind:
        result = [job for job in result if kind.lower() in job.kind.lower()]
    profile = load_profile(email)
    return sorted(
        (enrich_job(job, profile) for job in result),
        key=lambda job: job.match,
        reverse=True,
    )


@app.get("/jobs/{job_id}", response_model=Job)
def get_job(job_id: str, email: str = Query(default="")) -> Job:
    for job in JOBS:
        if job.id == job_id:
            return enrich_job(job, load_profile(email))
    raise HTTPException(status_code=404, detail="Opportunity not found")


@app.get("/profile", response_model=Profile)
def get_profile(email: str = Query(default="")) -> Profile:
    normalized_email = email.strip().lower()
    if not normalized_email:
        return Profile()
    connection = get_db()
    try:
        row = connection.execute(
            "SELECT * FROM profiles WHERE email = ?", (normalized_email,)
        ).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Profile not found")
        return profile_from_row(row)
    finally:
        connection.close()


@app.put("/profile", response_model=Profile)
def save_profile(profile: Profile) -> Profile:
    normalized_email = profile.email.strip().lower()
    if not normalized_email:
        raise HTTPException(status_code=400, detail="email is required")
    connection = get_db()
    try:
        connection.execute(
            """
            INSERT INTO profiles (
                email, profession, mode, ai_opportunities, skills
            ) VALUES (?, ?, ?, ?, ?)
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


@app.post("/applications/prepare", response_model=ApplicationDrafts)
def prepare_application_endpoint(request: PreparationRequest) -> ApplicationDrafts:
    job = next((item for item in JOBS if item.id == request.job_id), None)
    if job is None:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return prepare_application(job, request.profile)


@app.get("/api/v1/module/manifest")
def manifest() -> dict[str, Any]:
    return {
        "id": "jobia",
        "name": "JobIA",
        "parent_system": PARENT_MODULE,
        "host_channel": HOST_CHANNEL,
        "role": "specialized employment intelligence module",
        "clients": ["JobIA-Web", "JobIA-app"],
        "trainer": TRAINER_MODULE,
        "contract": API_CONTRACT,
        "integration": "bidirectional-with-bitey",
        "persistence": "sqlite",
    }
