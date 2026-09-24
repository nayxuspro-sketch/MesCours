# Module M07.C06 — Catégoriser : CASE, COALESCE, NULLIF

**Outils comparés : DuckDB 1.5.5 (CLI + Python), SQLite natif Python, PostgreSQL cité.
Durée indicative : 3 h. Niveau : N2 → N3. Prérequis : M07.C01 (SELECT, FROM, alias) ; M07.C04 (agrégats) ; M07.C05 (GROUP BY).**

> **L'idée du chapitre.** Jusqu'ici, on a **lu** et **compté** les données. C06 les
> **transforme** : « segmenter les clients en 3 classes », « étiqueter chaque vente selon
> sa taille », « remplacer les absences par un texte neutre ». C'est le travail de
> **catégorisation** : `CASE` (la brique de logique conditionnelle du `SELECT`),
> `COALESCE` (le premier non nulle), `NULLIF` (le comparateur qui produit du `NULL`). Ces
> trois fonctions sont les outils de tout le travail de préparation de données : créer une
> colonne d'étiquette, normaliser un libellé, gérer les absences sans casser les agrégats.
> Le fil rouge est la base `commercial.duckdb` : on y segmente les 1 200 clients en 3
> types (particuliers 850, entreprises 229, comptoirs 121), on étiquette les 50 008 ventes
> en 3 tranches de montant, et on mesure le CA des produits **inactifs**
> (471 206 245 FCFA — un produit « retiré » peut très bien avoir été vendu hier).

> **Base de travail — `commercial.duckdb` (empreinte `0b9c12397d9c8af2…`).** Le chapitre
> mobilise : 1 200 clients (850 particuliers, 229 entreprises, 121 comptoirs ; Ouagadougou
> 512, Bobo-Dioulasso 441, Koudougou 247), 50 008 ventes (tranches : 12 753 / 21 509 /
> 15 746), 380 produits (362 actifs, 18 inactifs). Aucune colonne du socle ne contient de
> `NULL` (le générateur les exclut) : les fonctions `COALESCE` / `NULLIF` sont donc
> démontrées sur des expressions, pas sur des données réellement absentes.

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous saurez :

- **construire une colonne d'étiquette** avec `CASE WHEN … THEN … ELSE … END` (forme
  simple et forme de recherche) ;
- **segmenter** un jeu de données en classes (types de clients, tranches de montant) et
  agréger sur ces classes ;
- **gérer les absences** avec `COALESCE(x, défaut)` et comprendre pourquoi un `NULL` dans
  une somme « disparaît » ;
- **produire du `NULL` volontairement** avec `NULLIF(a, b)` et l'exploiter (filtrer les
  zéros, détecter des égalités) ;
- **combiner** ces fonctions dans un `SELECT` (et dans un `GROUP BY`) pour préparer des
  tableaux de bord lisibles.

## 2. Pourquoi cette notion est importante

- **`CASE` est l'outil n° 1 de la transformation de données** : 90 % des « colonnes
  créées » dans un entrepôt sont des `CASE` (segmentation, étiquettes, règles métier).
  C'est aussi la brique des comptages conditionnels de C04/C05 (`SUM(CASE WHEN …)`).
- **`COALESCE` est le remède aux `NULL`** : un champ vide qui casse une somme, un libellé
  null qui devient « (non renseigné) » dans le rapport. Le maîtriser, c'est ne plus être
  surpris par les `NULL` en production.
- **`NULLIF` est le miroir de `COALESCE`** : il transforme une valeur en `NULL` quand elle
  est égale à une référence — un filtre de zéros sans `WHERE`, une détection d'égalité.

## 3. Explication simple — `CASE` est le carrefour du `SELECT`

Le `SELECT` de C01 copiait des colonnes. C06 lui ajoute une **logique de carrefour** :
selon la valeur d'une colonne, on sort un libellé différent. Comme à un carrefour routier,
on regarde une plaque (la condition) et on prend une sortie (le libellé) :

- plaque « `type_client = 'particulier'` » → sortie « Particulier » ;
- plaque « `type_client = 'entreprise'` » → sortie « Entreprise » ;
- plaque « `type_client = 'comptoir'` » → sortie « Comptoir » ;
- sinon → sortie « Autre » (le `ELSE`).

`COALESCE` et `NULLIF` sont les deux faces de la gestion des **absences** :
`COALESCE(x, défaut)` dit « si `x` est absent, prends `défaut` » ; `NULLIF(a, b)` dit « si
`a` vaut `b`, rends `absent` (NULL) ; sinon rends `a` ».

