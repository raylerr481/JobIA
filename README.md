# JobIA

**Módulo especializado de empleo y trabajo de Bitey IA.**

JobIA no es una IA independiente: es el módulo de Bitey IA especializado en oportunidades profesionales, perfiles, matching, aplicaciones y alertas. Su backend implementa el contrato `jobia-v1` que consumen sus canales web y Android.

## Arquitectura

```text
                         BITEY IA
                    inteligencia general
                           │
             ┌─────────────┼─────────────┐
             │             │             │
          JobIA         Bitey SBT     otros módulos
       empleo/trabajo      trading
             │
       ┌─────┴─────┐
       │           │
   JobIA-Web    JobIA-app
      Web         Android
     canal         canal

Bitey IA Web = canal web de Bitey IA
```

### Responsabilidad de cada repositorio

- **`bitey-web`** → canal web de Bitey IA; presenta y coordina las capacidades generales del sistema.
- **`JobIA`** → módulo/backend especializado de empleo de Bitey IA y contrato API `jobia-v1`.
- **`JobIA-Web`** → canal web de JobIA; consume la API de JobIA.
- **`JobIA-app`** → canal Android de JobIA; consume la misma API.
- **`bitey-trainer`** → capacidad interna de Bitey IA para entrenamiento, evaluación y validación; no es un cliente ni un segundo cerebro.

JobIA puede recibir solicitudes delegadas desde Bitey IA cuando una tarea requiere especialización laboral. También puede solicitar capacidades generales de Bitey IA mediante APIs/contratos controlados cuando sean necesarias.

## Contrato API JobIA v1

Endpoints principales actuales:

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

`/jobs` admite filtros como `q`, `modality`, `location` y `kind`. El contrato es versionado para permitir evolución sin acoplar los canales a implementaciones internas.

## Responsabilidades de JobIA

```text
JobIA
 ├── oportunidades
 ├── normalización
 ├── matching y ranking
 ├── explicación de compatibilidad
 ├── perfiles profesionales
 ├── preparación de aplicaciones
 └── alertas
```

El backend es la autoridad para la inteligencia especializada de empleo. Los canales no deben duplicar esa lógica en producción.

## Bitey Trainer

`bitey-trainer` entrena, evalúa y valida capacidades que pueden ser utilizadas por JobIA. El flujo es:

```text
Definir → Implementar → Probar → Medir → Mejorar
        → Validar → Publicar capacidad → JobIA consume
```

Trainer no controla directamente las interfaces y no crea un backend público paralelo.

## Canales

### JobIA-Web

Canal web oficial de JobIA. Obtiene la URL del backend mediante `VITE_JOBIA_API_URL` y no contiene secretos.

### JobIA-app

Canal Android oficial de JobIA. Utiliza la misma API `jobia-v1` y no mantiene un backend paralelo.

## Seguridad

- Credenciales de proveedores únicamente en backend.
- Ninguna clave `service_role` de Supabase en clientes.
- Datos protegidos por autenticación/autorización.
- Acciones externas sensibles requieren consentimiento.
- Los resultados de modelos externos deben evaluarse antes de convertirse en acciones.

## Coste e IA

El módulo sigue un enfoque free-first. No requiere Gemini ni un proveedor de pago concreto. La selección de modelos y capacidades generales corresponde a las políticas de Bitey IA.

## Desarrollo

```bash
python -m venv .venv
# Windows: .\\.venv\\Scripts\\Activate.ps1
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Principio

> **Bitey IA es el sistema general. JobIA es su módulo especializado de empleo. Bitey IA Web es el canal web de Bitey IA. JobIA-Web y JobIA-app son los canales web y Android de JobIA. Bitey Trainer entrena y valida capacidades de Bitey IA.**
