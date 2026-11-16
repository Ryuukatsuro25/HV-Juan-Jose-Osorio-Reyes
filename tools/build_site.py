"""
Genera index.html a partir de data/cv.json (la misma fuente que el PDF).

Uso:  python tools/build_site.py
Después de editar data/cv.json ejecuta también tools/build_cv.py para regenerar los PDF.

Orden: Inicio → Sobre mí → Experiencia → Habilidades → Formación → Proyectos → Portafolio → Contacto.
"""
import json
from html import escape as e
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = json.loads((ROOT / "data" / "cv.json").read_text(encoding="utf-8"))
C = D["contact"]
SITE = f"https://{C['site'].rstrip('/')}/"
CV_PDF = "assets/documents/Juan_Jose_Osorio_Reyes_CV.pdf"
VISIBLE_PROJECTS = 6  # proyectos visibles antes de pulsar "Ver todos"

# ---------- Íconos SVG en línea ----------
def svg(path, fill=False, w=24):
    if fill:
        return f'<svg class="ico" viewBox="0 0 {w} {w}" aria-hidden="true"><path fill="currentColor" d="{path}"/></svg>'
    return (f'<svg class="ico" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{path}</svg>')

GH = svg("M12 .5a11.5 11.5 0 0 0-3.64 22.41c.58.1.79-.25.79-.56v-2c-3.2.7-3.88-1.37-3.88-1.37-.53-1.33-1.29-1.69-1.29-1.69-1.05-.72.08-.7.08-.7 1.16.08 1.77 1.19 1.77 1.19 1.04 1.77 2.71 1.26 3.37.96.1-.75.4-1.26.73-1.55-2.55-.29-5.24-1.28-5.24-5.68 0-1.25.45-2.28 1.18-3.08-.12-.29-.51-1.46.11-3.04 0 0 .97-.31 3.17 1.18a11 11 0 0 1 5.77 0c2.2-1.49 3.17-1.18 3.17-1.18.62 1.58.23 2.75.11 3.04.74.8 1.18 1.83 1.18 3.08 0 4.41-2.69 5.38-5.26 5.67.41.36.78 1.06.78 2.14v3.17c0 .31.21.67.8.56A11.5 11.5 0 0 0 12 .5Z", fill=True)
LI = svg("M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.34V9h3.42v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28ZM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 4.13ZM7.12 20.45H3.56V9h3.56v11.45ZM22.22 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.22 0Z", fill=True)
MAIL = svg('<path d="M3 5h18v14H3z"/><path d="m3 6 9 7 9-7"/>')
DL = svg('<path d="M12 3v12m0 0-5-5m5 5 5-5M4 20h16"/>')
EXT = svg('<path d="M14 4h6v6M20 4l-9 9M18 14v6H4V6h6"/>')
COPY = svg('<rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15V5a1 1 0 0 1 1-1h10"/>')
PIN = svg('<path d="M12 21s-7-6.1-7-11a7 7 0 0 1 14 0c0 4.9-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>')
PHONE = svg('<path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A17 17 0 0 1 3 5a2 2 0 0 1 2-2"/>')
UP = svg('<path d="m6 14 6-6 6 6"/>')
SUN = svg('<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>')
MOON = svg('<path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/>')
CHEV = svg('<path d="m6 9 6 6 6-6"/>')

SKILL_ICONS = {
    "Lenguajes": svg('<path d="m8 8-5 4 5 4M16 8l5 4-5 4M14 4l-4 16"/>'),
    "Web y backend": svg('<rect x="3" y="4" width="18" height="7" rx="1.5"/><rect x="3" y="13" width="18" height="7" rx="1.5"/><path d="M7 7.5h.01M7 16.5h.01"/>'),
    "IA y datos": svg('<path d="M12 3l1.8 4.7L18.5 9.5l-4.7 1.8L12 16l-1.8-4.7L5.5 9.5l4.7-1.8z"/><path d="M19 15l.8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8z"/>'),
    "Herramientas": svg('<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.6 2.6-2.4-.6-.6-2.4z"/>'),
    "UX/UI": svg('<rect x="3" y="3" width="18" height="14" rx="2"/><path d="M8 21h8M12 17v4M7 8h6M7 12h10"/>'),
    "Redes": svg('<circle cx="12" cy="5" r="2"/><circle cx="5" cy="19" r="2"/><circle cx="19" cy="19" r="2"/><path d="M12 7v4M12 11l-6 6M12 11l6 6"/>'),
    "Multimedia": svg('<rect x="3" y="5" width="14" height="14" rx="2"/><path d="m17 10 4-2v8l-4-2"/>'),
}
GAME = svg('<rect x="2" y="7" width="20" height="11" rx="5"/><path d="M7 11v3M5.5 12.5h3M15.5 12h.01M18 13.5h.01"/>')
AREA_ICON = {"web": "Web y backend", "software": "IA y datos", "redes": "Redes", "ux": "UX/UI"}
AREA_LABEL = {"ux": "UX/UI", "web": "Web", "software": "Software e IA", "juegos": "Videojuegos", "redes": "Redes"}

