"""
Genera las dos versiones del CV en PDF a partir de data/cv.json:

  assets/documents/Juan_Jose_Osorio_Reyes_CV.pdf       -> versión ATS (una columna, sin foto)
  assets/documents/Juan_Jose_Osorio_Reyes_CV_foto.pdf  -> misma información, con foto

Diseño: una sola columna (compatible con ATS), fuentes incrustadas (Carlito + Poppins),
encabezado con banda de color, proyectos agrupados por categoría y fechas alineadas a la derecha.

Uso:  pip install reportlab   y luego   python tools/build_cv.py
"""
import json
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (Image, KeepTogether, ListFlowable, ListItem,
                                Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)

ROOT = Path(__file__).resolve().parent.parent
FONTS = Path(__file__).resolve().parent / "fonts"
DATA = json.loads((ROOT / "data" / "cv.json").read_text(encoding="utf-8"))
OUT_DIR = ROOT / "assets" / "documents"
PHOTO = ROOT / "assets" / "img" / "profile.png"

# ---------- Fuentes (incrustadas en el PDF) ----------
pdfmetrics.registerFont(TTFont("Body", str(FONTS / "Carlito-Regular.ttf")))
pdfmetrics.registerFont(TTFont("Body-Bold", str(FONTS / "Carlito-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Body-Italic", str(FONTS / "Carlito-Italic.ttf")))
pdfmetrics.registerFont(TTFont("Head", str(FONTS / "Poppins-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Head-Med", str(FONTS / "Poppins-Medium.ttf")))
pdfmetrics.registerFontFamily("Body", normal="Body", bold="Body-Bold", italic="Body-Italic", boldItalic="Body-Bold")

# ---------- Paleta ----------
NAVY = HexColor("#0b3d62")
ACCENT = HexColor("#1f6fb2")
INK = HexColor("#1f2937")
MUTED = HexColor("#5b6472")
SOFT = HexColor("#e8f0f8")
LIGHT_TXT = HexColor("#d6e6f5")

PAGE_W, PAGE_H = letter
MARGIN_X = 1.6 * cm
CONTENT_W = PAGE_W - 2 * MARGIN_X - 12  # 12 = padding interno del frame (6 pt por lado)

S = {
    "name": ParagraphStyle("name", fontName="Head", fontSize=22, leading=26, textColor=white),
    "headline": ParagraphStyle("headline", fontName="Head-Med", fontSize=10.5, leading=14, textColor=LIGHT_TXT),
    "contact": ParagraphStyle("contact", fontName="Body", fontSize=9.6, leading=12.5, textColor=white),
    "h": ParagraphStyle("h", fontName="Head", fontSize=11, leading=14, textColor=NAVY),
    "cat": ParagraphStyle("cat", fontName="Head-Med", fontSize=9.4, leading=12, textColor=ACCENT, spaceBefore=4, spaceAfter=1),
    "body": ParagraphStyle("body", fontName="Body", fontSize=9.8, leading=12.3, textColor=INK),
    "title": ParagraphStyle("title", fontName="Body-Bold", fontSize=10.6, leading=13, textColor=INK),
    "date": ParagraphStyle("date", fontName="Body", fontSize=9.4, leading=13, textColor=MUTED, alignment=TA_RIGHT),
    "meta": ParagraphStyle("meta", fontName="Body-Italic", fontSize=9, leading=11.2, textColor=MUTED),
    "bullet": ParagraphStyle("bullet", fontName="Body", fontSize=9.7, leading=12, textColor=INK),
    "skill_l": ParagraphStyle("skill_l", fontName="Body-Bold", fontSize=9.9, leading=12.4, textColor=NAVY),
}


def p(text, style):
    return Paragraph(text, S[style])


def a(url, label=None, color="#0b3d62"):
    return f'<a href="https://{url}" color="{color}">{escape(label or url)}</a>'


def heading(title):
    """Encabezado de sección: texto + línea de acento."""
    t = Table([[p(escape(title.upper()), "h")]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -1), 1.2, NAVY),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    return [Spacer(1, 7), t, Spacer(1, 3)]


def title_row(left, right):
    """Título a la izquierda y fecha alineada a la derecha."""
    t = Table([[p(left, "title"), p(escape(right), "date")]], colWidths=[CONTENT_W - 3.6 * cm, 3.6 * cm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return t


def bullets(items):
    return ListFlowable(
        [ListItem(p(escape(b), "bullet"), leftIndent=11, value="•") for b in items],
        bulletType="bullet", bulletFontName="Body-Bold", bulletFontSize=9,
        bulletColor=ACCENT, leftIndent=11, start="•")


def header(with_photo):
    c = DATA["contact"]
    lt = "#ffffff"
    line1 = "  |  ".join([escape(c["city"]), escape(c["phone"]),
                          f'<a href="mailto:{c["email"]}" color="{lt}">{escape(c["email"])}</a>'])
    line2 = "  |  ".join([a(c["linkedin"], color=lt), a(c["github"], color=lt)])
    line3 = "Portafolio web: " + a(c["site"], color=lt)
    text = [p(escape(DATA["name"]), "name"), p(escape(DATA["headline"]), "headline"),
            Spacer(1, 5), p(line1, "contact"), p(line2, "contact"), p(line3, "contact")]

    if with_photo and PHOTO.exists():
        cells, widths = [[text, Image(str(PHOTO), width=2.7 * cm, height=2.7 * cm)]], [CONTENT_W - 3.1 * cm, 3.1 * cm]
    else:
        cells, widths = [[text]], [CONTENT_W]
    t = Table(cells, colWidths=widths)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (0, -1), 14), ("RIGHTPADDING", (-1, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 12), ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("ALIGN", (-1, 0), (-1, -1), "RIGHT"),
    ]))
    return [t]


def skills_table():
    rows = [[p(escape(lbl), "skill_l"), p(escape(val), "body")] for lbl, val in DATA["skills"]]
    t = Table(rows, colWidths=[3.75 * cm, CONTENT_W - 3.75 * cm])
    style = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
    ]
    for i in range(0, len(rows), 2):
        style.append(("BACKGROUND", (0, i), (-1, i), SOFT))
    t.setStyle(TableStyle(style))
    return t


