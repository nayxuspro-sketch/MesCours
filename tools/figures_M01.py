#!/usr/bin/env python3
"""Figures SVG du module M01. Style unique, texte en DejaVu Sans (police système du PDF).

Usage : python3 tools/figures_M01.py  →  figures/M01_C0*.svg
Les chiffres affichés viennent de data/reference/chiffres_cites.json (règle de production n° 3).
"""
import os

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(RACINE, "figures")
L = 760
BLEU, VERT, AMBRE, GRIS, ROUGE = "#e8f0fb", "#e8f5ec", "#fdf3dd", "#f0f0ee", "#fbe9e7"
TRAIT, FOND, GRIS_T = "#3c4653", "#ffffff", "#c3ccd8"


def svg(hauteur, corps, legende=""):
    h = hauteur + (26 if legende else 0)
    entete = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{L}" height="{h}" viewBox="0 0 {L} {h}" '
              f'font-family="DejaVu Sans"><rect width="{L}" height="{h}" fill="{FOND}"/>')
    bas = (f'<text x="8" y="{hauteur + 17}" font-size="11" fill="#6a7382">{legende}</text>' if legende else '') + '</svg>'
    return entete + DEF + corps + bas


def boite(x, y, w, h, titre, couleur=BLEU, taille=13, gras=True):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{couleur}" stroke="{TRAIT}" stroke-width="0.9"/>'
            f'<text x="{x + w / 2}" y="{y + h / 2 + 4.5}" font-size="{taille}" font-weight="{"bold" if gras else "normal"}" '
            f'fill="#1c2430" text-anchor="middle">{titre}</text>')


