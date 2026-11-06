#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convertisseur Markdown -> DOCX (OOXML moderne, python-docx)
Rapport : Analyse de la qualité technique et pédagogique — Thème 7 SDSR (sdsr.ticanalyse.org)

Conventions du Markdown source :
  [[COVER]] ... [[COVER_END]]  -> encadré de métadonnées rendu en page de couverture
  [[PAGEBREAK]]                -> saut de page
  ## Titre / ### Sous-titre     -> titres hiérarchisés
  | a | b |                    -> tableau (ligne de séparation détectée)
  - puce                       -> puce
  1. numéroté                   -> liste numérotée (numéros littéraux)
  **gras**  `code`             -> mise en forme en ligne
  > encadré                    -> encadré italique
"""
import re
import sys

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

SRC = "Theme7_analyse_technique_et_pedagogique.md"
OUT = "Theme7_Analyse_technique_et_pedagogique_SDSR.docx"

NAVY = RGBColor(0x1F, 0x38, 0x64)
BLUE = RGBColor(0x2E, 0x74, 0xB5)
GREY = RGBColor(0x59, 0x59, 0x59)
DARK = RGBColor(0x21, 0x21, 0x21)
HDR_BG = "1F3864"
SUB_BG = "2E74B5"
BAND_BG = "EEF3F9"
BOX_BG = "F4F6FA"

BODY_FONT = "Calibri"
MONO_FONT = "Consolas"
BODY_SIZE = Pt(10.5)


# --------------------------------------------------------------------------- utils
def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hexcolor)
    tcPr.append(shd)


def cell_margins(table, top=60, bottom=60, left=100, right=100):
    tblPr = table._tbl.tblPr
    mar = OxmlElement("w:tblCellMar")
    for tag, val in (("top", top), ("left", left), ("bottom", bottom), ("right", right)):
        el = OxmlElement("w:" + tag)
        el.set(qn("w:w"), str(val))
        el.set(qn("w:type"), "dxa")
        mar.append(el)
    tblPr.append(mar)


def repeat_header(row):
    trPr = row._tr.get_or_add_trPr()
    el = OxmlElement("w:tblHeader")
    el.set(qn("w:val"), "true")
    trPr.append(el)


def add_page_field(paragraph):
    run = paragraph.add_run()
    f1 = OxmlElement("w:fldChar")
    f1.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE "
    f2 = OxmlElement("w:fldChar")
    f2.set(qn("w:fldCharType"), "end")
    run._r.append(f1)
    run._r.append(instr)
    run._r.append(f2)
    run.font.size = Pt(8.5)
    run.font.color.rgb = GREY


def hr(paragraph, color="BFCBDD", size=6):
    pPr = paragraph._p.get_or_add_pPr()
    borders = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), str(size))
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), color)
    borders.append(bottom)
    pPr.append(borders)


# ------------------------------------------------------------------- inline rich text
TOKEN = re.compile(r"(\*\*.+?\*\*|`[^`]+`)")


def add_rich(paragraph, text, size=BODY_SIZE, color=DARK, italic=False, bold=False):
    for part in TOKEN.split(text):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**") and len(part) > 4:
            r = paragraph.add_run(part[2:-2])
            r.bold = True
        elif part.startswith("`") and part.endswith("`") and len(part) > 2:
            r = paragraph.add_run(part[1:-1])
            r.font.name = MONO_FONT
            r.font.size = Pt(size.pt - 0.5)
            r.font.color.rgb = NAVY
        else:
            r = paragraph.add_run(part)
        r.font.size = size
        r.font.name = BODY_FONT
        if bold:
            r.bold = True
        if italic:
            r.italic = True
        if color is not None and r.font.color.rgb is None:
            r.font.color.rgb = color
    return paragraph


# ---------------------------------------------------------------------------- document
doc = Document()

sec = doc.sections[0]
sec.page_width = Cm(21.0)
sec.page_height = Cm(29.7)
sec.top_margin = Cm(2.0)
sec.bottom_margin = Cm(1.8)
sec.left_margin = Cm(2.0)
sec.right_margin = Cm(2.0)

st = doc.styles["Normal"]
st.font.name = BODY_FONT
st.font.size = BODY_SIZE
st.font.color.rgb = DARK
st.element.rPr.rFonts.set(qn("w:eastAsia"), BODY_FONT)
st.paragraph_format.space_after = Pt(5)
st.paragraph_format.space_before = Pt(0)
st.paragraph_format.line_spacing = 1.08

for name, size, color, before, after in (
    ("Heading 1", 17, NAVY, 16, 8),
    ("Heading 2", 13.5, BLUE, 12, 5),
    ("Heading 3", 11.5, NAVY, 9, 4),
):
    s = doc.styles[name]
    s.font.name = BODY_FONT
    s.font.size = Pt(size)
    s.font.bold = True
    s.font.color.rgb = color
    s.paragraph_format.space_before = Pt(before)
    s.paragraph_format.space_after = Pt(after)
    s.paragraph_format.keep_with_next = True

# pied de page
footer_p = sec.footer.paragraphs[0]
footer_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
fr = footer_p.add_run("Analyse de la qualité technique et pédagogique — Thème 7 « Violence et addiction » (SDSR)   ·   page ")
fr.font.size = Pt(8.5)
fr.font.color.rgb = GREY
fr.font.name = BODY_FONT
add_page_field(footer_p)


# ----------------------------------------------------------------------- parsing helpers
def is_sep(line):
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    return bool(cells) and all(re.fullmatch(r":?-{2,}:?", c or "-") for c in cells)


def split_row(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def is_bold_cell(cell):
    return cell.startswith("**") and cell.endswith("**") and len(cell) > 4


def add_table(rows, header=True):
    ncols = max(len(r) for r in rows)
    table = doc.add_table(rows=0, cols=ncols)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = True
    cell_margins(table)
    # largeurs proportionnelles au contenu
    weights = []
    for i in range(ncols):
        longest = max((len(r[i]) if i < len(r) else 0) for r in rows)
        weights.append(max(6, min(60, longest)))
    total = sum(weights)
    usable = Cm(17.0)
    for r_i, row in enumerate(rows):
        cells = table.add_row().cells
        for c_i in range(ncols):
            cell = cells[c_i]
            cell.width = int(usable * (weights[c_i] / total))
            txt = row[c_i] if c_i < len(row) else ""
            para = cell.paragraphs[0]
            para.paragraph_format.space_after = Pt(1)
            para.paragraph_format.space_before = Pt(1)
            para.paragraph_format.line_spacing = 1.0
            if header and r_i == 0:
                shade(cell, HDR_BG)
                add_rich(para, txt, size=Pt(9.5), color=RGBColor(0xFF, 0xFF, 0xFF), bold=True)
                for r in para.runs:
                    r.bold = True
            else:
                if header and r_i % 2 == 0:
                    shade(cell, BAND_BG)
                add_rich(para, txt, size=Pt(9.5), color=DARK, bold=is_bold_cell(txt))
                if is_bold_cell(txt):
                    for r in para.runs:
                        r.bold = True
    if header:
        repeat_header(table.rows[0])
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return table


def add_box(lines):
    table = doc.add_table(rows=1, cols=1)
    table.style = "Table Grid"
    cell_margins(table, top=110, bottom=110, left=160, right=160)
    cell = table.rows[0].cells[0]
    shade(cell, BOX_BG)
    first = True
    for line in lines:
        para = cell.paragraphs[0] if first else cell.add_paragraph()
        first = False
        para.paragraph_format.space_after = Pt(2)
        add_rich(para, line, size=Pt(10), color=NAVY)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


# ------------------------------------------------------------------------ read source
with open(SRC, encoding="utf-8") as fh:
    md = fh.read()

lines = md.splitlines()

cover_lines = []
body_lines = []
mode = "cover"
for line in lines:
    if line.strip() == "[[COVER]]":
        continue
    if line.strip() == "[[COVER_END]]":
        mode = "body"
        continue
    (cover_lines if mode == "cover" else body_lines).append(line)

# =============================================================== PAGE DE COUVERTURE
title = None
subtitle = None
meta_rows = []
for line in cover_lines:
    s = line.strip()
    if not s:
        continue
    if s.startswith("# "):
        title = s[2:].strip()
    elif s.startswith("## ") and title and subtitle is None and not meta_rows:
        subtitle = s[3:].strip()
    elif s.startswith("|"):
        cells = split_row(s)
        if not is_sep(s):
            meta_rows.append(cells)
    elif title is None:
        title = s
    elif subtitle is None and not meta_rows:
        subtitle = s

for _ in range(2):
    doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run(title or "Analyse")
r.font.size = Pt(26)
r.font.bold = True
r.font.color.rgb = NAVY
r.font.name = BODY_FONT

if subtitle:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(subtitle)
    r.font.size = Pt(13)
    r.font.color.rgb = BLUE
    r.font.name = BODY_FONT

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
hr(p)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Document d’analyse — ressources sélectionnées, contrôles techniques et évaluation pédagogique")
r.font.size = Pt(10)
r.font.color.rgb = GREY
r.font.name = BODY_FONT
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Ressource analysée : sdsr.ticanalyse.org/theme-7/ — Serious Game SDSR, Thème 7 « Violence et addiction »")
r.font.size = Pt(10)
r.font.color.rgb = GREY
r.font.name = BODY_FONT

doc.add_paragraph()
if meta_rows:
    ncols = max(len(r_) for r_ in meta_rows)
    table = doc.add_table(rows=0, cols=ncols)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_margins(table, top=70, bottom=70, left=130, right=130)
    for row in meta_rows:
        cells = table.add_row().cells
        for c_i in range(ncols):
            cell = cells[c_i]
            txt = row[c_i] if c_i < len(row) else ""
            para = cell.paragraphs[0]
            para.paragraph_format.space_after = Pt(1)
            para.paragraph_format.space_before = Pt(1)
            para.paragraph_format.line_spacing = 1.0
            if c_i == 0 and ncols >= 2:
                shade(cell, "E7EDF6")
                add_rich(para, txt, size=Pt(9.5), color=NAVY, bold=True)
                for run in para.runs:
                    run.bold = True
            else:
                add_rich(para, txt, size=Pt(9.5), color=DARK)

doc.add_page_break()

# ====================================================================== CORPS DU DOC
i = 0
n = len(body_lines)
while i < n:
    raw = body_lines[i]
    line = raw.rstrip()
    s = line.strip()

    if not s:
        i += 1
        continue

    if s == "[[PAGEBREAK]]":
        doc.add_page_break()
        i += 1
        continue

    if s.startswith("|"):
        block = []
        while i < n and body_lines[i].strip().startswith("|"):
            block.append(body_lines[i].strip())
            i += 1
        rows = []
        for b in block:
            if is_sep(b):
                continue
            rows.append(split_row(b))
        if rows:
            add_table(rows, header=True)
        continue

    if s.startswith("### "):
        h = doc.add_heading(s[4:].strip(), level=3)
        hr(h, color="D6E0EE", size=4)
        i += 1
        continue

    if s.startswith("## "):
        h = doc.add_heading(s[3:].strip(), level=2)
        hr(h, color="BFCBDD", size=6)
        i += 1
        continue

    if s.startswith("# "):
        doc.add_heading(s[2:].strip(), level=1)
        i += 1
        continue

    if s.startswith("> "):
        block = []
        while i < n and body_lines[i].strip().startswith(">"):
            block.append(body_lines[i].strip().lstrip(">").strip())
            i += 1
        add_box(block)
        continue

    m_num = re.match(r"^(\d+)[.)]\s+(.*)$", s)
    if m_num:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.7)
        p.paragraph_format.first_line_indent = Cm(-0.7)
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(m_num.group(1) + ".  ")
        r.bold = True
        r.font.color.rgb = BLUE
        r.font.size = BODY_SIZE
        r.font.name = BODY_FONT
        add_rich(p, m_num.group(2))
        i += 1
        continue

    if s.startswith("- ") or s.startswith("* "):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.7)
        p.paragraph_format.first_line_indent = Cm(-0.45)
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run("•   ")
        r.font.color.rgb = BLUE
        r.font.bold = True
        r.font.size = BODY_SIZE
        r.font.name = BODY_FONT
        add_rich(p, s[2:].strip())
        i += 1
        continue

    # paragraphe ordinaire (regroupe les lignes consécutives)
    block = [s]
    i += 1
    while i < n:
        nxt = body_lines[i].strip()
        if not nxt:
            break
        if nxt.startswith(("|", "#", ">", "- ", "* ", "[[")):
            break
        if re.match(r"^\d+[.)]\s", nxt):
            break
        block.append(nxt)
        i += 1
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    add_rich(para, " ".join(block))

doc.save(OUT)

# -------------------------------------------------------------------------- contrôles
from docx import Document as _D

chk = _D(OUT)
paras = chk.paragraphs
tables = chk.tables
words = sum(len(p.text.split()) for p in paras)
for t in tables:
    for row in t.rows:
        for c in row.cells:
            words += len(c.text.split())
print("Fichier   :", OUT)
print("Paragraphes:", len(paras))
print("Tableaux  :", len(tables))
print("Mots      :", words)
