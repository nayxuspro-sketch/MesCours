#!/usr/bin/env python3
"""classeur_M03.py — fabrique le classeur d'atelier du module M03 (Excel).

Le fichier produit n'est pas un accessoire : c'est la **preuve exécutable** du module.
Il contient les deux fichiers de travail (l'énoncé reçu, l'attendu nettoyé), les
référentiels, une feuille `Calculs` qui écrit en dur chaque formule enseignée, un
`TCD` reconstruit à la main par COUNTIFS/SUMIFS/AVERAGEIFS, et une feuille mensuelle
qui rapproche les ventes des objectifs. Les valeurs attendues sont lues dans
`chiffres_cites.json` : le classeur et le manuel ne peuvent donc pas diverger.

Les formules sont écrites en **noms anglais**, parce que c'est ce que le fichier `.xlsx`
stocke réellement — en français, Excel affiche `SOMME` mais écrit `SUM`. C'est ce qui
permet à `tools/controle_formules.py` de les recalculer.

Usage : python3 tools/classeur_M03.py
"""
import json, os, datetime as dt
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REF = os.path.join(ROOT, "01_socle_donnees", "data", "reference")
PROJ = os.path.join(ROOT, "01_socle_donnees", "data", "projection")
BRUT = os.path.join(ROOT, "01_socle_donnees", "data", "brut")
OUT = os.path.join(PROJ, "m03_classeur_atelier.xlsx")

GRAS = Font(bold=True)
FOND = PatternFill("solid", fgColor="EDF3F8")
FIN = PatternFill("solid", fgColor="F7F1E3")
GRIS = Font(color="666666", size=9)
LIRE = Font(color="1F4E79", bold=True)
CADRE = Border(bottom=Side(style="thin", color="CCCCCC"))
MONNAIE = '#\u202f##0\u202f"FCFA"'
PCT = "0,0%"


def cle_categorie(nom):
    import unicodedata
    s = "".join(c for c in unicodedata.normalize("NFKD", str(nom)) if not unicodedata.combining(c))
    return "".join(ch if ch.isalnum() else "_" for ch in s.lower()).strip("_")


