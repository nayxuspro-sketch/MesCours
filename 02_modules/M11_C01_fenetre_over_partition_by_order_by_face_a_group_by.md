# Module M11.C01 — La fonction de fenêtre : `OVER`, `PARTITION BY`, `ORDER BY`, et pourquoi `GROUP BY` ne suffit plus

**Outils : DuckDB 1.5.5 (exécuté), SQLite (contrôle croisé, exécuté), PostgreSQL et SQL Server (cités, non exécutés — règle §1.5).
Durée indicative : 5 h. Niveau : N3 → N4. Prérequis : M07 (tout : `SELECT`, agrégats, `GROUP BY`, jointures, sous-requêtes) ;
M06.C04 (DuckDB, SQLite, PostgreSQL) ; M02 (moyenne, médiane, dispersion).**

> **L'idée du chapitre.** M07 a appris à **réduire** : `GROUP BY` transforme des milliers de lignes en quelques
> totaux. C'est exactement ce qu'il faut quand la question est « combien ». Mais la question d'un responsable
> est presque toujours « **par rapport à quoi** » — quelle part du total, quel écart à la moyenne, où se situe
> cette ligne dans son groupe. Et là, `GROUP BY` a un défaut rédhibitoire : il **supprime la ligne** dont on
> parle. La fonction de fenêtre fait l'inverse : elle calcule le contexte **et laisse la ligne en place**. Ce
> chapitre pose le mécanisme (`OVER`, `PARTITION BY`, `ORDER BY`, cadre de fenêtre) et surtout la question
> préalable à toute requête de BI — **comparer à quoi ?** — avec un contre-exemple mesuré qui coûte cher :
> oublier `PARTITION BY` ne provoque aucune erreur, et divise la réponse par cinq.

> **Matériel de l'atelier — DuckDB 1.5.5 · Python 3.13 · socle M11 (`03_exercices/dossier_M11/socle_m11.sql`).**
> Le socle est un **script** de 3 595 octets : 5 petites tables (produits, magasins, vendeurs, objectifs,
> calendrier) et 2 vues sur les fichiers du socle M01-M03. Il se rejoue en mémoire en **0,4 s** et ne crée
> **aucune donnée nouvelle** : c'est le même fichier de ventes que M01 à M03 — **240 000** lignes,
> **237 191** ventes nettes (**2 809** retours), **44** mois, **5** magasins, **23 497** clients,
> **15 595 154 955** FCFA de chiffre d'affaires net. Toutes les sorties publiées dans ce chapitre sont
> celles de l'atelier, exécutées le 24/09/2026.

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous savez :

1. **Expliquer la différence d'usage** entre un agrégat (`GROUP BY`) et une **fonction de fenêtre**
   (*window function*) : l'un réduit la table, l'autre ajoute une colonne — et dire laquelle des deux
   répond à « quelle part du total ? ».
2. **Écrire et lire une fenêtre** : `OVER ()`, `PARTITION BY`, `ORDER BY` à l'intérieur de la fenêtre,
   et un **cadre de fenêtre** (`ROWS BETWEEN … AND …`).
3. **Déterminer la base de comparaison** d'un chiffre — par magasin, par année, sur toute la table — et
   **prouver** votre choix en montrant que les parts somment à 100 % au niveau où elles doivent sommer.
4. **Reconnaître les trois pièges du chapitre** sur un résultat réel : la fenêtre évaluée après le `WHERE`,
   la jointure sur une clé incomplète, et la partition qui vaut le groupe (qui affiche toujours 100 %).
5. **Choisir entre une fenêtre et une sous-requête scalaire** pour ramener un « contexte » dans une requête
   agrégée, et justifier le choix autrement que par le goût.

## 2. Pourquoi cette notion est importante

Un responsable de magasin ne demande pas « quel est le chiffre d'affaires de la société ? ». Il demande
**« quelle est ma part ? »**. Un responsable de rayon demande **« ce mois est-il bon ? »**, ce qui suppose
un mois moyen à côté. Un directeur commercial demande **« qui sont mes dix meilleurs vendeurs ? »**, ce qui
suppose un classement **dans** un groupe. Ces trois questions ont un point commun : elles comparent une
**ligne** à un **ensemble de lignes**. C'est le métier de la fenêtre.

Le socle du module rend l'enjeu immédiatement visible. Prenez les **5** magasins : un simple `GROUP BY`
donne leurs totaux, et rien de plus. Pour obtenir leur **part**, il faut le total général — et le réflexe de
M07 est d'écrire une sous-requête scalaire qui le ramène :

```sql
SELECT m.nom, SUM(v.montant_ttc) AS ca,
       ROUND(100.0 * SUM(v.montant_ttc)
             / (SELECT SUM(montant_ttc) FROM ventes WHERE NOT est_retour), 2) AS part_pct
FROM ventes v JOIN magasin m USING (id_magasin)
WHERE NOT v.est_retour GROUP BY 1 ORDER BY ca DESC;
```

Cette requête est **juste**, et c'est celle que M07 vous aurait fait écrire. Elle a deux défauts, tous les
deux mesurables : elle réclame **le total de la table** à chaque fois qu'on veut un pourcentage (ici une
seconde lecture complète des 237 191 lignes), et elle devient illisible dès qu'on veut **deux** contextes
— la part de la société *et* la part du magasin dans son propre réseau. Le même résultat s'écrit avec une
fenêtre, et l'atelier a chronométré les deux écritures : **150 ms** pour la fenêtre, **292 ms** pour la
sous-requête scalaire, soit **×1,9** pour la même sortie, ligne pour ligne.

