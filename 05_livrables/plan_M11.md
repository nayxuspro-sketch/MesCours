# Plan M11 — SQL avancé pour la BI

**Module M11 · phase 4 (Business Intelligence) · 7 chapitres · 30 h · niveau N3 → N4 ·
budget 105 pages [89, 121] · projet « Les 12 rapports SQL de la cellule commerciale » ·
évaluation : quiz 20 Q + 5 exercices + étude de cas + 18 requêtes auto-testées.**
Rédigé le 24 septembre 2026, avant la rédaction (étape 1 du calque M05—M10).

---

## 1. Cadrage

### 1.1 Position dans l'architecture

M11 **ouvre la phase 4 — Business Intelligence** (5 modules · 35 chapitres · 150 h : M11 SQL avancé,
M12 fondamentaux de la BI, M13 modélisation, M14 Power BI, M15 DAX). Il vient après M07 (SQL :
interroger, agréger, rejoindre) et M09 (EDA), et **avant** M12 (les indicateurs) et M13 (le modèle) :
c'est le module qui fournit la **matière** que les trois suivants vont modéliser puis publier.

Ce que M11 apporte et que M07 ne pouvait pas apporter : M07 écrit des requêtes qui **agrègent** ;
M11 écrit des requêtes qui **comparent** (un mois au précédent, un magasin aux autres, un client à
son histoire). C'est la différence entre « combien » et « par rapport à quoi » — et c'est exactement
ce qu'un tableau de bord exigera en M14.

> **Écart de libellé à reporter en errata (clôture M11).** Le tableau §C.3 étiquette M11 et M12 en
> **palier P3**, alors que le listing des phases (§C.1) place M11—M15 en **phase 4** et que M11 ouvre
> explicitement cette phase. Source de vérité retenue : **§C.1** (la phase 4 commence à M11). L'errata
> sera porté au fichier d'architecture dans le push de clôture de M11, comme l'a été celui du §E.7
> pour M10.

**Outils.** DuckDB 1.5.5 (**exécuté**, avec la base `commercial.duckdb` du socle), SQLite (**exécuté**
pour le contrôle croisé), PostgreSQL **cité sans exécuté** (règle §1.5 : la procédure et les
différences de dialecte sont documentées, jamais présentées comme mesurées), SQL Server **cité** pour
les variantes de syntaxe (`TOP` au lieu de `LIMIT`, `QUALIFY` absent). DuckDB est le moteur de
l'atelier parce qu'il exécute les fonctions de fenêtre, `QUALIFY`, `PIVOT`, `UNNEST` et
`GROUPING SETS` — tout le programme du module — sans installation serveur.

### 1.2 Sept compétences de sortie (la matrice de couverture)

| # | Compétence de sortie | Chapitre | Preuve exigée |
|---|---|---|---|
| 1 | Écrire une **fonction de fenêtre** et l'opposer à `GROUP BY` | C01 | la même question traitée des deux façons, avec les deux résultats comparés |
| 2 | **Classer, cumuler, décaler** : rangs, totaux progressifs, écarts, variations en % | C02 | top N par groupe, cumul annuel, écart M-1, variation en % — 4 requêtes testées |
| 3 | Traiter le **temps en SQL** : agrégats partiels, calendrier, année sur année, mois glissants, absence de ventes | C03 | la comparaison 2025/2026 par mois **avec les mois sans vente à zéro** |
| 4 | Construire une **cohorte** et un **RFM** : première commande, rétention, récence, fréquence, montant | C04 | la matrice de rétention par cohorte d'inscription + les 5 segments nommés |
| 5 | Écrire les requêtes **avancées** : CTE, CTE récursive, `PIVOT`, `UNNEST`, `QUALIFY`, agrégats conditionnels, `ROLLUP` | C05 | un tableau croisé produit en SQL, comparé à son équivalent en lignes |
| 6 | **Diagnostiquer une requête lente** : `EXPLAIN`, index, `SELECT *`, partitionnement | C06 | le plan d'exécution avant/après index, et le temps mesuré |
| 7 | **Versionner et tester** une requête : conventions, commentaires, tests de non-régression, contrôle de cohérence entre deux sources | C07 | les 12 rapports du projet, dont 3 tests de non-régression verts |

### 1.3 Fait du socle (mesuré le 24/09/2026 — à figer en clés `m11_*` à l'étape 2)

