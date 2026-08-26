# JobIA

**Agente IA de empleo, trabajo y oportunidades profesionales.**

JobIA is a product in active development and its user-facing application is the **JobIA App**. It helps users discover legitimate employment, freelance and AI-related opportunities matched to their real skills and preferences.

## Relationship with Bitey IA

Bitey IA is the general-purpose **Supracerebro**. JobIA is a specialized product within its ecosystem.

```text
BITEY IA / SUPRACEREBRO
          │
        JobIA
          │
   Bitey Trainer
   (internal motor)
          │
      JobIA App
```

**Bitey Trainer is not an app. It is the intelligence/training engine used by JobIA.** JobIA consumes validated Trainer capabilities through secure backend contracts instead of duplicating the intelligence engine.

## Main capabilities

- Search AI and IT jobs.
- Search remote, hybrid and onsite work.
- Search legitimate AI-training/evaluation and human-in-the-loop opportunities.
- Save opportunities.
- Rank and explain matches.
- Notify by email and, when configured and consented, WhatsApp/mobile channels.
- Prepare tailored CV/resume content.
- Prepare cover letters, proposals and application answers.
- Analyze compensation/salary.
- Track applications and user decisions.

## Professional profile

JobIA is multi-profession. Profiles can contain profession, skills, education, certifications, experience, languages, location, availability, preferred modality, compensation and CV information supplied by the user.

## Bitey Trainer

Trainer develops and validates the intelligence used by JobIA, including opportunity discovery/normalization, skill and transferable-skill matching, ranking, compensation analysis, AI-work classification, application preparation and feedback-driven improvement.

Trainer supports HUMAN, BITEY and HYBRID workflows. It must never misrepresent an AI as a human or bypass platform, identity, assessment or contractual rules.

## Application workflow

Default flow is:

```text
Discover → Match → Explain → Prepare → User reviews → User authorizes
```

Automatic submission is never assumed and must not bypass consent or platform requirements.

## Architecture

```text
JobIA App
   ↓ HTTPS
JobIA API
   ↓
Bitey Trainer
   ↓
Bitey IA / authorized services
   ↓
Supabase and controlled integrations
```

Provider credentials and sensitive matching/integration logic remain server-side.

## Alerts

Users control search and alert frequency. Opportunities that pass configured thresholds may generate email, WhatsApp or mobile notifications where the channel is implemented and consented.

## Privacy and security

- Account-level isolation.
- RLS/authorization where applicable.
- No provider secrets in the app.
- No Supabase service-role keys in the app.
- Explicit control of CV/profile data.
- Human approval for sensitive application actions.

## Roadmap

1. Validate Bitey Trainer intelligence.
2. Stabilize JobIA API contracts.
3. Complete JobIA Android MVP.
4. Validate APK on physical devices.
5. Improve matching, alerts and application assistance.
6. Expand to additional professions and opportunity sources.

## Guiding principle

> **Bitey Trainer builds and validates the intelligence; JobIA puts that intelligence in the hands of workers. Bitey IA remains the general Supracerebro.**
