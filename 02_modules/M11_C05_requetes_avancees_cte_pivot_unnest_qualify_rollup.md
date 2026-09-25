# Module M11.C05 — Requêtes avancées : CTE, tableau croisé, `UNNEST`, `QUALIFY`, récapitulatifs

**Outils : DuckDB 1.5.5 (exécuté), SQLite (contrôle croisé, exécuté), PostgreSQL et SQL Server (cités, non exécutés — règle §1.5.
Durée indicative : 4 h. Niveau : N3 → N4. Prérequis : M11.C01 à C04 (fenêtres, cadres, temps, cohortes) ;
M07.C05 (jointures) ; M05.C04 (tableau croisé dans un tableur).**

> **L'idée du chapitre.** Une requête longue n'est pas une requête compliquée : c'est une requête dont on a
> nommé les étapes. Ce chapitre présente les six outils qui font passer d'un calcul à un **rapport** :
> la table d'expression commune (CTE) qui nomme, le **tableau croisé** qui met les mois en colonnes,
> `QUALIFY` qui classe et filtre dans la même requête, `UNNEST` qui inverse le grain, les
> **récapitulatifs multi-niveaux** qui rendent les sous-totaux dans une seule passe, et la **récursion**,
> précieuse pour les hiérarchies et inutile pour les calendriers. Et parce qu'aucun de ces outils ne
> remplace une donnée propre, le chapitre commence par l'exemple qui le prouve : le référentiel produits du
> socle écrit ses catégories de **16** façons pour **7** familles réelles, et un classement lancé sur les
> libellés bruts rend **16** lignes de réponse pour **7** rayons.

> **Matériel de l'atelier — DuckDB 1.5.5 · socle M11 (`03_exercices/dossier_M11/socle_m11.sql`).**
> **154** produits, **7** familles après repliement, **5** modes de paiement, **3** canaux,
> **145 212** tickets, **15 595 154 955** FCFA. Sorties de l'atelier, exécutées le 24/09/2026.

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous savez :

1. **Découper une requête longue en étapes nommées** avec `WITH`, et réutiliser la même étape plusieurs fois.
2. **Replier un libellé** sans perdre d'information : casse, espaces, accents, pluriel — et **mesurer** ce que
   chaque repliement change au classement.
3. **Croiser deux dimensions** avec `PIVOT` **et** avec l'agrégat conditionnel (`SUM(...) FILTER`), en
   sachant dans quel cas chacun est préférable.
4. **Classer et filtrer dans la même requête** avec `QUALIFY`, sans sous-requête enveloppante.
5. **Inverser un grain** avec `UNNEST`, en redonnant la définition de la ligne obtenue.
6. **Produire un récapitulatif multi-niveaux** (`ROLLUP`, `CUBE`, `GROUPING SETS`) et **distinguer un
   sous-total d'un zéro** avec `GROUPING()`.
7. **Employer la récursion** là où elle sert, et **écrire la version simple** là où elle ne sert pas.

## 2. Pourquoi cette notion est importante

Un rapport de direction ne demande pas « le chiffre d'affaires par mode de paiement » : il demande **le
tableau** — les modes en colonnes, les années en lignes, les sous-totaux, et une ligne de total. En SQL
brut, cette demande produit une requête d'une trentaine de lignes et de trois requêtes collées à la main
dans un tableur. Les outils de ce chapitre font ce travail **dans le moteur**, où le contrôle est possible.

Le chapitre porte aussi un avertissement, et il est mesuré. Le référentiel produits du socle contient
**154** produits répartis en **16** libellés de catégorie qui n'écrivent que **7** familles réelles : la
casse, les espaces finaux, les accents et le pluriel font le reste. Sur ces libellés bruts, un
« meilleur produit par catégorie » rend **16** lignes, dont trois s'appellent Matériaux ; sur les familles
repliées, il en rend **7**. Le même catalogue, la même question, deux rapports incompatibles — et c'est le
repliement du libellé, une étape nommée dans une CTE, qui décide lequel est juste.

Enfin, ces outils ont un **coût de portabilité** : `QUALIFY` n'existe pas en PostgreSQL, `PIVOT` ne s'écrit
pas de la même façon en SQL Server, `UNNEST` se nomme autrement selon les moteurs. Un rapport destiné à
d'autres outils doit le savoir — et le dire.

## 3. Explication simple — la recette, le tableau, l'étagère

**La CTE, c'est la recette étapes par étapes.** Au lieu d'écrire une seule phrase de quinze lignes, on
écrit : « d'abord je prépare la pâte, ensuite je la laisse reposer, enfin je la cuis ». Chaque étape porte un
nom, et une étape peut servir deux fois — c'est même son principal intérêt.

**Le tableau croisé, c'est le tableau à double entrée du cours de mathématiques.** Une liste de
1 000 lignes « mois, mode de paiement, montant » devient un tableau de 4 lignes et 6 colonnes. Rien n'est
ajouté, rien n'est perdu : c'est un changement de **forme**, pas de **fond**.

**`QUALIFY`, c'est le tri suivi du filtre, en un geste.** On numérote les lignes par famille, et on garde
les numéros 1. En SQL classique, il faut deux requêtes imbriquées pour obtenir cela.

**`UNNEST`, c'est renverser une étagère.** Un ticket porte une liste d'articles ; `UNNEST` en fait une ligne
par article. La base grossit d'un coup — **1,63** produit par ticket en moyenne — et le grain change.

**Les récapitulatifs, ce sont les totaux du tableau.** Pas en bas du tableau, collés à la main : **dans** la
requête, avec `ROLLUP`, et une colonne `GROUPING()` qui dit ce qui est un détail et ce qui est un sous-total.

## 4. Vocabulaire essentiel

| Terme (français) | Équivalent anglais | Définition en une phrase |
|---|---|---|
| **table d'expression commune** | *CTE, common table expression* | Un bloc `WITH nom AS (...)` qui donne un nom à une étape intermédiaire. |
| **requête en escalier** | *chained / staged query* | Une requête dont chaque étape est nommée et vérifiable isolément. |
| **repliement d'un libellé** | *normalisation / folding* | Ramener plusieurs graphies d'une même valeur à une seule, par étapes explicites. |
| **famille de produits** | *product family* | Le regroupement le plus large du catalogue, obtenu après repliement du libellé. |
| **tableau croisé** | *pivot / cross-tab* | Une sortie où une dimension passe des lignes aux colonnes. |
| **agrégat conditionnel** | *conditional aggregate* | Un agrégat limité par une condition : `SUM(montant) FILTER (WHERE mode = …)`. |
| **liste** | *list / array* | Une valeur qui contient plusieurs valeurs, produite par `LIST` ou `ARRAY_AGG`. |
| **éclatement** | *unnest / explode* | Transformer une liste en plusieurs lignes. |
| **récapitulatif multi-niveaux** | *rollup / cube / grouping sets* | Un agrégat qui calcule le détail **et** les sous-totaux en une seule requête. |
| **sous-total** | *subtotal* | Une ligne qui agrège un sous-ensemble des lignes détaillées. |
| **indicateur de regroupement** | *grouping()* | La fonction qui distingue un sous-total d'une valeur réellement absente. |
| **récursion** | *recursive CTE* | Une CTE qui se rappelle elle-même pour parcourir une hiérarchie ou une suite. |

> **Définition.** Une **table d'expression commune** — *CTE* — est un bloc `WITH nom AS (requête)` placé
> avant la requête principale. Elle ne stocke rien : elle **nomme**. Son intérêt n'est pas la performance,
> mais le fait qu'on peut exécuter chaque étape séparément, la vérifier, et la réutiliser dans plusieurs
> requêtes. Une requête de rapport lisible est presque toujours une suite de trois à six CTE.

> **Définition.** Le **repliement d'un libellé** consiste à ramener plusieurs graphies d'une même valeur à
> une seule écriture. Il se fait par étapes **explicites** : casse (`UPPER`), espaces (`TRIM`), accents, et
> singulier/pluriel. Chaque étape se mesure — sur le socle, **16** libellés deviennent **9** écritures après
> casse et espaces, puis **7** familles après accents et pluriel. Une étape qu'on ne mesure pas est une
> étape qui a perdu des lignes sans le dire.

> **Définition.** Un **récapitulatif multi-niveaux** est une agrégation qui produit, dans **une** requête,
> le détail et les sous-totaux. `ROLLUP (a, b)` rend le détail par couple, les sous-totaux de `a` et le
> total général ; `CUBE` rend en plus les sous-totaux de `b` seul ; `GROUPING SETS (…)` énumère exactement
> les niveaux voulus. Le nombre de lignes n'est plus celui du détail : il faut donc **nommer** les lignes
> de total, et c'est le rôle de `GROUPING()`.

> **Définition.** Le **grain** d'un jeu de lignes est ce que représente **une** ligne. `UNNEST` le change
> sans prévenir : une ligne « ticket » devient une ligne « article de ticket ». Toute agrégation écrite
> après un `UNNEST` doit être relue à l'aune de ce nouveau grain — sinon `COUNT(*)` compte des articles en
> croyant compter des tickets.

## 5. Cours approfondi

### 5.1 La CTE : nommer les étapes, et réutiliser la bonne

Voici la forme que prend toute requête de rapport un peu longue :

```sql
WITH n AS (
    SELECT id_produit,
           CASE WHEN UPPER(TRIM(categorie)) IN ('MATERIAUX', 'MATÉRIAUX') THEN 'MATÉRIAUX'
                WHEN UPPER(TRIM(categorie)) IN ('PEINTURE', 'PEINTURES') THEN 'PEINTURE'
                WHEN UPPER(TRIM(categorie)) = 'ELECTRICITÉ' THEN 'ÉLECTRICITÉ'
                ELSE UPPER(TRIM(categorie)) END AS famille
    FROM produit
),
ca AS (SELECT n.famille, SUM(v.montant_ttc) AS ca
       FROM ventes v JOIN n USING (id_produit)
       WHERE NOT v.est_retour GROUP BY 1)
SELECT famille, ca, ROUND(100.0 * ca / SUM(ca) OVER (), 2) AS part_pct
FROM ca ORDER BY ca DESC;
```

Trois points à retenir. La CTE **`n`** ne fait qu'une chose : replier le libellé. La CTE **`ca`** ne fait
qu'agréger. La requête finale ne fait qu'ajouter la part, avec une fenêtre sur l'agrégat. Aucune des trois
n'est compliquée, et chacune se vérifie seule : `SELECT * FROM n` doit rendre **154** lignes, avec **7**
familles distinctes.

C'est la **réutilisation** qui fait la valeur d'une CTE : la même CTE `n` sert ensuite à croiser les
familles avec les quartiers, puis avec les années, sans que le repliement soit réécrit — donc sans risque
qu'il soit réécrit **différemment**.

### 5.2 Le tableau croisé : `PIVOT` et l'agrégat conditionnel

Deux écritures produisent le même tableau. La première est DuckDB :

```sql
PIVOT (SELECT YEAR(date_vente) AS an, mode_paiement AS mp, montant_ttc AS m
       FROM ventes WHERE NOT est_retour)
ON mp USING SUM(m) GROUP BY an ORDER BY an;
```

```text
an   | Chèque    | Créance 30 j | Espèces     | Mobile Money | Virement
2023 | 623750816 | 273920936    | 1155573169  | 886824267    | 503512359
2024 | 723192393 | 321227804    | 1393160843  | 1047845325   | 580893385
2025 | 857090551 | 374566410    | 1612526524  | 1228076360   | 652440441
2026 | 593972283 | 262208583    | 1156476174  | 892367109    | 455529223
```

La seconde est du SQL de tous les moteurs :

```sql
SELECT YEAR(date_vente) AS an,
       SUM(montant_ttc) FILTER (WHERE mode_paiement = 'Espèces') AS especes,
       SUM(montant_ttc) FILTER (WHERE mode_paiement = 'Mobile Money') AS mobile,
       SUM(montant_ttc) FILTER (WHERE mode_paiement = 'Chèque') AS cheque
FROM ventes WHERE NOT est_retour GROUP BY 1 ORDER BY 1;
```

Les totaux sont identiques : pour 2023, la somme des cinq colonnes du `PIVOT` vaut **3 443 581 547** FCFA,
exactement le chiffre d'affaires de l'année. Le `PIVOT` est donc un **confort**, pas un moteur de calcul —
et il a un piège de présentation : il range ses colonnes par ordre **alphabétique**.

> **Attention.** `PIVOT` trie les colonnes produites par ordre alphabétique : `Chèque`, `Créance 30 j`,
> `Espèces`, `Mobile Money`, `Virement` — alors que l'ordre des données est `Espèces`, `Mobile Money`,
> `Chèque`, `Virement`, `Créance 30 j`. Un `SELECT *` publié tel quel donne donc un tableau dont l'ordre des
> colonnes n'est pas celui des libellés. Règle : on **nomme** les colonnes dans l'ordre voulu (`SELECT
> Especes, "Mobile Money", Cheque, …`) ou on garde l'agrégat conditionnel, dont l'ordre est écrit à la main.

### 5.3 `QUALIFY` : classer et filtrer dans la même requête

Le classement par groupe de C02 exigeait deux niveaux de requête : un pour le rang, un pour le filtre.
`QUALIFY` (disponible dans DuckDB, Snowflake, BigQuery, Teradata) n'en exige qu'un :

```sql
WITH n AS (SELECT id_produit, CASE … END AS famille FROM produit),
     v AS (SELECT n.famille, p.designation, ROUND(SUM(x.montant_ttc)) AS ca
           FROM ventes x JOIN n USING (id_produit) JOIN produit p USING (id_produit)
           WHERE NOT x.est_retour GROUP BY 1, 2)
SELECT famille, designation, ca FROM v
QUALIFY ROW_NUMBER() OVER (PARTITION BY famille ORDER BY ca DESC, designation) = 1
ORDER BY ca DESC;
```

```text
MATÉRIAUX     | Gravier 15/25 (m3) — réf 1        | 351651755
PLOMBERIE     | Lavabo céramique — réf 2          | 349907568
BOIS & PANNEAUX | Panneau MDF 12 mm — réf 2       | 255397413
ÉLECTRICITÉ   | Lampe solaire murale — réf 2      | 132272554
QUINCAILLERIE | Pince coupante 200 mm — réf 2     | 119995326
PEINTURE      | Antirouille rouge brique 1 L — réf 2 | 110331930
CONSOMMABLES  | Pelle carrée — réf 1              | 101865391
```

**7** lignes, une par famille, et le départage est explicite (`ca DESC, designation`) — sans lui, deux
produits à égalité de chiffre d'affaires changeraient de place d'une exécution à l'autre (leçon de C04).

> **Attention.** Le **même** `QUALIFY` écrit sur les libellés bruts de `produit.categorie` rend **16**
> lignes — pour **7** familles réelles. Trois de ces lignes s'appellent Matériaux (`MATERIAUX`,
> `Materiaux`, `Matériaux `), et trois autres Quincaillerie. Le tableau est parfaitement exécuté, et il
> présente trois fois le même rayon : `QUALIFY` ne remplace pas la propreté des données, il la rend
> seulement plus visible.

