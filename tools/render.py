#!/usr/bin/env python3
"""
La Voie des Données — moteur de composition du manuel
Markdown -> HTML stylé (gabarits éditoriaux A4) -> PDF via WeasyPrint.

Usage :
    python3 tools/render.py fichier.md                      # .pdf à côté du .md
    python3 tools/render.py fichier.md --out doc.pdf
    python3 tools/render.py --batch "00_architecture/*.md"  # rend chaque fichier
    python3 tools/render.py fichier.md --html-only          # ne produit que le HTML

Conventions de rendu (à utiliser dans tous les fichiers .md du manuel) :
    > **Définition.** texte…          -> encadré bleu « Définition »
    > **À retenir.** texte…           -> encadré vert
    > **Attention.** texte…           -> encadré ambre
    > **Conseil professionnel.** …    -> encadré gris
    > **Dans les faits.** …           -> encadré fin
    > **Boîte à outils.** …           -> encadré pointillé, police mono
    Les titres h2/h3 alimentent la table des matières automatique.
"""
from __future__ import annotations
import argparse, base64, glob, os, re, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")

# (fichier source variable, [(poids), ...]) -> instances statiques fabriquées à la demande.
VARIABLE_SOURCES = {
    "serif.ttf": [400, 600, 700],
    "serif-it.ttf": [400, 600],
    "sans.ttf": [400, 600, 700],
    "mono.ttf": [400, 700],
}
FALLBACKS = {
    "serif": "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "serif-it": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf",
    "sans": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "mono": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
}
FALLBACKS_BOLD = {k: v.replace(".ttf", "-Bold.ttf") for k, v in FALLBACKS.items()}


def ensure_static_fonts():
    """Materialise des TTF à poids fixe (les polices variables cassent la table
    ToUnicode du PDF : le texte en gras ne serait plus sélectionnable ni cherchable)."""
    made = []
    try:
        from fontTools.ttLib import TTFont
        from fontTools.varLib import instancer
    except Exception as e:
        print("  (fontTools indisponible, polices de repli DejaVu : %s)" % e)
        return False
    for src, weights in VARIABLE_SOURCES.items():
        path = os.path.join(FONT_DIR, src)
        if not os.path.exists(path):
            continue
        for w in weights:
            out = os.path.join(FONT_DIR, "%s-%d.ttf" % (os.path.splitext(src)[0], w))
            if os.path.exists(out):
                continue
            f = TTFont(path)
            instancer.instantiateVariableFont(f, {"wght": w}, inplace=True, updateFontNames=True)
            f.save(out)
            made.append(os.path.basename(out))
    if made:
        print("  instances statiques créées :", ", ".join(made))
    return True


def font_faces():
    """CSS @font-face pour les 4 familles, en poids statiques."""
    css, have = "", {}
    ok = ensure_static_fonts()
    fams = {"serif-embed": "serif", "sans-embed": "sans", "mono-embed": "mono", "serif-it-embed": "serif-it"}
    for fam, key in fams.items():
        for w in (VARIABLE_SOURCES.get(key + ".ttf", None) or [400]):
            fn = os.path.join(FONT_DIR, "%s-%d.ttf" % (key, w))
            style = " normal" if not key.endswith("-it") else " italic"
            if ok and os.path.exists(fn):
                pass
            else:
                fn = FALLBACKS_BOLD.get(key, "") if w >= 600 else FALLBACKS.get(key, "")
                if not os.path.exists(fn):
                    continue
                style = " normal"
            b64 = base64.b64encode(open(fn, "rb").read()).decode()
            fmt = "truetype"
            css += (f"@font-face {{ font-family:'{fam}'; font-weight:{w}; font-style:{style};"
                    f" src:url(data:font/ttf;base64,{b64}) format('{fmt}'); }} ")
            have[(fam, w)] = fn
    for (fam, w), fn in have.items():
        print(f"  police {fam:14s} {w:>3}  {os.path.basename(fn)}")
    return css


