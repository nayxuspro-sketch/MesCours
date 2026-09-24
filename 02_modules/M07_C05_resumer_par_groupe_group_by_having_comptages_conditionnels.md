# Module M07.C05 — Résumer par groupe : GROUP BY, HAVING, comptages conditionnels

**Outils comparés : DuckDB 1.5.5 (CLI + Python), SQLite natif Python, PostgreSQL cité.
Durée indicative : 4 h. Niveau : N2 → N3. Prérequis : M07.C01 (SELECT, FROM, alias) ; M07.C02 (WHERE) ; M07.C03 (ORDER BY, LIMIT) ; M07.C04 (agrégats).**

> **L'idée du chapitre.** C04 a réduit **toute la table** à une ligne de synthèse. C05 va
> plus loin : **une ligne de synthèse par groupe**. « Le CA de chaque magasin. » « Le
> nombre de ventes de chaque rayon. » « Le panier moyen par magasin et par année. » C'est
> `GROUP BY` — la clause la plus utile de l'analyse métier. Le chapitre couvre la syntaxe
> de base, le regroupement par **clé** (et non par libellé — le piège du `rayon` doublé),
> le regroupement multi-colonnes, `HAVING` (le filtre qui s'applique aux groupes, pas aux
> lignes), la distinction `WHERE` / `HAVING`, et les **comptages conditionnels**
> (`SUM(CASE WHEN …)` combiné à `GROUP BY`) qui produisent les tableaux de bord croisés.
> Le fil rouge est la base `commercial.duckdb` : on y mesure le CA de chacun des
> **5 magasins** (entre 1 564 937 883 et 1 596 813 264 FCFA) et de chacune des **8
> catégories** (entre 699 533 080 et 1 236 006 465 FCFA).

> **Base de travail — `commercial.duckdb` (empreinte `0b9c12397d9c8af2…`).** Le chapitre
> mobilise : 50 008 ventes répartis sur 5 magasins (de 9 873 à 10 099 ventes chacun),
> 8 catégories (de 4 764 à 7 166 ventes chacune), 2 années (2025 : 24 920 ventes ; 2026 :
> 25 088), et 5 modes de paiement. Le CA total reste 7 908 259 731 FCFA.

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous saurez :

- **regrouper** un résultat par une colonne avec `GROUP BY` et produire une ligne de
  synthèse par groupe ;
- **regrouper par clé** (id unique) et comprendre pourquoi regrouper par **libellé** est
  dangereux quand le libellé est doublé ;
- **regrouper sur plusieurs colonnes** (`GROUP BY a, b`) pour des coupes croisées ;
- **filtrer les groupes** avec `HAVING` (et distinguer `WHERE` de `HAVING`) ;
- **combiner** `ORDER BY` et `LIMIT` avec `GROUP BY` pour un « top N par groupe » ;
- **compter conditionnellement** avec `SUM(CASE WHEN … THEN 1 ELSE 0 END)` dans un
  `GROUP BY`.

## 2. Pourquoi cette notion est importante

- « Le CA par magasin », « les ventes par catégorie », « le panier moyen par ville et par
  année » : ce sont **les questions d'un tableau de bord**. Sans `GROUP BY`, on ne sort
  d'une table qu'une seule ligne de synthèse (C04) ou des lignes brutes (C01–C03).
- Le **regroupement par libellé doublé** est un piège silencieux : le total est juste,
  mais les lignes se fondent les unes dans les autres sans avertissement. Le socle M07 en
  contient un de démonstration : la colonne `rayon` de `categorie` porte deux fois
  « Alimentaire », deux fois « Bricolage », deux fois « Jardinage » (les `sous_categorie`
  distinguent).
- La frontière **`WHERE` / `HAVING`** est l'un des points les plus demandés en entretien :
  `WHERE` filtre les **lignes avant** le regroupement ; `HAVING` filtre les **groupes
  après** l'agrégation.

## 3. Explication simple — `GROUP BY` est une plieuse par tiroirs

C04 : un tas de tickets, on scanne le tas, un seul chiffre sort. C05 : on met des
**tiroirs** sur le bureau — un tiroir par magasin, un par rayon, un par année. Chaque
ticket va dans son tiroir (selon sa valeur dans la colonne de regroupement). Puis on
**applique la même plieuse à chaque tiroir** : un chiffre par tiroir.

Concrètement, `GROUP BY id_magasin` sur 50 008 ventes produit **5 lignes** (une par
magasin), chaque ligne portant les agrégats calculés **sur les seules ventes de ce
magasin**. Le total des 5 lignes de `SUM(montant_ttc)` redonne le CA global de C04
(7 908 259 731 FCFA) — c'est le **contrôle de cohérence** à faire systématiquement.

> **Définition.** La clause **`GROUP BY`** — *grouper par* — subdivise les lignes du
> résultat en **groupes** selon les valeurs de la colonne (ou des colonnes) citées : les
> lignes qui partagent la même valeur forment un groupe, et chaque fonction d'agrégat du
> `SELECT` est calculée **séparément sur chaque groupe**. Le résultat contient une ligne
> par groupe.

