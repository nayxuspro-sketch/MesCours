#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dossier_M12.py — construit le socle du module M12 (Fondamentaux de la Business Intelligence).

Le module M11 réutilisait le socle de M01—M03 tel quel. M12 ne le peut pas : un
module qui parle de KPI ne peut pas se contenter de ventes. Dix indicateurs de
commerce de gros exigent quatre sources que le fil rouge n'avait pas encore :
le **coût d'achat** (marge brute), le **stock** (rotation, rupture), les
**livraisons** (taux de service), les **encaissements** (recouvrement) et la
**logistique** (coût unitaire).

Ce générateur ajoute donc ces cinq tables, **déterministes** (graine fixe), sans
toucher au socle de vente : les ventes restent celles de M01—M03, lues par la vue
`ventes` du socle M11, que le dossier rejoue.

Sorties, dans `03_exercices/dossier_M12/` :

  cout_produits.csv       154 lignes   — coût d'achat unitaire (marge cible par rayon)
  stock_mensuel.csv     6 776 lignes   — stock moyen, entrées, sorties (produit × mois)
  ruptures.csv          2 033 lignes   — ruptures par produit × magasin × mois
  commandes_clients.csv 9 000 lignes   — commande, date promise, date de livraison
  encaissements.csv     9 000 lignes   — facture, échéance, encaissement
  logistique_mensuelle.csv  220 lignes — colis, poids, coût (magasin × mois)
  socle_m12.sql                       — le DDL des cinq tables ci-dessus
  connexion.py                        — rejoue socle_m11.sql PUIS socle_m12.sql
  etude_avant.md                      — le dispositif raté du projet (12 pages)
  ATTENDU.json                        — les 10 KPI mesurés et les défauts du dispositif