> **Définition.** L'expression **`CASE`** — *expression conditionnelle* — est la brique de
> logique conditionnelle du `SELECT`. Sa forme de recherche est
> `CASE WHEN cond1 THEN r1 WHEN cond2 THEN r2 … ELSE r0 END` : les conditions sont testées
> **dans l'ordre**, la première qui passe choisit le résultat ; `ELSE` est la valeur de
> repli si aucune ne passe.

## 4. Vocabulaire essentiel

| Français — English | Définition simple | Piège à éviter |
|---|---|---|
| **CASE (recherche)** | `CASE WHEN c1 THEN r1 … ELSE r0 END` : un libellé par condition, testées dans l'ordre. | croire que les branches sont évaluées toutes en même temps (non, dans l'ordre, la 1ʳᵉ qui passe gagne). |
| **CASE (simple)** | `CASE x WHEN v1 THEN r1 … END` : compare `x` à une valeur. | le confondre avec la forme de recherche (syntaxes différentes). |
| **ELSE** | valeur de repli si aucune condition ne passe. | l'oublier (le résultat est `NULL` pour les non-couverts). |
| **segment** | classe de lignes partageant une étiquette `CASE`. | des segments qui se chevauchent (les `WHEN` sont exclusifs par construction). |
| **COALESCE** | `COALESCE(a, b, …)` : la **première** valeur non `NULL` de la liste. | croire qu'il remplace les zéros (il ne regarde que les `NULL`). |
| **NULLIF** | `NULLIF(a, b)` : `NULL` si `a = b`, sinon `a`. | le retourner (c'est `COALESCE` qui retourne). |
| **étiquette** | la colonne de texte produite par un `CASE`. | l'utiliser dans un `WHERE` avant qu'elle existe (il faut la recalculer ou une vue). |

## 5. Cours approfondi

### 5.1 `CASE` forme de recherche — segmenter les clients

```sql
SELECT id_client,
       nom,
       type_client,
       CASE
         WHEN type_client = 'particulier' THEN 'Particulier'
         WHEN type_client = 'entreprise'  THEN 'Entreprise'
         WHEN type_client = 'comptoir'    THEN 'Comptoir'
         ELSE 'Autre'
       END AS segment
FROM client
ORDER BY segment, nom
LIMIT 6;
```

La colonne `segment` est une **étiquette** : elle est calculée à la volée, elle n'existe
pas dans la table. Les 3 `WHEN` couvrent exactement les 3 valeurs du socle (850
particuliers, 229 entreprises, 121 comptoirs) : le `ELSE 'Autre'` n'attrapera rien ici,
mais il protège le code contre une 4ᵉ valeur qui arriverait demain.

> **Attention.** Les branches `WHEN` sont testées **dans l'ordre écrit**, et **la première
> qui passe gagne**. Un `CASE` où la condition la plus générale vient avant la plus
> restrictive rend les branches suivantes mortes. Ici les 3 `WHEN` sont mutuellement
> exclusifs (une valeur de `type_client` ne peut en valoir qu'une), donc l'ordre est sans
> effet — mais sur des conditions qui se chevauchent (des intervalles), l'ordre change le
> résultat.

### 5.2 `CASE` forme simple — le même, en plus court

Quand on compare **la même colonne** à plusieurs valeurs constantes, la forme simple est
plus lisible :

```sql
SELECT type_client,
       CASE type_client
         WHEN 'particulier' THEN 'Particulier'
         WHEN 'entreprise'  THEN 'Entreprise'
         WHEN 'comptoir'    THEN 'Comptoir'
         ELSE 'Autre'
       END AS segment
FROM client
LIMIT 3;
```

`CASE x WHEN v1 …` est un sucre syntaxique de `CASE WHEN x = v1 …`. Pour des conditions
arbitraires (comparaisons, `BETWEEN`, `LIKE`), seule la forme de recherche convient.

### 5.3 `CASE` pour étiqueter des tranches — la segmentation numérique

La question classique : « combien de ventes petites, moyennes, grosses ? » On découpe
`montant_ttc` en 3 tranches :

```sql
SELECT CASE
         WHEN montant_ttc < 50000   THEN 'a) moins de 50 000'
         WHEN montant_ttc < 200000  THEN 'b) 50 000 à 199 999'
         ELSE 'c) 200 000 et plus'
       END AS tranche,
       COUNT(*) AS nb_ventes,
       ROUND(MIN(montant_ttc)) AS min_m,
       ROUND(MAX(montant_ttc)) AS max_m
FROM vente
GROUP BY 1
ORDER BY tranche;
```

| tranche                 | nb_ventes | min_m  | max_m   |
|-------------------------|-----------|--------|---------|
| a) moins de 50 000      | 12 753    | 763    | 49 964  |
| b) 50 000 à 199 999     | 21 509    | 50 008 | 199 920 |
| c) 200 000 et plus      | 15 746    | 200 017| 594 363 |

