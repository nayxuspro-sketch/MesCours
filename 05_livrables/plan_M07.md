# Plan M07 — SQL : interroger, agréger, rejoindre

**Module M07 · 8 chapitres · 30 h · niveau N2 → N3 · prérequis M06 (indispensable), M02 (agrégats), M04 (qualité).**

> **L'idée du module.** Le classeur a montré ses limites en M06 (3ᵉ table jointe, 50 000ᵉ ligne). Le
> SGBD les résout par la **structure** (schéma, contraintes, 3FN). Mais une base sans requête ne sert
> à rien : c'est SQL qui **transforme** les données en réponses. M07 fait passer l'apprenant de
> *« je sais ce qu'est une table »* à *« je sais poser une question métier en SQL, la faire
> exécuter, lire le résultat, et corriger la requête quand elle est fausse »*. Les **8 chapitres**
> couvrent l'ordre réel d'exécution (C01), le filtrage (C02), le tri (C03), l'agrégation (C04), le
> groupement (C05), la catégorisation (C06), la jointure (C07), la structuration (C08 — sous-requêtes
> et CTE). Le **projet M07.P** ferme le module : 30 questions métier sur la base commerciale d'une
> chaîne de 5 magasins, dont 6 « pièges de fiabilité » qui exigent de repérer un doublon. La
> **transition** finale annonce M08 (pandas comme accélérateur) : *« SQL vous donne le chiffre,
> Python vous donne la méthode, la vitesse, et la capacité de refaire tout cela en une seconde le
> mois prochain. »*

## 1. Cadrage

### 1.1 Position dans l'architecture

- **Phase** 2 — Maîtrise opérationnelle.
- **Après** M06 (bases de données : comprendre), **avant** M08 (Python/pandas), M11 (SQL avancé),
  M13 (modélisation en étoile), M21 (projet fil rouge).
- **Prérequis** :
  - **M06** — vocabulaire relationnel, schéma 3FN, exécution DuckDB/SQLite ; **indispensable**.
  - **M02** — agrégats (somme, moyenne, écart-type), compréhension d'une mesure.
  - **M04** — qualité des résultats, lecture des contrôles.
- **Verrouillé** par M11 (fenêtres, `EXPLAIN`, index), M08 (parallèle SQL/pandas), M21 (fil rouge
  en SQL sur 489 lignes).

### 1.2 Huit compétences de sortie (la matrice de couverture)

1. **Écrire** une requête `SELECT` simple, avec alias, `DISTINCT`, `LIMIT`, et **comprendre**
   l'ordre réel d'exécution (`FROM` → `WHERE` → `GROUP BY` → `HAVING` → `SELECT` → `ORDER BY` →
   `LIMIT`).
2. **Filtrer** avec `WHERE` (opérateurs, `IN`, `BETWEEN`, `LIKE`, `IS NULL`, dates) en respectant
   les priorités logiques (`AND` avant `OR`, parenthéser pour clarifier).
3. **Trier** avec `ORDER BY` (multi-clés, tri par alias, `ASC`/`DESC`, `NULLS FIRST/LAST`).
4. **Agréger** avec `COUNT`/`COUNT(*)`/`COUNT(DISTINCT)`, `SUM`, `AVG`, `MIN`, `MAX`, `ROUND`,
   en comprenant que les `NULL` ne comptent pas dans les moyennes.
5. **Résumer par groupe** avec `GROUP BY`, distinguer `WHERE` (avant agrégation) et `HAVING`
   (après), et compter avec une condition (`COUNT(CASE WHEN … THEN 1 END)`).
6. **Catégoriser en SQL** avec `CASE` (simple et recherché), `COALESCE`, `NULLIF`, et construire
   des tranches (`< 1000`, `1000-5000`, etc.).
7. **Joindre** avec `INNER`, `LEFT`/`RIGHT`, `FULL`, `CROSS`, auto-jointure, jointure multiple, et
   repérer les **4 symptômes de l'explosion de lignes** (jointure 1-N naïvement sur la mauvaise
   colonne, `DISTINCT` qui masque un mauvais `JOIN`, jointure multiple qui double, jointure
   manquante qui creuse un trou).