Mais la vraie raison d'apprendre la fenêtre n'est pas la vitesse — les deux requêtes donnent exactement le
même tableau. C'est que la fenêtre rend **visible** la question « comparer à quoi ? », parce qu'on doit
l'écrire noir sur blanc : `OVER ()` dit *toute la table*, `OVER (PARTITION BY id_magasin)` dit *dans son
magasin*, `OVER (PARTITION BY annee)` dit *dans son année*. La sous-requête scalaire cache ce choix dans
une sous-requête qu'on ne relit pas. Et un choix caché, en BI, c'est un chiffre faux qui a l'air juste.

**Le chiffre qui ouvre ce chapitre.** Sur ce socle, le plus gros client identifié de la base n'est pas un
client : c'est un identifiant **0** qui totalise **2 852 612 447** FCFA et **18,3 %** du chiffre d'affaires
net du réseau — tout en étant **absent** du référentiel clients. Celui qui écrit une fenêtre de classement
sans le savoir met en tête de son rapport commercial un client « non identifié » : la fenêtre ne protège de
rien, elle exécute ce qu'on lui demande. C'est la leçon que le module déroulera jusqu'à l'étude de cas.

## 3. Explication simple — le tableau d'affichage du stade

Imaginez un match. Chaque spectateur (une ligne de la table) a un numéro de place, un prix payé, une tribune.
À un moment, l'écran géant affiche trois informations : **le total du stade**, **le total de votre tribune**,
**le nombre de spectateurs de votre tribune**.

- `GROUP BY`, c'est la **feuille de caisse** : on plie la foule en quelques tas, et les individus
  disparaissent. On sait qu'il y a 5 tas, on ne sait plus qui est dans lequel.
- La **fenêtre**, c'est l'**écran du stade** : chaque spectateur reste assis à sa place et **voit** l'information
  de son groupe. Le nombre de places ne change pas : 237 191 personnes restent 237 191 personnes, on a
  simplement ajouté trois colonnes à leur billet.

Trois conséquences, qui sont tout le chapitre :

1. **Le nombre de lignes ne change pas.** Si votre requête avec fenêtre rend 5 lignes là où vous attendiez
   237 191, vous avez écrit un `GROUP BY`, pas une fenêtre.
2. **Ce que voit chaque ligne dépend de la fenêtre.** `OVER ()` = tout le stade ; `OVER (PARTITION BY
   tribune)` = votre tribune. Changez la fenêtre, changez le chiffre — sans changer une seule donnée.
3. **L'ordre compte dès qu'on demande un cumul.** Un cumul (« total depuis l'ouverture ») n'existe que
   **dans un ordre** : il faut dire lequel (`ORDER BY`), sinon le moteur choisit, et vous ne saurez pas quoi.

## 4. Vocabulaire essentiel

| Terme (français) | Équivalent anglais | Définition en une phrase |
|---|---|---|
| **fonction de fenêtre** | *window function* | Un calcul qui regarde un ensemble de lignes liées à la ligne courante **sans réduire** le nombre de lignes du résultat. |
| **fenêtre** | *window* | L'ensemble de lignes que la fonction voit : décrit par `OVER (…)`. |
| **partition** | *partition* | La découpe de la fenêtre en groupes indépendants (`PARTITION BY id_magasin`) : le **facteur de comparaison**. |
| **ordre de fenêtre** | *window order* | L'ordre à l'intérieur de la partition (`ORDER BY date_vente`) : il rend possibles cumuls, rangs et décalages. |
| **cadre de fenêtre** | *window frame* | Les lignes effectivement prises en compte autour de la ligne courante (`ROWS BETWEEN 2 PRECEDING AND CURRENT ROW`). |
| **part relative** | *share of total* | Le rapport d'une ligne au total de sa fenêtre ; la somme des parts vaut 100 % **au niveau de la partition**. |
| **sous-requête scalaire** | *scalar subquery* | Une sous-requête qui rend **une seule valeur**, utilisée comme un nombre dans une expression — l'ancêtre de la fenêtre. |
| **ordre d'exécution** | *logical order of execution* | L'ordre dans lequel le moteur interprète les clauses (`FROM` → `WHERE` → `GROUP BY` → *fenêtres* → `SELECT` → `ORDER BY`). |
| **grain** | *grain* | Ce que représente une ligne du résultat : le vérifier avant de joindre, de fenêtrer et de conclure. |
| **total de contrôle** | *control total* | Le chiffre qu'un rapport doit retrouver coûte que coûte (ici **15 595 154 955** FCFA) et qui démasque toute multiplication de lignes. |

> **Définition.** Une **fonction de fenêtre** — *window function* — est un calcul qui prend en entrée un
> **ensemble de lignes** (la fenêtre) et rend **une valeur par ligne**. Elle s'écrit toujours après un
> nom de fonction, avec le mot-clé `OVER` : `SUM(x) OVER (…)`, `AVG(x) OVER (…)`, `COUNT(*) OVER ()`. Sans
> `OVER`, la même fonction est un agrégat ordinaire et réduit la table.

> **Définition.** La **partition** — *partition* — est la subdivision de la fenêtre en groupes **indépendants
> les uns des autres**. Deux partitions ne se voient pas : un `SUM` de fenêtre partitionné par magasin ne
> connaît jamais le total de la société. C'est exactement ce qu'on veut quand la bonne question est
> « quelle part de *son* marché ? ».

## 5. Cours approfondi

### 5.1 L'ordre d'exécution : pourquoi une fenêtre n'est pas un agrégat

Le moteur lit une requête dans un ordre qui n'est pas celui de l'écriture :

```
FROM  →  WHERE  →  GROUP BY  →  HAVING  →  FENÊTRES  →  SELECT  →  DISTINCT  →  ORDER BY  →  LIMIT
```

Deux conséquences se paient comptant, et elles sont mesurées au §5.7 :

1. **Une fenêtre s'évalue après `GROUP BY`.** Dans une requête agrégée, elle ne peut donc partitionner que
   sur ce qui **existe** à cet étage : une colonne de regroupement ou une expression agrégée. Écrire
   `SUM(SUM(x)) OVER (PARTITION BY colonne_non_groupee)` fait échouer la requête — et le message d'erreur de
   DuckDB dit précisément pourquoi (voir §8, erreur n°1).
2. **Une fenêtre s'évalue après `WHERE`.** Filtrer une ligne avant de calculer une part ne laisse plus
   qu'une ligne dans la fenêtre : la part devient **100,0 %**. Mesuré au §7.5 sur janvier 2023 : **8,3 %**
   quand le filtre est appliqué **après** le calcul, **100,0 %** quand il est appliqué avant.

### 5.2 `OVER ()` : la fenêtre sur toute la table

La fenêtre vide dit « **toutes les lignes du résultat** ». C'est la forme qui ramène le total général à
côté de chaque ligne :

```sql
SELECT m.nom AS magasin,
       SUM(v.montant_ttc) AS ca,
       ROUND(100.0 * SUM(v.montant_ttc) / SUM(SUM(v.montant_ttc)) OVER (), 2) AS part_pct
FROM ventes v JOIN magasin m USING (id_magasin)
WHERE NOT v.est_retour
GROUP BY 1 ORDER BY ca DESC;
```

La double écriture `SUM(SUM(v.montant_ttc)) OVER ()` surprend la première fois : **le `SUM` intérieur est
l'agrégat du `GROUP BY`** (il fabrique le total du magasin), **le `SUM` extérieur est la fenêtre** (il
additionne ces totaux, donc toute la table). On lit la requête de l'intérieur vers l'extérieur :
regrouper par magasin, puis comparer chaque total au total des totaux.

