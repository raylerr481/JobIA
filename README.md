# JobIA

**Tu buscador inteligente de empleo, trabajo remoto y oportunidades profesionales.**

JobIA is the user-facing application of the Bitey ecosystem for people who want to discover work opportunities that match their real-world profile. It is intentionally broader than technology or AI jobs: a programmer, accountant, economics graduate, teacher, technician, construction worker, administrative worker, designer, driver, or any other professional can use JobIA.

## Product vision

JobIA turns employment discovery into a personalized workflow:

**Create profile → describe what you can do → define where/how you want to work → search → match → prioritize → alert → prepare → user approves → apply.**

The product adapts the search to the individual instead of assuming that every worker should search for the same job categories.

## JobIA and Bitey Trainer

These are related but different products/modules:

- **JobIA** — the future mobile application used by workers.
- **Bitey Trainer** — the employment/AI-training intelligence module inside the broader Bitey IA/Supracerebro ecosystem.
- **Bitey IA / Supracerebro** — the broader intelligence and orchestration layer.

JobIA does **not** duplicate Bitey Trainer. JobIA consumes Bitey Trainer capabilities through a secure backend/API.

While Bitey Trainer is being developed and tested, its real-world capabilities should continuously become the validated intelligence foundation that JobIA will later expose as a mobile product.

## Development relationship

```text
                 BITEY IA / SUPRACEREBRO
                          |
                          v
                   BITEY TRAINER
              employment intelligence
                          |
             +------------+------------+
             |                         |
             v                         v
      Real-world tests             Future API
             |                         |
             +------------+------------+
                          v
                        JOBIA
                   mobile application
                          |
                 +--------+--------+
                 |        |        |
                 v        v        v
              Android    iOS      Web (future)
```

The development algorithm is intentionally incremental:

1. Implement a capability in Bitey Trainer.
2. Test it against real opportunities and realistic worker profiles.
3. Measure false positives, false negatives, language mismatches, duplicate jobs, and unsuitable recommendations.
4. Improve the matching/ranking rules.
5. Define the capability as a reusable contract.
6. Expose the validated capability through the JobIA API when stable.
7. Integrate it into the JobIA mobile experience.
8. Repeat the cycle as new capabilities are developed.

This means **Bitey Trainer is the laboratory and intelligence engine; JobIA is the product interface for workers.**

## Universal worker profile

JobIA must not be designed only for people with technical careers.

A worker may create a profile using:

- Name and professional identity.
- Location and preferred work area.
- Remote, hybrid, or onsite preference.
- Skills and practical abilities.
- Formal education and certifications.
- Work experience.
- Languages and proficiency.
- Availability and desired schedule.
- Employment type.
- Salary/rate expectations.
- Preferred industries and job categories.
- CV/resume, if the user chooses to provide one.
- A natural-language description of what the person knows how to do.

A person does not need to know the professional terminology used by job boards. They can explain their abilities in ordinary language and JobIA can transform that information into structured matching attributes.

### Example worker profiles

**Accountant** — accounting, Excel, financial records, bookkeeping, administrative work.

**Economics graduate** — data analysis, research, Excel, reporting, economics.

**Construction worker** — masonry, construction assistance, finishing, physical work, local availability.

**IT professional** — programming, networks, technical support, AI tools, data and cloud.

The matching engine should discover transferable skills instead of rejecting a worker because their job title does not exactly match the title of an opportunity.

## Work preferences

During onboarding JobIA should ask where and how the person wants to work:

- Remote.
- Hybrid.
- Onsite.
- Country.
- State/province.
- City.
- Maximum commuting distance when relevant.
- Working hours.
- Full-time/part-time/freelance/contract.
- Minimum compensation.

These preferences become matching constraints rather than merely profile text.

## Opportunity intelligence

Bitey Trainer should progressively provide JobIA with:

- Opportunity discovery.
- Source normalization.
- Duplicate detection.
- Stale/closed opportunity detection when possible.
- Skill matching.
- Transferable-skill matching.
- Language matching.
- Location matching.
- Remote/hybrid/onsite classification.
- Compensation analysis.
- Experience-level analysis.
- Human-only / agent-allowed / hybrid classification.
- Match scoring.
- Explanation of strengths and gaps.
- Opportunity prioritization.
- User feedback signals.
- Notifications and reports.

## Three execution modes

### HUMAN
The opportunity requires a human worker. JobIA assists with discovery, analysis, preparation, and tracking. The user remains the worker and final decision maker.

### BITEY
The opportunity explicitly permits an agent, service provider, or automated workflow, and the applicable terms allow Bitey to perform the work. Bitey can execute authorized work through the backend.

