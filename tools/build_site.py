"""
Genera index.html a partir de data/cv.json (la misma fuente que el PDF).

Uso:  python tools/build_site.py
Después de editar data/cv.json ejecuta también tools/build_cv.py para regenerar los PDF.

Orden de la página: Presentación → Perfil → Experiencia → Habilidades → Formación → Proyectos → Contacto.
"""
import json
from html import escape as e
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = json.loads((ROOT / "data" / "cv.json").read_text(encoding="utf-8"))
C = D["contact"]
SITE = f"https://{C['site'].rstrip('/')}/"
CV_PDF = "assets/documents/Juan_Jose_Osorio_Reyes_CV.pdf"

# ---------- Íconos SVG en línea (heredan el color del texto) ----------
GH = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 .5a11.5 11.5 0 0 0-3.64 22.41c.58.1.79-.25.79-.56v-2c-3.2.7-3.88-1.37-3.88-1.37-.53-1.33-1.29-1.69-1.29-1.69-1.05-.72.08-.7.08-.7 1.16.08 1.77 1.19 1.77 1.19 1.04 1.77 2.71 1.26 3.37.96.1-.75.4-1.26.73-1.55-2.55-.29-5.24-1.28-5.24-5.68 0-1.25.45-2.28 1.18-3.08-.12-.29-.51-1.46.11-3.04 0 0 .97-.31 3.17 1.18a11 11 0 0 1 5.77 0c2.2-1.49 3.17-1.18 3.17-1.18.62 1.58.23 2.75.11 3.04.74.8 1.18 1.83 1.18 3.08 0 4.41-2.69 5.38-5.26 5.67.41.36.78 1.06.78 2.14v3.17c0 .31.21.67.8.56A11.5 11.5 0 0 0 12 .5Z"/></svg>'
LI = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.34V9h3.42v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28ZM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 4.13ZM7.12 20.45H3.56V9h3.56v11.45ZM22.22 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.22 0Z"/></svg>'
MAIL = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2" d="M3 5h18v14H3zM3 6l9 7 9-7"/></svg>'
DL = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M12 3v12m0 0-5-5m5 5 5-5M4 20h16"/></svg>'
EXT = '<svg class="ico ico-sm" viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M14 4h6v6M20 4l-9 9M18 14v6H4V6h6"/></svg>'
THEME = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 1 0 0 20V2Z"/><circle cx="12" cy="12" r="9.2" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>'

# Pruebas reales de cada verbo del encabezado (todo sale de proyectos documentados en el CV)
VERBS = [
    ("Investigo", "Diagnóstico de usabilidad con 25 participantes para mi trabajo de grado."),
    ("Diseño", "Prototipos en Figma, identidades visuales y video para marcas locales."),
    ("Programo", "Aplicaciones web y de escritorio con Python, JavaScript, Node.js y APIs de IA."),
]


def split_list(val):
    """Separa por comas sin romper paréntesis: 'APIs de LLM (OpenAI, Anthropic)'."""
    out, depth, cur = [], 0, ""
    for ch in val:
        depth += ch == "("
        depth -= ch == ")"
        if ch == "," and depth == 0:
            out.append(cur.strip())
            cur = ""
        else:
            cur += ch
    out.append(cur.strip())
    return [x for x in out if x]


def tags(items, cls="tags"):
    return f'<ul class="{cls}">' + "".join(f"<li>{e(x)}</li>" for x in items) + "</ul>"


def ext_link(url, label):
    return f'<a class="text-link" href="https://{e(url)}" target="_blank" rel="noopener">{e(label)}{EXT}<span class="sr-only"> (se abre en otra pestaña)</span></a>'


def section(sid, title, body, extra_cls=""):
    return f'''
    <section id="{sid}" class="row {extra_cls}" aria-labelledby="{sid}-t">
      <div class="wrap row-grid">
        <h2 id="{sid}-t" class="row-title">{e(title)}</h2>
        <div class="row-body reveal">{body}
        </div>
      </div>
    </section>'''


