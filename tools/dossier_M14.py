#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dossier_M14.py — le dossier de l'apprenant pour le module M14.

Sept pieces, toutes regenerables :

  * `modele_powerbi.md`       — ce qu'il faut CONSTRUIRE dans l'outil : les 12 relations,
                                les 15 gestes de Power Query, les 10 mesures avec leur code,
                                les 3 pages et les 14 visuels, les 4 signets ;
  * `retours_comite.md`       — les 11 retours du comite d'utilisateurs (projet P2) ;
  * `rapport_avant.md`        — les 8 pages du rapport que le client ne comprend pas
                                (etude de cas) ;
  * `grille_conception_M14.md`— la grille en 18 points, ses 4 familles et les 6 ajouts ;
  * `connexion.py`            — ouvrir le socle depuis le dossier M14 (3 `dirname`) ;
  * `ATTENDU.json`            — les 10 valeurs du rapport et les compteurs du module,
                                mesures par `tools/mesures_M14.py` ;
  * `modele_import/LISEZ_MOI.md` — comment regenerer les CSV d'import (hors atelier).

Les CSV d'import eux-memes ne sont PAS versionnes : 12 tables et 29,3 Mo, dont 240 000
lignes de ventes. Ils se regenerent en une commande, et l'atelier vit sous quota.

Usage :
    python3 tools/dossier_M14.py            # ecrit le dossier et publie ce qu'il a ecrit
    python3 tools/dossier_M14.py --verifier # controle seulement, n'ecrit rien
