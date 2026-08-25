# JobIA

**Your AI-powered job finder.**

JobIA is the future mobile product built on top of the Bitey Trainer intelligence engine. It is designed to help people discover work opportunities that match their real skills, languages, location, availability, salary expectations, and preferred work mode.

## Vision

JobIA turns job searching from a manual process into a personalized, intelligent workflow:

**Create profile → define goals → discover opportunities → match → prioritize → alert → prepare application → user approves → apply.**

JobIA is not intended to replace the worker. It assists the worker, explains why an opportunity matches, prepares materials, and keeps the final decision and authorization with the user.

## Relationship with Bitey Trainer

JobIA is the user-facing product. **Bitey Trainer is the reusable intelligence engine.**

Bitey Trainer provides:

- Opportunity discovery and normalization.
- Duplicate and low-quality opportunity filtering.
- Skill and language matching.
- Remote / hybrid / onsite classification.
- Human-only, agent-allowed, and hybrid workflow classification.
- Match scoring and explanations.
- CV and application preparation.
- Opportunity prioritization.
- User feedback and learning signals.
- Notification and reporting workflows.

JobIA should consume these capabilities through a secure API rather than duplicating the intelligence layer inside the mobile application.

## Planned architecture

```text
Google Play / App Store
          |
          v
       JobIA App
   Expo / React Native
          |
       HTTPS API
          |
          v
      JobIA Backend
          |
          v
     Bitey Trainer
          |
          v
      Supracerebro
          |
          +---- AI providers / routing
          |
          v
        Supabase
```

## User profile

During onboarding, JobIA will collect only information needed to personalize employment discovery, including:

- Name and professional identity.
- Location and preferred work area.
- Remote, hybrid, or onsite preference.
- Skills and experience.
- Languages and proficiency.
- Education and certifications.
- Employment type and availability.
- Salary/rate expectations.
- Preferred job categories.
- CV/resume, when the user chooses to provide it.

The profile is transformed into structured matching data by the backend.

## Opportunity modes

JobIA supports three conceptual modes:

### HUMAN
The opportunity explicitly requires a human worker. JobIA assists with discovery, analysis, preparation, and human review.

### BITEY
The opportunity explicitly permits an agent, service provider, or automated workflow where the contractual terms allow it. Bitey may perform authorized work through its backend capabilities.

### HYBRID
Bitey prepares, automates, or pre-evaluates the work and the human performs required judgment, validation, identity, language, or approval steps.

JobIA must never misrepresent an AI agent as a human worker or bypass a platform's rules.

## Core features

### Phase 1 — Intelligence engine
- Personal worker profile.
- Opportunity ingestion.
- Matching and scoring.
- Human/Bitey/Hybrid classification.
- Opportunity reports.
- Notifications.
- Feedback tracking.

### Phase 2 — Mobile MVP
- Account creation.
- Worker onboarding.
- Skills and preferences.
- Opportunity feed.
- Match score.
- Opportunity details.
- Favorites.
- Alerts.
- Application preparation.

### Phase 3 — Advanced assistant
- CV adaptation.
- Cover letters and proposals.
- Interview preparation.
- Application tracking.
- Personalized search rules.
- Learning from accepted/rejected opportunities.

## Data and privacy

Sensitive credentials and provider secrets must remain on the backend. The mobile app must never contain private AI-provider keys, database service-role keys, or platform credentials.

User data must be isolated per account. Any aggregate learning must use appropriate privacy controls and must not expose another user's personal information.

## Current status

JobIA is a **product foundation repository**. The immediate development focus remains on Bitey Trainer and its real-world testing. The mobile application should be developed only after the matching, opportunity discovery, reporting, and alerting workflows are sufficiently validated.

## Roadmap

1. Validate Bitey Trainer with real opportunities.
2. Stabilize the worker-profile and matching schemas.
3. Expose a secure API for JobIA.
4. Build the Expo/React Native mobile MVP.
5. Test Android APK builds on physical devices.
6. Prepare Android App Bundle (AAB) for Google Play.
7. Add iOS support after the Android workflow is stable.
8. Introduce paid/premium features only after the core product proves useful.

## Ecosystem

- **JobIA** — user-facing employment discovery product.
- **Bitey Trainer** — employment and AI-training intelligence engine.
- **Bitey IA / Supracerebro** — broader AI intelligence and orchestration layer.
- **Supabase** — data, authentication, and persistence layer.

---

JobIA is part of the BiteFixes/Bitey ecosystem and is designed to evolve from the validated Bitey Trainer prototype into a production mobile product.
