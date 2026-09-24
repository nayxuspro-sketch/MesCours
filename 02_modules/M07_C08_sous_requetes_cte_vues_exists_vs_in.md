# Module M07.C08 — Sous-requêtes, CTE, vues, EXISTS vs IN

**Outils comparés : DuckDB 1.5.5 (CLI + Python), SQLite natif Python, PostgreSQL cité.
Durée indicative : 4 h. Niveau : N2 → N3. Prérequis : M07.C01 (SELECT, FROM) ; M07.C05 (GROUP BY) ; M07.C07 (jointures).**

> **L'idée du chapitre.** C07 a relié les tables par des jointures. C08 montre comment
> **structurer** une requête quand la question est composée : d'abord calculer quelque
> chose, puis filtrer sur le résultat. C'est le passage de la requête « plate » à la
> requête « en couches » : la **sous-requête** (une requête dans une autre), la **CTE**
> (`WITH` — une sous-requête nommée), la **vue** (une sous-requête enregistrée), et la
> famille **`EXISTS` / `IN`** (exister ou non dans un ensemble) qui inclut le pattern
> canonique de la **double négation** (piège P6 : « les clients qui ont acheté **tous**
> les produits X »). Le fil rouge est la base `commercial.duckdb` : on y identifie le
> client n° 1 par CA (Client_0073, 11 561 026 FCFA), on lit la vue `v_ca_mensuel_magasin`
> (120 lignes), et on mesure que **119 clients** ont acheté les 2 produits les plus chers
> (double négation).

> **Base de travail — `commercial.duckdb` (empreinte `0b9c12397d9c8af2…`).** Le chapitre
> mobilise : 50 008 ventes, 1 200 clients (tous ont au moins une vente — les « clients sans
> vente » sont donc 0), 380 produits (55 dans la catégorie Alimentaire-Boissons, id 1), et
> la vue `v_ca_mensuel_magasin` (120 lignes : 5 magasins × 24 mois).

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous saurez :

- **écrire une sous-requête scalaire** (une valeur) dans le `SELECT` ou le `WHERE` ;
- **écrire une sous-requête dans le `FROM`** (table dérivée) et l'agréger ;
- **nommer une sous-requête** avec `WITH` (CTE) pour lisibilité et réutilisation ;
- **créer une vue** et comprendre sa différence avec une CTE (enregistrée vs éphémère) ;
- **distinguer `IN` de `EXISTS`** (et leurs négations) pour tester l'appartenance à un
  ensemble ;
- **écrire le pattern de double négation** (`NOT EXISTS … NOT EXISTS`) pour les questions
  « **tous les** » (piège P6).

## 2. Pourquoi cette notion est importante

- **Les questions métier réelles sont composées** : « les ventes au-dessus du panier
  moyen », « le client qui a le plus dépensé », « les clients qui ont tout acheté ».
  Aucune ne se pose en une seule requête plate — il faut d'abord **calculer**, puis
  **utiliser le résultat**.
- **La CTE (`WITH`) est l'outil de lisibilité** : une requête de 40 lignes devient 4 blocs
  nommés. C'est la différence entre une requête lisible par un collègue et une requête
  qu'on n'ose pas toucher.
- **`EXISTS` vs `IN`** est l'un des points les plus demandés en entretien, et la
  **double négation** est le pattern canonique des questions « tous les » — celles que
  `IN` et `COUNT` ne savent pas poser.

## 3. Explication simple — la sous-requête est une question dans une question

Une sous-requête, c'est poser **une question à l'intérieur d'une autre**. « Trouve-moi les
ventes **au-dessus du panier moyen** » se décompose en deux questions : (1) « quel est le
panier moyen ? » (2) « quelles ventes dépassent ce chiffre ? ». En SQL, la question (1)
s'écrit **dedans** la question (2) :

```
SELECT … FROM vente
WHERE montant_ttc > ( SELECT AVG(montant_ttc) FROM vente )
                       ↑ la question dans la question
```

Le moteur exécute d'abord la question de l'intérieur (le panier moyen : 158 140 FCFA),
puis la question de l'extérieur avec ce résultat. `WITH` (la CTE) fait la même chose, mais
**nomme** la question intérieure : `WITH panier AS (SELECT AVG(…) …) SELECT … WHERE …
> (SELECT … FROM panier)`. Et la **vue** enregistre cette CTE nommée dans la base, pour la
réutiliser.