# Frases del titular que se escriben y borran en el inicio (todas salen del CV)
ROLES = ["Desarrollo web", "Diseño UX/UI", "Integración de APIs de IA", "Producción multimedia"]


def split_list(val):
    """Separa por comas sin romper paréntesis: 'APIs de LLM (OpenAI, Anthropic)'."""
    out, depth, cur = [], 0, ""
    for ch in val:
        depth += ch == "("
        depth -= ch == ")"
        if ch == "," and depth == 0:
            out.append(cur.strip()); cur = ""
        else:
            cur += ch
    out.append(cur.strip())
    return [x for x in out if x]


def tags(items, cls="tags"):
    return f'<ul class="{cls}">' + "".join(f'<li style="--i:{i}">{e(x)}</li>' for i, x in enumerate(items)) + "</ul>"


def head(title, sub=""):
    s = f'<p class="section-sub">{e(sub)}</p>' if sub else ""
    return f'<header class="section-head reveal"><h2 class="section-title">{e(title)}</h2>{s}</header>'


# ---------- Secciones ----------
def hero():
    roles = e(json.dumps(ROLES, ensure_ascii=False))
    return f'''
    <section id="inicio" class="hero" aria-labelledby="nombre">
      <div class="hero-bg" aria-hidden="true">
        <span class="blob b1"></span><span class="blob b2"></span><span class="blob b3"></span>
        <span class="grid-bg"></span>
      </div>

      <div class="container">
        <div class="hero-card">
          <div class="avatar-wrap load" style="--d:0">
            <img src="assets/img/profile.png" alt="Fotografía de {e(D["name"])}" class="avatar" width="168" height="168" />
          </div>
          <div class="hero-text">
            <p class="hello load" style="--d:1">Hola, soy</p>
            <h1 id="nombre" class="display load" style="--d:2">{e(D["name"])}</h1>
            <p class="role load" style="--d:3">
              <span class="sr-only">Estudiante de Ingeniería Multimedia: desarrollo web, diseño UX/UI, integración de APIs de IA y producción multimedia.</span>
              <span aria-hidden="true">Ingeniería Multimedia · <span class="typed" data-roles="{roles}">{e(ROLES[0])}</span><span class="caret"></span></span>
            </p>
            <p class="tagline load" style="--d:4">Diseño y construyo productos web, desde la investigación con usuarios hasta el código desplegado.</p>
            <ul class="badges load" style="--d:4" aria-label="Datos rápidos">
              <li>{PIN}<span>{e(C["city"])}</span></li>
              <li><span>UAO · Trabajo de grado en curso</span></li>
              <li><span>Inglés B1</span></li>
            </ul>
            <div class="hero-actions load" style="--d:5">
              <a class="btn primary" href="{CV_PDF}" target="_blank" rel="noopener">{DL}<span>Descargar CV</span></a>
              <a class="btn ghost" href="#contacto">{MAIL}<span>Contactar</span></a>
              <a class="btn icon-only" href="https://{e(C["github"])}" target="_blank" rel="noopener" aria-label="GitHub (se abre en otra pestaña)">{GH}</a>
              <a class="btn icon-only" href="https://www.{e(C["linkedin"])}/" target="_blank" rel="noopener" aria-label="LinkedIn (se abre en otra pestaña)">{LI}</a>
            </div>
          </div>
        </div>
      </div>
      <a class="scroll-hint" href="#sobre-mi" aria-label="Ir a Sobre mí"><span></span></a>
    </section>'''


def about():
    n_projects = sum(len(g["projects"]) for g in D["project_groups"])
    stats = [(n_projects, "", "proyectos documentados"), (25, "", "participantes en mi investigación UX"), (4, "+", "años como freelance (desde 2022)")]
    stat_html = "".join(
        f'<div class="stat card spot reveal" style="--d:{i}"><span class="stat-n"><span data-count="{n}">{n}</span>{suf}</span><span class="stat-l">{e(l)}</span></div>'
        for i, (n, suf, l) in enumerate(stats))
    return f'''
    <section id="sobre-mi" class="section">
      <div class="container">
        {head("Sobre mí")}
        <div class="about-grid">
          <div class="card lead reveal"><p>{e(D["summary"])}</p></div>
          <div class="stats">{stat_html}</div>
        </div>
      </div>
    </section>'''