# ---------- Bloques ----------
def hero():
    verbs = "".join(
        f'<li style="--i:{i}"><span class="verb">{e(v)}</span><span class="proof">{e(t)}</span></li>'
        for i, (v, t) in enumerate(VERBS))
    return f'''
    <section id="inicio" class="hero" aria-labelledby="nombre">
      <div class="wrap hero-grid">
        <div class="hero-main">
          <h1 id="nombre">{e(D["name"])}</h1>
          <p class="role">Estudiante de Ingeniería Multimedia en la Universidad Autónoma de Occidente. Desarrollo web y UX/UI.</p>
          <ul class="verbs" aria-label="Qué hago">{verbs}</ul>
          <div class="actions">
            <a class="btn btn-solid" href="{CV_PDF}" target="_blank" rel="noopener">{DL}<span>Descargar CV</span></a>
            <a class="btn btn-outline" href="mailto:{e(C["email"])}">{MAIL}<span>Escribirme</span></a>
            <a class="btn btn-square" href="https://{e(C["github"])}" target="_blank" rel="noopener" aria-label="GitHub (se abre en otra pestaña)">{GH}</a>
            <a class="btn btn-square" href="https://www.{e(C["linkedin"])}/" target="_blank" rel="noopener" aria-label="LinkedIn (se abre en otra pestaña)">{LI}</a>
          </div>
        </div>
        <aside class="hero-side">
          <img class="portrait" src="assets/img/profile.png" alt="Fotografía de {e(D["name"])}" width="240" height="240" />
          <dl class="facts">
            <div><dt>Universidad</dt><dd>UAO, trabajo de grado en curso</dd></div>
            <div><dt>Ubicación</dt><dd>{e(C["city"])}</dd></div>
            <div><dt>Inglés</dt><dd>B1, certificado EF SET</dd></div>
          </dl>
        </aside>
      </div>
    </section>'''


def experience():
    out = ""
    for ex in D["experience"]:
        b = "".join(f"<li>{e(x)}</li>" for x in ex["bullets"])
        out += f'''
          <article class="entry">
            <header class="entry-head">
              <h3>{e(ex["role"])}</h3>
              <p class="when">{e(ex["date"])}</p>
            </header>
            <p class="where">{e(ex["org"])}, {e(ex["place"])}</p>
            <ul class="bullets">{b}</ul>
          </article>'''
    return out


def skills():
    rows = "".join(
        f'<div class="skill"><dt>{e(lbl)}</dt><dd>{tags(split_list(val))}</dd></div>'
        for lbl, val in D["skills"])
    return f'<dl class="skills">{rows}</dl>'


def education():
    out = ""
    for ed in D["education"]:
        out += f'''
          <article class="entry">
            <header class="entry-head">
              <h3>{e(ed["title"])}</h3>
              <p class="when">{e(ed["date"])}</p>
            </header>
            <p class="where">{e(ed["org"])}</p>
            <p>{e(ed["detail"])}</p>
          </article>'''
    out += f'''
          <h3 class="sub">Certificaciones e idiomas</h3>
          <article class="entry compact">
            <header class="entry-head">
              <h4>Inglés B1 intermedio</h4>
              <p class="when">ene. 2026</p>
            </header>
            <p class="where">EF SET English Certificate, 50/100. Español nativo.</p>
            <p>{ext_link("cert.efset.org/es/2oEXjs", "Verificar certificado")}</p>
          </article>
          <article class="entry compact">
            <header class="entry-head">
              <h4>Diplomado internacional en producción de contenidos para infancia y juventud</h4>
              <p class="when">2022</p>
            </header>
            <p class="where">Ministerio de Cultura de Colombia, 8 módulos.</p>
            <details class="more">
              <summary>Ver los 8 certificados</summary>
              <div id="diploma-grid" class="diploma-grid"></div>
            </details>
          </article>'''
    return out


def project_links(links):
    if not links:
        return ""
    parts = []
    for lbl, url in links:
        label = "Ver código en GitHub" if lbl == "Código" else "Abrir sitio"
        parts.append(ext_link(url, label))
    return '<p class="links">' + "".join(parts) + "</p>"


def featured(pr):
    metrics = "".join(f"<div><dt>{e(l)}</dt><dd>{e(n)}</dd></div>" for n, l in pr["metrics"])
    case = "".join(f"<div><h5>{e(h)}</h5><p>{e(t)}</p></div>" for h, t in pr["case"])
    return f'''
          <article class="case" data-area="ux">
            <p class="case-meta">{e(pr["context"])}, {e(pr["date"])}</p>
            <h3>{e(pr["name"])}</h3>
            <p class="case-lead">Investigué los problemas de usabilidad del portal corporativo de un proveedor de internet por fibra y estoy rediseñando su experiencia a partir de la evidencia recogida con usuarios.</p>
            <dl class="metrics">{metrics}</dl>
            {tags([s.strip() for s in pr["stack"].split("·")])}
            <details class="more">
              <summary>Leer el caso de estudio</summary>
              <div class="case-grid">{case}</div>
            </details>
          </article>'''


