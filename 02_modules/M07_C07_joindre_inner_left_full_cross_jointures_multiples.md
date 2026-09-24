# Module M07.C07 — Joindre : INNER, LEFT, FULL, CROSS, jointures multiples

**Outils comparés : DuckDB 1.5.5 (CLI + Python), SQLite natif Python, PostgreSQL cité.
Durée indicative : 5 h. Niveau : N2 → N3. Prérequis : M07.C01 (SELECT, FROM, alias) ; M07.C05 (GROUP BY) ; M07.C06 (CASE).**

> **L'idée du chapitre.** C04–C06 travaillaient sur **une table à la fois** (ou sur des
> agrégats d'une table). C07 brise cette limite : **relier plusieurs tables** par leurs
> clés. « Le CA de chaque vente, avec le nom du client et la ville du magasin. » « Les
> magasins qui n'ont pas encore d'objectif. » C'est la **jointure** — *join* : l'opération
> qui fait d'un schéma en 9 tables un ensemble interrogeable. Le chapitre couvre
> `INNER JOIN` (les correspondances des deux côtés), `LEFT JOIN` (garder le côté gauche,
> `NULL` à droite), `FULL OUTER JOIN` (les deux côtés), `CROSS JOIN` (le produit
> cartésien), les **jointures multiples en étoile**, et les deux pièges du module —
> **P4** (la jointure qui double les lignes) et **P5** (le `DISTINCT` qui masque un
> mauvais `JOIN`). Le fil rouge est la base `commercial.duckdb` : on y relie 50 008 ventes
> à leurs 1 200 clients, 380 produits, 5 magasins et 5 modes de paiement, et on montre
> qu'une jointure mal conçue gonfle 50 008 lignes en **2 131 064**.

> **Base de travail — `commercial.duckdb` (empreinte `0b9c12397d9c8af2…`).** Le chapitre
> mobilise : 50 008 ventes, 1 200 clients (tous présents dans `vente`), 380 produits (tous
> vendus au moins une fois), 5 magasins, 5 modes de paiement, 8 catégories, et la table
> `objectif_magasin` **vide** (0 lignes) — un objet de démonstration idéal pour le
> `LEFT JOIN` (elle produit des `NULL` réels).

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous saurez :

- **relier deux tables** par une clé avec `INNER JOIN … ON` et comprendre le résultat
  (les correspondances des deux côtés) ;
- **garder le côté gauche** avec `LEFT JOIN` et interpréter les `NULL` du côté droit
  (les lignes sans correspondance) ;
- **garder les deux côtés** avec `FULL OUTER JOIN` ;
- **produire le produit cartésien** avec `CROSS JOIN` et savoir quand c'est voulu ;
- **enchaîner plusieurs jointures** en étoile autour d'une table centrale (`vente`) ;
- **détecter** une jointure qui double les lignes (piège P4) et un `DISTINCT` qui masque
  un mauvais `JOIN` (piège P5).

## 2. Pourquoi cette notion est importante

- **Toute interrogation métier multi-table est une jointure** : « le CA par client avec son
  nom », « les ventes de chaque ville ». Un schéma en 9 tables (le socle M07) ne devient
  lisible qu'au travers de jointures.
- **Le choix de type de jointure est une décision sémantique** : `INNER` répond à « les
  ventes **qui ont** un client » ; `LEFT` répond à « **tous** les magasins, avec leur
  objectif s'il existe ». Se tromper de type, c'est répondre à une autre question.
- **Les pièges P4/P5 sont les bugs les plus coûteux en production** : un total gonflé par
  une jointure qui double, ou un `DISTINCT` qui « répare » un mauvais `JOIN` sans que
  personne ne le sache.

## 3. Explication simple — la jointure est un accord de clés

Imaginez deux fiches : une **vente** (qui note `id_client = 73`) et un fichier des
**clients** (une fiche par `id_client`). La jointure `vente JOIN client ON vente.id_client
= client.id_client` fait l'**accord** : pour chaque vente, on retrouve la fiche du client
de même `id`, et on met les deux côte à côte. Le résultat a **les colonnes des deux
tables**, et **autant de lignes qu'il y a de paires accordées**.

`INNER JOIN` = « ne gardez que les paires qui se sont accordées ». `LEFT JOIN` = « gardez
toutes les ventes, même celles qui n'ont trouvé aucun client (elles seront complétées de
`NULL` à droite) ». C'est tout.

> **Définition.** Une **jointure** — *join* — est l'opération qui met côte à côte les
> lignes de deux tables (ou plus) qui **s'accordent sur une clé**, via `ON` (par exemple
> `v.id_client = c.id_client`). Le résultat combine les colonnes des deux tables. Le type
> de jointure (`INNER`, `LEFT`, `FULL`, `CROSS`) décide quelles paires sont conservées.