> **Définition.** Une **sous-requête** — *subquery* — est une requête SQL **implantée à
> l'intérieur** d'une autre requête, dans le `SELECT`, le `WHERE` ou le `FROM`. Elle est
> exécutée d'abord (ou à la demande), et son résultat alimente la requête extérieure. On
> distingue la sous-requête **scalaire** (renvoie 1 valeur) et la sous-requête **de liste**
> (renvoie une colonne de valeurs, pour un `IN`).

## 4. Vocabulaire essentiel

| Français — English | Définition simple | Piège à éviter |
|---|---|---|
| **sous-requête scalaire** | une sous-requête qui renvoie **1 valeur** (1 ligne, 1 colonne). | l'utiliser quand elle renvoie plusieurs lignes (erreur). |
| **sous-requête de liste** | renvoie une **colonne** de valeurs, pour un `IN` / `NOT IN`. | `NOT IN` avec des `NULL` dans la liste (rien ne passe). |
| **CTE** (`WITH`) | une sous-requête **nommée**, déclarée en tête de requête. | croire qu'une CTE est optimisée comme une vue (c'est du sucre de lisibilité). |
| **vue** | une requête **enregistrée** dans la base, interrogée comme une table. | croire qu'elle fige les données (elle se recalcule à chaque lecture). |
| **table dérivée** | une sous-requête dans le `FROM` (avec un alias obligatoire). | oublier l'alias (erreur de syntaxe). |
| **EXISTS** | teste s'il **existe** au moins une ligne dans une sous-requête corrélée. | le confondre avec `IN` (EXISTS regarde l'existence, IN l'appartenance). |
| **corrélé** | une sous-requête qui référence une colonne de la requête extérieure. | le confondre avec une sous-requête indépendante (exécutée une fois). |
| **double négation** | `NOT EXISTS (… NOT EXISTS (…))` : le pattern des questions « **tous les** ». | essayer de le faire avec `IN` ou `COUNT` (faux ou illisible). |

## 5. Cours approfondi

### 5.1 La sous-requête scalaire dans le `SELECT`

La sous-requête scalaire renvoie **une valeur** qu'on place dans le `SELECT` :

```sql
SELECT v.id_vente, v.montant_ttc,
       (SELECT AVG(montant_ttc) FROM vente) AS panier_moyen_global
FROM vente v
ORDER BY v.id_vente
LIMIT 3;
```

→ Chaque ligne affiche le montant de la vente **et** le panier moyen global (158 140
FCFA, recalculé). C'est le motif « contexte » : afficher une valeur de référence à côté de
chaque ligne.

### 5.2 La sous-requête scalaire dans le `WHERE`

« Les ventes au-dessus du panier moyen » :

```sql
SELECT COUNT(*) AS nb_ventes
FROM vente
WHERE montant_ttc > (SELECT AVG(montant_ttc) FROM vente);
```

Le moteur calcule d'abord `AVG(montant_ttc)` = 158 140 FCFA, puis filtre les ventes qui le
dépassent : **20 289** ventes. La comparaison est faite contre la valeur calculée, pas
contre une constante — c'est la force de la sous-requête scalaire dans le `WHERE`.

> **Définition.** Une **sous-requête scalaire** — *scalar subquery* — est une sous-requête
> qui doit renvoyer **exactement une valeur** (1 ligne, 1 colonne). Elle s'utilise dans le
> `SELECT` (valeur de référence par ligne) ou le `WHERE` (filtre contre une valeur
> calculée). Si elle renvoie plus d'une ligne, DuckDB/PostgreSQL renvoient une erreur ;
> c'est un garde-fou, pas un bug.

### 5.3 La sous-requête dans le `FROM` — la table dérivée

Quand la question intérieure renvoie **plusieurs lignes**, on la met dans le `FROM` (avec
un **alias obligatoire**) :

```sql
SELECT seg, COUNT(*) AS nb
FROM (
  SELECT CASE
           WHEN c.type_client = 'particulier' THEN 'Particulier'
           WHEN c.type_client = 'entreprise'  THEN 'Entreprise'
           ELSE 'Comptoir'
         END AS seg
  FROM vente v
  JOIN client c ON c.id_client = v.id_client
) t
GROUP BY seg
ORDER BY nb DESC;
```

La sous-requête (alias `t`) produit 50 008 lignes avec une colonne `seg` ; l'extérieur
les regroupe. C'est l'alternative à la CTE — même chose, sans nom.

### 5.4 La CTE (`WITH`) — nommer la question intérieure

