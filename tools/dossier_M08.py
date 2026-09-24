#!/usr/bin/env python3
"""
dossier_M08.py — socle du module M08 « Python pour l'analyse de données ».

Le module M08 n'invente pas de données : il **réexporte en CSV** la base commerciale M07
(figée, empreinte `df9333ff…a1dde`), que l'apprenant doit re-chausser en pandas. Le fil rouge
du module est la **vérification croisée SQL/pandas** : tout indicateur mesuré ici par DuckDB
doit être retrouvé par l'apprenant (et par `chiffres_manuel.py M08`, côté pandas) sans écart.

Usage : python3 tools/dossier_M08.py
Sorties (dossier 03_exercices/dossier_M08/) :
  - 8 CSV, un par table de la base M07 (dont `objectif_magasin.csv`, 0 ligne)
  - 00_brief.md   — le brief remis à l'apprenant
  - ATTENDU.json  — ~25 clés m08p_* (formes, audit, indicateurs ; côté SQL de la croisée)

Déterminisme : aucun tirage aléatoire (la base amont est figée). Deux exécutions → diff = 0.
"""
import hashlib
import json
import os

import duckdb
import pandas as pd

HERE = os.path.abspath(os.path.dirname(__file__))
RACINE = os.path.abspath(os.path.join(HERE, ".."))
SRC_DB = os.path.join(RACINE, "03_exercices", "dossier_M07", "commercial.duckdb")
SRC_ATTENDU = os.path.join(RACINE, "03_exercices", "dossier_M07", "ATTENDU.json")
OUT = os.path.join(RACINE, "03_exercices", "dossier_M08")

# Ordre d'export fixé (le plus gros d'abord) — il entre dans l'empreinte.
TABLES = ["vente", "client", "produit", "categorie", "magasin",
          "mode_paiement", "regle_tva", "objectif_magasin"]


def exporter():
    os.makedirs(OUT, exist_ok=True)
    con = duckdb.connect(SRC_DB, read_only=True)
    formes, empreinte = {}, hashlib.sha256()
    for table in TABLES:
        df = con.execute(f"SELECT * FROM {table}").fetchdf()
        chemin = os.path.join(OUT, table + ".csv")
        df.to_csv(chemin, index=False, encoding="utf-8")
        formes[table] = {"lignes": int(len(df)), "colonnes": int(df.shape[1])}
        with open(chemin, "rb") as fh:
            empreinte.update(fh.read())
    con.close()
    return formes, empreinte.hexdigest()