CSS_BASE = """
@page {
  size: A4; margin: 21mm 19mm 20mm 21mm;
  @top-left { content: "L A   V O I E   D E S   D O N N É E S"; font-family: sans-embed;
              font-size: 6.6pt; letter-spacing: .1em; color: #8d96a4; margin-bottom: 5mm; }
  @top-right { content: string(chaptitle); font-family: sans-embed; font-size: 6.6pt;
              color: #6d7686; margin-bottom: 5mm; }
  @bottom-left { content: string(modulename); font-family: sans-embed; font-size: 6.6pt; color: #8d96a4; }
  @bottom-center { content: counter(page); font-family: serif-embed; font-size: 8.4pt; color: #33415c; }
  @bottom-right { content: "%(footer)s"; font-family: sans-embed; font-size: 6.6pt; color: #8d96a4; }
}
@page :first { margin: 0; @top-left { content: none } @top-right { content: none }
              @bottom-left { content: none } @bottom-center { content: none } @bottom-right { content: none } }
:root {
  --ink:#16202e; --muted:#4a5568; --rule:#d5dbe6; --accent:#0f2a43; --accent2:#1d6fa5;
  --bg-def:#eef4fb; --bd-def:#8fb4d8;
  --bg-note:#eef7f0; --bd-note:#7cb08a;
  --bg-warn:#fdf3e2; --bd-warn:#dda martin;
  --code:#f6f7f9;
}
html { -weasy-hyphens: auto; }
body { font-family: serif-embed; font-size: 9.5pt; line-height: 1.42; color: var(--ink);
       text-align: justify; hyphens: auto; }
h1, h2, h3, h4, h5 { font-family: sans-embed; color: var(--accent); text-align: left; hyphens: none; }
h1 { font-size: 21pt; line-height: 1.15; margin: 0 0 10pt; font-weight: 700;
     border-bottom: 2.2pt solid var(--accent); padding-bottom: 6pt; }
h2 { font-size: 14.5pt; margin: 20pt 0 7pt; font-weight: 700;
     string-set: chaptitle content(); page-break-after: avoid; }
h3 { font-size: 11.4pt; margin: 14pt 0 5pt; font-weight: 650; string-set: modulename content();
     page-break-after: avoid; }
h4 { font-size: 10.1pt; margin: 11pt 0 4pt; font-weight: 650; color: var(--accent2); page-break-after: avoid; }
p { margin: 0 0 5.5pt; orphans: 2; widows: 2; }
strong { font-weight: 700; }
em, i { font-family: serif-it-embed, serif-embed; font-style: italic; }
ul, ol { margin: 0 0 6pt 0; padding-left: 15pt; }
li { margin-bottom: 2.2pt; }
hr { border: 0; border-top: .6pt solid var(--rule); margin: 12pt 0; }
code { font-family: mono-embed; font-size: 8.2pt; background: #eff1f5; padding: 0 1.6pt; border-radius: 1.5pt; }
pre { font-family: mono-embed; font-size: 7.6pt; line-height: 1.33; background: var(--code);
      border-left: 2.4pt solid var(--accent2); padding: 6pt 8pt; margin: 7pt 0 9pt;
      white-space: pre-wrap; word-break: break-word; page-break-inside: avoid; hyphens: none; }
pre code { background: none; font-size: inherit; padding: 0; }
table { border-collapse: collapse; width: 100%%; font-family: sans-embed; font-size: 7.7pt;
        line-height: 1.3; margin: 7pt 0 10pt; page-break-inside: auto; hyphens: none; }
thead { display: table-header-group; }
tr { page-break-inside: avoid; }
th { background: var(--accent); color: #fff; text-align: left; font-weight: 600; padding: 3.6pt 4.6pt;
     vertical-align: bottom; }
td { padding: 3.4pt 4.6pt; border-bottom: .5pt solid var(--rule); vertical-align: top; }
tbody tr:nth-child(even) td { background: #f7f9fc; }
td code { font-size: 7.3pt; }
blockquote { margin: 8pt 0; padding: 7pt 9pt 7pt 10pt; background: #f7f9fc;
             border-left: 2.6pt solid var(--accent2); page-break-inside: avoid; font-size: 9.2pt; }
blockquote p { margin-bottom: 4pt; }
blockquote p:last-child { margin-bottom: 0; }
figure { margin: 9pt 0; page-break-inside: avoid; text-align: center; }
img { max-width: 100%%; height: auto; }   /* les planches SVG (780 px = 585 pt) sont ramenées à la largeur utile */
figcaption { font-family: sans-embed; font-size: 7.6pt; color: var(--muted); text-align: left; margin-top: 3pt; }
a { color: var(--accent2); text-decoration: none; }
/* ---------- encadrés éditoriaux ---------- */
.callout { margin: 9pt 0; padding: 7.5pt 9pt; page-break-inside: avoid; font-size: 9.1pt;
           border: .5pt solid transparent; }
.callout .lbl { display: block; font-family: sans-embed; font-size: 7.2pt; letter-spacing: .12em;
           text-transform: uppercase; font-weight: 700; margin-bottom: 3.4pt; }
.c-def  { background: #eef4fb; border-color: #cfe0f1; } .c-def .lbl  { color:#1d6fa5; }
.c-note { background: #eef7f0; border-color: #cfe6d6; } .c-note .lbl { color:#2f7a4a; }
.c-warn { background: #fdf3e2; border-color: #efd9ab; } .c-warn .lbl { color:#9a6408; }
.c-pro  { background: #f2f3f6; border-color: #dcdfe6; } .c-pro .lbl  { color:#3c4757; }
.c-fact { background: #fff; border: 0; border-left: 1.6pt solid #b9c2d0; padding-left: 8pt; }
.c-fact .lbl { color:#6d7686; }
.c-tool { background: #fbfbfc; border: .6pt dashed #9aa5b5; } .c-tool .lbl { color:#4a5568; }
.c-tool, .c-tool code { font-family: mono-embed; font-size: 8pt; }
/* ---------- table des matières ---------- */
.toc { font-family: sans-embed; font-size: 8.4pt; }
.toc ul { list-style: none; padding-left: 0; margin: 0; }
.toc li { margin: 0 0 2.2pt; }
.toc a { color: var(--ink); text-decoration: none; }
.toc a::after { content: " " leader(dotted) " " target-counter(attr(href), page);
                color: var(--muted); font-weight: 400; }
.toc .l1 { font-weight: 700; color: var(--accent); font-size: 9.6pt; margin: 9pt 0 2.5pt;
           text-transform: uppercase; letter-spacing: .04em; }
.toc .l1 a::after { color: var(--accent); }
.toc .l2 { font-weight: 600; color: var(--accent); margin: 6pt 0 1.6pt; }
.toc .l3 { padding-left: 10pt; color: var(--muted); }
/* ---------- page de couverture ---------- */
.cover { page: cover; height: 297mm; box-sizing: border-box; padding: 30mm 24mm 22mm;
         background: linear-gradient(160deg, #0b1f33 0%%, #0f2a43 55%%, #17456b 100%%);
         color: #f2f6fb; }
@page cover { margin: 0; }
.cover h1 { color:#fff; border: 0; font-size: 40pt; line-height: 1.05; margin: 0 0 6mm; }
.cover .kicker { font-family: sans-embed; font-size: 9pt; letter-spacing: .3em; color:#8fc3ea;
         text-transform: uppercase; margin-bottom: 12mm; }
.cover .sub { font-family: serif-embed; font-size: 14.5pt; line-height:1.4; color:#dce8f5; margin-bottom: 10mm; }
.cover .meta { font-family: sans-embed; font-size: 8.6pt; line-height: 1.6; color:#a9c4de;
         border-top: .6pt solid #35597c; padding-top: 6mm; }
.cover .rule { height: 2.4mm; width: 46mm; background:#4aa3e0; margin: 8mm 0; }
.section-start { page-break-before: always; }
"""
CSS_BASE = CSS_BASE.replace("#dda martin", "#e6c98f")