## 4. Vocabulaire essentiel

| Français — English | Définition simple | Piège à éviter |
|---|---|---|
| **INNER JOIN** | les paires qui se sont accordées des **deux** côtés. | croire qu'elle garde toutes les lignes (elle les filtre). |
| **LEFT JOIN** | toutes les lignes du **gauche**, `NULL` à droite si aucune correspondance. | mettre le filtre du côté droit dans `WHERE` (il transforme le `LEFT` en `INNER`). |
| **FULL OUTER JOIN** | toutes les lignes des **deux** côtés, `NULL` où il manque. | le confondre avec `LEFT` (il garde aussi le droit seul). |
| **CROSS JOIN** | le **produit cartésien** : chaque ligne du gauche × chaque ligne du droit. | l'employer par accident (oubli de `ON`) : explosion de lignes. |
| **clé de jointure** | la (les) colonne(s) comparée(s) dans `ON`. | joindre sur une colonne non unique (doublons) sans le savoir. |
| **jointure en étoile** | une table centrale (`vente`) reliée à N tables de référence. | joindre les tables de référence entre elles (inutile, et source de doublons). |
| **explosion de jointure** | une jointure qui multiplie les lignes au lieu de les enrichir (P4). | ne pas vérifier `COUNT(*)` avant/après la jointure. |
| **ON vs WHERE** | `ON` définit l'accord ; `WHERE` filtre **après** (pour `LEFT`, le sens change). | mettre la condition du côté droit d'un `LEFT` dans `WHERE` (il filtre les `NULL`). |

## 5. Cours approfondi

### 5.1 `INNER JOIN` — les correspondances des deux côtés

```sql
SELECT v.id_vente, c.nom, v.montant_ttc
FROM vente v
INNER JOIN client c ON c.id_client = v.id_client
ORDER BY v.id_vente
LIMIT 3;
```

Chaque vente retrouve le client de même `id_client`. Sur le socle, **toutes** les ventes
ont un client existant (1 200 clients, tous présents dans `vente`) : le `INNER JOIN`
retourne donc 50 008 lignes, chacune enrichie du `nom` du client.

```sql
SELECT COUNT(*) AS nb_lignes
FROM vente v
INNER JOIN client c ON c.id_client = v.id_client;
```

→ **50 008** (aucune vente orpheline dans le socle). Le `INNER JOIN` n'a rien filtré
parce que la clé `id_client` de `vente` pointe toujours vers un client existant — c'est la
propriété d'intégrité référentielle que le socle garantit.

> **Définition.** La **clé étrangère** — *foreign key* (FK) — est la colonne d'une table
> qui pointe vers la clé primaire d'une autre table (`vente.id_client` →
> `client.id_client`). Une jointure `INNER` sur une FK intègre ne supprime jamais de ligne
> de la table centrale ; une FK **orpheline** (qui pointe vers une clé inexistante) serait,
> elle, éliminée par le `INNER JOIN`.

### 5.2 `LEFT JOIN` — garder le côté gauche, `NULL` à droite

La table `objectif_magasin` est **vide** (0 lignes) dans le socle. Le `LEFT JOIN` depuis
`magasin` est donc l'objet de démonstration idéal : chaque magasin reste, et son objectif
apparaît en `NULL`.

```sql
SELECT m.id_magasin, m.nom, o.ca_objectif_ttc
FROM magasin m
LEFT JOIN objectif_magasin o ON o.id_magasin = m.id_magasin
ORDER BY m.id_magasin;
```

| id_magasin | nom             | ca_objectif_ttc |
|------------|-----------------|-----------------|
| 1          | Ouaga Centre    | NULL            |
| 2          | Ouaga Patte d'Oie | NULL          |
| 3          | Bobo Centre     | NULL            |
| 4          | Bobo Sarfalao   | NULL            |
| 5          | Koudougou       | NULL            |

Cinq magasins, cinq lignes, **tous les objectifs en `NULL`** (la table de droite étant
vide). C'est exactement le comportement voulu : « tous les magasins, avec leur objectif
**s'il existe** ». Un `INNER JOIN` ici retournerait **0 ligne** (aucune paire accordée),
ce qui serait une erreur de réponse.

### 5.3 Le piège du `WHERE` sur le côté droit d'un `LEFT JOIN`

```sql
-- MAUVAIS : le filtre sur o élimine les NULL et transforme le LEFT en INNER
SELECT m.nom, o.ca_objectif_ttc
FROM magasin m
LEFT JOIN objectif_magasin o ON o.id_magasin = m.id_magasin
WHERE o.ca_objectif_ttc > 0;
```