### 5.4 `UNNEST` : inverser le grain

Un ticket contient une liste d'articles. Pour obtenir une ligne par article — le grain du détail — on
éclate la liste :

```sql
WITH t AS (SELECT v.id_ticket, LIST(DISTINCT p.designation ORDER BY p.designation) AS lp
           FROM ventes v JOIN produit p USING (id_produit)
           WHERE NOT v.est_retour AND v.id_ticket = (SELECT MIN(id_ticket) FROM ventes)
           GROUP BY 1)
SELECT id_ticket, UNNEST(lp) AS designation FROM t;
```

```text
T01-230101-000000 | Mètre ruban 5 m — réf 1
```

Le premier ticket du socle ne porte qu'une désignation, mais le maximum observé est de **4** produits
(**1,63** en moyenne, **1** en médiane sur **145 212** tickets). L'opération est donc asymétrique : elle
multiplie la base, et pas d'un facteur constant.

### 5.5 Les récapitulatifs : `ROLLUP`, `CUBE`, `GROUPING SETS`

Un tableau de direction comporte des sous-totaux. Sans récapitulatif, il faut trois requêtes et un
recollage manuel ; avec, une seule :

```sql
WITH n AS (SELECT id_produit, CASE … END AS f FROM produit),
     b AS (SELECT ma.quartier AS q, n.f, SUM(v.montant_ttc) AS ca
           FROM ventes v JOIN magasin ma USING (id_magasin)
           JOIN n USING (id_produit) WHERE NOT v.est_retour GROUP BY 1, 2)
SELECT COALESCE(q, 'TOTAL') AS quartier, COALESCE(f, 'sous-total') AS famille,
       GROUPING(q) AS gq, GROUPING(f) AS gf, ROUND(SUM(ca)) AS ca
FROM b GROUP BY ROLLUP (q, f) ORDER BY gq, quartier, gf, famille;
```

