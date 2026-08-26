# JobIA

**Tu buscador inteligente de empleo, trabajo remoto, presencial, híbrido y oportunidades profesionales.**

JobIA is the user-facing Android application for people who want to discover work and income opportunities matched to what they can actually do. It is deliberately multi-profession: IT is only one category.

## Current status

- Android/mobile product: active development and APK build validation.
- Web version: **not planned for the current phase**.
- Bitey Trainer: intelligence capability that can provide validated opportunity and AI-training intelligence through secure backend/API contracts.
- The immediate product goal is an installable Android APK for testing.

## Product vision

```text
Create account
    ↓
Build professional profile
    ↓
Choose work preferences
    ↓
Discover opportunities
    ↓
Match + rank + explain
    ↓
Alert user
    ↓
Prepare application
    ↓
User reviews and authorizes
```

JobIA should adapt the search to the individual rather than assuming that everyone is looking for the same profession.

## Universal professional profile

A user can be an IT professional, accountant, economics graduate, teacher, technician, construction worker, administrative worker, designer, driver, translator, salesperson, healthcare worker, or another professional.

The profile can contain:

- Name and professional identity.
- Email/account identity.
- Profession and preferred categories.
- Location.
- Skills and practical abilities.
- Education and certifications.
- Work experience.
- Languages and proficiency.
- Availability and preferred schedule.
- Employment type.
- Minimum compensation/rate.
- CV/resume when the user chooses to provide it.
- Natural-language description of what the user knows how to do.

JobIA should recognize transferable skills instead of requiring an exact job-title match.

## Work modality

The user can choose one or more:

- **Remote**.
- **Presencial / Onsite**.
- **Hybrid**.
- Any combination of the above.

For onsite/hybrid opportunities, JobIA can use country, state/province, city and commuting distance when relevant.

## AI and income opportunities

JobIA is not limited to conventional employment. The user can opt into opportunities related to AI and human-in-the-loop work, including where legitimately available:

- AI Trainer.
- AI Evaluator.
- Human-in-the-loop.
- Data annotation/labeling.
- Search evaluation.
- Content evaluation.
- Voice/audio evaluation.
- AI testing.
- Expert review.
- Technical AI evaluation.

A non-technical professional can also receive AI-related opportunities when their real skills and the opportunity requirements match.

## Bitey Trainer relationship

**Bitey Trainer is the intelligence/training capability; JobIA is the worker-facing product.**

Bitey Trainer can progressively provide:

- Opportunity discovery and normalization.
- Duplicate and stale-opportunity detection.
- Skill and transferable-skill matching.
- Language/location/modality matching.
- Compensation and experience analysis.
- Human-only / agent-allowed / hybrid classification.
- Match scoring and explanations.
- Opportunity prioritization.
- Alerts and reports.

JobIA consumes validated capabilities through secure backend APIs. It must not expose provider secrets or internal trainer credentials.

## Matching algorithm

A JobIA Match Score should consider, as applicable:

```text
profession + skills + experience + education
+ language + location + modality + schedule
+ compensation + user preferences
+ opportunity requirements
```

The result should explain **why** the opportunity matches and identify important gaps.

Example:

> **AI Response Evaluator — 91% match**
>
> Remote · English intermediate · $18–25/hour
>
> Why it matches: writing, QA, digital tools and evaluation experience.

## Alerts and frequency

Each user has independent notification preferences. The user can choose a search/alert frequency such as:

- Every few hours.
- Daily.
- Every two days.
- Weekly.
- Paused.

When a relevant opportunity passes the user's configured threshold, JobIA can notify the registered email and, where implemented and consented, mobile notifications.

There are **no global 8:00 AM JobIA Trainer routines** required by the product. Searches and alerts are user-specific.

## Three execution modes

### HUMAN
The opportunity requires a human worker. JobIA assists with discovery, analysis, preparation and tracking; the user remains the worker and final decision maker.

### BITEY
The opportunity explicitly permits an agent/service/automated workflow and applicable terms allow Bitey to perform the work. Execution must be authorized and compliant.

### HYBRID
Permitted automation, preparation, research, drafting or pre-evaluation is combined with required human judgment, validation, identity, physical action or approval.

JobIA and Bitey Trainer must never misrepresent an AI agent as a human or bypass platform rules.

## Application assistance

When allowed, JobIA may prepare tailored CV content, cover letters, freelance proposals, application answers and interview preparation. Default workflow is **prepare → user reviews → user authorizes**. Automatic submission must not bypass identity, consent, assessments, platform requirements or human-only obligations.

## Core Android experience

1. Register with email.
2. Build/review professional profile.
3. Select profession and skills.
4. Choose remote/onsite/hybrid preferences.
5. Set schedule and compensation preferences.
6. Choose opportunity categories, including AI-training opportunities.
7. Configure search/alert frequency.
8. View ranked opportunities and Match Scores.
9. Save/reject opportunities to improve future ranking.
10. Prepare applications with user approval.

## Architecture

```text
                 JobIA Android App
                        |
                      HTTPS
                        |
                    JobIA API
                        |
                 Bitey Trainer
                        |
                 Bitey IA / backend
                        |
          controlled AI/provider routing
                        |
                     Supabase
```

The mobile application remains lightweight. Provider credentials, private database keys, matching logic and sensitive integrations belong on the backend.

## Data model

Initial concepts include:

- `jobia_profiles`
- `jobia_preferences`
- `jobia_opportunities`
- `jobia_matches`
- `jobia_applications`
- `jobia_alerts`
- `jobia_feedback`

The schema should evolve from validated product requirements rather than prematurely duplicating trainer data.

## Privacy and security

JobIA handles professional and personal information. The design requires account-level isolation, Row Level Security where applicable, no provider secrets in the mobile app, no Supabase service-role keys in the mobile app, explicit control over profile/CV data, secure API authentication and consent for notifications/application assistance.

## Roadmap

### Phase 1 — Intelligence validation
- Develop and test Bitey Trainer capabilities.
- Test multiple professions and realistic profiles.
- Measure match quality and false positives.
- Improve alerts and explanations.

### Phase 2 — JobIA service layer
- Stable API contracts.
- Authentication and account isolation.
- Validated opportunity/matching services.

### Phase 3 — Android MVP
- Expo/React Native app.
- Registration/profile.
- Opportunity feed.
- Matching.
- Remote/onsite/hybrid filters.
- Alerts and frequency.
- Saved opportunities.
- Application preparation.

### Phase 4 — Android release
- Production Android App Bundle (AAB) for Google Play.
- Testing tracks.
- Production release after APK validation.

### Future
- iOS after Android workflow is stable.
- Advanced CV optimization.
- Interview preparation.
- Personalized search agents.
- Premium/business features where appropriate.

**Web is intentionally not part of the current JobIA release plan.**

## Guiding principle

> **Bitey Trainer builds and validates the intelligence. JobIA puts that intelligence in the hands of workers of any profession.**

JobIA is designed to help people find work and legitimate income opportunities based on what they can actually do, not only on the job title they already have.