```sql
-- JUSTE : la condition sur le côté droit va dans ON
SELECT m.nom, o.ca_objectif_ttc
FROM magasin m
LEFT JOIN objectif_magasin o ON o.id_magasin = m.id_magasin
    AND o.ca_objectif_ttc > 0
ORDER BY m.id_magasin;
```

Dans le `WHERE`, les lignes dont `ca_objectif_ttc` est `NULL` sont **éliminées** (car
`NULL > 0` est `NULL`, ni vrai ni faux) : le `LEFT JOIN` se comporte comme un `INNER`.
Dans l'`ON`, la condition ne filtre pas le côté gauche : les magasins sans objectif restent,
`NULL` à droite.

> **Attention.** Mettre la condition du **côté droit** d'un `LEFT JOIN` dans le `WHERE`
> transforme silencieusement la jointure en `INNER` (les `NULL` du droit sont éliminés).
> Pour filtrer le côté droit sans perdre le gauche, écrire la condition dans l'`ON`.
> C'est le piège de jointure le plus fréquent en production.

### 5.4 `FULL OUTER JOIN` — les deux côtés

`FULL OUTER JOIN` garde **toutes** les lignes des deux tables : celles qui s'accordent,
celles du gauche sans correspondance (`NULL` à droite), celles du droit sans
correspondance (`NULL` à gauche).

```sql
SELECT m.id_magasin, m.nom, o.annee
FROM magasin m
FULL OUTER JOIN objectif_magasin o ON o.id_magasin = m.id_magasin
ORDER BY m.id_magasin;
```

→ 5 lignes (les 5 magasins, `annee` en `NULL`) — ici identique au `LEFT JOIN` car la table
de droite est vide (il n'y a pas de ligne du droit « seule »). Sur deux tables toutes deux
peuplées et partiellement disjointes, le `FULL` ajouterait les lignes orphelines du droit.

### 5.5 `CROSS JOIN` — le produit cartésien

`CROSS JOIN` produit **toutes les paires** (chaque ligne du gauche × chaque ligne du
droit), sans condition. 5 magasins × 5 modes de paiement = **25 lignes** :

```sql
SELECT m.nom, mp.libelle
FROM magasin m
CROSS JOIN mode_paiement mp
ORDER BY m.id_magasin, mp.id_mode;
```

→ 25 combinaisons (chacun des 5 magasins avec chacun des 5 modes). C'est voulu quand on
veut une **grille complète** (tous les couples, même ceux à zéro) ; c'est un bug quand on
l'obtient par oubli de `ON` (une jointure qui explose).

> **Définition.** Le **produit cartésien** — *cross product* — est l'ensemble de toutes les
> paires (ligne du gauche × ligne du droit), sans condition : `|gauche| × |droit|` lignes.
> `CROSS JOIN` l'explicite (grille complète voulue) ; une `JOIN` sans `ON` (ou un `ON`
> toujours vrai) le produit par accident (explosion de lignes, cf. P4).

### 5.6 Jointures multiples en étoile

La table centrale `vente` se relie à **quatre** tables de référence (client, produit,
magasin, mode_paiement) — la **jointure en étoile**. On n'enchaîne que des `N → 1` (chaque
vente pointe vers une seule valeur de référence) : le résultat garde 50 008 lignes.

```sql
SELECT v.id_vente,
       c.nom AS client,
       p.designation AS produit,
       m.nom AS magasin,
       mp.libelle AS mode,
       v.montant_ttc
FROM vente v
JOIN client c        ON c.id_client   = v.id_client
JOIN produit p       ON p.id_produit  = v.id_produit
JOIN magasin m       ON m.id_magasin  = v.id_magasin
JOIN mode_paiement mp ON mp.id_mode   = v.id_mode
ORDER BY v.id_vente
LIMIT 3;
```

```sql
SELECT COUNT(*) AS nb_lignes
FROM vente v
JOIN client c        ON c.id_client   = v.id_client
JOIN produit p       ON p.id_produit  = v.id_produit
JOIN magasin m       ON m.id_magasin  = v.id_magasin
JOIN mode_paiement mp ON mp.id_mode   = v.id_mode;
```

→ **50 008** (chaque vente enrichie de 4 libellés, sans doublon). C'est le motif de
référence de tout « rapport détaillé ».

> **À retenir.** Une jointure en étoile ne **double jamais** les lignes tant que chaque
> relation est `N → 1` (une vente pointe vers un seul client, un seul produit, un seul
> magasin, un seul mode). Le contrôle est immédiat : `COUNT(*)` après l'étoile doit
> redonner le `COUNT(*)` de la table centrale. S'il ne redonne pas, une relation a
> multiplicé — c'est P4.