Trois segments, disjoints, qui se recouvrent totalement (12 753 + 21 509 + 15 746 =
50 008). C'est le contrôle de toute segmentation : **la somme des segments redonne le
total**. Remarquez l'astuce de la 2ᵉ branche : `montant_ttc < 200000` suffit car la 1ʳᵉ
a déjà attrapé `< 50000` — les branches précédentes étant passées, on est sûr d'être au-
dessus de 50 000.

> **À retenir.** Dans un `CASE` d'intervalle, **on n'écrit que la borne haute** de chaque
> branche (`< 50000`, puis `< 200000`, sinon) : la borne basse est implicitement couverte
> par la branche précédente. C'est ce qui rend les tranches **disjointes** sans écrire
> `BETWEEN 50000 AND 199999` — et c'est ce qu'il faut vérifier en relecture.

> **Définition.** Une **tranche** — *bucket* — est un intervalle de valeurs découpé par
> des `CASE WHEN` successifs (ici `< 50 000`, `< 200 000`, sinon). Les tranches sont
> **disjointes** (une ligne n'en vaut qu'une) et **exhaustives** (avec un `ELSE`, toute
> ligne est classée). La segmentation en tranches est la base des histogrammes et des
> « classements par taille ».

### 5.4 `CASE` combiné à `GROUP BY` — agréger sur les étiquettes

L'étiquette se réutilise dans le `GROUP BY` (via sa position, C03) ou en répétant
l'expression. Le CA par segment de client :

```sql
SELECT CASE
         WHEN c.type_client = 'particulier' THEN 'Particulier'
         WHEN c.type_client = 'entreprise'  THEN 'Entreprise'
         ELSE 'Comptoir'
       END AS segment,
       COUNT(*) AS nb_ventes,
       ROUND(AVG(v.montant_ttc)) AS panier_moyen,
       ROUND(SUM(v.montant_ttc)) AS ca
FROM vente v
JOIN client c ON c.id_client = v.id_client
GROUP BY 1
ORDER BY ca DESC;
```

| segment     | nb_ventes | panier_moyen | ca           |
|-------------|-----------|--------------|--------------|
| Particulier | 35 377    | 158 181      | 5 595 962 715|
| Entreprise  | 9 471     | 156 542      | 1 482 606 616|
| Comptoir    | 5 160     | 160 793      | 829 690 400  |

Le panier moyen des **comptoirs** (160 793 FCFA) est le plus élevé — ils achètent moins
(5 160 ventes) mais plus gros. Le total des 3 `ca` redonne 7 908 259 731 FCFA (contrôle
de cohérence de C05).

### 5.5 `COALESCE` — le premier non nulle

`COALESCE(a, b, c, …)` renvoie la **première** valeur de la liste qui n'est pas `NULL`.
C'est l'outil de **repli** :

```sql
-- Si plafond_credit est absent, afficher 0 (au lieu de NULL)
SELECT id_client, nom,
       COALESCE(plafond_credit, 0) AS plafond_sur
FROM client
ORDER BY id_client
LIMIT 3;
```

Sur le socle M07, `plafond_credit` n'a aucun `NULL` : `COALESCE(plafond_credit, 0)`
renvoie donc toujours `plafond_credit`. Mais la démonstration est valide — et c'est le
geste standard dès qu'une colonne réelle contient des absences.

Cas d'usage n° 2 : un **libellé de repli** dans un rapport :

```sql
SELECT nom,
       COALESCE(ville, '(non renseignée)') AS ville_affichee
FROM client
ORDER BY nom
LIMIT 3;
```

Un client sans ville n'affichera pas une case vide mais « (non renseignée) » — le rapport
reste lisible.

> **Définition.** La fonction **`COALESCE`** — *coalescer* — renvoie la **première**
> valeur de sa liste d'arguments qui n'est pas `NULL`. `COALESCE(x, défaut)` est le
> substitut portable de l'opérateur `??` (MySQL) et de `x IS NOT NULL THEN x` (un `CASE`)
> : elle transforme une absence en valeur de repli. Elle ne regarde que les `NULL` — un
> zéro ou un texte vide sont des valeurs présentes, pas des absences.

> **Attention.** `COALESCE` ne remplace **pas les zéros** et **pas les textes vides** :
> `COALESCE(0, 1)` renvoie 0, `COALESCE('', 'défaut')` renvoie `''` (le tiret médian est
> une valeur, pas un `NULL`). Pour « 0 ou vide ⇒ défaut », il faut un `CASE` explicite.

### 5.6 `NULLIF` — produire du `NULL` volontairement

