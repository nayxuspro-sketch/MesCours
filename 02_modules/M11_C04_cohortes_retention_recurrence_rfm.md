# Module M11.C04 — Cohortes, rétention et récurrence : RFM, et le client qui n'a pas de nom

**Outils : DuckDB 1.5.5 (exécuté), SQLite (contrôle croisé, exécuté), PostgreSQL et SQL Server (cités, non exécutés — règle §1.5.
Durée indicative : 4 h. Niveau : N3 → N4. Prérequis : M11.C01 à C03 (fenêtres, cadres, temps) ;
M09.C04 (segmentation client) ; M08.C06 (indicateurs de fidélité).**

> **L'idée du chapitre.** Il existe deux façons de mesurer si les clients reviennent, et la plus répandue
> est la mauvaise. La lecture **calendaire** demande « combien des clients actifs en juin sont revenus en
> juillet ? » — sur le socle, **13,2 %** (**432** des **3 276** clients de juin). La lecture **par cohorte**
> demande « quels clients dont c'était le premier achat en juin sont revenus en juillet ? » — **22,7 %**,
> mais sur **22** clients seulement. Les deux nombres prétendent décrire la même chose et n'ont ni la même
> base, ni la même signification : le premier est stable et mesure le **mélange** du fichier, le second est
> juste et trop petit pour être publié. Ce chapitre apprend à construire la **cohorte**, à lire la matrice
> en **triangle**, et à pondérer les taux avant de les commenter. Puis il assemble les trois mesures que
> tout le monde utilise sans les définir — récence, fréquence, montant — et montre ce qu'elles deviennent
> quand **18,3 %** du chiffre d'affaires est porté par un client qui n'a pas de nom.

> **Matériel de l'atelier — DuckDB 1.5.5 · socle M11 (`03_exercices/dossier_M11/socle_m11.sql`).**
> **23 497** clients de vente, **44** cohortes mensuelles, **237 191** lignes nettes, **15 595 154 955**
> FCFA, du **01/01/2023** au **31/08/2026**. Toutes les sorties publiées ici sont celles de l'atelier,
> exécutées le 24/09/2026.

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous savez :

1. **Construire une cohorte** sur l'événement métier qui compte — la **première commande** — et non sur la
   date d'inscription du référentiel.
2. **Produire une matrice de rétention** cohorte × ancienneté, et **reconnaître sa forme** : un triangle,
   pas un rectangle.
3. **Calculer une rétention pondérée** par la taille des cohortes, et expliquer pourquoi la moyenne simple
   des taux est fausse.
4. **Distinguer trois questions voisines** : la rétention par cohorte, la récurrence calendaire et
   l'activité d'un mois.
5. **Segmenter en RFM** avec `NTILE`, départage explicite, et nommer les segments sans inventer de seuils
   « métier ».
6. **Traiter le client non identifié** : le mesurer, décider, et l'écrire dans la note de méthode.

## 2. Pourquoi cette notion est importante

Le socle permet de répondre à une question que le comité de direction posera tôt ou tard : **nos clients
reviennent-ils ?** Il faut choisir un chiffre. Les candidats :

| Ce qui est calculé | Chiffre | Ce que ça mesure vraiment |
|---|---|---|
| Clients actifs en juin 2025 revenus en juillet 2025 | **13,2 %** (**432** / **3 276**) | le renouvellement du fichier **actif**, toutes cohortes mêlées |
| Clients dont juin 2025 est le **premier** achat, revenus en juillet | **22,7 %** (**5** / **22**) | la fidélité **des nouveaux** — sur un effectif trop faible pour conclure |
| Rétention moyenne pondérée au premier mois suivant, toutes cohortes | **15,8 %** | la fidélité de la base entière, chaque client pesant une fois |

Le troisième chiffre est le seul qui soit à la fois **juste** et **publiable**. Le premier est juste aussi,
mais il ne répond pas à la question posée : il dépend du **mélange** de cohortes du mois, et il resterait
autour de **13 %** même si plus aucun nouveau client ne revenait jamais. Le deuxième est juste et
inutilisable : **22** clients.

Ce chapitre existe parce que ces trois chiffres sortent de trois requêtes qui se ressemblent, que rien
dans le résultat n'indique laquelle on a écrite, et que le plus gros des trois (le plus flatteur) est celui
qu'on retient.

## 3. Explication simple — la promotion d'une année, et le verre à moitié plein

Une école veut savoir si ses élèves de première année poursuivent en deuxième. Deux méthodes.

**La méthode fausse.** En septembre, on compte tous les élèves présents : premières, deuxièmes, troisièmes
années confondues. On recompte les mêmes en octobre. On annonce « **93 %** de nos élèves restent ». Le
chiffre est exact et ne dit rien : la masse des troisièmes années, qui ne peuvent pas partir avant la fin du
cycle, écrase le résultat. C'est la lecture calendaire.

**La méthode juste.** On prend **une** promotion, celle entrée en septembre. On la suit : combien sont là en
octobre, en novembre, un an plus tard. On obtient une courbe. Cette courbe, comparée à celle des promotions
entrantes des deux années précédentes, dit si l'école retient mieux qu'avant. C'est la cohorte.

**Ce qu'aucune des deux ne donne.** La lecture calendaire ne dit pas la qualité du service ; la lecture par
cohorte ne dit presque rien pour la promotion entrée ce mois-ci, parce qu'elle est petite et récente. Ce
qu'il faut, c'est **toutes les cohortes, pondérées** : chaque élève pèse une fois, quelle que soit son
année d'entrée. Sur le socle, cela donne **15,8 %** — et ce chiffre-là ne bouge plus quand le mélange change.

## 4. Vocabulaire essentiel

| Terme (français) | Équivalent anglais | Définition en une phrase |
|---|---|---|
| **cohorte** | *cohort* | Un groupe de clients partageant un événement de départ daté — ici le mois de leur **première** commande. |
| **ancienneté** | *cohort age* | Le nombre de mois écoulés depuis l'événement de départ ; noté M+1, M+3, M+12. |
| **matrice de rétention** | *retention matrix* | Le tableau cohortes × anciennetés : chaque ligne est une cohorte, chaque colonne une ancienneté. |
| **rétention** | *retention* | La part d'une cohorte revenue au moins une fois pendant l'ancienneté considérée. |
| **récurrence** | *recurrence* | La part des clients actifs un mois donné qui reviennent le mois suivant — toutes cohortes mêlées. |
| **pondération** | *weighting* | Donner à chaque cohorte un poids proportionnel à sa taille, et non le même poids à toutes. |
| **récence** | *recency* | Le délai écoulé depuis le dernier achat d'un client. |
| **fréquence** | *frequency* | Le nombre d'achats (ou de tickets) d'un client sur la période. |
| **montant** | *monetary value* | Le chiffre d'affaires attribué au client sur la période. |
| **RFM** | *recency, frequency, monetary* | Les trois mesures réunies, chacune découpée en tiers, pour segmenter le fichier client. |
| **segment** | *segment* | Le croisement des trois découpages : ici `133`, `233`, `333` — trois chiffres, de 1 à 3. |
| **client non identifié** | *anonymous customer / default member* | Un identifiant technique qui agrège des achats sans porteur : ici le client **0**. |

> **Définition.** Une **cohorte** est un ensemble de clients réunis par un **événement daté** commun — et
> l'événement doit être choisi avec soin. Le référentiel du socle contient une date d'inscription qui
> commence en **2016**, alors que la première vente observée n'est jamais antérieure à janvier 2023 : les
> clients existaient avant les données. Une cohorte d'**inscription** décrirait donc un autre monde que la
> cohorte de **première commande**. Règle : la cohorte est datée sur l'événement que le rapport mesure.

> **Définition.** La **rétention** est la part d'une cohorte encore active après N périodes. Elle exige donc
> **deux** définitions explicites : ce qu'est « active » (ici : au moins un ticket non retourné dans le
> mois) et ce qu'est « N » (ici : des mois complets, pas des fenêtres de 30 jours). Deux rapports qui ne
> partagent pas ces deux définitions ne peuvent pas comparer leurs taux.