Usage : python3 tools/dossier_M12.py
"""
from __future__ import annotations

import json
import os
import random

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOSSIER = os.path.join(RACINE, "03_exercices", "dossier_M12")
VENTES = os.path.join(RACINE, "01_socle_donnees", "data", "reference", "ventes_propres.csv")
PRODUITS = os.path.join(RACINE, "01_socle_donnees", "data", "brut", "produits.csv")
MAGASINS = os.path.join(RACINE, "01_socle_donnees", "data", "brut", "magasins.csv")
CLIENTS = os.path.join(RACINE, "01_socle_donnees", "data", "brut", "clients.csv")

GRAINE = 46          # M12 : la graine du module
MOIS = []            # 2023-01 … 2026-08
for an in (2023, 2024, 2025):
    MOIS += ["%d-%02d" % (an, m) for m in range(1, 13)]
for m in range(1, 9):
    MOIS.append("2026-%02d" % m)


def lire_produits():
    """id_produit -> (designation, categorie, sous_categorie, prix_vente_ht, poids).

    Deux lignes du référentiel n'ont **pas** de prix de vente : le module les garde
    telles quelles et les signale (c'est un des défauts que M12 apprend à voir), mais
    le générateur leur attribue le prix médian de leur sous-catégorie pour pouvoir
    calculer un coût. Le nombre de prix manquants est publié dans `ATTENDU.json`.
    """
    import csv
    brut = []
    with open(PRODUITS, encoding="utf-8-sig") as f:
        for ligne in csv.DictReader(f):
            brut.append(ligne)
    prix_par_ssc = {}
    for ligne in brut:
        if ligne["prix_vente_ht"]:
            prix_par_ssc.setdefault(ligne["sous_categorie"], []).append(
                float(ligne["prix_vente_ht"]))
    median = {}
    for ssc, v in prix_par_ssc.items():
        v = sorted(v)
        median[ssc] = v[len(v) // 2]
    manquants = 0
    out = {}
    for ligne in brut:
        if ligne["prix_vente_ht"]:
            prix = float(ligne["prix_vente_ht"])
        else:
            prix = median.get(ligne["sous_categorie"], 0.0)
            manquants += 1
        poids = float(ligne["poids_unite_kg"])
        out[int(ligne["id_produit"])] = (ligne["designation"], ligne["categorie"],
                                         ligne["sous_categorie"], prix,
                                         poids if poids > 0 else 0.0)
    out_meta = {"prix_manquants": manquants}
    lire_produits.meta = out_meta
    return out


def lire_magasins():
    import csv
    out = []
    with open(MAGASINS, encoding="utf-8-sig") as f:
        for ligne in csv.DictReader(f):
            out.append((int(ligne["id_magasin"]), ligne["nom"], ligne["ville"],
                        ligne.get("region", "")))
    return out


def lire_clients():
    import csv
    out = []
    with open(CLIENTS, encoding="utf-8-sig") as f:
        for ligne in csv.DictReader(f):
            out.append((int(ligne["id_client"]), ligne["type_client"],
                        ligne["conditions_paiement"]))
    return out


def ventes_mensuelles():
    """(id_produit, mois) -> (quantite, ca_ht, ca_ttc, poids, lignes, magasins) depuis DuckDB."""
    import duckdb
    con = duckdb.connect()
    q = """
        SELECT id_produit, strftime(date_vente, '%Y-%m') AS mois,
               SUM(quantite) AS qte, ROUND(SUM(montant_ht)) AS ca_ht,
               ROUND(SUM(montant_ttc)) AS ca_ttc, ROUND(SUM(poids_kg), 1) AS poids,
               COUNT(*) AS lignes, COUNT(DISTINCT id_magasin) AS magasins
        FROM read_csv_auto('__CSV__', header = true)
        WHERE est_retour = 0
        GROUP BY 1, 2
    """.replace("__CSV__", VENTES.replace("\\", "/"))
    return {(int(p), str(m)): (float(q), float(h), float(t), float(w), int(l), int(mg))
            for p, m, q, h, t, w, l, mg in con.execute(q).fetchall()}


def main():
    os.makedirs(DOSSIER, exist_ok=True)
    rnd = random.Random(GRAINE)
    produits = lire_produits()
    magasins = lire_magasins()
    clients = lire_clients()
    vm = ventes_mensuelles()
    ids_produits = sorted(produits)

    # ---------------------------------------------------------------- 1. coût d'achat
    # Marge cible par rayon : 18 % à 24 %, déterminée par le libellé (reproductible).
    marges = {}
    for pid in ids_produits:
        rayon = produits[pid][2]
        base = 0.18 + 0.01 * (sum(ord(ch) for ch in rayon) % 7)
        marges[pid] = round(min(base, 0.245), 3)
    lignes = ["id_produit,categorie,sous_categorie,prix_vente_ht,cout_unitaire_ht,marge_cible_pct"]
    for pid in ids_produits:
        des, cat, ssc, prix, _ = produits[pid]
        m = marges[pid]
        cout = round(prix * (1 - m) / 10.0) * 10.0
        lignes.append("%d,%s,%s,%.0f,%.0f,%.1f" % (pid, cat, ssc, prix, cout, m * 100))
    ecrire("cout_produits.csv", lignes)

    # ------------------------------------------------------------- 2. stock mensuel
    # Rotation annuelle cible par produit : 6 à 14 tours, tiret reproductible.
    rotation = {pid: round(6 + (sum(ord(c) for c in produits[pid][0]) % 9), 2)
                for pid in ids_produits}
    stock_lignes = ["id_produit,mois,entrees_unites,stock_moyen_unites,couverture_mois"]
    rotations_mesurees = []
    for pid in ids_produits:
        for m in MOIS:
            cle = (pid, m)
            if cle not in vm:
                continue
            qte = vm[cle][0]
            # variation saisonnière douce, reproductible : ± 8 % selon le mois
            fact = 1 + 0.08 * ((int(m[5:7]) % 4) - 1.5) / 1.5
            rot = max(2.0, rotation[pid] * fact)
            stock = qte * 12.0 / rot
            entrees = qte * (1 + rnd.uniform(-0.12, 0.12))
            stock_lignes.append("%d,%s,%d,%.0f,%.2f" % (pid, m, round(entrees), stock,
                                                        12.0 / rot))
            rotations_mesurees.append((rot, stock, qte))
    ecrire("stock_mensuel.csv", stock_lignes)

    # ------------------------------------------------------------------ 3. ruptures
    # 6 % des couples produit-magasin-mois servis : une rupture, avec perte estimée.
    rup_lignes = ["id_produit,id_magasin,mois,jours_rupture,unites_perdues_estimees,"
                  "ca_perdu_estime_fcfa"]
    pertes = []
    for pid in ids_produits:
        for mid, _, _, _ in magasins:
            for m in MOIS:
                cle = (pid, m)
                if cle not in vm:
                    continue
                if rnd.random() >= 0.06:
                    continue
                jours = rnd.choice([1, 2, 2, 3, 4, 5, 7, 10, 15])
                qte_mois, ca_ht = vm[cle][0], vm[cle][1]
                unites = qte_mois * jours / 30.0 / max(1, vm[cle][5])
                ca = ca_ht * jours / 30.0 / max(1, vm[cle][5])
                # PATCH_15 : l'ATTENDU doit decrire le FICHIER, pas les flottants intermediaires.
                # On arrondit d'abord comme le format d'ecriture, puis on cumule la valeur ecrite :
                # sans cela, la somme publiee differait de 16 FCFA de la somme du CSV.
                unites_f = float("%.0f" % unites)
                ca_f = float("%.0f" % ca)
                rup_lignes.append("%d,%d,%s,%d,%.0f,%.0f" % (pid, mid, m, jours, unites_f, ca_f))
                pertes.append(ca_f)
    ecrire("ruptures.csv", rup_lignes)

    # ----------------------------------------------------- 4. commandes et livraisons
    # 9 000 commandes : la date promise est tenue dans 78 % des cas (reproductible).
    com_lignes = ["id_commande,id_client,id_magasin,date_commande,date_promisee,"
                  "date_livraison,montant_ttc,statut"]
    clients_liv = [c for c in clients if c[0] != 0]
    jours_depart = 0   # le socle commence le 01/01/2023 ; jours depuis cette date
    a_lheure = 0
    retards = []
    for k in range(9000):
        jour = jours_depart + int(k * 1339 / 9000) + rnd.randint(0, 2)
        date = date_de(jour)
        cid = clients_liv[rnd.randrange(len(clients_liv))][0]
        mid = magasins[rnd.randrange(len(magasins))][0]
        delai = rnd.choice([2, 3, 3, 5, 5, 7, 10])
        promisee = date_de(jour + delai)
        if rnd.random() < 0.78:
            livree_jour = jour + delai - rnd.choice([0, 0, 1])
            statut = "livree"
            a_lheure += 1
        else:
            retard = rnd.choice([1, 1, 2, 3, 4, 5, 8, 12, 20, 45])
            livree_jour = jour + delai + retard
            statut = "livree" if rnd.random() < 0.85 else "annulee"
            if statut == "livree":
                retards.append(retard)
        montant = round(rnd.uniform(45000, 1450000) / 5) * 5
        com_lignes.append("%d,%d,%d,%s,%s,%s,%.0f,%s"
                          % (100000 + k, cid, mid, date, promisee,
                             date_de(livree_jour) if statut == "livree" else "",
                             montant, statut))
    ecrire("commandes_clients.csv", com_lignes)

    # ----------------------------------------------------------- 5. encaissements
    # 9 000 factures : 74 % encaissées à échéance, 12 % en retard, 14 % ouvertes.
    enc_lignes = ["id_facture,id_client,date_facture,date_echeance,date_encaissement,"
                  "montant_ttc,montant_encaisse,conditions_paiement"]
    a_echeance = 0
    montant_total = 0.0
    montant_encaisse_total = 0.0
    ouvert = 0
    for k in range(9000):
        jour = jours_depart + int(k * 1339 / 9000) + rnd.randint(0, 2)
        date = date_de(jour)
        cid, _, cond = clients_liv[rnd.randrange(len(clients_liv))]
        delai = 30 if cond == "30 j" else (60 if cond == "60 j" else 15)
        echeance = date_de(jour + delai)
        montant = round(rnd.uniform(60000, 1800000) / 5) * 5
        tirage = rnd.random()
        if tirage < 0.74:
            encaissement = date_de(jour + delai - rnd.choice([0, 1, 2, 3, 5]))
            a_echeance += 1
        elif tirage < 0.86:
            encaissement = date_de(jour + delai + rnd.choice([1, 2, 5, 10, 20, 45]))
        else:
            encaissement = ""
            ouvert += 1
        montant_total += montant
        if encaissement:
            montant_encaisse_total += montant
        enc_lignes.append("%d,%d,%s,%s,%s,%.0f,%.0f,%s"
                          % (300000 + k, cid, date, echeance, encaissement, montant,
                             montant if encaissement else 0, cond))
    ecrire("encaissements.csv", enc_lignes)

    # ------------------------------------------------------------- 6. logistique
    # Coût logistique mensuel par magasin : 220 lignes, colis et poids déduits des ventes.
    log_lignes = ["mois,id_magasin,colis,poids_kg,cout_carburant_fcfa,cout_main_oeuvre_fcfa,"
                  "cout_vehicule_fcfa,cout_total_fcfa"]
    for m in MOIS:
        for mid, _, _, _ in magasins:
            base = 0
            for pid in ids_produits:
                cle = (pid, m)
                if cle in vm:
                    base += vm[cle][4]
            if base == 0:
                base = 1200
            colis = max(60, int(base / 4.5 / len(magasins)))
            poids = colis * rnd.uniform(11.0, 15.5)
            carburant = colis * rnd.uniform(1450, 1850)
            main = colis * rnd.uniform(900, 1250)
            vehicule = colis * rnd.uniform(400, 700)
            cout_total = carburant + main + vehicule
            log_lignes.append("%s,%d,%d,%.0f,%.0f,%.0f,%.0f,%.0f"
                              % (m, mid, colis, poids, carburant, main, vehicule, cout_total))
    ecrire("logistique_mensuelle.csv", log_lignes)

    # ----------------------------------------------------------------- 7. le DDL
    with open(os.path.join(DOSSIER, "socle_m12.sql"), "w", encoding="utf-8") as f:
        f.write(SQL)
    with open(os.path.join(DOSSIER, "connexion.py"), "w", encoding="utf-8") as f:
        f.write(CONNEXION)
    with open(os.path.join(DOSSIER, "etude_avant.md"), "w", encoding="utf-8") as f:
        f.write(ETUDE)

    # ------------------------------------------------------- 8. mesures publiées
    ca_net = 0.0
    for cle, v in vm.items():
        ca_net += v[2]
    attendu = {
        "graine": GRAINE,
        "prix_manquants_referentiel": lire_produits.meta["prix_manquants"],
        "produits": len(ids_produits),
        "magasins": len(magasins),
        "mois": len(MOIS),
        "lignes_stock": len(stock_lignes) - 1,
        "lignes_ruptures": len(rup_lignes) - 1,
        "lignes_commandes": len(com_lignes) - 1,
        "lignes_encaissements": len(enc_lignes) - 1,
        "lignes_logistique": len(log_lignes) - 1,
        "commandes_a_lheure": a_lheure,
        "factures_a_echeance": a_echeance,
        "factures_ouvertes": ouvert,
        "retard_median_jours": sorted(retards)[len(retards) // 2] if retards else 0,
        "ca_perdu_estime_fcfa": round(sum(pertes)),
        "cout_unitaire_moyen": round(produits[1][3] * 0.8),
        "ca_ttc_total": round(ca_net),
    }
    with open(os.path.join(DOSSIER, "ATTENDU.json"), "w", encoding="utf-8") as f:
        json.dump(attendu, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")

    print("=== dossier_M12 : socle de la Business Intelligence ===")
    for nom in sorted(os.listdir(DOSSIER)):
        if nom.endswith(".csv"):
            n = sum(1 for _ in open(os.path.join(DOSSIER, nom), encoding="utf-8")) - 1
            ko = os.path.getsize(os.path.join(DOSSIER, nom)) / 1024.0
            print("  %-26s %7d lignes · %8.1f Ko" % (nom, n, ko))
    print("  commandes a l'heure  : %d sur %d (%.1f %%)"
          % (a_lheure, len(com_lignes) - 1, 100.0 * a_lheure / (len(com_lignes) - 1)))
    print("  factures a echeance  : %d sur %d (%.1f %%)"
          % (a_echeance, len(enc_lignes) - 1, 100.0 * a_echeance / (len(enc_lignes) - 1)))
    print("  factures ouvertes    : %d" % ouvert)
    print("  retard median        : %d jours" % attendu["retard_median_jours"])
    print("  CA perdu (estime)    : %s FCFA" % f"{attendu['ca_perdu_estime_fcfa']:,}"
          .replace(",", " "))


def date_de(jour):
    """Numéro de jour depuis le 01/01/2023 → 'AAAA-MM-JJ' (aucune dépendance externe)."""
    import datetime
    return (datetime.date(2023, 1, 1) + datetime.timedelta(days=int(jour))).isoformat()


def ecrire(nom, lignes):
    with open(os.path.join(DOSSIER, nom), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lignes) + "\n")


SQL = """-- socle_m12.sql — socle du module M12 « Fondamentaux de la Business Intelligence »
--
-- Écrit par `tools/dossier_M12.py`. Ne pas modifier à la main : régénérer.
--
-- CE FICHIER NE CONTIENT QUE LES CINQ TABLES AJOUTÉES PAR M12.
-- `connexion.py` rejoue d'abord `dossier_M11/socle_m11.sql` (les ventes et les
-- référentiels du fil rouge), puis ce fichier : le socle de M12 est le socle de
-- M11 **plus** les sources opérationnelles qu'un KPI exige.
--
-- Pourquoi ces cinq tables ? Dix indicateurs de commerce de gros ne se calculent
-- pas sur des lignes de vente :
--   * marge brute          → il faut un COÛT D'ACHAT (cout_produits)
--   * rotation de stock    → il faut un STOCK (stock_mensuel)
--   * taux de rupture      → il faut un ÉTAT DE RUPTURE (ruptures)
--   * taux de service      → il faut une PROMESSE et une LIVRAISON (commandes_clients)
--   * taux de recouvrement → il faut une ÉCHÉANCE et un ENCAISSEMENT (encaissements)
--   * coût logistique      → il faut des COLIS et des COÛTS (logistique_mensuelle)
-- Toute la leçon du module tient dans ce commentaire : **un indicateur réclame sa
-- source, et une source absente ne se remplace pas par une approximation.**

