# JobIA

**Agente IA de empleo, trabajo y oportunidades profesionales.**

JobIA is a product in active development. It keeps its cross-platform application code here, while the dedicated browser frontend lives in **[JobIA-Web](https://github.com/raylerr481/JobIA-Web)**. Both clients consume the same secure JobIA API contract.

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
   ┌──────┴──────┐
 JobIA App    JobIA Web
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

## Clients

### JobIA App

The Expo application remains the mobile/native client in this repository and can target Android and web through Expo when needed.

### JobIA Web

The dedicated browser experience is maintained in [raylerr481/JobIA-Web](https://github.com/raylerr481/JobIA-Web). It provides a responsive desktop/mobile web dashboard, opportunity search, profile, alerts and application tracking while consuming the JobIA API.

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
                 BITEY IA
                    │
                  JobIA
                    │
              Bitey Trainer
                    │
             ┌──────┴──────┐
             │             │
         JobIA App      JobIA Web
             │             │
             └──── HTTPS ──┘
                    │
                 JobIA API
                    │
          Supabase / integrations
```

Provider credentials and sensitive matching/integration logic remain server-side.

## Alerts

Users control search and alert frequency. Opportunities that pass configured thresholds may generate email, WhatsApp or mobile notifications where the channel is implemented and consented.

## Privacy and security

- Account-level isolation.
- RLS/authorization where applicable.
- No provider secrets in the app or browser.
- No Supabase service-role keys in clients.
- Explicit control of CV/profile data.
- Human approval for sensitive application actions.

## Guiding principle

> **Bitey Trainer builds and validates the intelligence; JobIA puts that intelligence in the hands of workers. Bitey IA remains the general Supracerebro.**
