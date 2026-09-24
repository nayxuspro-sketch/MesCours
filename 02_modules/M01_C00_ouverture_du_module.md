# M01 — Lire les données et comprendre le métier de l'analyse

**Phase 0 · Culture numérique et posture professionnelle · 7 chapitres · 30 h · 525 pages disponibles à la fin de M07**

> **Ce que ce module vous apporte, en une phrase.** Vous allez apprendre à **lire** une donnée avant d'apprendre à la calculer : reconnaître une table, son grain, ses types, son format, sa provenance — et formuler la question qui rendra le calcul utile. Aucun autre module du parcours ne vous rendra aussi vite opérationnel sur un poste réel.

---

## Promesse du module

À la fin du module M01, vous êtes capable de :

- ouvrir un dossier de travail, **nommer** vos fichiers selon une convention qui survivra à trois ans, et **retrouver** en deux minutes l'origine d'un chiffre ;
- décrire une table en six phrases, dire ce que représente **une ligne**, et ne plus jamais confondre 489 lignes avec 316 ventes ;
- détecter, sans logiciel spécialisé, qu'une colonne de montants est du **texte** (ici 486 lignes sur 489) et expliquer ce que ça casse ;
- lire un fichier livré par un fournisseur en `;`, encodé en **Windows-1252**, à virgule décimale et chapeau de trois lignes — sans le qualifier de « corrompu » ;
- classer une variable (quantitative discrète, continue, nominale, ordinale) et **refuser** le calcul qu'elle ne permet pas ;
- raconter le **cycle de vie** complet d'une ligne de vente, et produire les trois documents qui rendent un chiffre défendable : dictionnaire, journal de transformation, manifeste ;
- écrire une **question analytique** correcte à partir d'une demande floue, et choisir l'outil qui convient en le justifiant.

## Carte des chapitres

| Chap. | Titre | Compétence visée | Outil | H |
|---|---|---|---|---|
| C01 | Se repérer dans un ordinateur de travail | ne plus perdre un fichier, comprendre un chemin, sauvegarder pour de vrai | Explorateur Windows | 4 |
| C02 | Donnée, information, connaissance, décision | formuler la différence avec des exemples de son environnement | papier | 3 |
| C03 | La table : lignes, colonnes, cellules, en-têtes, identifiants | lire une table et la décrire en langage clair | Excel / LibreOffice | 5 |
| C04 | Types de données et ce qu'ils autorisent | détecter un « nombre stocké en texte » et expliquer le dégât | Excel / LibreOffice | 5 |
| C05 | Structuré, semi-structuré, non structuré ; qualitatif, quantitatif | classer 20 exemples réels, choisir les statistiques licites | tableur + éditeur de texte | 4 |
| C06 | Le cycle de vie d'une donnée | retracer une ligne de la caisse au rapport annuel, documenter | schéma + traitement de texte | 4 |
| C07 | Métiers de la donnée et anatomie d'une analyse | cadrer une demande floue, choisir son outil et le justifier | traitement de texte | 5 |
| — | **Projet M01.P** | livrable évalué : fiche d'identité, questions, réponse chiffrée, autoportrait | tableur | 5 |

