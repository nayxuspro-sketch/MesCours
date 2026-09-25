# Projet M11.P — « Les 12 rapports SQL de la cellule commerciale »

**Module M11 · projet noté sur 20 · seuil 13 · durée imposée 4 h (chronomètre en marche) ·
rendu : 4 livrables — P1 les **12** requêtes (8 points), P2 le jeu de tests (5 points), P3 la note de
lecture (4 points), P4 la fiche de reprise (3 points).**

> **Ce que le projet évalue.** Non pas « la requête la plus savante », mais la **bibliothèque de
> rapports** : douze requêtes autonomes, **versionnées**, **testées** et **commentées en français**,
> chacune répondant à une question écrite. Vous recevez la commande de la cellule commerciale et le
> socle du module : **240 000** lignes de vente, **237 191** hors retours, **145 212** tickets,
> **23 497** clients, **5** magasins, **44** mois. La règle du projet est celle du module : **un
> rapport dont le total diffère d'un rapport à l'autre est rejeté**, même si chaque requête
> « fonctionne » — et un rapport que son lecteur ne peut pas rejouer ne vaut rien.

---

## 1. Énoncé

### La commande

La cellule commerciale d'une enseigne de quincaillerie (**5** magasins, **44** mois, **240 000**
lignes) commande sa **bibliothèque de rapports** : **12** requêtes autonomes, chacune répondant à une
question qu'elle s'est posée cette année. Elle les veut **en français**, **datées**, **testées**, et
livrées avec leur **mode d'emploi** — pas un dossier de requêtes, un **outil de travail**.

### Le matériel

| Élément | Chemin | Ce que c'est |
|---|---|---|
| Le socle | `03_exercices/dossier_M11/socle_m11.sql` | les **5** tables de référence et les **2** vues de ventes (**3 595** octets) |
| La connexion | `03_exercices/dossier_M11/connexion.py` | `ouvrir(materialiser=False)` — la matérialisation en mémoire pour les mesures |
| Les mesures de performance | `03_exercices/dossier_M11/PERF_M11.json` | les temps **gelés** du chapitre C06 (**24/09/2026**, médianes de **5** exécutions) |
| Le contrôle automatique | `tools/controle_sql_M11.py` | **18** requêtes rejouées et confrontées au fichier publié — le calque de votre livrable P2 |
| Les valeurs publiées | `01_socle_donnees/data/reference/chiffres_cites.json` | clés `m11_*`, `m11p_*`, `m11e_*` : **301** clés pour le module |
| Les 7 chapitres | `02_modules/M11_C01…C07` | fenêtres, rangs, temps, cohortes, requêtes avancées, plans, style et tests |

### Les six totaux de contrôle

Ces six nombres se recalculent depuis le socle — ils ne se recopient pas. Un rapport qui publie un
total différent doit **dire pourquoi** (périmètre plus étroit, période partielle, client non identifié
exclu) : c'est la seule tolérance admise, et elle s'écrit dans l'en-tête.

| Contrôle | Valeur attendue |
|---|---|
| Chiffre d'affaires net (retours exclus) | **15 595 154 955** FCFA |
| Lignes de vente (retours exclus) | **237 191** |
| Tickets de vente | **145 212** |
| Clients identifiés dans les ventes | **23 497** |
| Magasins | **5** |
| Mois couverts | **44** |

---

## 2. Les 12 questions métier (le catalogue imposé)

Chaque rapport répond à **une** question, citée telle quelle dans son en-tête. Le chapitre indiqué est
celui qui fournit la méthode ; la colonne « sortie » dit ce que le rapport doit **contenir**, pas la
façon de l'obtenir.

| Code | Question de la cellule | Chap. | Sortie attendue |
|---|---|---|---|
| **R01** | Combien avons-nous vendu chaque mois, et où en sommes-nous cette année ? | C01, C02 | mois, CA, cumul, part du mois dans son année |
| **R02** | Quels magasins vendent le plus — et lesquels ont le plus gros panier ? | C01, C02 | deux classements côte à côte, chacun avec son rang |
| **R03** | Quels sont nos 3 meilleurs produits par famille ? | C02 | 3 lignes par famille, rang, part dans la famille |
| **R04** | Quelle part du chiffre d'affaires font nos plus gros clients ? | C01, C04 | parts cumulées, top 1 %, top 5 %, top 10 %, top 20 % |
| **R05** | L'activité progresse-t-elle, à périmètre comparable ? | C03 | année sur année à mois constants, moyenne des variations |
| **R06** | La tendance de fond monte-t-elle ? | C03 | moyennes mobiles de 3 et 12 mois, **avec** leur compteur de fenêtre |
| **R07** | Tenons-nous nos objectifs ? | C03 | réalisé, objectif, taux — **trous compris** et déclarés |
| **R08** | Quel jour de la semaine travaillons-nous le mieux ? | C03 | CA par jour de vente, écart entre le meilleur et le pire |
| **R09** | Nos clients reviennent-ils ? | C04 | rétention pondérée à M+1, M+3, M+12, avec les effectifs |
| **R10** | Quels clients appeler en priorité, et pour quoi ? | C04 | segments RFM, effectif, part du CA, plage de récence |
| **R11** | Où vend-on quoi ? | C05 | tableau croisé quartier × famille **avec sous-totaux** |
| **R12** | Nos deux socles racontent-ils la même histoire ? | C07 | comparaison documentée des deux socles, écarts **expliqués** |