## 4. Vocabulaire essentiel

| Français — English | Définition simple | Piège à éviter |
|---|---|---|
| **GROUP BY** | une ligne de synthèse **par groupe** (par valeur distincte de la colonne). | oublier que chaque colonne du `SELECT` doit être agrégée ou dans le `GROUP BY`. |
| **groupe** | l'ensemble des lignes qui partagent la même valeur de la clé de regroupement. | confondre le nombre de groupes avec le nombre de lignes. |
| **clé de regroupement** | la colonne (ou les colonnes) du `GROUP BY` ; idéale : une clé unique (`id_*`). | regrouper par un libellé doublé (les groupes se fondent). |
| **HAVING** | filtre appliqué **aux groupes**, après les agrégats. | l'écrire dans `WHERE` (interdit : on ne filtre pas un agrégat là-dedans). |
| **WHERE** | filtre appliqué **aux lignes**, avant le regroupement. | mettre un agrégat dans `WHERE` (erreur d'exécution). |
| **regroupement multi-colonnes** | `GROUP BY a, b` : un groupe par couple (a, b). | croire que l'ordre des colonnes du `GROUP BY` change le total (il ne change que la granularité d'affichage). |
| **comptage conditionnel** | `SUM(CASE WHEN … THEN 1 ELSE 0 END)` dans un `GROUP BY`. | oublier le `ELSE 0` (les `NULL` ne s'additionnent pas). |
| **coupe croisée** | regroupement sur 2 dimensions (magasin × année). | multiplier les colonnes sans comprendre que chaque ligne = une combinaison. |

## 5. Cours approfondi

### 5.1 La syntaxe de base

```sql
SELECT id_magasin,
       COUNT(*)              AS nb_ventes,
       ROUND(SUM(montant_ttc)) AS ca
FROM vente
GROUP BY id_magasin
ORDER BY ca DESC;
```

| id_magasin | nb_ventes | ca            |
|------------|-----------|---------------|
| 4          | 10 061    | 1 596 813 264 |
| 1          | 10 099    | 1 595 223 423 |
| 2          | 10 033    | 1 578 987 708 |
| 5          | 9 942     | 1 572 297 452 |
| 3          | 9 873     | 1 564 937 883 |

Cinq groupes, cinq lignes. Chaque `nb_ventes` et `ca` est calculé **sur les seules ventes
du magasin**. Le total des 5 `nb_ventes` redonne 50 008 ; le total des 5 `ca` redonne
7 908 259 731. Le magasin 4 (Bobo Sarfalao) est en tête, mais l'écart entre le 1ᵉ et le
5ᵉ est faible (moins de 2 %).

Règle de syntaxe : **toute colonne du `SELECT` doit être soit agrégée, soit dans le
`GROUP BY`**. `id_magasin` est dans le `GROUP BY` ; `COUNT(*)` et `SUM(montant_ttc)` sont
agrégés. C'est la règle d'or de C04, généralisée.

### 5.2 Regrouper par clé, pas par libellé

Le socle M07 contient 8 catégories, mais seulement **5 libellés** de `rayon` : «
Alimentaire » apparaît deux fois (Boissons et Conserves), « Bricolage » deux fois
(Outillage et Quincaillerie), « Jardinage » deux fois (Plantes et Outillage).

Regrouper par `c.rayon` (le libellé) **fond les deux catégories** qui partagent le
même rayon :

```sql
SELECT c.rayon, COUNT(*) AS nb_ventes
FROM vente v
JOIN produit p ON p.id_produit = v.id_produit
JOIN categorie c ON c.id_categorie = p.id_categorie
GROUP BY c.rayon
ORDER BY nb_ventes DESC;
```

| rayon        | nb_ventes |
|--------------|-----------|
| Bricolage    | 12 418    |
| Jardinage    | 12 037    |
| Alimentaire  | 11 930    |
| Hygiene      | 6 825     |
| Decoration   | 6 798     |

Regrouper par `c.id_categorie` (la clé) garde **8 groupes distincts**. Le choix entre les
deux est un **choix métier** (vu « par rayon » ou vu « par catégorie »), pas une
coïncidence : si vous voulez 8 lignes, regroupez par la clé.

> **Définition.** Une **clé de regroupement** — *grouping key* — est la colonne (ou la
> liste de colonnes) citée dans `GROUP BY`. Elle doit être **unique par groupe** : on
> regroupe idéalement par une clé (`id_categorie`) plutôt que par un libellé (`rayon`),
> car un libellé doublé fusionne silencieusement deux groupes différents.

> **Attention.** Regrouper par un libellé doublé ne provoque **aucune erreur** : le
> moteur fusionne les groupes sans avertissement, et le total général reste juste. Le
> bug est donc silencieux — on ne le voit qu'en comptant les lignes du résultat (5 au
> lieu de 8). Vérifiez toujours le nombre de groupes attendus.