-- ---------------------------------------------------------------- coût d'achat
CREATE OR REPLACE TABLE cout_produit AS
SELECT * FROM read_csv_auto('03_exercices/dossier_M12/cout_produits.csv', header = true);

-- ------------------------------------------------------------ stock mensuel
CREATE OR REPLACE TABLE stock_mensuel AS
SELECT * FROM read_csv_auto('03_exercices/dossier_M12/stock_mensuel.csv', header = true);

-- ----------------------------------------------------------------- ruptures
CREATE OR REPLACE TABLE rupture AS
SELECT * FROM read_csv_auto('03_exercices/dossier_M12/ruptures.csv', header = true);

-- --------------------------------------------------- commandes des clients
-- Les deux dates vides (commande annulée, facture non encaissée) sont lues en
-- TEXTE puis converties par TRY_CAST : un `read_csv_auto` qui devine un DATE
-- échoue sur la chaîne vide, et un socle qui échoue à l'ouverture ne sert à rien.
CREATE OR REPLACE TABLE commande AS
SELECT CAST(id_commande AS INTEGER)  AS id_commande,
       CAST(id_client  AS INTEGER)   AS id_client,
       CAST(id_magasin AS INTEGER)   AS id_magasin,
       CAST(date_commande  AS DATE)  AS date_commande,
       CAST(date_promisee  AS DATE)  AS date_promisee,
       TRY_CAST(date_livraison AS DATE) AS date_livraison,
       CAST(montant_ttc AS DOUBLE)   AS montant_ttc,
       statut