"""
from __future__ import annotations

import json
import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOSSIER = os.path.join(RACINE, "03_exercices", "dossier_M14")

# --------------------------------------------------------------------------- donnees
# Les 12 relations du rapport : (fait, colonne, dimension, colonne, cardinalite, sens).
RELATIONS = (
    ("fait_ventes", "id_magasin", "dim_magasin", "id_magasin", "plusieurs à un", "dimension vers le fait"),
    ("fait_ventes", "id_produit", "dim_produit", "id_produit", "plusieurs à un", "dimension vers le fait"),
    ("fait_ventes", "id_client", "dim_client", "id_client", "plusieurs à un", "dimension vers le fait"),
    ("fait_ventes", "id_vendeur", "dim_vendeur", "id_vendeur", "plusieurs à un", "dimension vers le fait"),
    ("fait_ventes", "date_vente", "dim_date", "date", "plusieurs à un", "dimension vers le fait"),
    ("fait_commandes", "id_magasin", "dim_magasin", "id_magasin", "plusieurs à un", "dimension vers le fait"),
    ("fait_commandes", "id_client", "dim_client", "id_client", "plusieurs à un", "dimension vers le fait"),
    ("fait_commandes", "date_commande", "dim_date", "date", "plusieurs à un", "dimension vers le fait"),
    ("fait_encaissements", "id_client", "dim_client", "id_client", "plusieurs à un", "dimension vers le fait"),
    ("fait_encaissements", "date_facture", "dim_date", "date", "plusieurs à un", "dimension vers le fait"),
    ("fait_ruptures", "id_produit", "dim_produit", "id_produit", "plusieurs à un", "dimension vers le fait"),
    ("fait_ruptures", "id_magasin", "dim_magasin", "id_magasin", "plusieurs à un", "dimension vers le fait"),
)

INACTIVES = (
    ("fait_commandes", "date_promisee", "dim_date", "date",
     "la date promise : elle sert au taux de service, et s'active dans la mesure, jamais "
     "dans le filtre du rapport"),
    ("fait_commandes", "date_livraison", "dim_date", "date",
     "la date de livraison : candidate naturelle, mais le rapport se lit par date de "
     "commande — la livraison est une information de suivi"),
)

# Les 15 gestes de Power Query, sur les donnees du fil rouge.
GESTES = (
    ("1", "Source", "CSV", "ouvrir le fichier, délimiteur virgule, encodage UTF-8 avec BOM"),
    ("2", "Promouvoir les en-têtes", "Table", "la première ligne devient le nom des colonnes"),
    ("3", "Modifier le type", "Type", "types explicites : entiers, décimaux, dates, texte"),
    ("4", "Remplacer les valeurs", "Valeur", "les libellés de familles écrits de quatre façons"),
    ("5", "Colonne conditionnelle", "Colonne", "le drapeau de retour et le canal de vente"),
    ("6", "Fractionner la colonne", "Colonne", "`annee_mois` devient une année et un mois"),
    ("7", "Colonne personnalisée", "Colonne", "`date_mois` = premier jour du mois, pour la table de dates"),
    ("8", "Supprimer les colonnes", "Colonne", "les colonnes techniques qui ne servent à aucune page"),
    ("9", "Renommer", "Colonne", "des noms lisibles : `montant_ttc`, pas `mt_ttc_calc_2`"),
    ("10", "Filtrer les lignes", "Ligne", "retirer les statuts annulés de la requête des commandes"),
    ("11", "Dépivoter les colonnes", "Colonne", "les douze mois en colonnes deviennent deux colonnes"),
    ("12", "Regrouper les lignes", "Ligne", "fabriquer le fait mensuel à partir des lignes de vente"),
    ("13", "Fusionner les requêtes", "Requête", "le coût d'achat entre dans le référentiel produit"),
    ("14", "Ajouter les requêtes", "Requête", "empiler deux extractions d'années successives"),
    ("15", "Paramètre et fonction", "Requête", "le chemin du dossier devient un paramètre, la requête une fonction"),
)

# Les 10 mesures du rapport : (nom, code DAX, ce qu'elle rend, la definition ecrite).
MESURES = (
    ("[CA net]", "CALCULATE(SUM(fait_ventes[montant_ttc]), fait_ventes[est_retour] = 0)",
     "le chiffre d'affaires hors retours",
     "somme des montants TTC des lignes de vente, retours exclus"),
    ("[CA HT]", "CALCULATE(SUM(fait_ventes[montant_ht]), fait_ventes[est_retour] = 0)",
     "le chiffre d'affaires hors taxes, retours exclus",
     "somme des montants HT, retours exclus : c'est le dénominateur de la marge"),
    ("[Coût HT]", "CALCULATE(SUMX(fait_ventes, fait_ventes[quantite] "
                  "* RELATED(dim_produit[cout_unitaire_ht])), fait_ventes[est_retour] = 0)",
     "le coût d'achat des marchandises vendues",
     "quantité vendue multipliée par le coût standard du produit, porté par la dimension"),
    ("[Marge brute]", "[CA HT] - [Coût HT]", "la marge en valeur",
     "chiffre d'affaires HT moins coût standard des marchandises vendues"),
    ("[Taux de marge %]", "DIVIDE([Marge brute], [CA HT])", "la marge en pourcentage",
     "marge brute divisée par le chiffre d'affaires HT : DIVIDE rend un vide au lieu d'une erreur"),
    ("[Panier moyen]", "DIVIDE([CA net], DISTINCTCOUNT(fait_ventes[id_ticket]))",
     "le panier moyen par ticket",
     "chiffre d'affaires net divisé par le nombre de tickets distincts — pas par le nombre de lignes"),
    ("[Taux de rupture %]", "DIVIDE(COUNTROWS(fait_ruptures), [Couples servis])",
     "la part des couples produit-magasin-mois en rupture",
     "couples servis ayant connu au moins un jour de rupture, sur les couples réellement servis"),
    ("[Taux de retour lignes %]",
     "DIVIDE(CALCULATE(COUNTROWS(fait_ventes), fait_ventes[est_retour] = 1), COUNTROWS(fait_ventes))",
     "la part des lignes de retour",
     "lignes de retour divisées par toutes les lignes : la mesure logistique du retour"),
    ("[Taux de service %]",
     "DIVIDE([Commandes à l'heure], CALCULATE(COUNTROWS(fait_commandes), "
     "fait_commandes[statut] = \"livree\"))",
     "la part des commandes livrées à la date promise",
     "commandes livrées au plus tard à la date promise, sur les commandes livrées"),
    ("[Encours client]", "CALCULATE(SUM(fait_encaissements[montant_ttc]), "
     "ISBLANK(fait_encaissements[date_encaissement]))",
     "le montant des factures non encaissées",
     "montant des factures dont la date d'encaissement est vide : l'encours ouvert"),
    ("[Coût logistique par colis]", "DIVIDE(SUM(fait_logistique[cout_total]), "
     "SUM(fait_logistique[colis]))",
     "le coût moyen d'un colis",
     "coût logistique total divisé par le nombre de colis : l'unité est dans le nom"),
)

PAGES = (
    ("Direction", 5, ("carte du CA net", "jauge de l'objectif atteint",
                      "barres du CA par magasin, ordonnées", "courbe du CA mensuel",
                      "carte du taux de marge")),
    ("Commercial", 5, ("matrice magasin × famille", "barres du panier moyen par magasin",
                       "courbe des retours par mois", "segment des familles",
                       "carte du taux de retour")),
    ("Approvisionnement", 4, ("carte du taux de rupture", "barres des ruptures par famille",
                              "nuage couverture × rotation", "matrice des ruptures par magasin et mois")),
)

SIGNETS = (
    ("1", "Vue d'ensemble", "les quatre visuels de la page Direction, sans filtre de magasin"),
    ("2", "Focus magasin", "le même écran filtré sur le magasin choisi dans le segment"),
    ("3", "Détail produit", "l'exploration par clic ouverte depuis la matrice des familles"),
    ("4", "Aide à la lecture", "la page qui porte les définitions, les exclusions et la fraîcheur"),
)


def f(x):
    return "{:,}".format(int(round(float(x)))).replace(",", " ")


def _aeres(texte):
    """Une ligne vide entre les blocs (Markdown), jamais entre deux lignes de tableau."""
    sortie = []
    for ligne in texte.split("\n"):
        commence = ligne.startswith(("#", "**", ">", "- ", "1.", "2.", "3.", "4.", "5.", "6.",
                                     "7.", "8.", "9."))
        if (commence and sortie and sortie[-1] != "" and not sortie[-1].startswith("|")
                and not sortie[-1].startswith(("- ", "1.", "2.", "3.", "4.", "5.", "6.", "7.",
                                               "8.", "9."))):
            sortie.append("")
        sortie.append(ligne)
    return "\n".join(sortie)


def ecrire(nom, texte):
    chemin = os.path.join(DOSSIER, nom)
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    texte = _aeres(texte) if nom.endswith(".md") else texte
    with open(chemin, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(texte)
    return chemin, len(texte.encode("utf-8"))


def bloc_modele(m):
    l = []
    l.append("# M14 — Le modèle à construire dans Power BI\n")
    l.append("**Ce que vous montez, dans l'ordre.** Le modèle est celui de M13, importé tel quel : "
             "**12** tables du rapport, **12** relations actives, **2** relations inactives, "
             "**10** mesures, **3** pages et **14** visuels. Aucune capture d'écran : chaque geste "
             "est décrit par son libellé, son emplacement et son effet vérifiable.\n")
    l.append("**Déclaration d'exécution (§1.5).** Power BI Desktop n'est pas installé dans "
             "l'atelier : rien de ce document n'a été exécuté dans l'outil. Ce qui **est** mesuré, "
             "c'est ce que le rapport doit afficher : les **10** valeurs du fichier "
             "`ATTENDU.json`, calculées en SQL sur le modèle de M13.\n")
    l.append("## 1. Les 12 relations à déclarer\n")
    l.append("| # | Table de faits | Colonne | Dimension | Colonne | Cardinalité | Sens du filtre |\n")
    l.append("|---|---|---|---|---|---|---|\n")
    for i, (a, b, c, d, card, sens) in enumerate(RELATIONS, 1):
        l.append("| %d | `%s` | `%s` | `%s` | `%s` | %s | %s |\n" % (i, a, b, c, d, card, sens))
    par_nom = {t["table"]: t for t in m["m14_import_tables"]}
    preuves = " · ".join(
        "`%s` : %s valeurs distinctes de clé pour %s lignes" % (nom, f(par_nom[nom]["valeurs_uniques"]),
                                                          f(par_nom[nom]["lignes"]))
        for nom in ("dim_client", "dim_produit", "dim_magasin", "dim_vendeur", "dim_date"))
    l.append("\n**Ce que le contrôle dit de ces relations** : les **12** colonnes de dimension "
             "sont **uniques** dans leur table (%s). Une relation plusieurs à un n'a que cette "
             "condition à remplir, et elle suffit à garantir qu'aucune ligne ne se multiplie.\n"
             % preuves)
    l.append("## 2. Les 2 relations inactives, et pourquoi\n")
    l.append("| Table de faits | Colonne | Dimension | Raison |\n|---|---|---|---|\n")
    for a, b, c, d, raison in INACTIVES:
        l.append("| `%s` | `%s` | `%s` | %s |\n" % (a, b, c, raison))
    l.append("\n**La règle.** `fait_commandes` porte **trois** dates et il n'existe qu'**une** table "
             "de dates : une seule relation peut porter le filtre du rapport. Les deux autres "
             "restent **inactives** — elles existent, elles ne filtrent pas — et s'activent dans une "
             "mesure précise. Ce n'est pas un défaut : c'est la seule façon d'avoir trois temps "
             "dans un même fait.\n")
    l.append("\n**Le piège à ne pas commettre.** Ne reliez **jamais** un fait à la table de dates "
             "par une colonne non unique, comme `annee_mois` : elle apparaît **44** fois dans le "
             "calendrier (une fois par mois), le filtre se propage à ces **44** lignes, chaque ligne "
             "de vente se répète et le chiffre d'affaires est multiplié. C'est la faute que M13 a "
             "mesurée : un facteur **44,0** sur une jointure trop large.\n")
    l.append("## 3. Les 15 gestes de Power Query\n")
    l.append("| # | Geste | Porte sur | Ce qu'il fait sur le fil rouge |\n|---|---|---|---|\n")
    for num, geste, porte, quoi in GESTES:
        l.append("| %s | **%s** | %s | %s |\n" % (num, geste, porte, quoi))
    l.append("\n**Deux consignes de méthode.** (1) **Nommez chaque étape** : une étape laissée "
             "« Personnalisée1 » est une étape que personne ne pourra relire dans six mois. "
             "(2) **Une requête qui commence par un filtre** traite moins de lignes qu'une requête "
             "qui convertit tout avant de filtrer : l'ordre des étapes change le temps "
             "d'actualisation, pas seulement l'élégance.\n")
    l.append("## 4. Les 10 mesures, avec leur code\n")
    l.append("| Mesure | Code DAX | Ce qu'elle rend | Définition écrite |\n|---|---|---|---|\n")
    for nom, dax, quoi, definition in MESURES:
        l.append("| **%s** | `%s` | %s | %s |\n" % (nom, dax.replace("|", "\\|"), quoi, definition))
    l.append("\n**Trois avertissements, payés d'avance.**\n")
    l.append("1. **`DIVIDE` plutôt que `/`** : `DIVIDE` rend un vide au lieu d'une erreur quand le "
             "dénominateur est nul, et un rapport qui affiche des erreurs perd la confiance de son "
             "lecteur en une seconde.\n")
    l.append("2. **`RELATED` apparaît une fois** dans ce module, dans `[Coût HT]`, parce que le coût "
             "vit dans la dimension produit et pas dans le fait. M15 consacre un chapitre entier à "
             "ces fonctions d'itinéraire : ici, une seule ligne suffit.\n")
    l.append("3. **La part du réseau (Ouaga 2000 : %s %% des %s FCFA) s'affiche par un graphique**, "
             "pas par une mesure : un pourcentage du total demande `ALL`, qui est du ressort de M15. "
             "Un module qui enseigne `ALL` trop tôt fabrique des mesures que l'apprenant ne sait pas "
             "relire.\n"
             % (str(m["m14_v10_premier_part_reseau_pct"]).replace(".", ","),
                f(m["m14_v01_ca_net_fcfa"])))
    l.append("## 5. Les 3 pages et les 14 visuels\n")
    l.append("| Page | Visuels | Contenu |\n|---|---|---|\n")
    for nom, n, visuels in PAGES:
        l.append("| **%s** | %d | %s |\n" % (nom, n, " · ".join(visuels)))
    l.append("| **Détail** | 2 | détail magasin et détail produit, ouverts par exploration |\n")
    l.append("| **Aide** | 0 | aucune donnée : les définitions, les exclusions, la fraîcheur |\n")
    l.append("\n**Les 4 segments de la page Direction** : période, magasin, famille de produits, "
             "segment de client. Ils sont **synchronisés** avec les deux pages de détail, jamais avec "
             "la page d'aide.\n")
    l.append("\n## 6. Les 4 signets\n")
    l.append("| # | Signet | Ce qu'il montre |\n|---|---|---|\n")
    for num, nom, quoi in SIGNETS:
        l.append("| %s | **%s** | %s |\n" % (num, nom, quoi))
    l.append("\n## 7. La sécurité et l'actualisation, à documenter dans le dossier\n")
    l.append("- **Sécurité au niveau des lignes** : le retour n° **2** du comité (« je ne dois voir "
             "que mon magasin ») se traite par un rôle qui filtre `dim_magasin` sur l'utilisateur "
             "connecté — et par rien d'autre : un filtre posé dans chaque mesure se contourne en "
             "changeant de page. Le socle compte **%s** magasins, dont **1** dépôt sans vente.\n"
             % f([t for t in m["m14_import_tables"] if t["table"] == "dim_magasin"][0]["lignes"]))
    l.append("- **Actualisation planifiée** : fréquence, mode (Import), passerelle ou absence de "
             "passerelle, qui la surveille et qui prévient en cas d'échec. Un rapport qui se "
             "rafraîchit mal sans que personne ne le sache est pire qu'un rapport manuel.\n")
    l.append("- **Les 7 tests avant mise en production** : les totaux aux trois niveaux, le grain "
             "affiché, les vides expliqués, les dates cohérentes, les deux définitions d'un même "
             "indicateur, l'ouverture en moins de **3** secondes, et la relecture par un pair avec "
             "la grille en **18** points.\n")
    return "".join(l)


def bloc_retours():
    retours = (
        ("Le chiffre de la page Direction n'est pas celui de la page Commercial.",
         "Les deux pages ne lisent pas le même fait, ou l'une d'elles compte les retours.",
         "chercher la cause dans le MODÈLE : une relation, un filtre ou deux définitions"),
        ("Je ne devrais voir que mon magasin, pas ceux des autres.",
         "Le besoin est légitime et il se traite au bon endroit.",
         "rôle de sécurité au niveau des lignes sur la dimension des magasins"),
        ("Ajoutez le chiffre d'affaires par heure de la journée.",
         "La donnée n'existe pas : le fait de ventes porte une date, pas une heure.",
         "refus argumenté : une donnée absente ne s'invente pas, elle se collecte"),
        ("Mon équipe travaille en anglais.",
         "Les libellés d'un rapport se traduisent.",
         "traductions des textes du rapport, pas des noms de colonnes"),
        ("Les montants en dollars, personne ne les lit ici.",
         "La devise doit être portée par le visuel.",
         "format de devise en FCFA, et l'unité écrite dans le titre"),
        ("Mettez les douze indicateurs de la carte sur la première page.",
         "Douze visuels sur un écran, c'est douze messages que personne ne lit.",
         "refus partiel chiffré : cinq visuels sur la page, le reste en page de détail"),
        ("Envoyez-le en PDF chaque lundi matin.",
         "Un abonnement automatisé existe, à condition d'un espace de travail payant.",
         "abonnement au rapport, ou refus assumé et écrit"),
        ("Je veux le détail d'une vente en cliquant sur un magasin.",
         "L'exploration par clic descend d'un niveau en gardant le filtre.",
         "page de détail et exploration par clic"),
        ("Le total des retours est négatif, c'est une erreur.",
         "Les retours du socle portent une quantité négative : la convention existe, elle doit être écrite.",
         "définir et afficher la convention de signe"),
        ("Il met quarante secondes à s'ouvrir.",
         "Un rapport lent n'est pas utilisé, même juste.",
         "mesurer, trouver la cause (trop de visuels, colonne calculée, relation bidirectionnelle), corriger"),
        ("Je veux la couverture de stock en semaines, pas le taux de rupture.",
         "Une mesure nouvelle, une table du modèle qui n'est pas encore reliée.",
         "hors périmètre de M14 : c'est le travail de P2, et il exige une relation de plus"),
    )
    l = ["# M14 — Les 11 retours du comité d'utilisateurs\n",
         "**Le principe du projet P2.** Ces onze retours arrivent ensemble, dans le désordre, "
         "comme dans la vraie vie : certains sont contradictoires, un demande une donnée que "
         "l'entreprise ne produit pas, un autre veut tout voir sur un seul écran. Votre travail "
         "n'est pas de satisfaire tout le monde : c'est de **trier, prioriser, faire et refuser** "
         "en écrivant pourquoi.\n",
         "| # | Le retour, tel qu'il est dit | Ce qu'il cache | La bonne réponse à trouver |\n",
         "|---|---|---|---|\n"]
    for i, (dit, cache, reponse) in enumerate(retours, 1):
        l.append("| %d | « %s » | %s | %s |\n" % (i, dit, cache, reponse))
    l.append("\n**Ce que le barème attend de vous** : **3** refus au moins, chacun argumenté ; "
             "les retours contradictoires (le n° **6** contre la grille, le n° **1** contre le "
             "n° **9**) traités par une décision, pas par un compromis ; et une phrase finale qui "
             "dit ce que vous refusez de faire dans ce trimestre.\n")
    return "".join(l)


def bloc_avant(m):
    l = ["# M14 — Le rapport que le client ne comprend pas (étude de cas)\n",
         "**Le contexte.** Un consultant a livré ce rapport il y a trois mois. Il fonctionne : "
         "les chiffres sont justes, l'actualisation passe, rien ne plante. Le client l'a ouvert "
         "**quatre** fois le premier mois, puis plus. Son courriel tient en une ligne : « je ne "
         "comprends pas d'où sortent vos chiffres ». Vous avez **8** pages sous les yeux ; voici "
         "ce qu'elles contiennent, honnêtement décrites.\n"]
    pages = (
        ("P1", "Vue générale",
         "**12** visuels répartis sur l'écran, dont **3** graphiques à deux axes, une jauge sans "
         "cible, et deux cartes qui affichent le même indicateur calculé de deux façons différentes "
         "(**15 595 154 955** FCFA avec les retours, **15 419 985 157** FCFA sans). Aucun "
         "sous-titre ne dit laquelle est laquelle."),
        ("P2", "Détail par magasin",
         "un tableau de **6** lignes et **18** colonnes, sans tri, dont **4** colonnes de montants "
         "dont l'unité n'est écrite nulle part. Le total de la colonne ne correspond pas à la carte "
         "de la page P1."),
        ("P3", "Détail par produit",
         "**154** lignes, triées par ordre alphabétique, avec les **16** libellés de familles "
         "tels qu'ils sortent du fichier source — alors que le référentiel en compte **7**."),
        ("P4", "Tendances",
         "une courbe du chiffre d'affaires mensuel sur **44** mois, sans repère, dont le dernier "
         "point est un mois incomplet : la courbe « s'effondre » de **28,9 %** en fin de période."),
        ("P5", "Clients",
         "une carte de **23 913** clients, un camembert à **5** parts, et un classement des "
         "**10** premiers clients par chiffre d'affaires — sans dire si les retours sont déduits."),
        ("P6", "Ruptures",
         "un tableau de **2 428** lignes sans total, et un chiffre en rouge en haut à droite "
         "(**7,29 %**) que personne n'a expliqué."),
        ("P7", "Objectifs",
         "l'objectif du mois saisi à la main dans un classeur, collé dans un visuel texte. "
         "La somme annoncée est celle de **12** mois.\n"),
        ("P8", "Aide",
         "vide. Le titre est là, les définitions ne le sont pas."),
    )
    l.append("| Page | Titre | Ce qu'elle contient |\n|---|---|---|\n")
    for p, titre, quoi in pages:
        l.append("| **%s** | %s | %s |\n" % (p, titre, quoi))
    l.append("\n**Ce qui est vrai dans ce rapport.** Les chiffres de la carte P1 sont justes : ce "
             "sont deux définitions défendables du même indicateur, et **175 169 798** FCFA les "
             "séparent — l'écart exact des retours. Les **16** libellés de P3 sont ceux du fichier "
             "source : c'est le défaut que M13 a corrigé par un modèle, pas par une requête. La "
             "baisse de **28,9 %** de P4 est un effet de bord : le mois en cours est incomplet, et "
             "la comparaison honnête donne **+ 15,4 %**.\n")
    l.append("**Votre travail.**\n")
    l.append("1. Passez la **grille de conception en 18 points** sur les **8** pages, en gardant "
             "la **preuve** de chaque réponse (une phrase par point, pas une note).\n")
    l.append("2. Nommez les **trois** défauts qui expliquent le plus grand nombre d'incompréhensions, "
             "et dites pour chacun s'il se corrige dans le **modèle**, dans le **visuel** ou dans la "
             "**définition**.\n")
    l.append("3. Refaites la **page P1** : **5** visuels au maximum, chaque chiffre portant son "
             "unité, sa période et sa définition. Les trois valeurs à faire apparaître sont celles du "
             "fichier `ATTENDU.json`.\n")
    l.append("4. Écrivez la **page P8**, l'aide à la lecture, en **10** lignes : ce que chaque "
             "indicateur compte, ce qu'il exclut, et la fraîcheur de la donnée.\n")
    return "".join(l)


def bloc_grille(m):
    lignes = []
    for famille in m["m14_grille_familles"]:
        pass
    questions = m["m14_grille_questions_texte"]
    familles = m["m14_grille_familles"]
    l = ["# M14 — La grille de conception en 18 points (version enrichie)\n",
         "**Une question, un point, une preuve.** Chaque case se répond par oui ou non, et la "
         "réponse s'accompagne de sa preuve (« axe : zéro, oui, capture du visuel »). La grille "
         "servira **quatre** fois dans le parcours : M10 (première version), M14, M17 et M21. "
         "Elle se remplit **deux fois** ici : par vous, puis par un pair — et l'écart entre les "
         "deux totaux est votre premier indicateur de qualité.\n"]
    i = 0
    for fa in familles:
        l.append("## %s — %d points\n\n" % (fa["famille"], fa["points"]))
        for _ in range(fa["questions"]):
            l.append("%d. %s\n" % (i + 1, questions[i]))
            i += 1
        l.append("\n")
    l.append("## Les 6 ajouts du module, et où ils se logent\n")
    l.append("| Ajout | Famille | Où il entre |\n|---|---|---|\n")
    for a in m["m14_grille_ajouts"]:
        l.append("| %s | %s | %s |\n" % (a["ajout"], a["famille"], a["ou"]))
    l.append("\n**La règle de M14.** La grille s'**enrichit** sans changer de total : les six "
             "ajouts du module occupent des cases existantes, parce qu'une grille qui change de "
             "barème à chaque module ne se compare plus d'un projet à l'autre. Les **18** points se "
             "répartissent **4 / 5 / 5 / 4** : la décision servie, la justesse, la lisibilité, "
             "l'utilisation.\n")
    l.append("| Famille | Points | Ce qu'elle vérifie |\n|---|---|---|\n")
    l.append("| 1. La décision servie | 4 | la page répond à une décision nommée, et se lit en cinq secondes |\n")
    l.append("| 2. La justesse | 5 | les totaux, le grain, les vides, les dates, les définitions |\n")
    l.append("| 3. La lisibilité | 5 | l'échelle, l'ordre, la couleur, la légende, le vocabulaire |\n")
    l.append("| 4. L'utilisation | 4 | la performance, les segments, l'exploration, la page d'aide |\n")
    l.append("| **Total** | **18** | |\n")
    return "".join(l)


def bloc_connexion():
    return '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""connexion.py — ouvrir le socle depuis le dossier M14.

    import sys; sys.path.insert(0, '03_exercices/dossier_M14')
    from connexion import ouvrir
    con = ouvrir()

Le socle du module M14 est celui de M13 : M14 n'ajoute aucune table. Il n'ajoute qu'une
colonne, le cout d'achat, et cette colonne vit deja dans `cout_produit` (source M12) :
la FUSION de requetes de Power Query la fait entrer dans le referentiel produit.

Les fichiers d'import CSV ne sont pas versionnes (12 tables, 29,3 Mo) : ils se
regenere hors atelier par `python3 tools/mesures_M14.py --export`.
"""
from __future__ import annotations