def project_row(pr, slug, cat):
    b = "".join(f"<li>{e(x)}</li>" for x in pr["bullets"])
    when = f'<span class="p-date">{e(pr["date"])}</span>' if pr.get("date") else ""
    return f'''
            <li class="project" data-area="{slug}">
              <div class="p-head">
                <h4>{e(pr["name"])}</h4>
                <p class="p-meta"><span>{e(pr["context"])}</span>{when}</p>
              </div>
              <div class="p-body">
                <ul class="bullets">{b}</ul>
                {tags([s.strip() for s in pr["stack"].split("·")], "tags tags-sm")}
                {project_links(pr.get("links"))}
              </div>
            </li>'''


def projects():
    feat, rows = "", []
    for g in D["project_groups"]:
        for pr in g["projects"]:
            if "metrics" in pr:
                feat = featured(pr)
            else:
                rows.append(project_row(pr, g["slug"], g["category"]))
    others = [g for g in D["project_groups"] if any("metrics" not in p for p in g["projects"])]
    n_rows = len(rows)
    chips = [f'<button class="chip is-on" type="button" data-filter="all" aria-pressed="true">Todos <span>{n_rows}</span></button>']
    for g in others:
        n = sum(1 for p in g["projects"] if "metrics" not in p)
        chips.append(f'<button class="chip" type="button" data-filter="{g["slug"]}" aria-pressed="false">{e(g["category"])} <span>{n}</span></button>')
    return f'''{feat}
          <h3 class="sub">Más proyectos</h3>
          <div class="chips" role="group" aria-label="Filtrar proyectos por área">{"".join(chips)}</div>
          <p class="sr-only" aria-live="polite" id="filter-status"></p>
          <ul class="project-list">{"".join(rows)}
          </ul>
          <h3 class="sub">Diseño gráfico y audiovisual</h3>
          <p class="note">Trabajos freelance de identidad visual y video para marcas locales.</p>
          <div class="gallery">
            <figure><a href="assets/portfolio/MediaWeb_Studio.png" target="_blank" rel="noopener"><img src="assets/portfolio/MediaWeb_Studio.png" alt="Identidad visual de MediaWebStudio" loading="lazy" width="400" height="300" /></a><figcaption>MediaWebStudio, identidad visual</figcaption></figure>
            <figure><a href="assets/portfolio/mayester-sublimatie.jpg" target="_blank" rel="noopener"><img src="assets/portfolio/mayester-sublimatie.jpg" alt="Pieza gráfica para Mayester Sublimatie" loading="lazy" width="400" height="300" /></a><figcaption>Mayester Sublimatie, pieza gráfica</figcaption></figure>
            <figure><video class="hover-play" src="assets/portfolio/la-muelona.mp4" poster="assets/portfolio/la-muelona-poster.jpg" muted loop playsinline preload="none" controls aria-label="Video promocional La Muelona"></video><figcaption>La Muelona, video promocional</figcaption></figure>
            <figure><a href="assets/portfolio/saboresdemama.png" target="_blank" rel="noopener"><img src="assets/portfolio/saboresdemama.png" alt="Logotipo de Sabores de Mamá" loading="lazy" width="400" height="300" /></a><figcaption>Sabores de Mamá, logotipo</figcaption></figure>
          </div>'''


def contact():
    return f'''
          <p class="contact-lead">Si tienes una vacante en desarrollo web o UX/UI, escríbeme.</p>
          <a class="mail" href="mailto:{e(C["email"])}">{e(C["email"])}</a>
          <dl class="contact-list">
            <div><dt>Teléfono</dt><dd><a href="tel:{e(C["phone"].replace(" ", ""))}">{e(C["phone"])}</a></dd></div>
            <div><dt>LinkedIn</dt><dd>{ext_link(C["linkedin"], C["linkedin"].replace("linkedin.com", "linkedin.com"))}</dd></div>
            <div><dt>GitHub</dt><dd>{ext_link(C["github"], C["github"])}</dd></div>
            <div><dt>Ciudad</dt><dd>{e(C["city"])}</dd></div>
          </dl>
          <a class="btn btn-solid" href="{CV_PDF}" target="_blank" rel="noopener">{DL}<span>Descargar CV en PDF</span></a>'''