def experience():
    items = ""
    for ex in D["experience"]:
        b = "".join(f"<li>{e(x)}</li>" for x in ex["bullets"])
        items += f'''
          <article class="tl-item reveal">
            <span class="tl-dot" aria-hidden="true"></span>
            <div class="card">
              <header class="tl-head">
                <h3>{e(ex["role"])}</h3>
                <span class="pill">{e(ex["date"])}</span>
              </header>
              <p class="meta">{e(ex["org"])}, {e(ex["place"])}</p>
              <ul class="tl-body">{b}</ul>
            </div>
          </article>'''
    return f'''
    <section id="experiencia" class="section alt">
      <div class="container">
        {head("Experiencia")}
        <div class="timeline">{items}
        </div>
      </div>
    </section>'''


def skills():
    cards = "".join(f'''
          <article class="card skill-card spot reveal" style="--d:{i % 3}">
            <div class="skill-head"><span class="skill-ico">{SKILL_ICONS.get(lbl, "")}</span><h3>{e(lbl)}</h3></div>
            {tags(split_list(val))}
          </article>''' for i, (lbl, val) in enumerate(D["skills"]))
    return f'''
    <section id="habilidades" class="section">
      <div class="container">
        {head("Habilidades", "Las mismas que aparecen en mi CV, agrupadas por área.")}
        <div class="grid skills-grid">{cards}
        </div>
      </div>
    </section>'''


def education():
    ed = D["education"][0]
    return f'''
    <section id="formacion" class="section alt">
      <div class="container">
        {head("Formación")}
        <div class="grid edu-grid">
          <article class="card edu-main spot reveal">
            <span class="pill">{e(ed["date"])}</span>
            <h3>{e(ed["title"])}</h3>
            <p class="meta">{e(ed["org"])}</p>
            <p>{e(ed["detail"])}</p>
          </article>
          <article class="card spot reveal" style="--d:1">
            <span class="pill">ene. 2026</span>
            <h3>Inglés B1 intermedio</h3>
            <p class="meta">EF SET English Certificate · 50/100</p>
            <p>Español nativo.</p>
            <a class="link" href="https://cert.efset.org/es/2oEXjs" target="_blank" rel="noopener">Verificar certificado{EXT}</a>
          </article>
          <article class="card spot reveal" style="--d:2">
            <span class="pill">2022</span>
            <h3>Diplomado en producción de contenidos para infancia y juventud</h3>
            <p class="meta">Ministerio de Cultura de Colombia · 8 módulos</p>
            <button class="link as-btn" type="button" id="open-diplomas" aria-expanded="false" aria-controls="diploma-panel">Ver los 8 certificados{CHEV}</button>
          </article>
        </div>
        <div id="diploma-panel" class="diploma-panel" hidden>
          <div id="diploma-grid" class="grid diploma-grid"></div>
        </div>
      </div>
    </section>'''


def project_links(links):
    if not links:
        return ""
    out = []
    for lbl, url in links:
        if lbl == "Código":
            out.append(f'<a class="link" href="https://{e(url)}" target="_blank" rel="noopener">{GH}<span>Código</span></a>')
        else:
            out.append(f'<a class="link" href="https://{e(url)}" target="_blank" rel="noopener">{EXT}<span>Ver sitio</span></a>')
    return '<div class="p-links">' + "".join(out) + "</div>"


def featured(pr):
    metrics = "".join(
        f'<div class="metric"><span class="metric-n" data-count="{e(n)}">{e(n)}</span><span class="metric-l">{e(l)}</span></div>'
        for n, l in pr["metrics"])
    case = "".join(f"<div><h4>{e(h)}</h4><p>{e(t)}</p></div>" for h, t in pr["case"])
    return f'''
        <article class="card featured spot reveal" data-area="ux">
          <div class="featured-top">
            <div>
              <span class="area-tag area-ux">Caso de estudio · UX/UI</span>
              <h3>{e(pr["name"])}</h3>
              <p class="meta">{e(pr["context"])} · {e(pr["date"])}</p>
              <p>Investigué los problemas de usabilidad del portal corporativo de un proveedor de internet por fibra y estoy rediseñando su experiencia a partir de la evidencia recogida con usuarios.</p>
              {tags([s.strip() for s in pr["stack"].split("·")])}
            </div>
            <div class="metrics">{metrics}</div>
          </div>
          <details class="case">
            <summary>Leer el caso de estudio{CHEV}</summary>
            <div class="case-grid">{case}</div>
          </details>
        </article>'''