### 5.7 Le piège P4 — la jointure qui double

Le piège P4 : une jointure qui **multiplie** les lignes. Le cas d'école : relier `vente`
à elle-même via `id_client` (chaque vente « s'accorde » avec **toutes** les ventes du même
client) :

```sql
SELECT COUNT(*) AS nb_lignes_explosees
FROM vente v
JOIN vente v2 ON v2.id_client = v.id_client;
```

→ **2 131 064 lignes** pour 50 008 ventes uniques. Chaque vente est comptée une fois par
chacune des autres ventes de son client (son nombre de ventes + 1). Le `COUNT(*)` est
**gonflé d'un facteur ~42**. La bonne pratique : compter les ventes uniques
(`COUNT(DISTINCT v.id_vente)` → 50 008), et ne joindre que des relations `N → 1` (jamais
`N → N` sur la même entité sans raison).

> **Définition.** L'**explosion de jointure** — *join fan-out* — est le gonflement du
> nombre de lignes quand une jointure accorde **plusieurs lignes d'un côté à une ligne de
> l'autre** (relation `N → N`, ou jointure sur une colonne non unique). Le contrôle :
> comparer `COUNT(*)` **avant** et **après** la jointure — s'il explose, la jointure
> double (piège P4).

### 5.8 Le piège P5 — le `DISTINCT` qui masque un mauvais `JOIN`

Le piège P5 : un `COUNT(DISTINCT …)` peut donner **le bon chiffre par hasard**, alors que
la jointure est fausse. Le `DISTINCT` « répare » en dédoublonnant, sans que personne ne
sache que la jointure était mauvaise.

```sql
-- P5 : le DISTINCT "répare" le doublon de la jointure — chiffre juste, jointure fausse
SELECT COUNT(DISTINCT c.id_client) AS nb_clients_bobo
FROM vente v
JOIN client c ON c.id_client = v.id_client
WHERE c.ville = 'Bobo-Dioulasso';
```

Ici le chiffre (441 clients de Bobo) est juste **malgré** le fait que la jointure a déjà
multiplié les lignes (chaque client apparaît une fois par vente). Le `DISTINCT` masque le
problème. La bonne pratique : **vérifier le nombre de lignes avant l'agrégation**
(`SELECT COUNT(*)` sur la jointure seule), pas après le `DISTINCT`.

> **Attention.** Un `COUNT(DISTINCT col)` peut cacher une jointure qui double : le chiffre
> sort juste, mais la requête est fausse (et coûteuse). La règle P5 : **toujours contrôler
> `COUNT(*)` sur la jointure nue, avant tout `DISTINCT` ou agrégat**. Si le `COUNT(*)`
> explose, c'est la jointure qu'il faut corriger, pas le `DISTINCT` qu'il faut ajouter.

### 5.9 `ON` et alias — la lecture d'une jointure

La lecture d'une jointure : `FROM vente v JOIN client c ON c.id_client = v.id_client` =
« pour chaque vente `v`, cherche le client `c` de même `id_client`, et mets les deux côte
à côte ». Les alias (`v`, `c`) abrègent et évitent les homonymes (deux tables avec une
colonne `nom` — ici `client.nom` et `magasin.nom` : c'est l'alias qui distingue).

## 6. Exemple concret — la requête qui répond à une question métier

Le directeur commercial demande : *« Pour chaque vente, le nom du client, la ville du
magasin et le mode de paiement — et le CA total par ville. »*

**Étape 1 — Écrire la requête** (jointure en étoile, puis regroupement).

```sql
SELECT m.ville,
       COUNT(*) AS nb_ventes,
       ROUND(SUM(v.montant_ttc)) AS ca
FROM vente v
JOIN client c        ON c.id_client   = v.id_client
JOIN magasin m       ON m.id_magasin  = v.id_magasin
JOIN mode_paiement mp ON mp.id_mode   = v.id_mode
GROUP BY m.ville
ORDER BY ca DESC;
```

**Étape 2 — Prédire la sortie.** 3 villes (Ouagadougou, Bobo-Dioulasso, Koudougou) ; le
`COUNT(*)` de la jointure étoilée = 50 008 (pas d'explosion, toutes les relations sont
`N → 1`) ; Ouagadougou en tête (le plus de clients).

**Étape 3 — Exécuter.** Ouagadougou 21 290 ventes / 3 391 679 290 FCFA ; Bobo-Dioulasso
18 364 / 2 895 549 769 ; Koudougou 10 354 / 1 621 030 672.