def entetes(ws, cols, largeurs):
    ws.append(cols)
    for i, w in enumerate(largeurs, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for c in ws[1]:
        c.font = GRAS
        c.fill = FOND
        c.alignment = Alignment(vertical="center")
    ws.freeze_panes = "A2"


def main():
    K = json.load(open(os.path.join(REF, "chiffres_cites.json"), encoding="utf-8"))["M03"]
    en = pd.read_csv(os.path.join(PROJ, "ventes_magasin5_2025.csv"), sep=";", encoding="utf-8-sig",
                     dtype=str, keep_default_na=False)
    p = pd.read_csv(os.path.join(REF, "ventes_magasin5_2025_ATTENDU.csv"), sep=";")
    produits = pd.read_csv(os.path.join(REF, "produits_propres.csv"))
    clients = pd.read_csv(os.path.join(REF, "clients_propres.csv"))
    magasins = pd.read_csv(os.path.join(BRUT, "magasins.csv"))
    vendeurs = pd.read_csv(os.path.join(BRUT, "vendeurs.csv"))
    objectifs = pd.read_csv(os.path.join(BRUT, "objectifs_de_ca.csv"), sep=";", encoding="cp1252")
    objectifs.columns = [c.strip() for c in objectifs.columns]
    n = len(p)
    derniers = n + 1

    wb = Workbook()

    # ---------------------------------------------------------------- Aidez-moi
    ws = wb.active
    ws.title = "Aidez-moi"
    ws.column_dimensions["A"].width = 112
    lignes = [
        ("Classeur d'atelier — module M03 (Excel pour l'analyse de données)", GRAS),
        ("", None),
        (f"Généré le {dt.date.today().isoformat()} par tools/classeur_M03.py. Ne pas modifier à la main : "
         f"toute valeur de contrôle provient de 01_socle_donnees/data/reference/chiffres_cites.md.", GRIS),
        ("", None),
        ("Feuilles et à quoi elles servent :", GRAS),
        ("  ventes_brutes — le fichier REÇU par l'entreprise : %d lignes × %d colonnes, tout en texte, "
         "défauts compris (montants avec séparateur, dates manuscrites, doublons)." % (K["m03_lignes_enonce"], K["m03_colonnes"]), None),
        ("  ventes — le fichier NETTOYÉ (l'attendu du projet M01) : %d lignes, types corrigés, montants en nombres. "
         "C'est la feuille de travail du module." % K["m03_lignes_attendu"], None),
        ("  produits · clients · magasins · vendeurs · objectifs — les référentiels, pour les recherches "
         "(RECHERCHEX, INDEX/EQUIV) et le rapprochement des objectifs.", None),
        ("  Calculs — une ligne par fonction de la fiche : le nom affiché, la formule telle qu'elle est stockée, "
         "la valeur attendue, la valeur rendue, et une colonne de contrôle.", None),
        ("  TCD — le tableau croisé que votre TCD doit reproduire, construit au COUNTIFS/SUMIFS. "
         "Si votre TCD ne rend pas ces nombres, l'un des deux a tort.", None),
        ("  Mensuel — le chiffre d'affaires mois par mois et l'objectif correspondant, avec le doute "
         "à lire avant toute conclusion de performance.", None),
        ("", None),
        ("Trois choses à vérifier avant de toucher à une formule :", GRAS),
        ("  1. la barre de formule montre ce que la cellule CONTIENT ; l'affichage montre ce qu'elle MONTRE ;", None),
        ("  2. %d montants sur %d de la feuille ventes_brutes sont du texte : un =SOMME() y renvoie 0, "
         "et ce n'est pas une erreur du tableur ;" % (K["m03_montant_lus_comme_texte"], K["m03_lignes_enonce"]), None),
        ("  3. la dernière cellule utilisée de la feuille ventes est N%d : 13 colonnes de données plus la colonne "
         "utilitaire ; le fichier plat, lui, s'arrête en %s. Si votre sélection s'arrête avant, vous perdez des lignes "
         "sans le savoir." % (len(p) + 1, K["m03_derniere_cellule_attendu"]), None),
        ("", None),
        ("En cas d'écart avec le manuel : relancer `python3 01_socle_donnees/scripts/chiffres_manuel.py M01 M02 M03` "
         "puis `python3 tools/classeur_M03.py`.", GRIS),
    ]
    for txt, f in lignes:
        ws.append([txt])
        if f:
            ws.cell(ws.max_row, 1).font = f

    # ---------------------------------------------------------------- ventes_brutes (tout en texte, verbatim)
    ws = wb.create_sheet("ventes_brutes")
    entetes(ws, list(en.columns), [22, 11, 7, 26, 20, 8, 40, 14, 9, 13, 8, 12, 13])
    for row in en.itertuples(index=False):
        ws.append(list(row))
    ws.auto_filter.ref = "A1:M%d" % (len(en) + 1)

    # Ce que le tableur VOIT dans la feuille reçue, une fois le classeur ouvert : les montants y sont du
    # texte, donc NB compte 0 et SOMME additionne 0. C'est la leçon de C02 §5.1 et de C05 §5.6, et c'est
    # ce que la feuille « Calculs » doit annoncer comme valeur attendue — sinon l'auto-contrôle du classeur
    # rougit à la première ouverture. Les nombres du CSV (3 montants saisis sans séparateur de milliers,
    # 2 444 FCFA) sont gardés dans le commentaire de la fiche, qui explique le décrochage.
    nb_brut = sum(1 for v in en["montant_ttc"] if isinstance(v, (int, float)))
    somme_brut = round(sum(float(v) for v in en["montant_ttc"] if isinstance(v, (int, float))), 0)
    lignes_brutes = ", ".join(str(x) for x in K["m03_lignes_montants_nombres"])

    # ---------------------------------------------------------------- ventes (types corrigés + tableau structuré)
    ws = wb.create_sheet("ventes")
    entetes(ws, list(p.columns), [22, 11, 7, 26, 20, 8, 40, 14, 9, 13, 8, 12, 13])
    for row in p.itertuples(index=False):
        vals = []
        for c, v in zip(p.columns, row):
            if c == "date":
                vals.append(dt.datetime.strptime(str(v), "%Y-%m-%d"))
            elif c in ("quantite",):
                vals.append(int(v))
            elif c == "client":
                # les identifiants clients arrivent en flottant (10857.0) à cause des 18 vides :
                # on les écrit en entier, sinon la recherche C06 ne trouve plus la clé.
                vals.append("" if pd.isna(v) else int(round(float(v))))
            elif c in ("prix_unitaire_ht", "remise", "montant_ht", "montant_ttc"):
                vals.append(float(v))
            else:
                vals.append("" if pd.isna(v) else str(v))
        ws.append(vals)
    ws.cell(1, 14, "montant recalculé (colonne utilitaire)").font = GRAS
    for r in range(2, derniers + 1):
        ws.cell(r, 14, "=ROUND(I%d*J%d*(1-K%d),0)" % (r, r, r))
        ws.cell(r, 14).number_format = MONNAIE
        ws.cell(r, 2).number_format = "DD/MM/YYYY"
        for col in (10, 12, 13):
            ws.cell(r, col).number_format = MONNAIE
        ws.cell(r, 11).number_format = "0%"
    tab = Table(displayName="TableVentes", ref="A1:M%d" % derniers)
    tab.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2", showRowStripes=True)
    ws.add_table(tab)

    # ---------------------------------------------------------------- référentiels
    ws = wb.create_sheet("produits")
    entetes(ws, list(produits.columns), [10, 40, 16, 18, 7, 12, 12, 16, 16, 6, 6])
    for row in produits.itertuples(index=False):
        ws.append([None if pd.isna(v) else (float(v) if isinstance(v, (int, float)) else str(v)) for v in row])
    nb_prod = len(produits)

    ids = set(p["client"].astype(str).str.replace(".0", "", regex=False))
    cli = clients[clients["id_client"].astype(str).isin(ids)]
    ws = wb.create_sheet("clients")
    entetes(ws, list(clients.columns), [10, 22, 12, 14, 14, 20, 22, 12, 10, 12, 12])
    for row in cli.itertuples(index=False):
        ws.append([None if pd.isna(v) else (float(v) if isinstance(v, (int, float)) else str(v)) for v in row])
    nb_cli = len(cli)

    for nom, df in (("magasins", magasins), ("vendeurs", vendeurs)):
        ws = wb.create_sheet(nom)
        entetes(ws, list(df.columns), [11, 34, 14, 14, 14, 12, 11, 12, 12])
        for row in df.itertuples(index=False):
            ws.append([None if pd.isna(v) else (float(v) if isinstance(v, (int, float)) else str(v)) for v in row])

    ws = wb.create_sheet("objectifs")
    entetes(ws, list(objectifs.columns), [11, 8, 7, 12, 16, 16])
    for row in objectifs.itertuples(index=False):
        ws.append([float(v) if isinstance(v, (int, float)) else str(v) for v in row])
    nb_obj = len(objectifs)

    # ---------------------------------------------------------------- Calculs : le catalogue de formules
    ws = wb.create_sheet("Calculs")
    entetes(ws, ["n°", "Fonction (telle que l'affiche Excel FR)", "Formule, telle qu'elle est stockée",
                 "Valeur que la formule doit rendre", "Ce que la formule rend", "contrôle"],
            [5, 40, 74, 30, 30, 12])
    L = "ventes!M2:M%d" % derniers
    B = "ventes!B2:B%d" % derniers
    E = "ventes!E2:E%d" % derniers
    F = "ventes!F2:F%d" % derniers
    H = "ventes!H2:H%d" % derniers
    I = "ventes!I2:I%d" % derniers
    J = "ventes!J2:J%d" % derniers
    Kc = "ventes!K2:K%d" % derniers
    Lh = "ventes!L2:L%d" % derniers
    Gcol = "ventes!G2:G%d" % derniers
    Mcol = "ventes!M2:M%d" % derniers
    MB = "ventes_brutes!M2:M%d" % (K["m03_lignes_enonce"] + 1)
    IB = "ventes_brutes!I2:I%d" % (K["m03_lignes_enonce"] + 1)
    fiches = [
        ("NB sur la colonne des montants", "=COUNT(%s)" % L, K["m03_lignes_attendu"],
         "les 480 montants réellement numériques de la feuille nettoyée"),
        ("NBVAL — compter tout ce qui est écrit", "=COUNTA(ventes_brutes!A2:A%d)" % (K["m03_lignes_enonce"] + 1),
         K["m03_lignes_enonce"], "les 489 lignes reçues, nombres et textes confondus"),
        ("NB appliqué aux montants reçus", "=COUNT(%s)" % MB, nb_brut,
         "le symptôme de l'import raté, dans le classeur : %d montant numérique sur %d. Le CSV reçu en contient "
         "%d (lignes %s), mais en collant la feuille dans un classeur ils redeviennent du texte — voyez C02 §5.1."
         % (nb_brut, K["m03_lignes_enonce"], K["m03_montant_lus_comme_nombres"], lignes_brutes)),
        ("SOMME sur la feuille reçue", "=SUM(%s)" % MB, somme_brut,
         "le cas le plus dangereux du module : un total faux, zéro franc, et aucune erreur affichée. Le même "
         "=SOMME() sur le CSV importé avec conversion rend %s FCFA — les %d lignes saisies sans séparateur de "
         "milliers (lignes %s), et rien de plus."
         % (format(int(K["m03_ca_enonce_partiel"]), ",").replace(",", " "),
            K["m03_montant_lus_comme_nombres"], lignes_brutes)),
        ("SOMME", "=SUM(%s)" % L, K["m03_ca_attendu"], "le total de référence du module, sur la feuille nettoyée"),
        ("MOYENNE", "=AVERAGE(%s)" % L, K["m03_moyenne_ligne"], "au niveau de la ligne, pas du ticket"),
        ("MEDIANE", "=MEDIAN(%s)" % L, K["m03_mediane_ligne"], "le centre robuste du module M02"),
        ("ECARTYPE.STANDARD", "=STDEV.S(%s)" % L, K["m03_ecart_type_ligne"], "dispersion sur échantillon"),
        ("MAX", "=MAX(%s)" % L, K["m03_max_ligne"], "et sa voisine MIN, qui est négative"),
        ("MIN", "=MIN(%s)" % L, K["m03_min_ligne"], "un retour de marchandise, pas une saisie farfelue"),
        ("QUARTILE.INC · premier", "=QUARTILE.INC(%s,1)" % L, K["m03_q1_ligne"], "méthode inclusive, celle d'Excel 2010 et suivants"),
        ("QUARTILE.INC · troisième", "=QUARTILE.INC(%s,3)" % L, K["m03_q3_ligne"], "le IQR se lit dans la foulée"),
        ("NB.SI sur la quantité reçue", '=COUNTIF(%s,">500")' % IB, K["m03_quantite_au_dessus_de_500"],
         "les sept quantités hors échelle du fichier reçu"),
        ("SOMME.SI.ENS catégorie", '=SUMIFS(%s,%s,"Plomberie")' % (L, H), K["m03_tcd_plomberie_ca"],
         "le CA d'un rayon, une condition"),
        ("MOYENNE.SI.ENS", '=AVERAGEIFS(%s,%s,"Electricité")' % (L, H), K["m03_tcd_electricite_moyenne"],
         "moyenne conditionnelle"),
        ("NB.SI.ENS deux conditions", '=COUNTIFS(%s,"Peinture",%s,">0")' % (H, Kc), K["m03_tcd_peinture_remises"],
         "les lignes remisées du rayon Peinture"),
        ("RECHERCHEV, le piège classique", '=VLOOKUP(%d,%s!G2:J%d,4,FALSE)' % (K["m03_max_ligne"], "ventes", derniers),
         "#N/A", "la valeur cherchée n'est pas dans la PREMIÈRE colonne de la plage : c'est l'exercice 6.2"),
        ("RECHERCHEX, le même voyage", '=XLOOKUP(ventes!M%d,%s,%s,"non trouvé")' % (K["m03_ligne_plus_gros_montant_ligne"], Mcol, Gcol),
         K["m03_produit_du_plus_gros_montant"], "aucun numéro de colonne à compter, et un mot de secours en cas d'absence"),
        ("INDEX / EQUIV, la voie compatible", "=INDEX(%s,MATCH(MAX(%s),%s,0))" % (Gcol, L, L),
         K["m03_produit_du_plus_gros_montant"], "ce que vous écrivez en 2019 et sous LibreOffice"),
        ("EQUIV · la position", "=MATCH(MAX(%s),%s,0)" % (L, L), K["m03_ligne_plus_gros_montant_position"],
         "position dans la plage ; ajoutez 1 pour obtenir la ligne du classeur, et vérifiez : %s" % K["m03_cellule_plus_gros_montant_ligne"]),
        ("Tester si la colonne est entièrement numérique", '=IF(COUNT(%s)=COUNTA(%s),"tout est nombre","du texte s’est glissé")'
         % (MB, MB), "du texte s’est glissé",
         "NB = NBVAL est le test de conformité d'une colonne numérique ; à écrire une fois par fichier, pas une fois par question"),
        ("Réparer une cellule", '=VALUE(SUBSTITUTE(ventes_brutes!M2," ",""))', K["m03_premiere_ligne_montant"],
         "la première ligne du fichier reçu, redevenue un nombre"),
        ("Joindre les valeurs distinctes", '=TEXTJOIN(", ",TRUE,UNIQUE(%s))' % H, K["m03_categories_ordre_fichier"],
         "les sept rayons en une cellule, dans l'ordre du fichier"),
        ("JOURS OUVRES", "=NETWORKDAYS(DATE(2025,1,1),DATE(2025,12,2))", K["m03_jours_ouvres_entre_min_max"],
         "le dénominateur d'une moyenne journalière honnête"),
        ("Amplitude réelle de l'extrait", "=MAX(%s)-DATE(2025,1,1)" % B, K["m03_jours_entre_min_max"],
         "une soustraction de dates rend un nombre de jours ; c'est plus lisible que DATEDIF et cela marche partout"),
        ("Attraper l'erreur", '=IFERROR(1/0,"rien à afficher")', "rien à afficher",
         "à n'utiliser que si vous savez quelle erreur vous cachez"),
        ("Contrôle de cohérence du montant", "=ROUND(SUM(ventes!N2:N%d)-SUM(%s),0)" % (derniers, Lh),
         K["m03_ecart_controle_montant_ht"],
         "la colonne utilitaire N recalcule quantité × prix × (1 − remise) ; l'écart avec le montant enregistré doit se "
         "compter en francs, pas en milliers"),
        ("Réalisation vs objectif, extrait", "=SUM(%s)/SUMIFS(objectifs!E2:E%d,objectifs!A2:A%d,5,objectifs!B2:B%d,2025)"
         % (L, nb_obj + 1, nb_obj + 1, nb_obj + 1), K["m03_realisation_extrait_pct"] / 100.0,
         "18,2 % : ce ratio compare un extrait de 4 jours par mois à une cible annuelle. Il ne dit rien de la performance"),
    ]
    r = 1
    for i, (nom, formule, attendu, dis) in enumerate(fiches, start=1):
        r += 1
        ws.cell(r, 1, i)
        ws.cell(r, 2, nom)
        ws.cell(r, 3, formule.replace("=", "", 1))
        ws.cell(r, 3).font = Font(name="Menlo", size=9)
        if attendu is not None:
            c = ws.cell(r, 4, attendu)
            c.number_format = "0.000%" if "objectif" in nom else "#,##0.####"
        ws.cell(r, 5, formule)
        ws.cell(r, 5).number_format = "#,##0.####"
        ws.cell(r, 6, '=IF(EXACT(D%d,E%d),"ok","à revoir")' % (r, r) if attendu is not None else "—")
        ws.cell(r, 7, dis).font = GRIS
    ws.column_dimensions["G"].width = 74
    ws.freeze_panes = "A2"
    nb_fiches = len(fiches)

    # ---------------------------------------------------------------- TCD reconstitué
    ws = wb.create_sheet("TCD")
    entetes(ws, ["categorie", "lignes", "CA (FCFA)", "moyenne par ligne", "part du CA", "lignes remisées"],
            [20, 9, 16, 16, 12, 15])
    cats = list(p["categorie"].dropna().unique())
    tot_row = 1 + len(cats) + 1
    for i, c in enumerate(cats, start=2):
        ws.cell(i, 1, c)
        ws.cell(i, 2, '=COUNTIFS(%s,$A%d)' % (H, i))
        ws.cell(i, 3, '=SUMIFS(%s,%s,$A%d)' % (L, H, i))
        ws.cell(i, 4, '=IFERROR(C%d/B%d,"")' % (i, i))
        ws.cell(i, 5, '=IFERROR(C%d/$C$%d,"")' % (i, tot_row))
        ws.cell(i, 6, '=COUNTIFS(%s,$A%d,%s,">0")' % (H, i, Kc))
        ws.cell(i, 3).number_format = MONNAIE
        ws.cell(i, 4).number_format = MONNAIE
        ws.cell(i, 5).number_format = PCT
    t = tot_row
    ws.cell(t, 1, "Total").font = GRAS
    ws.cell(t, 2, "=SUM(B2:B%d)" % (t - 1))
    ws.cell(t, 3, "=SUM(C2:C%d)" % (t - 1))
    ws.cell(t, 4, "=C%d/B%d" % (t, t))
    ws.cell(t, 5, "=SUM(E2:E%d)" % (t - 1))
    ws.cell(t, 6, "=SUM(F2:F%d)" % (t - 1))
    for col in range(1, 7):
        ws.cell(t, col).fill = FIN
        ws.cell(t, col).font = GRAS
    ws.cell(t, 3).number_format = MONNAIE
    ws.cell(t, 4).number_format = MONNAIE
    ws.cell(t, 5).number_format = PCT
    ws.cell(t + 2, 1, "Le TOTAL de la ligne CA doit être exactement le total de la feuille : s'il diffère d'un "
                      "centime, un filtre est resté actif quelque part.").font = GRIS

    # ---------------------------------------------------------------- Mensuel (ventes ↔ objectifs)
    ws = wb.create_sheet("Mensuel")
    entetes(ws, ["mois", "CA de l'extrait (FCFA)", "nb de lignes", "objectif magasin 5", "CA / objectif",
                 "jours ouvrés du mois"], [7, 20, 12, 20, 14, 16])
    for i in range(1, 13):
        r = 1 + i
        ws.cell(r, 1, i)
        ws.cell(r, 2, '=SUMIFS(%s,%s,">="&DATE(2025,$A%d,1),%s,"<"&DATE(2025,$A%d+1,1))' % (L, B, r, B, r))
        ws.cell(r, 3, '=COUNTIFS(%s,">="&DATE(2025,$A%d,1),%s,"<"&DATE(2025,$A%d+1,1))' % (B, r, B, r))
        ws.cell(r, 4, '=SUMIFS(objectifs!E2:E%d,objectifs!A2:A%d,5,objectifs!B2:B%d,2025,objectifs!C2:C%d,$A%d)'
                % (nb_obj + 1, nb_obj + 1, nb_obj + 1, nb_obj + 1, r))
        ws.cell(r, 5, '=IFERROR(B%d/D%d,"objectif absent")' % (r, r))
        ws.cell(r, 6, '=NETWORKDAYS(DATE(2025,$A%d,1),EOMONTH(DATE(2025,$A%d,1),0))' % (r, r))
        ws.cell(r, 2).number_format = MONNAIE
        ws.cell(r, 4).number_format = MONNAIE
        ws.cell(r, 5).number_format = "0%"
    r = 15
    ws.cell(r, 1, "Total").font = GRAS
    ws.cell(r, 2, "=SUM(B2:B13)").number_format = MONNAIE
    ws.cell(r, 3, "=SUM(C2:C13)")
    ws.cell(r, 4, "=SUM(D2:D13)").number_format = MONNAIE
    ws.cell(r, 5, "=IFERROR(B%d/D%d,\"\")" % (r, r)).number_format = "0%"
    for c in range(1, 7):
        ws.cell(r, c).fill = FIN
        ws.cell(r, c).font = GRAS
    ws.cell(r + 2, 1, "Lecture honnête du ratio CA / objectif : ici l'extrait ne couvre que les jours 1 à 4 de "
                      "chaque mois (voir M02.C07), donc ce ratio ne mesure PAS la performance annuelle du magasin. "
                      "Il mesure un extrait. La population entière donne un rapport de %.2f à %.2f selon le "
                      "magasin-mois (le projet M03.P le discutera avec le fichier complet) : avant de parler de "
                      "surperformance, on vérifie l'échelle du fichier d'objectifs."
            % (K["m03_ratio_ca_objectif_min"], K["m03_ratio_ca_objectif_max"])).font = GRIS

    wb.save(OUT)
    print("classeur écrit →", OUT)
    print("  feuilles :", wb.sheetnames)
    print("  ventes %d lignes · brute %d lignes · produits %d · clients %d · objectifs %d · formules de fiche %d"
          % (n, len(en), nb_prod, nb_cli, nb_obj, nb_fiches))


if __name__ == "__main__":
    main()