`NULLIF(a, b)` renvoie `NULL` **si `a = b`**, sinon `a`. C'est le miroir de `COALESCE` :
là où `COALESCE` transforme un `NULL` en valeur, `NULLIF` transforme une valeur en `NULL`.

Usage n° 1 : **filtrer les zéros d'une somme** sans `WHERE` :

```sql
-- La marge d'un produit à prix nul : NULL au lieu de 0 (signal d'absence)
SELECT NULLIF(0, 0)        AS zero_devenu_null,
       NULLIF(5, 0)        AS cinq_garde_cinq,
       NULLIF('a', 'a')    AS egal_devenu_null;
```

→ `NULL`, `5`, `NULL`. Les deux égalités produisent du `NULL`, l'inégalité garde la valeur.

Usage n° 2 : **combinaison `COALESCE` + `NULLIF`** pour « vider les zéros puis mettre un
repli » (mêmes types des deux côtés du `COALESCE` — ici des textes) :

```sql
SELECT COALESCE(NULLIF('0', '0'), 'aucun')  AS zero_vide_puis_repli,
       COALESCE(NULLIF('5', '0'), 'aucun')  AS cinq_garde_cinq;
```

→ « aucun » (le « 0 » devient `NULL`, le `COALESCE` met le repli) / « 5 ». Sur des
nombres, le repli doit être un nombre : `COALESCE(NULLIF(0, 0), -1)`.

> **Définition.** La fonction **`NULLIF`** — *nullifier si égal* — renvoie `NULL` quand
> ses deux arguments sont égaux, sinon le premier argument. `NULLIF(a, 0)` est le filtre
> de zéros portable : il transforme un zéro (valeur « pas de donnée ») en `NULL` (absence),
> ce qui permet ensuite à `COALESCE` de poser un repli. C'est le miroir exact de
> `COALESCE` : l'un sort des `NULL`, l'autre y entre.

### 5.7 Le `CASE` dans le `WHERE` — filtrer sur une étiquette

On ne peut pas filtrer sur une étiquette du `SELECT` (elle n'existe pas encore au moment
du `WHERE`) : on **recalcule** la condition, ou on encapsule dans une vue / CTE (C08).
Ici, la recalcul direct :

```sql
SELECT COUNT(*) AS nb_ventes_grosses
FROM vente
WHERE montant_ttc >= 200000;
```

→ 15 746 ventes (la tranche c). Le `WHERE` ne voit que des expressions sur les colonnes
réelles ; l'étiquette du `SELECT` est calculée **après** (ordre d'exécution C01).

### 5.8 Ce que ce chapitre ne couvre pas

- Les **fonctions de texte** (`UPPER`, `LOWER`, `TRIM`, `SUBSTR`, `LIKE`) : M11.
- Les **vues** et **CTE** pour encapsuler une étiquette réutilisable : C08.
- L'optimisation des `CASE` imbriqués et des fonctions scalaires : M11.

## 6. Exemple concret — la requête qui répond à une question métier

La responsable fidélité demande : *« Combien de ventes par type de client, et quel est le
CA de chaque type ? Et si un type avait un libellé vide, que faudrait-il afficher ? »*

**Étape 1 — Écrire la requête** (segmentation + `COALESCE` de repli).

```sql
SELECT COALESCE(CASE c.type_client
                   WHEN 'particulier' THEN 'Particulier'
                   WHEN 'entreprise'  THEN 'Entreprise'
                   WHEN 'comptoir'    THEN 'Comptoir'
                   ELSE 'Autre'
                 END, '(inconnu)') AS segment,
       COUNT(*) AS nb_ventes,
       ROUND(SUM(v.montant_ttc)) AS ca
FROM vente v
JOIN client c ON c.id_client = v.id_client
GROUP BY 1
ORDER BY ca DESC;
```

**Étape 2 — Prédire la sortie.** 3 segments (les 3 types du socle) ; le `COALESCE` de
repli ne s'activera que si un `type_client` serait `NULL` (aucun ici). Particulier en
tête (le plus de ventes).

**Étape 3 — Exécuter.** Particulier 35 377 ventes / 5 595 962 715 FCFA ; Entreprise 9 471 /
1 482 606 616 ; Comptoir 5 160 / 829 690 400.

**Étape 4 — Comparer.** 3 segments, aucun « (inconnu) » (pas de `NULL` dans le socle),
total 7 908 259 731 FCFA. Le `COALESCE` est un filet de sécurité, pas un acteur ici.

