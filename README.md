# Portafolio — JJOR

Estructura lista para subir a tu hosting (estático).

```
jjor-portfolio/
├─ index.html
├─ cv.html
├─ css/
│  └─ styles.css
├─ js/
│  └─ script.js
├─ assets/
│  ├─ foto.svg
│  └─ cover.svg
├─ icons/
│  ├─ favicon.svg
│  ├─ icon-192.png
│  └─ icon-512.png
└─ manifest.webmanifest
```

## Edita estos puntos
- En `index.html` y `cv.html`: cambia enlaces de **LinkedIn/GitHub** y el `canonical` por tu dominio real.
- Sustituye `/assets/foto.svg` por tu foto y `/assets/cover.svg` por una imagen real de portada (ideal: **1200×630**).
- En `index.html` > sección **Proyectos**: cambia títulos, descripciones y URLs (demo/código).
- En `cv.html`: completa **Experiencia** y **Educación** con tus datos.

## PDF del CV
Abre `cv.html` y pulsa **Imprimir** → Guardar como PDF. Los estilos ya ocultan header/gradientes para un PDF limpio.

## Accesibilidad / SEO / Rendimiento
- Skip link, `aria-expanded`, `aria-selected` y `hidden` para filtros accesibles.
- Open Graph/Twitter, `canonical`, `theme-color` y JSON‑LD (`Person`).
- Imágenes con `loading="lazy"` + dimensiones para evitar CLS.
- `prefers-reduced-motion` respetado.
- Fallbacks para `color-mix`/`oklab`.

## Deploy rápido
- GitHub Pages: sube la carpeta al branch `main` y activa Pages.
- Netlify/Vercel: arrastra la carpeta o crea un proyecto (framework: None / Static).
