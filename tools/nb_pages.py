#!/usr/bin/env python3
"""Compte les pages d'un PDF produit par WeasyPrint.

Les objets de page sont écrits dans des flux compressés (objstml) : on décompresse
tout et on compte les occurrences de `/Type /Page` en excluant `/Type /Pages`.
Un `/Count` présent dans le fichier sert de contrôle croisé.

Usage : python3 tools/nb_pages.py 05_livrables/M01.pdf [...]
"""
import re, sys, zlib

def analyse(chemin):
    brut = open(chemin, "rb").read()
    pages = 0
    counts = set()
    for m in re.finditer(rb"stream\r?\n(.*?)endstream", brut, re.S):
        try:
            txt = zlib.decompress(m.group(1))
        except Exception:
            txt = m.group(1)
        pages += len(re.findall(rb"/Type\s*/Page(?![s])", txt))
        counts.update(int(c) for c in re.findall(rb"/Count\s+(\d+)", txt))
    return pages, max([c for c in counts if c >= pages] or [0])

if __name__ == "__main__":
    for p in sys.argv[1:]:
        n, c = analyse(p)
        ecart = "" if n == c else f"  (contrôle /Count = {c} → à vérifier)"
        print(f"{p} → {n} pages{ecart}")
