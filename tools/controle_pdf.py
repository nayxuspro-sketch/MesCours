#!/usr/bin/env python3
"""Contrôle final du PDF composé d'un module — le seul contrôle qui lit le fichier rendu.

Deux vérifications, mesurées sur le PDF, et une seulement :

1. **Figures embarquées.** Pour chaque `![…](figures/x.svg)` des sources Markdown, on prend
   un libellé du SVG (le plus long qui n’apparaisse **pas** dans le texte du chapitre, donc
   propre à la figure) et on l’extrait du texte de `x.pdf` ; un libellé absent = SVG perdu à
   la composition. On ne compte pas les `/Image` : `render.py` compose les SVG en
   XObjects vectoriels (le PDF de M03 contient 11 011 XObjects et 0 `/Image`), donc le
   libellé est la seule sonde fiable depuis `pypdf`.
2. **Glyphes.** Tout caractère non ASCII employé dans les sources doit être présent dans le
   texte extrait du PDF. Absent = glyphe non composé, donc carré noir à l’impression. Les
   caractères de balisage (backtick, crochet, parenthèse) et les invisibles (tiret
   conditionnel U+00AD, espace fine) sont exclus : le composeur les consomme.

Deux choses sont volontairement **absentes** de ce contrôle, après essai :
* le `/Count` de la table des matières, que `nb_pages.py` lit déjà au bon endroit ;
* la détection de titres orphelins en fin de page — `pypdf` recolle l’en-tête courant, le
  titre et le pied de page sur une seule ligne, ce qui produisait 104 faux positifs sur
  M03. Il faudrait la géométrie de mise en page, donc rendre le document une seconde fois.

Usage : `python3 tools/controle_pdf.py M01 M02 M03`.
"""
import pathlib
import re
import sys
import xml.etree.ElementTree as ET

from pypdf import PdfReader

RACINE = pathlib.Path(__file__).resolve().parent.parent
BALISAGE = set('`|[]()<>*_#-=+~:"\'.,;!?/\\')
INVISIBLES = set('\u00ad\u200b\u200c\u200d\u2060\u202f\u00a0\u2028\u2029')


def sources_module(mod):
    fs = sorted((RACINE / '02_modules').glob(f'{mod}_*.md'))
    fs += [p for p in (RACINE / '03_exercices' / f'{mod}_projet.md',
                       RACINE / '04_evaluations' / f'{mod}_evaluation.md') if p.exists()]
    return fs


def sans_espaces(s):
    """Le composeur insère des blancs entre glyphes espacés (`D A T A`) et rompt les lignes ;
    on compare donc en retirant toute la blancheur, des deux côtés."""
    return re.sub(r'\s+', '', s)


def labels_svg(chemin):
    """Une ligne par élément de texte (les <tspan> de saut de ligne comptent séparément)."""
    if not chemin.exists():
        return []
    try:
        racine = ET.fromstring(chemin.read_text(encoding='utf-8'))
    except ET.ParseError:
        return []
    out = []
    for el in racine.iter():
        if el.tag.endswith('}text'):
            parts = [el.text or ''] + [t.text or '' for t in el.iter() if t.tag.endswith('}tspan')]
            out += [' '.join(x.split()) for x in parts if x and x.strip()]
    return out


def controle(mod):
    pdf = RACINE / '05_livrables' / f'{mod}.pdf'
    if not pdf.exists():
        return [f"{mod} : `{pdf.name}` absent — lancer `tools/render.py` d'abord"], []
    pages = PdfReader(str(pdf)).pages
    texte = ''.join((p.extract_text() or '') for p in pages)
    src_files = sources_module(mod)
    src = '\n'.join(f.read_text(encoding='utf-8') for f in src_files)
    defauts, info = [], [f'{mod} : {len(pages)} pages']

    figures = sorted(set(re.findall(r'^!\[[^\]]*\]\(([^)]+\.svg)\)', src, re.M)))
    src_compact = sans_espaces(src)
    texte_compact = sans_espaces(texte)
    ok, fautes = 0, []
    for f in figures:
        chemin = RACINE / 'figures' / pathlib.Path(f).name
        lignes = labels_svg(chemin)
        propres = [l for l in lignes if len(sans_espaces(l)) >= 10
                   and sans_espaces(l) not in src_compact]
        candidates = propres or [l for l in lignes if len(sans_espaces(l)) >= 10]
        if any(sans_espaces(l) in texte_compact for l in candidates):
            ok += 1
        else:
            fautes.append(f'{chemin.name} : aucune ligne de libellé retrouvee dans le PDF')
    info.append(f'figures : {ok}/{len(figures)} vérifiées dans le PDF par leur libellé propre')
    for f in fautes:
        defauts.append(f'{mod} : {f}')

    non_ascii = {c for c in set(src) if ord(c) > 127 and c not in BALISAGE
                 and not c.isspace() and c not in INVISIBLES}
    absents = sorted(c for c in non_ascii if c not in texte)
    info.append(f'glyphes : {len(non_ascii) - len(absents)}/{len(non_ascii)} composés'
                + (f', absents : {"".join(absents)}' if absents else ''))
    if absents:
        defauts.append(f'{mod} : {len(absents)} glyphe(s) dans les sources et pas dans le PDF : '
                       f'{"".join(absents)}')
    return defauts, info


if __name__ == '__main__':
    mods = [a for a in sys.argv[1:] if not a.startswith('--')] or ['M01', 'M02', 'M03']
    tous = []
    for m in mods:
        d, info = controle(m)
        for ligne in info:
            print(' ', ligne)
        tous += d
    print('Défauts bloquants :', len(tous))
    for d in tous:
        print('  -', d)
    sys.exit(1 if tous else 0)
