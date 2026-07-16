# El Kit del Viajero — Viajes Casal

Landing page estática lista para publicarse en GitHub Pages.

## Sprint 2 - Crecimiento orgánico

El repositorio incluye ahora un Centro de Recursos SEO completamente estático y compatible con GitHub Pages:

- `blog/`: portada del centro de recursos y 10 artículos.
- `guias/`: formulario de acceso a 5 checklists descargables.
- `output/pdf/`: archivos PDF finales.
- `mochilas/`, `powerbanks/`, `adaptadores/`, `candados-tsa/` y `organizadores/`: landings por categoría.
- `sitemap.xml` y `robots.txt`: archivos de descubrimiento para buscadores.
- `assets/recursos.css` y `assets/recursos.js`: estilos y comportamiento compartidos.

Los artículos incluyen breadcrumbs, tabla de contenidos, tiempo estimado de lectura, enlaces internos, preguntas frecuentes y datos estructurados `Article` y `FAQPage`.

Para regenerar las páginas y PDFs después de editar los datos fuente:

```powershell
python scripts/generate_sprint2.py
python scripts/generate_guides.py
```

El formulario guarda el lead localmente como demostración y desbloquea las descargas. Antes de una campaña real, conecta `assets/recursos.js` con Brevo, Mailchimp, Tally u otro proveedor de email marketing.

## Archivos

- `index.html`: contiene toda la página, estilos y funciones.
- `README.md`: instrucciones de configuración.

## 1. Agregar enlaces de afiliado

Abre `index.html` y busca:

```javascript
const affiliateLinks = {
  mochila: "#",
  organizadores: "#",
  powerbank: "#",
  adaptador: "#",
  candado: "#",
  bascula: "#",
  portapasaporte: "#",
  almohada: "#",
  liquidos: "#"
};
```

Sustituye cada `#` por el enlace generado desde tu cuenta de afiliado de Mercado Libre.

Ejemplo:

```javascript
mochila: "https://mercadolibre.com/sec/ENLACE-DE-AFILIADO"
```

Los botones ya utilizan `rel="sponsored noopener"` para identificar correctamente los enlaces comerciales.

## 2. Cambiar WhatsApp

Busca todas las apariciones de:

```text
5210000000000
```

Reemplázalas por tu número con clave de país, sin espacios, guiones ni el signo `+`.

Ejemplo para México:

```text
5219981234567
```

## 3. Configurar SEO

En la parte superior de `index.html` reemplaza:

```text
https://TU-USUARIO.github.io/el-kit-del-viajero/
```

por la URL definitiva del repositorio.

También puedes modificar:

- `<title>`
- `meta description`
- Open Graph
- Nombre de la agencia
- Aviso de privacidad
- Términos de uso

## 4. Conectar la captura de correos

El formulario es visual y no almacena información todavía.

Puedes sustituirlo o conectarlo con:

- Tally
- Brevo
- Mailchimp
- ConvertKit
- Google Forms

## 5. Publicar en GitHub Pages

1. Crea un repositorio público llamado `el-kit-del-viajero`.
2. Sube `index.html` y `README.md`.
3. En GitHub entra a **Settings**.
4. Selecciona **Pages**.
5. En **Build and deployment**, elige **Deploy from a branch**.
6. Selecciona la rama `main` y la carpeta `/root`.
7. Guarda los cambios.
8. GitHub mostrará la dirección pública del sitio.

La URL normalmente será:

```text
https://TU-USUARIO.github.io/el-kit-del-viajero/
```

## 6. Recomendaciones antes de publicar

- Comprueba cada enlace de afiliado en una ventana privada.
- Coloca tu aviso de privacidad.
- Mantén visible el aviso de afiliación.
- Revisa periódicamente que los productos sigan disponibles.
- No publiques precios fijos si cambian con frecuencia.
- Sustituye cualquier imagen que no represente fielmente el producto enlazado.