**Étape 4 — Comparer.** 3 villes, total 50 008 ventes, total 7 908 259 731 FCFA. La
jointure étoilée n'a rien doublé (contrôle P4 passé).

> **Conseil professionnel.** Avant tout `GROUP BY` après une jointure, **vérifiez que la
> jointure ne double pas** : `SELECT COUNT(*)` sur la jointure nue doit redonner le nombre
> de lignes de la table centrale (ici 50 008). Si c'est le cas, le `GROUP BY` est fiable ;
> sinon, corrigez la jointure d'abord. C'est le réflexe anti-P4/P5.

## 7. Démonstration pas à pas — 6 requêtes sur le fil rouge

### 7.1 Question 1 — Ventes enrichies du nom du client

```sql
SELECT v.id_vente, c.nom, v.montant_ttc
FROM vente v
JOIN client c ON c.id_client = v.id_client
ORDER BY v.id_vente
LIMIT 3;
```

→ 50 008 lignes disponibles (toutes les ventes ont un client).

### 7.2 Question 2 — Magasins sans objectif (`LEFT JOIN` sur table vide)

```sql
SELECT m.nom, o.ca_objectif_ttc
FROM magasin m
LEFT JOIN objectif_magasin o ON o.id_magasin = m.id_magasin
WHERE o.ca_objectif_ttc IS NULL;
```

