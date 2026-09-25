#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dossier_M13.py — construit le socle du module M13 (Modelisation des donnees).

M11 a donne la matiere, M12 a donne les indicateurs et leur carte ; M13 batit la
STRUCTURE qui fait tenir les deux : un modele relationnel, en etoile, executable et
verifiable.

Le module n'invente presque rien : les dimensions et les faits sortent des sources
existantes (ventes de M01—M03, referentiels, cinq tables operationnelles de M12).
Il ajoute seulement ce qu'un modele ne peut pas demontrer sans : de l'HISTOIRE.

  mouvements_clients.csv   1 120 lignes — changements de segment, de ville ou de
                                           conditions de paiement, dates d'effet
  tarifs_produits.csv        616 lignes — 154 produits x 4 revisions de prix
  (dimensions historisees : construites par socle_m13.sql, pas exportees en CSV —
   24 892 versions client + la ligne « client non identifie », 616 versions produit)
  table_plate.csv             18 lignes — l'extrait denormalise du chapitre C02
  socle_m13.sql                        — les 12 tables du modele (5 dimensions + 7 faits)
  modele_fautif.sql                    — les modeles qui donnent un CA faux
  connexion.py                         — rejoue M11, M12 puis M13
  ATTENDU.json                         — les mesures de reference du modele
  revue_modele.md                      — le modele annote : 5 defauts a trouver (C07)

