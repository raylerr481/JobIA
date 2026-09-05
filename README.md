# JobIA

**Backend y plataforma de inteligencia para empleo y oportunidades profesionales.**

JobIA es el núcleo backend del producto JobIA. Este repositorio **no es el frontend web ni la aplicación Android**: contiene la API, la lógica de negocio y los servicios que utilizan los clientes oficiales.

## Ecosistema JobIA

JobIA está organizado en tres repositorios independientes:

```text
                    JOBIA
              Backend / API / IA
                    │
          ┌─────────┴─────────┐
          │                   │
     JobIA-Web            JobIA App
    Frontend web        App Android
```

- **JobIA** → backend, API, lógica y servicios de inteligencia.
- **JobIA-Web** → frontend web que consume la API de JobIA.
- **JobIA App** → aplicación Android instalable que consume la API de JobIA.

Los clientes no duplican el backend. La lógica sensible y las credenciales de proveedores permanecen del lado servidor.

## Responsabilidades del backend

El backend proporciona los contratos y servicios necesarios para:

- Descubrir y normalizar oportunidades profesionales.
- Buscar empleos y trabajos remotos, híbridos y presenciales.
- Clasificar oportunidades de IA, evaluación y human-in-the-loop.
- Analizar perfiles, habilidades y habilidades transferibles.
- Calcular compatibilidad y ranking de oportunidades.
- Explicar por qué una oportunidad coincide con un perfil.
- Analizar compensación y salario.
- Preparar CV/resumen profesional, cartas y respuestas de aplicación.
- Gestionar oportunidades guardadas, aplicaciones y preferencias.
- Gestionar alertas y canales de notificación cuando estén implementados y autorizados.
- Integrar memoria, conocimiento y datos mediante los servicios configurados del backend.

## Flujo de JobIA

```text
Descubrir → Normalizar → Analizar → Hacer match → Explicar
                     ↓
                  Preparar
                     ↓
             Usuario revisa
                     ↓
             Usuario autoriza
```

JobIA no debe asumir el envío automático de candidaturas ni saltarse consentimiento, verificaciones de identidad, evaluaciones o reglas de plataformas externas.

## Bitey Trainer

**Bitey Trainer es un motor interno de inteligencia y entrenamiento utilizado por JobIA; no es una aplicación independiente.**

Trainer desarrolla y valida capacidades relacionadas con descubrimiento, normalización, matching, ranking, análisis de compensación, clasificación de trabajos de IA, preparación de aplicaciones y mejora mediante feedback.

Los clientes consumen capacidades del backend mediante contratos de API; no necesitan contener las credenciales ni la implementación sensible de estos servicios.

## Relación con Bitey IA

Bitey IA es una plataforma de inteligencia más amplia. JobIA es un producto especializado para empleo y oportunidades profesionales dentro de ese ecosistema.

La separación técnica es deliberada: **JobIA sigue siendo un producto autónomo con su propio backend y sus propios clientes**.

## Clientes oficiales

### JobIA-Web

Frontend web oficial mantenido en [`raylerr481/JobIA-Web`](https://github.com/raylerr481/JobIA-Web). Consume la API de JobIA mediante HTTPS/JSON.

### JobIA App

Aplicación Android instalable de JobIA. Consume los mismos contratos de backend y está separada del frontend web.

> El código Android debe permanecer en su repositorio propio. No se debe convertir este repositorio backend en una aplicación móvil.

## Seguridad

- Las claves privadas de proveedores permanecen en el servidor.
- Nunca exponer claves `service_role` de Supabase a clientes.
- Mantener autorización y aislamiento de datos por cuenta.
- Proteger CV, perfil y datos personales.
- Validar entradas y respuestas de integraciones externas.
- Aplicar consentimiento explícito para acciones sensibles.

## Datos e integraciones

JobIA puede utilizar Supabase y otras integraciones configuradas para persistencia, memoria, conocimiento y servicios externos. Las integraciones deben respetar la separación entre backend y clientes.

No se requiere una base de datos gráfica separada para definir la arquitectura de JobIA.

## Desarrollo

La implementación y los comandos concretos dependen de la estructura actual del backend. Antes de añadir una integración nueva, debe mantenerse el contrato público consumido por **JobIA-Web** y **JobIA App**.

## Principio de arquitectura

> **JobIA es el backend y núcleo de servicios; JobIA-Web es el frontend web; JobIA App es la aplicación Android. Tres repositorios, un mismo producto y una única plataforma backend de JobIA.**