CALLOUT_MAP = {
    "définition": ("c-def", "Définition"), "definition": ("c-def", "Définition"),
    "à retenir": ("c-note", "À retenir"), "a retenir": ("c-note", "À retenir"),
    "attention": ("c-warn", "Attention"), "erreur fréquente": ("c-warn", "Erreur fréquente"),
    "conseil professionnel": ("c-pro", "Conseil professionnel"), "conseil": ("c-pro", "Conseil professionnel"),
    "dans les faits": ("c-fact", "Dans les faits"), "boîte à outils": ("c-tool", "Boîte à outils"),
    "boite à outils": ("c-tool", "Boîte à outils"),
}


def slug(s: str) -> str:
    s = re.sub(r"<[^>]+>", "", s)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^\w\s-]", "", s).strip().lower()
    return re.sub(r"[\s-]+", "-", s)[:70] or "section"


def to_html(md_text: str) -> str:
    import markdown as md
    body = md.markdown(
        md_text,
        extensions=["extra", "sane_lists", "smarty", "attr_list", "md_in_html"],
        output_format="html5",
    )
    # encadrés éditoriaux : > **Définition.** …
    def callout(m):
        inner = m.group(1)
        lab = re.match(r"\s*<strong>\s*([^<.]{2,60}?)\.?\s*</strong>", inner)
        if lab:
            key = re.sub(r"[^a-zà-ÿ ]", "", lab.group(1).lower().strip())
            for k, (cls, txt) in CALLOUT_MAP.items():
                if key.startswith(k):
                    rest = inner[lab.end():].lstrip()
                    if rest.lower().lstrip().startswith((".</p>", "</p>")):
                        rest = rest[4:] if rest.startswith(".") else rest
                    rest = re.sub(r"^\s*\.\s*", "", rest)
                    return f'<div class="callout {cls}"><span class="lbl">{txt}</span>{rest}</div>'
        return f'<div class="callout c-fact">{inner}</div>'
    body = re.sub(r"<blockquote>(.*?)</blockquote>", callout, body, flags=re.S)
    # ancres : la source de vérité des ids, ce qui garantit que la table des
    # matières (construite à partir du HTML final) ne casse jamais
    seen = set()
    def anchor(m):
        lvl, attrs, txt = m.group(1), m.group(2) or "", m.group(3)
        if 'id=' in attrs:
            return m.group(0)
        base = s = slug(txt); i = 2
        while s in seen:
            s = f"{base}-{i}"; i += 1
        seen.add(s)
        return f'<h{lvl} id="{s}"{attrs}>{txt}</h{lvl}>'
    body = re.sub(r"<h([1-4])((?: [^>]*)?)>(.*?)</h\1>", anchor, body, flags=re.S)
    return body, seen


