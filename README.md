# CV Responsive — Juan José Osorio Reyes

Proyecto listo para producción, con HTML/CSS/JS sin dependencias de build.
- 100% responsive (grids fluidas + clamp en tipografía/espacios + múltiples breakpoints)
- Modo claro/oscuro persistente
- Menú móvil accesible (aria, escape para cerrar)
- Portafolio con tarjetas "clic completo" (stretched-link)
- Diplomas con visor (dialog) y carga desde `data/diplomas.json`

## Estructura
.
├── assets/ (imágenes, íconos, PDFs)
├── css/
│   └── styles.css
├── data/
│   └── diplomas.json
├── js/
│   └── app.js
└── index.html

## Despliegue
1. Sube esta carpeta completa a tu hosting (Netlify, Vercel, GitHub Pages o servidor).
2. Asegura que los PDFs de `assets/` y `data/diplomas.json` estén en las rutas indicadas.
3. ¡Listo! No requiere backend.