def fleche(x1, y1, x2, y2):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{TRAIT}" stroke-width="1.1" marker-end="url(#f)"/>'


ALERTES = []


def _largeur(s, taille):
    return 0.605 * taille * len(s)


def txt(x, y, s, taille=11.5, gras=False, couleur="#1c2430", ancre="start"):
    l = _largeur(s, taille)
    gauche = x - l / 2 if ancre == "middle" else x
    if gauche + l > L - 8 or gauche < 4:
        ALERTES.append(f"débord : « {s[:58]}… » y={y}")
    return (f'<text x="{x}" y="{y}" font-size="{taille}" font-weight="{"bold" if gras else "normal"}" '
            f'fill="{couleur}" text-anchor="{ancre}">{s}</text>')


DEF = ('<defs><marker id="f" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" '
       'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#3c4653"/></marker></defs>')
TITRE, NOTE, ERREUR = 13.5, 11, "#8a5b06"


# ---------------------------------------------------------------- C01 : chemins et fichiers
c = [txt(10, 20, "Un chemin = un lecteur + des dossiers + un nom + une extension", TITRE, True)]
morceaux = [("C:/", AMBRE), ("Users/a.minani/Documents/Sahel/", BLEU), ("01_Extract/", VERT),
            ("ventes_magasin5_2025", GRIS), (".csv", ROUGE)]
notes = ["lecteur", "dossiers", "sous-dossier", "nom", "extension"]
x, y0 = 10, 34
for i, (part, col) in enumerate(morceaux):
    w = 6.7 * len(part) + 10
    c.append(f'<rect x="{x}" y="{y0}" width="{w}" height="24" fill="{col}" stroke="{TRAIT}" stroke-width="0.7"/>')
    c.append(txt(x + w / 2, y0 + 16, part, 11.5, ancre="middle"))
    c.append(txt(max(x + 2, 62), y0 + 38, notes[i], 9.5, couleur="#41505f",
                 ancre=("middle" if i in (0, 4) else "start")))
    x += w
c.append(txt(10, 88, "Séparateur : « / » sous Linux, macOS et dans Python ; « \\ » sous Windows.", 10.5))
c.append(txt(10, 101, "Excel et Python acceptent les deux ; l'Explorateur Windows n'en accepte qu'un.", 10.5, couleur="#41505f"))
y = 114
for nom, legende, note in [("ventes_magasin5_2025.csv", "le fichier des ventes du magasin 5, année 2025", "nom écrit par vous, date explicite"),
                           ("ventes_magasin5_2025_v2.xlsx", "la version 2, retravaillée dans Excel", "piège : « v2 » ne dit ni qui ni quand"),
                           ("rapport_final(1).pdf", "le même rapport téléchargé deux fois", "piège : nom fabriqué par le navigateur")]:
    c.append(boite(10, y, 240, 28, nom, GRIS, 11.5))
    c.append(txt(262, y + 12, legende, 11))
    c.append(txt(262, y + 25, note, 10, couleur=(ERREUR if "piège" in note else "#41505f")))
    y += 36
c.append(txt(10, y + 6, "Convention du manuel : AAAA-MM-JJ_quoi_qui.ext, sans espace ni accent.", 11.5, True))
c.append(txt(10, y + 22, "exemple : 2026-09-17_ventes_M5_minani.csv", 11, couleur="#1a7f4b"))
open(os.path.join(OUT, "M01_C01_chemins.svg"), "w", encoding="utf-8").write(
    svg(y + 32, "".join(c), "Figure 1 — Décortiquer un chemin, et les trois noms de fichiers qui posent problème dès la première semaine."))

# ------------------------------------------------- C02 : donnée → information → connaissance → décision
c = [txt(10, 20, "La chaîne qui transforme une ligne de caisse en décision", TITRE, True)]
etapes = [("DONNÉE", ["11 × 4 500 = 48 015 FCFA", "valeur isolée, sans", "contexte ni période"], BLEU),
          ("INFORMATION", ["36 073 185 FCFA de CA", "magasin 5, année 2025", "donnée replacée"], VERT),
          ("CONNAISSANCE", ["décembre = 4,2 × mai", "la Plomberie pèse 24,3 %", "comparaison utile"], AMBRE),
          ("DÉCISION", ["avancer les stocks de", "plomberie au 1er déc.", "un acte, un chef"], ROUGE)]
x = 10
for nom, lignes, col in etapes:
    c.append(boite(x, 34, 175, 26, nom, col, 12.5))
    for k, li in enumerate(lignes):
        c.append(txt(x + 6, 76 + 14 * k, li, 9.5, couleur=("#1c2430" if k == 0 else "#41505f")))
    if x > 10:
        c.append(fleche(x - 16, 47, x - 2, 47))
    x += 188
c.append(txt(10, 126, "Tout le métier est dans les deux flèches du milieu : sans comparaison, rien ne se décide.", NOTE, True))
c.append(boite(10, 138, 740, 40, "", GRIS, 11, gras=False))
c.append(txt(20, 154, "Demande reçue   : « le magasin 5 marche bien ? » — ni prouvable, ni réfutable.", 11))
c.append(txt(20, 167, "Question analytique : « quel mois de 2025 s'écarte le plus de la médiane mensuelle ? »", 11, True))
open(os.path.join(OUT, "M01_C02_chaine.svg"), "w", encoding="utf-8").write(
    svg(190, "".join(c), "Figure 2 — Les quatre maillons, chiffrés sur le fichier réel de l'atelier (ventes_magasin5_2025.csv)."))

# ---------------------------------------------------------------- C03 : anatomie d'une table
c = [txt(10, 18, "Une table vue de près : en-têtes, variables (colonnes), observations (lignes)", TITRE, True)]
cols = ["n_ticket", "date", "magasin", "vendeur", "client", "quantite", "prix_unitaire_ht", "montant_ttc"]
vals = [["T05-250101-075845", "2025-01-01", "Magasin 5", "Moussa I.", "10857", "11", "4 500", "56 658"],
        ["T05-250101-075845", "2025-01-01", "Magasin 5", "Moussa I.", "0.0", "2", "12 000", "28 320"],
        ["T05-250101-075846", "2025-01-01", "Magasin 5", "Salamatu S.", "", "2 000", "21 950", "51 802"],
        ["T05-250102-075902", "2025-01-02", "Magasin 5", "Adama B.", "3312", "1", "14 000", "16 520"]]
w = [132, 62, 62, 68, 46, 54, 92, 82]
x0, y0, rh = 10, 30, 24
x = x0
for i, h in enumerate(cols):
    c.append(f'<rect x="{x}" y="{y0}" width="{w[i]}" height="{rh}" fill="#dfe6ef" stroke="{TRAIT}" stroke-width="0.7"/>')
    c.append(txt(x + w[i] / 2, y0 + 16, h, (9 if len(h) > 12 else 10), True, ancre="middle"))
    x += w[i]
for j, ligne in enumerate(vals):
    x = x0
    for i, v in enumerate(ligne):
        c.append(f'<rect x="{x}" y="{y0 + rh * (j + 1)}" width="{w[i]}" height="{rh}" '
                 f'fill="{"#fff" if j % 2 else "#f7f8fa"}" stroke="{GRIS_T}" stroke-width="0.6"/>')
        c.append(txt(x + 5, y0 + rh * (j + 1) + 16, v, 10))
        x += w[i]
# trois repères numérotés, dessinés dans la cellule pour ne jamais masquer une valeur
c.append(f'<rect x="{x0}" y="{y0 + rh}" width="{w[0]}" height="{rh * 2}" fill="none" stroke="#b07a10" stroke-width="1.6"/>')
c.append(txt(x0 + w[0] - 14, y0 + rh * 2 + 17, "①", 12, couleur="#b07a10"))
cx = x0 + sum(w[:4])
c.append(f'<rect x="{cx}" y="{y0 + rh * 2}" width="{w[4]}" height="{rh}" fill="none" stroke="#1a7f4b" stroke-width="1.6"/>')
c.append(txt(cx + w[4] - 14, y0 + rh * 2 + 17, "②", 12, couleur="#1a7f4b"))
c.append(f'<rect x="{cx}" y="{y0 + rh * 3}" width="{w[4]}" height="{rh}" fill="none" stroke="#b3261e" stroke-width="1.6"/>')
c.append(txt(cx + w[4] - 14, y0 + rh * 3 + 17, "③", 12, couleur="#b3261e"))
yy = y0 + rh * 5 + 20
for marqueur, couleur, lignes in [
        ("①", "#b07a10", ["un ticket occupe 2 lignes : compter les lignes pour compter les ventes gonfle le résultat de 55 %",
                          "(le fichier compte 489 lignes, 316 tickets, et jusqu'à 4 lignes pour un même ticket)."]),
        ("②", "#1a7f4b", ["« 0.0 » n'est pas un manque : c'est la vente au comptoir, sans client identifié.",
                          "Elle est volontaire dans le fichier et doit rester dans les totaux."]),
        ("③", "#b3261e", ["cellule vide = valeur absente : 18 lignes du fichier sont dans ce cas.",
                          "On signale, on documente, on ne remplit pas au hasard."])]:
    for k, li in enumerate(lignes):
        c.append(txt(10, yy, (f"{marqueur} " if k == 0 else "     ") + li, 10.5, couleur=couleur))
        yy += 15
    yy += 3
for t_ in ["Grain : une ligne = un article vendu sur un ticket ; 1,52 ligne par ticket en moyenne.",
           "Clé : n_ticket identifie le ticket ; (n_ticket, produit) identifie la ligne. Sans clé, pas de fusion propre.",
           "Schéma : les 13 colonnes et leur type. Le CSV ne le dit pas : le déduire, puis le vérifier."]:
    c.append(txt(10, yy, "· " + t_, 10.5))
    yy += 15
open(os.path.join(OUT, "M01_C03_table.svg"), "w", encoding="utf-8").write(
    svg(yy + 2, "".join(c), "Figure 3 — Les quatre premières lignes réelles du fichier de l'atelier, annotées."))

# ---------------------------------------------------------------- C04 : types de données
c = [txt(10, 18, "Le même nombre, deux destins", TITRE, True)]
col_t = [("montant_ttc écrit en NOMBRE", VERT, ["56 658", "28 320", "aligné à droite", "SOMME = 84 978 FCFA", "moyenne, tri, graphique : OK"]),
         ("montant_ttc écrit en TEXTE", ROUGE, ["'56 658 ", "'28 320 ", "aligné à gauche", "SOMME = 0", "tri : 16 520 avant 56 658"]),
         ("le même défaut, mesuré ici", GRIS, ["486 lignes sur 489 sont du texte", "déguisé en montant", "→ 0,74 % d'écart de total", "18 clients absents", "65 dates au format français"])]
x = 10
for titre, col, lignes in col_t:
    c.append(boite(x, 30, 244, 24, titre, col, 11))
    for k, li in enumerate(lignes):
        c.append(txt(x + 8, 70 + 17 * k, li, 10.5, gras=(k in (0, 1))))
    x += 258
c.append(f'<line x1="10" y1="160" x2="750" y2="160" stroke="{GRIS_T}"/>')
x = 10
for nom, col, ex1, ex2 in [("TEXTE", GRIS, "vendeur, categorie", "on trie, on regroupe"),
                          ("NOMBRE", BLEU, "quantite, prix_unitaire", "sommes et moyennes"),
                          ("DATE", VERT, "date (vrai objet-date)", "intervalles, mois"),
                          ("BOOLEEN", AMBRE, "est_retour : 0 ou 1", "filtrer les retours"),
                          ("MONTANT", ROUGE, "montant_ttc en FCFA", "TVA 18 %, arrondi")]:
    c.append(boite(x, 172, 140, 22, nom, col, 11.5))
    c.append(txt(x + 70, 208, ex1, 10, ancre="middle"))
    c.append(txt(x + 70, 221, ex2, 10, ancre="middle", couleur="#41505f"))
    x += 150
c.append(txt(10, 242, "Symptômes : total à 0, tri absurde, triangles verts en coin de cellule.", NOTE, True))
open(os.path.join(OUT, "M01_C04_types.svg"), "w", encoding="utf-8").write(
    svg(254, "".join(c), "Figure 4 — Le défaut n° 1 des fichiers livrés, vu sans calculer et mesuré sur le fichier réel."))

# ---------------------------------------------------------------- C05 : classer les données
c = [txt(10, 18, "Deux classements, pas un seul", TITRE, True)]
for i, (nom, col, ex) in enumerate([("STRUCTURÉE", BLEU, "les 10 fichiers du socle : CSV, XLSX"),
                                    ("SEMI-STRUCTURÉE", VERT, "JSON des logs de caisse, XML d'un export Sage, e-mails"),
                                    ("NON STRUCTURÉE", AMBRE, "SMS du commercial, photo d'un bon, PDF du fournisseur")]):
    y = 34 + i * 46
    c.append(boite(10, y, 160, 24, nom, col, 11.5))
    c.append(txt(182, y + 16, ex, 11))
c.append(f'<line x1="10" y1="172" x2="750" y2="172" stroke="{GRIS_T}"/>')
c.append(boite(10, 184, 250, 24, "QUANTITATIVE : on peut calculer", BLEU, 11.5))
c.append(txt(20, 226, "discrète : quantite (11, 2, 2 000 — jamais 1,5)", 10.5))
c.append(txt(20, 241, "continue : poids_kg, taux_remise (0,032)", 10.5))
c.append(boite(278, 184, 250, 24, "QUALITATIVE : on peut classer", GRIS, 11.5))
c.append(txt(288, 226, "nominale : categorie (aucun ordre)", 10.5))
c.append(txt(288, 241, "ordinale : type_client (ordre connu)", 10.5))
c.append(boite(546, 184, 204, 24, "LE TEST QUI CLASSE", AMBRE, 11.5))
c.append(txt(556, 226, "« 2 catégories valent-elles", 10.5))
c.append(txt(556, 241, "2 fois l'autre ? » sinon, ce", 10.5))
c.append(txt(556, 254, "n'est pas une échelle ratio.", 10.5))
c.append(txt(10, 276, "Ce que la colonne EST décide ce que vous avez le DROIT de calculer.", NOTE, True))
c.append(txt(474, 276, "la moyenne d'une nominale est un non-sens", 10, couleur="#41505f"))
open(os.path.join(OUT, "M01_C05_classer.svg"), "w", encoding="utf-8").write(
    svg(288, "".join(c), "Figure 5 — Classer les colonnes du socle, c'est déjà savoir quels calculs seront licites au module 2."))

# ---------------------------------------------------------------- C06 : cycle de vie
c = [txt(10, 18, "Le voyage d'une ligne, de la caisse au rapport annuel", TITRE, True)]
etapes = [("NAISSANCE", "caisse magasin 5", "01/01/2025 11:01", BLEU),
          ("STOCKAGE", "export CSV", "28,5 Mo, brut", BLEU),
          ("TRANSFORMATION", "nettoyage", "489 → 480 lignes", VERT),
          ("USAGE", "tableau de bord", "12 lecteurs", VERT),
          ("ARCHIVAGE", "classeur 2023-24", "lecture seule", GRIS),
          ("SUPPRESSION", "purge + registre", "le dico survit", GRIS)]
x = 10
for i, (nom, l1, l2, col) in enumerate(etapes):
    c.append(boite(x, 30, 108, 26, nom, col, 10.5))
    c.append(txt(x + 54, 72, l1, 9, ancre="middle"))
    c.append(txt(x + 54, 84, l2, 9, ancre="middle", couleur="#41505f"))
    if i:
        c.append(fleche(x - 16, 43, x - 2, 43))
    x += 122
c.append(f'<line x1="10" y1="98" x2="750" y2="98" stroke="{GRIS_T}"/>')
c.append(txt(10, 116, "Responsable : caissier → admin. de l'ERP → vous → le BI → la DAF → la DAF, encore.", NOTE))
for i, t_ in enumerate(["Où le chiffre meurt : export coupé, fichier réécrasé, arrondi, filtre oublié, fusion dupliquée (+9 lignes ici).",
                        "Ce qui prouve votre travail dans trois ans : le journal de transformation et le dictionnaire, pas votre mémoire.",
                        "Règle du manuel : on ne modifie jamais un fichier brut ; du brut on tire du propre, et on garde les deux."]):
    c.append(txt(10, 138 + 16 * i, "· " + t_, 10.5, couleur=("#1c2430")))
open(os.path.join(OUT, "M01_C06_cycle.svg"), "w", encoding="utf-8").write(
    svg(190, "".join(c), "Figure 6 — Six étapes, cinq responsables, et l'endroit exact où votre total peut disparaître."))

# ---------------------------------------------------------------- C07 : métiers et cadrage
c = [txt(10, 18, "Qui fait quoi, et les cinq questions à écrire avant de toucher un fichier", TITRE, True)]
metiers = [("DATA ENGINEER", "prépare flux,", "bases, qualité", "Airflow · SQL · DuckDB", BLEU),
           ("DATA ANALYST", "pose les questions,", "mesure, explique", "Excel · SQL · Python", VERT),
           ("BI ANALYST", "modélise, construit", "les tableaux durables", "Power BI · DAX", AMBRE),
           ("DATA SCIENTIST", "prévoit, teste,", "modélise l'inconnu", "Python · R · stats", GRIS),
           ("DÉCIDEUR", "choisit, assume,", "finance", "votre note de 2 pages", "#f7f7f5")]
x = 10
for nom, l1, l2, l3, col in metiers:
    c.append(boite(x, 32, 136, 26, nom, col, 10.5))
    c.append(txt(x + 68, 74, l1, 10, ancre="middle"))
    c.append(txt(x + 68, 87, l2, 10, ancre="middle"))
    c.append(txt(x + 68, 103, l3, 10, ancre="middle", couleur="#41505f"))
    if x > 10:
        c.append(fleche(x - 14, 45, x - 2, 45))
    x += 148
c.append(f'<line x1="10" y1="116" x2="750" y2="116" stroke="{GRIS_T}"/>')
for i, q in enumerate(["1. Décision visée — qu'est-ce qui changera selon la réponse ?",
                       "2. Question analytique — une phrase : unité (FCFA TTC), période (2025), périmètre (magasin 5), comparaison.",
                       "3. Donnée nécessaire — la table, le grain, la colonne, le fichier exact.",
                       "4. Critère de réussite — le chiffre attendu, la tolérance, qui valide, avant de calculer.",
                       "5. Limites — ce que le résultat ne dira pas : ici, pas de marge nette (aucun coût de structure dans le jeu)."]):
    c.append(txt(14, 134 + 17 * i, q, 10.5, gras=(i == 0)))
open(os.path.join(OUT, "M01_C07_metiers.svg"), "w", encoding="utf-8").write(
    svg(228, "".join(c), "Figure 7 — La chaîne de valeur, et le formulaire de cadrage resservi dans les 22 modules."))

n = len([f for f in os.listdir(OUT) if f.startswith('M01')])
print(f"{n} figures M01 écrites dans {OUT}")
if ALERTES:
    print("\n".join(dict.fromkeys(ALERTES)))
    raise SystemExit("_corriger les débordements ci-dessus (largeur max %d px)_" % (L - 8))