### 5.3 Regrouper sur plusieurs colonnes

`GROUP BY a, b` produit un groupe par **couple** (a, b). Coupe croisée magasin × année :

```sql
SELECT id_magasin,
       EXTRACT(YEAR FROM date_vente) AS annee,
       COUNT(*)              AS nb_ventes,
       ROUND(SUM(montant_ttc)) AS ca
FROM vente
WHERE id_magasin = 4
GROUP BY 1, 2
ORDER BY annee;
```

| id_magasin | annee | nb_ventes | ca          |
|------------|-------|-----------|-------------|
| 4          | 2025  | 5 064     | 797 593 324 |
| 4          | 2026  | 4 997     | 799 219 940 |

Deux groupes (le couple magasin 4 × 2025, le couple magasin 4 × 2026). Sur les 5 magasins
et 2 années, la requête sans `WHERE` produirait **10 groupes**.

### 5.4 `HAVING` — filtrer les groupes

`WHERE` ne voit que des lignes ; `HAVING` voit des **groupes déjà agrégés**. Question :
« quelles catégories ont plus de 6 500 ventes ? »

```sql
SELECT c.id_categorie, c.rayon, c.sous_categorie, COUNT(*) AS nb_ventes
FROM vente v
JOIN produit p ON p.id_produit = v.id_produit
JOIN categorie c ON c.id_categorie = p.id_categorie
GROUP BY c.id_categorie, c.rayon, c.sous_categorie
HAVING COUNT(*) > 6500
ORDER BY nb_ventes DESC;
```

| id_categorie | rayon       | sous_categorie | nb_ventes |
|--------------|-------------|----------------|-----------|
| 1            | Alimentaire | Boissons       | 7 166     |
| 4            | Bricolage   | Quincaillerie  | 7 037     |
| 8            | Hygiene     | Cosmétique     | 6 825     |
| 7            | Decoration  | Interieur      | 6 798     |

Quatre groupes passent le filtre. Le `HAVING` peut aussi s'appliquer à `SUM`, `AVG`,
`MIN`, `MAX` — tout agrégat :

```sql
SELECT id_magasin, ROUND(SUM(montant_ttc)) AS ca
FROM vente
GROUP BY id_magasin
HAVING ROUND(SUM(montant_ttc)) > 1550000000
ORDER BY ca DESC;
```

Ici les **5 magasins** passent (le plus petit CA, 1 564 937 883 FCFA, dépasse le seuil) :
le seuil est bas relativement à la répartition quasi uniforme du générateur.

> **Définition.** La clause **`HAVING`** — *ayant* — est le filtre qui s'applique aux
> **groupes** après le calcul des agrégats. Elle s'écrit entre `GROUP BY` et `ORDER BY`,
> et seule elle permet de filtrer sur une valeur agrégée (`HAVING COUNT(*) > 10`). `WHERE`
> filtre les lignes **avant** le regroupement et ne peut pas référencer d'agrégat.

### 5.5 `WHERE` et `HAVING` ensemble

On peut (et on doit souvent) combiner les deux : `WHERE` réduit les lignes **avant** le
regroupement, `HAVING` filtre les groupes **après** :

```sql
SELECT id_magasin, COUNT(*) AS nb_ventes_2026
FROM vente
WHERE EXTRACT(YEAR FROM date_vente) = 2026
GROUP BY id_magasin
HAVING COUNT(*) > 4900
ORDER BY nb_ventes_2026 DESC;
```

Ordre d'exécution (rappel C01/C04) : `FROM` → **`WHERE`** (lignes) → **`GROUP BY`**
(groupes) → **`HAVING`** (groupes) → `SELECT` → `ORDER BY` → `LIMIT`.

> **À retenir.** `WHERE` = filtre sur les **lignes** (avant agrégation, pas d'agrégat
> autorisé) ; `HAVING` = filtre sur les **groupes** (après agrégation, agrégats
> autorisés). Si vous filtrez sur un total, c'est `HAVING`.

### 5.6 Comptages conditionnels dans un `GROUP BY`

Le motif de C04 §5.10 (`SUM(CASE WHEN …)`) combine parfaitement avec `GROUP BY` : chaque
groupe porte plusieurs colonnes de mesures conditionnelles. Répartition Espèces / Carte
**par magasin** :

```sql
SELECT id_magasin,
       COUNT(*) AS total,
       SUM(CASE WHEN id_mode = 1 THEN 1 ELSE 0 END) AS especes,
       SUM(CASE WHEN id_mode = 2 THEN 1 ELSE 0 END) AS cartes
FROM vente
GROUP BY id_magasin
ORDER BY id_magasin;
```

| id_magasin | total  | especes | cartes |
|------------|--------|---------|--------|
| 1          | 10 099 | 4 109   | 2 502  |
| 2          | 10 033 | 4 043   | 2 532  |
| 3          | 9 873  | 3 973   | 2 414  |
| 4          | 10 061 | 4 093   | 2 469  |
| 5          | 9 942  | 3 957   | 2 449  |