def project_block(pr):
    title = escape(pr["name"])
    if pr.get("context"):
        title += f' <font name="Body" color="#5b6472">· {escape(pr["context"])}</font>'
    parts = [title_row(title, pr.get("date", "")), p(escape(pr["stack"]), "meta"), bullets(pr["bullets"])]
    if pr.get("links"):
        links = "   ".join(f'<b>{escape(lbl)}:</b> {a(url)}' for lbl, url in pr["links"])
        parts.append(p(links, "meta"))
    parts.append(Spacer(1, 3))
    return parts


def story(with_photo):
    st = header(with_photo)

    st += heading("Perfil profesional")
    st.append(p(escape(DATA["summary"]), "body"))

    st += heading("Habilidades técnicas")
    st.append(skills_table())

    for i, ex in enumerate(DATA["experience"]):
        title = f'{escape(ex["role"])} <font name="Body" color="#5b6472">· {escape(ex["org"])}, {escape(ex["place"])}</font>'
        st.append(KeepTogether((heading("Experiencia") if i == 0 else [])
                               + [title_row(title, ex["date"]), Spacer(1, 2), bullets(ex["bullets"])]))

    for gi, g in enumerate(DATA["project_groups"]):
        for pi, pr in enumerate(g["projects"]):
            block = []
            if gi == 0 and pi == 0:
                block += heading("Proyectos")   # el título de sección nunca queda huérfano
            if pi == 0:
                block.append(p(escape(g["category"]), "cat"))
            block += project_block(pr)
            st.append(KeepTogether(block))

    for i, ed in enumerate(DATA["education"]):
        title = f'{escape(ed["title"])} <font name="Body" color="#5b6472">· {escape(ed["org"])}</font>'
        st.append(KeepTogether((heading("Educación") if i == 0 else [])
                               + [title_row(title, ed["date"]), p(escape(ed["detail"]), "body")]))

    certs = heading("Certificaciones e idiomas")
    rows = [[p(f"<b>{escape(n)}</b> · {escape(o)}", "body"), p(escape(dt), "date")] for n, o, dt in DATA["certifications"]]
    t = Table(rows, colWidths=[CONTENT_W - 3.6 * cm, 3.6 * cm])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                           ("TOPPADDING", (0, 0), (-1, -1), 1), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    st.append(KeepTogether(certs + [t, p(f"<b>Idiomas:</b> {escape(DATA['languages'])}", "body")]))
    return st


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Body", 8.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(MARGIN_X, 0.75 * cm, f"{DATA['name']}  ·  {DATA['contact']['email']}")
    canvas.drawRightString(PAGE_W - MARGIN_X, 0.75 * cm, f"Página {doc.page}")
    canvas.setStrokeColor(NAVY)
    canvas.setLineWidth(3)
    canvas.line(0, PAGE_H - 0.12 * cm, PAGE_W, PAGE_H - 0.12 * cm)
    canvas.restoreState()


class CVDoc(SimpleDocTemplate):
    """Dibuja el pie de página DESPUÉS del contenido, para que el ATS lea primero el nombre y no el pie."""
    def afterPage(self):
        footer(self.canv, self)


def build(filename, with_photo):
    out = OUT_DIR / filename
    doc = CVDoc(str(out), pagesize=letter,
                            leftMargin=MARGIN_X, rightMargin=MARGIN_X,
                            topMargin=1.0 * cm, bottomMargin=1.3 * cm,
                            title=f"{DATA['name']} - Hoja de vida", author=DATA["name"],
                            subject=DATA["headline"],
                            keywords="Ingeniería Multimedia, Desarrollo Web, UX/UI, Python, JavaScript, Figma, Node.js")
    doc.build(story(with_photo))
    print("OK", out.relative_to(ROOT))


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build("Juan_Jose_Osorio_Reyes_CV.pdf", with_photo=False)
    build("Juan_Jose_Osorio_Reyes_CV_foto.pdf", with_photo=True)