> **Dans les faits.** L'atelier a exécuté les deux écritures sur le socle et comparé les sorties ligne à
> ligne : **identiques**. Seul le chronomètre les distingue — **150 ms** pour la fenêtre, **292 ms** pour la
> sous-requête scalaire. La fenêtre ne « calcule pas mieux » : elle évite de redemander le total à chaque
> ligne. Et elle a un avantage décisif en relecture : le total y est **visible** dans le texte de la requête.

### 5.3 `PARTITION BY` : le facteur de comparaison

`PARTITION BY` découpe la fenêtre. C'est **le** paramètre du chapitre, celui qui décide du sens du chiffre.
La même mesure, trois partitions, trois lectures :

| Ce qu'on écrit | La question à laquelle on répond | Ce que la somme des parts vaut |
|---|---|---|
| `OVER ()` | quelle part de **toute la société** ? | 100 % sur l'ensemble du résultat |
| `OVER (PARTITION BY id_magasin)` | quelle part **de son magasin** ? | 100 % **dans chaque magasin** |
| `OVER (PARTITION BY annee)` | quelle part **de son année** ? | 100 % **dans chaque année** |

Le tableau ci-dessus est aussi la **procédure de vérification** : après avoir écrit une part, on l'additionne
au niveau de sa partition. Si l'on n'obtient pas 100 %, la partition ne décrit pas ce qu'on raconte.

> **À retenir.** Dans une requête où le `GROUP BY` et le `PARTITION BY` portent sur la même colonne, la part
> vaut **toujours 100,0 %** : chaque groupe compare son total à lui-même. C'est le résultat le plus vide qui
> existe, il a l'air parfaitement crédible sur un rapport, et c'est l'erreur n°3 du §8.

### 5.4 `ORDER BY` dans la fenêtre : l'ordre change la valeur

Sans `ORDER BY`, la fenêtre est « toutes les lignes de la partition » : `SUM(…) OVER (PARTITION BY m)` donne
le total du magasin sur **chaque** ligne du magasin. Avec `ORDER BY` **dans** la fenêtre, la même fonction
devient **cumulative** : elle additionne de la première ligne jusqu'à la ligne courante. Attention, cet
`ORDER BY` **n'est pas** celui du résultat : c'est lui qui définit la progression du calcul. Une requête
peut très bien cumuler par date (`ORDER BY date_vente` dans la fenêtre) et **rendre** les lignes triées par
montant décroissant (`ORDER BY ca DESC` à la fin).

> **Définition.** Le **cadre de fenêtre** — *window frame* — précise **quelles lignes** autour de la ligne
> courante la fonction voit : `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` (les deux précédentes et la
> courante), `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` (depuis le début), `ROWS BETWEEN UNBOUNDED
> PRECEDING AND UNBOUNDED FOLLOWING` (toute la partition). Dès qu'on écrit `ORDER BY` dans une fenêtre,
> le cadre par défaut devient « du début à la ligne courante » : c'est lui qui transforme un `SUM` en cumul.

### 5.5 Le cadre : cumul et moyenne glissante

Sur les cinq premières ventes du magasin 1, l'atelier a publié le cumul et la moyenne glissante de trois
lignes. Les valeurs du cumul sont **53 690 ; 55 729 ; 76 969 ; 134 081 ; 171 605** FCFA : chaque ligne
ajoute son montant à la précédente. La moyenne glissante de trois lignes, elle, vaut **53 690 ; 27 865 ;
25 656 ; 26 797 ; 38 625** FCFA : elle ne monte pas, elle **suit** — la première ligne n'a qu'elle-même,
la deuxième en a deux, les suivantes en ont trois.