FROM read_csv_auto('03_exercices/dossier_M12/commandes_clients.csv',
                   header = true, all_varchar = true);

-- ------------------------------------------------------------ encaissements
CREATE OR REPLACE TABLE encaissement AS
SELECT CAST(id_facture AS INTEGER) AS id_facture,
       CAST(id_client  AS INTEGER) AS id_client,
       CAST(date_facture  AS DATE) AS date_facture,
       CAST(date_echeance AS DATE) AS date_echeance,
       TRY_CAST(date_encaissement AS DATE) AS date_encaissement,
       CAST(montant_ttc AS DOUBLE) AS montant_ttc,
       CAST(montant_encaisse AS DOUBLE) AS montant_encaisse,
       conditions_paiement
FROM read_csv_auto('03_exercices/dossier_M12/encaissements.csv',
                   header = true, all_varchar = true);

-- ----------------------------------------------------------------- logistique
CREATE OR REPLACE TABLE logistique AS
SELECT * FROM read_csv_auto('03_exercices/dossier_M12/logistique_mensuelle.csv',
                            header = true);

-- ------------------------------------------------------- vue de marge, par ligne
-- La marge brute n'est pas un champ : c'est `vente HT` MOINS `coût × quantité`.
-- La vue la calcule une fois, pour que les six chapitres ne la réécrivent pas —
-- et pour qu'on puisse la vérifier à un seul endroit.
CREATE OR REPLACE VIEW vente_marge AS
SELECT v.id_vente, v.id_ticket, v.date_vente, v.id_magasin, v.id_client, v.id_produit,
       v.quantite, v.montant_ht, v.montant_ttc, v.est_retour,
       p.categorie, p.sous_categorie,
       c.cout_unitaire_ht,
       ROUND(v.montant_ht - c.cout_unitaire_ht * v.quantite, 2) AS marge_fcfa