import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def ouvrir(fautif=False):
    """Ouvre le socle M13 (donc M11, M12 et M13) et rend la connexion DuckDB."""
    sys.path.insert(0, os.path.join(RACINE, "03_exercices", "dossier_M13"))
    from connexion import ouvrir as ouvrir_m13
    return ouvrir_m13(fautif=fautif)


if __name__ == "__main__":
    c = ouvrir()
    print("modele M14 (celui de M13, plus le cout d'achat) :")
    print("  fait_ventes      :", c.execute("SELECT COUNT(*) FROM fait_ventes").fetchone()[0])
    print("  dim_produit      :", c.execute("SELECT COUNT(*) FROM dim_produit").fetchone()[0])
    print("  cout_produit     :", c.execute("SELECT COUNT(*) FROM cout_produit").fetchone()[0])
    sys.exit(0)
'''


def bloc_lisez_moi():
    return '''# Les fichiers d'import du rapport M14

**Ces fichiers ne sont pas versionnés.** Le dossier contient **12** tables et **29,3** Mo, dont
**240 000** lignes de ventes : l'atelier vit sous un quota de **128** Mo, et un fichier d'import se
régénère, il ne se stocke pas.

## Les produire

```bash
python3 tools/mesures_M14.py --export                  # écrit dans /tmp/m14_import
python3 tools/mesures_M14.py --export --ou chemin/dir  # écrit ailleurs
```