Chaque ligne est un magasin ; chaque colonne `especes` / `cartes` est un sous-comptage.
C'est le schéma des **tableaux de bord croisés** : lignes = dimension 1, colonnes =
mesures conditionnelles.

> **Définition.** Le **comptage conditionnel** — *conditional count* — est le motif
> `SUM(CASE WHEN condition THEN 1 ELSE 0 END)` : il convertit « compter les lignes qui
> vérifient la condition » en expression agrégable. Combiné à `GROUP BY`, il produit une
> colonne de comptage par condition, sur chaque groupe.

### 5.7 `COUNT(DISTINCT …)` dans un groupe

Les agrégats de C04 fonctionnent aussi **par groupe**. Nombre de clients distincts qui
ont acheté dans chaque magasin :

```sql
SELECT id_magasin, COUNT(DISTINCT id_client) AS nb_clients
FROM vente
GROUP BY id_magasin
ORDER BY id_magasin;
```

→ 1 199, 1 199, 1 200, 1 200, 1 199. Quatre magasins servent 1 199 clients distincts,
deux en servent 1 200 : la couverture est quasi totale (sur 1 200 clients au total).

### 5.8 Ce que ce chapitre ne couvre pas

- Les **fenêtres** (`SUM() OVER (PARTITION BY …)` : agrégat par groupe **sans** réduire
  les lignes) : M11.
- Les **sous-requêtes** et **CTE** (pré-agrégations nommées) : C08.
- L'optimisation des gros `GROUP BY` (index, plans d'exécution) : M11.

## 6. Exemple concret — la requête qui répond à une question métier

Le directeur des magasins demande : *« Le CA de chaque magasin, le nombre de ventes, et
le panier moyen — mais seulement les magasins qui font plus de 9 900 ventes. »*

**Étape 1 — Écrire la requête.**

```sql
SELECT m.id_magasin,
       m.nom,
       COUNT(*)                  AS nb_ventes,
       ROUND(SUM(v.montant_ttc)) AS ca,
       ROUND(AVG(v.montant_ttc)) AS panier_moyen
FROM vente v
JOIN magasin m ON m.id_magasin = v.id_magasin
GROUP BY m.id_magasin, m.nom
HAVING COUNT(*) > 9900
ORDER BY ca DESC;
```

**Étape 2 — Prédire la sortie.** `FROM vente` charge 50 008 lignes ; `JOIN magasin`
apporte le nom ; `GROUP BY` forme 5 groupes ; `HAVING COUNT(*) > 9900` élimine les
groupes de moins de 9 900 ventes. À l'œil, on prédit que 2 magasins sortent (les deux
moins vendus) — il resterait 3 magasins.

**Étape 3 — Exécuter.** Quatre lignes : Bobo Sarfalao (10 061 ventes,
1 596 813 264 FCFA), Ouaga Centre (10 099, 1 595 223 423), Ouaga Patte d'Oie
(10 033, 1 578 987 708), Koudougou (9 942, 1 572 297 452). Le panier moyen varie entre
157 379 et 158 713 FCFA.

**Étape 4 — Comparer.** La prédiction était fausse sur un point : Koudougou (9 942)
passe le seuil de 9 900, seul Bobo Centre (9 873) sort. Le contrôle de cohérence (la
somme des CA des 5 magasins = 7 908 259 731) reste le filet de sécurité.

> **Conseil professionnel.** Prévoyez **toujours le cas limite** du seuil de `HAVING` :
> un groupe exactement **au seuil** passe ou non selon `>` ou `>=`. Avant de publier,
> vérifiez le nombre de groupes attendus — ici 5 au lieu de 4 — et ajustez le seuil ou
> l'opérateur. Une surprise de seuil est la première cause de « le rapport a 4 lignes au
> lieu de 5 ».

## 7. Démonstration pas à pas — 6 requêtes sur le fil rouge

### 7.1 Question 1 — CA par magasin

```sql
SELECT id_magasin, COUNT(*) AS nb, ROUND(SUM(montant_ttc)) AS ca
FROM vente
GROUP BY id_magasin
ORDER BY ca DESC;
```

→ 5 lignes : 1 596 813 264 / 1 595 223 423 / 1 578 987 708 / 1 572 297 452 /
1 564 937 883 FCFA.

### 7.2 Question 2 — CA par catégorie (la clé, pas le rayon)

```sql
SELECT c.id_categorie, c.rayon, c.sous_categorie,
       COUNT(*) AS nb, ROUND(SUM(v.montant_ttc)) AS ca
FROM vente v
JOIN produit p ON p.id_produit = v.id_produit
JOIN categorie c ON c.id_categorie = p.id_categorie
GROUP BY c.id_categorie, c.rayon, c.sous_categorie
ORDER BY ca DESC;
```