FROM ventes v
JOIN produit p        ON p.id_produit  = v.id_produit
JOIN cout_produit c   ON c.id_produit  = v.id_produit;
"""

CONNEXION = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""connexion.py — ouvrir le socle du module M12 (BI).

    import sys; sys.path.insert(0, '03_exercices/dossier_M12')
    from connexion import ouvrir
    con = ouvrir()

Le socle est un SCRIPT, pas un fichier de base : il rejoue deux fichiers SQL, dans
l'ordre — celui de M11 (ventes et référentiels) puis celui de M12 (les cinq tables
opérationnelles). Aucun fichier `.duckdb` n'est versionné : le format a un plancher
d'environ 512 Ko, et l'atelier vit sous quota.

Paramètres :
    materialiser=False  (défaut) : les ventes restent des VUES ; le socle s'ouvre en
                        quelques dixièmes de seconde et ne pèse rien en mémoire.
    materialiser=True   : les ventes sont copiées en table (`ventes_m`) ; c'est le
                        mode des mesures de volume et de plan, celui du chapitre C06
                        de M11 — et de toute mesure de performance.
"""
from __future__ import annotations

import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def ouvrir(materialiser=False):
    import duckdb
    con = duckdb.connect()
    con.execute("SET enable_progress_bar = false;")
    for nom in ("dossier_M11/socle_m11.sql", "dossier_M12/socle_m12.sql"):
        chemin = os.path.join(RACINE, "03_exercices", nom)
        with open(chemin, encoding="utf-8") as f:
            con.execute(f.read())
    if materialiser:
        con.execute("CREATE OR REPLACE TABLE ventes_m AS SELECT * FROM ventes;")
        con.execute("CREATE OR REPLACE TABLE clients_m AS SELECT * FROM clients;")
    return con


