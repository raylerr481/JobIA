# JobIA

**Módulo backend especializado de empleo de Bitey IA Web.**

JobIA es la capa de servicios de empleo dentro del ecosistema de **Bitey IA Web**. Expone una API estable para los clientes JobIA-Web y JobIA-app, mientras que la inteligencia general, memoria cognitiva, orquestación de modelos y políticas globales pertenecen a Bitey IA Web.

## Arquitectura del ecosistema

```text
                         BITEY IA WEB
                  General / Integral AI
                           │
              Cognitive Core / Policies
                           │
                  ┌────────▼────────┐
                  │      JobIA       │
                  │ módulo backend   │
                  │ empleo / matching│
                  └────────┬─────────┘
                           │
                    HTTPS / JSON
                 ┌─────────┴─────────┐
                 │                   │
            JobIA-Web           JobIA-app
          Frontend web       Android instalable
```

### Responsabilidad de cada repositorio

- **`bitey-web`** → plataforma general de Bitey IA, cerebro/orquestación, herramientas, memoria y políticas.
- **`JobIA`** → backend especializado de empleo y contrato API de JobIA.
- **`JobIA-Web`** → frontend web; consume exclusivamente la API de JobIA.
- **`JobIA-app`** → aplicación Android; consume la misma API de JobIA.
- **`bitey-trainer`** → motor interno de entrenamiento/validación de inteligencia para JobIA; no es una aplicación ni un cliente.

JobIA es, por tanto, **un módulo de Bitey IA Web**, pero mantiene un backend especializado para que los clientes web y Android compartan el mismo contrato.

## Contrato API JobIA v1

Endpoints base actuales:

- `GET /health`
- `GET /api/v1/capabilities`
- `GET /api/v1/module/status`
- `GET /api/v1/module/manifest`
- `GET /api/v1/cognitive/status`
- `GET /jobs`
- `GET /jobs/{job_id}`
- `GET /profile?email=...`
- `PUT /profile`

`/jobs` admite `q`, `modality`, `location` y `kind` como filtros. El contrato puede crecer sin romper los clientes existentes.

## Relación con Bitey IA Web

JobIA no sustituye al cerebro de Bitey. El reparto es deliberado:

```text
Bitey IA Web
  ├── entiende contexto y objetivo
  ├── decide qué capacidad necesita
  ├── aplica políticas y permisos
  └── coordina modelos/herramientas
          │
          ▼
       JobIA
  ├── oportunidades
  ├── normalización
  ├── matching
  ├── ranking
  ├── perfiles
  ├── aplicaciones
  └── alertas
```

La futura integración cognitiva debe usar contratos versionados, nunca acoplar los clientes a implementaciones internas de Bitey.

## Bitey Trainer

`bitey-trainer` desarrolla y valida capacidades de descubrimiento, matching, ranking, evaluación, compensación y preparación de aplicaciones. Las capacidades validadas se publican hacia JobIA mediante contratos seguros.

```text
Bitey Trainer → valida inteligencia → JobIA → clientes
```

Trainer no controla la interfaz web ni la aplicación Android y no debe convertirse en un segundo cerebro.

## Clientes

### JobIA-Web

El frontend web oficial obtiene la URL del backend mediante `VITE_JOBIA_API_URL`. No contiene secretos ni lógica privada del servidor.

### JobIA-app

La aplicación Android utiliza la misma API JobIA. No mantiene un backend paralelo ni duplica la lógica de matching.

## Seguridad

- Credenciales de proveedores únicamente en backend.
- Ninguna clave `service_role` de Supabase en clientes.
- Datos de perfil y aplicaciones protegidos por autenticación/autorización.
- Acciones externas sensibles requieren consentimiento.
- El resultado de modelos externos se considera no confiable hasta ser evaluado por la política de Bitey.

## Coste e IA

El módulo no exige Gemini ni un proveedor de pago concreto. La selección de modelos pertenece a las políticas de Bitey IA Web y debe respetar el modo económico configurado, incluyendo `free_only` cuando esté activo.

## Desarrollo

```bash
python -m venv .venv
# Windows: .\.venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Principio

> **Bitey IA Web es el sistema general; JobIA es su módulo especializado de empleo; JobIA es el backend compartido; JobIA-Web y JobIA-app son sus dos clientes; Bitey Trainer valida la inteligencia que JobIA utiliza.**
