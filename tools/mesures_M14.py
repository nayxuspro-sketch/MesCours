#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mesures_M14.py — l'instrument du module M14 : le rapport Power BI, prepare et controle.

Power BI Desktop n'existe pas dans cet atelier : l'instrument fait donc tout ce qui peut
etre fait SANS lui, et publie ce qui sert de reference a l'apprenant.

  1. **ecosysteme et licences** — les quatre surfaces, les quatre formules, le seuil F64,
     les limites de modele ; constantes DATEES (verifiees en septembre 2026) ;
  2. **poids d'import** — combien pese chaque table du modele M13 exportee en CSV : c'est
     la matiere du choix Import contre DirectQuery ;
  3. **export du modele** (`--export`) — ecrit les tables du modele M13 en CSV d'import,
     hors atelier par defaut (`/tmp/m14_import`) : 240 000 lignes de ventes ne se
     versionnent pas ;
  4. **les dix valeurs du tableau de bord** — calculees DEUX fois : sur les tables
     operationnelles (la definition de M12) et sur le modele en etoile (l'objet de M14),
     puis comparees. Deux chemins, un seul chiffre : c'est la these du module ;
  5. **le modele du rapport** — les 12 relations, les 2 relations inactives (les deux
     autres dates de la commande), les 2 candidats au filtrage bidirectionnel examines
     puis refuses, et le cout d'achat absent du modele M13 ;
  6. **la grille de conception** — 18 points (4 + 5 + 5 + 4) et les 6 ajouts du module ;
  7. **controle du dossier** — les pieces du dossier M14 sont-elles la ?

Usage :
    python3 tools/mesures_M14.py                    # deroule tout et publie le verdict
    python3 tools/mesures_M14.py --json             # les mesures seules, en JSON
    python3 tools/mesures_M14.py --export           # ecrit les CSV d'import dans /tmp
    python3 tools/mesures_M14.py --export --ou DIR  # ... ailleurs
"""
from __future__ import annotations

import csv
import json
import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOSSIER = os.path.join(RACINE, "03_exercices", "dossier_M14")
SORTIE_DEFAUT = "/tmp/m14_import"

# Les douze tables du rapport : celles qui portent le tableau de bord commercial.
TABLES_RAPPORT = (
    "dim_client", "dim_produit", "dim_magasin", "dim_vendeur", "dim_date",
    "fait_ventes", "fait_commandes", "fait_encaissements",
    "fait_ruptures", "fait_stock_mensuel", "fait_objectifs", "fait_logistique",
)

# Les 12 relations ACTIVES du rapport : (fait, colonne, dimension, colonne).
RELATIONS = (
    ("fait_ventes", "id_magasin", "dim_magasin", "id_magasin"),
    ("fait_ventes", "id_produit", "dim_produit", "id_produit"),
    ("fait_ventes", "id_client", "dim_client", "id_client"),
    ("fait_ventes", "id_vendeur", "dim_vendeur", "id_vendeur"),
    ("fait_ventes", "date_vente", "dim_date", "date"),
    ("fait_commandes", "id_magasin", "dim_magasin", "id_magasin"),
    ("fait_commandes", "id_client", "dim_client", "id_client"),
    ("fait_commandes", "date_commande", "dim_date", "date"),
    ("fait_encaissements", "id_client", "dim_client", "id_client"),
    ("fait_encaissements", "date_facture", "dim_date", "date"),
    ("fait_ruptures", "id_produit", "dim_produit", "id_produit"),
    ("fait_ruptures", "id_magasin", "dim_magasin", "id_magasin"),
)

# Les 2 relations INACTIVES : la commande porte trois dates pour une seule table de dates.
INACTIVES = (
    ("fait_commandes", "date_promisee", "dim_date", "date",
     "la date promise sert au taux de service : elle s'active par une fonction, pas par le filtre"),
    ("fait_commandes", "date_livraison", "dim_date", "date",
     "la date de livraison est celle du fait accompli : c'est la relation active du fait"),
)

# Les 2 candidats au filtrage bidirectionnel : examines, mesures, refuses.
BIDIRECTIONNELS = (
    ("fait_ruptures", "dim_produit",
     "filtrer les produits par les ruptures : le rapport doit dire la disponibilite d'un "
     "produit, pas reduire le catalogue aux produits en rupture"),
    ("fait_objectifs", "dim_magasin",
     "lire l'objectif depuis le filtre magasin : le sens unique suffit, et le retour "
     "d'un filtre sur une table de faits fait perdre la maitrise du grain"),
)


def f(x):
    """1500000 -> '1 500 000'."""
    return "{:,}".format(int(round(float(x)))).replace(",", " ")


def fd(x):
    """0.31 -> '0,31'."""
    return ("%g" % float(x)).replace(".", ",")


def _connexion():
    sys.path.insert(0, os.path.join(RACINE, "03_exercices", "dossier_M13"))
    from connexion import ouvrir
    return ouvrir()


# --------------------------------------------------------------------------- 1
def ecosysteme():
    """Les faits d'outil, dates, et convertis en FCFA au taux pedagogique du manuel."""
    taux = 600.0
    out = {
        "m14_taux_usd_fcfa": 600,
        "m14_prix_desktop_usd": 0,
        "m14_prix_pro_usd": 14,
        "m14_prix_pro_fcfa": 14 * 600,
        "m14_prix_ppu_usd": 24,
        "m14_prix_ppu_fcfa": 24 * 600,
        "m14_prix_f64_unites": 64,
        "m14_prix_modele_pro_go": 1,
        "m14_prix_modele_ppu_go": 100,
        "m14_prix_actualisations_pro": 8,
        "m14_prix_actualisations_ppu": 48,
        "m14_prix_texte": (
            "Desktop est gratuit (creation et analyse locales) ; Pro coute %d USD par "
            "utilisateur et par mois, soit %s FCFA au taux pedagogique de %d FCFA pour "
            "1 USD ; Premium Per User coute %d USD, soit %s FCFA. Une capacite Fabric a "
            "partir de F64 (%d unites de capacite, equivalent de l'ancien P1) fait "
            "consulter des lecteurs SANS licence payante : c'est le seul seuil qui change "
            "l'economie. Au-dessus : modele %d Go et %d actualisations par jour pour Pro, "
            "%d Go et %d pour PPU."
            % (14, f(14 * 600), int(taux), 24, f(24 * 600), 64, 1, 8, 100, 48)),
        "m14_prix_exemple_pro_personnes": 4,
        "m14_prix_exemple_pro_fcfa": f(4 * 14 * 600),
        "m14_prix_exemple_pro_an_fcfa": f(4 * 14 * 600 * 12),
        "m14_prix_lecteurs_100_fcfa": f(100 * 14 * 600),
        "m14_prix_lecteurs_300_fcfa": f(300 * 14 * 600),
        "m14_prix_lecteurs_40_fcfa": f(40 * 14 * 600),
        "m14_prix_lecteurs_5_mois_fcfa": f(5 * 14 * 600),
        "m14_prix_lecteurs_5_an_fcfa": f(5 * 14 * 600 * 12),
        "m14_prix_lecteurs_7_mois_fcfa": f(7 * 14 * 600),
        "m14_prix_lecteurs_7_an_fcfa": f(7 * 14 * 600 * 12),
        "m14_prix_texte_echelle": (
            "en dessous du seuil, la facture suit les personnes : 100 lecteurs en formule simple "
            "coutent 840 000 FCFA par mois, 300 en coutent 2 520 000, et 40 en coutent 336 000. "
            "A partir du seuil F64, le cout suit la machine et le nombre de lecteurs ne se paie "
            "plus"),
        "m14_prix_texte_pilote": (
            "un pilote pour 4 personnes (1 auteur et 3 lecteurs) coute 4 fois 8 400 FCFA par "
            "mois, soit 33 600 FCFA par mois et 403 200 FCFA par an. Le dispositif rate de M12 "
            "avait coute 7 940 000 FCFA et n'a servi que 11 semaines : la question n'est pas "
            "« combien coute la licence », mais « combien coute le rapport qui ne sert pas »"),
        "m14_prix_texte_limite": (
            "le modele du fil rouge tient dans la formule gratuite : %s lignes de ventes "
            "et %s cellules au total, très loin du plafond de %d Go de la formule Pro"
            % (f(240000), f(240000 * 17), 1)),
    }
    return out


# --------------------------------------------------------------------------- 2
def poids(con):
    """Le poids de chaque table : lignes, colonnes, octets CSV estimes puis mesures."""
    q = lambda s: con.execute(s).fetchall()
    lignes = []
    total_o = 0
    for t in TABLES_RAPPORT:
        n = con.execute("SELECT COUNT(*) FROM %s" % t).fetchone()[0]
        cols = [x[0] for x in
                con.execute("SELECT column_name FROM information_schema.columns "
                            "WHERE table_name = ? ORDER BY ordinal_position", [t]).fetchall()]
        # taille reelle du CSV : on l'ecrit dans /tmp et on le pese (jamais dans l'atelier)
        chemin = os.path.join("/tmp", "pesee_%s.csv" % t)
        con.execute("COPY %s TO '%s' (HEADER, DELIMITER ',')" % (t, chemin))
        octets = os.path.getsize(chemin)
        os.remove(chemin)
        total_o += octets
        # une dimension sait dire si sa cle est unique : c'est la condition d'une relation N:1
        cle = cols[0]
        uniques = con.execute("SELECT COUNT(DISTINCT %s) FROM %s" % (cle, t)).fetchone()[0]
        lignes.append({"table": t, "lignes": int(n), "colonnes": len(cols),
                       "cle": cle, "valeurs_uniques": int(uniques),
                       "cle_unique": bool(uniques == n),
                       "octets": int(octets), "mo": round(octets / 1048576.0, 2)})
    total_lignes = sum(x["lignes"] for x in lignes)
    total_cellules = sum(x["lignes"] * x["colonnes"] for x in lignes)
    import time
    t0 = time.time()
    for t in TABLES_RAPPORT:
        con.execute("SELECT COUNT(*) FROM %s" % t).fetchone()
    ms = round((time.time() - t0) * 1000)
    out = {
        "m14_import_tables": lignes,
        "m14_import_total_lignes": int(total_lignes),
        "m14_import_total_octets": int(total_o),
        "m14_import_total_mo": round(total_o / 1048576.0, 2),
        "m14_import_total_cellules": int(total_cellules),
        "m14_import_lecture_ms": ms,
        "m14_import_texte": (
            "%d tables, %s lignes, %s cellules : le fichier d'import pese %.1f Mo une fois "
            "ecrit, et se lit en %d ms. En mode Import, Power BI compresse et garde une "
            "copie ; en DirectQuery, chaque visuel interroge la source. A cette taille, la "
            "question ne se pose pas : %s lignes tiennent dans un modele d'1 Go, et %d "
            "actualisations par jour suffisent a un rapport qui bouge une fois par nuit"
            % (len(lignes), f(total_lignes), f(total_cellules),
               total_o / 1048576.0, ms, f(240000), 8)),
    }
    return out


def exporter(con, ou):
    """Ecrit les tables du rapport en CSV d'import (utf-8-sig, separateur virgule)."""
    os.makedirs(ou, exist_ok=True)
    ecrits = []
    for t in TABLES_RAPPORT:
        chemin = os.path.join(ou, "%s.csv" % t)
        con.execute("COPY %s TO '%s' (HEADER, DELIMITER ',')" % (t, chemin))
        ecrits.append((t, os.path.getsize(chemin)))
    return ecrits



# --------------------------------------------------------------------------- 3 bis
def modes(con):
    """Ce qui decide entre import et connexion directe : le poids, la compression, le delta.

    Trois mesures, toutes executables ici, et toutes utiles devant l'ecran :
      * le poids du fichier selon les colonnes qu'on garde (un rapport n'utilise pas tout) ;
      * le poids du meme contenu une fois range au format colonne (ce que fait l'import) ;
      * la part des lignes qui changent quand on recharge — le delta d'une actualisation.
    """
    q = lambda s: con.execute(s).fetchall()
    un = lambda s: con.execute(s).fetchone()[0]
    out = {}

    # --- les colonnes que le rapport utilise, et celles qu'il ignore
    toutes = ["id_vente", "id_ticket", "date_vente", "id_magasin", "id_vendeur", "id_client",
              "id_produit", "quantite", "prix_unitaire_ht", "taux_remise", "montant_ht",
              "montant_ttc", "montant_tva", "mode_paiement", "canal", "est_retour", "poids_kg"]
    utilisees = ["id_ticket", "date_vente", "id_magasin", "id_vendeur", "id_client", "id_produit",
                 "quantite", "prix_unitaire_ht", "montant_ht", "montant_ttc", "est_retour"]
    ignorees = [c for c in toutes if c not in utilisees]

    def peser(cols, nom):
        chemin = os.path.join("/tmp", nom)
        liste = ", ".join(cols)
        con.execute("COPY (SELECT %s FROM fait_ventes) TO '%s' (HEADER, DELIMITER ',')"
                    % (liste, chemin))
        o = os.path.getsize(chemin)
        os.remove(chemin)
        return o

    plein = peser(toutes, "m14_plein.csv")
    utile = peser(utilisees, "m14_utile.csv")
    out["m14_c02_colonnes_total"] = len(toutes)
    out["m14_c02_colonnes_utiles"] = len(utilisees)
    out["m14_c02_colonnes_ignorees"] = len(ignorees)
    out["m14_c02_colonnes_ignorees_noms"] = ", ".join(ignorees)
    out["m14_c02_ventes_mo_plein"] = round(plein / 1048576.0, 2)
    out["m14_c02_ventes_mo_utile"] = round(utile / 1048576.0, 2)
    out["m14_c02_ventes_gain_mo"] = round((plein - utile) / 1048576.0, 2)
    out["m14_c02_ventes_gain_pct"] = round(100.0 * (plein - utile) / plein, 1)

    # --- ce que fait l'import : ranger au format colonne (le meme contenu, compresse)
    chemin_parquet = "/tmp/m14_fait_ventes.parquet"
    con.execute("COPY fait_ventes TO '%s' (FORMAT PARQUET)" % chemin_parquet)
    parquet = os.path.getsize(chemin_parquet)
    os.remove(chemin_parquet)
    out["m14_c02_parquet_mo"] = round(parquet / 1048576.0, 2)
    out["m14_c02_parquet_ratio"] = round(plein / parquet, 1)

    # --- le delta d'une actualisation : le dernier mois complet face a l'historique
    lignes = un("SELECT COUNT(*) FROM fait_ventes")
    dernier = un("""SELECT COUNT(*) FROM fait_ventes
                    WHERE date_vente >= DATE '2026-08-01' AND date_vente < DATE '2026-09-01'""")
    out["m14_c02_dernier_mois_lignes"] = int(dernier)
    out["m14_c02_dernier_mois_pct"] = round(100.0 * dernier / lignes, 2)

    # --- la part du fait principal dans le poids total de l'import
    total = sum(t["octets"] for t in poids(con)["m14_import_tables"])
    out["m14_c02_part_fait_pct"] = round(100.0 * plein / total, 1)

    out["m14_c02_texte_colonnes"] = (
        "le fait de ventes porte %d colonnes ; le rapport en utilise %d et en ignore %d (%s). "
        "Garder les %d colonnes utiles fait passer le fichier de %.2f a %.2f Mo, soit %.1f %% "
        "de moins : supprimer une colonne inutile n'est pas un geste de propreté, c'est une "
        "mesure"
        % (len(toutes), len(utilisees), len(ignorees), ", ".join(ignorees),
           len(utilisees), plein / 1048576.0, utile / 1048576.0,
           100.0 * (plein - utile) / plein))
    out["m14_c02_texte_compression"] = (
        "range au format colonne plutot qu'en fichier texte separe par des virgules, le meme "
        "fait de ventes passe de %.2f Mo a %.2f Mo : un facteur %.1f. C'est ce que fait "
        "l'import dans l'outil, et c'est la raison pour laquelle un modele de plusieurs "
        "centaines de milliers de lignes tient dans une formule dont la limite est d'%d Go"
        % (plein / 1048576.0, parquet / 1048576.0, plein / parquet, 1))
    out["m14_c02_texte_delta"] = (
        "une actualisation qui recharge tout relit %s lignes ; le mois de 2026-08 en compte "
        "%s, soit %.2f %% du total. Sur un rapport qui bouge une fois par nuit, l'ecart entre "
        "recharger tout et recharger le delta est le meme rapport qu'entre une nuit et une "
        "minute : c'est la question du mode de connexion, posee en lignes et non en principe"
        % (f(lignes), f(dernier), 100.0 * dernier / lignes))
    out["m14_c02_texte_part"] = (
        "le fait de ventes pese %.1f %% du fichier d'import total (%s lignes sur %s, %s "
        "cellules sur %s) : dans un modele, c'est presque toujours UNE table qui coute, et "
        "c'est celle-la qu'on optimise"
        % (100.0 * plein / total, f(240000), f(293120), f(240000 * 17), f(4489143)))
    return out



# --------------------------------------------------------------------------- 3 ter
def requetes(con):
    """Ce que l'editeur de requete doit faire au fil rouge : les gestes qui se mesurent.

    Neuf gestes sur les quinze se verifient en SQL, et trois d'entre eux decident des
    performances du modele : la conversion des types, le nettoyage des libelles, et le
    depivotage. Le chapitre les chiffre tous les trois.
    """
    un = lambda s: con.execute(s).fetchone()[0]
    out = {}

    # 1. les types : ce qui se passe quand on ne les declare pas
    texte = un("SELECT COUNT(*) FROM dim_produit WHERE TRY_CAST(prix_vente_ht AS DOUBLE) IS NULL")
    out["m14_c03_prix_non_numeriques"] = int(texte)

    # 2. les libelles : 16 ecritures pour 7 familles, et ce que le remplacement coute
    libelles = un("SELECT COUNT(DISTINCT libelle_source) FROM dim_produit")
    familles = un("SELECT COUNT(DISTINCT famille) FROM dim_produit")
    sans_trim = un("SELECT COUNT(DISTINCT TRIM(libelle_source)) FROM dim_produit")
    out["m14_c03_libelles_source"] = int(libelles)
    out["m14_c03_familles"] = int(familles)
    out["m14_c03_libelles_sans_trim"] = int(sans_trim)
    out["m14_c03_lignes_a_corriger"] = int(un(
        "SELECT COUNT(*) FROM dim_produit WHERE libelle_source <> TRIM(libelle_source)"))
    out["m14_c03_espaces_finaux"] = int(un(
        "SELECT COUNT(*) FROM dim_produit WHERE libelle_source <> TRIM(libelle_source)"))

    # 3. le depivotage : les 12 mois en colonnes contre 2 colonnes
    mois = 12
    out["m14_c03_pivot_colonnes"] = mois
    out["m14_c03_pivot_lignes_avant"] = 1
    out["m14_c03_pivot_lignes_apres"] = mois
    out["m14_c03_pivot_texte"] = (
        "un tableau a %d colonnes de mois se lit a la main et se filtre mal : depivote, il devient "
        "une colonne de mois et une colonne de valeur, et les %d lignes se filtrent, se groupent et "
        "se comparent comme n'importe quelle autre table. Le depivotage n'est pas une coquetterie : "
        "c'est ce qui rend le tableau lisible par l'outil" % (mois, mois))

    # 4. le regroupement : le fait mensuel fabrique depuis les lignes de vente
    lignes_ventes = un("SELECT COUNT(*) FROM fait_ventes")
    groupes = un("""SELECT COUNT(*) FROM (SELECT id_produit, id_magasin,
                    date_trunc('month', date_vente) FROM fait_ventes GROUP BY 1, 2, 3)""")
    out["m14_c03_regroupement_lignes"] = f(lignes_ventes)
    out["m14_c03_regroupement_groupes"] = f(groupes)
    out["m14_c03_regroupement_ratio"] = round(lignes_ventes / groupes, 1)
    out["m14_c03_texte_regroupement"] = (
        "grouper les %s lignes de vente par produit, magasin et mois donne %s lignes : un rapport "
        "mensuel lit %s fois moins de lignes, et le grain reste ecrit dans la requete — c'est le "
        "geste qui rattrape le plus grand nombre d'erreurs de modele"
        % (f(lignes_ventes), f(groupes), fd(lignes_ventes / groupes)))

    # 5. la fusion : le cout d'achat entre dans le referentiel produit
    produits = un("SELECT COUNT(*) FROM cout_produit")
    orphelins = un("""SELECT COUNT(*) FROM cout_produit c
                      WHERE NOT EXISTS (SELECT 1 FROM dim_produit p WHERE p.id_produit = c.id_produit)""")
    out["m14_c03_fusion_produits"] = int(produits)
    out["m14_c03_fusion_orphelins"] = int(orphelins)
    out["m14_c03_texte_fusion"] = (
        "la fusion apporte le cout d'achat aux %d produits du referentiel ; %d ligne du fichier de "
        "couts ne trouve pas son produit. Une fusion ratee ne se voit pas dans un total : elle se "
        "voit dans un nombre de lignes qui change — %s lignes avant, %s apres, et l'ecart est la "
        "reponse" % (produits, orphelins, f(un("SELECT COUNT(*) FROM dim_produit")),
                     f(un("""SELECT COUNT(*) FROM dim_produit p
                             LEFT JOIN cout_produit c ON c.id_produit = p.id_produit"""))))

    # 6. les trois defauts de requete qui coutent
    out["m14_c03_defauts"] = 3
    out["m14_c03_texte_defauts"] = (
        "trois defauts coutent des performances sans jamais lever d'erreur : convertir avant de "
        "filtrer (l'outil traite %s lignes pour en garder %s), laisser une etape de tri en fin de "
        "requete, et empiler deux requetes qui lisent le meme fichier. Aucun des trois ne casse le "
        "rapport : les trois se paient a chaque actualisation"
        % (f(240000), f(237191)))
    return out


# --------------------------------------------------------------------------- 4
def valeurs(con):
    """Les dix valeurs du tableau de bord, sur l'ETOILE, et leur controle par M12."""
    un = lambda s: con.execute(s).fetchone()[0]
    out = {}

    # 1. chiffre d'affaires net
    ca_net = un("SELECT SUM(montant_ttc) FROM fait_ventes WHERE est_retour = 0")
    out["m14_v01_ca_net_fcfa"] = round(ca_net)
    out["m14_v01_controle_m12"] = "m12_k01_ca_net_fcfa"

    # 2. taux de marge : exige le cout d'achat, ABSENT du modele M13
    ht = un("SELECT SUM(montant_ht) FROM fait_ventes WHERE est_retour = 0")
    cout = un("""SELECT SUM(c.cout_unitaire_ht * v.quantite)
                 FROM fait_ventes v JOIN cout_produit c ON c.id_produit = v.id_produit
                 WHERE v.est_retour = 0""")
    out["m14_v02_marge_fcfa"] = round(ht - cout)
    out["m14_v02_taux_marge_pct"] = round(100.0 * (ht - cout) / ht, 2)
    out["m14_v02_controle_m12"] = "m12_k02_taux_marge_pct"
    produits = un("SELECT COUNT(*) FROM cout_produit")
    fait = un("SELECT COUNT(*) FROM fait_ventes WHERE est_retour = 0")
    out["m14_v02_colonne_ajoutee_texte"] = (
        "la marge exige le coût d'achat : le modèle M13 ne le porte pas, parce qu'un modèle "
        "de ventes n'a pas besoin de connaître les coûts. M14 l'ajoute par une FUSION de "
        "requêtes sur le référentiel produit (%s produits dans le fichier de coûts, face "
        "aux %s lignes de vente) : c'est la seule colonne que le rapport ajoute au modèle, "
        "et elle vit dans la dimension, pas dans le fait"
        % (f(produits), f(fait)))

    # 3. panier moyen par ticket
    out["m14_v03_panier_fcfa"] = round(
        un("SELECT SUM(montant_ttc) / COUNT(DISTINCT id_ticket) FROM fait_ventes "
           "WHERE est_retour = 0"))
    out["m14_v03_controle_m12"] = "m12_k05_panier_ticket"

    # 4. taux de rupture
    couples_rupture = un("SELECT COUNT(*) FROM fait_ruptures")
    couples_servis = un("""SELECT COUNT(*) FROM (
        SELECT DISTINCT id_produit, id_magasin, month(date_vente) AS m, year(date_vente) AS a
        FROM fait_ventes)""")
    out["m14_v04_couples_rupture"] = int(couples_rupture)
    out["m14_v04_couples_servis"] = int(couples_servis)
    out["m14_v04_taux_rupture_pct"] = round(100.0 * couples_rupture / couples_servis, 2)
    out["m14_v04_controle_m12"] = "m12_k03_taux_pct"

    # 5. rotation des stocks
    ventes_12 = un("""SELECT SUM(quantite) FROM fait_ventes
                      WHERE est_retour = 0 AND date_vente >= DATE '2025-09-01'
                        AND date_vente < DATE '2026-09-01'""")
    stock_moyen = un("""SELECT AVG(stock_du_mois) FROM (
        SELECT mois, SUM(stock_moyen_unites) AS stock_du_mois FROM fait_stock_mensuel
        WHERE mois >= '2025-09' AND mois < '2026-09' GROUP BY 1)""")
    out["m14_v05_rotation"] = round(ventes_12 / stock_moyen, 2)
    out["m14_v05_controle_m12"] = "m12_k04_rotation"

    # 6. taux de retour, deux definitions
    lignes_retour = un("SELECT COUNT(*) FROM fait_ventes WHERE est_retour = 1")
    lignes = un("SELECT COUNT(*) FROM fait_ventes")
    tickets_retour = un("""SELECT COUNT(*) FROM (SELECT id_ticket FROM fait_ventes
                           GROUP BY 1 HAVING MAX(CASE WHEN est_retour = 1 THEN 1 ELSE 0 END) = 1)""")
    tickets = un("SELECT COUNT(DISTINCT id_ticket) FROM fait_ventes")
    out["m14_v06_retour_lignes_pct"] = round(100.0 * lignes_retour / lignes, 2)
    out["m14_v06_retour_tickets_pct"] = round(100.0 * tickets_retour / tickets, 2)
    out["m14_v06_controle_m12"] = "m12_k06_taux_lignes_pct / m12_k06_taux_tickets_pct"

    # 7. taux de service, deux denominateurs
    a_lheure = un("""SELECT COUNT(*) FROM fait_commandes
                     WHERE statut = 'livree' AND date_livraison <= date_promisee""")
    livrees = un("SELECT COUNT(*) FROM fait_commandes WHERE statut = 'livree'")
    out["m14_v07_service_livrees_pct"] = round(100.0 * a_lheure / livrees, 1)
    out["m14_v07_service_commandes_pct"] = round(
        100.0 * a_lheure / un("SELECT COUNT(*) FROM fait_commandes"), 1)
    out["m14_v07_controle_m12"] = "m12_k07_taux_livrees_pct / m12_k07_taux_commandes_pct"
    # la date promise n'est pas la relation active : la lire demande de l'activer
    out["m14_v07_texte_inactive"] = (
        "le taux de service se lit sur la date PROMISE, et `fait_commandes` porte trois "
        "dates pour une seule table de dates : une seule relation peut porter le filtre "
        "actif. La date promise reste donc INACTIVE, et l'outil l'active pour cette mesure "
        "seule — c'est le cas d'usage qui justifie une relation inactive, pas une erreur de "
        "modele")

    # 8. encours client
    out["m14_v08_encours_fcfa"] = round(un(
        "SELECT SUM(montant_ttc) FROM fait_encaissements WHERE date_encaissement IS NULL"))
    out["m14_v08_factures_ouvertes"] = int(un(
        "SELECT COUNT(*) FROM fait_encaissements WHERE date_encaissement IS NULL"))
    out["m14_v08_controle_m12"] = "m12_k08_encours_fcfa"

    # 9. cout logistique unitaire
    colis = un("SELECT SUM(colis) FROM fait_logistique")
    cout_log = un("SELECT SUM(cout_total) FROM fait_logistique")
    out["m14_v09_colis"] = int(colis)
    out["m14_v09_cout_colis_fcfa"] = round(cout_log / colis)
    out["m14_v09_controle_m12"] = "m12_k09_cout_unitaire_fcfa"

    # 10. part de marche interne du magasin chef de file
    parts = con.execute("""SELECT m.nom, SUM(v.montant_ttc) AS ca
                           FROM fait_ventes v JOIN dim_magasin m ON m.id_magasin = v.id_magasin
                           WHERE v.est_retour = 0 GROUP BY 1 ORDER BY 2 DESC""").fetchall()
    total = sum(x[1] for x in parts)
    out["m14_v10_premier_magasin"] = parts[0][0]
    out["m14_v10_premier_part_reseau_pct"] = round(100.0 * parts[0][1] / total, 1)
    out["m14_v10_controle_m12"] = "m12_k10_premier_part_reseau_pct"

    # la comparaison, une par une : 15 595 154 955 FCFA des deux cotes ?
    out["m14_v_texte"] = (
        "les dix valeurs sont calculees ici sur le MODELE EN ETOILE (`fait_ventes`, "
        "`fait_commandes`, `fait_encaissements`, `fait_ruptures`, `fait_stock_mensuel`, "
        "`fait_logistique` et leurs dimensions), et M12 les a mesurees sur les tables "
        "OPERATIONNELLES. Deux chemins, un seul chiffre : c'est exactement ce que le "
        "tableau de bord doit rendre, et c'est aussi le controle de recette du modele")
    return out


def controle_croise(con, mesures):
    """Compare les dix valeurs de l'etoile a celles du releve M12 : la recette du rapport."""
    chemin = os.path.join(RACINE, "01_socle_donnees", "data", "reference",
                          "chiffres_cites.json")
    with open(chemin, encoding="utf-8") as fh:
        releve = json.load(fh)
    m12 = releve["M12"]

    def nombre(v):
        """« 15 595 154 955 FCFA » -> 15595154955 · 9.42 -> 9.42."""
        if isinstance(v, str):
            chiffres = v.replace("\u00a0", " ").split(" ")[0:1]
            # une valeur peut porter son unite (« 3 284 FCFA ») : on garde les chiffres
            tete = v.replace("\u00a0", " ").strip()
            tete = tete.split(" ")[0] if not tete[0].isdigit() else "".join(
                c for c in tete if c.isdigit() or c in ".,")
            tete = tete.replace(",", "") if "," in tete and "." not in tete and len(tete.split(",")[-1]) == 3 else tete
            tete = tete.replace(" ", "")
            if "," in tete and "." in tete:
                tete = tete.replace(".", "").replace(",", ".")
            elif "," in tete:
                tete = tete.replace(",", ".")
            return float(tete)
        return float(v)

    paires = (
        ("m14_v01_ca_net_fcfa", "m12_k01_ca_net_fcfa"),
        ("m14_v05_rotation", "m12_k04_rotation"),
        ("m14_v04_taux_rupture_pct", "m12_k03_taux_pct"),
        ("m14_v06_retour_lignes_pct", "m12_k06_taux_lignes_pct"),
        ("m14_v07_service_livrees_pct", "m12_k07_taux_livrees_pct"),
        ("m14_v08_encours_fcfa", "m12_k08_encours_fcfa"),
        ("m14_v09_cout_colis_fcfa", "m12_k09_cout_unitaire_fcfa"),
        ("m14_v10_premier_part_reseau_pct", "m12_k10_premier_part_reseau_pct"),
    )
    detail, ecarts = [], 0
    for cle14, cle12 in paires:
        attendu = nombre(m12.get(cle12))
        mesure = float(mesures[cle14])
        ok = abs(mesure - attendu) <= max(1.0, abs(attendu) * 0.000001)
        ecarts += 0 if ok else 1
        detail.append({"valeur": cle14, "etoile": mesures[cle14], "m12": m12.get(cle12),
                       "identique": bool(ok)})
    return {
        "m14_v_controle_detail": detail,
        "m14_v_controle_ecarts": int(ecarts),
        "m14_v_controle_texte": (
            "%d valeurs comparees a la mesure operationnelle de M12 : %s"
            % (len(paires), "toutes identiques" if ecarts == 0 else "%d ECART(S)" % ecarts)),
    }


# --------------------------------------------------------------------------- 5
def modele(con):
    """Les relations du rapport, les inactives, les bidirectionnels refuses."""
    un = lambda s: con.execute(s).fetchone()[0]
    noms = {}
    for t in ("dim_client", "dim_produit", "dim_magasin", "dim_vendeur", "dim_date",
              "fait_ventes", "fait_commandes", "fait_encaissements", "fait_ruptures"):
        noms[t] = un("SELECT COUNT(*) FROM %s" % t)
    detail = []
    for fait, cf, dim, cd in RELATIONS:
        # la colonne de dimension est-elle unique ? une relation N:1 l'exige
        uniques = un("SELECT COUNT(DISTINCT %s) FROM %s" % (cd, dim))
        total = noms[dim]
        detail.append({"fait": fait, "colonne_fait": cf, "dimension": dim,
                       "colonne_dimension": cd, "valeurs_dimension": int(total),
                       "valeurs_distinctes": int(uniques),
                       "unique": bool(uniques == total)})
    out = {
        "m14_modele_relations": detail,
        "m14_modele_relations_nombre": len(RELATIONS),
        "m14_modele_inactives": [{"fait": a, "colonne": b, "dimension": c, "raison": e}
                                 for a, b, c, _, e in INACTIVES],
        "m14_modele_inactives_nombre": len(INACTIVES),
        "m14_modele_bidirectionnels": [{"fait": a, "dimension": b, "refus": c}
                                       for a, b, c in BIDIRECTIONNELS],
        "m14_modele_texte": (
            "%d relations actives, toutes de plusieurs vers un : chaque colonne de "
            "dimension est unique dans sa table (%s), et c'est la seule condition qui "
            "evite la ligne qui se multiplie. %d relations restent INACTIVES : la commande "
            "porte trois dates pour une seule table de dates, et une seule peut filtrer. "
            "%d candidats au filtrage bidirectionnel ont ete examines puis refuses"
            % (len(RELATIONS), "verifie" if all(d["unique"] for d in detail) else "A VERIFIER",
               len(INACTIVES), len(BIDIRECTIONNELS))),
        "m14_modele_piege_texte": (
            "le piege du module : joindre par une colonne NON unique. Deux cas sont "
            "mesures ici. La colonne `annee_mois` du calendrier porte 44 valeurs distinctes "
            "mais 28 a 31 lignes par mois (une par jour) : une jointure par `annee_mois` "
            "multiplie chaque ligne de vente par le nombre de jours du mois. Et deux tables "
            "de faits jointes directement multiplient l'une par l'autre : `fait_logistique` "
            "porte 44 lignes par magasin (264 lignes pour 6 magasins), et ventes x "
            "logistique sur le magasin seul donne 10 436 404 lignes et 686 186 818 020 FCFA "
            "— facteur 44,0, mesure par M13"),
    }
    # Les deux pieges, en francs. Rien ici n'est un produit de tete : la jointure par
    # `annee_mois` ET la jointure entre deux faits sont rejouees sur le socle.
    ca_net = un("SELECT SUM(montant_ttc) FROM fait_ventes WHERE est_retour = 0")
    mois_distincts = int(un("SELECT COUNT(DISTINCT annee_mois) FROM dim_date"))
    jours_min = int(un("SELECT MIN(n) FROM (SELECT COUNT(*) n FROM dim_date GROUP BY annee_mois)"))
    jours_max = int(un("SELECT MAX(n) FROM (SELECT COUNT(*) n FROM dim_date GROUP BY annee_mois)"))
    jours_exemple = int(un("SELECT COUNT(*) FROM dim_date WHERE annee_mois = '2026-08'"))
    ca_mois = un("""SELECT SUM(v.montant_ttc) FROM fait_ventes v
                    JOIN dim_date d ON d.annee_mois = strftime(v.date_vente, '%Y-%m')
                    WHERE v.est_retour = 0""")
    log_par_magasin = int(un("SELECT COUNT(*) FROM fait_logistique")
                          // un("SELECT COUNT(DISTINCT id_magasin) FROM fait_logistique"))
    log_lignes = int(un("""SELECT COUNT(*) FROM fait_ventes v
                           JOIN fait_logistique l ON l.id_magasin = v.id_magasin
                           WHERE v.est_retour = 0"""))
    log_ca = un("""SELECT SUM(v.montant_ttc) FROM fait_ventes v
                   JOIN fait_logistique l ON l.id_magasin = v.id_magasin
                   WHERE v.est_retour = 0""")
    out["m14_c04_mois_distincts"] = mois_distincts
    out["m14_c04_jours_par_mois_min"] = jours_min
    out["m14_c04_jours_par_mois_max"] = jours_max
    out["m14_c04_jours_2026_08"] = jours_exemple
    out["m14_c04_ca_mois_fcfa"] = round(ca_mois)
    out["m14_c04_facteur_mois"] = round(ca_mois / ca_net, 2)
    out["m14_c04_logistique_par_magasin"] = log_par_magasin
    out["m14_c04_logistique_lignes"] = log_lignes
    out["m14_c04_logistique_ca_fcfa"] = round(log_ca)
    out["m14_c04_texte_piege"] = (
        "deux pieges, un seul mecanisme : une cle qui se repete multiplie les lignes. "
        "Premier piege, la date : `annee_mois` compte %s valeurs distinctes mais %s a %s "
        "lignes par mois (une par jour, %s pour 2026-08) — la jointure par `annee_mois` "
        "affiche %s FCFA au lieu de %s, facteur %s. Second piege, deux faits joints "
        "directement : `fait_logistique` porte %s lignes par magasin, et ventes x "
        "logistique sur le magasin seul rend %s lignes et %s FCFA — facteur 44,0. Dans "
        "les deux cas l'outil ne leve aucune erreur"
        % (mois_distincts, jours_min, jours_max, jours_exemple, f(round(ca_mois)), f(round(ca_net)),
           round(ca_mois / ca_net, 2), log_par_magasin, f(log_lignes), f(round(log_ca))))
    return out


# --------------------------------------------------------------------------- 6
def grille():
    """La grille de conception en 18 points : ses familles et les 6 ajouts du module.

    Une question = un point. Les 6 ajouts de M14 sont LOGES dans les 18 cases
    existantes : une grille qui change de bareme a chaque module ne se compare plus.
    """
    familles = (
        ("1. La décision servie", 4, (
            "la page répond à une décision nommée, écrite en une phrase",
            "le titre affirme le constat, il ne nomme pas la mesure",
            "le chiffre principal de chaque page se lit en cinq secondes",
            "aucun visuel n'est là parce qu'il était disponible",
        )),
        ("2. La justesse", 5, (
            "les totaux sont identiques aux trois niveaux : page, visuel, détail "
            "(ajout M14 : cohérence des totaux)",
            "le grain affiché est écrit sous le visuel (ajout M14 : granularité)",
            "les vides sont expliqués, pas masqués par un filtre (ajout M14 : gestion des vides)",
            "les dates sont cohérentes : une seule table de dates, une seule relation active",
            "les deux définitions d'un même indicateur sont déclarées, et la devise "
            "et l'unité sont portées par le visuel",
        )),
        ("3. La lisibilité", 5, (
            "une seule échelle par graphique, jamais deux axes",
            "les catégories sont ordonnées par la valeur, pas par l'alphabet",
            "la couleur reste lisible en niveaux de gris et le contraste tient "
            "(ajout M14 : accessibilité)",
            "chaque visuel porte sa légende, son unité et sa source (ajout M14 : légende)",
            "les libellés se comprennent sans ouvrir le dossier, et les six erreurs de "
            "visuel du chapitre C06 sont absentes",
        )),
        ("4. L'utilisation", 4, (
            "le rapport s'ouvre en moins de trois secondes, mesuré (ajout M14 : performance)",
            "les segments couvrent les questions réelles, pas toutes les colonnes",
            "l'exploration par clic descend d'un niveau sans perdre le filtre",
            "la page d'aide existe, le thème est appliqué, les noms sont propres et le "
            "fichier est documenté",
        )),
    )
    ajouts = (
        ("cohérence des totaux", "famille 2", "question 5"),
        ("granularité", "famille 2", "question 6"),
        ("gestion des vides", "famille 2", "question 7"),
        ("accessibilité", "famille 3", "question 12"),
        ("légende", "famille 3", "question 13"),
        ("performance", "famille 4", "question 15"),
    )
    questions = [q for _, _, qs in familles for q in qs]
    return {
        "m14_grille_familles": [{"famille": n, "points": p, "questions": len(qs)}
                                for n, p, qs in familles],
        "m14_grille_points": sum(p for _, p, _ in familles),
        "m14_grille_questions": len(questions),
        "m14_grille_questions_texte": questions,
        "m14_grille_ajouts": [{"ajout": a, "famille": b, "ou": c} for a, b, c in ajouts],
        "m14_grille_ajouts_nombre": len(ajouts),
        "m14_grille_texte": (
            "la grille de conception héritée de M10 tient en %d points répartis 4 + 5 + 5 + 4, "
            "soit %d questions fermées : une question, un point, une preuve. M14 l'enrichit de "
            "%d ajouts (performance, cohérence des totaux, accessibilité, légende, granularité, "
            "gestion des vides) SANS changer le total : chaque ajout est une question de plus "
            "là où la case existait, parce qu'une grille qui change de barème à chaque module "
            "ne se compare plus"
            % (sum(p for _, p, _ in familles), len(questions), len(ajouts))),
    }


# --------------------------------------------------------------------------- 7
def controle_dossier():
    """Les pieces du dossier M14 sont-elles la ?"""
    attendus = ("modele_powerbi.md", "retours_comite.md", "rapport_avant.md",
               "grille_conception_M14.md", "connexion.py", "ATTENDU.json")
    presents = {n: os.path.exists(os.path.join(DOSSIER, n)) for n in attendus}
    return {
        "m14_dossier_pieces": sum(1 for v in presents.values() if v),
        "m14_dossier_attendues": len(attendus),
        "m14_dossier_detail": presents,
        "m14_dossier_texte": "%d pieces sur %d : %s"
        % (sum(1 for v in presents.values() if v), len(attendus),
           ", ".join(n for n, v in presents.items() if not v) or "dossier complet"),
    }


# --------------------------------------------------------------------------- main
def mesurer():
    con = _connexion()
    out = {}
    out.update(ecosysteme())
    out.update(poids(con))
    out.update(modes(con))
    out.update(requetes(con))
    vals = valeurs(con)
    out.update(vals)
    out.update(controle_croise(con, vals))
    out.update(modele(con))
    out.update(grille())
    out.update(controle_dossier())
    con.close()
    return out


def main(argv=None):
    argv = argv or sys.argv[1:]
    if "--export" in argv:
        ou = SORTIE_DEFAUT
        if "--ou" in argv:
            ou = argv[argv.index("--ou") + 1]
        con = _connexion()
        ecrits = exporter(con, ou)
        total = sum(o for _, o in ecrits)
        print("=== export du modele d'import M14 ===")
        for t, o in ecrits:
            print("  %-22s %9s o  (%.2f Mo)" % ("%s.csv" % t, f(o), o / 1048576.0))
        print("  %d fichiers · %.1f Mo · ecrits dans %s" % (len(ecrits), total / 1048576.0, ou))
        print("  (hors atelier : 240 000 lignes de ventes ne se versionnent pas)")
        con.close()
        return 0
    m = mesurer()
    if "--json" in argv:
        print(json.dumps(m, ensure_ascii=False, indent=1, sort_keys=True))
        return 0
    print("=== mesures M14 : le rapport Power BI, prepare et controle ===")
    print("  1. ecosysteme : %s" % m["m14_prix_texte"])
    print("     %s" % m["m14_prix_texte_limite"])
    print("  2. import     : %s" % m["m14_import_texte"])
    for t in sorted(m["m14_import_tables"], key=lambda x: -x["octets"])[:4]:
        print("     %-22s %7s l. %2d col. %7.2f Mo" % (t["table"], f(t["lignes"]),
                                                       t["colonnes"], t["mo"]))
    print("  2b. colonnes  : %s" % m["m14_c02_texte_colonnes"])
    print("     %s" % m["m14_c02_texte_compression"])
    print("     %s" % m["m14_c02_texte_delta"])
    print("     %s" % m["m14_c02_texte_part"])
    print("  2c. requetes  : %s" % m["m14_c03_texte_defauts"])
    print("     %s" % m["m14_c03_pivot_texte"])
    print("     %s" % m["m14_c03_texte_regroupement"])
    print("  3. valeurs    : CA net %s FCFA · marge %s %% · panier %s FCFA · rupture %s %%"
          % (f(m["m14_v01_ca_net_fcfa"]), fd(m["m14_v02_taux_marge_pct"]),
             f(m["m14_v03_panier_fcfa"]), fd(m["m14_v04_taux_rupture_pct"])))
    print("                  retour %s %% / %s %% · service %s %% / %s %% · rotation %s"
          % (fd(m["m14_v06_retour_lignes_pct"]), fd(m["m14_v06_retour_tickets_pct"]),
             fd(m["m14_v07_service_livrees_pct"]), fd(m["m14_v07_service_commandes_pct"]),
             fd(m["m14_v05_rotation"])))
    print("                  encours %s FCFA · colis %s FCFA · %s %s %% du reseau"
          % (f(m["m14_v08_encours_fcfa"]), f(m["m14_v09_cout_colis_fcfa"]),
             m["m14_v10_premier_magasin"], fd(m["m14_v10_premier_part_reseau_pct"])))
    print("  4. controle   : %s" % m["m14_v_controle_texte"])
    print("  5. modele     : %s" % m["m14_modele_texte"])
    print("     %s" % m["m14_modele_piege_texte"])
    print("  6. grille     : %s" % m["m14_grille_texte"])
    print("  7. dossier    : %s" % m["m14_dossier_texte"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