> **Conseil professionnel.** Dans une requête de production, **toute étiquette `CASE` qui
> peut tomber dans le vide doit avoir un `ELSE`**, et ce `ELSE` doit être un libellé
> explicite (« (inconnu) », « (non classé) ») plutôt qu'un `NULL` : un `NULL` dans une
> colonne de segment disparaît des `GROUP BY` lisibles et des tableaux de bord. Le
> `COALESCE` autour du `CASE` est le filet de dernier recours.

## 7. Démonstration pas à pas — 6 requêtes sur le fil rouge

### 7.1 Question 1 — Les 3 types de clients

```sql
SELECT type_client, COUNT(*) AS nb_clients
FROM client
GROUP BY type_client
ORDER BY nb_clients DESC;
```

→ particulier 850, entreprise 229, comptoir 121.

### 7.2 Question 2 — Le CA par type de client

```sql
SELECT c.type_client,
       COUNT(*) AS nb_ventes,
       ROUND(SUM(v.montant_ttc)) AS ca
FROM vente v
JOIN client c ON c.id_client = v.id_client
GROUP BY c.type_client
ORDER BY ca DESC;
```

→ particulier 5 595 962 715 FCFA, entreprise 1 482 606 616, comptoir 829 690 400.

### 7.3 Question 3 — Les 3 villes et leur CA

```sql
SELECT c.ville,
       COUNT(*) AS nb_ventes,
       ROUND(SUM(v.montant_ttc)) AS ca
FROM vente v
JOIN client c ON c.id_client = v.id_client
GROUP BY c.ville
ORDER BY ca DESC;
```

→ Ouagadougou 21 290 ventes / 3 391 679 290 FCFA, Bobo-Dioulasso 18 364 / 2 895 549 769,
Koudougou 10 354 / 1 621 030 672.

### 7.4 Question 4 — La segmentation en 3 tranches

```sql
SELECT CASE
         WHEN montant_ttc < 50000  THEN 'a) moins de 50 000'
         WHEN montant_ttc < 200000 THEN 'b) 50 000 à 199 999'
         ELSE 'c) 200 000 et plus'
       END AS tranche,
       COUNT(*) AS nb_ventes
FROM vente
GROUP BY 1
ORDER BY tranche;
```

→ 12 753 / 21 509 / 15 746 (total 50 008).

### 7.5 Question 5 — Les ventes des comptoirs, par ville

```sql
SELECT c.ville, COUNT(*) AS nb_ventes
FROM vente v
JOIN client c ON c.id_client = v.id_client
WHERE c.type_client = 'comptoir'
GROUP BY c.ville
ORDER BY nb_ventes DESC;
```

→ Ouagadougou 2 621, Bobo-Dioulasso 1 534, Koudougou 1 005.

### 7.6 Question 6 — Le CA des produits inactifs (piège silencieux)

```sql
SELECT COUNT(*) AS nb_ventes,
       ROUND(SUM(v.montant_ttc)) AS ca
FROM vente v
JOIN produit p ON p.id_produit = v.id_produit
WHERE p.actif = FALSE;
```