## Ce que vous obtenez

| Table | Nature | Ce qu'elle porte |
|---|---|---|
| `dim_client.csv` | dimension | **23 913** clients, **8** attributs |
| `dim_produit.csv` | dimension | **154** produits, **11** attributs |
| `dim_magasin.csv` | dimension | **6** points de vente, dont **1** dépôt sans vente |
| `dim_vendeur.csv` | dimension | **22** vendeurs |
| `dim_date.csv` | dimension de temps | **1 339** jours, **15** attributs |
| `fait_ventes.csv` | fait | **240 000** lignes au grain du ticket, **17** colonnes |
| `fait_commandes.csv` | fait | **9 000** commandes, **3** dates |
| `fait_encaissements.csv` | fait | **9 000** factures |
| `fait_ruptures.csv` | fait | **2 428** couples produit-magasin-mois |
| `fait_stock_mensuel.csv` | fait | **6 776** lignes produit-mois |
| `fait_objectifs.csv` | fait | **218** objectifs magasin-mois |
| `fait_logistique.csv` | fait | **264** lignes magasin-mois |

## Dans Power BI

`Accueil > Obtenir les données > Texte/CSV`, un fichier à la fois — ou
`Obtenir les données > Dossier` pour les importer d'un coup, et c'est l'occasion d'écrire le
**paramètre** de chemin du geste n° **15**.