## 5. Cours approfondi

### 5.1 La cohorte d'entrée : 44 lignes, une seule par client

```sql
WITH p AS (SELECT id_client, date_trunc('month', MIN(date_vente)) AS co
           FROM ventes WHERE NOT est_retour GROUP BY 1)
SELECT co, COUNT(*) AS taille FROM p GROUP BY 1 ORDER BY 1;
```

**44** lignes, du `2023-01` au `2026-08`. La première cohorte contient **3 593** clients, la dernière
(**2026-08**) exactement **3**. Ce déséquilibre n'est pas une anomalie de la base : c'est le résultat
attendu d'une période d'observation qui commence. Tous les clients qui étaient déjà là en janvier 2023 sont
comptés comme « entrants de janvier 2023 » — on dit que la série est **tronquée à gauche**.

> **Attention.** La troncature à gauche ne se corrige pas : on ne peut pas inventer les achats antérieurs
> au 01/01/2023. Elle se **déclare**. Sans cette phrase dans la note de méthode, le lecteur croira que la
> base a gagné **3 593** clients en un mois et en a perdu **3 590** en trois ans et demi.

### 5.2 La matrice : un triangle, jamais un rectangle

La matrice croise chaque cohorte avec chaque ancienneté. Extrait des six premières cohortes, sur six
anciennetés :

