# El Kit del Viajero — Viajes Casal

Landing page estática lista para publicarse en GitHub Pages.

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