8. **Structurer** une requête complexe en sous-requêtes scalaires, `IN`, `FROM`, CTE (`WITH`), vues,
   et choisir `EXISTS` vs `IN` selon le cas.

### 1.3 Fait du socle (mesurés le 19/09/2026)

- **Socle déjà livré** (issu de M06) : `03_exercices/dossier_M06/quincaillerie_export.csv` (24 000
  lignes × 42 col), `schema_3fn.sql` (7 tables 3FN), `controles_integrite.sql`, et la base DuckDB
  en mémoire reconstruite à la demande par `python3 -c "import duckdb; …"`.
- **SGBD installé** : DuckDB 1.5.5 (`pip install --no-cache-dir duckdb`), utilisé en CLI
  (`duckdb fichier.duckdb`) et en Python (`duckdb.connect()`). SQLite natif Python 3.13. PostgreSQL
  reste cité sans exécuté (la règle M06 §1.5 perdure).
- **Client graphique** : DBeaver cité (téléchargement libre, multi-SGBD) sans exécution — un
  apprenant qui installe DBeaver en local gagne la même vue que le formateur.
- **Cinq ajouts au socle** nécessaires pour M07 (à ouvrir en étape 2 du plan) :
  1. `tools/dossier_M07.py` — générateur de la base commerciale d'une chaîne de 5 magasins (le
     projet M07.P), graine à fixer.
  2. Le fichier `03_exercices/dossier_M07/commercial.sql` — script de création de la base
     (8-12 tables : `magasin`, `client`, `produit`, `categorie`, `mode_paiement`, `vente`,
     `ligne_vente`, `objectif`, `promotion`).
  3. Le fichier `03_exercices/dossier_M07/commercial.duckdb` — base pré-construite pour les
     apprenants qui veulent sauter l'étape de chargement.
  4. Le **fichier `ATTENDU.json`** à ~ 30 clés `m07p_*` (les réponses des 30 questions métier, et
     les 6 « pièges » où la requête naïve donne un résultat faux).
  5. Le **fichier `30_questions.sql`** — énoncés des 30 questions (sans les réponses), classé par
     difficulté croissante.

### 1.4 Le projet M07.P — « La base commerciale d'une chaîne de 5 magasins »

- **Énoncé.** Une enseigne de distribution à Ouagadougou vous confie sa **base commerciale**
  (8 tables, ~ 50 000 lignes de ventes, 5 magasins, 1 200 clients, 380 produits). Le directeur vous
  pose **30 questions métier** de difficulté croissante : *« quel est le CA mensuel par magasin »*,
  *« quels clients ont acheté dans 3 magasins ou plus en 6 mois »*, *« quels produits sont
  surreprésentés dans les retours »*, etc. Six de ces questions sont des **« pièges de
  fiabilité »** : la requête naïve donne un résultat faux parce qu'elle ne voit pas un doublon, un
  NULL, ou une jointure multiple qui double les lignes.
- **Livrables** (grille /20, seuil 13) :
  - **E1 — Le fichier `.sql` commenté** (10 points) — 30 requêtes numérotées Q01-Q30, chacune
    avec un en-tête de 3 lignes (énoncé, table(s) utilisée(s), piège éventuel). La requête doit
    être lisible, alignée, et utiliser `WITH` pour les questions Q20-Q30.
  - **E2 — La note « les trois questions que je ne peux pas trancher »** (4 points) — 1 page,
    3 questions où l'apprenant hésite entre deux requêtes (par exemple Q12 sur le CA TTC vs HT)
    et explique son choix et son doute.
  - **E3 — Le tableau des 6 pièges** (6 points) — pour chacun des 6 pièges, la **requête naïve**
    (1 ligne), le **résultat faux** observé, la **requête corrigée**, le **bon résultat**, et
    l'**explication** en 1 phrase (par exemple : *« le piège était que `vente` et `retour`
    partagent le même `id_ticket` ; il fallait filtrer sur `est_retour = FALSE` »*).