**41** lignes : **35** couples détail, **5** sous-totaux de quartier, **1** total général
(**15 595 154 955** FCFA). Les deux colonnes `GROUPING()` disent, ligne par ligne, ce qui est du détail
(`0`) et ce qui est un sous-total (`1`) — sans elles, un `NULL` de sous-total se confondrait avec une
famille non renseignée.

`GROUPING SETS` répond à un autre besoin : quand on veut certains niveaux **sans** les autres. Sur le même
socle, `GROUPING SETS ((quartier), (famille), (quartier, famille))` rend **47** lignes — **5** quartiers,
**7** familles, **35** couples — chacune à son propre grain.

> **Dans les faits.** Le tableau croisé des modes de paiement rend la période partielle **visible d'un
> coup d'œil** : les cinq colonnes progressent de 2023 à 2025, puis reculent toutes ensemble en 2026 — qui
> ne compte que **8** mois (C03, §5.3). Aucun commentaire n'était nécessaire : la forme du tableau le dit.

### 5.6 La récursion : pour les hiérarchies, pas pour les calendriers

`WITH RECURSIVE` fait se rappeler une requête elle-même. Le cas d'école — la suite des mois — se résout
plus simplement avec `generate_series` :

```sql
WITH RECURSIVE m AS (SELECT DATE '2023-01-01' AS d
                     UNION ALL SELECT d + INTERVAL 1 MONTH FROM m WHERE d < DATE '2026-08-01')
SELECT COUNT(*) AS mois FROM m;
```