→ 8 lignes, du plus gros au plus petit : Decoration (1 236 006 465), Hygiene
(1 163 845 193), Jardinage-Plantes (1 160 443 887), Alimentaire-Boissons
(1 026 270 112), Jardinage-Outillage (950 960 303), Bricolage-Quincaillerie
(939 911 483), Alimentaire-Conserves (731 289 207), Bricolage-Outillage
(699 533 080) FCFA.

### 7.3 Question 3 — Panier moyen par magasin

```sql
SELECT id_magasin, ROUND(AVG(montant_ttc)) AS panier_moyen
FROM vente
GROUP BY id_magasin
ORDER BY panier_moyen DESC;
```

→ 158 713 (magasin 4) / 158 507 (3) / 158 147 (5) / 157 959 (1) / 157 379 (2) FCFA.
L'écart total est de 1 334 FCFA, soit moins de 1 % : le panier moyen est quasi
uniforme entre magasins.

### 7.4 Question 4 — Le CA par année

```sql
SELECT EXTRACT(YEAR FROM date_vente) AS annee,
       COUNT(*) AS nb, ROUND(SUM(montant_ttc)) AS ca
FROM vente
GROUP BY 1
ORDER BY annee;
```

→ 2025 : 24 920 ventes, 3 925 215 671 FCFA ; 2026 : 25 088 ventes, 3 983 044 060 FCFA.
Le 2026 dépasse le 2025 de 57 828 389 FCFA (+1,5 %).

### 7.5 Question 5 — Catégories actives (`HAVING`)

```sql
SELECT c.rayon, COUNT(*) AS nb_ventes
FROM vente v
JOIN produit p ON p.id_produit = v.id_produit
JOIN categorie c ON c.id_categorie = p.id_categorie
GROUP BY c.rayon
HAVING COUNT(*) > 6500
ORDER BY nb_ventes DESC;
```

→ 4 rayons : Bricolage 12 418, Jardinage 12 037, Alimentaire 11 930, Hygiene 6 825,
Decoration 6 798 — non, 5 lignes passent car Decoration (6 798) dépasse 6 500.
Le `HAVING` garde 5 groupes sur 5 (seuil bas) ; le seuil 12 000 ne en garderait que 2
(Bricolage, Jardinage).

### 7.6 Question 6 — Espèces et cartes par magasin

```sql
SELECT id_magasin,
       SUM(CASE WHEN id_mode = 1 THEN 1 ELSE 0 END) AS especes,
       SUM(CASE WHEN id_mode = 2 THEN 1 ELSE 0 END) AS cartes
FROM vente
GROUP BY id_magasin
ORDER BY especes DESC;
```

→ Magasin 1 : 4 109 Espèces / 2 502 Carte ; magasin 4 : 4 093 / 2 469 ; magasin 2 :
4 043 / 2 532 ; magasin 3 : 3 973 / 2 414 ; magasin 5 : 3 957 / 2 449.

## 8. Erreurs fréquentes

