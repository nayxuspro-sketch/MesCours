#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dossier_M11.py — construit le socle SQL du module M11 (SQL avance pour la BI).

Le module ne cree AUCUNE donnee nouvelle : il change les questions posees au socle
de M01-M03 (`ventes_propres.csv`) et a ses referentiels (`data/brut/`).

Sorties, dans `03_exercices/dossier_M11/` :

  socle_m11.sql      le DDL lisible — unique source de verite, 3 Ko
  connexion.py       l'ouverture du socle, depuis n'importe quel dossier de travail

**Pourquoi il n'y a pas de fichier `.duckdb` versionne.** Le format DuckDB a un
plancher d'environ 512 Ko par fichier : meme un socle de 265 651 lignes declarees
(petites tables + vues) pesait 1,5 Mo sur le disque, alors que l'atelier est a
127,9 Mo sur 128. Le socle est donc un **script** : `connexion.py` le rejoue en
memoire en 0,4 s. Rien a stocker, rien a versionner, et la base se reconstruit
partout de la meme facon.

Usage : python3 tools/dossier_M11.py
"""
from __future__ import annotations

import hashlib
import os
import sys
import time

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOSSIER = os.path.join(RACINE, "03_exercices", "dossier_M11")

# --------------------------------------------------------------------------- le DDL
SQL = """-- socle_m11.sql — socle du module M11 « SQL avancé pour la BI »
--
-- Écrit par `tools/dossier_M11.py`. Ne pas modifier à la main : régénérer.
--
-- MODE D'EMPLOI. Les chemins de ce fichier sont relatifs à la RACINE du dépôt.
-- Ouvrir le socle par `03_exercices/dossier_M11/connexion.py`, ou depuis la racine :
--
--     python3 -c "import sys; sys.path.insert(0,'03_exercices/dossier_M11'); \\
--                 from connexion import ouvrir; con = ouvrir()"
--
-- Le socle ne crée aucune donnée : il DÉCLARE ce qui existe déjà.
--   * tables : les référentiels courts, chargés une fois (produits, magasins, vendeurs,
--              objectifs, calendrier) ;
--   * vues   : les deux gros volumes (ventes, clients), lus dans leurs CSV d'origine
--              et donc jamais recopiés.

-- ------------------------------------------------------------------ référentiels
CREATE OR REPLACE TABLE produit AS
SELECT * FROM read_csv_auto('01_socle_donnees/data/brut/produits.csv', header = true);

CREATE OR REPLACE TABLE magasin AS
SELECT * FROM read_csv_auto('01_socle_donnees/data/brut/magasins.csv', header = true);

CREATE OR REPLACE TABLE vendeur AS
SELECT * FROM read_csv_auto('01_socle_donnees/data/brut/vendeurs.csv', header = true);

-- `objectifs_de_ca.csv` est séparé par des points-virgules, pas par des virgules :
-- sans `delim`, la table se charge en UNE colonne et le rapport est faux en silence.
CREATE OR REPLACE TABLE objectif_mois AS
SELECT * FROM read_csv_auto('01_socle_donnees/data/brut/objectifs_de_ca.csv',
                            header = true, delim = ';');

-- Le calendrier : une ligne par jour, y compris les jours sans vente.
CREATE OR REPLACE TABLE calendrier AS
SELECT * FROM read_csv_auto('01_socle_donnees/data/reference/dim_date.csv', header = true);

-- ------------------------------------------------------------------ volumes (vues)
CREATE OR REPLACE VIEW ventes AS
SELECT
    id_vente            AS id_vente,
    id_ticket           AS id_ticket,
    CAST(date_vente AS DATE) AS date_vente,
    CAST(heure AS TIME)      AS heure,
    id_magasin          AS id_magasin,
    id_vendeur          AS id_vendeur,
    id_client           AS id_client,
    id_produit          AS id_produit,
    quantite            AS quantite,
    prix_unitaire_ht    AS prix_unitaire_ht,
    taux_remise         AS taux_remise,
    montant_ht          AS montant_ht,
    montant_tva         AS montant_tva,
    montant_ttc         AS montant_ttc,
    mode_paiement       AS mode_paiement,
    canal               AS canal,
    CAST(est_retour AS BOOLEAN) AS est_retour,
    poids_kg            AS poids_kg
FROM read_csv_auto('01_socle_donnees/data/reference/ventes_propres.csv', header = true);

CREATE OR REPLACE VIEW clients AS
SELECT
    id_client           AS id_client,
    nom                 AS nom,
    type_client         AS type_client,
    ville               AS ville,
    region              AS region,
    CAST(date_creation AS DATE) AS date_creation,
    segment             AS segment,
    conditions_paiement AS conditions_paiement
FROM read_csv_auto('01_socle_donnees/data/brut/clients.csv', header = true);

