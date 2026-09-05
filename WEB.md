# JobIA Web

JobIA is now a web-capable application in addition to the Android application described in the README.

## Run locally

```bash
npm install
npm run web
```

Then open the URL shown by Expo in the browser.

## Production web build

```bash
npm install
npm run build:web
```

Expo exports the browser application to `dist/`.

## Deployment

The repository includes `netlify.toml` configured for a static Expo web deployment:

- Build command: `npm run build:web`
- Publish directory: `dist`
- SPA fallback: all routes resolve to `/index.html`

The web frontend uses the same JobIA application code and preserves the product principles from the main README: opportunity discovery, matching, explanations, profile/preferences, alerts and application preparation. Real opportunity data must come from the authorized JobIA API/Bitey Trainer backend; the UI must not expose provider credentials or Supabase service-role keys.

## Product relationship

```text
BITEY IA
   │
 JobIA
 ┌─┴───────────────┐
Web             Android
 │                  │
 └────── HTTPS ────┘
          │
       JobIA API
          │
     Bitey Trainer
          │
   Supabase / integrations
```

The web client is a presentation and interaction layer. Intelligence, credentials, matching logic and controlled integrations remain server-side.
