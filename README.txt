
# CV + Portafolios (Versión ordenada con animaciones mejoradas) — Juan José Osorio Reyes

Abrir `index.html` para ver el CV. Abrir `portfolio.html` para el Portafolios.
- Carpeta `assets/` ya creada con imágenes SVG de ejemplo.
- Animaciones mejoradas: hero flotante, reveal on scroll, transiciones de tarjetas.
- Sidebar con filtros y buscador en el Portafolios.
- Modo claro/oscuro con persistencia.

## Personalización rápida
- **Perfil laboral** y texto: `index.html` (sección #perfil).
- **Formación** y módulos del diplomado: `index.html` (sección #formacion).
- **Habilidades**: editar las listas en `index.html` o añadir más etiquetas.
- **Galería**: `gallery-data.json`. Cambia `thumb` por tus imágenes reales dentro de `assets/` y `link` por tus URLs.

Sugerencia: reemplaza los SVG por thumbnails JPG/PNG de tus proyectos para una vista más realista.


## Envío real de formulario (Formspree)
- Crea un formulario en Formspree y copia el **Form ID** (tiene el formato `/f/abcdxyz`).
- Abre `index.html` y reemplaza `https://formspree.io/f/XXXXXX` por tu URL real.
- Los campos `nombre`, `correo`, `mensaje` se enviarán por POST.