def project_card(pr, slug, idx):
    extra = " is-extra" if idx >= VISIBLE_PROJECTS else ""
    when = f' · {e(pr["date"])}' if pr.get("date") else ""
    stack = [s.strip() for s in pr["stack"].split("·")][:4]
    return f'''
          <article class="card project spot{extra}" data-area="{slug}">
            <div class="p-cover area-bg-{slug}" aria-hidden="true"><span class="p-ico">{GAME if slug == "juegos" else SKILL_ICONS[AREA_ICON[slug]]}</span></div>
            <div class="p-body">
              <span class="area-tag area-{slug}">{e(AREA_LABEL[slug])}</span>
              <h3>{e(pr["name"])}</h3>
              <p class="meta">{e(pr["context"])}{when}</p>
              <p class="p-desc">{e(pr["bullets"][0])}</p>
              {tags(stack, "tags tags-sm")}
              {project_links(pr.get("links"))}
            </div>
          </article>'''


def projects():
    feat, cards, idx = "", [], 0
    for g in D["project_groups"]:
        for pr in g["projects"]:
            if "metrics" in pr:
                feat = featured(pr)
            else:
                cards.append(project_card(pr, g["slug"], idx)); idx += 1
    chips = [f'<button class="chip is-on" type="button" data-filter="all" aria-pressed="true">Todos <span>{idx}</span></button>']
    for g in D["project_groups"]:
        n = sum(1 for p in g["projects"] if "metrics" not in p)
        if n:
            chips.append(f'<button class="chip" type="button" data-filter="{g["slug"]}" aria-pressed="false">{e(AREA_LABEL[g["slug"]])} <span>{n}</span></button>')
    more = (f'<div class="more-wrap"><button class="btn ghost" id="show-all" type="button" aria-expanded="false">'
            f'<span>Ver todos los proyectos ({idx})</span>{CHEV}</button></div>') if idx > VISIBLE_PROJECTS else ""
    return f'''
    <section id="proyectos" class="section">
      <div class="container">
        {head("Proyectos", "Qué hice, con qué herramientas y dónde verlo.")}
        {feat}
        <div class="chips reveal" role="group" aria-label="Filtrar proyectos por área">{"".join(chips)}</div>
        <p class="sr-only" aria-live="polite" id="filter-status"></p>
        <div class="grid projects-grid" id="projects-grid">{"".join(cards)}
        </div>
        {more}
      </div>
    </section>'''


def portfolio():
    items = [
        ("assets/portfolio/MediaWeb_Studio.png", "Identidad visual de MediaWebStudio", "MediaWebStudio", "Identidad visual", "img"),
        ("assets/portfolio/mayester-sublimatie.jpg", "Pieza gráfica para Mayester Sublimatie", "Mayester Sublimatie", "Pieza gráfica", "img"),
        ("assets/portfolio/la-muelona.mp4", "Video promocional La Muelona", "La Muelona", "Video promocional", "video"),
        ("assets/portfolio/saboresdemama.png", "Logotipo de Sabores de Mamá", "Sabores de Mamá", "Logotipo", "img"),
    ]
    figs = ""
    for i, (src, alt, t, k, kind) in enumerate(items):
        media = (f'<video class="g-media hover-play" src="{src}" poster="assets/portfolio/la-muelona-poster.jpg" muted loop playsinline preload="none" aria-label="{e(alt)}"></video>'
                 if kind == "video" else f'<img class="g-media" src="{src}" alt="{e(alt)}" loading="lazy" width="400" height="300" />')
        figs += f'''
          <figure class="g-item reveal" style="--d:{i}">
            <a href="{src}" target="_blank" rel="noopener" aria-label="Abrir {e(t)}, {e(k.lower())}">{media}</a>
            <figcaption><strong>{e(t)}</strong><span>{e(k)}</span></figcaption>
          </figure>'''
    return f'''
    <section id="portafolio" class="section alt">
      <div class="container">
        {head("Portafolio gráfico y audiovisual", "Trabajos freelance de identidad visual y video para marcas locales.")}
        <div class="grid gallery">{figs}
        </div>
      </div>
    </section>'''


