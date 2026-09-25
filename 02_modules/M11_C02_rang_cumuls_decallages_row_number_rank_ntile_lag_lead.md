# Module M11.C02 — Classer, cumuler, décaler : `ROW_NUMBER`, `RANK`, `DENSE_RANK`, `NTILE`, `SUM() OVER`, `LAG`, `LEAD`

**Outils : DuckDB 1.5.5 (exécuté), SQLite (contrôle croisé, exécuté), PostgreSQL et SQL Server (cités, non exécutés — règle §1.5).
Durée indicative : 5 h. Niveau : N3 → N4. Prérequis : M11.C01 (fenêtres, `OVER`, `PARTITION BY`, cadre) ;
M07.C03 (`ORDER BY`, `LIMIT`), M07.C05 (`GROUP BY`) ; M02 (moyenne, médiane).**

> **L'idée du chapitre.** C01 a montré comment **comparer** une ligne à un ensemble. C02 en fait un usage
> qui produit des chiffres faux à une fréquence inquiétante : **ranger**. Un classement est une affirmation
> — « ce vendeur est le premier », « ce client fait partie des 10 % les plus fidèles » — et toute affirmation
> de rang se paie d'une décision : celle du **départage**. Le socle du module rend le problème visible :
> parmi les 23 497 clients, il n'existe que **21** nombres de tickets différents, et **3 316** clients ont
> exactement le même (**8** tickets). Selon la fonction employée, le même socle place le dernier client au
> rang **23 444** ou au rang **21** — deux nombres justes, un seul interprétable. Et le classement peut
> contredire le total : les 5 magasins du réseau sont rangés **exactement à l'envers** selon qu'on les
> classe par chiffre d'affaires ou par panier moyen.

> **Matériel de l'atelier — DuckDB 1.5.5 · Python 3.13 · socle M11 (`03_exercices/dossier_M11/socle_m11.sql`,
> rejoué en 0,4 s).** Rappel du socle : **240 000** lignes, **237 191** ventes nettes (**2 809** retours),
> **44** mois, **5** magasins, **145 212** tickets, **23 497** clients, **15 595 154 955** FCFA de chiffre
> d'affaires net. Toutes les sorties de ce chapitre sont celles de l'atelier, exécutées le 24/09/2026.

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous savez :

1. **Choisir entre `ROW_NUMBER`, `RANK` et `DENSE_RANK`** sur un cas réel comportant des ex æquo, et
   **expliquer** ce que chacun affirme — numéroter, classer, ou compter les niveaux.
2. **Départager un classement** : reconnaître qu'une mesure comporte des égalités massives et écrire la
   clé qui rend le résultat reproductible.
3. **Découper en groupes de taille égale** avec `NTILE`, et savoir pourquoi un découpage en tiers n'est
   pas un classement.
4. **Extraire un top N par groupe** (les 3 premiers produits de chaque famille) et **filtrer après** le
   calcul du rang, jamais avant.
5. **Calculer un cumul et une variation** avec `SUM() OVER (ORDER BY …)` et `LAG`/`LEAD`, en traitant
   explicitement le premier trou du décalage.
6. **Lire un classement comme une affirmation discutable** : vérifier qu'il répond bien à la question
   posée, et pas à une autre.

## 2. Pourquoi cette notion est importante

Trois des demandes les plus fréquentes d'un responsable se formulent en rang :

- « sortez-moi le **top 20** des produits » : un classement tronqué ;
- « le chiffre **cumulé** depuis janvier » : une somme en mouvement ;
- « la **progression** par rapport au mois dernier » : un décalage.

Chacune se trompe d'une façon différente, et aucune ne produit de message d'erreur. Un top tronqué au
mauvais rang publie cinq lignes pour un cinquième rang : les 5 clients à **20** tickets du socle occupent
les rangs 2, 3, 4, 5 et 6 en numérotation, mais **tous le rang 2** en classement — un rapport qui annonce
« le 5e client » raconte une hiérarchie qui n'existe pas. Un cumul sans ordre explicite change de valeur
selon l'heure de la journée. Une variation calculée sur le premier mois d'une série compare à un vide et
publie `NULL`, que la plupart des tableurs affichent comme une cellule vide — donc comme un zéro.

**Le chiffre qui structure ce chapitre.** Le socle contient **23 497** clients et seulement **21** valeurs
distinctes de « nombre de tickets ». La mesure est donc **massivement** faite d'égalités : **3 316** clients
partagent 8 tickets. Sur cette mesure, `RANK` descend jusqu'au rang **23 444** tandis que `DENSE_RANK`
s'arrête à **21**. Les deux requêtes sont exactes ; l'une des deux n'a aucun intérêt pour un décideur, et
il faut savoir laquelle on publie avant que le comité de direction ne compare deux rapports incompatibles.

## 3. Explication simple — le podium et les dossards

À l'arrivée d'une course, trois documents différents peuvent être imprimés, et ils ne disent pas la même
chose :