**44** — la même série que la table calendrier de C03, en plus verbeux et plus lent. La récursion mérite
d'être écrite quand la **profondeur** est inconnue : arborescence d'organisation, nomenclature de produits,
chaîne d'approbation. Sur un catalogue à deux niveaux (famille, sous-catégorie) et **29** couples, elle est
un luxe ; sur un arbre d'articles imbriqué sur sept niveaux, elle est la seule solution.

### 5.7 Ce que chaque moteur sait faire

| Élément | DuckDB (exécuté) | PostgreSQL (cité) | SQL Server (cité) |
|---|---|---|---|
| `WITH` (CTE) | oui | oui | oui |
| `WITH RECURSIVE` | oui | oui | oui, sans le mot `RECURSIVE` |
| `QUALIFY` | oui | **non** : sous-requête obligatoire | **non** : `TOP` ou `ROW_NUMBER` |
| `PIVOT` | oui, `PIVOT (…) ON … USING …` | **non** : `crosstab` (extension) ou agrégat conditionnel | oui, `PIVOT (…) FOR … IN (…)` |
| `UNNEST` | oui | `unnest()` | `OPENJSON` / `STRING_SPLIT` selon la source |
| `ROLLUP` / `CUBE` / `GROUPING SETS` | oui | `ROLLUP`, `CUBE`, `GROUPING SETS` | idem, `GROUPING()` fourni |