Le `WITH` **nomme** la sous-requête du `FROM` (ou d'une étape intermédiaire) :

```sql
WITH ca_par_client AS (
  SELECT c.id_client, c.nom, ROUND(SUM(v.montant_ttc)) AS ca
  FROM vente v
  JOIN client c ON c.id_client = v.id_client
  GROUP BY c.id_client, c.nom
)
SELECT nom, ca
FROM ca_par_client
ORDER BY ca DESC
LIMIT 3;
```

→ Client_0073 en tête avec **11 561 026 FCFA** (le client n° 1 par CA, id 73). Le `WITH`
ne change pas le résultat par rapport à la table dérivée — il change la **lisibilité** :
chaque étape a un nom, on peut la relire séparément.

> **Définition.** Une **CTE** — *Common Table Expression* — est une sous-requête **nommée**,
> déclarée en tête de requête par `WITH nom AS (SELECT …)`, puis référencée comme une table
> dans le reste de la requête. Elle est **éphémère** (n'existe que durant l'exécution de la
> requête) et sert surtout à la **lisibilité** : découper une requête complexe en étapes
> nommées. Elle se distingue d'une **vue** (enregistrée dans la base, réutilisable).

### 5.5 La vue — une CTE enregistrée

La base contient déjà la vue `v_ca_mensuel_magasin` (120 lignes : 5 magasins × 24 mois).
Une vue est une requête **enregistrée** dans le schéma, interrogée comme une table :

```sql
SELECT id_magasin, annee, mois, nb_ventes, ROUND(ca_ttc) AS ca_ttc
FROM v_ca_mensuel_magasin
ORDER BY ca_ttc DESC
LIMIT 3;
```

→ Le plus gros mois : magasin 3, 2025-08, 444 ventes, 78 965 529 FCFA. La vue **ne fige
pas** les données : elle se **recalcule** à chaque lecture (si `vente` change, la vue
change). C'est le motif de C05/C06 « l'étiquette réutilisable » : on calcule une fois (la
vue), on relit partout.

> **Définition.** Une **vue** — *view* — est une requête SQL **enregistrée** dans le
> schéma de la base, interrogable comme une table (`SELECT … FROM vue`). Contrairement à
> une CTE (éphémère, liée à une requête), une vue **persiste** et est **réutilisable** par
> n'importe quelle requête. Elle ne stocke pas de données : elle **se recalcule** à chaque
> lecture. C'est l'outil d'encapsulation des étiquettes et des agrégats de base de travail.

### 5.6 `IN` — appartenir à un ensemble

`WHERE x IN (sous-requête)` teste si `x` appartient à la liste renvoyée :

```sql
SELECT COUNT(DISTINCT v.id_client) AS nb_clients
FROM vente v
JOIN produit p ON p.id_produit = v.id_produit
WHERE p.id_categorie IN (SELECT id_categorie FROM produit WHERE actif = FALSE);
```

Ou, plus simplement, « les clients qui ont acheté au moins un produit de la catégorie 1 » :

```sql
SELECT COUNT(DISTINCT v.id_client) AS nb_clients
FROM vente v
WHERE v.id_produit IN (SELECT id_produit FROM produit WHERE id_categorie = 1);
```

→ **1 196 clients** (sur 1 200) ont acheté au moins un des 55 produits de la catégorie
Alimentaire-Boissons. Le `IN` est l'opérateur « **au moins un** ».

> **À retenir.** Le sens de `IN` est « **au moins un** » : `WHERE x IN (…)` = « il existe
> au moins une valeur de la liste égale à `x` ». C'est pourquoi `IN` **ne pose jamais** une
> question « tous les » — pour celle-ci, il faut la double négation (§5.9). Confondre
> « au moins un » et « tous » est l'erreur la plus fréquente des requêtes d'appartenance.

### 5.7 `NOT IN` et le piège des `NULL`

`NOT IN` est le « **aucun** » : « les clients qui n'ont acheté **aucun** produit de la
catégorie 1 » :

```sql
SELECT COUNT(*) AS nb_clients
FROM client c
WHERE c.id_client NOT IN (SELECT id_client FROM vente v
                          JOIN produit p ON p.id_produit = v.id_produit
                          WHERE p.id_categorie = 1);
```

→ **4 clients** (1 200 − 1 196). Attention au piège : si la sous-requête du `NOT IN`
renvoie **un seul `NULL`**, le `NOT IN` ne renvoie **aucune ligne** (car `x NOT IN (a,
NULL)` est `NULL` si `x ≠ a` — ni vrai ni faux). C'est le défaut classique du `NOT IN`.

### 5.8 `EXISTS` / `NOT EXISTS` — exister ou non

`EXISTS` teste s'il **existe** au moins une ligne dans une sous-requête **corrélée** (qui
référence la ligne extérieure) :