| Cohorte | Taille | M+0 | M+1 | M+2 | M+3 | M+4 | M+5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2023-01 | 3 593 | 100,0 % | 14,6 % | 18,3 % | 17,5 % | 15,0 % | 12,9 % |
| 2023-02 | 2 817 | 100,0 % | 19,1 % | 17,8 % | 15,9 % | 12,6 % | 11,5 % |
| 2023-03 | 3 137 | 100,0 % | 16,2 % | 15,0 % | 11,3 % | 10,5 % | 13,7 % |
| 2023-04 | 2 389 | 100,0 % | 14,6 % | 13,3 % | 11,3 % | 13,0 % | 15,9 % |
| 2023-05 | 1 653 | 100,0 % | 11,6 % | 11,4 % | 13,3 % | 16,0 % | 18,4 % |
| 2023-06 | 1 239 | 100,0 % | 11,0 % | 13,6 % | 14,9 % | 19,9 % | 17,5 % |

Deux choses sautent aux yeux, et aucune n'est un taux de fidélité.

**Le triangle.** Les **44** cohortes n'ont pas le même recul : **32** sont observables jusqu'à M+12, **20**
jusqu'à M+24. La matrice a donc la forme d'un escalier, et la case M+24 de la cohorte de 2026-08 est
**impossible** — pas vide par manque de données, mais par manque de **temps**. Un tableau qui la remplirait
par zéro publierait une chute que personne n'a mesurée.

**Le mélange des cohortes.** Chaque ligne a sa taille : **3 593** en tête, **1 239** six mois plus tard. Une
rétention « moyenne » calculée comme la moyenne des taux donnerait donc le même poids à ces deux
populations — c'est la faute du §5.3.

![La matrice de rétention par cohorte de première commande — 44 cohortes, 13 anciennetés, et les cases grisées là où le recul manque (production : `tools/figures_M11.py`)](../figures/M11_C04_matrice_retention.svg)

### 5.3 Le piège des deux lectures

Le même mois, deux questions, deux réponses :

```sql
-- lecture calendaire : les actifs de juin, revenus en juillet
WITH a AS (SELECT DISTINCT id_client, date_trunc('month', date_vente) AS m
           FROM ventes WHERE NOT est_retour)
SELECT COUNT(*) AS base_juin,
       COUNT(*) FILTER (WHERE id_client IN (SELECT id_client FROM a WHERE m = DATE '2025-07-01')) AS revenus
FROM a WHERE m = DATE '2025-06-01';
```

```text
base_juin | revenus
3276      | 432
```

**13,2 %**. C'est un taux de **récurrence**, pas de rétention : il mesure la proportion des clients actifs
d'un mois qui reviennent le mois suivant, quelle que soit leur date d'entrée. Il est utile (c'est la
« respiration » du fichier) et il ne répond pas à « nos nouveaux clients reviennent-ils ? ».

Pour répondre à cette question-là, il faut la même paire de mois vue **par la cohorte** :

```sql
WITH p AS (SELECT id_client, date_trunc('month', MIN(date_vente)) AS co
           FROM ventes WHERE NOT est_retour GROUP BY 1),
     a AS (SELECT DISTINCT id_client, date_trunc('month', date_vente) AS m
           FROM ventes WHERE NOT est_retour),
     c AS (SELECT id_client FROM p WHERE co = DATE '2025-06-01')
SELECT (SELECT COUNT(*) FROM c) AS base,
       (SELECT COUNT(*) FROM c WHERE id_client IN
        (SELECT id_client FROM a WHERE m = DATE '2025-07-01')) AS revenus;
```

```text
base | revenus
22   | 5
```

**22,7 %**, sur **22** clients. Le chiffre est juste et n'est pas publiable : à cette taille, un client de
plus ou de moins le fait bouger de 4,5 points.

Le troisième chiffre est celui qu'on publie — la **moyenne pondérée de toutes les cohortes** : **15,8 %**
au premier mois, chaque client pesant une fois. Le contrôle qui justifie la pondération tient en une
requête : sur les **23** cohortes d'au moins **100** clients, la moyenne **simple** des taux vaut **16,4 %**
et la moyenne **pondérée** **15,8 %**. L'écart n'est pas énorme, mais il existe — et il vient de là : dans la
moyenne simple, une cohorte de **22** clients pèse autant qu'une cohorte de **3 593**.