> **Attention.** Ce tableau distingue trois colonnes qui ne pèsent pas pareil : DuckDB a été **exécuté**
> pour chaque ligne, PostgreSQL et SQL Server sont **cités** — aucune ligne de cette colonne n'a été jouée
> dans l'atelier. C'est la règle §1.5 du manuel, et elle vaut pour la syntaxe comme pour les chiffres : un
> rapport qui publie du code non exécuté le **déclare**.

> **Conseil professionnel.** Écrivez le tableau croisé d'un rapport récurrent en **agrégat conditionnel**,
> même si votre moteur sait faire `PIVOT`. Trois raisons : les colonnes y sont nommées dans l'ordre voulu,
> une période sans donnée y sort à `NULL` au lieu de disparaître, et le code s'exécute partout. Gardez
> `PIVOT` pour l'exploration, là où la liste des colonnes n'est pas connue d'avance.

### 5.8 Ce que ce chapitre ne couvre pas

La **performance** de ces constructions — coût du `PIVOT`, effet d'un index, lecture d'un plan d'exécution —
est le sujet de C06. Reste ici une règle : aucun de ces outils ne rend une requête rapide ; ils la rendent
**lisible**, ce qui est la condition pour pouvoir un jour la rendre rapide.

## 6. Exemple concret — le tableau que la direction avait demandé

La demande : « le chiffre d'affaires par quartier et par famille, avec les sous-totaux, pour les quatre
années ». La réponse tient en deux étapes nommées et un `ROLLUP`. Ce que la direction reçoit :

- **41** lignes, dont **5** sous-totaux de quartier et **1** total général de **15 595 154 955** FCFA ;
- un détail par couple quartier × famille, où les familles se nomment MATÉRIAUX, PLOMBERIE, ÉLECTRICITÉ,
  QUINCAILLERIE, BOIS & PANNEAUX, CONSOMMABLES et PEINTURE — **7** familles, pas **16** libellés ;
- et les deux familles de tête à **3 535 582 421** et **3 452 082 064** FCFA, soit **0,5** point d'écart.

Ce dernier point est le plus utile au comité : sur ce catalogue, savoir laquelle de MATÉRIAUX et de
PLOMBERIE arrive en tête dépend **du repliement des libellés**. La réponse honnête n'est pas « Matériaux
est premier », c'est « les deux sont à égalité, à 0,5 point près ».

## 7. Démonstration pas à pas — six étapes sur le socle

### 7.1 Étape 1 — le repliement mesuré

`SELECT COUNT(DISTINCT categorie) FROM produit` → **16**. Après `UPPER(TRIM(...))` → **9**. Après repliement
des accents et du pluriel → **7**. Trois nombres, trois définitions du catalogue.

### 7.2 Étape 2 — la CTE réutilisée

