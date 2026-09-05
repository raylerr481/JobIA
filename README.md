# JobIA

**JobIA is the specialized employment and work module of Bitey IA.**

JobIA is not an independent AI system. It is the employment specialization of Bitey IA, covering professional opportunities, profiles, matching, applications, and alerts. Its backend exposes the versioned `jobia-v1` contract consumed by its web and Android channels.

## Language and naming standard

All repository documentation, API contracts, backend identifiers, variable names, model fields, endpoint parameters, configuration keys, database-facing names, and code references must use **English**.

This is a technical naming standard, not a requirement that the user interface support only English. User-facing content may be localized separately.

Examples:

- `job_id`, not `id_puesto`;
- `company`, not `empresa`;
- `location`, not `ubicacion`;
- `modality`, not `modalidad`;
- `skills`, not `habilidades`;
- `match`, not `coincidencia`;
- `application`, not `postulacion`;
- `VITE_JOBIA_API_URL` and `EXPO_PUBLIC_JOBIA_API_URL` remain English technical identifiers.

Do not introduce Spanish variable names, JSON keys, endpoint parameters, database fields, or internal API identifiers in new code.

## Architecture

```text
                         BITEY IA
                    general intelligence
                           │
             ┌─────────────┼─────────────┐
             │             │             │
          JobIA         Bitey SBT     other modules
       employment/work     trading
             │
       ┌─────┴─────┐
       │           │
   JobIA-Web    JobIA-app
      Web         Android
    channel       channel

Bitey IA Web = web channel of Bitey IA
```

### Repository responsibilities

- **`bitey-web`** → web channel of Bitey IA.
- **`JobIA`** → specialized employment/work module and backend API `jobia-v1`.
- **`JobIA-Web`** → web channel of JobIA; consumes the JobIA API.
- **`JobIA-app`** → Android channel of JobIA; consumes the same API.
- **`bitey-trainer`** → internal Bitey IA capability for training, evaluation, and validation; it is not a client or second brain.

JobIA can receive delegated requests from Bitey IA when employment specialization is required. JobIA can also request general Bitey IA capabilities through controlled APIs/contracts when necessary.

## JobIA API v1 contract

Current primary endpoints:

- `GET /health`
- `GET /api/v1/capabilities`
- `GET /api/v1/module/status`
- `GET /api/v1/module/manifest`
- `GET /api/v1/cognitive/status`
- `GET /api/v1/contract`
- `GET /jobs`
- `GET /jobs/{job_id}`
- `GET /profile?email=...`
- `PUT /profile`
- `POST /applications/prepare`

`/jobs` supports filters such as `q`, `modality`, `location`, and `kind`. The contract is versioned so channels can evolve without depending on internal implementation details.

## JobIA responsibilities

```text
JobIA
 ├── opportunities
 ├── normalization
 ├── matching and ranking
 ├── compatibility explanations
 ├── professional profiles
 ├── application preparation
 └── alerts
```

The backend is the authority for specialized employment intelligence. Channels must not duplicate this intelligence in production.

## Bitey Trainer

`bitey-trainer` trains, evaluates, and validates capabilities that can be used by JobIA. The lifecycle is:

```text
Define → Implement → Test → Measure → Improve
       → Validate → Publish capability → JobIA consumes
```

Trainer does not directly control interfaces and does not create a parallel public backend.

## Channels

### JobIA-Web

Official web channel of JobIA. It receives the backend URL through `VITE_JOBIA_API_URL` and contains no secrets.

### JobIA-app

Official Android channel of JobIA. It uses the same `jobia-v1` API and does not maintain a parallel backend.

## Security

- Provider credentials exist only on the backend.
- No Supabase `service_role` key is exposed to clients.
- Protected data requires authentication/authorization.
- Sensitive external actions require explicit user consent.
- External model output must be evaluated before becoming an action.

## Cost and AI policy

The module follows a free-first approach. It does not require Gemini or a specific paid provider. Model and general capability selection is governed by Bitey IA policies.

## Development

```bash
python -m venv .venv
# Windows: .\\.venv\\Scripts\\Activate.ps1
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Principle

> **Bitey IA is the general system. JobIA is its specialized employment/work module. Bitey IA Web is the web channel of Bitey IA. JobIA-Web and JobIA-app are the web and Android channels of JobIA. Bitey Trainer trains and validates Bitey IA capabilities.**