def mesurer():
    """L'équivalent SQL (DuckDB) des indicateurs pandas de `chiffres_manuel.py M08` :
    c'est la moitié gauche de la vérification croisée."""
    con = duckdb.connect(SRC_DB, read_only=True)
    q = lambda s: con.execute(s).fetchone()[0]
    a = {
        "formes": {},
        # Audit (les 4 défauts du socle M07, re-mesurés)
        "lignes_brutes": q("SELECT COUNT(*) FROM vente"),
        "doublons": q("""
            SELECT COUNT(*) - COUNT(DISTINCT (id_client, id_produit, id_magasin, date_vente,
                   date_limite_remise, quantite, prix_unitaire_ht, taux_tva, montant_ttc,
                   montant_remise, est_retour, id_mode)::VARCHAR)
            FROM vente"""),
        "ventes_uniques": q("""
            SELECT COUNT(*) FROM (SELECT DISTINCT id_client, id_produit, id_magasin, date_vente,
                   date_limite_remise, quantite, prix_unitaire_ht, taux_tva, montant_ttc,
                   montant_remise, est_retour, id_mode FROM vente)"""),
        # P2 — retours : en brut 208 (les 8 doublons sont des copies de lignes retours),
        # 200 après dédoublonnage (le chiffre officiel M07). L'ordre des opérations est la leçon.
        "retours_brut": q("SELECT COUNT(*) FROM vente WHERE est_retour = TRUE"),
        "retours_dedoublonnes": q("""
            SELECT COUNT(*) FROM (
              SELECT DISTINCT id_client, id_produit, id_magasin, date_vente, date_limite_remise,
                     quantite, prix_unitaire_ht, taux_tva, montant_ttc, montant_remise,
                     est_retour, id_mode
              FROM vente) WHERE est_retour = TRUE"""),
        # P3 — dates : la condition naïve (documentée M07 C02) compte 21 406 lignes ;
        # le groupe semé = les deadlines tombant au 20 du mois (15 après dédoublonnage).
        "dates_vente_apres_limite": q(
            "SELECT COUNT(*) FROM vente WHERE date_vente > date_limite_remise"),
        "deadlines_jour_20_brut": q(
            "SELECT COUNT(*) FROM vente WHERE EXTRACT(DAY FROM date_limite_remise) = 20"),
        "deadlines_jour_20": q("""
            SELECT COUNT(*) FROM (
              SELECT DISTINCT id_client, id_produit, id_magasin, date_vente, date_limite_remise,
                     quantite, prix_unitaire_ht, taux_tva, montant_ttc, montant_remise,
                     est_retour, id_mode
              FROM vente) WHERE EXTRACT(DAY FROM date_limite_remise) = 20"""),
        "manquants_total": 0,  # rempli plus bas, colonne par colonne (mesuré, pas affirmé)
        "table_vide": "objectif_magasin",
        # Indicateurs (les réponses pandas du projet M08.P)
        "ca_brut": int(q("SELECT ROUND(SUM(montant_ttc)) FROM vente")),
        "ca_sans_retours": int(q("SELECT ROUND(SUM(montant_ttc)) FROM vente WHERE est_retour = FALSE")),
        "ecart_ca_retours": int(q("SELECT ROUND(SUM(montant_ttc)) FROM vente")) - int(q(
            "SELECT ROUND(SUM(montant_ttc)) FROM vente WHERE est_retour = FALSE")),
        "panier_moyen": int(q("SELECT ROUND(AVG(montant_ttc)) FROM vente")),
        "panier_moyen_sans_retours": int(q(
            "SELECT ROUND(AVG(montant_ttc)) FROM vente WHERE est_retour = FALSE")),
        "nb_ventes_2025": q("SELECT COUNT(*) FROM vente WHERE EXTRACT(YEAR FROM date_vente) = 2025"),
        "ca_2025": q("SELECT ROUND(SUM(montant_ttc)) FROM vente WHERE EXTRACT(YEAR FROM date_vente) = 2025"),
        "nb_ventes_2026": q("SELECT COUNT(*) FROM vente WHERE EXTRACT(YEAR FROM date_vente) = 2026"),
        "ca_2026": q("SELECT ROUND(SUM(montant_ttc)) FROM vente WHERE EXTRACT(YEAR FROM date_vente) = 2026"),
        "top_magasin_id": int(con.execute(
            "SELECT id_magasin FROM vente GROUP BY 1 ORDER BY SUM(montant_ttc) DESC LIMIT 1"
        ).fetchone()[0]),
        # ca_top_magasin rempli juste après (le top doit être connu avant d'être utilisé)
        "ca_categorie_top": int(q("""
            SELECT ROUND(SUM(v.montant_ttc)) FROM vente v
            JOIN produit p ON p.id_produit = v.id_produit
            JOIN categorie c ON c.id_categorie = p.id_categorie
            WHERE c.id_categorie = 7""")),
        "plus_gros_mois_ca": int(q("SELECT ROUND(MAX(ca_ttc)) FROM v_ca_mensuel_magasin")),
        "plus_gros_mois_magasin": q(
            "SELECT id_magasin FROM v_ca_mensuel_magasin ORDER BY ca_ttc DESC LIMIT 1"),
        "plus_gros_mois_annee": q(
            "SELECT annee FROM v_ca_mensuel_magasin ORDER BY ca_ttc DESC LIMIT 1"),
        "plus_gros_mois_mois": q(
            "SELECT mois FROM v_ca_mensuel_magasin ORDER BY ca_ttc DESC LIMIT 1"),
        "vue_lignes": int(q("SELECT COUNT(*) FROM v_ca_mensuel_magasin")),
    }
    a["ca_top_magasin"] = int(q(
        f"SELECT ROUND(SUM(montant_ttc)) FROM vente WHERE id_magasin = {a['top_magasin_id']}"))
    # manquants : colonne par colonne (la base M07 n'a AUCUN NULL — mesuré, pas affirmé)
    total = 0
    for (t,) in con.execute("SELECT table_name FROM information_schema.tables "
                            "WHERE table_schema='main' AND table_type='BASE TABLE'").fetchall():
        for row in con.execute(f"PRAGMA table_info('{t}')").fetchall():
            total += q(f"SELECT COUNT(*) FROM {t} WHERE {row[1]} IS NULL")
    a["manquants_total"] = total
    a["formes"] = {t: [q(f"SELECT COUNT(*) FROM {t}"), len(con.execute(f"PRAGMA table_info('{t}')").fetchall())]
                   for t in TABLES}
    con.close()
    return a


