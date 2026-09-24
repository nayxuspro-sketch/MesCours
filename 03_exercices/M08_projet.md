# Projet M08.P — « Le script qui fait le travail de trois matinées »

**Module M08 · projet de fin de module · 2 h · barème /20, seuil de passage 13/20**

> **Le cadre réel.** Vous recevez le dossier `03_exercices/dossier_M08/` : 8 CSV
> réexportés de la base commerciale M07 (50 008 ventes sur 2025—2026, 1 200 clients,
> 380 produits, 5 magasins), dont un fichier **vide**. Personne ne les a encore regardés :
> ce que contient `vente.csv` (doublons ? retours ? dates ?) n'est connu que de
> l'`ATTENDU.json` — et de vos propres yeux. À vous d'écrire **un seul script commenté**,
> `analyse_commerciale.py`, qui, exécuté **d'une traite**, produit les 6 sections du projet
> : import, audit, nettoyage, indicateurs, 4 graphiques, classeur de synthèse. C'est la
> synthèse des huit chapitres (C01 l'environnement, C02 les types et les erreurs, C03 les
> boucles, C04 les conteneurs, C05 les fonctions et la lecture de traceback, C06 la
> vecteurisation, C07 la lecture et le filtrage, C08 le `groupby` en centimes et
> l'export Excel) — et la **croisée SQL/pandas** est la colonne vertébrale : chaque
> indicateur doit redonner, à 2 FCFA près, ce que M07 a requêté en SQL.

> **Note de cohérence.** Le dossier est réexporté de façon **déterministe** par
> `python3 tools/dossier_M08.py` (aucun tirage aléatoire, base M07 figée) : deux
> exécutions → diff = 0, empreinte dossier `b9a8d973119342ec…`.
> `03_exercices/dossier_M08/ATTENDU.json` contient le **côté SQL de la croisée**
> (25 clés `m08p_*` mesurées par DuckDB) : vous n'y recourez qu'**après** avoir produit
> vos propres nombres, pour comparer, pas pour copier. Le script du chapitre, exécuté
> d'une traite le 19/09/2026, est commité dans le dépôt :
> `03_exercices/dossier_M08/analyse_commerciale_modele.py` — les sorties publiées ci-dessous
> sont **ses** sorties, pas un exemple illustratif.

---

## 1. Énoncé

### Le matériel

| Élément | Chemin | Ce que c'est |
|---|---|---|
| Dossier de travail | `03_exercices/dossier_M08/` | 8 CSV : `vente.csv` (50 008 lignes × 13 colonnes, **4 défauts** : 8 doublons, 208 retours bruts / 200 dédoublonnés, 21 406 dates sous la condition naïve + 15 deadlines aberrantes, 0 manquant), `client.csv` (1 200), `produit.csv` (380), `categorie.csv` (8), `magasin.csv` (5), `mode_paiement.csv` (5), `regle_tva.csv` (2), `objectif_magasin.csv` (**0 ligne**) |
| Brief | `03_exercices/dossier_M08/00_brief.md` | le brief remis à l'apprenant (ce qu'on attend, rien de plus) |
| Résultats attendus | `03_exercices/dossier_M08/ATTENDU.json` | le côté SQL de la croisée (25 clés `m08p_*` : formes, audit, indicateurs, totaux en float DuckDB) |
| Script modèle | `03_exercices/dossier_M08/analyse_commerciale_modele.py` | le script du chapitre (corrigé de référence, exécuté le 19/09/2026) |

### Les 6 sections, et ce qu'elles notent

| # | Section | Ce que ça mobilise | Livrable |
|---|---|---|---|
| S1 | Import des 8 CSV avec contrôle des formes | C07 `read_csv` | dictionnaire nom → lignes, imprimé |
| S2 | Audit : doublons, retours brut/net, dates inversées, deadlines aberrantes, manquants, table vide — avec la **méthode** qui les a trouvés | C02, C03, C07 | rapport imprimé, les 4 défauts chiffrés **avec leur définition exacte** |
| S3 | Nettoyage : dédoublonnage (12 colonnes métier), exclusion des retours des indicateurs | C07, C08 | le DataFrame propre (49 800 lignes) |
| S4 | Indicateurs en centimes : CA brut / CA propre / panier moyen / CA par magasin / par catégorie / plus gros mois | C06, C08 | les 6 indicateurs, addition **en centimes entiers** |
| S5 | Les 4 graphiques (`matplotlib`, backend `Agg`) : CA mensuel, CA par magasin, répartition par catégorie, histogramme des montants | C06, C08 | 4 fichiers PNG |
| S6 | Export du classeur `synthese_commerciale.xlsx` : 4 feuilles nommées (`audit`, `indicateurs`, `par_magasin`, `par_mois`) | C08 | comptages **identiques** au corrigé M07.P, totaux **± 2 FCFA** documentés |

---

## 2. Grille de notation détaillée (/20)