### 1.5 Évaluation M07

- **Quiz** 20 Q (5 blocs : `SELECT`/`WHERE`, agrégats, `GROUP BY`/`HAVING`, jointures,
  sous-requêtes/CTE).
- **35 exercices de requêtes** auto-validés par `tools/controle_sql.py M07` — chaque requête a un
  résultat attendu (`m07p_*`), et le script compare la sortie réelle à la sortie attendue. Les
  exercices sont classés par chapitre (C01-C08).
- **Étude de cas d'audit** — « le directeur financier conteste le total mars » : l'apprenant
  reçoit 4 chiffres différents pour le CA de mars (3 254 000, 3 218 000, 3 412 000, 3 198 000 FCFA)
  et doit, par 3 requêtes successives, retrouver la cause de l'écart (doublon, retour inclus,
  date inversée).
- **Corrigés** chiffrés sur le dossier livré.

### 1.6 Règles d'exécution (rappel de la cadence M06, §1.5)

- DuckDB et SQLite **exécutés** ; PostgreSQL **cité sans exécuté** (la règle M06 §1.5 perdure ; le
  module M11 reprendra l'exécution PostgreSQL avec un serveur installé).
- Chaque chapitre contient **au moins une commande DuckDB exécutée** dont la sortie est publiée
  dans le PDF (jamais « le résultat est … » sans le texte de sortie).
- Chaque chiffre ≥ 4 chiffres cité dans un .md est **sourcé dans `chiffres_cites.json`** (les
  `m07_*` et `m07p_*`) ou reformulé.

## 2. Vocabulaire du module (à définir au premier emploi)

| Français — English | Première définition | Piège à éviter |
|---|---|---|
| **requête** — *query* | une instruction SQL posée au SGBD, qui retourne un résultat tabulaire. | confondre avec « table » : une requête n'est pas stockée, sauf si on en fait une vue. |
| **SELECT** | la clause qui **liste les colonnes** à retourner. | croire que `SELECT` « va chercher » les données : c'est `FROM` qui les cherche, `SELECT` ne fait que choisir les colonnes. |
| **FROM** | la clause qui **indique la ou les tables sources**. | croire que l'ordre des clauses reflète l'ordre d'exécution : `SELECT` s'écrit en premier, **s'exécute en 5ᵉ position**. |
| **WHERE** | la clause qui **filtre les lignes** avant agrégation. | l'utiliser après `GROUP BY` (c'est `HAVING` qu'il faut). |
| **GROUP BY** | la clause qui **regroupe les lignes** partageant une caractéristique. | mettre une colonne dans `SELECT` sans la mettre dans `GROUP BY` (PostgreSQL rejette ; MySQL laisse passer silencieusement). |
| **HAVING** | la clause qui **filtre les groupes** après agrégation. | l'utiliser pour filtrer des lignes (c'est `WHERE` qu'il faut). |
| **jointure** — *join* | la clause qui **combine deux tables** sur une condition. | croire que toutes les jointures sont des `INNER` : un `LEFT JOIN` mal écrit produit des NULL silencieux. |
| **INNER JOIN** | jointure qui **ne garde que les lignes** présentes dans les deux tables. | croire que c'est « le défaut » : un `LEFT JOIN` est souvent plus prudent en audit. |
| **LEFT JOIN** | jointure qui **garde toutes les lignes** de la table de gauche, et complète à `NULL` si la droite est absente. | oublier que les colonnes de la droite peuvent être `NULL` après jointure, et rater le `WHERE … IS NULL` qui repère les orphelins. |
| **sous-requête** — *subquery* | une requête **imbriquée** dans une autre (dans `WHERE`, `FROM`, ou `SELECT`). | imbriquer 4 niveaux : illisible ; préférer une CTE (`WITH`). |
| **CTE** — *Common Table Expression* | une requête **nommée en tête** de la requête principale, réutilisable. | croire qu'elle améliore les performances : en DuckDB, elle est purement syntaxique (lisibilité), pas optimisation. |
| **vue** — *view* | une requête **stockée** comme si c'était une table. | confondre avec une table matérialisée : une vue est recalculée à chaque appel. |

## 3. Découpage en 8 chapitres

### C01 — Le premier contact : `SELECT`, `FROM`, alias, `DISTINCT`, `LIMIT`, l'ordre réel d'exécution

- **Objectif.** L'apprenant écrit sa première requête, la lit, et comprend que l'ordre d'exécution
  SQL n'est pas l'ordre d'écriture.
- **Plan sommaire** :
  1. La requête vide : `SELECT 1;`, `SELECT 'Bonjour';`, `SELECT current_date;`.
  2. La requête à 1 table : `SELECT id, nom FROM client;` — `id` et `nom` sont des **colonnes**, pas
     des lignes.
  3. L'alias de colonne : `SELECT id AS identifiant, nom AS nom_client FROM client;`.
  4. L'alias de table : `SELECT c.id, c.nom FROM client AS c;`.
  5. `DISTINCT` : pourquoi la même valeur revient 14 fois et comment la dédoublonner.
  6. `LIMIT` : la sortie tronquée à 5 lignes — ce n'est pas un tri, c'est une fenêtre.
  7. **L'ordre réel d'exécution** : `FROM` → `WHERE` → `GROUP BY` → `HAVING` → `SELECT` → `DISTINCT`
     → `ORDER BY` → `LIMIT`. C'est la clé de tout le module : 90 % des erreurs viennent d'un
     malentendu sur cet ordre.
  8. **Exercice fil rouge** : sur la base DuckDB `sahel_ventes`, écrire 5 requêtes de difficulté
     croissante, prédire la sortie, et vérifier.
- **Livrables spécifiques** : 1 figure SVG « l'ordre d'exécution » (les 7-8 étapes sous forme de
  pipeline horizontal).

### C02 — Filtrer : `WHERE`, opérateurs, `IN`, `BETWEEN`, `LIKE`, `IS NULL`, dates, priorités logiques

- **Objectif.** L'apprenant filtre les lignes d'une table sur une ou plusieurs conditions, en
  maîtrisant les priorités logiques.
- **Plan sommaire** :
  1. Les opérateurs de comparaison : `=`, `<>`, `<`, `>`, `<=`, `>=`.
  2. `IN (…liste…)` — équivalent à une cascade de `OR`, mais lisible.
  3. `BETWEEN x AND y` — bornes **incluses**, piège classique.
  4. `LIKE` et les jokers `%` (n'importe quoi) et `_` (un caractère). `ILIKE` pour la casse
     (PostgreSQL).
  5. `IS NULL` / `IS NOT NULL` — `= NULL` ne marche jamais.
  6. Les dates : `date '2025-03-01'`, `date_vente BETWEEN '2025-03-01' AND '2025-03-31'`,
     `EXTRACT(YEAR FROM date_vente) = 2025`.
  7. Les priorités logiques : `AND` avant `OR`, parenthéser pour clarifier.
  8. **Exercice fil rouge** : sur `sahel_ventes`, 8 requêtes WHERE de difficulté croissante, dont
     2 pièges (`= NULL` qui retourne 0 lignes, et `BETWEEN` mal lu).
- **Livrables spécifiques** : 1 figure SVG « les 6 opérateurs de filtrage » (panneau d'aiguillage).

### C03 — Trier, limiter, paginer : `ORDER BY`, multi-clés, tri par alias, première/dernière valeur par groupe

- **Objectif.** L'apprenant trie les résultats sur une ou plusieurs colonnes, et comprend la
  différence entre `LIMIT` (fenêtre) et `ORDER BY` (tri).
- **Plan sommaire** :
  1. `ORDER BY colonne ASC` / `ORDER BY colonne DESC`.
  2. Multi-clés : `ORDER BY region ASC, ville DESC, nom ASC` — l'ordre des colonnes compte.
  3. Tri par alias de `SELECT` — autorisé en DuckDB et PostgreSQL.
  4. Tri par position : `ORDER BY 1, 3` (1 = 1ʳᵉ colonne du SELECT) — fragile, à éviter.
  5. `NULLS FIRST` / `NULLS LAST` — comportement par défaut dialecte-dépendant.
  6. **Pagination** : `LIMIT 10 OFFSET 20` — les 11ᵉ à 20ᵉ lignes. Lenteur sur les grosses
     tables (mention pour culture, optimisation en M11).
  7. Première/dernière valeur par groupe — astuce : `ORDER BY … LIMIT 1` à l'intérieur d'une
     sous-requête ou d'un `DISTINCT ON` (PostgreSQL).
  8. **Exercice fil rouge** : sur `sahel_ventes`, 6 requêtes de tri, dont le « top 3 des magasins
     par CA » et le « top 1 produit par catégorie ».
- **Livrables spécifiques** : 1 figure SVG « pipeline ORDER BY + LIMIT ».

### C04 — Agréger : `COUNT`/`COUNT(*)`/`COUNT(DISTINCT)`, `SUM`, `AVG`, `MIN`, `MAX`, `NULL` et moyennes, `ROUND`

- **Objectif.** L'apprenant calcule une mesure sur un ensemble de lignes.
- **Plan sommaire** :
  1. `COUNT(*)` vs `COUNT(colonne)` : la différence se joue sur les `NULL`.
  2. `COUNT(DISTINCT colonne)` : combien de valeurs uniques.
  3. `SUM`, `AVG`, `MIN`, `MAX` — toutes ignorent les `NULL` (sauf `COUNT(*)`).
  4. Le piège des moyennes : `AVG(colonne)` ≠ `(SUM/COUNT(*))` quand il y a des NULL.
  5. `ROUND(x, 2)` — arrondi à 2 décimales (le centime).
  6. Les agrégats sans `GROUP BY` : une seule ligne en sortie.
  7. **Exercice fil rouge** : CA total, panier moyen, nombre de clients uniques, top montant.
- **Livrables spécifiques** : 1 figure SVG « les 5 fonctions d'agrégation × 3 cas NULL ».

### C05 — Résumer par groupe : `GROUP BY`, ce qui est autorisé dans `SELECT`, `HAVING` vs `WHERE`, comptages conditionnels

- **Objectif.** L'apprenant produit un résumé par catégorie, et distingue le filtrage avant et
  après agrégation.
- **Plan sommaire** :
  1. La règle d'or : **toute colonne du `SELECT` qui n'est pas agrégée doit être dans
     `GROUP BY`**.
  2. `WHERE` filtre les lignes **avant** agrégation ; `HAVING` filtre les groupes **après**.
  3. Comptage conditionnel : `COUNT(CASE WHEN condition THEN 1 END)` — bien plus lisible qu'une
     jointure multiple.
  4. Les agrégats dans `HAVING` : `HAVING SUM(montant) > 1_000_000`.
  5. **Exercice fil rouge** : CA par magasin, par mois, par catégorie — avec HAVING pour ne garder
     que les magasins au-dessus de 5 M FCFA.
- **Livrables spécifiques** : 1 figure SVG « WHERE vs HAVING » (pipeline horizontal).

### C06 — Catégoriser en SQL : `CASE` simple et recherché, entonnoirs, tranches de prix, `COALESCE`, `NULLIF`

- **Objectif.** L'apprenant construit des catégories en SQL sans passer par Excel.
- **Plan sommaire** :
  1. `CASE WHEN … THEN … ELSE … END` — l'IF/ELSE du SQL.
  2. `CASE` simple : 1 condition, 1 résultat (`CASE WHEN age < 18 THEN 'mineur' ELSE 'majeur' END`).
  3. `CASE` recherché : plusieurs `WHEN` successifs, dans l'ordre.
  4. Tranches de prix : `< 1000`, `1000-5000`, `5000+`.
  5. `COALESCE(a, b, c, …)` : le premier non-NULL parmi la liste.
  6. `NULLIF(a, b)` : `NULL` si `a = b`, sinon `a` — permet d'éviter la division par zéro.
  7. **Exercice fil rouge** : segmentation RFM (récence, fréquence, montant) en SQL pur.
- **Livrables spécifiques** : 1 figure SVG « entonnoir CASE WHEN ».

### C07 — Joindre : `INNER`, `LEFT`/`RIGHT`, `FULL`, `CROSS`, auto-jointure, jointure multiple, les 4 symptômes de l'explosion de lignes, `UNION`

- **Objectif.** L'apprenant combine 2 tables ou plus, et repère les pièges.
- **Plan sommaire** :
  1. La syntaxe ANSI : `FROM a JOIN b ON a.x = b.y`. L'opérateur de jointure (`=`, `<`, `<>`).
  2. `INNER JOIN` : ne garde que les appariements.
  3. `LEFT JOIN` : garde toute la gauche, complète à `NULL` si pas d'appariement.
  4. `RIGHT JOIN` : symétrique du `LEFT JOIN` (rarement utilisé, on préfère inverser l'ordre).
  5. `FULL OUTER JOIN` : garde tout des deux côtés.
  6. `CROSS JOIN` : produit cartésien (à éviter, sauf cas spécifiques).
  7. **Auto-jointure** : une table jointe avec elle-même (par exemple, employés et leur manager).
  8. **Jointure multiple** : `vente JOIN client … JOIN produit … JOIN magasin …` — chaque jointure
     successive filtre ou multiplie.
  9. **Les 4 symptômes de l'explosion de lignes** :
     - Lignes comptées 2× ou 3× après une jointure 1-N naïve sur la mauvaise colonne.
     - `DISTINCT` utilisé pour masquer un mauvais `JOIN`.
     - Jointure multiple qui double parce qu'une des tables est un N-M non décomposé.
     - Jointure manquante qui creuse un trou (résultat trop bas sans erreur).
  10. `UNION` (et `UNION ALL`) : empiler deux résultats de même schéma.
  11. **Exercice fil rouge** : CA par magasin × mois × catégorie, avec jointure 4 tables et
     détection de 2 pièges.
- **Livrables spécifiques** : 1 figure SVG « les 4 symptômes de l'explosion de lignes » (un
  diagramme par symptôme).

### C08 — Structurer : sous-requêtes (scalaire, `IN`, `FROM`), CTE (`WITH`), vues, `EXISTS` vs `IN`, style et lisibilité

- **Objectif.** L'apprenant structure une requête complexe en briques lisibles et réutilisables.
- **Plan sommaire** :
  1. Sous-requête scalaire : `SELECT (SELECT MAX(montant) FROM vente) AS top_montant;`.
  2. Sous-requête `IN` : `WHERE id_client IN (SELECT id_client FROM client WHERE ville = 'Ouaga');`.
  3. Sous-requête `FROM` : `FROM (SELECT … FROM …) AS sous_requete;`.
  4. **CTE** (`WITH`) : `WITH ca_magasin AS (SELECT id_magasin, SUM(montant) FROM vente GROUP BY
     id_magasin) SELECT … FROM ca_magasin …`. La lisibilité avant tout.
  5. **Vues** : `CREATE VIEW ca_par_magasin AS SELECT …;`. Une vue est une requête stockée,
     recalculée à chaque appel.
  6. `EXISTS` vs `IN` : `EXISTS` est plus rapide quand la sous-requête peut s'arrêter au premier
     match ; `IN` est plus lisible pour les petites listes.
  7. **Style et lisibilité** : indentation, alias parlants (`m` pour `magasin`, `v` pour `vente`),
     commentaires `--` pour les en-têtes, blocs `WITH` nommés.
  8. **Exercice fil rouge** : réécriture de 3 requêtes du C07 en CTE, et mesure de la lisibilité
     (lignes de code, niveaux d'indentation).
- **Livrables spécifiques** : 1 figure SVG « sous-requête vs CTE vs vue » (les 3 formes de
  structuration).

## 4. Budget pages

| Chapitre | Pages (calibre 12,5) | Estimé |
|---|---|---|
| C01 Le premier contact | 12 | 11-14 |
| C02 Filtrer | 12 | 11-14 |
| C03 Trier, limiter, paginer | 12 | 11-14 |
| C04 Agréger | 12 | 11-14 |
| C05 Résumer par groupe | 12 | 11-14 |
| C06 Catégoriser | 12 | 11-14 |
| C07 Joindre | 12 | 11-14 |
| C08 Structurer | 12 | 11-14 |
| Appareil (couverture, TOC, projet, évaluation) | 17 | 15-20 |
| **Total** | **117** | budget module |

Budget §F.4 = 117 p., tolérance ±15 % = **[99, 135] p.** Si dérive : coupes naturelles en C05
(`GROUP BY` §6 sur la règle d'or), C07 (réduire l'auto-jointure à 1 exemple), C08 (réduire les
styles à 2 plutôt que 3).

## 5. Chiffres cibles (à mesurer dans `chiffres_manuel.py M07`)

- **Base commerciale** : 5 magasins, ~ 1 200 clients, ~ 380 produits, ~ 50 000 ventes.
- **Pièges de fiabilité** : 6 (doublon exact, doublon partiel, retour inclus par erreur, date
  inversée, jointure multiple qui double, NULL dans la condition).
- **30 questions métier** : 6 faciles (1 ligne), 12 moyennes (2-5 lignes), 9 avancées (5-15
  lignes avec CTE), 3 expert (jointure 4 tables + CASE).
- **Empreinte sha256** de la base livrée : à fixer à l'étape 2 (graine).
- **Exemples reproductibles** : 2 exécutions successives de `chiffres_manuel.py M07` → diff = 0
  sur ~ 30 clés `m07p_*`.

## 6. Risques et parades

| Risque | Parade |
|---|---|
| Trop de syntaxe, pas assez de sens | Chaque chapitre commence par *« pourquoi cette clause existe »*, pas par sa grammaire. |
| Confusion `WHERE` vs `HAVING` | Figure dédiée C05, et exercices où la même question est posée avec l'une et l'autre clause. |
| Confusion `INNER` vs `LEFT JOIN` | Tableau C07 §2-3, et exercice où l'audit (jointure externe NULL) repère ce que `INNER` aurait raté. |
| 35 exercices auto-validés trop mécaniques | Chaque exercice a un **énoncé métier** (*« quels clients ont dépensé plus de 500 000 FCFA en mars ? »*), pas un exercice de syntaxe. |
| DucksDB et PostgreSQL syntaxe différente (`ILIKE`, `DISTINCT ON`, `SERIAL`) | Encadrés « DuckDB vs PostgreSQL » dans les chapitres concernés ; règle « DuckDB par défaut, PostgreSQL cité si écart ». |

## 7. Étapes de production (calque M05/M06)

1. **Étape 1 — Plan** (ce document) ✅.
2. **Étape 2 — Socle** : `tools/dossier_M07.py` + `03_exercices/dossier_M07/` + `chiffres_manuel.py
   M07()` (~ 30 clés).
3. **Étape 3 — Rédaction** : 8 chapitres, cadence 1 push par chapitre validé `--strict`.
4. **Étape 4 — Figures** : `tools/figures_M07.py` (8 planches SVG, extension ≤ 776 px, jeu
   latin-1 étendu).
5. **Étape 5 — PDF** : `tools/render.py --join "02_modules/M07_*.md"` → `M07.pdf` (budget 117 p.
   ±15 %).
6. **Étape 6 — Fiche de contrôle** : `05_livrables/fiche_controle_M07.md` Q1-Q10.
7. **Étape 7 — P2** : `03_exercices/M07_projet.md` (3 livrables /20 seuil 13) +
   `04_evaluations/M07_evaluation.md` (20 Q + 35 exercices auto-validés + 1 étude de cas) +
   `README.md` (mise à jour) + push final.
