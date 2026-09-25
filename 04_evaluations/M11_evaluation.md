# Évaluation M11 — « SQL avancé pour la BI »

**Module M11 · 30 h · niveau N3 → N4 · 7 chapitres.**
**Total : 70 points** — quiz **20** (seuil **14/20** §B.6), exercices à rendre **20** (dont **2** de
type E4, « correction d'erreurs »), auto-test SQL **10**, étude de cas **20** (seuil **12**). Durée
conseillée : 1 h pour le quiz, 2 h pour les exercices, 45 min pour l'auto-test, 1 h 30 pour l'étude de
cas.
**Matériel autorisé** : `03_exercices/dossier_M11/` (socle et connexion), `01_socle_donnees/`,
`01_socle_donnees/data/reference/chiffres_cites.json` (clés `m11_*`, `m11p_*`, `m11e_*`) et l'instrument
`tools/controle_sql_M11.py`. **Toute réponse chiffrée doit être mesurable** : un chiffre qui ne se
retrouve pas dans le socle ne rapporte pas de point.

> **Ce que cette évaluation vérifie.** Que vous savez **interroger** un socle de vente et **défendre**
> vos chiffres. Les questions ne demandent pas d'écrire des requêtes savantes : elles demandent de
> **dire** quelle construction répond à une question, de **prédire** la sortie d'une requête, de
> **diagnostiquer** un total faux, et de nommer ce qu'on manipule. Deux exercices (E4 et E5) portent sur
> des **requêtes erronées** : la justification pèse plus que la correction.

---

## A · Questions de récupération (non notées)

Répondez de mémoire, en une ligne chacune. Elles ne rapportent rien : elles disent ce qu'il faut relire.

1. Qu'est-ce qui distingue une fonction de fenêtre d'un `GROUP BY` sur le **nombre de lignes** rendues ?
2. Que font respectivement `RANK`, `DENSE_RANK` et `ROW_NUMBER` quand deux lignes sont à égalité ?
3. Qu'est-ce qu'un **cadre de fenêtre**, et que change `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` ?
4. Qu'est-ce qu'une **cohorte**, et sur quel événement se date-t-elle ?
5. Que fait `QUALIFY` que `WHERE` ne peut pas faire ?
6. Que change `UNNEST` au **grain** d'un jeu de lignes ?
7. Que lit un plan d'exécution, et dans quel sens se lit-il ?

---

## B · Quiz (20 questions · 20 points · 1 point par question)

Quatre familles de **5** questions : trouver la requête, prédire le résultat, diagnostiquer, nommer.

### Bloc 1 — Quelle requête pour quelle question (C01—C05) (Q1 à Q5)

**Q1.** La cellule demande « quelle part de l'année représente ce mois ? ». Quelle construction répond ?
a) un `GROUP BY` sur l'année ; b) `SUM(ca_mois) OVER (PARTITION BY annee)` ; c) `LAG(ca_mois) OVER
(ORDER BY mois)` ; d) `NTILE(12) OVER (ORDER BY mois)`.

**Q2.** « Le **3ᵉ** meilleur produit de chaque famille » : quelle construction donne la bonne réponse
**et** son rang ?
a) `GROUP BY famille HAVING COUNT(*) <= 3` ; b) `RANK() OVER (PARTITION BY famille ORDER BY ca DESC)`
puis un filtre `<= 3`, avec `id_produit` en clé de départage ; c) `LIMIT 3` ; d) `NTILE(3) OVER (PARTITION
BY famille)`.

**Q3.** « Les clients qui ont acheté en janvier et pas en février » : quelle construction ne se trompe
pas de sens ?
a) `INNER JOIN` sur le mois ; b) **`EXCEPT`** (ou une jointure externe gauche avec test de nullité) ;
c) `UNION ALL` ; d) `GROUP BY id_client` sans filtre de mois.

**Q4.** Pour dater la **cohorte** d'un client, quel événement prend-on ?
a) sa date d'inscription au référentiel ; b) la date de sa **première commande** dans les ventes ;
c) sa dernière commande ; d) la première commande de l'année en cours.

**Q5.** « Le chiffre d'affaires par quartier, **avec ses sous-totaux**, dans un seul résultat » :
a) trois requêtes à recoller ; b) `GROUP BY ROLLUP (quartier, famille)` ; c) `PIVOT` ; d) `UNION` des
détails et des totaux.

### Bloc 2 — Prédisez le résultat (Q6 à Q10)

**Q6.** Que rend `SELECT id_client, COUNT(*) FROM ventes WHERE est_retour = 0 GROUP BY 1 HAVING
COUNT(*) = 8` ?
a) **8** clients ; b) **3 316** clients ; c) **8** lignes de vente ; d) aucun client.

**Q7.** Une requête filtre d'abord le mois de **janvier 2023**, puis calcule
`SUM(montant_ttc) OVER (PARTITION BY annee_de_vente)`. Quelle part du chiffre d'affaires de 2023 le
rapport publiera-t-il pour ce mois ?
a) **8,3 %**, la vraie part ; b) **100,0 %**, parce que le filtre a été appliqué **avant** la fenêtre ;
c) **12,5 %** ; d) une erreur d'exécution.

**Q8.** Sur les clients classés par **nombre de tickets**, que valent `MAX(RANK())` et
`MAX(DENSE_RANK())` ?
a) **23 444** et **23 444** ; b) **23 444** et **21** ; c) **23 497** et **21 444** ; d) **21** et **21**.

**Q9.** Combien de lignes rend `GROUP BY ROLLUP (quartier, famille)` sur ce socle, et de quoi sont-elles
faites ?
a) **35** lignes, les couples ; b) **41** lignes : **35** couples, **5** sous-totaux de quartier et
**1** total général ; c) **47** lignes ; d) **44** lignes, une par mois.

**Q10.** Une moyenne mobile de **12** mois est calculée au **3ᵉ** mois du socle. Combien de lignes
portent réellement dans sa fenêtre ?
a) **12** ; b) **3** ; c) **0** ; d) **1**.

### Bloc 3 — Diagnostic (Q11 à Q15)

**Q11.** Un suivi des objectifs joint les ventes au référentiel des objectifs avec un `INNER JOIN` : le
magasin 4 perd deux mois. Combien manque-t-il de lignes, et combien de ventes sont-elles concernées ?
a) **2** couples, **93 749 490** FCFA ; b) **44** couples, **6 685 260 000** FCFA ; c) **2** couples,
**5 317 736 710** FCFA ; d) aucun, la jointure interne ne perd rien.

**Q12.** Un rapport compare 2026 (**8** mois) à 2025 (**12** mois) et annonce **−28,9 %**. Que faut-il
publier ?
a) **−28,9 %**, le chiffre est exact ; b) **+15,4 %**, la comparaison **à périmètre égal** ; c) **0 %** ;
d) **+18,8 %**, la croissance de 2024.

**Q13.** Un rapport de rétention publie **13,2 %** (**432** clients revenus sur **3 276** actifs), alors
qu'une lecture par cohorte donne **22,7 %** sur **22** clients. Quelle est la cause ?
a) une panne du moteur ; b) deux **définitions** différentes de la rétention — **calendaire** contre
**par cohorte** — et un dénominateur qui ne mesure pas la même population ;
c) un filtre de date oublié ; d) une erreur d'arrondi.

**Q14.** Un « meilleur produit par catégorie » écrit sur les libellés bruts du référentiel rend **46**
lignes ; sur les familles repliées, il en rend **21**. Que révèle l'écart ?
a) une erreur de la requête ; b) un **défaut de normalisation** du référentiel : **16** libellés bruts
pour **9** écritures et **7** familles réelles ; c) une différence de période ; d) une limite mémoire
du moteur.

**Q15.** Un rapport qui fait `SELECT *` sur la vue coûte **581** ms, la même requête sur trois colonnes
nommées **96** ms. Qu'annonce le plan **avant** toute mesure ?
a) rien d'utile ; b) la lecture de **18** colonnes contre **3** : le coût est dans la projection ;
c) qu'il faut un index ; d) que la vue est corrompue.

### Bloc 4 — Vocabulaire (Q16 à Q20)

**Q16.** Qu'appelle-t-on le **grain** d'un résultat ?
a) sa taille en octets ; b) ce que représente **une ligne** (un mois, un client, un ticket, un couple
quartier-famille) ; c) le nombre de colonnes ; d) la clé de tri.

**Q17.** Qu'appelle-t-on une **clé de départage**, et que se passe-t-il sans elle ?
a) la clé primaire de la table ; b) la seconde colonne de tri qui rend l'ordre **déterministe** : sans
elle, un classement peut changer de réponse entre deux exécutions ; c) un index ; d) un filtre.

**Q18.** Que fait `QUALIFY` ?
a) il filtre **avant** le calcul de la fenêtre ; b) il filtre **après** le calcul de la fenêtre, ce que
`WHERE` ne peut pas faire ; c) il trie ; d) il crée une vue.

**Q19.** Pourquoi un rapport coûte-t-il **142** ms sur la **vue** et **1** ms sur la table équivalente ?
a) la table est plus petite ; b) une **vue** ne stocke rien : elle **relit** sa source à chaque appel ;
c) la vue est mal écrite ; d) les deux requêtes ne sont pas les mêmes.

**Q20.** Que doit contenir la **note de méthode** d'un rapport de performance ?
a) seulement les temps mesurés ; b) les temps, la version du moteur, le protocole, la date, et ce qui
**n'a pas** été exécuté ; c) une capture d'écran ; d) la liste des index de la base.

---

## C · Exercices à rendre (20 points · 5 exercices, dont 2 de type E4)

### E1 — Le top 3 par famille, deux fois (niveau 3 · 3 points)

Produisez les **3** meilleurs produits de chaque famille du catalogue, une première fois sur les libellés
tels quels, une seconde fois après repliement (casse, espaces, accents, pluriel). Donnez le **nombre de
lignes** rendu par chaque version, et expliquez l'écart en deux phrases.

### E2 — Les deux périmètres de la concentration (niveau 3 · 3 points)

Calculez la part du chiffre d'affaires du dixième supérieur des clients, **avec** puis **sans** le client
non identifié. Écrivez la phrase qui doit accompagner la publication de chacune des deux valeurs.

### E3 — Le suivi des objectifs, trous compris (niveau 3 · 4 points)

Produisez le suivi mensuel 2024 du magasin 4 : réalisé, objectif, taux de réalisation, et une colonne
`etat` à trois valeurs (complet, objectif manquant, vente manquante). Le rapport doit faire apparaître
les mois sans objectif, avec le montant de ventes concerné — **aucune ligne ne doit disparaître**.

### E4 — « Ce rapport annonce un chiffre d'affaires net » (type E4 · niveau 4 · 5 points)

Voici la requête telle qu'elle a été livrée :

```sql
SELECT COUNT(*) AS lignes, ROUND(SUM(montant_ttc)) AS ca_net
FROM ventes;
```

Elle rend **240 000** lignes et **15 419 985 157** FCFA, publiés comme « chiffre d'affaires net ».

1. **Nommez l'erreur** en une phrase, sans écrire de requête.
2. **Corrigez** la requête et donnez les deux valeurs attendues.
3. **Mesurez l'écart** en FCFA et en pourcentage, et dites dans quel sens il joue.
4. Dites ce que ce total ferait à un rapport de suivi des objectifs, dont l'objectif cumulé est de
   **6 685 260 000** FCFA.
5. Écrivez la ligne d'en-tête qui aurait empêché l'erreur.

### E5 — « Ce classement change de réponse à chaque exécution » (type E4 · niveau 4 · 5 points)

Voici la requête telle qu'elle a été livrée :

```sql
SELECT id_client, NTILE(3) OVER (ORDER BY nb_tickets) AS segment
FROM (SELECT id_client, COUNT(*) AS nb_tickets FROM ventes GROUP BY 1) t;
```

Relancée **15** fois le **24/09/2026**, elle a compté **2 718**, **2 720**, **2 728** puis **2 738**
clients dans son segment principal — sans qu'aucune donnée ne change.

1. **Nommez la cause**, en citant le fait du socle qui la rend possible.
2. **Corrigez** la requête, et donnez la taille des trois tiers une fois l'ordre fixé.
3. Expliquez pourquoi ce défaut est **pire** qu'une requête lente.
4. Écrivez le **test de non-régression** qui aurait détecté le problème (valeur attendue, requête
   rejouée, verdict).

---

## D · Auto-test SQL (10 points · 18 requêtes · auto-corrigé)

L'instrument `tools/controle_sql_M11.py` rejoue **18** requêtes et confronte chaque résultat aux valeurs
publiées du module. Exécutez-le et **rendez sa sortie** (les **18** lignes de verdict et la ligne de
bilan).

**Barème :** **18** contrôles au vert = **10** points ; **14** à **17** = **7** points ; **10** à **13** =
**4** points ; moins de **10** = **0** point, avec un mot d'explication obligatoire sur les écarts.

> **Attention.** Ne modifiez **aucune** requête de l'instrument : un contrôle n'est un contrôle que s'il
> rejoue la requête **publiée**. Si un écart apparaît, cherchez d'abord ce qui a changé dans le socle ou
> dans le fichier publié — et notez-le, c'est la réponse attendue.

---

## E · Étude de cas — « 10 % des clients font-ils 60 % du CA ? » (20 points · seuil 12)

### La commande

La direction commerciale a entendu, en séminaire, que « **10 %** des clients font **60 %** du chiffre
d'affaires ». Elle vous demande de **vérifier la formule sur son propre fichier** et de lui dire, en une
page, si elle peut la reprendre à son compte.

### Les quatre productions attendues

1. **Le chiffre vrai** — la part du chiffre d'affaires portée par le dixième supérieur des clients, avec
   le **périmètre** annoncé (ventes nettes, période, magasins) et la **définition du décile** retenue.
2. **Le classement des clients, avant et après retrait du client non identifié** — ce que change le
   retrait, et le mot qui l'explique.
3. **La conclusion tenable** — trois lignes pour la direction, chiffres compris, sans formule recopiée
   sans vérification.
4. **La question suivante à poser** — celle que votre rapport ne tranche pas, et que la direction devra
   poser à son tour.

### Le résultat attendu (à retrouver, pas à recopier)

Sur ce socle, la réponse est **non**, et elle est stable : le dixième supérieur pèse **38,1 %** du
chiffre d'affaires net, **24,2 %** une fois le client **0** écarté, **51,0 %** pour le top **20 %**,
**30,0 %** pour le top **5 %** et **21,6 %** pour le top **1 %**.

> **Attention.** Le résultat dépend de la **définition** du dixième : `NTILE(100) <= 1` retient **2 350**
> clients et donne **38,1 %** ; un `ROW_NUMBER()` sur **10 %** du fichier en retient **2 349** et donne
> **38,0 %**. Un rapport qui publie un pourcentage sans publier sa définition de décile produit un
> chiffre que personne ne peut reproduire.

### Barème de l'étude de cas

| Critère | Points |
|---|---|
| **1.** Le chiffre vrai : périmètre annoncé, définition du décile écrite, valeur exacte | 5 |
| **2.** Le classement avant / après retrait du client **0**, et le mot qui l'explique | 5 |
| **3.** La conclusion tenable : trois lignes, utilisables, sans surinterprétation | 5 |
| **4.** La question suivante, formulée comme une question à laquelle on peut répondre | 5 |
| **Total** | **20** |

---

## Correction détaillée

### A · Réponses de récupération

1. Une fenêtre **conserve** les lignes (elle ajoute des colonnes) ; `GROUP BY` **réduit** la table aux
   groupes.
2. `RANK` laisse des trous après une égalité, `DENSE_RANK` n'en laisse pas, `ROW_NUMBER` attribue des
   rangs uniques — d'où la nécessité d'une clé de départage.
3. Le cadre est la portion de la partition prise en compte autour de la ligne courante ; `2 PRECEDING`
   retient trois lignes et ne s'étend pas au-delà des lignes existantes.
4. Un groupe de clients partagé par un événement daté — ici la **première commande**, et non la date
   d'inscription du référentiel.
5. `QUALIFY` filtre **après** le calcul de la fenêtre : il permet de garder le rang 1 par groupe dans la
   même requête.
6. `UNNEST` passe d'une ligne « ticket » à une ligne « article de ticket » : le grain change, et
   `COUNT(*)` ne compte plus la même chose.
7. Le plan décrit les opérateurs et les colonnes lues avant l'exécution ; il se lit **de bas en haut**.

### B · Corrigé du quiz (1 point par question)

| Question | Réponse | Pourquoi |
|---|---|---|
| Q1 | **b** | La part se calcule par une fenêtre **partitionnée par année** (C01). |
| Q2 | **b** | `RANK` partitionné, filtré à **3**, avec `id_produit` en départage (C02). |
| Q3 | **b** | `EXCEPT` (ou jointure externe gauche + nullité) : le `INNER JOIN` répond à une autre question (C05). |
| Q4 | **b** | La cohorte se date sur la **première commande** (C04). |
| Q5 | **b** | `ROLLUP` produit les **41** lignes en une requête (C05). |
| Q6 | **b** | **3 316** clients partagent exactement **8** tickets (**14,1 %**). |
| Q7 | **b** | Le filtre avant la fenêtre ne laisse qu'une ligne : **100,0 %** au lieu de **8,3 %** (C01). |
| Q8 | **b** | **23 444** en `RANK` contre **21** en `DENSE_RANK` (C02). |
| Q9 | **b** | **35** couples + **5** sous-totaux + **1** total général (C05). |
| Q10 | **b** | Au 3ᵉ mois, la fenêtre ne porte que sur **3** lignes (C03). |
| Q11 | **a** | **2** couples manquants (magasin 4, 2024-02 et 2024-03) pour **93 749 490** FCFA (C03). |
| Q12 | **b** | À périmètre égal : **+15,4 %** (C03). |
| Q13 | **b** | Rétention calendaire contre rétention par cohorte : deux définitions, deux populations (C04). |
| Q14 | **b** | **16** libellés bruts, **9** écritures, **7** familles : **46** lignes contre **21** (C05). |
| Q15 | **b** | Le plan annonce **18** colonnes contre **3** : le coût se lit avant l'exécution (C06). |
| Q16 | **b** | Le grain est ce que représente une ligne (C01, C05). |
| Q17 | **b** | La clé de départage rend l'ordre déterministe ; sans elle, le rapport change (C02, C07). |
| Q18 | **b** | `QUALIFY` filtre après la fenêtre (C05). |
| Q19 | **b** | Une vue relit sa source : **142** ms contre **1** ms (C06). |
| Q20 | **b** | Temps, moteur, protocole, date, et ce qui n'a pas été exécuté (C06, C07). |

### C · Corrigé des exercices à rendre

**E1.** Les libellés bruts rendent **46** lignes pour **16** catégories ; après repliement des graphies,
le même top 3 rend **21** lignes pour **7** familles. L'écart est la trace exacte du défaut de
normalisation du référentiel, pas un problème de requête.

**E2.** Avec le client **0** : **38,1 %** ; sans lui : **24,2 %**. Les deux phrases attendues : « le
dixième supérieur des **2 350** clients pèse **38,1 %** du chiffre d'affaires net » et « hors client non
identifié, ce dixième pèse **24,2 %** — l'écart est porté par un seul identifiant, non rattaché à un
client du référentiel ».

**E3.** Structure `FULL OUTER JOIN` avec `CASE` à trois états ; les **2** lignes sans objectif portent
**42 514 372** et **51 235 118** FCFA, soit **93 749 490** FCFA de réalisé sans référence. Le taux de
réalisation y vaut `NULL` — ni **0**, ni 100 %.

**E4 — les cinq attendus.** 1. La requête ne filtre pas les retours : elle compte les **2 809** lignes
de retour dans un total annoncé « net ». 2. Correction : `WHERE est_retour = 0` → **237 191** lignes et
**15 595 154 955** FCFA. 3. Écart : **−175 169 798** FCFA, soit **−1,1 %** — le total faux est **plus
bas** que le vrai, puisque les retours sont négatifs, alors que le nombre de lignes est **plus haut** de
**1,2 %** (**240 000** comptées contre **237 191**) : l'erreur se lit à l'envers selon l'indicateur.
4. Face à un objectif cumulé de **6 685 260 000** FCFA, le total faux afficherait **230,7 %** au lieu de
**233,3 %** : l'erreur reste invisible dans le vert de l'indicateur. 5. En-tête : « Hypothèses : ventes
**nettes** de retours (`est_retour = 0`) ; les **2 809** lignes de retour sont exclues, jamais
sommées. »

**E5 — les quatre attendus.** 1. L'`ORDER BY` n'a **pas** de clé de départage : **3 316** clients
partagent exactement **8** tickets (**14,1 %** du fichier), et le moteur est libre de placer les ex æquo
comme il veut. 2. Correction : `ORDER BY nb_tickets, id_client` → les trois tiers comptent **7 833**,
**7 832** et **7 832** clients, stables d'une exécution à l'autre. 3. Une requête lente se corrige et se
mesure ; une requête **instable** publie des chiffres contradictoires d'un jour à l'autre, et le rapport
perd sa crédibilité avant qu'on ait trouvé pourquoi. 4. Le test attendu rejoue **à l'identique** la
requête corrigée et compare la taille du premier tiers à **7 833** : tout autre résultat fait échouer le
contrôle et sort en code non nul.

### D · Corrigé de l'auto-test

La sortie attendue comporte **18** lignes de verdict au vert, du comptage des lignes (**240 000**,
**237 191** hors retours) au ratio de saison (**1,65**), et se termine par
« **18** controles sur 18 : OK — le socle et le fichier publie disent la meme chose. »

### E · Corrigé de l'étude de cas — les quatre attendus

1. **Le chiffre vrai.** **38,1 %** du chiffre d'affaires net, périmètre : ventes nettes (retours exclus),
   01/01/2023 au 31/08/2026, **5** magasins, client **0** **inclus** ; définition du décile :
   `NTILE(100) <= 1`, soit **2 350** clients (l'autre définition usuelle, un `ROW_NUMBER` sur **10 %**
   du fichier, retient **2 349** clients et donne **38,0 %**).
2. **Le classement, avant et après.** Le client **0** pèse **2 852 612 447** FCFA — **18,3 %** du
   chiffre d'affaires — sur **42 658** lignes et **38 984** tickets, sans exister dans le référentiel.
   Il occupe donc toujours la première place d'un classement par montant : une fois écarté, le dixième
   supérieur tombe à **24,2 %**, et le classement des têtes change intégralement. Le mot à employer est
   **périmètre** : retirer le client **0** retire **18,3 %** du chiffre d'affaires, c'est un choix, et
   il s'écrit.
3. **La conclusion tenable.** Trois lignes, du type : « sur notre fichier, les **10 %** de clients les
   plus gros pèsent **38 %** du chiffre d'affaires, et **24 %** une fois le client non identifié écarté —
   la formule des **60 %** ne s'applique pas ici ; la concentration est réelle mais plus faible, et le
   top **20 %** pèse **51,0 %**. »
4. **La question suivante.** « Quelle part du chiffre d'affaires de chaque **cohorte** est portée par
   des clients non identifiés ? » Tant que le client **0** représente **18,3 %** du chiffre d'affaires,
   toute lecture de la rétention se fait sur un cinquième du total qu'on ne sait pas attribuer — c'est
   la question qui manque aux **12** rapports du projet, et elle se pose avec les outils du chapitre C04.

---

## Barème global et seuils

| Partie | Points | Seuil |
|---|---|---|
| B · Quiz (**20** questions) | **20** | **14/20** (§B.6) |
| C · Exercices à rendre (**5**, dont **2** E4) | **20** | — |
| D · Auto-test SQL (**18** requêtes) | **10** | — |
| E · Étude de cas | **20** | **12/20** (§B.6) |
| **Total** | **70** | **49/70** pour la validation du module |

**Épreuve de palier.** Cette évaluation prépare l'épreuve **P4** de la phase 4 (§B.6) : les quatre
compétences qu'elle mesure — écrire une requête qui répond à une question posée, prédire ce qu'une
fenêtre va changer, diagnostiquer un total faux, publier un taux avec son effectif et sa définition —
sont celles que l'épreuve de palier reprend, sur un socle différent.