Le format est prévu pour l'import : **UTF-8 avec BOM**, séparateur virgule, en-têtes sur la
première ligne, dates au format ISO. Les **2** prix manquants du référentiel produit
(identifiants `62` et `149`) sont **vides**, et c'est voulu : le module apprend à traiter un
manquant, pas à le masquer.

## La règle du dossier

Un rapport qui dépend d'un fichier doit **savoir d'où il vient**. Écrivez, dans la page d'aide
du rapport : le chemin source, la date de l'extraction, la personne qui la produit, et ce qui
se passe si elle manque.
'''


def main(argv=None):
    argv = argv or sys.argv[1:]
    sys.path.insert(0, os.path.join(RACINE, "tools"))
    import mesures_M14

    m = mesures_M14.mesurer()
    pieces = (
        ("modele_powerbi.md", bloc_modele(m)),
        ("retours_comite.md", bloc_retours()),
        ("rapport_avant.md", bloc_avant(m)),
        ("grille_conception_M14.md", bloc_grille(m)),
        ("connexion.py", bloc_connexion()),
        ("modele_import/LISEZ_MOI.md", bloc_lisez_moi()),
    )
    # les attendus du rapport, mesures par l'instrument
    attendu = {
        "genere_par": "tools/dossier_M14.py (mesures lues sur le socle M13)",
        "valeurs_du_rapport": {
            "ca_net_fcfa": m["m14_v01_ca_net_fcfa"],
            "taux_marge_pct": m["m14_v02_taux_marge_pct"],
            "panier_moyen_fcfa": m["m14_v03_panier_fcfa"],
            "taux_rupture_pct": m["m14_v04_taux_rupture_pct"],
            "rotation": m["m14_v05_rotation"],
            "retour_lignes_pct": m["m14_v06_retour_lignes_pct"],
            "retour_tickets_pct": m["m14_v06_retour_tickets_pct"],
            "service_livrees_pct": m["m14_v07_service_livrees_pct"],
            "service_commandes_pct": m["m14_v07_service_commandes_pct"],
            "encours_fcfa": m["m14_v08_encours_fcfa"],
            "cout_par_colis_fcfa": m["m14_v09_cout_colis_fcfa"],
            "premier_magasin_part_reseau_pct": m["m14_v10_premier_part_reseau_pct"],
        },
        "compteurs_du_module": {
            "relations_actives": m["m14_modele_relations_nombre"],
            "relations_inactives": m["m14_modele_inactives_nombre"],
            "mesures": len(MESURES),
            "pages": len(PAGES),
            "visuels": sum(n for _, n, _ in PAGES),
            "segments": 4,
            "signets": len(SIGNETS),
            "gestes_power_query": len(GESTES),
            "retours_comite": 11,
            "grille_points": m["m14_grille_points"],
            "grille_questions": m["m14_grille_questions"],
            "grille_ajouts": m["m14_grille_ajouts_nombre"],
            "tables_import": len(m["m14_import_tables"]),
            "lignes_import": m["m14_import_total_lignes"],
            "mo_import": m["m14_import_total_mo"],
        },
        "controle": m["m14_v_controle_texte"],
    }
    pieces = pieces + (("ATTENDU.json", json.dumps(attendu, ensure_ascii=False, indent=1,
                                                   sort_keys=True) + "\n"),)

    if "--verifier" in argv:
        for nom, _ in pieces:
            chemin = os.path.join(DOSSIER, nom)
            etat = "present" if os.path.exists(chemin) else "MANQUANT"
            print("  %-32s %s" % (nom, etat))
        return 0

    print("=== dossier M14 ===")
    for nom, texte in pieces:
        chemin, octets = ecrire(nom, texte)
        print("  %-32s %7s o" % (nom, "{:,}".format(octets).replace(",", " ")))
    print("  %d pieces · valeurs du rapport : %s" % (len(pieces), m["m14_v_controle_texte"]))
    print("  dossier : %s" % DOSSIER)
    return 0


if __name__ == "__main__":
    sys.exit(main())