| Livrable | Détail | Points |
|---|---|---|
| **E1** | Le script commenté : 6 sections numérotées, chaque section avec un en-tête de 2 lignes, **aucune valeur en dur** (tout est calculé), `if __name__ == "__main__":` | /8 |
| **E2** | Le rapport d'audit imprimé : les 4 défauts du socle chiffrés **avec leur définition exacte** (8 doublons → 50 000 uniques ; 208 retours en brut / 200 après dédoublonnage ; 21 406 dates sous la condition naïve + 15 deadlines aberrantes ; 0 valeur manquante, 1 table vide) **et la méthode** qui les a trouvés | /4 |
| **E3** | Le classeur de synthèse : 4 feuilles nommées, comptages identiques au corrigé M07.P, totaux monétaires à ± 2 FCFA (la dérive float, mesurée et **documentée dans le rapport d'audit**), pas de cellule en dur | /4 |
| **E4** | La note « ce qui a failli tourner en boucle » : 1 page — les 2-3 blocs où vous avez hésité entre une boucle et une vectorisation, et pourquoi la version vectorisée gagne (**mesure de temps fournie**) | /4 |

**Total : /20. Seuil de passage : 13/20.** E2 et E3 pèsent 8 points ensemble :
c'est le cœur du module — produire le chiffre juste ne suffit pas, il faut le
**vérifier** (audit) et le **livrer** (classeur lisible par machine).

---

## 3. Corrigé-type (sorties réelles du script modèle)

> Le script modèle est `03_exercices/dossier_M08/analyse_commerciale_modele.py`.
> Exécutez-le (venv pandas 3.0.6, `matplotlib` en backend `Agg`) : les sorties
> ci-dessous sont celles de son exécution du 19/09/2026, publiées telles quelles.

```text
S1 formes : {'v': 50008, 'c': 1200, 'p': 380, 'cat': 8, 'm': 5, 'mode': 5, 'tva': 2, 'o': 0}
S2 audit : doublons=8 retours_brut=208 retours_net=200
          dates_naives=21406 deadlines_j20=15 manquants=0
          table vide : ['o']
S3 propres : 49800 lignes (doublons sortis, retours exclus)
S4 ca_brut=7908259732 ca_propre=7876320164 panier=158140
   top magasin : 4 1596813264
   top categorie : 7 1236006464
   plus gros mois : magasin 3 (2025-08) : 78965529
S5 graphiques : ['g1_ca_mensuel.png', 'g2_ca_magasin.png', 'g3_ca_categorie.png', 'g4_hist_montants.png']
S6 classeur : {'audit': (7, 2), 'indicateurs': (4, 2), 'par_magasin': (5, 1), 'par_mois': (120, 3)}
```

Chaque chiffre du S4 est une **clé du socle** (`chiffres_cites.json`) :
`ca_brut` = `m08p_ca_brut`, `ca_propre` = `m08p_ca_sans_retours`,
`panier` = `m08p_panier_moyen`, top magasin 4 = `m08p_ca_top_magasin`,
top catégorie 7 = `m08p_ca_categorie_top`, plus gros mois =
`m08p_plus_gros_mois_ca`. Le S2 chiffre les 4 défauts avec leurs définitions —
**E2 et E3 sur la même sortie**. Le S6 est **lisible par machine** :
le rechargement `pd.read_excel(…, sheet_name=None)` renvoie les 4 feuilles avec
leurs formes (120 × 3 et 5 × 1 notamment) — le classeur n'est pas qu'un
document, c'est une interface.

---

## 4. Les contrôles de fiabilité (rappel et vérification)

| Contrôle | Défaut / écart | La leçon | Chiffre de contrôle |
|---|---|---|---|
| **D1** | 8 doublons exacts (12 colonnes métier) | dédoublonner sur **toutes** les colonnes métier, pas sur une projection | 50 008 → 50 000 uniques |
| **D2** | 208 retours en brut / 200 après dédoublonnage, à montant **positif** | l'ordre des opérations de l'audit : les 8 doublons **sont** des retours | CA gonflé 7 908 259 732 vs propre 7 876 320 164 (écart 31 939 568) |
| **D3** | 21 406 dates sous la condition naïve `date_vente > date_limite_remise` + 15 deadlines tombant au 20 du mois | documenter la **convention** (mois de la vente) avant de compter | 24 mois de vue |
| **D4** | `objectif_magasin.csv` vide (0 ligne) | le `merge` renvoie 50 008 cellules `NaN` : c'est un **signal**, pas un bug | (50 008, 16) après merge |
| **Centimes** | diviser **par ligne** avant de sommer perd les centimes de chaque ligne | additionner en centimes entiers, diviser **une fois** après l'agrégat | le plus gros mois sort à 228 FCFA de son total exact (78 965 301 au lieu de 78 965 529) |
| **Croisée** | la somme `float` de DuckDB s'écarte de 1 FCFA de l'addition en centimes | la dérive `float` est **mesurée et sourcée**, pas cachée | 5 totaux à 1 FCFA près (clés `m08p_ecart_somme_float_*`) |

> **Règle du projet.** Un chiffre juste obtenu **sans l'audit** ne passe pas
> E2 — c'est la règle du projet M07.P, reprise ici : seul compte le chiffre
> juste, obtenu sans se faire piéger, avec la méthode qui l'a trouvé.

---

## 5. Critères de passage

| Critère | Condition |
|---|---|
| Note totale | ≥ 13/20 |
| E2 | les 4 défauts du socle chiffrés **avec leur définition exacte** (pas « il y a des doublons », mais « 8 doublons exacts sur les 12 colonnes métier → 50 000 ventes uniques ») |
| E3 | les 4 feuilles nommées + la dérive float **écrite dans le rapport d'audit** (± 2 FCFA, sourcée) |
| Exécution | le script **exécuté d'une traite** (sorties capturées), pas assemblé section par section à la main |
| Vérification | la croisée : vos totaux redonnent le côté SQL de `ATTENDU.json` à 2 FCFA près (comptages exacts) |

> **L'esprit du projet.** « Trois matinées », c'est le temps qu'un collègue passe
> à importer, auditer, nettoyer, calculer, graphiquer et exporter à la main —
> quatre ou cinq allers-retours machine, chacun une source d'erreur. Le script
> commenté est l'outil qui fait disparaître ces allers-retours **et** qui
> documente la méthode pour la prochaine fois. C'est la 2ᵉ pièce du portfolio
> (la 1ʳ est le corrigé M07.P) : la même base, deux moteurs, un seul total.
