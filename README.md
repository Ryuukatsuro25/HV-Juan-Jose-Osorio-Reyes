# CV web — Juan José Osorio Reyes

Hoja de vida web y en PDF de Juan José Osorio Reyes, estudiante de Ingeniería Multimedia (Universidad Autónoma de Occidente, Cali). Enfoque: desarrollo web, UX/UI e integración de APIs de IA.

**Sitio:** https://ryuukatsuro25.github.io/HV-Juan-Jose-Osorio-Reyes/

## Estructura

```
index.html                     Página (orden: Inicio → Proyectos → Experiencia → Habilidades → Formación → Portafolio gráfico → Contacto)
css/styles.css                 Estilos (tema claro/oscuro)
js/app.js                      Tema, animaciones, certificados del diplomado y video al pasar el cursor
data/cv.json                   FUENTE ÚNICA del contenido del CV en PDF
data/diplomas.json             Módulos del diplomado de MinCultura
tools/build_cv.py              Genera los PDF a partir de data/cv.json
tools/fonts/                   Fuentes incrustadas en el PDF (Carlito y Poppins, licencia OFL)
assets/documents/
  Juan_Jose_Osorio_Reyes_CV.pdf       Versión ATS: una columna, sin foto (para portales de empleo)
  Juan_Jose_Osorio_Reyes_CV_foto.pdf  Misma información con foto (para enviar directamente)
```

## Actualizar el CV

1. Edita `data/cv.json`.
2. Regenera los PDF:
   ```bash
   pip install reportlab
   python tools/build_cv.py
   ```
3. Si cambiaste proyectos, habilidades o fechas, actualiza lo mismo en `index.html` (los proyectos están agrupados por área igual que en el PDF) para que la web y el PDF digan exactamente lo mismo.

## Publicar en GitHub Pages

Settings → Pages → Source: *Deploy from a branch* → rama `main`, carpeta `/ (root)`.
Si la URL final es distinta a la de arriba, cámbiala en `index.html` (`canonical`, `og:url`, `og:image` y JSON-LD) y en `data/cv.json` (`contact.site`), y vuelve a generar los PDF.