> **Définition.** La **pondération** consiste à donner à chaque cohorte un poids proportionnel à son
> effectif. Un taux moyen pondéré est la somme des clients revenus divisée par la somme des clients de
> départ — jamais la moyenne des taux. Le calcul direct est d'ailleurs plus simple : `SUM(actifs) /
> SUM(effectif)`.

> **Dans les faits.** La différence entre **16,4 %** et **15,8 %** paraît faible, et elle est **signée** :
> les petites cohortes récentes ont des taux plus élevés (elles contiennent des primo-acheteurs encore
> chauds), donc la moyenne simple **surestime** systématiquement. Sur un fichier client en forte croissance,
> l'écart se creuse — et il va toujours dans le sens flatteur.

### 5.4 Une rétention qui ne baisse pas

Le résultat le plus important du chapitre est peut-être le plus décevant :

| Ancienneté | M+1 | M+3 | M+6 | M+12 | M+24 |
|---|---:|---:|---:|---:|---:|
| Rétention pondérée | **15,8 %** | **15,4 %** | **15,9 %** | **17,2 %** | **18,2 %** |

La courbe est **plate**, et elle remonte même légèrement. La cohorte de janvier 2023 vue dans son intégralité
le confirme : de M+1 à M+43, elle reste entre **11,5 %** et **22,6 %**, sans tendance à la baisse, et se
termine à **16,9 %**.

L'interprétation est un exercice de rigueur, pas d'enthousiasme. Le socle ne raconte **pas** une entreprise
qui perd ses clients chaque mois. Il raconte une base composée de deux populations : une minorité d'acheteurs
réguliers, présents presque tous les mois, et une majorité de clients de passage — le socle compte
**3 316** clients à **8** tickets et **64** clients dont toute l'histoire tient dans **un seul** mois. Le
taux de **15,8 %** est le poids de la première population dans le fichier.

> **Attention.** « 15,8 % de rétention » ne signifie pas que **84 %** des clients sont perdus. Le taux
> compte comme active toute personne ayant acheté **au moins une fois** dans le mois : il ne mesure pas
> l'intensité, et un client régulier qui saute un mois compte comme sorti. Avant de parler de perte, il faut
> une deuxième mesure — la **récence** du §5.6.

### 5.5 Le RFM : trois mesures, une décision

Le RFM réunit trois colonnes par client — **R**écence, **F**réquence, **M**ontant — et les découpe chacune
en trois blocs de taille égale représentés par `1`, `2`, `3` :

```sql
WITH c AS (SELECT id_client, MAX(date_vente) AS derniere, COUNT(DISTINCT id_ticket) AS f,
                  SUM(montant_ttc) AS m
           FROM ventes WHERE NOT est_retour GROUP BY 1),
     s AS (SELECT id_client,
                  NTILE(3) OVER (ORDER BY derniere ASC, id_client) AS r,
                  NTILE(3) OVER (ORDER BY f DESC, id_client) AS f3,
                  NTILE(3) OVER (ORDER BY m DESC, id_client) AS m3,
                  m
           FROM c)