C'est toute la différence entre un indicateur de **niveau** (le cumul, qui dépend du passé entier) et un
indicateur de **tendance** (la moyenne glissante, qui oublie). Les deux se calculent avec la même fonction
`SUM`/`AVG` : seul le **cadre** change.

> **Attention.** Le cumul dépend de l'`ORDER BY` de la fenêtre, donc du **départage** entre lignes de même
> date. Le socle contient des milliers de ventes par jour : `ORDER BY date_vente` seul laisse le moteur
> choisir l'ordre des lignes d'une même journée, et le cumul de midi n'est plus celui du matin. Écrivez
> `ORDER BY date_vente, id_vente` — la clé de départage, ici l'identifiant unique de la ligne.

### 5.6 La même question, deux écritures : fenêtre contre sous-requête scalaire

> **Définition.** Une **sous-requête scalaire** — *scalar subquery* — est une sous-requête placée dans une
> expression et qui rend **une seule valeur** (une ligne, une colonne) : `SUM(x) / (SELECT SUM(y) FROM t)`.
> C'est la façon dont on écrivait un contexte avant les fenêtres. Elle reste légitime pour une constante —
> un seuil, un taux de référence — et devient illisible dès qu'il faut deux contextes différents.

| Critère | Fonction de fenêtre | Sous-requête scalaire |
|---|---|---|
| Sortie | identique | identique |
| Coût mesuré ici | **150 ms** | **292 ms** |
| Le choix de comparaison est-il visible ? | oui, dans `OVER (…)` | non, enfoui dans la sous-requête |
| Deux contextes dans la même requête ? | oui (`OVER ()` et `OVER (PARTITION BY …)`) | oui, mais deux sous-requêtes |
| S'écrit sur une requête agrégée ? | oui (`SUM(SUM(x)) OVER (…)`) | oui (`SUM(x) / (SELECT …)`) |
| S'ajoute à une table non agrégée ? | oui, directement | oui, mais une sous-requête par contexte |

La règle de travail du module : **dès qu'un chiffre exprime une comparaison, la fenêtre est la forme
attendue** — parce que la relecture doit pouvoir vérifier le facteur de comparaison sans exécuter la requête.

> **Attention.** La vitesse ne justifie pas un choix de syntaxe. Les **150 ms** contre **292 ms** de l'atelier
> dépendent de la machine, de la version du moteur et de la taille du socle : sur dix lignes, la sous-requête
> scalaire sera plus rapide. Écrivez la fenêtre parce que le **facteur de comparaison y est explicite** —
> c'est un argument de relecture, pas un argument de performance. Le seul argument de performance du module
> qui survive à un changement de machine est celui du chapitre C06, et il est mesuré sur un plan d'exécution.

### 5.7 Les trois pièges, mesurés

1. **La fenêtre s'évalue après le `WHERE`** : janvier 2023 vaut **8,3 %** de son année quand la fenêtre est
   calculée puis filtrée ; **100,0 %** quand filtre et fenêtre sont dans le même `SELECT`. Le résultat
   « 100,0 % » est faux et n'émet aucun avertissement.
2. **La jointure sur une clé incomplète** : joindre les ventes à une table de totaux **mensuels par magasin**
   en oubliant `id_magasin` dans la condition multiplie chaque ligne par le nombre de magasins du mois. Le
   rapport annonce alors **77 975 774 775** FCFA sur **1 185 955** lignes — soit cinq fois le total du socle,
   et le contrôle des 5 magasins « fonctionne » toujours.
3. **La partition qui vaut le groupe** : `GROUP BY YEAR(date_vente)` avec
   `OVER (PARTITION BY YEAR(date_vente))` affiche 100,0 % pour chaque année. La requête est valide, la
   réponse est vide.

> **Conseil professionnel.** Terminez chaque rapport de comparaison par **un total de contrôle** : un
> `SELECT SUM(montant_ttc) FROM ventes WHERE NOT est_retour` qui doit rendre **15 595 154 955** FCFA. C'est
> cinq secondes d'écriture, et c'est la seule ligne qui attrape les pièges 2 et 3 — les deux seuls du
> chapitre qui produisent un nombre **plus grand** ou **trop rond** sans jamais lever d'erreur.

### 5.8 Ce que ce chapitre ne couvre pas

Les **rangs** (`ROW_NUMBER`, `RANK`, `NTILE`), les **décalages** (`LAG`, `LEAD`) et les **variations** d'une
période à l'autre sont le sujet de C02 : ce sont les mêmes fenêtres, appliquées à l'ordonnancement. Le
traitement du **temps** (mois sans vente à fabriquer, comparaison inter-annuelle, moyennes mobiles de 12 mois)
est celui de C03. Ici, on ne fait que comparer une ligne à un ensemble — et on apprend à dire lequel.

## 6. Exemple concret — la part de chaque magasin, et ce qu'elle décide

Le directeur commercial demande le poids de chaque magasin. La requête de référence rend **5 lignes** :

| Magasin | CA net (FCFA) | Part du réseau |
|---|---|---|
| Sahel Distribution — Ouaga 2000 | 5 312 205 459 | 34,06 % |
| Sahel Distribution — Gounghin | 3 424 978 244 | 21,96 % |
| Sahel Distribution — Bobo Kibidwé | 3 099 946 956 | 19,88 % |
| Sahel Distribution — Koudougou Centre | 2 024 794 213 | 12,98 % |
| Sahel Distribution — Kaya Marché | 1 733 230 083 | 11,11 % |
| **Total** | **15 595 154 955** | **100,00 %** |

Trois lectures que ce tableau autorise — et une qu'il interdit :