La CTE `n` du §5.1 sert trois fois : classement par famille, croisement avec les quartiers, croisement avec
les années. Une seule définition du repliement, donc un seul classement possible.

### 7.3 Étape 3 — le tableau croisé

Le `PIVOT` des modes de paiement par année (§5.2) et sa vérification : la somme des cinq colonnes de 2023
égale **3 443 581 547** FCFA, le chiffre d'affaires de l'année. Puis la même table en agrégat conditionnel,
pour constater que les colonnes y sont dans l'ordre métier.

### 7.4 Étape 4 — `QUALIFY` avec et sans repliement

**7** lignes avec la CTE de repliement, **16** sans. C'est la démonstration la plus courte du chapitre : un
outil puissant posé sur des données sales produit une réponse fausse **plus vite**.

### 7.5 Étape 5 — `UNNEST` et le grain

Le premier ticket du socle (`T01-230101-000000`) ne porte qu'une désignation ; le maximum est de **4**
produits par ticket. Après éclatement, la base ne compte plus **145 212** tickets mais des lignes
d'articles : tout `COUNT(*)` écrit ensuite compte **des articles**.

### 7.6 Étape 6 — le récapitulatif

**41** lignes en `ROLLUP` (35 + 5 + 1), **47** en `GROUPING SETS` (5 + 7 + 35). Le contrôle tient en une
requête : le total général du récapitulatif doit être **égal** au chiffre d'affaires net du socle
(**15 595 154 955** FCFA). S'il diffère, un `NULL` a été compté comme un zéro, ou un `GROUPING` a été oublié.

## 8. Erreurs fréquentes

1. **Croire que la CTE accélère.** Elle nomme. Un moteur peut la recalculer plusieurs fois ; c'est un
   excellent découpage de lecture et pas une optimisation. La performance se mesure (C06).
2. **Publier un `PIVOT` en `SELECT *`.** Les colonnes sortent par ordre alphabétique — `Chèque` avant
   `Espèces` — et le tableau publié n'a plus l'ordre du métier.
3. **Classer sur les libellés bruts.** **16** lignes pour **7** familles : le même rayon apparaît trois fois
   sous trois graphies (Matériaux, materiaux, MATÉRIAUX ).
4. **Agréger après un `UNNEST` sans redéfinir le grain.** Les tickets deviennent des articles
   (**1,63** par ticket en moyenne) : un `COUNT(*)` compare alors des articles à des tickets.
5. **Confondre un `NULL` de sous-total et une valeur absente.** Sans `GROUPING()`, la ligne de total général
   ressemble à une ligne dont la dimension est vide — et un lecteur pressé la somme comme un détail.
6. **Recopier une syntaxe non exécutée.** `QUALIFY` en PostgreSQL et `PIVOT … ON … USING` en SQL Server
   n'existent pas : un rapport portable s'écrit en agrégat conditionnel.

## 9. Bonnes pratiques professionnelles

1. **Une étape nommée par intention.** `n` pour le repliement, `ca` pour l'agrégat, `rg` pour le rang :
   une CTE qui s'appelle `tmp` empêche la relecture.
2. **Mesurer chaque repliement.** **16** → **9** → **7** : chaque étape publie son compte avant d'être
   utilisée dans un rapport.
3. **Nommer les colonnes d'un tableau croisé.** Jamais `SELECT *` sur un `PIVOT` ; l'ordre des colonnes fait
   partie de la donnée.
4. **Écrire le départage de tout classement.** `ORDER BY ca DESC, designation` : la leçon de C04 vaut pour
   `QUALIFY` comme pour `ROW_NUMBER`.
5. **Vérifier le total des récapitulatifs** contre le total de référence (**15 595 154 955** FCFA), et
   déclarer les niveaux calculés. Un sous-total non vérifié est un chiffre de plus à défendre.

## 10. Exercice guidé

**Situation.** La direction commerciale veut un tableau unique : les **7** familles en lignes, les
**4** années en colonnes, le total par famille à droite, le total par année en bas, et la part de chaque case.

**Consigne.**

1. Écrivez la CTE de repliement des libellés, et donnez ses trois comptes : libellés bruts, écritures,
   familles. (2 pts)
2. Produisez le tableau croisé des familles par année, en **agrégat conditionnel**, avec les colonnes dans
   l'ordre des années. (3 pts)
3. Ajoutez les sous-totaux de ligne et de colonne, et dites par quelle construction ils sont produits.
   (3 pts)
4. Expliquez, en deux phrases, pourquoi il ne faut **pas** écrire ce tableau en `SELECT *` sur un `PIVOT`.
   (2 pts)

## 11. Exercices autonomes