def contact():
    return f'''
    <section id="contacto" class="section">
      <div class="container narrow">
        <div class="card contact-card spot reveal">
          <h2 class="section-title">¿Hablamos?</h2>
          <p>Si tienes una vacante en desarrollo web o UX/UI, escríbeme.</p>
          <div class="mail-row">
            <a class="mail" href="mailto:{e(C["email"])}">{e(C["email"])}</a>
            <button class="btn icon-only" type="button" id="copy-mail" data-mail="{e(C["email"])}" aria-label="Copiar correo">{COPY}</button>
          </div>
          <ul class="contact-list">
            <li><a href="tel:{e(C["phone"].replace(" ", ""))}">{PHONE}<span>{e(C["phone"])}</span></a></li>
            <li><a href="https://www.{e(C["linkedin"])}/" target="_blank" rel="noopener">{LI}<span>LinkedIn</span></a></li>
            <li><a href="https://{e(C["github"])}" target="_blank" rel="noopener">{GH}<span>GitHub</span></a></li>
            <li><span>{PIN}<span>{e(C["city"])}</span></span></li>
          </ul>
          <a class="btn primary" href="{CV_PDF}" target="_blank" rel="noopener">{DL}<span>Descargar CV en PDF</span></a>
        </div>
      </div>
    </section>'''


JSONLD = json.dumps({
    "@context": "https://schema.org", "@type": "Person", "name": D["name"],
    "jobTitle": D["headline"], "url": SITE, "image": SITE + "assets/img/profile.png",
    "email": "mailto:" + C["email"],
    "address": {"@type": "PostalAddress", "addressLocality": "Cali", "addressCountry": "CO"},
    "alumniOf": {"@type": "CollegeOrUniversity", "name": "Universidad Autónoma de Occidente"},
    "knowsAbout": ["Desarrollo web", "UX/UI", "Python", "JavaScript", "Node.js", "Figma", "APIs de IA", "Producción multimedia"],
    "sameAs": ["https://" + C["github"], "https://www." + C["linkedin"] + "/"]}, ensure_ascii=False, indent=2)

NAV = [("sobre-mi", "Sobre mí"), ("experiencia", "Experiencia"), ("habilidades", "Habilidades"),
       ("formacion", "Formación"), ("proyectos", "Proyectos"), ("contacto", "Contacto")]

HTML = f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{e(D["name"])}: Ingeniería Multimedia, Desarrollo Web y UX/UI</title>
  <meta name="description" content="{e(D["name"])}, estudiante de Ingeniería Multimedia (UAO, Cali) enfocado en desarrollo web, diseño UX/UI e integración de APIs de IA. Experiencia, habilidades, proyectos y CV en PDF." />
  <meta name="theme-color" content="#0b0e14" />
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

  <!-- Tema guardado y bandera de JS antes de pintar (evita parpadeos) -->
  <script>
    document.documentElement.classList.add('js');
    try {{ if (localStorage.getItem('theme') === 'light') document.documentElement.classList.add('light'); }} catch (err) {{}}
  </script>

  <link rel="preload" href="assets/fonts/inter-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin />
  <link rel="preload" href="assets/fonts/inter-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin />
  <link rel="stylesheet" href="css/styles.css" />
</head>
<body>
  <a class="skip-link" href="#main">Saltar al contenido</a>
  <div class="progress" aria-hidden="true"></div>

  <header class="site-header">
    <div class="container nav-wrap">
      <a href="#inicio" class="brand" aria-label="Ir al inicio">JJ<span>O</span></a>
      <nav class="main-nav" id="main-nav" aria-label="Navegación principal">
        {"".join(f'<a href="#{i}">{t}</a>' for i, t in NAV)}
      </nav>
      <div class="nav-actions">
        <button id="themeToggle" class="icon-btn" type="button" aria-label="Cambiar a tema claro">
          <span class="i-sun">{SUN}</span><span class="i-moon">{MOON}</span>
        </button>
        <button id="menuToggle" class="icon-btn menu-btn" type="button" aria-label="Abrir menú" aria-expanded="false" aria-controls="main-nav">
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>
  </header>

  <main id="main">
{hero()}
{about()}
{experience()}
{skills()}
{education()}
{projects()}
{portfolio()}
{contact()}
  </main>

  <footer class="site-footer">
    <div class="container footer-wrap">
      <small>© <span id="year">2026</span> {e(D["name"])} · Ingeniería Multimedia</small>
      <nav class="footer-nav" aria-label="Pie de página">
        <a href="#inicio">Inicio</a><a href="#proyectos">Proyectos</a><a href="#contacto">Contacto</a>
      </nav>
    </div>
  </footer>

  <button class="to-top" type="button" aria-label="Volver arriba">{UP}</button>
  <div class="toast" role="status" aria-live="polite"></div>

  <div id="lightbox" class="lightbox" hidden role="dialog" aria-modal="true" aria-label="Vista del certificado">
    <div class="lightbox-body">
      <button class="lightbox-close" type="button" aria-label="Cerrar">×</button>
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