→ 2 434 ventes, 471 206 245 FCFA. Les 18 produits **inactifs** ont tout de même généré
cette CA (sur l'historique 2025–2026) : « inactif » signifie « plus proposé », pas «
jamais vendu ». C'est le piège d'interprétation classique d'une colonne de statut.

## 8. Erreurs fréquentes

| # | Erreur | Symptôme | Correction |
|---|--------|----------|------------|
| 1 | Oublier le `ELSE` dans un `CASE` | lignes non couvertes = `NULL` dans l'étiquette | toujours un `ELSE` explicite. |
| 2 | Branche `WHEN` trop générale en 1ʳᵉ position | branches suivantes jamais atteintes (mortes) | conditions de la plus spécifique à la plus générale. |
| 3 | Filtrer sur une étiquette dans le `WHERE` | erreur ou résultat inattendu | recalculer la condition, ou vue/CTE (C08). |
| 4 | Attendre que `COALESCE` remplace un 0 | le 0 passe tel quel | `COALESCE(NULLIF(x, 0), défaut)` pour vider les zéros. |
| 5 | Confondre `CASE x WHEN v` (simple) et `CASE WHEN c` (recherche) | syntaxe erronée | simple = comparaison d'une valeur ; recherche = conditions arbitraires. |
| 6 | Croire que « inactif » = « jamais vendu » | sous-estimer l'historique d'un statut | vérifier le CA réel par statut (cf. 7.6). |

> **Attention.** L'erreur 2 est la plus subtile : un `CASE` où la branche la plus
> générale est en premier **rend les autres branches mortes** sans erreur. Sur des
> intervalles, toujours du plus étroit au plus large, ou utiliser des bornes fermées
> explicites (`BETWEEN`).

> **Attention.** Un `NULL` dans un `CASE` : `WHEN NULL = 'x'` est **`NULL`** (ni vrai ni
> faux), donc la branche ne passe pas. Pour tester l'absence, écrire `WHEN x IS NULL THEN`
> — jamais `WHEN x = NULL`.

## 9. Bonnes pratiques professionnelles

- **Toujours un `ELSE`** dans un `CASE` de segmentation, avec un libellé explicite.
- **L'ordre des `WHEN`** : du plus spécifique au plus général (surtout sur des intervalles).
- **Contrôler la segmentation** : la somme des segments redonne le total (ici 50 008).
- **`COALESCE` sur toute colonne affichée** qui peut être absente en production.
- **Documenter le statut** : « actif / inactif » doit être défini (plus proposé vs jamais
  vendu) — sinon les rapports mentent par omission.
- **Préférer une vue/CTE** (C08) quand l'étiquette `CASE` est réutilisée plusieurs fois.

## 10. Exercice guidé — le rapport de segmentation (15 min, /10)

**Énoncé.** Produire, par type de client (3 lignes, triées par CA décroissant) : le
segment (étiquette lisible), le nombre de ventes, le panier moyen arrondi, le CA arrondi.
Ajouter un `COALESCE` de repli « (inconnu) » autour du `CASE`.

**Grille de correction (/10).**

| Critère | Points |
|---|---|
| `CASE` 3 branches + `ELSE` | 2 |
| `COALESCE(…, '(inconnu)')` | 1 |
| `COUNT(*)`, `ROUND(AVG(…))`, `ROUND(SUM(…))` | 2 |
| `JOIN client` + `GROUP BY 1` | 2 |
| `ORDER BY ca DESC` | 1 |
| 3 lignes, Particulier en tête (5 595 962 715) | 2 |

**Corrigé.** Cf. §6, étape 1. → Particulier 35 377 / 158 181 / 5 595 962 715 ; Entreprise
9 471 / 156 542 / 1 482 606 616 ; Comptoir 5 160 / 160 793 / 829 690 400.

## 11. Exercices autonomes

### Exercice 1 — Les 3 types de clients

Compter les clients par `type_client`, trié décroissant.

### Exercice 2 — Le CA par ville

Une ligne par ville : nombre de ventes, CA arrondi, trié par CA décroissant.

### Exercice 3 — La segmentation en tranches

Les 3 tranches de montant (< 50 000 / 50 000–199 999 / ≥ 200 000) avec leur nombre de
ventes. Vérifier que le total redonne 50 008.

### Exercice 4 — `NULLIF` en solo

Quel est le résultat de `SELECT NULLIF(7, 7), NULLIF(7, 8), NULLIF('x', 'x');` ?

### Exercice 5 — `COALESCE` + `NULLIF`

Réécrire « si `plafond_credit` vaut 0 ou est `NULL`, afficher 500 000 ; sinon le
`plafond_credit` » avec `COALESCE` et `NULLIF`.

### Exercice 6 — Comptoirs par ville

Les ventes des comptoirs, une ligne par ville, triées décroissant.

### Exercice 7 — Le CA des produits inactifs

Nombre de ventes et CA des produits `actif = FALSE`.

### Exercice 8 — Diagnostic d'erreur

Pourquoi cette requête est-elle une erreur, et comment la corriger ?

```sql
SELECT segment, COUNT(*)
FROM (
  SELECT CASE
           WHEN type_client = 'particulier' THEN 'Particulier'
           WHEN type_client = 'entreprise'  THEN 'Entreprise'
           ELSE 'Comptoir'
         END AS segment
  FROM client
) t
GROUP BY segment;
```

## 12. Correction détaillée

**Exercice 1.**

```sql
SELECT type_client, COUNT(*) AS nb_clients
FROM client
GROUP BY type_client
ORDER BY nb_clients DESC;
```

→ particulier 850, entreprise 229, comptoir 121.

**Exercice 2.** Cf. §7.3 → Ouagadougou 21 290 / 3 391 679 290 ; Bobo-Dioulasso 18 364 /
2 895 549 769 ; Koudougou 10 354 / 1 621 030 672 FCFA.

**Exercice 3.** Cf. §7.4 → 12 753 / 21 509 / 15 746 ; total 50 008 ✓.

**Exercice 4.** `NULL`, `7`, `NULL` : les deux égalités (7=7, 'x'='x') produisent du
`NULL` ; l'inégalité (7≠8) garde 7.

**Exercice 5.**

```sql
SELECT COALESCE(NULLIF(plafond_credit, 0), 500000) AS plafond_final
FROM client
ORDER BY id_client
LIMIT 3;
```

`NULLIF(plafond_credit, 0)` transforme le 0 en `NULL` ; `COALESCE(…, 500000)` met le
repli pour les `NULL` (et les 0). Sur le socle, aucun plafond n'est 0 ni `NULL` : le
`plafond_final` vaut toujours le `plafond_credit`.

**Exercice 6.** Cf. §7.5 → Ouagadougou 2 621, Bobo-Dioulasso 1 534, Koudougou 1 005.

**Exercice 7.** Cf. §7.6 → 2 434 ventes, 471 206 245 FCFA.

**Exercice 8.** Cette requête est en fait **correcte** (une sous-requête nommée `t` qui
produit `segment`, puis un `GROUP BY segment` valide) — le piège est de chercher l'erreur
alors qu'il n'y en a pas. Le cas qui **serait** une erreur, c'est de vouloir
`GROUP BY segment` **sans** la sous-requête (l'alias du `SELECT` n'est pas groupable
telle quelle dans tous les SGBD). La bonne pratique : encapsuler l'étiquette (sous-requête
ici, vue ou CTE en C08) avant de la regrouper.

