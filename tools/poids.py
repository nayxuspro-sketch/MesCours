#!/usr/bin/env python3
"""poids.py — garde-fou de quota de l'atelier (128 Mo persistés).

Le dépôt ne doit persister que la **source** : Markdown, SVG, scripts, JSON de vérité terrain. Tout le reste est
un artefact régénérable, et un artefact qui dort dans le snapshot finit par faire exploser le quota — c'est arrivé
le 18/09/2026 à 128,9 Mo. Ce contrôle dit trois choses : ce qui est compté, qui le pèse, et comment le rendre.

Usage :
    python3 tools/poids.py            # état + palmarès + remèdes
    python3 tools/poids.py --strict   # code de sortie 1 au-delà du seuil d'alerte
"""
import os
import sys

# noms de dossiers exclus du snapshot par la plateforme : ils ne comptent pas dans le quota
EXCLUS = {'.arena', '.cache', '.local', '.mypy_cache', '.next', '.nox', '.npm', '.nuxt', '.output',
          '.parcel-cache', '.pytest_cache', '.ruff_cache', '.svelte-kit', '.tox', '.turbo', '.venv',
          '.vite', '__pycache__', 'build', 'coverage', 'dist', 'node_modules', 'out', 'target'}
PLAFOND = 128.0 * 2**20
ALERTE = 118.0 * 2**20
RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ce qui est régénérable, et par quoi
REMEDES = [
    ('05_livrables/', '.html', 'sortie intermédiaire de composition → `rm 05_livrables/*.html` (20 s pour la refaire)'),
    ('00_architecture/', '.html', 'sortie de composition → supprimer, `render.py` la rend'),
    ('tools/fonts/', '-400.ttf', 'instance de police → recréée par `render.py` (ensure_static_fonts)'),
    ('tools/fonts/', '-600.ttf', 'instance de police → recréée par `render.py`'),
    ('tools/fonts/', '-700.ttf', 'instance de police → recréée par `render.py`'),
    ('tools/fonts/', '-It-', 'instance de police à casse ancienne → plus personne ne la référence'),
    ('data/', '.duckdb', 'base dérivée → `python3 01_socle_donnees/scripts/generation_socle.py` (graine 20260917)'),
    ('01_socle_donnees/', '.xlsx', 'classeur d’atelier → `python3 tools/classeur_M03.py`'),
    ('05_livrables/', '.pdf', 'PDF composé → `render.py` ; à pousser dans `.cache/livrables/` si le quota serre'),
    ('figures/', '.svg', 'planches → `tools/figures_M0*.py`'),
]


def remede(chemin):
    for base, motif, txt in REMEDES:
        if base in chemin and motif in chemin:
            return txt
    if '01_socle_donnees/data/' in chemin:
        return ('socle de données : cité par son nom dans le manuel (12 fichiers) → à garder ; '
                'se régénère aussi par `generation_socle.py`')
    return 'source éditable — à garder'


def main():
    strict = '--strict' in sys.argv
    total = 0
    fichiers = 0
    palmares = []
    pour_la_source = 0
    for dossier, sous, noms in os.walk(RACINE):
        sous[:] = [d for d in sous if d not in EXCLUS]
        for n in noms:
            p = os.path.join(dossier, n)
            try:
                s = os.path.getsize(p)
            except OSError:
                continue
            rel = os.path.relpath(p, RACINE)
            total += s
            fichiers += 1
            if n.endswith(('.md', '.svg', '.py', '.json', '.txt')):
                pour_la_source += s
            palmares.append((s, rel))
    palmares.sort(reverse=True)

    print(f'atelier : {total / 2**20:.1f} Mo persistés sur {PLAFOND / 2**20:.0f} · {fichiers} fichiers · '
          f'marge {(PLAFOND - total) / 2**20:+.1f} Mo')
    print(f'  dont source éditable (.md .svg .py .json) : {pour_la_source / 2**20:.1f} Mo '
          f'({100 * pour_la_source / total:.0f} %) · artefacts : {(total - pour_la_source) / 2**20:.1f} Mo')
    print('\nles dix plus gros fichiers, et leur remède :')
    for s, rel in palmares[:10]:
        print(f'  {s / 2**20:6.2f} Mo  {rel:<58} {remede(rel)}')
    reg = sum(s for s, rel in palmares if not remede(rel).startswith(('source éditable', 'socle de données')))
    print(f'\nce qui pourrait être rendu sans rien perdre de la source : {reg / 2**20:.1f} Mo')
    if total > ALERTE:
        print(f'⚠ au-delà du seuil d’alerte ({ALERTE / 2**20:.0f} Mo) : supprimer les artefacts listés ci-dessus, '
              'puis re-composer seulement le module en cours.')
        if strict:
            sys.exit(1)
    else:
        print('✔ sous le seuil d’alerte — rien à faire.')


if __name__ == '__main__':
    main()