**Douze questions, douze rapports, une seule vérité de total** : les **12** rapports publient le même
chiffre d'affaires net quand ils parlent de la même période — **15 595 154 955** FCFA sur le socle
complet, ou un sous-ensemble dont le périmètre est écrit noir sur blanc.

### Le format d'en-tête, imposé

Chaque rapport s'ouvre sur ces six lignes — c'est ce qui distingue une bibliothèque d'un fichier de
brouillons :

```
-- Rxx — <question de la cellule, recopiée telle quelle>
-- Hypothèses : <ce qu'on suppose : retours exclus, client 0 inclus, période complète…>
-- Grain : <une ligne = un mois / un client / un couple quartier-famille>
-- Source : <socle M11, vue ventes, référence produit>
-- Total de contrôle : <le nombre que le rapport doit rendre>
-- Date : <le jour de rédaction>
```

---

## 3. Les 4 livrables

### P1 — Les 12 requêtes (8 points)

Une requête par question, dans l'ordre R01 → R12, chacune avec **son en-tête complet**, un
`ORDER BY` **explicite** — avec sa clé de départage quand deux lignes peuvent être à égalité —, et son
**total de contrôle**.

Ce qui est vérifié à la correction :

- R02 : les deux classements sont donnés avec leur **rang** ; le rapport signale que l'ordre n'est pas
  le même (**Kaya** a le plus gros panier, **Ouagadougou** le plus gros chiffre d'affaires).
- R03 : le classement porte sur les **7** familles réelles, pas sur les **16** libellés du
  référentiel ; le rapport publie les **deux** comptes (**46** lignes contre **21**).
- R04 : la part du top 10 % est publiée **avec** et **sans** le client non identifié, et la définition
  du décile est écrite.
- R05 : aucune comparaison entre périodes de longueurs différentes ; la période partielle est annoncée.
- R06 : chaque moyenne mobile porte le nombre de lignes de sa fenêtre ; les douze premiers mois sont
  marqués comme **non comparables**.
- R07 : les **2** couples magasin-mois sans objectif apparaissent dans le rapport, avec un état
  explicite et **93 749 490** FCFA de ventes sans référence.
- R09 : la rétention est **pondérée** par la taille des cohortes ; le tableau porte les effectifs.
- R10 : le traitement du client **0** est écrit ; tous les classements sont départagés.
- R11 : les sous-totaux sont produits dans la **même** requête (`ROLLUP` ou `GROUPING SETS`), et le
  total général égale le chiffre d'affaires net.

### P2 — Le jeu de tests (5 points)

Chaque requête est livrée avec **au moins un test de non-régression**, dans l'esprit de
`tools/controle_sql_M11.py` : une valeur attendue (le total, le nombre de lignes, une valeur extrême),
la requête rejouée **à l'identique**, le verdict, et un **code de sortie** utilisable en chaîne.

Ce qui est vérifié :

- **au moins un** test par rapport, soit **12** au minimum, plus la sortie de l'instrument du module
  (**18** lignes) publiée ;
- les tests **recopient** la requête du rapport caractère pour caractère : la plus petite réécriture
  change la réponse — un classement des clients par nombre de tickets rend **23 444** en ordre
  décroissant et **23 497** en ordre croissant ;
- un écart produit un **code de sortie non nul** : un test qui se contente d'afficher « échec » ne
  protège rien.

> **Attention.** Un test qui « améliore » la requête qu'il rejoue ne teste plus le chiffre publié : il
> fabrique une alerte, ou pire, il valide une valeur qui n'apparaît nulle part dans le rapport.

### P3 — La note de lecture (4 points · 2 pages)

Deux pages, pour la personne qui n'écrira jamais une ligne de SQL : ce que les **12** rapports disent
**ensemble**, et les **3** précautions à connaître avant de citer un chiffre :

1. le client **0** — **18,3 %** du chiffre d'affaires, absent du référentiel, premier de tout
   classement ;
2. les **retours** — **2 809** lignes négatives : un total « net » qui les compte n'est pas un total ;
3. les **grains** — ligne, ticket, client : quatre nombres pour la même question (**146 161** tickets
   au total, **145 212** avec au moins une vente, **2 797** qui portent au moins un retour, dont
   **1 848** mixtes et **949** uniquement des retours).

La note se termine par **la question à laquelle les 12 rapports ne répondent pas** — par exemple
pourquoi un client achète, ou ce qui se passera au prochain trimestre : un rapport décrit, il
n'explique pas.

### P4 — La fiche de reprise (3 points)

Un pair — qui n'a pas écrit les rapports — en reprend **3**, exécute leurs tests, et note **ce qui
manque** pour qu'il puisse travailler sans vous : hypothèse non écrite, colonne ambiguë, test absent,
nom de table supposé connu. La fiche publiée est la **sienne**, pas la vôtre ; votre annotation de son
retour tient en trois lignes.

> **Conseil professionnel.** Écrivez l'en-tête **avant** la requête. Tant que la ligne « Hypothèses »
> n'est pas rédigée, la requête n'est pas finie : c'est en l'écrivant qu'on découvre qu'on hésite entre
> ventes brutes et ventes nettes — et cette hésitation est exactement ce qui fait publier deux chiffres
> différents du même indicateur.

---

## 4. Barème

| Livrable | Critère | Points |
|---|---|---|
| **P1** · les **12** requêtes | **12** requêtes rendues, dans l'ordre R01 → R12 | 4 |
| | Les **12** en-têtes complets (question, hypothèses, grain, source, total, date) | 2 |
| | `ORDER BY` explicite et **clé de départage** partout où une égalité est possible | 1 |
| | Total de contrôle présent et exact | 1 |
| **P2** · le jeu de tests | Au moins **1** test par rapport (**12** au minimum) | 2 |
| | Requêtes rejouées **à l'identique** (aucune réécriture) | 1,5 |
| | Sortie de `tools/controle_sql_M11.py` publiée (**18** lignes) | 1 |
| | Code de sortie non nul en cas d'écart | 0,5 |
| **P3** · la note de lecture | Les **3** précautions (client **0**, retours, grains), chacune chiffrée | 2 |
| | Ce que les **12** rapports disent **ensemble**, en une page | 1 |
| | La question à laquelle ils ne répondent pas | 1 |
| **P4** · la fiche de reprise | Les **3** rapports repris par un pair, tests exécutés | 2 |
| | Le compte rendu de ce qui manque, et votre réponse en trois lignes | 1 |
| | **Total** | **20** |

**Seuil de validation : 13/20.** Un livrable non rendu vaut zéro : il n'y a pas de points de présence.

---

## 5. Ce qui fait rejeter un livrable

1. **Un total qui change d'un rapport à l'autre** sans explication de périmètre : la règle du projet,
   et la seule faute éliminatoire.
2. **Un classement sans clé de départage.** **3 316** clients partagent exactement **8** tickets
   (**14,1 %** du fichier) : la frontière des tiers a compté de **2 718** à **2 738** clients selon
   l'exécution, sans qu'aucune donnée n'ait changé.
3. **Une jointure interne vers une table de référence** qui supprime en silence les **2** mois sans
   objectif du magasin 4.
4. **Une comparaison de périodes de longueurs différentes** présentée comme une évolution : 2026
   (**8** mois) contre 2025 (**12** mois) donne **−28,9 %** ; à périmètre égal, **+15,4 %**.
5. **Un rapport dont les chiffres ne sont pas dans le fichier publié** : toute valeur citée se retrouve
   dans `chiffres_cites.json`, ou n'est pas publiée.
6. **Un test qui réécrit la requête qu'il contrôle** : ce n'est plus le chiffre du rapport qui est
   vérifié.
7. **Un moteur annoncé sans l'être** : PostgreSQL et SQL Server sont **cités** dans le module, jamais
   exécutés ; un rapport qui publie une sortie « PostgreSQL » non produite est faux.

---

## 6. Déroulé conseillé (4 séances, environ 8 h)

| Séance | Objet | Livrable visé |
|---|---|---|
| 1 | Lire la commande, rejouer le socle, recalculer les **6** totaux, écrire les en-têtes des **12** rapports | P1 (en-têtes) |
| 2 | Écrire R01 → R06, avec sorties réelles et totaux de contrôle | P1 |
| 3 | Écrire R07 → R12 (trous d'objectif, cohortes pondérées, RFM départagé, tableau croisé, contrôle croisé) | P1 |
| 4 | Le jeu de tests, la note de lecture, l'échange de relecture avec un pair | P2, P3, P4 |

---

## 7. Comment vous corriger vous-même

1. **Les totaux** : `python3 tools/controle_sql_M11.py` doit rendre **18** lignes au vert sur le socle
   livré ; vos **12** tests s'ajoutent à la suite, dans le même format.
2. **Les sorties** : recopiez les sorties réelles de votre atelier, jamais une sortie approximative ;
   un tableau publié avec des valeurs arrondies « à la main » perd le contrôle.
3. **La relecture croisée** : échangez votre P4 avec un camarade. Le test est simple : peut-il
   **rejouer** trois de vos rapports et retrouver vos chiffres sans vous demander d'explication ? Si
   oui, la bibliothèque est bonne — c'est la définition du projet.

> **Le critère de réussite du projet.** Un lecteur qui n'a jamais vu le socle ouvre votre dossier, lit
> l'en-tête d'un rapport, exécute la requête, obtient votre chiffre, lance le test qui le vérifie, et
> comprend en une phrase à quoi le rapport sert. Douze fois de suite.