## 13. Mini-projet — « La grille de segmentation complète » (40 min)

Produire la **grille de segmentation** de la base : 4 requêtes, chacune vérifiée à la main.

| Requête | Lignes attendues |
|---|---|
| G1 : segment par type de client (nb, panier moyen, CA) | 3 |
| G2 : tranche de montant (nb, min, max) | 3 |
| G3 : CA par ville (nb, CA) | 3 |
| G4 : statut produit (actif/inactif) : nb de produits, nb de ventes, CA | 2 |

**Contrôles de cohérence.** (i) La somme des `nb_ventes` de G2 = 50 008. (ii) La somme des
`ca` de G1 = 7 908 259 731 FCFA. (iii) G4 : actif 362 produits, inactif 18 ; le CA
inactif = 471 206 245 FCFA.

**Corrigé.**

```sql
-- G1
SELECT COALESCE(CASE c.type_client
                   WHEN 'particulier' THEN 'Particulier'
                   WHEN 'entreprise'  THEN 'Entreprise'
                   WHEN 'comptoir'    THEN 'Comptoir'
                   ELSE 'Autre'
                 END, '(inconnu)') AS segment,
       COUNT(*) AS nb,
       ROUND(AVG(v.montant_ttc)) AS panier_moyen,
       ROUND(SUM(v.montant_ttc)) AS ca
FROM vente v JOIN client c ON c.id_client = v.id_client
GROUP BY 1
ORDER BY ca DESC;

-- G2
SELECT CASE
         WHEN montant_ttc < 50000  THEN 'a) moins de 50 000'
         WHEN montant_ttc < 200000 THEN 'b) 50 000 à 199 999'
         ELSE 'c) 200 000 et plus'
       END AS tranche,
       COUNT(*) AS nb,
       ROUND(MIN(montant_ttc)) AS min_m,
       ROUND(MAX(montant_ttc)) AS max_m
FROM vente
GROUP BY 1
ORDER BY tranche;

-- G3
SELECT c.ville, COUNT(*) AS nb, ROUND(SUM(v.montant_ttc)) AS ca
FROM vente v JOIN client c ON c.id_client = v.id_client
GROUP BY c.ville
ORDER BY ca DESC;

-- G4
SELECT p.actif,
       COUNT(DISTINCT p.id_produit) AS nb_produits,
       COUNT(*) AS nb_ventes,
       ROUND(SUM(v.montant_ttc)) AS ca
FROM vente v JOIN produit p ON p.id_produit = v.id_produit
GROUP BY p.actif
ORDER BY p.actif DESC;
```

> **Dans les faits.** PostgreSQL et SQLite partagent cette syntaxe `CASE` / `COALESCE` /
> `NULLIF` (elles sont **standard SQL**) : la grille s'exécute telle quelle sur les deux.
> MySQL aussi, mais son opérateur `??` (équivalent `COALESCE` à 2 arguments) est un
> ajout non standard : pour la portabilité, écrire `COALESCE`.

## 14. Boîte à outils du chapitre

> **Boîte à outils.** Ce chapitre installe 3 outils de transformation : `CASE` (la brique
> de segmentation, formes simple et recherche), `COALESCE` (le repli des `NULL`),
> `NULLIF` (le producteur de `NULL`). Ensemble, ils couvrent la quasi-totalité du travail
> de « création de colonnes d'étiquette » d'un entrepôt. Le `ELSE` obligatoire et le
> contrôle « somme des segments = total » sont les deux réflexes.

