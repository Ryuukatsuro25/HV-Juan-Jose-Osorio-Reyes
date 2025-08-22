
# Carpeta: CV + Portafolios — Juan José Osorio Reyes

Abrir `index.html` en tu navegador para ver el **CV interactivo**.
Abrir `portfolio.html` para ver el **Portafolios** con galerías por categoría.

## Cómo personalizar
- **Texto del CV**: edita `index.html` (secciones Perfil, Formación y Habilidades).
- **Habilidades**: busca el contenedor `<div class="tags">` o ajusta la lista en `styles.css` para estilos.
- **Portafolios**: edita `gallery-data.json`. Cada categoría tiene un campo `description` y una lista `items`.
  - Reemplaza `thumb` por la ruta de tu imagen (por ejemplo, `assets/mi-render.jpg`).
  - Cambia `link` para dirigir a un video de YouTube, itch.io, repositorio, etc.

## Imágenes
Actualmente se usan **placeholders** (SVG embebidos). Para usar tus imágenes:
1. Crea la carpeta `assets/` junto a estos archivos.
2. Copia tus imágenes allí.
3. Reemplaza el campo `thumb` de cada item en `gallery-data.json` con `assets/tu-imagen.jpg`.

## Modo claro/oscuro
Usa el botón 🌓 en el menú para alternar el tema. La preferencia queda guardada en el navegador.

## Estructura
- `index.html` — CV con hero, perfil, formación, habilidades y contacto.
- `portfolio.html` — Portafolios con filtros y buscador.
- `styles.css` — Estilos globales, responsive y accesibles.
- `main.js` — Interactividad del CV (menú, tema, formulario demo).
- `portfolio.js` — Interactividad del portafolios (filtros, lightbox).
- `gallery-data.json` — Datos de las galerías por categoría.

¡Éxitos con tus postulaciones y proyectos!
