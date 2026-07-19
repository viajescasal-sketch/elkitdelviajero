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

## Plantilla y automatización

El correo transaccional recibe estas variables:

- `{{params.LEAD_MAGNET_URL}}`: enlace directo a la guía solicitada.
- `{{params.GUIDE_NAME}}`: nombre de la guía.
- `{{params.DOWNLOAD_PAGE}}`: biblioteca completa de descargas.

Para los contactos que marcan la autorización opcional de promociones, configura en Brevo una automatización disparada al ingresar a la lista:

1. Entrega inmediata de la guía (ya la envía el Worker).
2. Día 2: consejo de organización y enlace al artículo relacionado.
3. Día 5: accesorios recomendados, identificando los enlaces de afiliado.
4. Día 8: invitación a cotizar el viaje con Viajes Casal.

Quienes no acepten promociones solo deben recibir el correo transaccional solicitado.