### HYBRID
Bitey performs permitted automation, preparation, research, drafting, testing, or pre-evaluation while the human performs required judgment, validation, identity, language, physical action, or approval.

JobIA and Bitey Trainer must never misrepresent an AI agent as a human or bypass a platform's rules.

## Core mobile experience

### Onboarding

1. Create account.
2. Enter name and basic professional information.
3. Select or describe skills.
4. Add education and experience.
5. Add languages.
6. Choose location.
7. Choose remote/hybrid/onsite preferences.
8. Set schedule and compensation expectations.
9. Upload a CV if desired.
10. Review the generated worker profile.

### Daily experience

The user opens JobIA and sees prioritized opportunities such as:

> **AI Response Evaluator — 91% match**
>
> Remote · English intermediate · $18–25/hour
>
> Why it matches: writing, QA, digital tools, evaluation experience.
>
> [View] [Save] [Prepare application]

The explanation is as important as the score. JobIA should tell the worker **why** an opportunity is recommended and what could prevent a successful application.

## Application assistance

When allowed by the source/platform, JobIA may prepare:

- Tailored CV content.
- Cover letters.
- Freelance proposals.
- Application answers.
- Interview preparation.
- Skills-gap explanations.

The default workflow is **prepare → user reviews → user authorizes**. Automatic submission must never bypass identity, consent, platform requirements, assessments, or other human-only obligations.

## Personalization loop

JobIA should learn from explicit user feedback:

```text
Opportunity found
      |
      v
User views
      |
 +----+----+
 |         |
Accept   Reject
 |         |
 +----+----+
      |
      v
Preference signal
      |
      v
Better future ranking
```

Learning must use privacy controls and must not expose another user's personal information.

## Architecture

```text
Google Play / App Store
          |
          v
       JobIA App
    Expo / React Native
          |
        HTTPS
          |
          v
      JobIA API
          |
          v
     Bitey Trainer
          |
          v
      Supracerebro
          |
          +---- controlled AI/provider routing
          |
          v
       Supabase
```

The mobile application must remain lightweight. Provider credentials, private database keys, matching logic, and sensitive integrations belong on the backend.

## Data model

The initial JobIA data layer is designed around concepts such as:

- `jobia_profiles`
- `jobia_preferences`
- `jobia_opportunities`
- `jobia_matches`
- `jobia_applications`
- `jobia_alerts`
- `jobia_feedback`

The schema should evolve from validated Bitey Trainer requirements rather than prematurely duplicating trainer tables.

## Privacy and security

JobIA will handle potentially sensitive professional and personal information. The design must include account-level data isolation, Row Level Security where applicable, no provider secret keys in the mobile application, no Supabase service-role keys in the mobile application, explicit user control over CV/profile data, secure API authentication, clear consent for notifications/application assistance, and privacy-preserving aggregate learning.

## Roadmap

### Phase 1 — Bitey Trainer validation
- Build and test employment intelligence.
- Test with real profiles.
- Test multiple occupations and skill sets.
- Measure match quality.
- Improve reports and alerts.

### Phase 2 — JobIA service layer
- Define stable API contracts.
- Connect validated Bitey Trainer capabilities.
- Support multiple worker profiles.
- Add authentication and account isolation.

### Phase 3 — JobIA mobile MVP
- Expo/React Native application.
- Android APK testing.
- Worker onboarding.
- Profile management.
- Opportunity feed.
- Matching.
- Alerts.
- Saved opportunities.

### Phase 4 — Store release
- Production Android App Bundle (AAB).
- Google Play testing tracks.
- Production release.
- iOS build after Android workflow is stable.

### Phase 5 — Advanced product
- CV optimization.
- Application assistant.
- Interview preparation.
- Personalized search agents.
- Premium features.
- Business/API offering where appropriate.

## Current status

JobIA is currently a **product foundation and future mobile application**. The immediate priority is to develop and validate Bitey Trainer. Every validated capability should be designed so that it can later be consumed by JobIA rather than becoming isolated trainer-only code.

## Ecosystem

- **JobIA** — user-facing employment application for workers of any profession.
- **Bitey Trainer** — intelligence module for employment discovery, matching, AI training/evaluation, and human-in-the-loop workflows.
- **Bitey IA / Supracerebro** — broader AI orchestration and intelligence platform.
- **Supabase** — authentication, data, persistence, and backend services.

## Guiding principle

> **Bitey Trainer builds and validates the intelligence. JobIA puts that intelligence in the hands of workers.**

JobIA is designed to help people find work based on what they can actually do, not only on the job title they already have.