**E1 — Trois façons, un seul tableau (40 min).** Produisez le croisement quartiers × familles : (a) en
`PIVOT`, (b) en agrégat conditionnel, (c) en `GROUPING SETS`. Puis répondez en quatre lignes : quel tableau
porte des sous-totaux, lequel a les colonnes dans l'ordre métier, et lequel faudrait-il publier si le
rapport partait vers un moteur qui ignore `PIVOT`.

**E2 — Le panier du premier ticket, et sa généralisation (35 min).** À partir de la CTE qui éclate un
ticket en lignes, calculez la composition moyenne d'un ticket par famille de produits. Contrainte : le
grain doit être redit — une ligne par article — et le total des articles doit être confronté aux
**145 212** tickets du socle.

## 12. Correction détaillée

**Exercice guidé.**

1. **Les trois comptes.** **16** libellés bruts, **9** écritures après `UPPER(TRIM(...))`, **7** familles
   après repliement des accents (`MATÉRIAUX`/`MATERIAUX`, `ELECTRICITÉ`) et du pluriel
   (`PEINTURE`/`PEINTURES`). La CTE écrit ces trois règles une fois pour toutes.
2. **Le tableau.** `SUM(montant_ttc) FILTER (WHERE YEAR(date_vente) = 2023) AS ca_2023`, puis 2024, 2025,
   2026, avec `GROUP BY famille` sur la CTE de repliement. Colonnes dans l'ordre chronologique, comme dans
   le rapport.
3. **Les sous-totaux.** `GROUP BY ROLLUP (famille, annee)` : les cellules, les sous-totaux de famille, les
   sous-totaux d'année et le total général dans la **même** requête — **41** lignes pour le croisement
   quartier × famille, et la même structure ici. `GROUPING(famille)` et `GROUPING(annee)` nomment les
   lignes de total.
4. **Pourquoi pas `SELECT *`.** Parce que `PIVOT` produit ses colonnes par ordre alphabétique : les années
   seraient bien ordonnées (`2023`, `2024`…), mais des libellés comme `Chèque` et `Espèces` se retrouveraient
   dans l'ordre inverse de celui du métier — et le tableau publié serait, à la lettre, un autre tableau.

**E1 (trois façons).** (a) Le `PIVOT` est le plus court à écrire et le moins contrôlable : colonnes
alphabétiques, aucune notion de sous-total. (b) L'agrégat conditionnel donne l'ordre métier des colonnes et
fonctionne partout, mais les sous-totaux demandent un `ROLLUP` supplémentaire ou une requête d'union. (c) Le
`GROUPING SETS` est le seul qui produit les trois niveaux en une passe, au prix d'une lecture plus difficile.
Pour un rapport qui part vers un moteur sans `PIVOT` : l'agrégat conditionnel, éventuellement enveloppé
dans un `GROUPING SETS`.

**E2 (le panier éclaté).** Après éclatement, la base compte les lignes d'articles, pas les tickets : le
nombre de lignes dépasse nécessairement la médiane de **1** produit par ticket, et le total des articles
doit être comparé aux **145 212** tickets — jamais confondu avec eux. La composition moyenne par famille se
lit alors par ticket et non par ligne d'article : le dénominateur est le nombre de **tickets**, pas le
nombre de lignes éclatées.

## 13. Mini-projet de chapitre

**Le tableau de bord d'une famille de produits, 2 pages.** Choisissez une famille du catalogue et produisez
son tableau de bord : ventes par année, par quartier et par mode de paiement, avec sous-totaux et parts,
plus le top 3 des désignations.

**Livrables et barème.**

| Critère | Ce qui est vérifié | Points |
|---|---|---|
| La CTE de repliement | les trois comptes (16 / 9 / 7) publiés, une seule définition | 5 |
| Le tableau croisé | deux dimensions croisées, colonnes nommées dans l'ordre métier | 5 |
| Les sous-totaux | produits par `ROLLUP` ou `GROUPING SETS`, `GROUPING()` utilisé, total vérifié | 5 |
| Le top 3 | `QUALIFY` avec départage explicite, une ligne par désignation | 3 |
| **Total** | | **18** |

## 14. Résumé du chapitre