-- ------------------------------------------------- copie de travail (performance)
-- Les deux vues relisent le CSV à chaque requête : 0,14 s pour un simple comptage.
-- `connexion.py(materialiser=True)` crée les copies en mémoire `ventes_m` et
-- `clients_m` (0,46 s) : la même requête tombe alors sous la milliseconde. C'est la
-- mesure d'ouverture du chapitre C06 — une vue n'est pas lente, elle est relue.
"""

CONNEXION = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""connexion.py — ouvre le socle M11 de n'importe quel dossier de travail.

    import sys; sys.path.insert(0, "03_exercices/dossier_M11")
    from connexion import ouvrir

    con = ouvrir()                    # le socle, prêt à interroger (0,4 s)
    con = ouvrir(materialiser=True)   # + copies en mémoire `ventes_m`, `clients_m`
                                      #   pour tout ce qui parle de performance

Le socle est un SCRIPT, pas un fichier de base : cette fonction le rejoue en mémoire.
Les vues pointent vers des CSV par des chemins **relatifs à la racine du dépôt** :
la fonction s'y place avant d'ouvrir, sinon DuckDB ne trouve pas les fichiers.
C'est le premier réflexe de tout rapport M11.
"""
from __future__ import annotations

import os

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FICHIER_SQL = os.path.join(RACINE, "03_exercices", "dossier_M11", "socle_m11.sql")


def ouvrir(materialiser: bool = False):
    """Rend une connexion DuckDB en mémoire, socle chargé."""
    import duckdb
    os.chdir(RACINE)
    sql = open(FICHIER_SQL, encoding="utf-8").read()
    con = duckdb.connect()
    con.execute(sql)
    if materialiser:
        con.execute("CREATE OR REPLACE TABLE ventes_m AS SELECT * FROM ventes")
        con.execute("CREATE OR REPLACE TABLE clients_m AS SELECT * FROM clients")
    return con
'''


def main() -> int:
    try:
        import duckdb
    except ImportError as e:  # pragma: no cover
        raise SystemExit("duckdb indisponible (%s) — installer duckdb avant de verifier le socle" % e)

    os.makedirs(DOSSIER, exist_ok=True)
    chemin_sql = os.path.join(DOSSIER, "socle_m11.sql")
    chemin_py = os.path.join(DOSSIER, "connexion.py")
    open(chemin_sql, "w", encoding="utf-8").write(SQL)
    open(chemin_py, "w", encoding="utf-8").write(CONNEXION)

    os.chdir(RACINE)
    t0 = time.time()
    con = duckdb.connect()
    con.execute(SQL)
    t_ddl = time.time() - t0

    print("=== dossier_M11 : socle reconstruit ===")
    total = 0
    for nom, genre in [("produit", "table"), ("magasin", "table"), ("vendeur", "table"),
                       ("objectif_mois", "table"), ("calendrier", "table"),
                       ("ventes", "vue"), ("clients", "vue")]:
        n = con.execute('SELECT COUNT(*) FROM "%s"' % nom).fetchone()[0]
        total += n
        print("  %-14s %-5s %9s lignes" % (nom, genre, f"{n:,}".replace(",", " ")))
    print("  total déclaré  : %s lignes" % f"{total:,}".replace(",", " "))

    # Controle d'integrite : tout identifiant de vente doit exister dans son referentiel.
    for cle, ref in [("id_produit", "produit"), ("id_magasin", "magasin"), ("id_vendeur", "vendeur")]:
        orphelins = con.execute(
            f'SELECT COUNT(DISTINCT v.{cle}) FROM ventes v '
            f'LEFT JOIN "{ref}" r ON r.{cle} = v.{cle} WHERE r.{cle} IS NULL').fetchone()[0]
        print("  orphelins %-11s : %d" % (cle, orphelins))
    non_ref = con.execute(
        "SELECT COUNT(DISTINCT v.id_client) FROM ventes v "
        "LEFT JOIN clients c ON c.id_client = v.id_client WHERE c.id_client IS NULL").fetchone()[0]
    print("  clients de vente absents du référentiel : %d" % non_ref)

    # Les deux mesures de performance qui ouvrent le chapitre C06.
    t1 = time.time()
    vue = con.execute("SELECT COUNT(*) FROM ventes WHERE est_retour").fetchone()[0]
    t_vue = time.time() - t1
    t2 = time.time()
    con.execute("CREATE OR REPLACE TABLE ventes_m AS SELECT * FROM ventes")
    t_mat = time.time() - t2
    t3 = time.time()
    table_ = con.execute("SELECT COUNT(*) FROM ventes_m WHERE est_retour").fetchone()[0]
    t_table = time.time() - t3
    assert vue == table_
    print("  vue relue     : %.3f s   |  copie en mémoire : %.2f s  |  table : %.3f s"
          % (t_vue, t_mat, t_table))
    con.close()

    h = hashlib.sha256(open(chemin_sql, "rb").read()).hexdigest()[:16]
    print("  DDL rejoué en %.2f s   |  socle_m11.sql : %s (%d octets)"
          % (t_ddl, h, os.path.getsize(chemin_sql)))
    print("  aucun fichier .duckdb : le socle est un script, il ne pèse rien en dépôt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