Toutes ces valeurs sont **mesurées**, pas estimées, sur `01_socle_donnees/data/reference/ventes_propres.csv`
(le socle de M01—M03, réutilisé ici : **240 000** lignes, 2023-01-01 → 2026-08-31) et sur
`data/brut/clients.csv`. Le module **ne crée aucune donnée nouvelle** : il change les **questions**
posées à un socle existant.

| Fait | Mesure | Ce qu'il rend possible |
|---|---|---|
| Volume | **240 000** lignes, dont **237 191** hors retours (**2 809** retours) | test de volumétrie, comparaison avec `vente.csv` (M07/M09) |
| Chiffre d'affaires net | **15 595 154 955** FCFA | total de contrôle de tous les rapports |
| Clients | **23 497** identifiants de vente distincts, **23 912** clients référencés | la jointure à vérifier (voir ci-dessous) |
| Tickets | **145 212** | grains : ligne / ticket / client — le piège central du module |
| Magasins | **5**, CA de **1 733 230 083** à **5 312 205 459** FCFA | classements, parts, écarts au premier |
| Période | **44** mois (**2023-01** → **2026-08**) | cohortes, année sur année, mois glissants |
| Concentration | top **5 %** = **30,0 %** du CA · top **10 %** = **38,1 %** · top **20 %** = **51,0 %** | l'étude de cas (voir §1.5) : la revendication « 10 % → 60 % » est **fausse sur ce socle** |
| Fréquence | médiane **8** tickets par client, moyenne **9,9**, maximum **38 984** | RFM, distribution, valeurs extrêmes |
| **Le client 0** | **38 984** tickets, **42 658** lignes, **2 852 612 447** FCFA, soit **18,3 %** du CA net — et **absent du référentiel** `clients.csv` (seul identifiant de vente non référencé) | le cas d'intégrité référentielle : jointure interne vs externe, et le classement de clients qui bascule |
| Sans le client 0 | top **10 %** = **24,2 %** du CA | ce que devient une conclusion quand on retire un artefact |
| Référentiel clients | **1 911** villes manquantes (8 %), **0** doublon d'identifiant | jointures et valeurs manquantes en SQL |
| Intégrité référentielle | **0** orphelin pour les produits (**154**), les magasins (**6** référencés, **5** utilisés) et les vendeurs (**22**) | l'intégrité n'est pas un hasard : elle se **vérifie** (rapport R12) |
| Objectifs de CA | **218** couples magasin-mois attendus **220** : **magasin 4** sans objectif en **2024-02** et **2024-03** ; total des objectifs **6 685 260 000** FCFA, soit **233,3 %** du réalisé | le mois manquant de C03, le rapport réalisé/objectif de R05, et le désaccord de sources de R12 |
| Retours | **2 809** lignes | agrégats conditionnels, taux, seuils |

