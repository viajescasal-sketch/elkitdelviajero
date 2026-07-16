# Worker de suscripción - El Kit del Viajero

Endpoint previsto:

`https://kit-viajero-brevo.viajesbumerancasal.workers.dev/suscribir`

Configuración pública:

- Lista Brevo: `3`
- Plantilla transaccional: `1`
- Origen permitido: `https://viajescasal-sketch.github.io`

La clave de Brevo nunca debe añadirse al repositorio. Configúrala de forma interactiva:

```powershell
npx wrangler secret put BREVO_API_KEY
```

Después despliega con:

```powershell
npx wrangler deploy
```