```sql
SELECT COUNT(*) AS nb_clients
FROM client c
WHERE EXISTS (SELECT 1 FROM vente v WHERE v.id_client = c.id_client);
```

→ **1 200** (tous les clients ont au moins une vente). Le `NOT EXISTS` est le « aucun » :

```sql
SELECT COUNT(*) AS nb_clients_sans_vente
FROM client c
WHERE NOT EXISTS (SELECT 1 FROM vente v WHERE v.id_client = c.id_client);
```

→ **0** (aucun client sans vente dans le socle). Le `EXISTS`/`NOT EXISTS` est souvent plus
lisible (et plus sûr face aux `NULL`) que `IN`/`NOT IN` pour les tests d'existence.

> **Définition.** **`EXISTS`** teste s'il **existe** au moins une ligne dans sa
> sous-requête (généralement **corrélée** : elle référence une colonne de la requête
> extérieure). **`NOT EXISTS`** est sa négation. Contrairement à `IN`/`NOT IN`, ils sont
> **insensibles aux `NULL`** de la liste et court-circuitent dès qu'une ligne existe —
> c'est l'outil de référence pour les tests d'existence et la double négation.

### 5.9 Le pattern de double négation — les « **tous les** » (P6)

La question « les clients qui ont acheté **tous** les produits les plus chers » (ou « tous
les produits d'une catégorie ») ne se pose **ni** avec `IN` (qui dit « au moins un »)
**ni** avec `COUNT` (fragile). Le pattern canonique est la **double négation** :
« il n'existe **aucun** produit X que le client n'a **pas** acheté » :

```sql
SELECT c.id_client, c.nom
FROM client c
WHERE NOT EXISTS (
  SELECT 1
  FROM (SELECT id_produit FROM vente ORDER BY montant_ttc DESC LIMIT 2) top
  WHERE NOT EXISTS (
    SELECT 1 FROM vente v
    WHERE v.id_client = c.id_client AND v.id_produit = top.id_produit
  )
);
```

Logique : on cherche les clients `c` tels qu'**il n'existe aucun** produit du top 2 que `c`
**n'a pas** acheté. C'est-à-dire les clients qui ont acheté les **deux**. → **119 clients**.

> **Définition.** Le **pattern de double négation** — *double negation* — est l'écriture
> `NOT EXISTS (SELECT … WHERE NOT EXISTS (SELECT …))` qui exprime « **tous les** » : on
> nie l'existence d'un contre-exemple. « Le client a acheté **tous** les produits X »
> équivaut à « il n'existe **aucun** produit X que le client n'a **pas** acheté ». C'est
> le pattern canonique (piège P6) des questions universelles, là où `IN` (« au moins un »)
> et `COUNT` (fragile) échouent.

> **Attention.** Ne pas poser une question « **tous les** » avec `IN` :
> `WHERE id_client IN (…)` renvoie ceux qui ont acheté **au moins un**, pas **tous**.
> Et ne pas le faire avec un `COUNT` comparé au total (fragile, et faux dès qu'un produit
> est acheté en double). La double négation est l'écriture sûre.

## 6. Exemple concret — la requête qui répond à une question métier

Le directeur demande : *« Quel est le client qui a le plus dépensé, et combien de clients
ont acheté les 2 produits les plus chers ? »*

**Étape 1 — Écrire les deux requêtes** (une CTE pour le top client, une double négation pour
les 2 plus chers).

```sql
-- (a) Le client n°1 par CA
WITH ca_par_client AS (
  SELECT c.id_client, c.nom, ROUND(SUM(v.montant_ttc)) AS ca
  FROM vente v
  JOIN client c ON c.id_client = v.id_client
  GROUP BY c.id_client, c.nom
)
SELECT nom, ca
FROM ca_par_client
ORDER BY ca DESC
LIMIT 1;

-- (b) Les clients qui ont acheté les 2 produits les plus chers
SELECT COUNT(*) AS nb_clients
FROM client c
WHERE NOT EXISTS (
  SELECT 1
  FROM (SELECT id_produit FROM vente ORDER BY montant_ttc DESC LIMIT 2) top
  WHERE NOT EXISTS (
    SELECT 1 FROM vente v
    WHERE v.id_client = c.id_client AND v.id_produit = top.id_produit
  )
);
```

**Étape 2 — Prédire.** (a) 1 ligne, le client n° 1 par CA (id 73). (b) Un nombre < 1 200
(ceux qui ont les 2 produits du top).

**Étape 3 — Exécuter.** (a) Client_0073, 11 561 026 FCFA. (b) **119** clients.

**Étape 4 — Comparer.** Le top client est cohérent avec l'ATTENDU (id 73). Les 119 clients
du (b) sont plausibles (les 2 produits les plus chers sont vendus, mais pas par tous).

> **Conseil professionnel.** Quand une question contient « **tous les** », « **chaque** »,
> « **aucun** », passez directement à la **double négation** (`NOT EXISTS … NOT EXISTS`).
> Ne perdez pas de temps à essayer `IN` ou `COUNT` : ils donnent le mauvais sens (« au
> moins un ») ou un résultat fragile. Le « tous les » = « aucun contre-exemple ».

## 7. Démonstration pas à pas — 6 requêtes sur le fil rouge

### 7.1 Question 1 — Panier moyen comme référence (scalaire dans `SELECT`)

```sql
SELECT id_vente, montant_ttc,
       (SELECT ROUND(AVG(montant_ttc)) FROM vente) AS panier_moyen
FROM vente
ORDER BY id_vente
LIMIT 3;
```

→ 3 lignes, chacune avec le panier moyen global (158 140 FCFA) en référence.

### 7.2 Question 2 — Le client n° 1 par CA (CTE)

```sql
WITH ca_par_client AS (
  SELECT c.id_client, c.nom, ROUND(SUM(v.montant_ttc)) AS ca
  FROM vente v
  JOIN client c ON c.id_client = v.id_client
  GROUP BY c.id_client, c.nom
)
SELECT id_client, nom, ca
FROM ca_par_client
ORDER BY ca DESC
LIMIT 1;
```

→ id 73, Client_0073, 11 561 026 FCFA.

### 7.3 Question 3 — La vue mensuelle (120 lignes)

```sql
SELECT COUNT(*) AS nb_lignes,
       ROUND(MAX(ca_ttc)) AS plus_gros_mois
FROM v_ca_mensuel_magasin;
```

→ **120** lignes, plus gros mois 78 965 529 FCFA (magasin 3, 2025-08).

### 7.4 Question 4 — Les clients ayant acheté la catégorie 1 (`IN`)

```sql
SELECT COUNT(DISTINCT v.id_client) AS nb_clients
FROM vente v
WHERE v.id_produit IN (SELECT id_produit FROM produit WHERE id_categorie = 1);
```

→ **1 196** clients.

### 7.5 Question 5 — Les clients sans vente (`NOT EXISTS`)

```sql
SELECT COUNT(*) AS nb_clients_sans_vente
FROM client c
WHERE NOT EXISTS (SELECT 1 FROM vente v WHERE v.id_client = c.id_client);
```

→ **0** (tous les clients ont au moins une vente).

### 7.6 Question 6 — Les 2 produits les plus chers (double négation)

```sql
SELECT COUNT(*) AS nb_clients
FROM client c
WHERE NOT EXISTS (
  SELECT 1
  FROM (SELECT id_produit FROM vente ORDER BY montant_ttc DESC LIMIT 2) top
  WHERE NOT EXISTS (
    SELECT 1 FROM vente v
    WHERE v.id_client = c.id_client AND v.id_produit = top.id_produit
  )
);
```

→ **119** clients.

## 8. Erreurs fréquentes

| # | Erreur | Symptôme | Correction |
|---|--------|----------|------------|
| 1 | Sous-requête scalaire qui renvoie plusieurs lignes | erreur « more than one row returned » | `LIMIT 1`, ou transformer en sous-requête de liste. |
| 2 | Table dérivée sans alias | erreur de syntaxe | toujours un alias (`) t`). |
| 3 | `NOT IN` avec des `NULL` dans la liste | 0 ligne (au lieu du résultat attendu) | `NOT EXISTS`, ou filtrer les `NULL` de la liste. |
| 4 | Poser « tous les » avec `IN` | renvoie « au moins un » (trop de clients) | double négation `NOT EXISTS … NOT EXISTS`. |
| 5 | Croire qu'une vue fige les données | la vue change quand la base change | une vue se recalcule à chaque lecture. |
| 6 | CTE complexe sans nom | requête illisible, impossible à maintenir | découper en CTE nommées (une par étape). |

> **Attention.** Le piège du `NOT IN` avec `NULL` est silencieux : si la sous-requête
> renvoie un `NULL`, `x NOT IN (…, NULL)` est `NULL` pour tout `x` qui n'est pas dans la
> partie non nulle — **aucune ligne ne passe**. C'est le bug le plus classique des
> « exclusions ». Privilégier `NOT EXISTS` (insensible aux `NULL`).

> **Attention.** Une CTE n'est **pas une optimisation** : c'est du sucre de lisibilité.
> Sur certaines bases, une CTE peut même être **matérialisée** (calculée une fois, stockée)
> alors qu'une table dérivée serait inline. Ne pas écrire une CTE « pour aller plus
> vite » : on écrit une CTE **pour être lisible**.

## 9. Bonnes pratiques professionnelles

- **Une CTE par étape** de la logique : `WITH brut AS (…), agrégé AS (…), résultat AS (…)`
  puis `SELECT … FROM résultat`.
- **La sous-requête scalaire** pour une valeur de référence (panier moyen, seuil) ; la
  **sous-requête de liste** pour un `IN`.
- **`NOT EXISTS` plutôt que `NOT IN`** dès que la liste peut contenir des `NULL`.
- **« Tous les » = double négation** : `NOT EXISTS (… NOT EXISTS (…))`.
- **Vue pour les étiquettes réutilisées** (CA mensuel, segmentation) ; CTE pour les étapes
  éphémères d'une seule requête.
- **Nommer les CTE** par leur rôle métier (`ca_par_client`, `top_produits`), pas `t1`,
  `t2`.

## 10. Exercice guidé — le top client et les acheteurs du top (15 min, /10)

**Énoncé.** (a) Renvoyer le client n° 1 par CA (id, nom, CA) avec une CTE. (b) Renvoyer le
nombre de clients qui ont acheté les 2 produits les plus chers (double négation).

**Grille de correction (/10).**

| Critère | Points |
|---|---|
| (a) CTE `ca_par_client` avec `GROUP BY` + `ORDER BY ca DESC LIMIT 1` | 3 |
| (a) Résultat : id 73, Client_0073, 11 561 026 FCFA | 2 |
| (b) Double négation `NOT EXISTS … NOT EXISTS` correcte | 4 |
| (b) Résultat : 119 clients | 1 |

**Corrigé.** Cf. §6, étape 1. (a) → 73, Client_0073, 11 561 026. (b) → 119.

## 11. Exercices autonomes

### Exercice 1 — Le panier moyen en référence

Afficher les 5 premières ventes avec le panier moyen global (sous-requête scalaire dans le
`SELECT`).

### Exercice 2 — Le client n° 1 par CA

Avec une CTE, renvoyer l'id, le nom et le CA du client le plus dépensier.

### Exercice 3 — La vue mensuelle

Nombre de lignes de `v_ca_mensuel_magasin` et le plus gros mois (en CA).

### Exercice 4 — Les acheteurs de la catégorie 1

Le nombre de clients distincts ayant acheté au moins un produit de la catégorie 1
(`IN`).

### Exercice 5 — Les clients sans vente

Le nombre de clients n'ayant **aucune** vente (`NOT EXISTS`).

### Exercice 6 — Les acheteurs du top 2

Le nombre de clients ayant acheté les **2** produits les plus chers (double négation).

### Exercice 7 — `NOT IN` vs `NOT EXISTS`

Réécrire l'exercice 5 avec `NOT IN` et expliquer en quoi `NOT EXISTS` est plus sûr.

### Exercice 8 — Un `COUNT` à 0 : bug ou bon résultat ?

Cette requête renvoie **0**. Est-ce un bug ? Vérifiez par une méthode indépendante et
expliquez pourquoi le 0 est (ou non) un résultat cohérent.

```sql
SELECT COUNT(*) FROM client c
WHERE c.id_client NOT IN (
  SELECT v.id_client FROM vente v
  WHERE v.montant_ttc > (SELECT AVG(montant_ttc) FROM vente)
);
```

## 12. Correction détaillée

**Exercice 1.** Cf. §7.1 → 5 lignes, chacune avec 158 140 FCFA en référence.

**Exercice 2.** Cf. §7.2 → id 73, Client_0073, 11 561 026 FCFA.

**Exercice 3.** Cf. §7.3 → 120 lignes, plus gros mois 78 965 529 FCFA.

**Exercice 4.** Cf. §7.4 → **1 196** clients.

**Exercice 5.** Cf. §7.5 → **0** client.

**Exercice 6.** Cf. §7.6 → **119** clients.

**Exercice 7.**

```sql
SELECT COUNT(*) FROM client c
WHERE c.id_client NOT IN (SELECT id_client FROM vente);
```

Sur ce socle, les deux renvoient 0 (tous les clients ont une vente). Mais `NOT IN` est
fragile : si une seule `id_client` de la sous-requête était `NULL`, le `NOT IN` renverrait
0 ligne **même s'il existe des clients sans vente**. `NOT EXISTS` est insensible aux
`NULL` et toujours correct.

**Exercice 8.** Ce 0 est un **bon résultat**, pas un bug. La requête compte les clients
n'ayant **aucune** vente au-dessus de la moyenne globale (158 140 FCFA). Chaque client
ayant en moyenne 42 ventes (50 008 / 1 200) et des montants répartis de 763 à 594 363
FCFA, il est quasi-certain que chacun a au moins une vente au-dessus de la moyenne : le
`COUNT` renvoie donc légitimement 0. La vérification par méthode indépendante : la même
question en `NOT EXISTS` renvoie aussi 0. Leçon : un `COUNT` à 0 n'est un bug que s'il
contredit les données — on le contrôle par une requête indépendante (ici `NOT EXISTS`), et
on se méfie du `NOT IN` seulement quand la liste sous-jacente peut contenir des `NULL`
(pas le cas ici : `id_client` est non nul).

## 13. Mini-projet — « L'audit des requêtes composées » (40 min)

Produire l'audit des requêtes composées : 4 requêtes, chacune vérifiée à la main.

| Requête | Lignes / valeur attendue |
|---|---|
| S1 : le client n° 1 par CA (CTE) | 73, 11 561 026 |
| S2 : le plus gros mois de la vue mensuelle | 78 965 529 |
| S3 : les acheteurs de la catégorie 1 (`IN`) | 1 196 |
| S4 : les acheteurs du top 2 (double négation) | 119 |

**Contrôles de cohérence.** (i) S3 ≤ 1 200 (nombre de clients). (ii) S4 ≤ S3 (les acheteurs
du top 2 sont un sous-ensemble). (iii) S2 ≤ 7 908 259 731 / 120 (un mois ne dépasse pas le
moyenne mensuelle du CA total).

**Corrigé.**

```sql
-- S1
WITH ca_par_client AS (
  SELECT c.id_client, c.nom, ROUND(SUM(v.montant_ttc)) AS ca
  FROM vente v
  JOIN client c ON c.id_client = v.id_client
  GROUP BY c.id_client, c.nom
)
SELECT id_client, nom, ca
FROM ca_par_client
ORDER BY ca DESC
LIMIT 1;

-- S2
SELECT ROUND(MAX(ca_ttc)) AS plus_gros_mois
FROM v_ca_mensuel_magasin;

-- S3
SELECT COUNT(DISTINCT v.id_client) AS nb_clients
FROM vente v
WHERE v.id_produit IN (SELECT id_produit FROM produit WHERE id_categorie = 1);

-- S4
SELECT COUNT(*) AS nb_clients
FROM client c
WHERE NOT EXISTS (
  SELECT 1
  FROM (SELECT id_produit FROM vente ORDER BY montant_ttc DESC LIMIT 2) top
  WHERE NOT EXISTS (
    SELECT 1 FROM vente v
    WHERE v.id_client = c.id_client AND v.id_produit = top.id_produit
  )
);
```

> **Dans les faits.** `WITH` (CTE), `EXISTS`/`NOT EXISTS`, `IN` et les vues sont
> **standard SQL** : identiques sur DuckDB, PostgreSQL et SQLite. Seule nuance : la
> **matérialisation des CTE** varie (PostgreSQL peut choisir de matérialiser ou d'inline ;
> DuckDB gère les CTE récursives ; SQLite aussi depuis la version 3.8.3). Pour la
> portabilité, éviter les CTE **récursives** dans du code qui doit tourner sur SQLite
> ancien.

## 14. Boîte à outils du chapitre

> **Boîte à outils.** Ce chapitre installe 4 outils de structuration : la **sous-requête**
> (scalaire et de liste), la **CTE** (`WITH`, la sous-requête nommée), la **vue** (la CTE
> enregistrée), et la famille **`EXISTS`/`IN`** avec le pattern de **double négation** pour
> les « tous les ». La règle : une CTE par étape, `NOT EXISTS` plutôt que `NOT IN`, et la
> double négation pour les questions universelles.

| Outil | Usage | Syntaxe | Piège |
|---|---|---|---|
| Sous-requête scalaire | 1 valeur de référence | `(SELECT AVG(…) FROM vente)` | plusieurs lignes = erreur |
| Sous-requête de liste | un `IN` | `WHERE x IN (SELECT …)` | `NOT IN` + `NULL` = 0 ligne |
| Table dérivée | sous-requête du `FROM` | `FROM (SELECT …) t` | alias obligatoire |
| CTE (`WITH`) | étape nommée | `WITH nom AS (SELECT …)` | sucre de lisibilité, pas d'optimisation |
| Vue | CTE enregistrée | `CREATE VIEW … AS SELECT …` | se recalcule, ne fige pas |
| `EXISTS` / `NOT EXISTS` | test d'existence | `WHERE EXISTS (SELECT 1 …)` | corrélée, court-circuit |
| Double négation | les « tous les » | `NOT EXISTS (… NOT EXISTS (…))` | P6 : ne pas le faire avec `IN` |

## 15. Résumé du chapitre

- **Sous-requête scalaire** (1 valeur, dans le `SELECT` ou le `WHERE`) ; **sous-requête de
  liste** (une colonne, pour un `IN`).
- **CTE (`WITH`)** = sous-requête **nommée**, éphémère, outil de **lisibilité** (une par
  étape). **Vue** = CTE **enregistrée**, réutilisable, **se recalcule** (ne fige pas).
- **`IN`** = « au moins un » ; **`NOT IN`** = « aucun », mais **fragile face aux `NULL`**
  (renvoie 0 ligne si la liste contient un `NULL`).
- **`EXISTS`/`NOT EXISTS`** = test d'existence, **insensible aux `NULL`**, souvent plus
  sûr que `IN`/`NOT IN`.
- **Double négation** (`NOT EXISTS … NOT EXISTS`) = le pattern canonique des « **tous
  les** » (P6) : « aucun contre-exemple ». `IN` et `COUNT` ne le font pas.
- **Nuance de portabilité** : CTE, vues, `EXISTS` standard ; la matérialisation des CTE et
  les CTE récursives varient entre SGBD.

## 16. À retenir

- **Une CTE par étape**, nommée par son rôle métier : lisibilité avant tout.
- **Sous-requête scalaire** = 1 valeur de référence ; **de liste** = un `IN`.
- **`NOT EXISTS` plutôt que `NOT IN`** (sécurité face aux `NULL`).
- **« Tous les » = double négation** : `NOT EXISTS (… NOT EXISTS (…))` — jamais `IN`.
- **Une vue se recalcule** : c'est une encapsulation, pas un snapshot.

> **À retenir.** La sous-requête est une **question dans une question** ; la CTE la
> **nomme** ; la vue l'**enregistre** ; `EXISTS`/`IN` testent l'**appartenance**. Et dès
> que la question dit « **tous les** », on écrit la **double négation** : nier
> l'existence d'un contre-exemple est la seule écriture sûre.

## 17. Évaluation formative (auto-correction, 8 min)

Sans document, en 8 minutes, répondre aux 5 questions. Auto-correction en bas.

1. Différence entre une sous-requête scalaire et une sous-requête de liste ?
2. Quelle est la différence entre une CTE et une vue ?
3. Pourquoi `NOT IN` peut-il renvoyer 0 ligne, et comment éviter ce bug ?
4. Comment écrit-on « les clients qui ont acheté **tous** les produits X » ?
5. Une vue fige-t-elle les données ?

**Réponses** :

1. La sous-requête **scalaire** renvoie **1 valeur** (1 ligne, 1 colonne) — elle s'utilise
   dans le `SELECT` ou le `WHERE`. La sous-requête **de liste** renvoie une **colonne de
   valeurs** — elle s'utilise dans un `IN` / `NOT IN`.
2. Une **CTE** est une sous-requête **nommée**, **éphémère** (n'existe que durant la
   requête), déclarée par `WITH`. Une **vue** est une requête **enregistrée** dans le
   schéma, **réutilisable** par n'importe quelle requête, interrogée comme une table. Les
   deux se recalculent ; la vue persiste, la CTE non.
3. Parce que si la sous-requête du `NOT IN` renvoie **un `NULL`**, alors `x NOT IN (…,
   NULL)` est `NULL` (ni vrai ni faux) pour tout `x` non présent — **aucune ligne ne
   passe**. Éviter avec `NOT EXISTS` (insensible aux `NULL`) ou en filtrant les `NULL` de
   la liste.
4. Par la **double négation** : `WHERE NOT EXISTS (SELECT 1 FROM produit X WHERE NOT
   EXISTS (SELECT 1 FROM vente v WHERE v.id_client = c.id_client AND v.id_produit =
   p.id_produit))` — « il n'existe **aucun** produit X que le client **n'a pas** acheté ».
   `IN` (« au moins un ») et `COUNT` (fragile) ne le font pas.
5. **Non.** Une vue **se recalcule** à chaque lecture : si la table sous-jacente change, la
   vue change. C'est une encapsulation de requête, pas un snapshot de données.
