# CV web — Juan José Osorio Reyes

Hoja de vida web y en PDF de Juan José Osorio Reyes, estudiante de Ingeniería Multimedia (Universidad Autónoma de Occidente, Cali). Enfoque: desarrollo web, UX/UI e integración de APIs de IA.

**Sitio:** https://hv-juanjoseosorioreyes.netlify.app/

## Estructura

```
index.html            Página generada (no editar a mano: usa tools/build_site.py)
css/styles.css        Estilos (basados en la plantilla original): tema oscuro/claro, vidrio, animaciones y diseño responsive
js/app.js             Tema, menú móvil, progreso de lectura, aparición al hacer scroll, texto animado, contadores,
                      filtro de proyectos, certificados, copiar correo y volver arriba
data/cv.json          FUENTE ÚNICA del contenido (web y PDF)
data/diplomas.json    Módulos del diplomado de MinCultura
tools/build_site.py   Genera index.html a partir de data/cv.json
tools/build_cv.py     Genera los PDF a partir de data/cv.json
tools/fonts/          Fuentes del PDF (Carlito y Poppins, licencia OFL)
assets/fonts/         Fuente de la web (Inter, licencia OFL), alojada en el sitio
assets/documents/
  Juan_Jose_Osorio_Reyes_CV.pdf       Versión ATS: una columna, sin foto
  Juan_Jose_Osorio_Reyes_CV_foto.pdf  Misma información con foto
```

Orden de la página: Inicio → Sobre mí → Experiencia → Habilidades → Formación → Proyectos → Portafolio → Contacto.

## Actualizar el contenido

1. Edita `data/cv.json`.
2. Regenera la web y los PDF:
   ```bash
   pip install reportlab
   python tools/build_site.py
   python tools/build_cv.py
   ```

## Publicar

El sitio se publica en Netlify desde este repositorio (no necesita paso de compilación: `index.html` ya viene generado).
Si la URL cambia, actualízala en `data/cv.json` (`contact.site`) y vuelve a ejecutar los dos scripts: así se corrigen a la vez la URL canónica, la vista previa de LinkedIn/WhatsApp y el enlace del PDF.