Six outils, une même idée : rendre une requête longue **lisible et vérifiable**. La **CTE** nomme les
étapes et se réutilise — c'est elle qui porte le repliement des libellés (**16** → **9** → **7**). Le
**tableau croisé** change la forme sans changer le fond, et l'agrégat conditionnel le fait partout, avec des
colonnes dans l'ordre métier — là où `PIVOT` trie alphabétiquement. `QUALIFY` classe et filtre en une passe :
**7** lignes sur les familles repliées, **16** sur les libellés bruts, et c'est la donnée qui décide, pas
l'outil. `UNNEST` inverse le grain (**1,63** produit par ticket en moyenne, **4** au maximum) et oblige à
redire ce qu'est une ligne. Les **récapitulatifs** rendent le détail et les sous-totaux ensemble — **41**
lignes en `ROLLUP`, **47** en `GROUPING SETS` — à condition que `GROUPING()` distingue un total d'un `NULL`.
Et la **récursion** sert les hiérarchies : pour les **44** mois du socle, `generate_series` fait le travail
en une ligne.

## 15. À retenir

1. **Une requête longue se découpe en étapes nommées.** Une étape qu'on ne peut pas exécuter seule ne peut
   pas être vérifiée.
2. **Un repliement de libellé se mesure à chaque étape.** **16** libellés, **9** écritures, **7** familles :
   trois nombres à publier avant tout classement.
3. **`PIVOT` range ses colonnes par ordre alphabétique.** Le tableau publié doit nommer ses colonnes.
4. **`QUALIFY` ne nettoie pas les données, il les rend visibles.** **16** lignes pour **7** rayons.
5. **`UNNEST` change le grain.** Après éclatement, la ligne est un article, plus un ticket.
6. **`GROUPING()` sépare un sous-total d'une absence.** Sans lui, un total général se lit comme un détail.
7. **La récursion est faite pour les hiérarchies**, pas pour égrener **44** mois.

> **À retenir.** Le chiffre qui résume le chapitre n'est pas un total : c'est la paire **16** / **7**. Seize
> façons d'écrire sept rayons, et un outil avancé qui publie seize lignes sans broncher. Le nettoyage des
> libellés n'est pas une étape préparatoire qu'on repousse : c'est la première CTE du rapport.

> **À retenir.** Les deux familles de tête du catalogue sont à **0,5** point l'une de l'autre
> (**3 535 582 421** et **3 452 082 064** FCFA). Un rapport qui annonce « Matériaux est notre première
> famille » énonce donc moins une vérité qu'une conséquence de son propre repliement.

## 16. Évaluation formative

Répondez sans machine, puis vérifiez avec l'atelier (5 minutes) :

1. Combien de libellés de catégorie compte le référentiel produits, combien d'écritures après casse et
   espaces, combien de familles après accents et pluriel ?
2. Que produit un « meilleur produit par catégorie » écrit sur les libellés bruts, et pourquoi est-ce un
   problème ?
3. Dans quel ordre `PIVOT` range-t-il ses colonnes, et pourquoi est-ce gênant pour un rapport ?
4. Quelle écriture du tableau croisé fonctionne dans tous les moteurs, et pourquoi ?
5. Que change `UNNEST` au grain d'une table, et quel chiffre du socle le rappelle ?
6. Combien de lignes rend `ROLLUP (quartier, famille)`, et comment se décomposent-elles ?
7. À quoi sert `GROUPING()`, et que se passe-t-il si on l'oublie ?
8. Combien de lignes rend `GROUPING SETS ((quartier), (famille), (quartier, famille))`, et de quoi sont-elles
   faites ?
9. Quand la récursion est-elle préférable à `generate_series`, et pourquoi ?
10. Quelles sont les deux familles de tête du catalogue, et de combien d'écart ?

**Réponses.** 1. **16** libellés, **9** écritures, **7** familles. 2. **16** lignes, dont trois graphies du
même rayon : le classement dépend du libellé et non du produit. 3. Par ordre **alphabétique** (`Chèque`,
`Créance 30 j`, `Espèces`…), alors que l'ordre métier est `Espèces`, `Mobile Money`, `Chèque`, `Virement`,
`Créance 30 j`. 4. L'**agrégat conditionnel** (`SUM(...) FILTER (WHERE ...)`) : colonnes nommées dans
l'ordre voulu, `NULL` préservé, et syntaxe portable. 5. Il fait passer d'une ligne par ticket à une ligne
par article — **1,63** produit par ticket en moyenne, **4** au maximum. 6. **41** lignes : **35** couples,
**5** sous-totaux de quartier, **1** total général. 7. À distinguer un sous-total d'une valeur absente ;
sans lui, la ligne de total général se lit comme une ligne de détail. 8. **47** lignes : **5** quartiers,
**7** familles, **35** couples. 9. Quand la profondeur de la hiérarchie n'est pas connue d'avance — un
arbre d'organisation, pas une suite de **44** mois. 10. **MATÉRIAUX** (**3 535 582 421** FCFA) et
**PLOMBERIE** (**3 452 082 064** FCFA), à **0,5** point près.