def build_toc(html_body: str, levels=(1, 2, 3)) -> str:
    """Table des matières déduite du HTML rendu : ids et libellés garantis cohérents."""
    items = []
    for m in re.finditer(r'<h([1-4]) id="([^"]+)"[^>]*>(.*?)</h\1>', html_body, flags=re.S):
        lvl, hid, txt = int(m.group(1)), m.group(2), m.group(3)
        if lvl not in levels:
            continue
        txt = re.sub(r"<[^>]+>", "", txt).strip()
        txt = (txt.replace("&amp;", "&").replace("&quot;", '"').replace("&#39;", "'"))
        if re.match(r"^(Table des|Fin de)", txt, re.I) or re.match(r"^\s*(PARTIE|ANNEXE)", txt, re.I) and lvl == 2:
            continue
        items.append((lvl, hid, txt))
    if not items:
        return ""
    out = ['<h2 id="table-des-matieres">Table des matières</h2>', '<div class="toc"><ul>']
    for lvl, hid, txt in items:
        out.append(f'<li class="l{lvl}"><a href="#{hid}">{txt}</a></li>')
    out.append("</ul></div>")
    return "\n".join(out)


def split_front(md_text: str):
    """Sépare le bloc H1 (titre) du corps, pour construire la couverture."""
    lines = md_text.splitlines()
    title, sub = "", ""
    i = 0
    while i < len(lines) and not lines[i].startswith("# "):
        i += 1
    if i < len(lines):
        title = lines[i][2:].strip()
        for j in range(i + 1, min(i + 5, len(lines))):
            if lines[j].startswith("## "):
                sub = lines[j][3:].strip()
                break
    return title, sub


def render(md_path: str, out_pdf: str | None = None, html_only=False, toc=True, cover=True,
           footer="Édition 2026"):
    src = open(md_path, encoding="utf-8").read()
    html_body, _ = to_html(src)
    css = CSS_BASE % {"footer": footer}
    css = font_faces() + css
    pieces = []
    if cover:
        t, s = split_front(src)
        pieces.append(f'''<div class="cover">
        <div class="kicker">Manuel professionnel · Édition 2026</div>
        <h1>{t or "La Voie des Données"}</h1><div class="rule"></div>
        <div class="sub">{s or ""}</div>
        <div class="meta">Analyse de données appliquée &amp; Business Intelligence<br>
        {os.path.basename(md_path)} · document de production</div></div>''')
        pieces.append('<div class="section-start"></div>')
    if toc:
        pieces.append(build_toc(html_body))
        pieces.append('<div class="section-start"></div>')
    doc = f"<!DOCTYPE html><html lang='fr'><head><meta charset='utf-8'><style>{css}</style></head><body>{''.join(pieces)}{html_body}</body></html>"
    html_out = (out_pdf[:-4] + ".html") if (out_pdf and out_pdf.endswith(".pdf")) else os.path.splitext(md_path)[0] + ".html"
    open(html_out, "w", encoding="utf-8").write(doc)
    print("HTML   →", html_out)
    if html_only:
        return html_out
    from weasyprint import HTML
    out = out_pdf or os.path.splitext(md_path)[0] + ".pdf"
    HTML(string=doc, base_url=os.path.dirname(os.path.abspath(md_path))).write_pdf(out)
    n = os.path.getsize(out) // 1024
    print("PDF    →", out, f"({n} Ko)")
    return out