JSONLD = json.dumps({
    "@context": "https://schema.org", "@type": "Person", "name": D["name"],
    "jobTitle": D["headline"], "url": SITE, "image": SITE + "assets/img/profile.png",
    "email": "mailto:" + C["email"],
    "address": {"@type": "PostalAddress", "addressLocality": "Cali", "addressCountry": "CO"},
    "alumniOf": {"@type": "CollegeOrUniversity", "name": "Universidad Autónoma de Occidente"},
    "knowsAbout": ["Desarrollo web", "UX/UI", "Python", "JavaScript", "Node.js", "Figma", "APIs de IA", "Producción multimedia"],
    "sameAs": ["https://" + C["github"], "https://www." + C["linkedin"] + "/"]}, ensure_ascii=False, indent=2)

NAV = [("experiencia", "Experiencia"), ("habilidades", "Habilidades"), ("formacion", "Formación"),
       ("proyectos", "Proyectos"), ("contacto", "Contacto")]

HTML = f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{e(D["name"])}: Ingeniería Multimedia, Desarrollo Web y UX/UI</title>
  <meta name="description" content="{e(D["name"])}, estudiante de Ingeniería Multimedia (UAO, Cali) enfocado en desarrollo web, diseño UX/UI e integración de APIs de IA. Experiencia, habilidades, proyectos y CV en PDF." />
  <meta name="theme-color" content="#0b3d62" />
  <meta name="color-scheme" content="light dark" />
  <link rel="canonical" href="{SITE}" />
  <link rel="icon" href="assets/icons/favicon.svg" type="image/svg+xml" />

  <meta property="og:type" content="profile" />
  <meta property="og:title" content="{e(D["name"])}: Desarrollo Web y UX/UI" />
  <meta property="og:description" content="Ingeniería Multimedia (UAO). Desarrollo web, UX/UI e IA aplicada." />
  <meta property="og:url" content="{SITE}" />
  <meta property="og:image" content="{SITE}assets/img/profile.png" />
  <meta property="og:locale" content="es_CO" />

  <script type="application/ld+json">
{JSONLD}
  </script>

  <!-- Aplica el tema guardado antes de pintar, para evitar un parpadeo -->
  <script>
    try {{ var t = localStorage.getItem('theme'); if (t) document.documentElement.dataset.theme = t; }} catch (err) {{}}
    document.documentElement.classList.add('js');
  </script>

  <!-- Fuentes alojadas en el propio sitio (más rápido y sin depender de terceros) -->
  <link rel="preload" href="assets/fonts/sora-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin />
  <link rel="preload" href="assets/fonts/source-sans-3-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin />
  <link rel="stylesheet" href="css/styles.css" />
</head>
<body>
  <a class="skip" href="#main">Saltar al contenido</a>

  <header class="top">
    <div class="wrap top-in">
      <a class="brand" href="#inicio">Juan José Osorio Reyes</a>
      <nav class="nav" aria-label="Secciones">
        {"".join(f'<a href="#{i}">{t}</a>' for i, t in NAV)}
      </nav>
      <div class="top-actions">
        <button class="btn btn-square btn-ghost" id="theme" type="button" aria-label="Cambiar entre tema claro y oscuro">{THEME}</button>
        <a class="btn btn-solid btn-sm" href="{CV_PDF}" target="_blank" rel="noopener">{DL}<span>CV</span></a>
      </div>
    </div>
  </header>

  <main id="main">
{hero()}
{section("perfil", "Perfil", f'<p class="summary">{e(D["summary"])}</p>')}
{section("experiencia", "Experiencia", experience())}
{section("habilidades", "Habilidades", skills())}
{section("formacion", "Formación", education())}
{section("proyectos", "Proyectos", projects())}
{section("contacto", "Contacto", contact(), "row-contact")}
  </main>

  <footer class="foot">
    <div class="wrap foot-in">
      <small>© <span id="year">2026</span> {e(D["name"])}</small>
      <a class="text-link" href="#inicio">Volver arriba</a>
    </div>
  </footer>

  <div id="lightbox" class="lightbox" hidden role="dialog" aria-modal="true" aria-label="Vista del certificado">
    <div class="lightbox-body">
      <button class="lightbox-close btn btn-square" type="button" aria-label="Cerrar">×</button>
      <img id="lightbox-img" alt="" />
      <iframe id="lightbox-pdf" title="Certificado en PDF"></iframe>
    </div>
  </div>

  <script src="js/app.js" defer></script>
</body>
</html>
'''

(ROOT / "index.html").write_text(HTML, encoding="utf-8")
print("OK index.html")