| Outil | Usage | Syntaxe | Piège |
|---|---|---|---|
| `CASE WHEN … END` | étiquette par condition | `CASE WHEN x < 50000 THEN 'petit' ELSE 'grand' END` | `ELSE` oublié, branches mortes |
| `CASE x WHEN v END` | étiquette par valeur | `CASE type WHEN 'pro' THEN 'Pro' END` | le confondre avec la forme recherche |
| `COALESCE` | repli des `NULL` | `COALESCE(ville, '(non renseignée)')` | ne remplace pas 0 / vide |
| `NULLIF` | produire du `NULL` | `NULLIF(plafond, 0)` | le retourner (c'est `COALESCE`) |
| `COALESCE(NULLIF(…))` | vider les zéros puis repli | `COALESCE(NULLIF(x,0), 0)` | l'oublier sur une somme |
| Contrôle | cohérence | somme des segments = total | ne pas vérifier le total |

## 15. Résumé du chapitre

- **`CASE`** est la brique de segmentation : forme de recherche (conditions arbitraires)
  et forme simple (comparaison d'une valeur). Les `WHEN` sont testés **dans l'ordre**, la
  1ʳᵉ qui passe gagne ; **toujours un `ELSE`**.
- **Segmenter** = découper en tranches disjointes et exhaustives ; le contrôle : la somme
  des segments redonne le total (50 008).
- **`COALESCE(a, b, …)`** = la première valeur non `NULL` : le repli des absences. Il ne
  regarde que les `NULL` (pas les 0, pas les vides).
- **`NULLIF(a, b)`** = `NULL` si `a = b`, sinon `a` : le producteur de `NULL` (le miroir
  de `COALESCE`). `COALESCE(NULLIF(x, 0), défaut)` vide les zéros puis met le repli.
- **Filtrer sur une étiquette** : on recalcule la condition dans le `WHERE`, ou on
  encapsule l'étiquette (sous-requête, vue, CTE — C08).
- **Interpréter les statuts** : « inactif » ≠ « jamais vendu » (ici 471 206 245 FCFA de
  CA sur 18 produits inactifs).

## 16. À retenir

- **`CASE` : toujours un `ELSE`**, ordre des `WHEN` du spécifique au général.
- **Segmentation** : tranches disjointes + exhaustives ; somme des segments = total.
- **`COALESCE` = repli des `NULL`** (pas des 0 / vides) ; **`NULLIF` = producteur de
  `NULL`**.
- **`COALESCE(NULLIF(x, 0), défaut)`** : le duo pour vider les zéros puis replier.
- **Statut ≠ historique** : vérifier le CA réel par statut avant d'interpréter.

> **À retenir.** `CASE`, `COALESCE`, `NULLIF` sont **standard SQL** : elles s'écrivent à
> l'identique sur DuckDB, PostgreSQL et SQLite. C'est l'un des rares pans du langage où la
> portabilité est totale — à condition de ne pas employer les raccourcis non standard
> (`??`, `IFNULL` MySQL, `DECODE` Oracle).

## 17. Évaluation formative (auto-correction, 8 min)

Sans document, en 8 minutes, répondre aux 5 questions. Auto-correction en bas.

1. À quoi sert le `ELSE` dans un `CASE`, et que se passe-t-il s'il est absent ?
2. Quelle est la différence entre `CASE x WHEN v1 …` et `CASE WHEN c1 …` ?
3. Que renvoie `COALESCE(NULL, 0, 'x')` ? Et `COALESCE(0, 'x')` ?
4. Que renvoie `NULLIF(5, 5)` ? Et `NULLIF(5, 0)` ?
5. Pourquoi « inactif » ne veut-il pas dire « jamais vendu » ?

**Réponses** :

1. Le `ELSE` est la valeur de repli si aucune condition ne passe. S'il est absent, les
   lignes non couvertes renvoient `NULL` — des segments invisibles dans les rapports.
2. `CASE x WHEN v1 …` compare **une valeur `x`** à des constantes (`x = v1`, `x = v2`…) —
   c'est un sucre. `CASE WHEN c1 …` teste des **conditions arbitraires** (comparaisons,
   `BETWEEN`, `LIKE`). Pour un intervalle, seule la forme de recherche convient.
3. `COALESCE(NULL, 0, 'x')` → `0` (la 1ʳᵉ non nulle). `COALESCE(0, 'x')` → `0` (le 0 est
   une valeur, pas un `NULL`, donc il est retenu).
4. `NULLIF(5, 5)` → `NULL` (égalité). `NULLIF(5, 0)` → `5` (inégalité, on garde le 1ᵉʳ
   argument).
5. Parce que le statut « inactif » décrit l'état **actuel** du produit (plus proposé),
   pas son historique : ici, les 18 produits inactifs ont généré 2 434 ventes pour
   471 206 245 FCFA sur 2025–2026. Un statut ne résume pas le passé.