SELECT CAST(r AS VARCHAR) || CAST(f3 AS VARCHAR) || CAST(m3 AS VARCHAR) AS segment, m FROM s;
```

`NTILE(3)` produit trois blocs de **7 833**, **7 832** et **7 832** clients sur les **23 497** du socle :
c'est le découpage le plus égal possible, et il est exact. La lettre `1` va au **meilleur** tiers, donc la
récence se trie en ordre **croissant** (dernier achat récent) alors que la fréquence et le montant se trient
en ordre **décroissant**.

Trois résultats sur le socle :

- Le segment **`133`** — récents, peu fréquents, gros montants — réunit **2 151** clients et **4 937 755 609**
  FCFA, soit **31,7 %** du chiffre d'affaires net. C'est le plus gros segment par le montant, et il est
  **injouable** en l'état : il contient le client **0** (voir §5.7).
- Le tiers des **récents** (dernier achat entre le **18/06/2026** et le **31/08/2026**) porte **48,7 %** du
  chiffre d'affaires, contre **23,1 %** pour le tiers des anciens (dernier achat entre le **31/01/2023** et le
  **13/03/2026**).
- Le fichier se répartit donc en **27** segments possibles (3 × 3 × 3), dont la plupart restent vides ou
  minuscules : c'est normal, et un rapport qui n'en nomme que quatre ou cinq fait le bon choix.

> **Définition.** Le **RFM** n'a pas de frontières intrinsèques : les coupures en trois blocs égaux sont un
> choix de méthode (égalité des effectifs), pas une vérité métier. D'autres entreprises coupent à des seuils
> absolus (« plus de **12** mois sans achat », « au moins **5** commandes »). Ce qui rend un RFM défendable
> n'est jamais le découpage : c'est le fait de l'**écrire**.

> **Conseil professionnel.** Nommez les segments avec les bornes qui les définissent, jamais avec un
> adjectif. « Récents à faible fréquence, dernier achat depuis le 18/06/2026 » se vérifie ; « clients
> premium » ne se vérifie pas — et se discute pendant trois réunions.

### 5.6 Fréquence, récurrence, récence : les trois chiffres qui tiennent

Trois mesures complètent le RFM et se calculent sans segmentation :

| Mesure | Requête | Résultat sur le socle |
|---|---|---|
| **Récurrence** | écart entre deux tickets consécutifs du même client | médiane **96** jours, moyenne **137,2** jours, sur **171 737** paires |
| **Récence** | délai depuis le dernier achat, au 31/08/2026 | moyenne **156** jours, médiane **122** jours |
| **Inactivité** | clients sans achat depuis plus d'un an | **1 848** clients, **4,3 %** du CA net |

Deux enseignements. D'abord, l'écart systématique entre médiane et moyenne (**96** contre **137,2** jours ;
**122** contre **156**) est encore l'effet des gros clients : la moyenne décrit une minorité, la médiane
décrit le client courant. Ensuite, la règle « pas d'achat depuis plus d'un an = client perdu » donne
**1 848** clients — un effectif de campagne de réactivation, avec des noms et des adresses, et seulement
**4,3 %** du chiffre d'affaires à la clé. C'est précisément le genre d'arbitrage qu'un rapport doit rendre
possible : le coût d'une campagne se compare à **4,3 %** du CA, pas à une intuition.

### 5.7 Le client 0 : 18,3 % du CA sans porteur

Sur **23 497** identifiants clients, un seul n'existe pas dans le référentiel : le client **0**. Il porte
**42 658** lignes, **38 984** tickets et **2 852 612 447** FCFA — **18,3 %** du chiffre d'affaires net du
socle.

Le traiter « à part » n'est pas une option esthétique : c'est ce qui décide de la conclusion. La question
posée par l'évaluation du module — « **10 %** des clients font-ils **60 %** du chiffre d'affaires ? » — se
répond ainsi :

| Périmètre | Part du CA du dixième supérieur | Nombre de clients |
|---|---:|---:|
| Tous clients | **38,1 %** | 2 350 |
| Client 0 exclu | **24,2 %** | 2 349 |

Dans les deux cas, la réponse est **non** — mais elle a deux valeurs différentes, et la note de méthode doit
dire laquelle est publiée. Le client **0** appartient au dixième supérieur dans la lecture « tous clients » :
c'est **un** identifiant qui pèse à lui seul plus que les neuf dixièmes du fichier.

Il y a plus grave, et c'est une leçon de reproductibilité : sans clé de départage explicite, `NTILE` et
`ROW_NUMBER` **ne sont pas déterministes**. Le même recoupement RFM, exécuté **15** fois le 24/09/2026 sans
`ORDER BY …, id_client`, a situé le segment principal entre **2 718** et **2 738** clients selon
l'ordonnancement interne du moteur. La cause est mesurable : **3 316** clients partagent exactement **8**
tickets (**14,1 %** du fichier), donc la frontière des tiers tombe au milieu d'une égalité massive et le
moteur choisit qui passe. Ce n'est pas un bug, c'est une requête incomplète.

> **Attention.** Un rapport dont le chiffre change d'une exécution à l'autre n'est pas un rapport. Toute
> utilisation de `NTILE`, `RANK` ou `ROW_NUMBER` doit porter une clé de départage — ici `id_client` — et
> **la même** dans toutes les requêtes du rapport. Le contrôle se fait en comparant deux exécutions, pas en
> relisant la requête.

### 5.8 Ce que ce chapitre ne couvre pas

La **valeur vie client** (somme actualisée des marges futures) et la **prédiction de départ** exigent des
modèles, traités en M14 et M19. Ici, tout est **descriptif** : on mesure ce qui a eu lieu, avec des
définitions écrites. C'est déjà suffisant pour occuper une réunion entière.

## 6. Exemple concret — trois façons de répondre à la même question

Un responsable marketing demande : « combien de nos clients nous restent d'une année sur l'autre ? »

| Réponse | Calcul | Valeur | Utilisable ? |
|---|---|---|---|
| Activité | clients actifs en juin 2025 revenus en juillet 2025 | **13,2 %** | non : mesure le fichier, pas la fidélité |
| Cohorte du mois | cohorte de juin 2025, revenue en juillet | **22,7 %** sur 22 clients | non : effectif trop faible |
| Rétention pondérée | toutes cohortes, à M+12 | **17,2 %** | oui, avec sa définition |

La réponse à envoyer est la troisième, **accompagnée** de la phrase qui la rend lisible : « **17,2 %** des
clients d'une cohorte achètent de nouveau douze mois après leur premier achat ; le taux est **plat** de M+1
à M+24 (**15,8 %** à **18,2 %**), ce qui décrit un noyau d'acheteurs réguliers dans une base majoritairement
composée de clients de passage ». Trois chiffres, une phrase, aucune ambiguïté sur ce qui est mesuré.

## 7. Démonstration pas à pas — cinq étapes sur le socle

### 7.1 Étape 1 — la cohorte d'entrée

**44** cohortes, de **3 593** clients (janvier 2023) à **3** (août 2026). Contrôle : la somme des tailles
redonne les **23 497** clients du socle, chacun dans une seule cohorte.

### 7.2 Étape 2 — la matrice et son triangle

Le tableau du §5.2. Contrôle de forme : **32** cohortes tiennent jusqu'à M+12, **20** jusqu'à M+24. Les
cellules au-delà ne sont pas nulles, elles sont **inexistantes**.

### 7.3 Étape 3 — les deux lectures, côte à côte

**13,2 %** (**432** des **3 276** clients actifs en juin 2025) en lecture calendaire ; **22,7 %** (**5** sur
**22**) en lecture par cohorte. Puis la version publiable : **15,8 %** pondéré, contre **16,4 %** en moyenne
simple sur les **23** cohortes d'au moins **100** clients.

### 7.4 Étape 4 — le RFM, avec le client 0

Les trois blocs de **7 833**, **7 832** et **7 832** clients ; le segment **`133`** à **2 151** clients et
**31,7 %** du CA ; le tiers des récents à **48,7 %** du CA. Puis le retrait du client **0** : dixième
supérieur à **38,1 %**, puis **24,2 %**.

### 7.5 Étape 5 — les mesures de contrôle

Récurrence médiane **96** jours ; récence médiane **122** jours ; **1 848** clients inactifs depuis plus d'un
an (**4,3 %** du CA) ; **64** clients à un seul mois d'activité. Ce sont ces quatre chiffres qui permettent de
qualifier le taux de rétention de **15,8 %** — sans eux, il n'est qu'un nombre.

## 8. Erreurs fréquentes

1. **Dater la cohorte sur l'inscription.** Le référentiel porte des dates de création à partir de **2016**,
   les ventes commencent en **2023** : une cohorte d'inscription ne décrit pas le même univers. La cohorte se
   date sur l'événement mesuré.
2. **Compter des clients sur une jointure.** La jointure de la cohorte de janvier 2023 (**3 593** clients)
   avec les **44** mois d'activité rend **30 090** lignes. Un `COUNT(*)` au lieu d'un `COUNT(DISTINCT
   id_client)` multiplie la base par l'historique — sans erreur, sans avertissement.
3. **Moyenner des taux sans pondérer.** **16,4 %** au lieu de **15,8 %** : la moyenne simple donne le même
   poids à la cohorte de juin 2025 (**22** clients) qu'à celle de janvier 2023 (**3 593**).
4. **Classer sans clé de départage.** `NTILE` sur une fréquence qui compte **3 316** clients à **8** tickets
   fait bouger le segment principal entre **2 718** et **2 738** clients d'une exécution à l'autre.
5. **Lire un taux de rétention comme un taux de fidélité.** **15,8 %** au premier mois, **18,2 %** à M+24 :
   la courbe est plate, elle ne décrit pas une fuite mais la part des acheteurs réguliers.

## 9. Bonnes pratiques professionnelles

1. **Écrire la définition de « actif » en tête du rapport.** Un ticket non retourné dans le mois, retours
   exclus : ce choix change le taux, et il doit être visible avant le premier chiffre.
2. **Publier la taille de la base à côté de chaque taux.** **22,7 %** sur **22** clients et **15,8 %** sur
   **23 483** clients ne se lisent pas avec le même crédit ; un taux sans effectif est une rumeur.
3. **Pondérer, jamais moyenner.** `SUM(revenus) / SUM(effectif)` en une seule requête, et non la moyenne de
   44 taux.
4. **Traiter le client non identifié comme un cas, pas comme un client.** Il est mesuré (**18,3 %** du CA),
   nommé, et exclu des classements — ou conservé avec la mention explicite que le classement est faussé.
5. **Figer les classements par une clé de départage.** `ORDER BY …, id_client` partout, et la preuve par
   deux exécutions comparées : c'est le seul moyen d'être reproductible.

## 10. Exercice guidé

**Situation.** La direction commerciale veut lancer une campagne de réactivation. Elle vous demande :
« combien de clients avons-nous perdus, et combien cela nous coûte-t-il ? »

**Consigne.**

1. Écrivez la requête qui définit un client perdu — et justifiez la borne choisie. (2 pts)
2. Donnez le nombre de clients concernés et leur part du chiffre d'affaires. (3 pts)
3. Calculez la récurrence médiane et la récence médiane du fichier, et dites laquelle des deux vous
   utiliseriez pour fixer le délai de la campagne, et pourquoi. (3 pts)
4. Un collègue propose de joindre le référentiel clients pour filtrer les « vrais » clients. Que change
   cette jointure sur le total du socle ? (2 pts)

## 11. Exercices autonomes

**E1 — La matrice de rétention complète, et sa lecture (45 min).** Produisez la matrice des **44** cohortes,
de M+0 à M+24, avec la taille de chaque cohorte en première colonne. Puis répondez en cinq lignes : les
cohortes récentes retiennent-elles mieux ou moins bien que celles de 2023 ? Quelles cases de la matrice ne
sont pas observables, et pourquoi ?

**E2 — Deux segments RFM, deux politiques (35 min).** Construisez le RFM avec départage explicite, puis
comparez deux segments : le plus gros par le montant et celui des clients anciens à forte fréquence. Pour
chacun : effectif, part du CA, plage de récence. Terminez par une phrase de politique commerciale par
segment — une seule, et vérifiable par les chiffres que vous venez de produire.

## 12. Correction détaillée

**Exercice guidé.**

1. **La borne.** Un an sans achat est la borne la plus défendable sur ce socle, parce que la récurrence
   observée est longue (médiane **96** jours, moyenne **137,2** jours) : douze mois représentent plusieurs
   cycles d'achat manqués. La requête est un `MAX(date_vente)` par client comparé au **31/08/2026**.
2. **L'effectif.** **1 848** clients, soit **4,3 %** du chiffre d'affaires net — **663 520 490** FCFA. La
   bonne phrase est : « **4,3 %** du CA est à la clé, pas plus » ; c'est ce chiffre qui compare la campagne à
   son coût.
3. **Quelle mesure choisir.** La récurrence médiane (**96** jours) décrit le rythme entre deux achats, la
   récence médiane (**122** jours) la distance au dernier achat. Pour fixer un délai de campagne, on part de
   la **récurrence** : elle est stable et ne dépend pas du jour d'observation, contrairement à la récence,
   qui est une mesure « au 31/08/2026 » et vieillit d'un jour par jour.
4. **La jointure au référentiel.** Elle **retire** le client **0** (absent du référentiel), donc
   **2 852 612 447** FCFA et **18,3 %** du CA net du périmètre analysé. C'est un choix légitime, à condition
   d'être écrit : sans cette phrase, le total du rapport ne coïncide plus avec celui du compte de résultat.

**E1 (la matrice).** Les cohortes de 2023 et 2024 ne se distinguent pas nettement : les taux de M+1 restent
dans une fourchette étroite (de **11,0 %** à **19,1 %** sur les six premières). Les cases non observables
sont celles des cohortes récentes au-delà de leur recul : **32** cohortes tiennent à M+12, **20** à M+24, et
les colonnes lointaines se remplissent de la droite vers la gauche à mesure que le temps passe. Une matrice
de rétention se lit toujours **en triangle**, et sa lecture doit nommer la pointe comme « pas encore
observable ».

**E2 (deux segments).** Le plus gros par le montant est **`133`** : **2 151** clients, **4 937 755 609**
FCFA, **31,7 %** du CA — il contient le client **0** et doit être rejoué sans lui avant toute décision. Le
tiers des **récents** (dernier achat entre le **18/06/2026** et le **31/08/2026**) porte **48,7 %** du CA,
contre **23,1 %** pour le tiers des **anciens** (dernier achat entre le **31/01/2023** et le **13/03/2026**).
Politique vérifiable : les récents ont un poids économique immédiat (relance de panier), les anciens un
enjeu de réactivation borné par les **4,3 %** du §5.6.

## 13. Mini-projet de chapitre

**La note de fidélité de la cellule commerciale, 2 pages.** À partir du socle, produisez la note de
fidélité du parc client au 31/08/2026 : matrice de rétention, rétention pondérée à M+1, M+12 et M+24,
répartition RFM, et la question du client non identifié.

**Livrables et barème.**

| Critère | Ce qui est vérifié | Points |
|---|---|---|
| La matrice | 44 cohortes, taille en première colonne, cases non observables marquées | 6 |
| La rétention pondérée | trois anciennetés, avec l'effectif de chaque calcul | 5 |
| Le RFM | trois blocs égaux, départage explicite, deux segments nommés avec leurs bornes | 4 |
| La note de méthode | définition d'« actif », traitement du client 0, troncature à gauche déclarée | 3 |
| **Total** | | **18** |

## 14. Résumé du chapitre

Mesurer la fidélité, c'est d'abord **choisir une cohorte** : l'événement de départ est la **première
commande** — la date d'inscription du référentiel commence en **2016** et ne décrit pas le même univers. La
matrice de rétention se lit en **triangle** : **32** des **44** cohortes ont **12** mois de recul, **20** en
ont **24**, et les cases au-delà ne sont pas vides, elles sont impossibles. Trois lectures se ressemblent et
ne disent pas la même chose : la **récurrence** calendaire (**13,2 %**, **432** des **3 276** clients actifs
en juin 2025), la rétention d'**une** cohorte (**22,7 %**, sur **22** clients) et la rétention **pondérée**
(**15,8 %** à M+1, **17,2 %** à M+12, **18,2 %** à M+24) — seule la troisième est publiable. La courbe
**plate** décrit un noyau d'acheteurs réguliers, pas une fuite. Le **RFM** répartit les **23 497** clients en
trois blocs de **7 833**, **7 832** et **7 832**, place le tiers des récents à **48,7 %** du CA et fait
apparaître le segment **`133`** à **31,7 %** — qui contient le client **0**, **18,3 %** du CA à lui seul. Et
la leçon de reproductibilité se mesure : sans départage explicite, `NTILE` a fait varier le segment principal
entre **2 718** et **2 738** clients sur **15** exécutions.

## 15. À retenir

1. **Une cohorte se date sur l'événement mesuré.** L'inscription n'est pas la première commande.
2. **Un taux sans effectif ne se publie pas.** **22,7 %** et **15,8 %** ne sont pas comparables sans dire
   qu'ils portent sur **22** et **23 483** clients.
3. **On pondère, on ne moyenne pas.** `SUM(revenus) / SUM(effectif)`, jamais la moyenne des taux.
4. **Une courbe de rétention plate n'est pas une bonne nouvelle : c'est une description.** Le socle ne perd
   pas ses clients, il en garde un noyau d'environ **16 %**.
5. **Un classement sans départage n'est pas reproductible.** **3 316** clients à **8** tickets suffisent à
   rendre une frontière de tiers instable.
6. **Le client non identifié décide de la conclusion.** **18,3 %** du CA, **38,1 %** ou **24,2 %** selon
   qu'on le garde ou non.

> **À retenir.** Le chapitre tient dans une comparaison : **13,2 %** de récurrence calendaire contre
> **15,8 %** de rétention pondérée. Le premier chiffre est plus facile à produire, plus stable, et il ne
> répond pas à la question. Le second demande une cohorte, une pondération et une phrase de méthode — et
> c'est le seul qu'on peut défendre devant un comité.

> **À retenir.** Le socle raconte une entreprise dont **1 848** clients n'ont pas acheté depuis plus d'un an
> et qui ne représentent que **4,3 %** du chiffre d'affaires : la fidélité se décide sur des ordres de
> grandeur, et les ordres de grandeur s'obtiennent en pondérant, pas en devinant.

## 16. Évaluation formative

Répondez sans machine, puis vérifiez avec l'atelier (5 minutes) :

1. Combien de cohortes compte le socle, et quelle est la taille de la première et de la dernière ?
2. Pourquoi la matrice de rétention a-t-elle la forme d'un triangle ?
3. Que vaut la rétention pondérée à M+1, et que vaut la moyenne simple des taux sur les cohortes d'au moins
   100 clients ?
4. Pourquoi **22,7 %** n'est-il pas le bon chiffre à publier, alors qu'il est juste ?
5. Que mesure la lecture calendaire, si elle ne mesure pas la fidélité ?
6. En combien de blocs `NTILE(3)` découpe-t-il **23 497** clients, et de quelles tailles ?
7. Quelle part du CA porte le tiers des clients récents ?
8. Pourquoi faut-il une clé de départage dans un `NTILE`, et quel signe le montre sur ce socle ?
9. Combien de clients n'ont pas acheté depuis plus d'un an, et quelle part du CA représentent-ils ?
10. Quelle est la part du chiffre d'affaires du dixième supérieur des clients, avec et sans le client 0 ?

**Réponses.** 1. **44** cohortes ; **3 593** clients en janvier 2023, **3** en août 2026. 2. Parce que les
cohortes récentes n'ont pas le **recul** nécessaire : **32** cohortes atteignent M+12, **20** atteignent
M+24. 3. **15,8 %** pondérée contre **16,4 %** en moyenne simple. 4. Parce qu'il porte sur **22** clients :
l'effectif est trop faible pour qu'un taux soit stable. 5. La **récurrence** du fichier actif, toutes
cohortes mêlées — **13,2 %** de juin à juillet 2025. 6. Trois blocs : **7 833**, **7 832** et **7 832**
clients. 7. **48,7 %** du CA net. 8. Parce que **3 316** clients partagent exactement **8** tickets
(**14,1 %** du fichier) : sans clé explicite, le segment principal a varié de **2 718** à **2 738** clients
sur **15** exécutions. 9. **1 848** clients, **4,3 %** du CA net. 10. **38,1 %** tous clients confondus,
**24,2 %** hors client 0.