**Deux détails de lecture que le module exploite** (mesurés à l'étape 1) : `objectifs_de_ca.csv` est
séparé par des **points-virgules** et non par des virgules, et les fichiers du dossier `brut/` portent
un **BOM** (`utf-8-sig`) — soit deux causes classiques de colonnes fantômes et de première colonne
illisible. Ils sont traités en C05 (chargement explicite) et en C07 (le test qui doit les détecter
avant la mise en production d'un rapport).

**Le chiffre qui porte le module.** Le client **0** : avec lui, le « meilleur client » réalise
**2 852 612 447** FCFA et **18,3 %** du chiffre d'affaires ; **sans** lui — c'est-à-dire en
reconnaissant qu'il s'agit d'un client **non identifié**, pas d'un client — le classement change de
tête et la concentration tombe de 38,1 % à **24,2 %**. Une seule ligne de `WHERE` décide donc de la
conclusion d'une analyse de fidélité : c'est la leçon de M11, énoncée dès C01 et vérifiée dans chaque
rapport.

### 1.4 Le projet M11.P — « Les 12 rapports SQL de la cellule commerciale »

- **Énoncé.** La cellule commerciale d'une enseigne de quincaillerie (5 magasins, 44 mois,
  240 000 lignes) commande sa **bibliothèque de rapports** : 12 requêtes autonomes, **versionnées**,
  **testées** et **commentées en français**, chacune répondant à une question écrite.
- **Livrables** (grille /20, seuil 13) :
  - **P1 — Les 12 requêtes** (8 pts) : une par question, chacune avec son en-tête (question,
    hypothèses, grain, source), son `ORDER BY` explicite et son total de contrôle.
  - **P2 — Le jeu de tests** (5 pts) : chaque requête accompagnée d'au moins un **test de
    non-régression** (total attendu, nombre de lignes, valeurs extrêmes) exécuté par
    `tools/controle_sql_M11.py`.
  - **P3 — La note de lecture** (4 pts) : 2 pages — ce que les 12 rapports disent ensemble, les
    **3 précautions** (client 0, retours, grains), et la question à laquelle ils ne répondent pas.
  - **P4 — La fiche de reprise** (3 pts) : un pair reprend **3** rapports, exécute les tests, et
    note ce qui manque pour qu'il puisse travailler sans l'auteur.
- **Les 12 rapports** (la colonne vertébrale du module, un par question métier) :

| # | Le rapport | La question | Le geste SQL |
|---|---|---|---|
| R01 | CA mensuel et variation | comment évolue l'activité mois par mois ? | agrégat + `LAG` |
| R02 | CA par magasin et part du total | quelle est la place de chaque magasin ? | fenêtre de part |
| R03 | Top 10 produits par catégorie | quels produits tirent chaque famille ? | rang partitionné |
| R04 | Classement des vendeurs et écart au premier | qui vend, et de combien devant ? | `RANK`, écart, `NTILE` |
| R05 | Réalisé cumulé contre objectif cumulé | où en est-on par rapport au rythme annuel ? | total progressif + jointure externe |
| R06 | Année sur année, mois par mois | la croissance est-elle réelle ou calendaire ? | comparaison inter-annuelle |
| R07 | Moyennes mobiles 3 et 12 mois | que dit la tendance sous le bruit ? | fenêtres mobiles |
| R08 | Rétention par cohorte d'entrée | les clients reviennent-ils ? | cohorte + matrice |
| R09 | RFM simplifié et segments | quels clients soigner en priorité ? | scoring + `CASE` |
| R10 | Panier par mode de paiement et effectifs | un panier moyen différent est-il un vrai écart ? | agrégat + taille |
| R11 | Taux de retour par magasin et par produit | où sont les problèmes de qualité ? | agrégat conditionnel |
| R12 | Rapport de contrôle des sources (ventes, référentiels, objectifs) | les sources racontent-elles la même histoire ? | comparaison croisée + `FULL OUTER JOIN` |

### 1.5 Évaluation M11

- **Quiz 20 Q** (seuil 14/20 §B.6) : 5 questions « quelle requête pour quelle question », 5 questions
  « prédisez le résultat » (une requête est donnée, l'apprenant prédit la sortie), 5 questions de
  diagnostic (pourquoi cette requête donne-t-elle un total faux ?) et 5 questions de vocabulaire.
- **5 exercices argumentés**, dont **2 de type E4** (requêtes erronées) : la question posée est
  « trouvez l'erreur », et la justification pèse plus que la correction.
- **Étude de cas notée** — « **les 10 % de clients qui font 60 % du CA** » : la direction reprend une
  affirmation lue ailleurs et demande de la vérifier. Réponse **mesurée** sur le socle : top 10 % =
  **38,1 %** du CA, top 20 % = **51,0 %**, et hors client anonyme, top 10 % = **24,2 %**. L'apprenant
  doit produire (a) le chiffre vrai, (b) le **classement des clients avant/après** retrait du client
  **0** (18,3 % du CA, **absent du référentiel**), (c) la conclusion tenable sur la concentration, et
  (d) la **question suivante** à poser (la part des clients non identifiés dans les cohortes).
- **18 requêtes de validation auto-testées** : `tools/controle_sql_M11.py` (à créer, calque de
  `controle_sql.py` de M07) compare le résultat de l'apprenant au résultat attendu, requête par
  requête, et rend « validé / non validé + quel test a échoué ».

### 1.6 Règles d'exécution (cadence héritée de M06—M10)

- **1 push par chapitre validé `--strict`** (7 pushes) + plan + socle + appareil + clôture.
- Push forcé autorisé ; **token re-testé via curl avant chaque push** ; **bundle avant
  `rm -rf .git`** ; `.git` supprimé après chaque push ; **aucun `.pyc`** sur le remote.
- **Tous les nombres ≥ 4 chiffres** des chapitres, du projet et de l'évaluation sont sourcés dans
  `chiffres_cites.json` (section `M11`, clés majuscules) ; **tables non exemptées** ; les nombres de
  littérature sont reformulés en pourcentages.
- **Typographie** : glyphes du jeu latin-1 étendu (chaque glyphe du `.md` doit sortir dans le PDF) ;
  **jamais de tiret demi-cadratin (U+2013)** (il ne se compose pas) — **cadratin U+2014** partout ; anglicismes avec
  couple français au premier emploi (« fonction de fenêtre » (*window function*), « table
  d'expression commune » (*CTE*), « tableau croisé » (*pivot*)).
- **§1.5** : DuckDB et SQLite **exécutés**, PostgreSQL et SQL Server **cités sans exécution** —
  la mention figure dans les encadrés des chapitres concernés (C01, C05, C06), jamais dans une note
  de bas de page.
- **Leçon PATCH_4** : apostrophe SQL par `replace("'", "''")` ; **pas** de guillemets doubles
  (DuckDB), **pas** de backticks.
- **Leçon PATCH_6** : à la clôture, vérifier l'**existence nommée** (`ls`) de chaque livrable du
  plan, jamais l'affirmation de la fiche.

### 1.7 La table des 20 questions métier (le fil du module)

Chaque chapitre porte ses requêtes de référence, exécutées et publiées avec leur sortie réelle. La
répartition prévue : **3** requêtes en C01 (fenêtre contre `GROUP BY`), **4** en C02 (rang, cumul,
décalage, variation), **3** en C03 (calendrier, inter-annuel, mois glissant), **3** en C04 (cohorte,
rétention, RFM), **3** en C05 (tableau croisé, récursif, récapitulatif), **2** en C06 (plan
d'exécution, effets d'un index), **2** en C07 (test de non-régression, contrôle croisé de deux
sources) — soit **20** requêtes, dont **12** reprises dans le projet.

## 2. Vocabulaire du module (à définir au premier emploi)

| Terme (français) | Équivalent anglais | Définition en une phrase |
|---|---|---|
| **fonction de fenêtre** | *window function* | Un calcul qui regarde un **ensemble de lignes liées** à la ligne courante (partition, ordre, cadre) sans réduire le nombre de lignes, contrairement à `GROUP BY`. |
| **partition** | *partition* | Le sous-ensemble sur lequel la fenêtre est calculée : « par magasin », « par mois » — le facteur de comparaison. |
| **cadre de fenêtre** | *window frame* | Les lignes effectivement prises en compte autour de la ligne courante (`ROWS BETWEEN … AND …`) : ce qui distingue un cumul d'une moyenne mobile. |
| **classement strict / à égalité** | *row number / rank / dense rank* | Trois façons de classer : rangs consécutifs (`ROW_NUMBER`), rangs qui sautent en cas d'égalité (`RANK`), rangs sans trou (`DENSE_RANK`). |
| **décalage** | *lag / lead* | La valeur de la ligne **précédente** ou **suivante** dans l'ordre de la fenêtre : c'est ce qui rend possible une variation. |
| **total progressif** | *running total* | Un cumul qui s'arrête à la ligne courante ; il **dépend de l'ordre**, et change si l'ordre change. |
| **mois glissant** | *rolling / moving average* | Une moyenne calculée sur une fenêtre qui **avance** (3 ou 12 mois) : elle lisse le bruit sans supprimer la tendance. |
| **cohorte** | *cohort* | Un groupe de clients partageant un événement de départ daté (mois de **première** commande) ; la rétention se mesure par cohorte. |
| **rétention** | *retention* | La part d'une cohorte encore active après N périodes — le seul indicateur de fidélité qui ne flatte pas la croissance. |
| **RFM** | *recency, frequency, monetary* | Trois mesures par client : depuis quand il n'a pas acheté, combien de fois, pour quel montant — utilisées ensemble pour segmenter. |
| **table d'expression commune** | *CTE, common table expression* | Un bloc `WITH …` qui nomme un résultat intermédiaire : c'est ce qui rend une requête longue lisible. |
| **tableau croisé** | *pivot* | Passer de « une ligne par mois et par mode » à « une ligne par mois, une colonne par mode ». |
| **récapitulatif multi-niveaux** | *rollup / cube / grouping sets* | Obtenir dans **une** requête les détails **et** les sous-totaux, sans concaténer six requêtes. |
| **plan d'exécution** | *execution plan* | La description, par le moteur, de **comment** il va exécuter la requête : c'est le seul moyen honnête de parler de performance. |
| **test de non-régression** | *regression test* | Un test qui rejoue une requête et compare son résultat attendu : il protège les rapports contre les modifications futures. |
| **grain** | *grain* | Ce que représente **une ligne** (une ligne de vente, un ticket, un client-mois) : la première question de tout rapport. |

## 3. Découpage en 7 chapitres

| Chap. | Titre | Contenu | H | p. |
|---|---|---|---|---|
| **C01** | Fonctions de fenêtre : `OVER`, `PARTITION BY`, `ORDER BY` — et la différence avec `GROUP BY` | le concept, le cadre de fenêtre, ce qui change dans le résultat (autant de lignes en sortie), 3 requêtes de référence | 5 | 13 |
| **C02** | Rang, cumuls, décalages : `ROW_NUMBER`, `RANK`, `DENSE_RANK`, `NTILE`, `SUM() OVER`, `LAG`, `LEAD` | top N par groupe, totaux progressifs, écarts et variations en %, le cas où le classement contredit le total | 5 | 13 |
| **C03** | Séries temporelles en SQL : dates partielles, calendrier, année sur année, mois glissants, absence de ventes | le mois sans vente qu'il faut **fabriquer**, la table calendrier, comparaisons inter-annuelles, fenêtres mobiles | 4 | 11 |
| **C04** | Cohortes, rétention et récurrence : première et dernière commande, panier, fréquence, RFM simplifié | cohorte d'entrée, matrice de rétention, segments RFM, le cas du client non identifié | 4 | 11 |
| **C05** | Requêtes avancées : CTE (dont récursives), `PIVOT`, `UNNEST`, `QUALIFY`, agrégats conditionnels, `ROLLUP`/`CUBE` | le tableau croisé en SQL, les récapitulatifs multi-niveaux, ce que DuckDB fait mieux | 4 | 11 |
| **C06** | Vues, index, `EXPLAIN`, requêtes lentes, coût du `SELECT *`, partitions | lire un plan d'exécution, mesurer l'effet d'un index, ce qu'un analyste doit savoir (et ignorer) | 5 | 13 |
| **C07** | Style, lisibilité, conventions, tests de non-régression, contrôle entre deux sources | la requête comme livrable : en-tête, nommage, tests, comparaison croisée des socles | 3 | 9 |

**Calque de rédaction** (hérité de M09/M10, imposé par `autovalide --strict`) : 17 sections par
chapitre, encadrés `Définition` 4—8, `À retenir` 2—4, `Attention` 2—5, `Conseil` 1—3,
`Dans les faits` 1—2 ; chaque chapitre s'achève par un mini-projet de chapitre noté sur 18 et une
évaluation formative courte.

## 4. Budget pages

| Élément | Calcul | Pages |
|---|---|---|
| Chapitres | 7 × 12,5 | **87,5 → 88 p.** |
| Appareil de module | ouverture, bilan, projet, évaluation | **17 p.** |
| **Total M11** | | **105 p.** |
| Fourchette ±15 % | | **[89, 121] p.** |

Répartition des chapitres ci-dessus (13 · 13 · 11 · 11 · 11 · 13 · 9 = **81 p.** de matière, le solde
allant aux blocs de tête et de queue de chaque chapitre). Contrôle final par
`tools/budget_pages.py --mesure`.

## 5. Chiffres cibles (à figer dans `chiffres_manuel.py M11`)

- **Forme du socle** : 240 000 lignes, 237 191 hors retours, 2 809 retours, 145 212 tickets,
  23 497 clients de vente, 23 912 clients référencés, 5 magasins, 44 mois, 12 rapports, 20 requêtes
  de référence, 18 requêtes auto-testées, 40 clés `m11_*` et `m11p_*`.
- **Le fait qui porte le module** : le client **0** — 38 984 tickets, 2 852 612 447 FCFA, 18,3 % du
  CA net, absent du référentiel ; concentration top 10 % de **38,1 %** (avec lui) à **24,2 %**
  (sans lui) ; top 20 % = 51,0 %.
- **Les écarts à mesurer par chapitre** : écart de CA entre le premier et le dernier magasin
  (5 312 205 459 contre 1 733 230 083 FCFA, soit un rapport **3,07**), médiane de **8** tickets par
  client contre une moyenne de **9,9**, **1 911** villes manquantes dans le référentiel clients,
  **2** couples magasin-mois sans objectif (**magasin 4**, **2024-02** et **2024-03**), et l'écart de
  total entre les deux socles (`ventes_propres.csv` et `vente.csv`) à expliquer, jamais à masquer.
- **Objectif** : deux exécutions de `chiffres_manuel.py M11` donnent un `diff` de **0 ligne**.

## 6. Risques et parades

| Risque | Parade |
|---|---|
| Le module devient un catalogue de syntaxe SQL | Chaque requête répond à une **question métier écrite**, reprise dans la table §1.7 ; une requête sans question est un échec. |
| Les fonctions de fenêtre sont appliquées sans comprendre le grain | C01 impose la comparaison **`GROUP BY` contre `OVER`** sur la même question, avec les deux résultats publiés côte à côte. |
| Le client **0** fausse tous les classements sans que personne ne le voie | Il est le **cas d'ouverture** du module : mesuré dès C01, retrouvé dans le rapport R12 et l'étude de cas, avec le classement avant/après. |
| PostgreSQL « exécuté » par glissement | Les encadrés des chapitres concernés portent la mention **cité, non exécuté** ; aucun plan d'exécution PostgreSQL n'est publié. |
| Les requêtes sont justes mais illisibles | C07 est entièrement consacré au style et aux tests ; le projet note l'**en-tête** et le **commentaire** autant que le résultat. |
| Le socle de M11 diverge de celui de M07/M09 | Le rapport R12 **compare les deux socles** et explique l'écart (périmètre, lignes, retours) au lieu de le cacher — c'est la leçon PATCH_3 du manuel. |
| Le poids de l'atelier ne permet aucune copie du socle | Le socle M11 est un **script SQL** (3,6 ko) posé sur des vues `read_csv_auto` ; tout ce qui exige du volume est **matérialisé en mémoire** pour la mesure (`ouvrir(materialiser=True)`), jamais écrit sur le disque. |

## 7. Étapes de production (calque M05—M10)

1. **Étape 1 — Plan** (ce document).
2. **Étape 2 — Socle** : `tools/dossier_M11.py` (base `socle_m11.duckdb` construite depuis les socles
   existants **sans générer de donnée nouvelle** : `ventes_propres.csv`, `clients.csv`, `produits.csv`,
   `magasins.csv`, `vendeurs.csv`), `diff`/empreinte sur deux exécutions, et les clés `m11_*` dans
   `chiffres_manuel.py` (≈ 40 clés, `diff` = 0).
   **Contrainte de poids (mesurée le 24/09/2026 : 127,9 Mo sur 128, marge +0,1 Mo).** La base M11 ne
   peut **pas** recopier les 240 000 lignes de vente : `socle_m11.duckdb` sera construit en **vues**
   au-dessus du socle de M07/M09 (`read_csv_auto` sur les CSV déjà versionnés), plus les tables de
   petite taille (produits, magasins, vendeurs, référentiel clients). Objectif : **< 1 Mo**. La
   démonstration qui exige du volume (index, `EXPLAIN`, requête lente de C06) s'appuiera sur une
   **matérialisation en mémoire** du même socle (`ouvrir(materialiser=True)`) : un fichier DuckDB pèse
   au minimum ~512 ko (mesuré), donc rien ne sera écrit — les temps sont gelés dans `PERF_M11.json`.
3. **Étape 3 — Rédaction** : 7 chapitres, **1 push par chapitre validé `--strict`** (7 pushes), chacun
   avec ses requêtes exécutées et leur sortie réelle.
4. **Étape 4 — Figures** : `tools/figures_M11.py` — 2 planches seulement (le module est un module de
   **requêtes**, pas de graphiques) : (a) la carte des fenêtres (partition, ordre, cadre) et
   (b) la matrice de rétention par cohorte ; largeur ≤ 776 px, jeu latin-1 étendu.
5. **Étape 5 — PDF** : `tools/render.py "02_modules/M11_*.md" --join --out 05_livrables/M11.pdf`
   (budget 105 p. ±15 % = [89, 121]) + `tools/controle_pdf.py M11`.
6. **Étape 6 — Fiche de contrôle** : `05_livrables/fiche_controle_M11.md` Q1—Q10.
7. **Étape 7 — Projet + évaluation + clôture** : `03_exercices/M11_projet.md` (12 rapports, 4
   livrables /20 seuil 13), `04_evaluations/M11_evaluation.md` (quiz 20 Q + 5 exercices + étude de cas
   + 18 requêtes auto-testées), `tools/controle_sql_M11.py`, `README.md`, `05_livrables/etat_avancement.md`,
   et l'**errata du §C.3** (palier de M11/M12 : P3 → phase 4).