Usage : python3 tools/dossier_M13.py
"""
from __future__ import annotations

import csv
import datetime
import json
import os
import random

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOSSIER = os.path.join(RACINE, "03_exercices", "dossier_M13")
CLIENTS = os.path.join(RACINE, "01_socle_donnees", "data", "brut", "clients.csv")
PRODUITS = os.path.join(RACINE, "01_socle_donnees", "data", "brut", "produits.csv")

GRAINE = 47          # M13 : la graine du module
DEBUT = datetime.date(2023, 1, 1)
FIN = datetime.date(2026, 8, 31)

# Les familles reelles du referentiel : 16 libelles ecrits de toutes les facons pour
# 7 familles. Le modele ne corrige pas la donnee (C02 montre que la correction
# appartient au referentiel) : il la declare dans une table de correspondance.
FAMILLES = {
    "Plomberie": "Plomberie", "PEINTURE": "Peinture", "Peinture": "Peinture",
    "Peintures": "Peinture", "peinture": "Peinture", "Bois & panneaux": "Bois et panneaux",
    "Electricité": "Electricite", "MATÉRIAUX": "Materiaux", "Materiaux": "Materiaux",
    "Matériaux": "Materiaux", "materiaux": "Materiaux", "QUINCAILLERIE": "Quincaillerie",
    "Quincaillerie": "Quincaillerie", "quincaillerie": "Quincaillerie",
    "Consommables": "Consommables",
}
SEGMENTS = ["Standard", "Argent", "Or"]


def lire(chemin):
    with open(chemin, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def date_de(jour):
    return (DEBUT + datetime.timedelta(days=int(jour))).isoformat()


def ecrire_csv(nom, entete, lignes):
    """Ecrit un CSV RECEVABLE : un champ qui contient une virgule est protege par des guillemets.

    `table_plate.csv` portait « Cable electrique 2,5 mm » sans protection : la ligne comptait
    13 champs au lieu de 12 et le fichier ne se lisait plus. Aucun total ne s'en apercevait —
    c'est le genre de defaut qu'un chapitre de modelisation doit montrer, puis corriger.
    """
    with open(os.path.join(DOSSIER, nom), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(entete.split(","))
        for l in lignes:
            w.writerow(["" if v is None else v for v in l])


def ecrire(nom, lignes):
    with open(os.path.join(DOSSIER, nom), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lignes) + "\n")


# ---------------------------------------------------------------- 1. les clients
def lire_clients():
    """id_client -> (segment, ville, conditions, date_creation)."""
    out = {}
    for c in lire(CLIENTS):
        try:
            ident = int(c["id_client"])
        except (KeyError, ValueError):
            continue
        out[ident] = {
            "segment": (c.get("segment") or "Standard").strip(),
            "ville": (c.get("ville") or "").strip(),
            "type_client": (c.get("type_client") or "").strip(),
            "conditions": (c.get("conditions_paiement") or "").strip(),
            "date_creation": (c.get("date_creation") or "").strip(),
        }
    return out


def mouvements(clients):
    """1 120 mouvements, exactement : 980 changements a historiser (type 2) et 140 corrections.

    Un changement de SEGMENT ou de VILLE s'historise : la question « quel etait le
    segment de ce client au moment de la vente ? » a une reponse differente selon la
    date. Une CORRECTION de saisie ne s'historise pas : la bonne valeur a toujours ete
    la bonne, on remplace (type 1).
    """
    rnd = random.Random(GRAINE)
    ids = sorted(clients)
    rnd.shuffle(ids)
    lignes, faits = [], set()
    cibles_scd2, cibles_scd1 = 980, 140
    i = 0
    while sum(1 for l in lignes if l[5] == 2) < cibles_scd2:
        ident = ids[i % 900]
        i += 1
        c = clients[ident]
        nature = rnd.choice(["segment", "segment", "ville"])
        avant = c[nature]
        if nature == "segment":
            if avant == "Standard" and rnd.random() < 0.72:
                apres = "Argent"
            elif avant == "Argent" and rnd.random() < 0.55:
                apres = "Or"
            else:
                apres = rnd.choice([x for x in SEGMENTS if x != avant])
        else:
            apres = rnd.choice([v for v in ("Ouagadougou", "Bobo-Dioulasso", "Koudougou",
                                            "Kaya", "Ouahigouya") if v != avant])
        if apres == avant:
            continue
        c[nature] = apres
        lignes.append((ident, date_de(rnd.randint(60, 1240)), nature, avant, apres, 2))
    while sum(1 for l in lignes if l[5] == 1) < cibles_scd1:
        ident = ids[900 + (i % 140)]
        i += 1
        nature = "ville" if rnd.random() < 0.6 else "conditions"
        if (ident, nature) in faits:
            continue
        propre = clients[ident][nature]
        # une correction de saisie : la valeur du referentiel est la BONNE, et le
        # mouvement documente l'erreur corrigee. Rien a historiser (type 1).
        avant = propre.lower() if nature == "ville" else propre + " "
        apres = propre
        if apres == avant:
            continue
        faits.add((ident, nature))
        lignes.append((ident, date_de(rnd.randint(30, 1300)), nature, avant, apres, 1))
    lignes.sort(key=lambda x: (x[1], x[0]))
    return lignes, cibles_scd2, cibles_scd1


# Les deux dimensions historisees ne sont PAS ecrites en CSV : elles se construisent
# en SQL (voir socle_m13.sql), a partir de l'histoire brute. C'est la demonstration
# centrale du module : un changement lent de dimension (type 2) est une REQUETE.


# --------------------------------------------------------------- 2. les tarifs
def tarifs(produits):
    """616 lignes : 154 produits x 4 revisions, la premiere etant le prix initial.

    La derive globale du tarif est la contrepartie du +25,0 % de prix constate en M12
    sur les ventes ; elle est mesuree et publiee, jamais choisie pour tomber juste.
    """
    rnd = random.Random(GRAINE + 1)
    prix_par_ssc = {}
    for p in produits:
        if p.get("prix_vente_ht"):
            prix_par_ssc.setdefault(p["sous_categorie"], []).append(float(p["prix_vente_ht"]))
    median = {k: sorted(v)[len(v) // 2] for k, v in prix_par_ssc.items()}
    dates = ["2023-01-01", "2024-01-01", "2025-01-01", "2026-01-01"]
    # facteurs CUMULES : la revision de 2025 s'applique au prix de 2024, pas au prix
    # d'origine. Une lecture additive produit une derive de 8,8 % la ou le socle en
    # mesure pres de 24 % — le genre d'ecart qui se voit dans un total.
    cumul = [1.0]
    for r in (0.064, 0.071, 0.086):
        cumul.append(cumul[-1] * (1 + r))
    lignes = []
    for p in sorted(produits, key=lambda x: int(x["id_produit"])):
        base = float(p["prix_vente_ht"]) if p.get("prix_vente_ht") else median.get(p["sous_categorie"], 1000.0)
        for i, d in enumerate(dates):
            bruit = 1 + rnd.uniform(-0.02, 0.02)
            prix = round(base * cumul[i] * bruit, 0)
            lignes.append((int(p["id_produit"]), d, int(prix)))
    return lignes


# ------------------------------------------------- 3. la table plate des anomalies
def table_plate():
    """18 lignes, 4 defauts : c'est la table de depart du chapitre C02.

    Elle contient exactement ce qu'on trouve dans un fichier de travail reel :
      * un client dont l'adresse change en cours d'historique (4 lignes, 2 adresses) ;
      * une famille ecrite de trois facons (PEINTURE / Peinture / peinture) ;
      * un produit qui n'apparait qu'une fois (l'insertion force a recopier le client) ;
      * un produit supprime dont il ne reste que des traces (perte d'information).
    """
    lignes = [
        # ticket, date, client, nom, ville, segment, produit, designation, categorie, qte, pu
        ("T-1001", "2023-02-14", 41, "SARL Faso Batiment", "Ouagadougou", "Argent",
         12, "Ciment CPJ45 50 kg", "Materiaux", 40, 4_800),
        ("T-1002", "2023-03-02", 41, "SARL Faso Batiment", "Ouagadougou", "Argent",
         12, "Ciment CPJ45 50 kg", "Materiaux", 25, 4_800),
        ("T-1003", "2023-06-19", 41, "SARL Faso Batiment", "Bobo-Dioulasso", "Argent",
         7, "Peinture acrylique 20 l", "PEINTURE", 6, 21_500),
        ("T-1004", "2024-01-08", 41, "SARL Faso Batiment", "Bobo-Dioulasso", "Or",
         7, "Peinture acrylique 20 l", "Peinture", 4, 23_900),
        ("T-1005", "2024-02-11", 58, "Quincaillerie du Sahel", "Koudougou", "Standard",
         7, "Peinture acrylique 20 l", "peinture", 3, 23_900),
        ("T-1006", "2024-02-11", 58, "Quincaillerie du Sahel", "Koudougou", "Standard",
         19, "Tole bac alu 6 m", "Materiaux", 12, 9_400),
        ("T-1007", "2024-05-30", 58, "Quincaillerie du Sahel", "Koudougou", "Standard",
         19, "Tole bac alu 6 m", "MATÉRIAUX", 8, 9_600),
        ("T-1008", "2024-09-04", 63, "Entreprise Zongo", "Kaya", "Argent",
         31, "Cable electrique 2,5 mm", "Electricité", 120, 1_150),
        ("T-1009", "2025-01-15", 63, "Entreprise Zongo", "Kaya", "Argent",
         31, "Cable electrique 2,5 mm", "Electricité", 80, 1_210),
        ("T-1010", "2025-01-15", 63, "Entreprise Zongo", "Kaya", "Or",
         44, "Tube PVC 100 mm", "Plomberie", 30, 5_400),
        ("T-1011", "2025-04-22", 71, "GIE Wende", "Ouagadougou", "Standard",
         44, "Tube PVC 100 mm", "Plomberie", 45, 5_400),
        ("T-1012", "2025-04-22", 71, "GIE Wende", "Ouagadougou", "Standard",
         52, "Disjoncteur 32 A", "quincaillerie", 24, 3_250),
        ("T-1013", "2025-08-07", 71, "GIE Wende", "Ouagadougou", "Argent",
         52, "Disjoncteur 32 A", "QUINCAILLERIE", 18, 3_250),
        ("T-1014", "2025-11-12", 77, "COOPAC Nord", "Ouahigouya", "Standard",
         60, "Brouette renforcee", "Quincaillerie", 5, 27_000),
        ("T-1015", "2026-01-20", 77, "COOPAC Nord", "Ouahigouya", "Standard",
         66, "Machette agricole", "quincaillerie", 60, 2_100),
        ("T-1016", "2026-02-03", 77, "COOPAC Nord", "Ouahigouya", "Standard",
         66, "Machette agricole", "Quincaillerie", 40, 2_100),
        ("T-1017", "2026-03-11", 84, "SARL Nabonswendé", "Ouagadougou", "Argent",
         73, "Vernis bois 5 l", "Peintures", 10, 14_500),
        ("T-1018", "2026-04-02", 84, "SARL Nabonswendé", "Ouagadougou", "Argent",
         73, "Vernis bois 5 l", "Peinture", 6, 14_500),
    ]
    return lignes


# ------------------------------------------------------------------ 4. le socle SQL
SQL = """-- socle_m13.sql — le modele de Sahel Distribution (module M13)
--
-- Ecrit par `tools/dossier_M13.py`. Ne pas modifier a la main : regenerer.
--
-- `connexion.py` rejoue trois fichiers, dans l'ordre :
--   1. dossier_M11/socle_m11.sql  — les ventes et les referentiels du fil rouge
--   2. dossier_M12/socle_m12.sql  — les cinq sources operationnelles
--   3. dossier_M13/socle_m13.sql  — CE FICHIER : le modele en etoile
--
-- Le modele compte DOUZE tables : CINQ dimensions et SEPT tables de faits.
--
--   Dimensions                      Faits
--   dim_client                      fait_ventes          (ligne de ticket)
--   dim_produit                     fait_commandes       (commande)
--   dim_magasin                     fait_encaissements   (facture)
--   dim_vendeur                     fait_stock_mensuel   (produit x mois)
--   dim_date                        fait_ruptures        (produit x magasin x mois)
--   (+ les versions historisees)    fait_logistique      (magasin x mois)
--                                   fait_objectifs       (magasin x mois)
--
-- Deux dimensions historisees (type 2) completent le modele, parce que la question
-- « quelle etait la valeur de cet attribut AU MOMENT du fait ? » n'a pas la meme
-- reponse que « quelle est sa valeur aujourd'hui » :
--   dim_client_scd   24 892 versions + la ligne « client non identifie »
--   dim_produit_scd     616 versions
--
-- Le grain de chaque table est ecrit AU-DESSUS d'elle : un modele dont les grains ne
-- sont pas ecrits est un modele qu'on ne peut pas auditer.

-- ================================================================ DIMENSIONS

-- ------------------------------------------------------------- dim_client
-- Grain : une ligne par client, etat COURANT de l'attribut.
CREATE OR REPLACE TABLE dim_client AS
SELECT CAST(id_client AS INTEGER)              AS id_client,
       nom,
       type_client,
       ville,
       region,
       TRY_CAST(date_creation AS DATE)         AS date_creation,
       segment,
       conditions_paiement
FROM clients;

-- Le client 0 du fichier de ventes n'existe pas dans le referentiel : le modele lui
-- donne une ligne explicite plutot que de laisser une cle etrangere orpheline. Une
-- dimension doit contenir la ligne « inconnu » — c'est une decision, pas un oubli.
INSERT INTO dim_client VALUES
    (0, 'CLIENT NON IDENTIFIE', 'Inconnu', 'Inconnu', 'Inconnu', NULL, 'Inconnu', 'Inconnu');

-- ------------------------------------------------------------ dim_produit
-- Grain : une ligne par produit. La famille est AJOUTEE : le referentiel porte 16
-- libelles pour 7 familles reelles, et c'est le modele qui porte la correspondance.
CREATE OR REPLACE TABLE dim_produit AS
SELECT CAST(id_produit AS INTEGER)             AS id_produit,
       designation,
       categorie                                AS libelle_source,
       CASE categorie
            WHEN 'PEINTURE' THEN 'Peinture'   WHEN 'Peinture' THEN 'Peinture'
            WHEN 'Peintures' THEN 'Peinture'  WHEN 'peinture' THEN 'Peinture'
            WHEN 'MATÉRIAUX' THEN 'Materiaux' WHEN 'Materiaux' THEN 'Materiaux'
            WHEN 'Matériaux' THEN 'Materiaux' WHEN 'materiaux' THEN 'Materiaux'
            WHEN 'QUINCAILLERIE' THEN 'Quincaillerie'
            WHEN 'Quincaillerie' THEN 'Quincaillerie'
            WHEN 'quincaillerie' THEN 'Quincaillerie'
            WHEN 'Electricité' THEN 'Electricite'
            ELSE categorie END                    AS famille,
       sous_categorie,
       unite,
       CAST(prix_vente_ht AS DOUBLE)           AS prix_vente_ht,
       CAST(poids_unite_kg AS DOUBLE)          AS poids_unite_kg,
       fournisseur,
       CAST(tva AS DOUBLE)                     AS tva,
       CAST(actif AS INTEGER)                  AS actif
FROM produit;

-- ------------------------------------------------------------ dim_magasin
-- Grain : une ligne par magasin. Le depot est present : il ne vend pas, mais il
-- recoit des colis — un fait sans vente n'est pas une dimension a supprimer.
CREATE OR REPLACE TABLE dim_magasin AS
SELECT CAST(id_magasin AS INTEGER) AS id_magasin, nom, ville, quartier, region,
       type_magasin, CAST(surface_m2 AS INTEGER) AS surface_m2, responsable,
       TRY_CAST(ouverture AS DATE) AS ouverture,
       CASE WHEN id_magasin IN (SELECT DISTINCT id_magasin FROM ventes)
            THEN 1 ELSE 0 END AS vend
FROM magasin;

-- ------------------------------------------------------------ dim_vendeur
-- Grain : une ligne par vendeur, rattache au magasin (hierarchie magasin -> vendeur).
CREATE OR REPLACE TABLE dim_vendeur AS
SELECT CAST(id_vendeur AS INTEGER) AS id_vendeur, nom_complet,
       CAST(id_magasin AS INTEGER) AS id_magasin,
       TRY_CAST(date_embauche AS DATE) AS date_embauche, statut, secteur_vente
FROM vendeur;

-- --------------------------------------------------------------- dim_date
-- Grain : une ligne par jour. C'est la SEULE table de dates du modele : aucune table
-- de faits ne porte d'attribut de calendrier, elles portent toutes une cle de date.
-- Trois attributs sont ajoutes au calendrier du fil rouge : la semaine commerciale
-- (samedi a vendredi), l'annee fiscale (1er juillet) et le libelle du jour ferie.
CREATE OR REPLACE TABLE dim_date AS
SELECT TRY_CAST(date AS DATE)                        AS date,
       CAST(annee AS INTEGER)                        AS annee,
       CAST(trimestre AS INTEGER)                    AS trimestre,
       CAST(mois AS INTEGER)                         AS mois,
       libelle_mois,
       CAST(semaine_iso AS INTEGER)                  AS semaine_iso,
       CAST(jour_semaine AS INTEGER)                 AS jour_semaine,
       libelle_jour,
       CAST(est_dimanche AS INTEGER)                 AS est_dimanche,
       CAST(est_ferie AS INTEGER)                    AS est_ferie,
       COALESCE(evenement, '')                       AS libelle_ferie,
       annee_mois,
       -- semaine commerciale : la semaine du samedi au vendredi, numerotee dans l'annee
       CAST(floor((dayofyear(date) + 5 - dayofweek(date) + 7) / 7) AS INTEGER)
                                                     AS semaine_commerciale,
       -- annee fiscale : elle commence le 1er juillet (choix du modele, declare)
       CASE WHEN CAST(mois AS INTEGER) >= 7
            THEN CAST(annee AS INTEGER) ELSE CAST(annee AS INTEGER) - 1 END
                                                     AS annee_fiscale,
       CASE WHEN CAST(mois AS INTEGER) >= 7 THEN 1 ELSE 2 END AS periode_fiscale
FROM calendrier;

-- ------------------------------------------------ dim_client_scd (type 2)
-- Grain : une version de client, valide du 1er jour au dernier jour (fin ouverte).
--
-- Un changement lent de dimension de type 2 est une REQUETE, pas un fichier recu.
-- La question a laquelle elle repond : « quelle etait la valeur de cet attribut AU
-- MOMENT du fait ? ». Trois etapes :
--   1. les bornes de version : la date d'entree en vigueur de chaque changement a
--      historiser (type 2), plus l'ouverture du compte client. Cette ouverture est la
--      PLUS ANCIENNE de deux dates : la date de creation ecrite au referentiel et la
--      premiere vente connue. 6 685 clients ont une premiere vente anterieure a leur
--      date de creation — le referentiel porte une date de SAISIE, le fait porte une
--      date de VENTE. Sans ce rattrapage, la jointure « au moment du fait » perdrait
--      28 784 lignes de ticket, sans erreur et sans avertissement ;
--   2. la valeur d'un attribut a une date : la derniere valeur posee a cette date,
--      sinon la valeur d'AVANT le premier changement, sinon celle du referentiel ;
--   3. la periode de validite : jusqu'a la veille du changement suivant, fin ouverte
--      pour la version courante.
-- Les corrections de saisie (type 1) ne creent AUCUNE version : la bonne valeur a
-- toujours ete la bonne.
CREATE OR REPLACE TABLE dim_client_scd AS
WITH prem AS (
    SELECT CAST(id_client AS INTEGER) AS id_client,
           MIN(TRY_CAST(date_vente AS DATE)) AS premiere_vente
    FROM ventes GROUP BY 1),
base AS (
    SELECT CAST(c.id_client AS INTEGER) AS id_client, c.ville, c.segment,
           c.conditions_paiement, c.type_client,
           COALESCE(TRY_CAST(c.date_creation AS DATE), DATE '2023-01-01') AS date_creation,
           p.premiere_vente
    FROM clients c
    LEFT JOIN prem p ON p.id_client = CAST(c.id_client AS INTEGER)),
mvt AS (
    SELECT CAST(id_client AS INTEGER) AS id_client, TRY_CAST(date_effet AS DATE) AS date_effet,
           nature, valeur_avant, valeur_apres, CAST(type_scd AS INTEGER) AS type_scd
    FROM read_csv_auto('03_exercices/dossier_M13/mouvements_clients.csv', header = true)),
bornes AS (
    SELECT id_client, date_effet AS debut FROM mvt WHERE type_scd = 2
    UNION
    SELECT id_client, LEAST(date_creation, COALESCE(premiere_vente, date_creation)) AS debut
    FROM base),
versions AS (
    SELECT id_client, debut,
           row_number() OVER (PARTITION BY id_client ORDER BY debut) AS version,
           lead(debut) OVER (PARTITION BY id_client ORDER BY debut) AS fin
    FROM bornes)
SELECT v.id_client, CAST(v.version AS INTEGER) AS version, v.debut AS date_debut,
       (v.fin - INTERVAL 1 DAY)::DATE                                          AS date_fin,
       COALESCE((SELECT m.valeur_apres FROM mvt m WHERE m.id_client = v.id_client
                   AND m.nature = 'segment' AND m.type_scd = 2 AND m.date_effet <= v.debut
                 ORDER BY m.date_effet DESC LIMIT 1),
                (SELECT m.valeur_avant FROM mvt m WHERE m.id_client = v.id_client
                   AND m.nature = 'segment' AND m.type_scd = 2
                 ORDER BY m.date_effet LIMIT 1),
                (SELECT b.segment FROM base b WHERE b.id_client = v.id_client))       AS segment,
       COALESCE((SELECT m.valeur_apres FROM mvt m WHERE m.id_client = v.id_client
                   AND m.nature = 'ville' AND m.type_scd = 2 AND m.date_effet <= v.debut
                 ORDER BY m.date_effet DESC LIMIT 1),
                (SELECT m.valeur_avant FROM mvt m WHERE m.id_client = v.id_client
                   AND m.nature = 'ville' AND m.type_scd = 2
                 ORDER BY m.date_effet LIMIT 1),
                (SELECT b.ville FROM base b WHERE b.id_client = v.id_client))         AS ville,
       COALESCE((SELECT m.valeur_apres FROM mvt m WHERE m.id_client = v.id_client
                   AND m.nature = 'conditions' AND m.type_scd = 2 AND m.date_effet <= v.debut
                 ORDER BY m.date_effet DESC LIMIT 1),
                (SELECT b.conditions_paiement FROM base b WHERE b.id_client = v.id_client))
                                                                                     AS conditions_paiement,
       (SELECT b.type_client FROM base b WHERE b.id_client = v.id_client)            AS type_client,
       CASE WHEN v.fin IS NULL THEN 1 ELSE 0 END                                 AS est_courante,
       CAST(v.id_client AS VARCHAR) || '-' || CAST(v.version AS VARCHAR)         AS cle_version
FROM versions v;

-- La decision prise pour dim_client vaut aussi pour sa version historisee : sans une
-- ligne « client non identifie », la jointure « au moment du fait » perdrait les
-- 43 161 lignes de ticket du client 0. Une dimension qui gagne une ligne inconnue
-- doit la gagner dans TOUTES ses formes — sinon le fait disparait d'un total.
INSERT INTO dim_client_scd VALUES
    (0, 1, DATE '1900-01-01', NULL, 'Inconnu', 'Inconnu', 'Inconnu', 'Inconnu', 1, '0-1');

-- ----------------------------------------------- dim_produit_scd (type 2)
-- Grain : une version de produit, prix valable sur la periode : 616 versions pour
-- 154 produits et 4 revisions. La dimension produit courante porte le prix ACTUEL ;
-- seule la dimension historisee permet de calculer une marge « au prix de l'epoque ».
CREATE OR REPLACE TABLE dim_produit_scd AS
WITH grille AS (
    SELECT CAST(id_produit AS INTEGER) AS id_produit, TRY_CAST(date_effet AS DATE) AS date_debut,
           CAST(prix_vente_ht AS DOUBLE) AS prix_vente_ht
    FROM read_csv_auto('03_exercices/dossier_M13/tarifs_produits.csv', header = true)),
v AS (
    SELECT id_produit, date_debut, prix_vente_ht,
           row_number() OVER (PARTITION BY id_produit ORDER BY date_debut)      AS version,
           lead(date_debut) OVER (PARTITION BY id_produit ORDER BY date_debut)  AS date_debut_suivante
    FROM grille)
SELECT v.id_produit, CAST(v.version AS INTEGER) AS version, v.date_debut,
       (v.date_debut_suivante - INTERVAL 1 DAY)::DATE   AS date_fin,
       v.prix_vente_ht, p.sous_categorie, p.famille,
       CASE WHEN v.date_debut_suivante IS NULL THEN 1 ELSE 0 END AS est_courante,
       CAST(v.id_produit AS VARCHAR) || '-' || CAST(v.version AS VARCHAR) AS cle_version
FROM v JOIN dim_produit p ON p.id_produit = v.id_produit;

-- ===================================================================== FAITS

-- ------------------------------------------------------------ fait_ventes
-- Grain : UNE LIGNE DE TICKET (240 000 lignes). C'est le grain le plus fin du
-- modele ; tout ce qui est plus agrege se calcule a partir de lui.
CREATE OR REPLACE TABLE fait_ventes AS
SELECT CAST(id_vente AS INTEGER)      AS id_vente,
       id_ticket,                      -- 'T01-230101-000000' : une cle METIER, pas un nombre
       TRY_CAST(date_vente AS DATE)   AS date_vente,
       CAST(id_magasin AS INTEGER)    AS id_magasin,
       CAST(id_vendeur AS INTEGER)    AS id_vendeur,
       CAST(id_client AS INTEGER)     AS id_client,
       CAST(id_produit AS INTEGER)    AS id_produit,
       CAST(quantite AS DOUBLE)       AS quantite,
       CAST(prix_unitaire_ht AS DOUBLE) AS prix_unitaire_ht,
       CAST(taux_remise AS DOUBLE)    AS taux_remise,
       CAST(montant_ht AS DOUBLE)     AS montant_ht,
       CAST(montant_ttc AS DOUBLE)    AS montant_ttc,
       CAST(montant_tva AS DOUBLE)    AS montant_tva,
       mode_paiement, canal,
       CAST(est_retour AS INTEGER)    AS est_retour,
       CAST(poids_kg AS DOUBLE)       AS poids_kg
FROM ventes;

-- ---------------------------------------------------------- fait_commandes
-- Grain : UNE COMMANDE (9 000).
CREATE OR REPLACE TABLE fait_commandes AS
SELECT id_commande, id_client, id_magasin,
       TRY_CAST(date_commande AS DATE)   AS date_commande,
       TRY_CAST(date_promisee AS DATE)   AS date_promisee,
       TRY_CAST(date_livraison AS DATE)  AS date_livraison,
       CAST(montant_ttc AS DOUBLE)       AS montant_ttc, statut
FROM commande;

-- ------------------------------------------------------ fait_encaissements
-- Grain : UNE FACTURE (9 000).
CREATE OR REPLACE TABLE fait_encaissements AS
SELECT id_facture, id_client,
       TRY_CAST(date_facture AS DATE)      AS date_facture,
       TRY_CAST(date_echeance AS DATE)     AS date_echeance,
       TRY_CAST(date_encaissement AS DATE) AS date_encaissement,
       CAST(montant_ttc AS DOUBLE)         AS montant_ttc,
       CAST(montant_encaisse AS DOUBLE)    AS montant_encaisse, conditions_paiement
FROM encaissement;

-- ------------------------------------------------------ fait_stock_mensuel
-- Grain : PRODUIT x MOIS (6 776) — un instantane periodique, donc SEMI-ADDITIF :
-- on additionne dans l'espace, jamais dans le temps.
CREATE OR REPLACE TABLE fait_stock_mensuel AS
SELECT id_produit, mois, CAST(entrees_unites AS DOUBLE) AS entrees_unites,
       CAST(stock_moyen_unites AS DOUBLE) AS stock_moyen_unites,
       CAST(couverture_mois AS DOUBLE)    AS couverture_mois
FROM stock_mensuel;

-- ---------------------------------------------------------- fait_ruptures
-- Grain : PRODUIT x MAGASIN x MOIS (2 428).
CREATE OR REPLACE TABLE fait_ruptures AS
SELECT id_produit, id_magasin, mois, CAST(jours_rupture AS INTEGER) AS jours_rupture,
       CAST(unites_perdues_estimees AS DOUBLE) AS unites_perdues,
       CAST(ca_perdu_estime_fcfa AS DOUBLE)    AS ca_perdu
FROM rupture;

-- --------------------------------------------------------- fait_logistique
-- Grain : MAGASIN x MOIS (264).
CREATE OR REPLACE TABLE fait_logistique AS
SELECT id_magasin, mois, CAST(colis AS INTEGER) AS colis,
       CAST(poids_kg AS DOUBLE) AS poids_kg,
       CAST(cout_carburant_fcfa AS DOUBLE) AS cout_carburant,
       CAST(cout_main_oeuvre_fcfa AS DOUBLE) AS cout_main_oeuvre,
       CAST(cout_vehicule_fcfa AS DOUBLE) AS cout_vehicule,
       CAST(cout_total_fcfa AS DOUBLE) AS cout_total
FROM logistique;

-- --------------------------------------------------------- fait_objectifs
-- Grain : MAGASIN x MOIS (218) — un FAIT, pas un referentiel : il porte un montant
-- et une date, et il se joint aux ventes par la cle (magasin, mois).
CREATE OR REPLACE TABLE fait_objectifs AS
SELECT id_magasin, annee, mois, annee_mois,
       CAST(ca_objectif_ttc AS DOUBLE) AS ca_objectif_ttc,
       CAST(marge_objectif_pct AS DOUBLE) AS marge_objectif_pct
FROM objectif_mois;

-- ------------------------------------------------------------ les vues de recette
-- La recette du modele : les totaux doivent etre IDENTIQUES a ceux des sources.
CREATE OR REPLACE VIEW recette_ca AS
SELECT (SELECT ROUND(SUM(montant_ttc)) FROM fait_ventes WHERE est_retour = 0) AS ca_modele,
       (SELECT ROUND(SUM(montant_ttc)) FROM ventes WHERE est_retour = 0)       AS ca_source;
"""

FAUTIF = """-- modele_fautif.sql — les modeles qui donnent un chiffre d'affaires faux
--
-- Ecrit par `tools/dossier_M13.py`. Ne pas modifier a la main : regenerer.
--
-- Ces trois vues sont les trois erreurs de modelisation les plus courantes du
-- chapitre C03 et de l'etude de cas :
--   * `ca_deux_tableaux`  : on additionne deux tables qui portent TOUTES LES DEUX
--                           un montant, sans verifier qu'elles parlent du meme fait ;
--   * `ca_trois_tableaux` : on y ajoute les encaissements — trois fois le meme
--                           argent, compte trois fois ;
--   * `ca_jointure_folle` : on joint les ventes a la logistique sur le magasin
--                           seul, et chaque ligne de vente est repetee 44 fois.

CREATE OR REPLACE VIEW ca_deux_tableaux AS
SELECT (SELECT SUM(montant_ttc) FROM ventes WHERE NOT est_retour)
     + (SELECT SUM(montant_ttc) FROM commande) AS ca;

CREATE OR REPLACE VIEW ca_trois_tableaux AS
SELECT (SELECT SUM(montant_ttc) FROM ventes WHERE NOT est_retour)
     + (SELECT SUM(montant_ttc) FROM commande)
     + (SELECT SUM(montant_encaisse) FROM encaissement) AS ca;

CREATE OR REPLACE VIEW ca_jointure_folle AS
SELECT SUM(v.montant_ttc) AS ca
FROM ventes v JOIN logistique l ON l.id_magasin = v.id_magasin
WHERE NOT v.est_retour;
"""

CONNEXION = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""connexion.py — ouvrir le socle du module M13 (modelisation des donnees).

    import sys; sys.path.insert(0, '03_exercices/dossier_M13')
    from connexion import ouvrir
    con = ouvrir()

Le socle est un SCRIPT, pas un fichier de base : il rejoue trois fichiers SQL, dans
l'ordre — M11 (ventes et referentiels), M12 (les cinq sources operationnelles),
M13 (le modele en etoile). Aucun fichier `.duckdb` n'est versionne : le format a un
plancher d'environ 512 Ko, et l'atelier vit sous quota.

Le modele M13 ajoute DOUZE tables (5 dimensions + 7 faits) et DEUX dimensions
historisees (type 2) ; les modeles fautifs sont dans `modele_fautif.sql`.

Parametres :
    materialiser=False  (defaut) : les ventes restent des VUES ; le socle s'ouvre en
                        quelques dixiemes de seconde et ne pese rien en memoire.
    materialiser=True   : les ventes et les faits sont copies en table ; c'est le mode
                        des mesures de volume et de plan.
"""
from __future__ import annotations

import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def ouvrir(materialiser=False, fautif=False):
    import duckdb
    con = duckdb.connect()
    con.execute("SET enable_progress_bar = false;")
    for nom in ("dossier_M11/socle_m11.sql", "dossier_M12/socle_m12.sql",
                "dossier_M13/socle_m13.sql"):
        chemin = os.path.join(RACINE, "03_exercices", nom)
        with open(chemin, encoding="utf-8") as f:
            con.execute(f.read())
    if fautif:
        chemin = os.path.join(RACINE, "03_exercices", "dossier_M13", "modele_fautif.sql")
        with open(chemin, encoding="utf-8") as f:
            con.execute(f.read())
    if materialiser:
        for t in ("ventes", "fait_ventes", "fait_commandes", "fait_encaissements"):
            con.execute("CREATE OR REPLACE TABLE %s_m AS SELECT * FROM %s;" % (t, t))
    return con


if __name__ == "__main__":
    c = ouvrir(fautif=True)
    tables = c.execute("SELECT table_name FROM information_schema.tables "
                       "ORDER BY table_name").fetchall()
    print("tables du modele M13 :", ", ".join(t[0] for t in tables if t[0].startswith(("dim_", "fait_"))))
    print("fait_ventes    :", c.execute("SELECT COUNT(*) FROM fait_ventes").fetchone()[0], "lignes")
    print("dim_client_scd :", c.execute("SELECT COUNT(*) FROM dim_client_scd").fetchone()[0], "versions")
    rec = c.execute("SELECT * FROM recette_ca").fetchone()
    print("recette        : modele %s / source %s" % (rec[0], rec[1]))
    sys.exit(0)
'''

REVUE = """# Revue de modele — « cinq defauts a trouver » (chapitre C07)

**Le modele ci-dessous est celui d'un stagiaire. Il produit des totaux, il s'ouvre, il a l'air
correct. Il porte cinq defauts qui font des faux totaux — et deux d'entre eux ne se voient pas a
l'oeil nu.**

```sql
CREATE TABLE vente (
    id_vente     INTEGER,
    date_vente   DATE,
    mois         VARCHAR,
    id_magasin   INTEGER,
    id_client    INTEGER,
    nom_client   VARCHAR,
    ville_client VARCHAR,
    id_produit   INTEGER,
    designation  VARCHAR,
    categorie    VARCHAR,
    quantite     DOUBLE,
    montant_ttc  DOUBLE,
    ca_objectif  DOUBLE
);

CREATE TABLE magasin (
    id_magasin INTEGER,
    nom        VARCHAR,
    ville      VARCHAR
);
```

**Defaut 1 — les attributs du client sont dans la table des ventes.** Le nom, la ville et le
segment du client sont recopies sur chaque ligne. Une adresse change : il faut mettre a jour
**240 000** lignes, et oublier une ligne suffit a creer deux villes pour un client. *Correction :
une dimension client, une ligne par client, une cle etrangere dans les faits.*

**Defaut 2 — `mois` est un texte, et `date_vente` est une date : le modele a deux temps.** Les deux
colonnes disent la meme chose autrement, et elles finiront par se contredire (un mois corrige dans
l'une, pas dans l'autre). *Correction : une seule table de dates, et une cle de date dans les faits.*

**Defaut 3 — `ca_objectif` est pose sur la ligne de vente.** L'objectif est un fait au grain
magasin x mois (**218** lignes) ; pose sur **240 000** lignes de vente, il est repete et se somme
avec les ventes : le total du modele vaut alors le chiffre d'affaires **plus 42,9 % d'objectifs**.
*Correction : une table de faits `fait_objectifs` au bon grain, jointe par la cle (magasin, mois).*

**Defaut 4 — aucune cle primaire, aucune cle etrangere.** Rien n'empeche d'ecrire une vente pour un
produit qui n'existe pas, ni le meme identifiant deux fois. *Correction : cles declarees, contrôles
d'unicite et d'orphelins a chaque chargement.*

**Defaut 5 — la categorie est recopiee telle quelle depuis le fichier d'origine.** Elle porte
**16** libelles pour **7** familles : tout tableau par categorie est faux, sans qu'aucune requete ne
soit fausse. *Correction : la correspondance appartient au referentiel, pas a la requete.*

**La grille de revue en 15 points du chapitre C07 reprend chacun de ces defauts**, et les transforme
en questions fermees dont la reponse est une preuve : une requete, un compte, ou un nom.
"""


def main():
    os.makedirs(DOSSIER, exist_ok=True)
    clients = lire_clients()
    produits = lire(PRODUITS)

    mvts, scd2, scd1 = mouvements(clients)
    ecrire_csv("mouvements_clients.csv",
               "id_mouvement,id_client,date_effet,nature,valeur_avant,valeur_apres,type_scd",
               [(i + 1, ident, date, nature, avant, apres, ts)
                for i, (ident, date, nature, avant, apres, ts) in enumerate(mvts)])


    grille = tarifs(produits)
    ecrire_csv("tarifs_produits.csv", "id_produit,date_effet,prix_vente_ht",
               [tuple(t) for t in grille])

    ecrire_csv("table_plate.csv",
               "id_ligne,id_ticket,date_vente,id_client,nom_client,ville_client,segment_client,"
               "id_produit,designation,categorie,quantite,prix_unitaire",
               [(i + 1,) + tuple(l) for i, l in enumerate(table_plate())])

    ecrire("socle_m13.sql", SQL.strip().split("\n"))
    ecrire("modele_fautif.sql", FAUTIF.strip().split("\n"))
    ecrire("connexion.py", CONNEXION.strip().split("\n"))
    ecrire("revue_modele.md", REVUE.strip().split("\n"))

    # ------------------------------------------------------------ les attendus
    familles = {}
    for p in produits:
        familles[FAMILLES.get(p["categorie"].strip(), p["categorie"].strip())] = \
            familles.get(FAMILLES.get(p["categorie"].strip(), p["categorie"].strip()), 0) + 1
    prix_2023 = [t for t in grille if t[1] == "2023-01-01"]
    prix_2026 = [t for t in grille if t[1] == "2026-01-01"]
    attendu = {
        "graine": GRAINE,
        "dimensions": 5, "faits": 7, "tables_du_modele": 12,
        "mouvements_total": len(mvts), "mouvements_scd2": scd2, "mouvements_scd1": scd1,
        "clients_avec_histoire": len({m[0] for m in mvts}),
        "versions_client": len(clients) + scd2,
        # la ligne « client non identifie » : la dimension historisee doit la porter
        # comme la dimension courante, sinon la jointure au moment du fait perd le client 0
        "lignes_client_scd": len(clients) + scd2 + 1,
        "clients_referentiel": len(clients),
        "clients_sans_mouvement": len(clients) - len({m[0] for m in mvts}),
        "revue_tarifaire_lignes": len(grille),
        "versions_produit": len(grille),
        "familles_reelles": len(familles),
        "produits_par_famille_max": max(familles.values()),
        "prix_tarif_2023_moyen": round(sum(t[2] for t in prix_2023) / len(prix_2023)),
        "prix_tarif_2026_moyen": round(sum(t[2] for t in prix_2026) / len(prix_2026)),
        "table_plate_lignes": len(table_plate()),
        "table_plate_clients": len({l[2] for l in table_plate()}),
        "table_plate_libelles_categorie": len({l[8] for l in table_plate()}),
    }
    attendu["derive_tarif_pct"] = round(
        100.0 * (attendu["prix_tarif_2026_moyen"] / attendu["prix_tarif_2023_moyen"] - 1), 1)
    with open(os.path.join(DOSSIER, "ATTENDU.json"), "w", encoding="utf-8") as f:
        json.dump(attendu, f, ensure_ascii=False, indent=2, sort_keys=True)

    print("dossier_M13 ecrit dans 03_exercices/dossier_M13/")
    for ligne in ("mouvements_clients.csv", "tarifs_produits.csv", "table_plate.csv",
                  "socle_m13.sql", "modele_fautif.sql", "connexion.py", "revue_modele.md",
                  "ATTENDU.json"):
        print("   %-24s %8d o" % (ligne, os.path.getsize(os.path.join(DOSSIER, ligne))))
    print("   dimensions : %d · faits : %d · tables : %d"
          % (attendu["dimensions"], attendu["faits"], attendu["tables_du_modele"]))
    print("   mouvements : %d (SCD2 %d / SCD1 %d) · versions client : %d"
          % (attendu["mouvements_total"], attendu["mouvements_scd2"],
             attendu["mouvements_scd1"], attendu["versions_client"]))
    print("   tarifs     : %d lignes, derive %.1f %% (%d -> %d FCFA)"
          % (attendu["revue_tarifaire_lignes"], attendu["derive_tarif_pct"],
             attendu["prix_tarif_2023_moyen"], attendu["prix_tarif_2026_moyen"]))
    print("   familles   : %d (max %d produits)" % (attendu["familles_reelles"],
                                                    attendu["produits_par_famille_max"]))


if __name__ == "__main__":
    main()