→ 5 magasins (tous, l'objectif étant `NULL` partout) : c'est la requête standard « les X
sans Y ».

### 7.3 Question 3 — La grille complète magasin × mode (`CROSS JOIN`)

```sql
SELECT COUNT(*) AS nb_combinaisons
FROM magasin m
CROSS JOIN mode_paiement mp;
```

→ **25** (5 × 5).

### 7.4 Question 4 — Le rapport détaillé en étoile

```sql
SELECT v.id_vente, c.nom AS client, m.nom AS magasin,
       mp.libelle AS mode, v.montant_ttc
FROM vente v
JOIN client c        ON c.id_client   = v.id_client
JOIN magasin m       ON m.id_magasin  = v.id_magasin
JOIN mode_paiement mp ON mp.id_mode   = v.id_mode
ORDER BY v.id_vente
LIMIT 3;
```

→ 50 008 lignes, chacune enrichie de 3 libellés.

### 7.5 Question 5 — Le piège P4 (jointure qui double)

```sql
SELECT COUNT(*) AS nb_explose, COUNT(DISTINCT v.id_vente) AS nb_uniques
FROM vente v
JOIN vente v2 ON v2.id_client = v.id_client;
```

→ **2 131 064** lignes explosees, **50 008** uniques. Le `COUNT(*)` est gonflé d'un
facteur ~42 : c'est l'explosion de jointure.

### 7.6 Question 6 — Le CA par ville (jointure étoilée + `GROUP BY`)

```sql
SELECT m.ville, COUNT(*) AS nb, ROUND(SUM(v.montant_ttc)) AS ca
FROM vente v
JOIN magasin m ON m.id_magasin = v.id_magasin
GROUP BY m.ville
ORDER BY ca DESC;
```

→ Ouagadougou 21 290 / 3 391 679 290 ; Bobo-Dioulasso 18 364 / 2 895 549 769 ; Koudougou
10 354 / 1 621 030 672 FCFA.

## 8. Erreurs fréquentes

| # | Erreur | Symptôme | Correction |
|---|--------|----------|------------|
| 1 | `WHERE` sur le côté droit d'un `LEFT JOIN` | les `NULL` disparaissent, le `LEFT` devient `INNER` | la condition dans l'`ON`. |
| 2 | Jointure sur une colonne non unique (P4) | `COUNT(*)` explose (2 131 064 au lieu de 50 008) | joindre sur une clé unique, ou `COUNT(DISTINCT)`. |
| 3 | `DISTINCT` ajouté « pour réparer » (P5) | chiffre juste, jointure fausse, requête lente | corriger la jointure, contrôler `COUNT(*)` avant. |
| 4 | `JOIN` sans `ON` (oubli) | produit cartésien par accident | ajouter l'`ON`, ou `CROSS JOIN` si voulu. |
| 5 | Colonnes homonymes sans alias | erreur « column is ambiguous » | alias sur chaque table (`v.`, `c.`). |
| 6 | `INNER JOIN` là où il faut `LEFT JOIN` | les lignes orphelines du gauche disparaissent | choisir le type selon la question. |

> **Attention.** Les erreurs 2 et 3 sont les pièges P4 et P5 du module : une jointure qui
> **double** (P4) et un `DISTINCT` qui **masque** un mauvais `JOIN` (P5). Les deux se
> contrôlent par le même geste : `COUNT(*)` sur la jointure **nue**, avant tout agrégat.

> **Attention.** Un `JOIN` sans `ON` (ou un `ON` toujours vrai, comme `ON 1=1`) produit le
> **produit cartésien** : `|gauche| × |droit|` lignes. Sur 50 008 ventes et 1 200 clients,
> ce serait un peu plus de 60 milliards de lignes — à ne jamais laisser passer en
> production.

## 9. Bonnes pratiques professionnelles

- **Joindre sur des clés uniques** (PK/FK) ; jamais sur une colonne libre (nom, libellé).
- **`COUNT(*)` avant/après** chaque jointure : le contrôle P4 est systématique.
- **Le type de jointure suit la question** : « les X qui ont Y » → `INNER` ; « tous les X,
  avec Y si existe » → `LEFT`.
- **Condition du côté droit d'un `LEFT` dans l'`ON`**, jamais dans le `WHERE`.
- **Alias sur chaque table** : `v.`, `c.`, `m.` — obligatoire dès deux colonnes homonymes.
- **Étoile, pas grappe** : relier la table centrale aux références, pas les références
  entre elles.

## 10. Exercice guidé — le rapport détaillé par ville (15 min, /10)

**Énoncé.** Produire, par ville (3 lignes, triées par CA décroissant) : le nombre de
ventes, le CA arrondi, le nombre de clients distincts. Utiliser une jointure en étoile.

**Grille de correction (/10).**

| Critère | Points |
|---|---|
| Jointures `vente`→`magasin` (et `client` pour le distinct) correctes | 3 |
| `COUNT(*)`, `ROUND(SUM(…))`, `COUNT(DISTINCT c.id_client)` | 3 |
| `GROUP BY m.ville` + `ORDER BY ca DESC` | 2 |
| 3 lignes, Ouagadougou en tête (3 391 679 290) | 2 |

**Corrigé.**

```sql
SELECT m.ville,
       COUNT(*) AS nb_ventes,
       ROUND(SUM(v.montant_ttc)) AS ca,
       COUNT(DISTINCT c.id_client) AS nb_clients
FROM vente v
JOIN client c  ON c.id_client  = v.id_client
JOIN magasin m ON m.id_magasin = v.id_magasin
GROUP BY m.ville
ORDER BY ca DESC;
```

→ Ouagadougou 21 290 / 3 391 679 290 / 512 ; Bobo-Dioulasso 18 364 / 2 895 549 769 / 441 ;
Koudougou 10 354 / 1 621 030 672 / 247.

## 11. Exercices autonomes

### Exercice 1 — Ventes + nom du client

Les 10 premières ventes avec le nom du client (jointure `INNER`).

### Exercice 2 — Magasins sans objectif

Les magasins dont l'objectif est `NULL` (`LEFT JOIN` + `WHERE … IS NULL`).

### Exercice 3 — La grille magasin × mode

Le nombre de combinaisons `CROSS JOIN` (magasin × mode_paiement).

### Exercice 4 — Le rapport étoilé

Les 5 premières ventes avec client, magasin, mode (3 libellés).

### Exercice 5 — Mesurer l'explosion (P4)

`COUNT(*)` et `COUNT(DISTINCT v.id_vente)` de la jointure `vente` × `vente` via
`id_client`. Donner le facteur de gonflement.

### Exercice 6 — Le CA par ville

Une jointure `vente`→`magasin`, `GROUP BY ville`, CA arrondi, trié décroissant.

### Exercice 7 — `LEFT` vs `INNER` sur table vide

Combien de lignes renvoient `INNER JOIN` et `LEFT JOIN` depuis `magasin` vers
`objectif_magasin` ? Expliquer.

### Exercice 8 — Diagnostic d'erreur

Pourquoi cette requête est-elle une erreur, et comment la corriger ?

```sql
SELECT v.id_vente, c.nom, m.nom
FROM vente v
JOIN client c ON c.id_client = v.id_client
JOIN magasin m ON m.id_magasin = v.id_magasin;
```

## 12. Correction détaillée

**Exercice 1.**

```sql
SELECT v.id_vente, c.nom, v.montant_ttc
FROM vente v
JOIN client c ON c.id_client = v.id_client
ORDER BY v.id_vente
LIMIT 10;
```

→ 10 lignes (les 10 premières ventes, enrichies du nom du client).

**Exercice 2.** Cf. §7.2 → 5 magasins (tous, l'objectif étant `NULL` partout).

**Exercice 3.** Cf. §7.3 → **25** combinaisons.

**Exercice 4.** Cf. §7.4 → 5 lignes, chacune avec 3 libellés.

**Exercice 5.** `COUNT(*)` = **2 131 064**, `COUNT(DISTINCT v.id_vente)` = **50 008**.
Facteur de gonflement ≈ 2 131 064 / 50 008 ≈ **42,6** : chaque vente est comptée une fois
par vente du même client. C'est l'explosion P4.

**Exercice 6.** Cf. §7.6 → Ouagadougou 3 391 679 290 ; Bobo-Dioulasso 2 895 549 769 ;
Koudougou 1 621 030 672 FCFA.

**Exercice 7.** `INNER JOIN` → **0 ligne** (aucune paire accordée, `objectif_magasin` est
vide) ; `LEFT JOIN` → **5 lignes** (les 5 magasins, objectif en `NULL`). Le choix dépend
de la question : « les magasins qui ont un objectif » (`INNER`, 0 ici) vs « tous les
magasins avec leur objectif si existe » (`LEFT`, 5).

**Exercice 8.** Piège de relecture : la requête est en fait **valide** (les deux `nom` sont
préfixés `c.` et `m.`, donc pas d'ambiguïté) — c'est la version « non préfixée » qui serait
une erreur. Si on écrivait `SELECT nom` sans alias, DuckDB renverrait « column "nom" is
ambiguous » (la colonne existe dans `client` et dans `magasin`). La règle : **toujours
préfixer les colonnes homonymes par l'alias** dès qu'une jointure met deux tables ayant la
même colonne.

## 13. Mini-projet — « L'audit de jointures du rapport détaillé » (45 min)

Produire l'audit de jointures du rapport détaillé : 4 requêtes, chacune vérifiée à la main.

| Requête | Lignes attendues |
|---|---|
| J1 : le rapport étoilé (client, magasin, mode) — `COUNT(*)` | 50 008 |
| J2 : magasins sans objectif (`LEFT JOIN` + `IS NULL`) | 5 |
| J3 : grille magasin × mode (`CROSS JOIN`) | 25 |
| J4 : CA par ville (étoile + `GROUP BY`) | 3 |

**Contrôles de cohérence.** (i) J1 : `COUNT(*)` = 50 008 (pas d'explosion, P4 passé).
(ii) J4 : la somme des `ca` = 7 908 259 731 FCFA. (iii) J3 : 25 = 5 × 5.

**Corrigé.**

```sql
-- J1
SELECT COUNT(*) AS nb_lignes
FROM vente v
JOIN client c        ON c.id_client   = v.id_client
JOIN produit p       ON p.id_produit  = v.id_produit
JOIN magasin m       ON m.id_magasin  = v.id_magasin
JOIN mode_paiement mp ON mp.id_mode   = v.id_mode;

-- J2
SELECT m.nom
FROM magasin m
LEFT JOIN objectif_magasin o ON o.id_magasin = m.id_magasin
WHERE o.ca_objectif_ttc IS NULL;

-- J3
SELECT COUNT(*) AS nb_combinaisons
FROM magasin m
CROSS JOIN mode_paiement mp;

-- J4
SELECT m.ville, COUNT(*) AS nb, ROUND(SUM(v.montant_ttc)) AS ca
FROM vente v
JOIN magasin m ON m.id_magasin = v.id_magasin
GROUP BY m.ville
ORDER BY ca DESC;
```

> **Dans les faits.** La syntaxe `JOIN … ON` est **identique** sur DuckDB, PostgreSQL et
> SQLite pour `INNER`/`LEFT`/`CROSS`. Le `FULL OUTER JOIN` est supporté par DuckDB et
> PostgreSQL ; **SQLite ne le supporte pas** (il faut le simuler par `LEFT JOIN` +
> `UNION` + `LEFT JOIN`). C'est la principale différence de portabilité du chapitre.

## 14. Boîte à outils du chapitre

> **Boîte à outils.** Ce chapitre installe 4 types de jointure (`INNER`, `LEFT`, `FULL`,
> `CROSS`), la **jointure en étoile** (la table centrale reliée aux références), et les
> deux contrôles anti-pièges (P4 : `COUNT(*)` avant/après ; P5 : ne jamais « réparer » un
> `JOIN` avec un `DISTINCT`). Le choix du type suit la question ; la condition du côté
> droit d'un `LEFT` va dans l'`ON`.

| Outil | Usage | Syntaxe | Piège |
|---|---|---|---|
| `INNER JOIN` | les paires accordées | `v JOIN c ON c.id=v.id` | filtre les orphelines du gauche |
| `LEFT JOIN` | tout le gauche, `NULL` à droite | `m LEFT JOIN o ON …` | `WHERE` sur le droit = `INNER` |
| `FULL OUTER JOIN` | les deux côtés | `m FULL JOIN o ON …` | absent de SQLite |
| `CROSS JOIN` | produit cartésien | `m CROSS JOIN mp` | explosion si par accident |
| Étoile | table centrale + références | `vente JOIN c JOIN m JOIN mp` | joindre les références entre elles |
| Contrôle P4 | explosion | `COUNT(*)` avant/après | 2 131 064 au lieu de 50 008 |
| Contrôle P5 | `DISTINCT` qui masque | `COUNT(*)` sur la jointure nue | chiffre juste, jointure fausse |

## 15. Résumé du chapitre

- **`INNER JOIN`** = les paires qui s'accordent des deux côtés (filtre les orphelines du
  gauche). **`LEFT JOIN`** = tout le gauche, `NULL` à droite. **`FULL OUTER JOIN`** = les
  deux côtés. **`CROSS JOIN`** = le produit cartésien (voulu en grille, bug par oubli
  d'`ON`).
- **La jointure en étoile** relie la table centrale (`vente`) aux références (client,
  produit, magasin, mode) en relations `N → 1` : elle enrichit sans doubler (50 008 lignes
  conservées).
- **Le type de jointure suit la question** : « les X qui ont Y » → `INNER` ; « tous les X,
  avec Y si existe » → `LEFT`.
- **P4** : une jointure sur une colonne non unique **double** les lignes (2 131 064 au
  lieu de 50 008) — contrôle par `COUNT(*)` avant/après.
- **P5** : un `DISTINCT` peut **masquer** un mauvais `JOIN` (chiffre juste, requête fausse)
  — contrôler la jointure nue avant tout `DISTINCT`.
- **`ON` vs `WHERE`** : la condition du côté droit d'un `LEFT JOIN` va dans l'`ON`, jamais
  dans le `WHERE`.

## 16. À retenir

- **Le type suit la question** : `INNER` = « qui a », `LEFT` = « tous, avec si existe ».
- **Étoile, pas grappe** : relier la centrale aux références, jamais les références entre
  elles.
- **`COUNT(*)` avant/après** chaque jointure (P4) ; **jamais de `DISTINCT` pour réparer**
  un `JOIN` (P5).
- **Condition du côté droit d'un `LEFT` dans l'`ON`**, pas dans le `WHERE`.
- **Alias + préfixe** sur chaque table : obligatoire dès deux colonnes homonymes.

> **À retenir.** Une jointure est un **accord de clés** : `ON v.id_client = c.id_client`.
> Le type (`INNER`/`LEFT`/`FULL`/`CROSS`) décide **qui reste** quand l'accord échoue. Le
> bon réflexe n'est pas la syntaxe (facile) mais le **contrôle du nombre de lignes**
> (difficile) : `COUNT(*)` avant et après, et la question « est-ce que ma jointure
> devrait doubler ? ».

## 17. Évaluation formative (auto-correction, 8 min)

Sans document, en 8 minutes, répondre aux 5 questions. Auto-correction en bas.

1. Différence entre `INNER JOIN` et `LEFT JOIN` ?
2. Pourquoi la condition du côté droit d'un `LEFT JOIN` doit-elle aller dans l'`ON` ?
3. Que produit un `CROSS JOIN` entre 5 magasins et 5 modes de paiement ?
4. C'est quoi l'explosion de jointure (P4), et comment la détecter ?
5. Pourquoi un `DISTINCT` peut-il masquer un mauvais `JOIN` (P5) ?

**Réponses** :

1. `INNER JOIN` ne garde que les paires qui s'accordent **des deux côtés** (les orphelines
   du gauche disparaissent) ; `LEFT JOIN` garde **toutes** les lignes du gauche, et
   complète de `NULL` à droite celles sans correspondance.
2. Parce que dans le `WHERE`, les lignes dont la colonne du droit est `NULL` sont
   **éliminées** (`NULL > 0` est `NULL`), ce qui transforme le `LEFT JOIN` en `INNER`. Dans
   l'`ON`, la condition ne filtre pas le côté gauche : les lignes sans correspondance
   restent.
3. Le **produit cartésien** : 5 × 5 = **25 lignes** (chaque magasin avec chaque mode), sans
   condition.
4. C'est le gonflement du nombre de lignes quand la jointure accorde plusieurs lignes d'un
   côté à une ligne de l'autre (relation `N → N`). Détection : `COUNT(*)` **avant** (50 008)
   et **après** la jointure (2 131 064) — si ça explose, la jointure double.
5. Parce que le `DISTINCT` **dédoublonne** le résultat : le chiffre final peut être juste
   **même si** la jointure a doublé les lignes. On ne voit pas le bug (chiffre correct),
   mais la requête est fausse et lente. D'où le contrôle de la jointure nue avant
   l'agrégat.