- **`ROW_NUMBER` = les dossards de classement.** Chaque coureur reçoit un numéro **unique**, de 1 à n, dans
  l'ordre d'arrivée. S'il y a égalité, on tranche arbitrairement (un tirage) ou par une règle explicite
  (« à égalité, celui dont l'identifiant est le plus petit »). Personne ne partage un dossard.
- **`RANK` = le podium.** Deux coureurs à égalité reçoivent la **même** place, et les places suivantes sont
  **sautées**. Trois arrivants ex æquo en 2e position : ils sont tous 2e, et le suivant est 5e. C'est la
  règle des médailles olympiques.
- **`DENSE_RANK` = le nombre de niveaux.** Deux coureurs à égalité partagent la 2e place, et le suivant
  prend la **3e** : on ne compte que les niveaux de performance réellement distincts.

Et **`NTILE(n)` = la photo de famille.** On coupe la troupe en n groupes de taille aussi égale que possible.
Ce n'est pas un classement : deux coureurs du même groupe peuvent avoir des performances très différentes,
et surtout, à la frontière, deux ex æquo peuvent tomber **de part et d'autre** de la ligne de coupe. C'est
ce que le chapitre mesure sur le socle : un tiers comptant **2 718**, **2 720**, **2 728** ou **2 738**
clients selon l'exécution — le même socle, le même code, quatre chiffres.

## 4. Vocabulaire essentiel

| Terme (français) | Équivalent anglais | Définition en une phrase |
|---|---|---|
| **numérotation** | *row numbering* | Attribuer un numéro unique à chaque ligne d'une partition (`ROW_NUMBER`) : aucune égalité possible. |
| **classement à égalité** | *rank* | Attribuer la même place aux lignes de même valeur, en sautant les places suivantes (`RANK`). |
| **rang dense** | *dense rank* | Attribuer la même place aux ex æquo sans sauter de place (`DENSE_RANK`) : il compte les **niveaux**. |
| **ex æquo** | *tie* | Deux lignes de valeur identique sur la mesure classée : le cas qui décide du choix de la fonction. |
| **clé de départage** | *tie-breaker* | La colonne ajoutée à l'`ORDER BY` d'une fenêtre pour rendre un classement reproductible (presque toujours l'identifiant). |
| **quantile** | *quantile / bucket* | Découpage en groupes de taille comparable (`NTILE(n)`) : tiers, quarts, déciles. |
| **top N par groupe** | *top-N per group* | Le motif `PARTITION BY groupe ORDER BY mesure DESC` puis filtre sur le rang — le classement le plus demandé en BI. |
| **cumul** | *running total* | Somme qui s'arrête à la ligne courante (`SUM(x) OVER (ORDER BY …)`) ; dépend de l'ordre et du départage. |
| **décalage** | *lag / lead* | La valeur de la ligne précédente ou suivante dans l'ordre (`LAG`/`LEAD`) : c'est ce qui rend possible une variation. |
| **trou de série** | *series gap* | La ligne qui n'a pas de prédécesseur (premier mois) : elle rend `NULL`, et ce `NULL` doit être **déclaré**. |

> **Définition.** Les trois fonctions de rang répondent à trois questions différentes sur la même mesure :
> « **donne-moi un numéro unique** » (`ROW_NUMBER`), « **quelle place mérite-t-elle ?** » (`RANK`),
> « **combien de niveaux de performance y a-t-il jusqu'ici ?** » (`DENSE_RANK`). Choisir, c'est décider de
> ce que le rapport affirmera — pas de ce qui est le plus pratique.

> **Définition.** Une **clé de départage** — *tie-breaker* — est une colonne ajoutée après la mesure dans
> l'`ORDER BY` d'une fenêtre (presque toujours la clé primaire de la table) pour que deux exécutions du même
> code produisent **le même** résultat. Sans elle, le moteur est libre : le classement n'est pas faux, il
> est **instable**.

## 5. Cours approfondi

### 5.1 Trois fonctions de rang, une seule mesure

```sql
WITH c AS (SELECT id_client, COUNT(DISTINCT id_ticket) t FROM ventes WHERE NOT est_retour GROUP BY 1)
SELECT id_client, t,
       ROW_NUMBER() OVER (ORDER BY t DESC, id_client) AS numero,
       RANK()       OVER (ORDER BY t DESC)           AS place,
       DENSE_RANK() OVER (ORDER BY t DESC)           AS niveau
FROM c ORDER BY t DESC, id_client;
```

Sur le socle, les premières lignes montrent le client **0** (identifiant non référencé) seul au sommet, puis
un groupe de clients à **20** tickets :

| `id_client` | tickets | `NUMERO` | `PLACE` | `NIVEAU` |
|---|---|---|---|---|
| 0 | 38 984 | 1 | 1 | 1 |
| 3545 | 20 | 2 | 2 | 2 |
| 14859 | 20 | 3 | 2 | 2 |
| 21036 | 20 | 4 | 2 | 2 |
| 21392 | 20 | 5 | 2 | 2 |

Cinq clients ont exactement **20** tickets. `NUMERO` les numérote 2, 3, 4, 5, 6 (l'ordre entre eux vient
du départage par identifiant) ; `PLACE` leur donne à tous **2** ; `NIVEAU` aussi **2**. Les trois colonnes
sont justes — elles répondent à trois questions que le demandeur n'a pas distinguées. « Le 5e meilleur
client » est une phrase vide : il n'existe pas de 5e meilleur client, il existe cinq clients deuxièmes.

### 5.2 Le départage : ce qui rend un classement reproductible

Sur la même mesure, l'écart entre `RANK` et `DENSE_RANK` s'amplifie à mesure qu'on descend : le `RANK`
maximum atteint **23 444** (il saute les places perdues par les 3 316 clients à 8 tickets, et par tous les
autres ex æquo), tandis que le `DENSE_RANK` maximum vaut **21** — soit exactement le nombre de niveaux de
fréquence observés.

> **Dans les faits.** L'atelier a exécuté **15** fois la même requête de segmentation RFM (C04) **sans** clé
> de départage : le segment principal a compté **2 718**, **2 720**, **2 728** puis **2 738** clients. Le
> socle n'a pas changé d'une ligne. Ce n'est pas une erreur de mesure : c'est `NTILE` qui, à la frontière
> d'un tiers, choisit librement parmi des ex æquo. **3 316** clients partageant 8 tickets suffisent à
> déplacer cette frontière — et un segment qui bouge de 20 clients est un segment qu'on ne peut pas
> comparer à celui du trimestre dernier.

La règle est donc simple et non négociable : **toute fenêtre d'ordonnancement reçoit un départage**.
`ORDER BY t DESC, id_client` au lieu de `ORDER BY t DESC`. C'est une colonne de plus, et c'est la
différence entre un indicateur et un tirage au sort.

> **Attention.** Le départage ne change pas la **valeur** de la mesure, il change la **frontière**. Un top 3
> par groupe avec ou sans départage peut désigner deux produits différents quand trois produits sont ex æquo
> — et le rapport, dans les deux cas, présentera trois lignes avec l'aplomb d'un résultat définitif.

### 5.3 `NTILE` : découper en tranches, pas classer

`NTILE(3) OVER (ORDER BY m DESC)` range les lignes en trois groupes de taille aussi égale que possible :
c'est le découpage utilisé partout pour « les 10 % les plus gros clients ». Deux précautions, mesurées au
§5.2 : le **départage** (sinon la frontière bouge) et la **définition** du découpage. Sur le socle, les deux
écritures les plus courantes du « top 10 % » ne gardent pas le même nombre de lignes : `NTILE(100) <= 10`
retient 2 350 clients, `ROW_NUMBER() <= 0,10 × 23 497` en retient 2 349. La part de chiffre d'affaires
publiée est alors de **38,1 %** ou de **38,0 %** — un dixième de point, mais deux rapports qui ne se
réconcilient plus.

> **Définition.** Un **quantile** — *quantile* — est une frontière qui coupe une population ordonnée en
> parties de taille comparable : les tiers (`NTILE(3)`), les déciles (`NTILE(10)`), les centiles
> (`NTILE(100)`). Un quantile n'est pas un seuil : il ne demande pas « combien valent-ils ? » mais
> « combien sont-ils ? ».

### 5.4 Le top N par groupe : le motif qui exige un filtre **après**

Le classement le plus demandé en BI est le top N **par** groupe : les 3 meilleurs produits par famille, les
5 meilleurs clients par magasin. Le motif s'écrit en deux temps, et l'ordre des temps compte :

```sql
SELECT * FROM (
  SELECT p.categorie, p.designation, SUM(v.montant_ttc) AS ca,
         ROW_NUMBER() OVER (PARTITION BY p.categorie ORDER BY SUM(v.montant_ttc) DESC) AS rg
  FROM ventes v JOIN produit p USING (id_produit)
  WHERE NOT v.est_retour
  GROUP BY 1, 2
) WHERE rg <= 3 ORDER BY categorie, ca DESC;
```

Le filtre `rg <= 3` est **à l'extérieur** de la requête qui calcule le rang. Écrit dans la même requête, il
s'appliquerait avant la fenêtre : `RANK` vaudrait alors **1** pour **toutes** les lignes restantes, et le
rapport publierait un « top 3 » qui contient tout ce qu'on a laissé passer. C'est exactement le piège du
`WHERE` avant la fenêtre (C01, §5.7), appliqué au cas le plus fréquent de la BI.

Exécuté sur le socle, ce top 3 rend **46** lignes — alors qu'un top 3 sur les **7** familles réelles du
catalogue en rend **21**. L'écart n'est pas un problème de requête : il vient des **16** libellés de
catégorie du référentiel produits (**9** écritures après casse et espaces, **7** familles après accents et
pluriel), un défaut de qualité que C05 puis C07 traitent à fond. Retenez pour l'instant que
le top N par groupe est l'endroit où une donnée mal normée devient **visible** : 46 lignes de réponse pour
7 familles, sans le moindre message d'alerte.

### 5.5 `SUM() OVER` : le cumul, et sa clôture

Un cumul s'écrit avec le même `SUM` que C01, plus un `ORDER BY` **dans** la fenêtre :

```sql
SELECT an, mm, ca, SUM(ca) OVER (PARTITION BY an ORDER BY mm) AS cumul
FROM (SELECT YEAR(date_vente) an, date_trunc('month', date_vente) mm, SUM(montant_ttc) ca
      FROM ventes WHERE NOT est_retour GROUP BY 1, 2);
```

Sur 2023, le cumul passe par **284 400 304** ; **547 583 580** ; **881 958 439** ; **1 196 335 034** FCFA,
et la part cumulée par **8,3** ; **15,9** ; **25,6** ; **34,7** %. Deux contrôles gratuits :

1. **la clôture** : au dernier mois de l'année, le cumul doit égaler le total de l'année —
   **3 443 581 547** FCFA pour 2023 ;
2. **la monotonie** : un cumul de chiffre d'affaires ne peut pas diminuer. S'il diminue, une ligne a été
   comptée deux fois ou une annulation n'a pas été traitée.

### 5.6 `LAG` et `LEAD` : la variation, et son premier trou

`LAG(ca) OVER (ORDER BY mm)` rend la valeur du mois **précédent**, `LEAD` celle du mois **suivant**. La
variation s'écrit alors directement, sans auto-jointure — la raison pour laquelle `LAG` a remplacé une
bonne moitié des jointures dites « auto-jointures » des rapports d'avant.

Un décalage de **12** lignes donne la comparaison **annuelle** à périmètre égal : c'est la façon la plus
honnête de comparer deux années, parce qu'elle compare **le même mois**. Sur les **32** mois du socle qui
ont un équivalent un an plus tôt, la progression annuelle moyenne vaut **+16,8 %** — et les premiers mois
de 2024 valent **+11,0 %**, **+23,5 %**, **+20,6 %**, **+27,7 %**, **+11,5 %**.

> **Définition.** Un **trou de série** — *series gap* — est une ligne dont le décalage n'a pas de
> prédécesseur : le premier mois d'une série, ou le premier mois après un filtre trop zélé. `LAG` rend
> alors `NULL`, et l'arithmétique propage ce `NULL` (`ca - NULL` vaut `NULL`). Ce n'est pas un bug : c'est
> la réponse exacte à une question impossible — « par rapport à quoi ? ».

> **Attention.** Le `WHERE` s'exécute avant la fenêtre. Une requête écrite
> `SELECT am, ca, LAG(ca, 12) OVER (ORDER BY am) … WHERE am >= '2024-01'` filtre **puis** décale : les
> douze premiers mois manquent à l'appel et la première variation annuelle publiée est `NULL`. L'atelier a
> reproduit ce résultat avant de le corriger en calculant la fenêtre dans une sous-requête, puis en
> filtrant au-dessus.

### 5.7 Le classement qui contredit le total

Le socle fournit la démonstration la plus nette de ce qui distingue un **total** d'un **classement**. Les
cinq magasins, rangés par chiffre d'affaires puis par panier moyen :

| Magasin | CA net (FCFA) | Rang CA | Panier moyen (FCFA) | Rang panier |
|---|---|---|---|---|
| Ouaga 2000 | 5 312 205 459 | 1 | 107 374 | 3 |
| Gounghin | 3 424 978 244 | 2 | 106 621 | 4 |
| Bobo Kibidwé | 3 099 946 956 | 3 | 105 724 | 5 |
| Koudougou Centre | 2 024 794 213 | 4 | 108 035 | 2 |
| Kaya Marché | 1 733 230 083 | 5 | 111 447 | 1 |

Le classement par panier est **l'inverse** du classement par chiffre d'affaires : le dernier magasin du
réseau a le plus gros panier moyen (**111 447** FCFA contre **107 374** pour le premier). Aucun des deux
tableaux n'est faux, et aucune des deux conclusions ne s'ensuit : un petit magasin sert moins de clients,
mais des clients qui achètent plus par visite. Publier « Kaya vend mal » ou « Kaya vend le mieux » est, dans
les deux cas, une erreur de lecture — la bonne phrase porte sur ce qui est mesuré : *le panier moyen, pas
l'activité*.

> **Conseil professionnel.** Avant de publier un classement, écrivez en une phrase la question à laquelle
> il répond, et vérifiez qu'elle contient bien la mesure classée : « les magasins **par chiffre d'affaires** »,
> « les magasins **par panier moyen** ». Un classement publié sans sa mesure est un classement qui sera lu
> comme un jugement de valeur.

### 5.8 Ce que ce chapitre ne couvre pas

Le temps **calendaire** — le mois sans vente qu'il faut fabriquer, la table de dates, l'absence de
comparaison quand la période est incomplète — est le sujet de C03 : `LAG` compare des **lignes**, pas des
**dates**, et deux mois qui se suivent dans un résultat ne sont pas forcément deux mois voisins au
calendrier. La segmentation par **cohortes** et le **RFM** complet sont ceux de C04.

## 6. Exemple concret — trois classements, un seul socle

Le directeur commercial demande « les meilleurs clients ». La question, telle quelle, ne détermine pas la
mesure : en tickets, en montant, en récence ? Le tableau de bord du module retient la **fréquence** (nombre
de tickets) et publie **trois** colonnes de rang — c'est le seul moyen de montrer la différence en
production :

| `id_client` | Tickets | `NUMERO` | `PLACE` | `NIVEAU` |
|---|---|---|---|---|
| 0 | 38 984 | 1 | 1 | 1 |
| 3545 | 20 | 2 | 2 | 2 |
| 14859 | 20 | 3 | 2 | 2 |
| 21036 | 20 | 4 | 2 | 2 |
| 21392 | 20 | 5 | 2 | 2 |
| 5 | 8 | 10 435 | 10 434 | 14 |

La dernière ligne est la leçon du chapitre. Un client à **8** tickets — la valeur la plus fréquente du
socle, partagée par **3 316** clients — porte le numéro **10 435** (unique, donc faux comme information
puisque 3 315 autres clients sont derrière lui à la même valeur), la place **10 434** (juste, illisible),
et le niveau **14** (lisible : il existe 14 niveaux de fréquence au-dessus du sien sur **21** possibles).

Et le client **0** ? Il est premier partout, avec **2 852 612 447** FCFA et **18,3 %** du chiffre
d'affaires du réseau — et il **n'existe pas** dans le référentiel clients : c'est l'identifiant des ventes
non identifiées. Le classement l'ignore superbement, parce qu'un classement ne vérifie rien : il ordonne
ce qu'on lui donne. Ce cas traverse tout le module et devient l'étude de cas de son évaluation.

## 7. Démonstration pas à pas — six étapes sur le socle

### 7.1 Étape 1 — mesurer l'ampleur des égalités avant de classer

```sql
WITH c AS (SELECT id_client, COUNT(DISTINCT id_ticket) t FROM ventes WHERE NOT est_retour GROUP BY 1)
SELECT COUNT(*) AS clients, COUNT(DISTINCT t) AS valeurs_distinctes, MAX(t) AS maximum FROM c;
```

```text
23497 | 21 | 38984
```

**23 497** clients pour **21** valeurs distinctes : le classement par fréquence est un classement
d'égalités. Toute la suite du chapitre en découle.

### 7.2 Étape 2 — les trois rangs côte à côte

C'est la requête du §5.1. Sa sortie montre le client 0 seul au sommet, puis les cinq clients à 20 tickets
qui partagent la place 2 (§6).

### 7.3 Étape 3 — l'écart maximal entre les deux classements

```sql
WITH c AS (SELECT id_client, COUNT(DISTINCT id_ticket) t FROM ventes WHERE NOT est_retour GROUP BY 1),
     r AS (SELECT RANK() OVER (ORDER BY t DESC) rk, DENSE_RANK() OVER (ORDER BY t DESC) dr FROM c)
SELECT MAX(rk), MAX(dr) FROM r;
```

```text
23444 | 21
```

Le dernier client du socle est **23 444e** ou **21e** selon la fonction. Dit autrement : « le nombre de
niveaux de fréquence » est une information, « le 23 444e client » n'en est pas une.

### 7.4 Étape 4 — le cumul, et son contrôle de clôture

```sql
WITH m AS (SELECT YEAR(date_vente) an, date_trunc('month', date_vente) mm, SUM(montant_ttc) ca
           FROM ventes WHERE NOT est_retour GROUP BY 1, 2),
     c AS (SELECT mm, SUM(ca) OVER (PARTITION BY an ORDER BY mm) cumul,
                  SUM(ca) OVER (PARTITION BY an) total FROM m WHERE an = 2023)
SELECT mm, cumul, total, cumul = total AS cloture FROM c ORDER BY mm;
```

```text
2023-01-01 |  284400304 | 3443581547 | false
2023-02-01 |  547583580 | 3443581547 | false
2023-03-01 |  881958439 | 3443581547 | false
...
2023-12-01 | 3443581547 | 3443581547 | true
```

Une seule ligne de contrôle (`cumul = total`) suffit à valider les douze mois.

### 7.5 Étape 5 — la variation mensuelle, puis annuelle

```sql
WITH m AS (SELECT date_trunc('month', date_vente) mm, SUM(montant_ttc) ca FROM ventes
           WHERE NOT est_retour GROUP BY 1)
SELECT mm, ca, LAG(ca) OVER (ORDER BY mm) AS mois_precedent,
       ROUND(100.0 * (ca - LAG(ca) OVER (ORDER BY mm)) / LAG(ca) OVER (ORDER BY mm), 1) AS var_pct
FROM m ORDER BY mm LIMIT 5;
```

```text
2023-01-01 | 284400304 | NULL       | NULL
2023-02-01 | 263183276 | 284400304  | -7.5
2023-03-01 | 334374859 | 263183276  | 27.1
2023-04-01 | 314376595 | 334374859  | -6.0
2023-05-01 | 275723327 | 314376595  | -12.3
```

Le premier mois rend `NULL` : il n'a pas de mois précédent. La variation mensuelle d'un socle de
quincaillerie est **bruyante** (de −12,3 % à +27,1 % en cinq mois) : c'est exactement pourquoi le
chapitre C03 lui préférera des moyennes mobiles.

### 7.6 Étape 6 — la comparaison annuelle, et le piège du filtre

Avec `LAG(ca, 12)`, la comparaison porte sur le **même mois** de l'année précédente : **+11,0 %**,
**+23,5 %**, **+20,6 %**, **+27,7 %**, **+11,5 %** pour les cinq premiers mois de 2024, et **+16,8 %** en
moyenne sur les **32** mois comparables. Écrite avec le filtre dans la même requête que la fenêtre, la même
requête publie `NULL` — le filtre a supprimé les douze mois dont `LAG` avait besoin.

## 8. Erreurs fréquentes

1. **Numéroter quand on voulait classer.** `ROW_NUMBER` attribue un numéro unique : sur une mesure à
   égalités, il **invente** une hiérarchie (5 clients à 20 tickets deviennent 2e, 3e, 4e, 5e et 6e). Le
   rapport qui en découle annonce « le 5e meilleur client » alors qu'il n'en existe que deux niveaux.
2. **Classer sans départage.** Sans colonne de départage, deux exécutions peuvent rendre deux frontières
   différentes : l'atelier a mesuré **2 718**, **2 720**, **2 728** et **2 738** clients pour un même
   segment RFM. Un indicateur qui bouge sans que la donnée bouge n'est pas un indicateur.
3. **Filtrer le top N dans la même requête que le rang.** `WHERE rg <= 3` s'applique **avant** la fenêtre :
   le rang vaut alors 1 pour toutes les lignes survivantes et le « top 3 » contient tout ce qui a passé le
   filtre. Le filtre sur un rang se met **toujours** dans une requête englobante.
4. **Publier une variation sur le premier mois.** `LAG` rend `NULL` au premier mois, et la division propage
   le `NULL`. Afficher ce `NULL` comme « 0 % » est la faute la plus coûteuse des séries temporelles : elle
   transforme un trou en information.
5. **Confondre le rang et le total.** Le premier magasin du réseau par chiffre d'affaires n'est que
   **3e** par panier moyen, et le dernier est **1er**. Les deux classements sont justes ; un rapport qui
   n'annonce pas sa mesure sera lu comme un jugement sur les équipes.

## 9. Bonnes pratiques professionnelles

1. **Mesurer les égalités avant de classer.** `COUNT(DISTINCT mesure)` à côté de `COUNT(*)` : si le rapport
   est faible (ici **21** valeurs pour **23 497** lignes), le choix de la fonction de rang n'est plus un
   détail, c'est le sujet.
2. **Toujours départager, et écrire pourquoi.** `ORDER BY mesure DESC, id_client` : la clé de départage est
   l'identifiant le plus petit, et cela se documente en commentaire dans la requête — un lecteur qui ne
   comprend pas la règle d'égalité ne peut pas reproduire le rapport.
3. **Choisir la fonction selon la phrase, pas l'inverse.** « Il est 2e » → `RANK`. « Il existe deux niveaux
   au-dessus » → `DENSE_RANK`. « Il est le 3e de la liste » → `ROW_NUMBER` **avec** départage assumé.
4. **Contrôler un cumul par sa clôture et sa monotonie.** Le dernier cumul égale le total de la période ;
   un cumul qui diminue signale un doublon ou une annulation non traitée.
5. **Déclarer les trous.** Quand une série commence, le premier décalage est `NULL` : on l'écrit dans la
   note de méthode du rapport (« les variations de janvier 2023 ne sont pas calculables : pas d'antériorité
   dans la base ») plutôt que de laisser la cellule vide.

## 10. Exercice guidé

**Situation.** Le comité de direction a reçu, la semaine dernière, deux rapports sur la fidélité des
clients, produits par deux analystes de l'équipe. Le premier conclut : « **5** clients dépassent 20 tickets ;
le 5e est à 20 tickets ». Le second conclut : « le seuil des plus fidèles est de **20** tickets ; **cinq**
clients l'atteignent ». Les deux rapports sont **incompatibles** et la direction demande pourquoi.

**Consigne.** Dans les 20 minutes (chrono) :

1. Écrivez la requête qui reproduit le classement du premier rapport, et celle du second. (3 pts)
2. Expliquez, en nommant les fonctions, pourquoi elles ne disent pas la même chose sur les **mêmes**
   données. (3 pts)
3. Montrez, chiffres en main, où les deux rapports divergent **le plus** : quel est l'écart maximal entre
   `RANK` et `DENSE_RANK` sur le socle ? (2 pts)
4. Écrivez la phrase que vous enverriez aux deux analystes pour qu'ils produisent à l'avenir des rapports
   comparables. (2 pts)

## 11. Exercices autonomes

**E1 — Le top N par famille, proprement (35 min).** Produisez les **3** produits les plus vendus de chaque
**famille** réelle du catalogue — au sens de **C05**, qui définit la famille comme le libellé replié (casse,
espaces, accents, pluriel) — et non de chaque libellé présent dans le fichier. Pour chaque produit
son rang, son chiffre d'affaires et la part qu'il représente **dans sa famille**. Contrainte : le filtre sur
le rang doit être **à l'extérieur** de la requête qui le calcule, et vous joindrez la preuve du nombre de
lignes attendu (3 × nombre de familles).

**E2 — Le cumul et la variation d'un magasin (30 min).** Pour le magasin de votre choix, publiez mois par
mois : le chiffre d'affaires, le cumul depuis janvier 2023, la variation mensuelle et la variation annuelle
à périmètre égal. Contrôles exigés : le cumul du dernier mois égale le total du magasin, et les mois sans
antériorité sont **déclarés** `NULL` (pas zéro).

## 12. Correction détaillée

**Exercice guidé.**

1. **Les deux requêtes.** Le premier rapport classe avec `ROW_NUMBER` (ou avec `LIMIT 5` sur un tri) :

   ```sql
   WITH c AS (SELECT id_client, COUNT(DISTINCT id_ticket) t FROM ventes WHERE NOT est_retour GROUP BY 1)
   SELECT id_client, t, ROW_NUMBER() OVER (ORDER BY t DESC, id_client) AS numero
   FROM c ORDER BY t DESC, id_client LIMIT 5;
   ```

   Le second annonce une **égalité**, donc un `RANK` (ou un `DENSE_RANK`) :

   ```sql
   WITH c AS (SELECT id_client, COUNT(DISTINCT id_ticket) t FROM ventes WHERE NOT est_retour GROUP BY 1)
   SELECT id_client, t, RANK() OVER (ORDER BY t DESC) AS place FROM c
   WHERE place <= 2 ORDER BY t DESC, id_client;
   ```
2. **Pourquoi les deux conclusions diffèrent.** Le premier affirme une **hiérarchie** (« le 5e est à
   20 tickets ») : `ROW_NUMBER` numérote des lignes, y compris quand elles ont la même valeur. Le second
   affirme un **niveau** (« cinq clients atteignent 20 tickets ») : `RANK` attribue la même place aux ex
   æquo. Sur des données sans égalité, les deux coïncident — c'est pourquoi l'erreur passe longtemps
   inaperçue.
3. **L'écart maximal.** Sur le socle, `MAX(RANK)` vaut **23 444** et `MAX(DENSE_RANK)` vaut **21**. L'écart
   vient des **3 316** clients à 8 tickets, qui font sauter 3 315 places à eux seuls.
4. **La phrase à envoyer.** « Merci de préciser dans chaque rapport la fonction de rang employée et la clé
   de départage : `RANK` pour parler de places (avec égalités partagées), `DENSE_RANK` pour parler de
   niveaux, `ROW_NUMBER` seulement quand un rang unique est explicitement demandé — et dans ce cas, écrire
   la règle de départage. »

**E1 (le top 3 par famille).** Il faut d'abord **normaliser** le libellé : `UPPER(TRIM(categorie))` réunit
casse et espaces (**9** écritures), et le repliement des accents et du pluriel ramène à **7** familles
(voir C05). Puis classer par famille :

```sql
WITH p AS (SELECT id_produit, UPPER(TRIM(categorie)) AS famille FROM produit),
     v AS (SELECT p.famille, p.id_produit, SUM(x.montant_ttc) AS ca
           FROM ventes x JOIN p USING (id_produit) WHERE NOT x.est_retour GROUP BY 1, 2)
SELECT * FROM (
  SELECT famille, id_produit, ca,
         ROW_NUMBER() OVER (PARTITION BY famille ORDER BY ca DESC, id_produit) AS rg,
         ROUND(100.0 * ca / SUM(ca) OVER (PARTITION BY famille), 1) AS part_famille_pct
  FROM v
) WHERE rg <= 3 ORDER BY famille, rg;
```

Contrôle attendu : **21** lignes (3 × **7** familles). Sans la normalisation, la même requête sur les
libellés bruts rend **46** lignes — l'écart est la trace exacte du défaut de qualité du référentiel.

**E2 (le cumul d'un magasin).** La structure attendue est celle du §7.4 avec `PARTITION BY id_magasin`,
plus un `LAG(ca, 12) OVER (PARTITION BY id_magasin ORDER BY am)` pour la variation annuelle. Les deux
contrôles : le cumul du dernier mois égale le total du magasin (**5 312 205 459** FCFA pour Ouaga 2000,
**1 733 230 083** FCFA pour Kaya Marché), et les douze premiers mois affichent une variation annuelle
`NULL` — déclarée, jamais remplacée par zéro.

## 13. Mini-projet de chapitre

**La note « trois classements, une mesure ».** Vous produisez 3 pages maximum pour le comité commercial :
trois classements du même socle, avec la mesure annoncée pour chacun et la preuve du départage.

**Livrables et barème.**

| Critère | Ce qui est vérifié | Points |
|---|---|---|
| Les trois classements | `ROW_NUMBER`, `RANK`, `DENSE_RANK` sur la même mesure, sorties publiées | 6 |
| La preuve du départage | la clé de départage écrite et justifiée ; une deuxième exécution rend le même résultat | 5 |
| Les chiffres d'égalité | **23 497** clients, **21** valeurs distinctes, **3 316** clients à 8 tickets, écart **23 444** contre **21** | 4 |
| La phrase de conclusion | une phrase par classement, avec la mesure annoncée et ce qu'elle interdit de dire | 3 |
| **Total** | | **18** |

## 14. Résumé du chapitre

Classer, c'est décider **ce qu'on affirme** : `ROW_NUMBER` numérote des lignes (hiérarchie inventée si
égalités), `RANK` attribue des places (les suivantes sont sautées), `DENSE_RANK` compte les niveaux.
Sur le socle, la mesure de fréquence ne compte que **21** niveaux pour **23 497** clients, dont **3 316**
partagent 8 tickets : le choix de la fonction n'est jamais neutre. `NTILE` découpe en tranches de taille
égale — utile pour « les 10 % les plus gros », dangereux sans **clé de départage** (l'atelier a mesuré des
frontières à **2 718**, **2 720**, **2 728** et **2 738** clients pour la même requête). Le **top N par
groupe** place le filtre **après** le rang, jamais avant. Le **cumul** se contrôle par sa clôture (le
cumul de décembre égale **3 443 581 547** FCFA pour 2023) et par sa monotonie. Le **décalage** (`LAG`,
`LEAD`) calcule variations mensuelles et annuelles — **+16,8 %** en moyenne sur les **32** mois
comparables du socle — à condition de **déclarer** le premier trou. Et un classement ne vaut que par sa
mesure : les cinq magasins sont rangés exactement à l'envers selon qu'on classe par chiffre d'affaires ou
par panier moyen.

## 15. À retenir

1. **`ROW_NUMBER` numérote, `RANK` classe, `DENSE_RANK` compte les niveaux.** Trois questions différentes,
   trois colonnes justes, un seul rapport recevable — celui qui annonce la sienne.
2. **Aucune fenêtre d'ordonnancement sans clé de départage.** Sans elle, le classement change sans que la
   donnée change.
3. **Le filtre sur un rang se met dans une requête englobante.** Dans la même requête, il s'applique avant
   la fenêtre et le rang vaut 1 partout.
4. **Un cumul se contrôle deux fois** : sa clôture (dernier cumul = total de la période) et sa monotonie.
5. **`LAG` du premier mois rend `NULL`, et ce `NULL` se déclare.** Le remplacer par zéro est une invention.

> **À retenir.** Un classement est une **phrase**, pas une colonne : « les magasins par panier moyen »
> n'affirme pas la même chose que « les magasins par chiffre d'affaires », même quand les deux tableaux
> contiennent les mêmes cinq noms.

> **À retenir.** L'égalité n'est pas un cas limite : c'est le cas normal d'une mesure de comptage. Un
> classement écrit sans penser aux ex æquo est un classement écrit pour un autre jeu de données.

## 16. Évaluation formative

Répondez sans machine, puis vérifiez avec l'atelier (5 minutes) :

1. Cinq clients ont 20 tickets. Que valent leur `ROW_NUMBER`, leur `RANK` et leur `DENSE_RANK` s'ils sont
   précédés d'un seul client à 38 984 tickets ?
2. Sur le socle, `MAX(RANK)` et `MAX(DENSE_RANK)` valent respectivement… ? Pourquoi un tel écart ?
3. Pourquoi `NTILE` a-t-il besoin d'une clé de départage, alors qu'il ne publie aucun rang ?
4. Où placer le filtre `rg <= 3` d'un top 3 par groupe, et que se passe-t-il sinon ?
5. Que vaut **2 718** dans ce chapitre ? Et **2 738** ?
6. Pourquoi le cumul de décembre doit-il égaler le total de l'année ?
7. Que rend `LAG(ca, 12)` pour le premier mois d'une série, et que publie-t-on à la place ?
8. Le premier magasin en chiffre d'affaires est 3e en panier moyen : quelle phrase peut-on écrire, et
   laquelle est interdite ?
9. Combien de lignes rend un top 3 par catégorie sur les libellés du fichier, et combien sur les familles
   réelles ?
10. Pourquoi la variation mensuelle du socle est-elle un mauvais indicateur de tendance, avant même le
    chapitre C03 ?

**Réponses.** 1. `ROW_NUMBER` : 2, 3, 4, 5, 6 ; `RANK` : 2 pour les cinq ; `DENSE_RANK` : 2 pour les cinq.
2. **23 444** et **21** : `RANK` saute les places des ex æquo (les **3 316** clients à 8 tickets en font
sauter 3 315 à eux seuls), `DENSE_RANK` compte les niveaux. 3. Parce que la frontière des tranches tombe
au milieu d'ex æquo : sans départage, le moteur choisit qui passe (mesuré : **2 718**, **2 720**, **2 728**,
**2 738**). 4. Dans une requête **englobante** ; dans la même requête, le `WHERE` s'exécute avant la fenêtre
et le rang vaut 1 pour toutes les lignes restantes. 5. Deux tailles observées du même segment RFM selon
l'exécution : la preuve que la frontière n'est pas reproductible. 6. Parce que le cumul est la somme des
mois de l'année : s'il diffère, une ligne a été comptée deux fois ou manque. 7. `NULL` ; on **déclare** le
trou dans la note de méthode. 8. « Ouaga 2000 réalise le plus gros chiffre d'affaires du réseau et un panier
moyen de **107 374** FCFA, inférieur à celui de Kaya Marché (**111 447** FCFA) » ; interdit : « Ouaga 2000
vend mieux que les autres ». 9. **46** lignes (16 libellés) contre **21** (7 familles). 10. Parce que la
variation mensuelle va de −12,3 % à +27,1 % en cinq mois sur un socle stable : elle mesure le calendrier et
le hasard plus que la tendance.