def brief(formes):
    n_vente = formes["vente"]["lignes"]
    txt = f"""# Brief M08 — « Le script qui fait le travail de trois matinées »

Vous avez reçu l'export CSV de la base commerciale de la chaîne de 5 magasins (la même base
que le module M07, que vous avez interrogée en SQL). Huit fichiers, un par table :

| Fichier | Lignes | Rôle |
|---|---|---|
| `vente.csv` | {n_venture(formes)} | les ventes (le jeu principal) |
| `client.csv` | {formes['client']['lignes']:,} | la clientèle |
| `produit.csv` | {formes['produit']['lignes']:,} | le catalogue |
| `categorie.csv` | {formes['categorie']['lignes']} | les rayons et sous-catégories |
| `magasin.csv` | {formes['magasin']['lignes']} | les 5 magasins |
| `mode_paiement.csv` | {formes['mode_paiement']['lignes']} | les 5 modes de paiement |
| `regle_tva.csv` | {formes['regle_tva']['lignes']} | le taux par année fiscale |
| `objectif_magasin.csv` | {formes['objectif_magasin']['lignes']} | **vide** — la direction n'a pas saisi les objectifs |

Deux consignes de lecture avant de toucher Python :

1. **Rien n'est « propre par avance ».** Ce fichier a été exporté par un stagiaire qui ne sait pas
   ce qu'il a dupliqué : l'audit (section 2 du projet) a de vrais défauts à trouver — des doublons,
   des retours comptés en positif, des dates impossibles, et une table vide.
2. **La vue mensuelle n'est pas exportée.** En SQL, `v_ca_mensuel_magasin` existe dans la base ;
   ici, elle est à **reconstruire** avec `pivot_table` (C08). Ce n'est pas une perte : c'est
   l'exercice.

Votre script devra finir par produire un classeur `synthese_commerciale.xlsx` dont les chiffres
sont **vérifiables** : vous connaissez déjà les réponses au SQL de M07.P. Zéro écart, c'est la
preuve que les deux chemins disent la même chose.
"""
    return txt


def n_venture(formes):
    return f"{formes['vente']['lignes']:,}"


def main():
    formes, empreinte = exporter()
    attendu = mesurer()
    src = json.load(open(SRC_ATTENDU, encoding="utf-8"))
    attendu["empreinte_dossier"] = empreinte
    attendu["empreinte_amont_m07"] = src.get("empreinte_sha256_bd_duckdb", "")[:16] + "…"
    json.dump(attendu, open(os.path.join(OUT, "ATTENDU.json"), "w"),
              indent=2, ensure_ascii=False)
    open(os.path.join(OUT, "00_brief.md"), "w", encoding="utf-8").write(brief(formes))
    for t in TABLES:
        print(f"  {t}.csv : {formes[t]['lignes']:,} l. × {formes[t]['colonnes']} col")
    print("empreinte dossier :", empreinte[:16] + "…")
    print("CA brut (côté SQL) :", attendu["ca_brut"], "· CA propre :", attendu["ca_sans_retours"],
          "· écart :", attendu["ecart_ca_retours"])
    print("doublons :", attendu["doublons"],
          "· retours brut/dedoublonnes :", attendu["retours_brut"], "/", attendu["retours_dedoublonnes"])
    print("dates vente>limite :", attendu["dates_vente_apres_limite"],
          "· deadlines au 20 brut/dedoublonnees :",
          attendu["deadlines_jour_20_brut"], "/", attendu["deadlines_jour_20"],
          "· manquants :", attendu["manquants_total"])


if __name__ == "__main__":
    main()