Total : **30 h** (25 h de chapitres + 5 h de projet et d'évaluation), conformément au programme validé.

## Prérequis

Aucun, sauf savoir utiliser une souris, un clavier et un navigateur. Le chapitre C01 prend en charge tout le reste, y compris « comment est rangé un ordinateur ». Si vous avez déjà pratiqué un tableur, commencez par l'exercice 3.1 : s'il vous semble évident, allez au C04 en lisant C03 en diagonale — mais ne sautez pas C02, dont le vocabulaire sert jusqu'au module 22.

## Outils à installer avant de commencer

| Outil | Version visée (vérifiée septembre 2026) | Rôle dans le module | Alternative libre |
|---|---|---|---|
| LibreOffice Calc | 24.8 ou supérieur | tous les exercices de tableur | — |
| Microsoft Excel | 2021 / Microsoft 365 | équivalent selon votre poste | LibreOffice suffit ici |
| Un éditeur de texte | Bloc-notes, gedit, VS Code | lire les fichiers bruts | n'importe lequel |
| Un terminal | PowerShell, Terminal, Git Bash | compter, vérifier encodage et empreintes | facultatif mais très utile |

Deux précisions utiles, parce qu'elles reviennent dans tous les forums : **LibreOffice 24.8 et supérieur** gère nativement les fonctions récentes (`RECHERCHEX`, `FILTRE`, `UNIQUE`, `LET`, `SEQUENCE`), là où les versions antérieures ne les avaient pas ; **Excel** propose `RECHERCHEX` depuis 2021, mais `FILTRE`, `UNIQUE`, `LET`, `SÉQUENCE` et `TRIBY` supposent Microsoft 365 ou Excel 2024. Le module 3 reprend ce point en détail ; ici, aucune fonction récente n'est nécessaire.

## Les données de travail du module

Tout le module, puis tout le parcours, travaille sur un jeu de données **réellement livré dans ce dossier**, pas sur un exemple fictif :

| Fichier | Rôle | Volumétrie réelle |
|---|---|---|
| `01_socle_donnees/data/projection/ventes_magasin5_2025.csv` | **votre fichier de travail** : extrait du magasin 5, année 2025 | **489 lignes × 13 colonnes** (dont 9 en double) |
| `01_socle_donnees/data/brut/ventes_brutes.csv` | le fichier complet, pour mesurer l'échelle | **243 360 lignes × 20 colonnes**, 28,5 Mo |
| `01_socle_donnees/data/reference/ventes_propres.csv` | la référence propre, pour vérifier vos calculs | **240 000 lignes** |
| `01_socle_donnees/data/reference/ventes_magasin5_2025_ATTENDU.csv` | le **corrigé** de l'extrait nettoyé | **480 lignes** |
| `01_socle_donnees/data/brut/tarif_fournisseur_peinture.csv` | le fichier hostile (encodage, chapeau, virgule) | **42 lignes** dont 38 utiles |
| `01_socle_donnees/data/reference/verites_terrain.csv` | les totaux de contrôle du jeu complet | CA TTC 4 ans : **15 419 985 157 FCFA** |
| `01_socle_donnees/data/reference/chiffres_cites.md` | **la source unique des chiffres cités dans ce manuel** | tous les nombres de ce module en viennent |

Règle de travail : si un nombre de l'énoncé ne correspond plus à votre fichier, **c'est votre fichier qui a changé**, pas l'énoncé. Régénérez (`python3 01_socle_donnees/scripts/generation_socle.py`) puis relisez `chiffres_cites.md`. Le jeu est déterministe : une graine fixe (20260917) produit toujours les mêmes fichiers, donc les mêmes chiffres, pour vous comme pour le correcteur.

## Livrables attendus du module

1. le dossier `Sahel/` rangeé selon la convention (C01, mini-projet P1) ;
2. la fiche d'identité des trois tables (C03, mini-projet P3) ;
3. le dictionnaire de types (C04, mini-projet P4) ;
4. la carte d'identité du lot de données (C05, mini-projet P5) ;
5. le dossier d'archivage d'une publication (C06, mini-projet P6) ;
6. les trois formulaires de cadrage (C07, mini-projet P7) ;
7. **le projet M01.P complet** (fiche, questions, réponse chiffrée, page d'autoportrait) ;
8. l'évaluation : quiz 15 questions, 4 exercices, étude de cas, notés sur 20.

## Comment travailler ce module (méthode recommandée)

| Séance | Durée | Contenu | Contrôle de fin de séance |
|---|---|---|---|
| 1 | 4 h | C01 + mise en place du poste | arborescence + 12 lignes de journal |
| 2 | 3 h | C02, cahier en main | cinq demandes réelles converties en questions |
| 3-4 | 5 h | C03 sur le fichier réel | six phrases + cinq comptages justes |
| 5-6 | 5 h | C04 : typage du fichier de l'atelier | `NB` = `NBVAL` après conversion, total à 36 073 185 FCFA |
| 7 | 4 h | C05 | classement des 13 colonnes + réponse en 5 lignes |
| 8 | 4 h | C06 | dictionnaire + journal + politique |
| 9 | 5 h | C07 | trois formulaires de cadrage |
| 10-11 | 5 h | projet M01.P et évaluation | rendu noté, quiz ≥ 14/20 pour passer en M02 |

**Seuil de passage en M02 :** quiz ≥ 14/20 **et** projet M01.P complet (les quatre livrables). Vous pouvez commencer M02 avec un 13/20 si vous reprenez les deux exercices manqués pendant le module suivant — le parcours est conçu pour que rien ne soit éliminatoire, sauf l'abandon.

## Ce qui vient après

Le module 2 (statistiques du résumé) utilise le **même fichier**, nettoyé par vos soins. Le module 3 (tableur avancé) remplace vos formules de comptage par des tableaux croisés. Le module 4 (qualité de la donnée) reprend vos 9 doublons, vos 65 dates et vos 7 quantités aberrantes, et en fait un chantier documenté. Vous n'apprendrez donc rien « en l'air » : chaque module consomme le livrable du précédent.