| # | Erreur | Symptôme | Correction |
|---|--------|----------|------------|
| 1 | Colonne non agrégée et non groupée dans `SELECT` | erreur « must appear in the GROUP BY clause » | l'ajouter au `GROUP BY` ou l'agréger. |
| 2 | Filtrer un agrégat dans `WHERE` | erreur « WHERE clause cannot contain aggregates » | utiliser `HAVING`. |
| 3 | Regrouper par un libellé doublé | nombre de lignes inexpliqué (5 au lieu de 8) | regrouper par la clé (`id_*`). |
| 4 | Oublier le `ELSE 0` dans un comptage conditionnel | colonnes de comptage trop faibles (les `NULL` ne s'additionnent pas) | `SUM(CASE WHEN … THEN 1 ELSE 0 END)`. |
| 5 | `ORDER BY` sur un alias inconnu du `GROUP BY` | ordre arbitraire ou erreur selon le SGBD | ordonner par l'agrégat ou la clé. |
| 6 | Attendre que `GROUP BY` supprime les doublons | doublons persistants | `GROUP BY` réduit par groupe ; pour supprimer des lignes, `DISTINCT` (C01). |

> **Attention.** L'erreur 3 est la plus sournoise : **aucun message d'erreur**, un total
> juste, mais des groupes fusionnés. Le nombre de lignes du résultat est le premier
> contrôle : si vous attendez 8 catégories et vous en voyez 5, vérifiez la clé de
> regroupement.

> **Attention.** `ORDER BY` dans une requête `GROUP BY` : on trie les **groupes**.
> `ORDER BY ca` (alias de l'agrégat) est accepté par DuckDB et PostgreSQL ; pour la
> portabilité maximale, répéter l'expression (`ORDER BY SUM(montant_ttc) DESC`) ou trier
> par position.

## 9. Bonnes pratiques professionnelles

- **Regrouper par la clé** (`id_*`), joindre le libellé dans le `SELECT` et le `GROUP BY`.
- **Vérifier le nombre de groupes** avant toute lecture : 5 magasins, 8 catégories,
  10 couples magasin×année.
- **Contrôle de cohérence** : la somme des agrégats par groupe doit redonner l'agrégat
  global (C04).
- **Un seuil de `HAVING` doit être documenté** : « > 9 900 ventes » est une décision
  métier, pas une constante anonyme.
- **`CASE` conditionnel : toujours un `ELSE 0`** dans les comptages (jamais de `NULL`
  dans une addition).
- **Nommer les colonnes** : `AS nb_ventes`, `AS ca`, `AS panier_moyen` — le libellé
  du tableau de bord est celui des alias.

## 10. Exercice guidé — le tableau de bord des 5 magasins (15 min, /10)

**Énoncé.** Produire une ligne par magasin (5 lignes, triées par CA décroissant) avec :
le nom du magasin, le nombre de ventes, le CA arrondi, le panier moyen arrondi, le
nombre de ventes Espèces, le nombre de ventes Carte.

**Grille de correction (/10).**

| Critère | Points |
|---|---|
| `GROUP BY m.id_magasin, m.nom` (clé + libellé) | 2 |
| `COUNT(*)`, `ROUND(SUM(…))`, `ROUND(AVG(…))` | 2 |
| 2 comptages conditionnels avec `ELSE 0` | 2 |
| `JOIN magasin` correct | 1 |
| `ORDER BY ca DESC` (alias de l'agrégat) | 1 |
| 5 lignes, triées : 1 596 813 264 en tête | 2 |

**Corrigé.**

```sql
SELECT m.id_magasin,
       m.nom,
       COUNT(*) AS nb_ventes,
       ROUND(SUM(v.montant_ttc)) AS ca,
       ROUND(AVG(v.montant_ttc)) AS panier_moyen,
       SUM(CASE WHEN v.id_mode = 1 THEN 1 ELSE 0 END) AS especes,
       SUM(CASE WHEN v.id_mode = 2 THEN 1 ELSE 0 END) AS cartes
FROM vente v
JOIN magasin m ON m.id_magasin = v.id_magasin
GROUP BY m.id_magasin, m.nom
ORDER BY ca DESC;
```

→ 5 lignes : Bobo Sarfalao (10 061 / 1 596 813 264 / 158 713 / 4 093 / 2 469), Ouaga
Centre (10 099 / 1 595 223 423 / 157 959 / 4 109 / 2 502), Ouaga Patte d'Oie
(10 033 / 1 578 987 708 / 157 379 / 4 043 / 2 532), Koudougou (9 942 / 1 572 297 452 /
158 147 / 3 957 / 2 449), Bobo Centre (9 873 / 1 564 937 883 / 158 507 / 3 973 / 2 414).

## 11. Exercices autonomes

### Exercice 1 — CA par catégorie

Une ligne par catégorie (8 lignes) : id, rayon, sous-catégorie, nombre de ventes, CA
arrondi, triée par CA décroissant.

### Exercice 2 — Panier moyen par magasin

Une ligne par magasin : panier moyen arrondi, triée décroissante.

### Exercice 3 — Le CA par année

Une ligne par année : nombre de ventes, CA arrondi.

### Exercice 4 — Catégories actives

Les catégories (par clé) ayant plus de 6 500 ventes, avec leur nombre de ventes.

### Exercice 5 — Rayon vs clé

Compter le nombre de groupes produits par `GROUP BY c.rayon` et par
`GROUP BY c.id_categorie` sur la même requête de base. Expliquer l'écart.

### Exercice 6 — Espèces et cartes par magasin

Deux comptages conditionnels par magasin, triés par nombre de ventes Espèces décroissant.

### Exercice 7 — Couper par magasin et par année

Le nombre de ventes du magasin 4 en 2025 et en 2026 (2 lignes).

### Exercice 8 — Diagnostic d'erreur

Que fait cette requête, et pourquoi est-elle une erreur ?

```sql
-- ERREUR ATTENDUE : un agrégat dans WHERE est interdit (cf. HAVING)
SELECT id_magasin, COUNT(*) AS nb
FROM vente
WHERE COUNT(*) > 9900;
```

## 12. Correction détaillée

**Exercice 1.**

```sql
SELECT c.id_categorie, c.rayon, c.sous_categorie,
       COUNT(*) AS nb, ROUND(SUM(v.montant_ttc)) AS ca
FROM vente v
JOIN produit p ON p.id_produit = v.id_produit
JOIN categorie c ON c.id_categorie = p.id_categorie
GROUP BY c.id_categorie, c.rayon, c.sous_categorie
ORDER BY ca DESC;
```

→ 8 lignes (cf. §7.2).

**Exercice 2.**

```sql
SELECT id_magasin, ROUND(AVG(montant_ttc)) AS panier_moyen
FROM vente
GROUP BY id_magasin
ORDER BY panier_moyen DESC;
```

→ 158 713 / 158 507 / 158 147 / 157 959 / 157 379 FCFA.

**Exercice 3.**

```sql
SELECT EXTRACT(YEAR FROM date_vente) AS annee,
       COUNT(*) AS nb, ROUND(SUM(montant_ttc)) AS ca
FROM vente
GROUP BY 1
ORDER BY annee;
```

→ 2025 : 24 920 / 3 925 215 671 ; 2026 : 25 088 / 3 983 044 060 FCFA.

**Exercice 4.**

```sql
SELECT c.id_categorie, COUNT(*) AS nb
FROM vente v
JOIN produit p ON p.id_produit = v.id_produit
JOIN categorie c ON c.id_categorie = p.id_categorie
GROUP BY c.id_categorie
HAVING COUNT(*) > 6500
ORDER BY nb DESC;
```

→ 4 catégories : 1 (7 166), 4 (7 037), 8 (6 825), 7 (6 798).

**Exercice 5.** `GROUP BY c.rayon` produit **5 groupes** (Bricolage 12 418, Jardinage
12 037, Alimentaire 11 930, Hygiene 6 825, Decoration 6 798) ; `GROUP BY c.id_categorie`
produit **8 groupes** (cf. §7.2). L'écart (3) vient des trois rayons doublés :
Alimentaire, Bricolage, Jardinage — chaque libellé en fusionne deux.

**Exercice 6.** Cf. §7.6 → Magasin 1 : 4 109 / 2 502, puis 4 : 4 093 / 2 469, 2 : 4 043 /
2 532, 3 : 3 973 / 2 414, 5 : 3 957 / 2 449.

**Exercice 7.**

```sql
SELECT EXTRACT(YEAR FROM date_vente) AS annee, COUNT(*) AS nb
FROM vente
WHERE id_magasin = 4
GROUP BY 1
ORDER BY annee;
```

→ 2025 : 5 064 ; 2026 : 4 997.

**Exercice 8.** C'est une erreur : `COUNT(*)` est un **agrégat**, et `WHERE` ne peut pas
en contenir (il filtre les lignes, avant le regroupement). Le bon écrit est
`GROUP BY id_magasin HAVING COUNT(*) > 9900`.

## 13. Mini-projet — « Le rapport mensuel multi-dimensionnel » (45 min)

Produire, dans un seul fichier SQL exécuté sur `commercial.duckdb`, les 4 requêtes du
rapport mensuel. Chaque requête est vérifiée à la main (nombre de lignes + cohérence des
totaux).

| Requête | Lignes attendues |
|---|---|
| R1 : CA, nb de ventes, panier moyen par magasin (trié CA décroissant) | 5 |
| R2 : CA par catégorie (par clé), trié CA décroissant | 8 |
| R3 : CA par année (2 lignes) | 2 |
| R4 : Espèces / Carte / Mobile Money (id 3) par magasin | 5 |

**Contrôles de cohérence.** (i) La somme des CA de R1 = 7 908 259 731 FCFA. (ii) La
somme des CA de R2 = 7 908 259 731 FCFA. (iii) La somme des CA de R3 = 7 908 259 731 FCFA.
(iv) La somme des `nb_ventes` de R1 = 50 008.

**Corrigé.**

```sql
-- R1
SELECT m.nom, COUNT(*) AS nb, ROUND(SUM(v.montant_ttc)) AS ca,
       ROUND(AVG(v.montant_ttc)) AS panier_moyen
FROM vente v JOIN magasin m ON m.id_magasin = v.id_magasin
GROUP BY m.nom
ORDER BY ca DESC;

-- R2
SELECT c.rayon, c.sous_categorie, COUNT(*) AS nb, ROUND(SUM(v.montant_ttc)) AS ca
FROM vente v
JOIN produit p ON p.id_produit = v.id_produit
JOIN categorie c ON c.id_categorie = p.id_categorie
GROUP BY c.rayon, c.sous_categorie
ORDER BY ca DESC;

-- R3
SELECT EXTRACT(YEAR FROM date_vente) AS annee, COUNT(*) AS nb,
       ROUND(SUM(montant_ttc)) AS ca
FROM vente
GROUP BY 1
ORDER BY annee;

-- R4
SELECT id_magasin,
       SUM(CASE WHEN id_mode = 1 THEN 1 ELSE 0 END) AS especes,
       SUM(CASE WHEN id_mode = 2 THEN 1 ELSE 0 END) AS cartes,
       SUM(CASE WHEN id_mode = 3 THEN 1 ELSE 0 END) AS mobile
FROM vente
GROUP BY id_magasin
ORDER BY id_magasin;
```

> **Dans les faits.** PostgreSQL exécute ces 4 requêtes avec le même résultat ; le
> `GROUP BY m.nom` (R1) est accepté car `nom` est fonctionnellement dépendant de
> `id_magasin` — DuckDB l'accepte aussi, mais la pratique portable reste de citer la clé
> (`GROUP BY m.id_magasin, m.nom`). MySQL en mode `ONLY_FULL_GROUP_BY` exigera que toute
> colonne du `SELECT` soit agrégée ou groupée ; en mode permissif, il devine — à éviter
> (cf. M07.C04 §13).

## 14. Boîte à outils du chapitre

> **Boîte à outils.** Ce chapitre installe 4 outils de regroupement : `GROUP BY` (une
> ligne de synthèse par groupe), le **regroupement par clé** (piège du libellé doublé),
> `HAVING` (filtre sur les groupes), et les **comptages conditionnels**
> (`SUM(CASE WHEN … THEN 1 ELSE 0 END)` par groupe). La distinction `WHERE` / `HAVING`
> est le réflexe à acquérir.

| Outil | Usage | Syntaxe | Piège |
|---|---|---|---|
| `GROUP BY col` | une ligne par groupe | `GROUP BY id_magasin` | colonne du `SELECT` ni agrégée ni groupée |
| Clé de regroupement | regrouper sans fusionner | `GROUP BY c.id_categorie` | le libellé doublé (rayon) fusionne |
| Multi-colonnes | coupe croisée | `GROUP BY id_magasin, annee` | chaque ligne = une combinaison |
| `HAVING` | filtrer les groupes | `HAVING COUNT(*) > 9900` | l'écrire dans `WHERE` (erreur) |
| `SUM(CASE …)` | comptage conditionnel | `SUM(CASE WHEN id_mode = 1 THEN 1 ELSE 0 END)` | oublier `ELSE 0` |
| Contrôle | cohérence des totaux | somme des groupes = total global | ne pas vérifier le nombre de groupes |

## 15. Résumé du chapitre

- **`GROUP BY`** subdivise les lignes en groupes ; chaque agrégat est calculé par groupe ;
  le résultat contient une ligne par groupe.
- **Regrouper par la clé** (`id_*`), pas par le libellé : un libellé doublé fusionne
  silencieusement deux groupes (5 rayons au lieu de 8 catégories).
- **`GROUP BY a, b`** = une ligne par couple (a, b) : les coupes croisées.
- **`WHERE`** filtre les lignes (avant agrégation) ; **`HAVING`** filtre les groupes
  (après agrégation). Filtrer sur un total ⇒ `HAVING`.
- Le **comptage conditionnel** `SUM(CASE WHEN … THEN 1 ELSE 0 END)` produit les tableaux
  de bord croisés : une colonne de mesure par condition, par groupe.
- **Contrôle systématique** : nombre de groupes + somme des agrégats = total global.

## 16. À retenir

- **Une ligne par groupe** : `GROUP BY` est la plieuse par tiroirs.
- **Clé, pas libellé** : le total juste ne suffit pas — le nombre de groupes doit être
  juste.
- **`WHERE` lignes / `HAVING` groupes** : si vous filtrez sur un total, c'est `HAVING`.
- **`ELSE 0` obligatoire** dans les comptages conditionnels.
- **Cohérence** : somme des CA par groupe = CA global (7 908 259 731 FCFA).

> **À retenir.** Le `HAVING` est le seul endroit où l'on peut **comparer un agrégat à un
> seuil** : `HAVING SUM(montant_ttc) > X`. Tout le reste de la requête (`WHERE`,
> `ORDER BY`, `LIMIT`) travaille sur des lignes ou sur des alias — jamais directement sur
> un agrégat dans `WHERE`.

## 17. Évaluation formative (auto-correction, 8 min)

Sans document, en 8 minutes, répondre aux 5 questions. Auto-correction en bas.

1. Combien de lignes produit `SELECT id_magasin, COUNT(*) FROM vente GROUP BY id_magasin;` ?
2. Pourquoi regrouper par `c.rayon` au lieu de `c.id_categorie` est-il risqué ici ?
3. Où écrire `COUNT(*) > 9900` : dans `WHERE` ou dans `HAVING` ? Pourquoi ?
4. Que fait `SUM(CASE WHEN id_mode = 1 THEN 1 ELSE 0 END)` dans un `GROUP BY` ?
5. Quel est le contrôle de cohérence à faire sur un `GROUP BY` ?

**Réponses** :

1. **5 lignes** — une par groupe, donc une par magasin (5 magasins dans le socle).
2. Parce que le libellé `rayon` est **doublé** (Alimentaire, Bricolage, Jardinage) : le
   regroupement fusionnerait silencieusement 8 catégories en 5 groupes, sans erreur.
3. Dans **`HAVING`** : `COUNT(*)` est un agrégat, et seuls les groupes sont filtrés par
   `HAVING`. Dans `WHERE`, c'est une erreur (« WHERE clause cannot contain
   aggregates »).
4. Il compte, **dans chaque groupe**, les lignes où `id_mode = 1` (les ventes Espèces) :
   une colonne de comptage conditionnel par groupe.
5. Deux contrôles : (i) le **nombre de groupes** est conforme (5 magasins, 8 catégories) ;
   (ii) la **somme des agrégats** par groupe redonne l'agrégat global (CA total
   7 908 259 731 FCFA).