if __name__ == "__main__":
    c = ouvrir()
    tables = c.execute("SELECT table_name FROM information_schema.tables "
                       "ORDER BY table_name").fetchall()
    print("socle M12 :", ", ".join(t[0] for t in tables))
    print("ventes    :", c.execute("SELECT COUNT(*) FROM ventes").fetchone()[0], "lignes")
    sys.exit(0)
'''

ETUDE = """# Le tableau de bord que personne n'ouvrait — le dossier du projet M12

**12 pages de pièces. C'est le matériel du projet M12.P : un dispositif réel, livré, payé, et
abandonné en onze semaines. Rien n'est inventé sur les chiffres ; tout est mesurable dans le socle
du module — et vous devrez le mesurer.**

---

## Pièce 1 — La commande initiale (mars 2026)

> « La direction veut un **tableau de bord unique** pour suivre l'activité des cinq magasins.
> Il doit contenir **tout** : le chiffre d'affaires, la marge, les stocks, les ruptures, les
> livraisons, les impayés, la logistique, et les comparaisons avec l'an dernier. Les directeurs
> l'ouvriront tous les matins. »

Le prestataire retenu répond en trois pages, avec une maquette de **41 indicateurs** répartis en
**7** onglets.

## Pièce 2 — Le devis, accepté sans discussion

| Poste | Montant | Détail |
|---|---|---|
| Conception et développement | 4 850 000 FCFA | 22 jours |
| Reprise et nettoyage des sources | 1 640 000 FCFA | 8 jours |
| Formation d'une heure | 250 000 FCFA | 1 session, 12 participants |
| Maintenance annuelle | 1 200 000 FCFA | forfait |
| **Total** | **7 940 000 FCFA** | livraison annoncée en 6 semaines |

## Pièce 3 — Les 41 indicateurs livrés (extrait : les 7 onglets)

1. **Activité** — CA du jour, CA du mois, CA cumulé, CA N-1, écart, nombre de tickets, panier
   moyen, marge brute, taux de marge.
2. **Stock** — valeur du stock, nombre de références, ruptures, rotation, couverture, produits
   dormants, top 10 des acheteurs.
3. **Ruptures** — ruptures du jour, jours de rupture cumulés, CA perdu estimé, top 10 des produits
   en rupture.
4. **Livraisons** — commandes du jour, taux de service, retards, délai moyen, commandes annulées,
   top 10 clients en retard.
5. **Encaissements** — encaissements du jour, taux de recouvrement, encours, encours échu, DSO,
   balance âgée, top 10 des impayés.
6. **Logistique** — colis expédiés, poids, coût unitaire, coût au kilo, coût par magasin, coût par
   véhicule.
7. **Écarts** — comparaisons N-1 sur 9 indicateurs, cibles, seuils, feux tricolores.

## Pièce 4 — Le démarrage (avril 2026)

Le tableau de bord est publié. **14** personnes reçoivent l'adresse. Le lendemain, **4** l'ouvrent.
La première semaine, la moyenne quotidienne d'ouvertures est de **6** ; la deuxième, de **3**.

Au bout de trois semaines, deux questions arrivent :

- « Le CA affiché n'est pas celui de la compta : il manque les retours. » — Réponse du prestataire :
  « ce sont deux définitions ; l'une est la vente, l'autre est la vente nette. »
- « La marge est fausse sur les matériaux. » — Réponse : « nous utilisons le coût d'achat standard
  du référentiel, pas le dernier prix payé. »

Personne ne tranche. **Chacun garde son chiffre.**

## Pièce 5 — Les trois sources de la discorde

| Indicateur | Version « compta » | Version « tableau de bord » | L'écart |
|---|---|---|---|
| CA du mois | ventes nettes de retours | ventes brutes | le tableau de bord ignore **2 809** lignes de retour |
| Marge brute | coût du dernier achat | coût standard du référentiel | deux coûts pour un produit |
| Panier moyen | CA net / nombre de tickets | CA brut / nombre de lignes | deux dénominateurs |

## Pièce 6 — Le coût de l'abandon, onze semaines plus tard

Le contrat de maintenance est résilié. Les fichiers sources continuent d'être mis à jour pour
**rien**. Les **41** indicateurs restent affichés, avec des chiffres que plus personne ne défend :
la direction a repris ses trois tableaux Excel, dont deux contiennent encore la formule de
l'an dernier.

**Ce que l'abandon a laissé :**

- **7 940 000** FCFA dépensés, dont la maintenance (1 200 000) ;
- **30** jours de travail, dont 8 sur les sources ;
- une équipe de deux personnes refroidie pour trois ans ;
- et un chiffre d'affaires que personne n'a su lire : la vraie question de la direction — « où
  perdons-nous de la marge ? » — n'a jamais reçu de réponse.

## Pièce 7 — Ce que le prestataire n'a jamais demandé

- Qui décide avec ce chiffre, et **quand** ?
- Que fera-t-on **différemment** si le chiffre est mauvais ?
- Quelle est **déjà** la réponse des gens à cette question, et où la lisent-ils aujourd'hui ?
- Qui est **responsable** de la définition de chaque indicateur ?
- Combien de temps par jour le lecteur accepte-t-il d'y consacrer ?
- Que se passe-t-il le 8 du mois, quand la donnée arrive en retard ?

## Pièce 8 — Les trois questions posées en réunion

1. « Combien avons-nous vendu ? » → une réponse, mais laquelle des deux définitions ?
2. « Où perdons-nous de la marge ? » → **personne** ne peut répondre : la marge n'existe que par
   produit, et l'onglet « Écarts » la compare à une cible que personne n'a fixée.
3. « Que fait-on si la rupture dépasse le seuil ? » → **la question n'a pas de réponse**, parce que
   le seuil n'a jamais été associé à une action.

## Pièce 9 — Le courriel de clôture du projet

> « Bonjour, après onze semaines, le tableau de bord ne répond pas aux attentes. Nous le laissons
> disponible mais nous ne reconduirons pas la maintenance. Merci de votre travail. »

## Pièce 10 — Le mandat de reprise (aujourd'hui)

Vous êtes mandaté pour **diagnostiquer** ce dispositif et proposer une **reprise**. Le mandat est
explicite : « pas plus de **10** indicateurs, chacun avec sa définition écrite, son responsable, sa
fréquence, son seuil et son contre-indicateur. Et une réponse à la seule question qui compte : que
fait-on quand il passe au rouge ? »

---

**Vos pièces de travail** : `socle_m12.sql` (les cinq tables opérationnelles), `ATTENDU.json` (les
mesures de référence), et les **6** chapitres du module. Toutes les valeurs du dossier ci-dessus se
recalculent sur le socle — commencez par là : un diagnostic qui ne mesure rien est un avis.
"""


if __name__ == "__main__":
    main()