def render_joined(fichiers, out_pdf, titre=None, sous_titre=None, html_only=False, toc=True,
                  cover=True, footer="Édition 2026"):
    """Assemble plusieurs fichiers Markdown en un seul document paginé (couverture et TOC communes).

    Les images relatives sont réécrites en chemins absolus : chaque fichier garde ses
    `../figures/…` dans le dépôt, mais l'assemblage, lui, doit les trouver.
    """
    corps, titres = [], []
    bases = set()
    for k, f in enumerate(fichiers):
        src = open(f, encoding="utf-8").read()
        base = os.path.dirname(os.path.abspath(f))
        bases.add(base)
        src = re.sub(r"!\[([^\]]*)\]\((?!https?:)([^)]+)\)",
                     lambda m: "![" + m.group(1) + "](" + os.path.normpath(os.path.join(base, m.group(2))) + ")",
                     src)
        html, _ = to_html(src)
        t_, s_ = split_front(src)
        titres.append(t_ or os.path.basename(f))
        if k:
            corps.append('<div class="section-start"></div>')
        corps.append(html)
    css = font_faces() + (CSS_BASE % {"footer": footer})
    pieces = []
    if cover:
        pieces.append(
            '<div class="cover">'
            '<div class="kicker">Manuel professionnel · Édition 2026</div>'
            "<h1>" + (titre or titres[0]) + "</h1><div class=\"rule\"></div>"
            '<div class="sub">' + (sous_titre or "") + "</div>"
            '<div class="meta">Analyse de données appliquée &amp; Business Intelligence<br>'
            + str(len(fichiers)) + " partie(s) assemblée(s) · document de production</div></div>")
        pieces.append('<div class="section-start"></div>')
    if toc:
        pieces.append(build_toc("".join(corps)))
        pieces.append('<div class="section-start"></div>')
    doc = ("<!DOCTYPE html><html lang='fr'><head><meta charset='utf-8'><style>" + css
           + "</style></head><body>" + "".join(pieces) + "".join(corps) + "</body></html>")
    if not out_pdf.endswith(".pdf"):
        out_pdf += ".pdf"
    os.makedirs(os.path.dirname(os.path.abspath(out_pdf)), exist_ok=True)
    html_out = out_pdf[:-4] + ".html"
    open(html_out, "w", encoding="utf-8").write(doc)
    print("HTML   →", html_out, "(" + str(len(fichiers)) + " fichier(s) joints)")
    if html_only:
        return html_out
    from weasyprint import HTML
    base_url = bases.pop() if len(bases) == 1 else os.path.dirname(HERE)
    HTML(string=doc, base_url=base_url).write_pdf(out_pdf)
    print("PDF    →", out_pdf, "(" + str(os.path.getsize(out_pdf) // 1024) + " Ko)")
    return out_pdf

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--out")
    ap.add_argument("--batch", action="store_true")
    ap.add_argument("--html-only", action="store_true")
    ap.add_argument("--no-toc", action="store_true")
    ap.add_argument("--no-cover", action="store_true")
    ap.add_argument("--footer", default="Édition 2026")
    ap.add_argument("--join", action="store_true", help="assemble tous les fichiers vises en un seul document")
    ap.add_argument("--titre", default=None)
    ap.add_argument("--sous-titre", default=None)
    a = ap.parse_args()
    if a.batch:
        for f in sorted(glob.glob(a.target)):
            render(f, html_only=a.html_only, toc=not a.no_toc, cover=not a.no_cover, footer=a.footer)
    elif a.join:
        fs = sorted(glob.glob(a.target))
        if not fs:
            raise SystemExit("aucun fichier pour " + a.target)
        racine = os.path.dirname(HERE)
        out = a.out or os.path.join(racine, "05_livrables", os.path.basename(os.path.dirname(fs[0])) + "-assemble.pdf")
        render_joined(fs, out, titre=a.titre, sous_titre=a.sous_titre, html_only=a.html_only,
                      toc=not a.no_toc, cover=not a.no_cover, footer=a.footer)
    else:
        render(a.target, a.out, html_only=a.html_only, toc=not a.no_toc, cover=not a.no_cover, footer=a.footer)