- **Le premier magasin fait plus du tiers du réseau** (34,06 %). C'est un fait de structure, pas de
  performance : il est plus grand (Ouaga 2000), il vend plus, et sa part est stable.
- **Le rapport entre le premier et le dernier vaut 3,06.** Toute action commerciale « pour égaliser » les
  magasins se heurte donc à un écart de taille, pas à un écart de talent — la surface, le bassin de
  population et l'assortiment ne sont pas dans la table.
- **La somme des parts vaut 100,00 %** : la partition est bien le réseau entier. C'est la preuve exigée au
  §5.3, et elle tient en une addition.

La lecture **interdite** est celle qu'un rapport pressé écrit tout de suite : « Ouaga 2000 porte le réseau ».
Faux : c'est le magasin le plus gros d'un réseau de cinq, et rien dans ces cinq lignes ne dit qu'il *tire*
les autres. Une part n'est pas une contribution au résultat — question qui exigera la marge (C06 du module
M13 et les coûts d'achat du socle).

## 7. Démonstration pas à pas — six étapes sur le socle

Toutes les commandes de cette section ont été exécutées dans l'atelier. Le socle se reconstruit d'abord :

```python
import sys; sys.path.insert(0, "03_exercices/dossier_M11")
from connexion import ouvrir
con = ouvrir()                       # 0,4 s : le script du socle est rejoué en mémoire
```

### 7.1 Étape 1 — le total de contrôle

```sql
SELECT COUNT(*), COUNT(*) FILTER (WHERE NOT est_retour), SUM(montant_ttc) FILTER (WHERE NOT est_retour)
FROM ventes;
```

```text
240000 | 237191 | 15595154955
```

C'est la ligne à retrouver à la fin de **chaque** rapport du module.

### 7.2 Étape 2 — la part, avec la fenêtre

```sql
SELECT m.nom AS magasin, SUM(v.montant_ttc) AS ca,
       ROUND(100.0 * SUM(v.montant_ttc) / SUM(SUM(v.montant_ttc)) OVER (), 2) AS part_pct
FROM ventes v JOIN magasin m USING (id_magasin)
WHERE NOT v.est_retour GROUP BY 1 ORDER BY ca DESC;
```

```text
Sahel Distribution — Ouaga 2000      | 5312205459 | 34.06
Sahel Distribution — Gounghin        | 3424978244 | 21.96
Sahel Distribution — Bobo Kibidwé    | 3099946956 | 19.88
Sahel Distribution — Koudougou Centre| 2024794213 | 12.98
Sahel Distribution — Kaya Marché     | 1733230083 | 11.11
```

### 7.3 Étape 3 — la même réponse par sous-requête scalaire

```sql
SELECT m.nom, SUM(v.montant_ttc) AS ca,
       ROUND(100.0 * SUM(v.montant_ttc) / (SELECT SUM(montant_ttc) FROM ventes WHERE NOT est_retour), 2)
FROM ventes v JOIN magasin m USING (id_magasin) WHERE NOT v.est_retour GROUP BY 1 ORDER BY ca DESC;
```

Sortie **identique**, colonne par colonne. La comparaison des deux écritures porte donc sur la lisibilité
et le coût (**150 ms** contre **292 ms**), pas sur la justesse.

### 7.4 Étape 4 — une part calculée dans son année

```sql
SELECT strftime(date_trunc('month', date_vente), '%Y-%m') AS mois, YEAR(date_vente) AS annee,
       ROUND(SUM(montant_ttc)) AS ca,
       ROUND(100.0 * SUM(montant_ttc) / SUM(SUM(montant_ttc)) OVER (PARTITION BY annee), 1) AS part_annee_pct
FROM ventes WHERE NOT est_retour GROUP BY 1, 2 ORDER BY 1;
```

```text
2023-01 | 2023 | 284400304 | 8.3
2023-02 | 2023 | 263183276 | 7.6
...
2023-12 | 2023 | 333819159 | 9.7
```

**44 lignes**, une par mois, chacune portant la part de son mois **dans son année**. Janvier 2023 pèse
**8,3 %** de 2023.

### 7.5 Étape 5 — le piège : le filtre et la fenêtre dans le même `SELECT`

```sql
WITH m AS (SELECT strftime(date_trunc('month', date_vente), '%Y-%m') am, YEAR(date_vente) an,
                  SUM(montant_ttc) ca FROM ventes WHERE NOT est_retour GROUP BY 1, 2)
SELECT ROUND(100.0 * ca / SUM(ca) OVER (PARTITION BY an), 1) FROM m WHERE am = '2023-01';
```

```text
100.0
```

Le `WHERE` s'exécute **avant** la fenêtre : au moment du calcul, la partition ne contient plus qu'une seule
ligne, celle qu'on vient de garder. La bonne écriture filtre **après**, dans une requête englobante :

```sql
WITH m AS (…)
SELECT part FROM (SELECT am, ROUND(100.0 * ca / SUM(ca) OVER (PARTITION BY an), 1) part FROM m)
WHERE am = '2023-01';
```

```text
8.3
```

Deux requêtes, deux réponses, un seul mot d'écart : l'emplacement du filtre. **8,3 %** est la part du mois
dans son année ; **100,0 %** est un artefact.

### 7.6 Étape 6 — la fenêtre n'a pas réduit la table

```sql
SELECT id_vente, id_magasin, ROUND(montant_ttc) AS montant,
       COUNT(*) OVER () AS lignes_du_socle, ROUND(AVG(montant_ttc) OVER ()) AS moyenne_generale
FROM ventes WHERE NOT est_retour LIMIT 5;
```

```text
47820  | 1 | 53690  | 237191 | 65749
92080  | 1 | 2039   | 237191 | 65749
92628  | 1 | 21240  | 237191 | 65749
99471  | 1 | 57112  | 237191 | 65749
119868 | 1 | 37524  | 237191 | 65749
```

Chaque ligne a **conservé** son identifiant, son magasin et son montant, et **reçu en plus** deux
informations de contexte : **237 191** lignes au total et **65 749** FCFA de montant moyen par ligne. Une
requête `GROUP BY` ne peut pas publier cela : elle aurait rendu **1** ligne.

## 8. Erreurs fréquentes

1. **Partitionner sur une colonne qui n'est plus là après `GROUP BY`.** Le moteur refuse : `column
   "date_vente" must appear in the GROUP BY clause or must be part of an aggregate function`. Ce n'est pas
   une brimade : à l'étage de la fenêtre, la colonne a déjà été remplacée par un groupe. La correction est
   d'ajouter l'**expression** au `GROUP BY` (ici `YEAR(date_vente) AS annee`) puis de partitionner sur
   l'alias. Retenez la règle : **une fenêtre ne partitionne que sur ce qui existe à son étage**.
2. **Filtrer avant de fenêtrer.** Le `WHERE` étant évalué avant les fenêtres, filtrer un mois puis calculer
   sa part sur l'année laisse une seule ligne dans la partition : **100,0 %** au lieu de **8,3 %**. Toute
   comparaison « cette ligne par rapport à son ensemble » doit filtrer **après** le calcul — donc dans une
   requête englobante.
3. **Partitionner sur sa propre clé de regroupement.** `GROUP BY annee` + `PARTITION BY annee` rend 100 %
   partout. Le chiffre est exact, la conclusion est nulle : si votre rapport de parts ne contient que des
   100 %, la partition n'a pas été choisie, elle a été recopiée.
4. **Joindre une table de totaux sans vérifier son grain.** La table des totaux mensuels par magasin
   contient **220** lignes (une par couple magasin-mois). Jointe sur le mois **seul**, elle apporte **5**
   lignes de totaux à chaque vente, et le rapport publie **77 975 774 775** FCFA au lieu de
   **15 595 154 955** : **5** fois trop, **1 185 955** lignes au lieu de **237 191**, et aucun message
   d'erreur. Le grain de la table jointe est **la** chose à vérifier avant la jointure.
5. **Croire qu'un cumul est un indicateur de niveau.** Un cumul dépend de la date de début, de l'ordre
   choisi et du départage des ex æquo : deux analystes honnêtes peuvent en publier deux valeurs différentes
   du même socle. Préciser `ORDER BY` **et** la clé de départage, sinon le cumul n'est pas reproductible.

## 9. Bonnes pratiques professionnelles

1. **Écrire les fenêtres dans cet ordre : le grain, la partition, l'ordre, le cadre.** Une requête de
   fenêtre se relit toujours dans le même sens : *quelle ligne par ligne ?* puis *comparée à quoi ?* puis
   *dans quel ordre ?* puis *sur quelle profondeur ?*. Si l'une des quatre réponses manque, la requête est
   incomplète même si elle tourne.
2. **Appliquer la preuve de la partition.** Après toute part relative, contrôler que la somme vaut 100 % au
   niveau voulu : sur tout le résultat (`OVER ()`), par magasin, par année. Sans ce contrôle, l'erreur n°3
   passe en production.
3. **Choisir la fenêtre pour ce qui se compare, la sous-requête pour ce qui s'isole.** Une constante
   (le taux de TVA de référence, un seuil) se lit par sous-requête ou par paramètre ; un **contexte
   changeant** (le total d'un groupe, la moyenne d'une famille) s'écrit en fenêtre, parce que le contexte
   doit être **vu**.
4. **Toujours nommer les colonnes de contexte.** `COUNT(*) OVER ()` se nomme `lignes_du_socle`, pas
   `c1`. Un rapport de BI est lu six mois plus tard par quelqu'un qui n'a pas la requête sous les yeux.
5. **Terminer par le total de contrôle.** **15 595 154 955** FCFA. Un écart de ce total signale une
   jointure multiplicatrice (erreur n°4) avant que la conclusion ne soit écrite.

## 10. Exercice guidé

**Situation.** Vous produisez le rapport « poids des vendeurs » pour le comité de direction. Le socle contient
**22** vendeurs. Votre stagiaire a publié ce tableau, qui a beaucoup plu :

| Vendeur | Part du CA | Rang |
|---|---|---|
| Vendeur 7 | 8,68 % | 1 |
| Vendeur 21 | 8,44 % | 2 |
| Vendeur 12 | 7,89 % | 3 |

**Consigne.** Dans les 20 minutes (chrono), sans ouvrir `ATTENDU.json` :

1. Écrivez la requête qui produit exactement ces trois colonnes, avec la part en fenêtre. (3 pts)
2. Ajoutez la **preuve** que la partition choisie est la bonne : une colonne ou une requête qui montre à
   quoi les parts additionnent. (3 pts)
3. Le stagiaire jure avoir testé : « la somme des colonnes fait 100 % ». Expliquez en deux lignes pourquoi
   son test ne prouve rien ici. (2 pts)
4. Le comité demande maintenant la part **par magasin** pour chaque vendeur (un vendeur appartient à un
   magasin). Modifiez la fenêtre. (2 pts)
5. Écrivez le **total de contrôle** que vous joindrez au rapport, et dites ce qu'un écart révélerait. (2 pts)

## 11. Exercices autonomes

**E1 — Le mois dans son année, dans son magasin, dans son réseau (35 min).** Sur le socle, produisez une
seule requête rendant pour chaque couple **magasin-mois** (220 lignes) : le CA, sa part dans l'année du
magasin, sa part dans le réseau pour ce mois. Les trois colonnes doivent sommer à 100 % **au niveau de leur
partition** — joignez à votre rendu le contrôle qui le prouve. Contrainte : aucune sous-requête scalaire,
uniquement des fenêtres.

**E2 — Le contrôle de grain (25 min).** Construisez la table des totaux mensuels par magasin, puis écrivez
**deux** jointures : l'une sur le mois seul, l'autre sur les deux clés. Publiez les deux totaux, expliquez
l'écart par le nombre de lignes, et déduisez-en la phrase que vous diriez à un collègue pour l'aider à
détecter ce piège dans son propre rapport.

## 12. Correction détaillée

**Exercice guidé.**

1. **La requête.** Le classement des vendeurs se calcule sur les ventes nettes, groupées par vendeur :

   ```sql
   SELECT v.id_vendeur,
          SUM(v.montant_ttc) AS ca,
          ROUND(100.0 * SUM(v.montant_ttc) / SUM(SUM(v.montant_ttc)) OVER (), 2) AS part_pct
   FROM ventes v WHERE NOT v.est_retour
   GROUP BY 1 ORDER BY ca DESC LIMIT 3;
   ```

   La fenêtre est `OVER ()` : la partition est le **réseau entier**, ce qui correspond à la question posée
   (« poids de chaque vendeur dans la société »).
2. **La preuve.** Une part ne se valide pas sur son maximum, elle se valide sur sa **somme** au niveau de la
   partition :

   ```sql
   WITH p AS (SELECT id_vendeur, SUM(montant_ttc) ca FROM ventes WHERE NOT est_retour GROUP BY 1)
   SELECT ROUND(SUM(100.0 * ca / SUM(ca) OVER ()), 2) FROM p;   -- 100.00
   ```

   Vingt-deux lignes, une somme, un verdict.
3. **Pourquoi le test du stagiaire ne prouve rien.** Il a vérifié que **ses trois lignes publiées** totalisent
   moins de 100 % — ou pire, il a additionné les parts de tout le monde sans le dire. Un contrôle de part se
   fait **sur la partition complète**, jamais sur l'extrait qu'on publie : un classement tronqué au top 3
   somme par construction à 24,99 %, et cela ne dit rien de la justesse de la partition.
4. **La part dans le magasin.** On ajoute `id_magasin` au `GROUP BY` (il faut qu'il existe à l'étage de la
   fenêtre), puis on partitionne dessus :

   ```sql
   SELECT id_magasin, id_vendeur, SUM(montant_ttc) AS ca,
          ROUND(100.0 * SUM(montant_ttc) / SUM(SUM(montant_ttc)) OVER (PARTITION BY id_magasin), 2)
   FROM ventes WHERE NOT est_retour GROUP BY 1, 2 ORDER BY 1, ca DESC;
   ```

   Le même vendeur change de part **sans qu'aucune donnée n'ait changé** : c'est le sens du chapitre.
5. **Le total de contrôle.** `SELECT SUM(montant_ttc) FROM ventes WHERE NOT est_retour;` doit rendre
   **15 595 154 955** FCFA. Un écart signalerait une jointure multiplicatrice (chaque ligne comptée
   plusieurs fois) ou un filtre sur les retours oublié — les deux erreurs qui font un chiffre trop gros.

**E1 (les trois parts emboîtées).** La structure attendue : le `GROUP BY` fabrique les couples magasin-mois
avec leur CA, puis **trois fenêtres** calculent trois contextes différents sur cette même table agrégée.

```sql
WITH m AS (SELECT id_magasin, YEAR(date_vente) an,
                  strftime(date_trunc('month', date_vente), '%Y-%m') am, SUM(montant_ttc) ca
           FROM ventes WHERE NOT est_retour GROUP BY 1, 2, 3)
SELECT id_magasin, am, ca,
       ROUND(100.0 * ca / SUM(ca) OVER (PARTITION BY id_magasin, an), 2) AS part_dans_l_annee,
       ROUND(100.0 * ca / SUM(ca) OVER (PARTITION BY am), 2) AS part_du_mois_reseau
FROM m ORDER BY am, id_magasin;
```

Le contrôle : `SUM(part_dans_l_annee)` sur un magasin et une année vaut 100,00 (les 12 mois, ou 8 en 2026) ;
`SUM(part_du_mois_reseau)` sur un mois vaut 100,00 (les 5 magasins). Le même CA, deux partitions, deux
lectures — et un tableau qui ne somme à 100 % à aucun autre niveau.

**E2 (le contrôle de grain).** La table des totaux compte **220** lignes. Jointe sur le mois **seul**, chaque
vente rencontre 5 lignes de totaux : le résultat passe à **1 185 955** lignes et le total annoncé à
**77 975 774 775** FCFA, cinq fois **15 595 154 955**. Jointe sur les deux clés, on retrouve **237 191**
lignes et le total juste. La phrase à dire à un collègue : « avant de joindre une table de totaux, écris
`COUNT(*)` **avant** et **après** la jointure : si le nombre de lignes augmente, ta clé de jointure est
incomplète ».

## 13. Mini-projet de chapitre

**La note de trois pages : « la part et l'écart ».** Vous produisez, pour le comité de la quincaillerie, une
note de 3 pages maximum portant sur le socle M11 (240 000 lignes, 44 mois, 5 magasins).

**Livrables et barème.**

| Critère | Ce qui est vérifié | Points |
|---|---|---|
| La requête de part | une fenêtre `OVER ()`, avec le total de contrôle **15 595 154 955** FCFA | 6 |
| La part par magasin **et** dans l'année | deux partitions dans la même note, chacune avec sa preuve à 100 % | 5 |
| Le piège documenté | le filtre avant/après fenêtre, chiffré (**8,3 %** contre **100,0 %**) | 4 |
| La phrase de conclusion | ce que la note autorise à dire, et ce qu'elle **interdit** de dire | 3 |
| **Total** | | **18** |

## 14. Résumé du chapitre

`GROUP BY` réduit une table à ses groupes ; une **fonction de fenêtre** ajoute à chaque ligne une information
calculée sur un **ensemble** de lignes, sans en supprimer aucune. Cet ensemble se déclare : `OVER ()` pour
toute la table, `OVER (PARTITION BY …)` pour un groupe, avec un `ORDER BY` interne dès qu'il s'agit de
cumuler, et un **cadre** (`ROWS BETWEEN …`) pour décider de la profondeur du regard. Le facteur de comparaison
est **le** contenu de la requête : `OVER ()` répond « part de la société », `PARTITION BY id_magasin` répond
« part de son magasin », et la même mesure change de sens sans qu'une donnée change. Trois pièges, tous
mesurés ici : le `WHERE` qui s'exécute **avant** la fenêtre (**100,0 %** au lieu de **8,3 %**), la jointure
sur une clé incomplète (**77 975 774 775** FCFA au lieu de **15 595 154 955**), la partition recopiée du
`GROUP BY` (100 % partout). Aucun des trois ne lève d'erreur — d'où la règle de la maison : **terminer
chaque rapport par son total de contrôle**.

## 15. À retenir

1. **`GROUP BY` répond « combien », la fenêtre répond « par rapport à quoi ».** Si votre question contient
   « part », « écart », « rang » ou « cumul », il vous faut une fenêtre.
2. **Le nombre de lignes ne change pas.** Une requête à fenêtre sur 237 191 lignes rend 237 191 lignes ; si
   vous en obtenez 5, vous avez écrit un `GROUP BY`.
3. **La partition est une décision, pas une syntaxe.** Elle doit être écrite dans la requête, prouvée par une
   somme à 100 %, et relisible six mois plus tard.
4. **La fenêtre s'évalue après le `WHERE` et après le `GROUP BY`.** Filtrer avant de comparer fausse la
   comparaison ; partitionner sur une colonne non regroupée fait échouer la requête.
5. **Un rapport de comparaison sans total de contrôle est un pari.** Le total du socle est **15 595 154 955**
   FCFA, et il tient en une ligne de SQL.

> **À retenir.** Une fonction de fenêtre ne change pas les données, elle change ce qu'on peut **dire** des
> données : elle rend une ligne comparable à un ensemble, explicitement.

> **À retenir.** La question à se poser avant d'écrire `OVER (` n'est jamais « quelle syntaxe ? » mais
> **« comparé à quoi ? »** — et la réponse doit figurer dans la requête, pas dans la tête de l'analyste.

## 16. Évaluation formative

Répondez sans machine, puis vérifiez avec l'atelier (5 minutes) :

1. Quelle est la différence, en une phrase, entre `SUM(x)` et `SUM(x) OVER ()` dans une requête **sans**
   `GROUP BY` ?
2. Combien de lignes rend `SELECT id_magasin, COUNT(*) OVER () FROM ventes WHERE NOT est_retour` ?
3. Dans `SUM(SUM(x)) OVER (PARTITION BY annee)`, que fait le `SUM` intérieur ? Que fait celui de la fenêtre ?
4. Vous lisez un rapport de parts où chaque ligne affiche 100,0 %. Quelle est la cause la plus probable ?
5. Vous voulez la part de janvier 2023 dans l'année 2023. Où placez-vous le filtre sur le mois, et pourquoi ?
6. Que vaut la somme des parts de tous les mois d'une année si la partition est `PARTITION BY annee` ?
7. Que se passe-t-il si vous joignez une table de totaux mensuels par magasin sur le mois seul ?
8. Un cumul est-il reproductible sans clé de départage ? Justifiez en trois mots.
9. Quelle est la forme la plus courte du total de contrôle du module ?
10. Pourquoi une part publiée sur un top 3 ne peut-elle pas être validée en additionnant ses trois lignes ?

**Réponses.** 1. `SUM(x)` sans `GROUP BY` réduit toute la table à une valeur ; `SUM(x) OVER ()` rend une
valeur **par ligne**, identique partout. 2. **237 191** lignes — une par vente nette ; la fenêtre ne réduit
pas. 3. Le `SUM` intérieur agrège le groupe (le mois) ; la fenêtre additionne ces totaux d'année. 4. Le
`PARTITION BY` porte sur la même colonne que le `GROUP BY` : chaque groupe se compare à lui-même ; c'est
l'erreur n°3. 5. **Après** le calcul de la part, dans une requête englobante — sinon la partition ne contient
plus qu'une ligne et la part vaut 100,0 % au lieu de **8,3 %**. 6. 100,00 %, et c'est la preuve attendue.
7. Chaque vente rencontre les totaux de tous les magasins du mois : **5** fois trop de lignes
(**1 185 955** au lieu de **237 191**) et **77 975 774 775** FCFA au lieu de **15 595 154 955**. 8. Non :
sans clé de départage, l'ordre des ex æquo est choisi par le moteur. 9.
`SELECT SUM(montant_ttc) FROM ventes WHERE NOT est_retour` → **15 595 154 955** FCFA. 10. Parce qu'un
classement tronqué ne somme à 100 % à aucun niveau : la preuve se fait sur la **partition complète**, pas
sur l'extrait publié.
