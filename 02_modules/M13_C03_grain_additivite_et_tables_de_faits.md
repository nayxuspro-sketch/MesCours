# Module M13.C03 — Grain, additivité et tables de faits

![Le grain et l'explosion : trois grains du fil rouge, la jointure faite sur la bonne clé, et les deux façons de fabriquer un faux total sans qu'aucune requête ne se plaigne (production : `tools/figures_M13.py`)](../figures/M13_C03_grain_et_explosion.svg)

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous savez :

1. **dire ce que porte une ligne** d'une table de faits, en une phrase qui ne laisse aucune place au
   doute — c'est le **grain**, et il s'écrit au-dessus de la table, pas dans la tête de celui qui l'a
   créée ;
2. **prouver un grain** au lieu de le déclarer : compter les lignes, compter les valeurs distinctes
   de la clé, et vérifier que les deux nombres coïncident — sur les **7** tables de faits du fil
   rouge, dont les **7** grains vont de la ligne de ticket à l'objectif mensuel par magasin ;
3. **classer une mesure** dans l'un des trois régimes d'additivité : ce qui s'additionne dans tous
   les sens (additif), ce qui s'additionne dans l'espace mais jamais dans le temps (semi-additif),
   et ce qui ne s'additionne pas du tout (non additif) ;
4. **reconnaître les trois façons de fabriquer un faux total** — joindre sur une clé trop large, sur
   une clé trop fine, ou mélanger deux grains dans la même addition — et **mesurer** chacune sur le
   socle, jusqu'au facteur **44,0** et au chiffre d'affaires multiplié par **44** ;
5. **écrire le contrôle négatif** qui disculpe la jointure quand c'est la clé qui est en cause :
   même requête, mauvaise clé contre bonne clé, facteur **44,0** contre facteur **1,0**.

---

## 2. Pourquoi cette notion est importante

Le chapitre C02 a nettoyé le tableau de départ : plus de valeurs multiples dans un champ, plus de
dépendance à une partie de clé. Le modèle est propre. Il n'est pas encore **juste**.

La différence entre propre et juste tient à une seule question : **quand vous lisez un total, savez-vous
ce que chaque ligne comptait ?** Le socle du fil rouge contient **240 000** lignes de ventes, mais aussi
**9 000** commandes, **9 000** encaissements, **6 776** lignes de stock mensuel, **2 428** ruptures, **264**
bilans logistiques et **218** objectifs. Ces tables vivent ensemble, partagent les mêmes clés, répondent
aux mêmes filtres, et **ne se comptent pas de la même façon**.

Toutes les erreurs de ce chapitre ont une propriété commune, et c'est ce qui les rend dangereuses :
**elles s'exécutent sans erreur**. Aucune ne lève d'exception, aucune ne renvoie zéro ligne, aucune ne
paraît suspecte. La requête fautive rend **10 436 404** lignes et **686 186 818 020** FCFA, quand le
chiffre juste est **15 595 154 955** FCFA : deux nombres qui ont la même forme, le même séparateur de
milliers, la même unité — et un seul des deux est le chiffre d'affaires de Sahel Distribution.

> **Dans les faits.** Le défaut décrit ici n'est pas un cas d'école. La mesure la plus parlante du
> socle est le **facteur 44,0** : un magasin possède **44** mois d'historique logistique, et une
> jointure sur le seul `id_magasin` multiplie donc chaque vente par **44** — les **237 191** ventes
> nettes deviennent **10 436 404** lignes. Un analyste qui découvre cela en réunion ne découvre pas
> une erreur de méthode : il découvre que son tableau publié la semaine dernière portait un chiffre
> d'affaires **44** fois trop gros, et que personne ne l'a vu.

Ce chapitre installe donc la grammaire de tout le reste du module : C04 construira l'étoile et les
dimensions conformes **sur** ces grains, C05 ajoutera les variantes quand l'étoile ne suffit plus, C06
traitera le temps du modèle, et C07 vérifiera l'ensemble par une grille de revue. Rien de ce qui suit
ne fonctionne si le grain n'est pas écrit, prouvé et respecté.

---

## 3. Explication simple — l'eau, la photo et la température

Trois images suffisent pour tenir les trois régimes d'additivité.

**L'eau.** Versez un litre dans un seau, puis un autre : vous avez deux litres. Le volume s'additionne
dans le temps comme dans l'espace, il se recompte à l'identique après avoir été découpé en seaux plus
petits, et le total du mois est la somme des totaux des jours. C'est une mesure **additive**, et le
chiffre d'affaires en fait partie : **44** totaux mensuels se re-somment exactement au total du modèle,
avec un facteur de **1,0**.

**La photo.** Prenez une photo du seau chaque jour. Additionnez les **44** photos : vous n'obtenez pas
**44** seaux, vous obtenez une pile de photos. Une photo de stock est un **instantané** : elle
s'additionne dans l'espace (six magasins font bien un stock de réseau) mais jamais dans le temps. Le
socle le prouve : les **44** mois d'instantanés se somment à **2 034 733** unités, soit **44** fois le
stock d'un mois (**46 244** unités) — un nombre parfaitement crédible, et qui ne veut rien dire. La
bonne lecture d'un instantané sur une période est **le dernier instantané** (**45 882** unités sur le
dernier mois du socle), ou une moyenne, jamais une somme.

**La température.** Deux pièces à 20 degrés ne font pas une pièce à 40 degrés. Un taux, une
pourcentage, une moyenne, une couverture en mois : ces mesures sont **non additives**, elles ne
s'additionnent ni dans l'espace ni dans le temps. Le plan d'objectifs du fil rouge en donne la
démonstration : ses **218** taux de marge se somment à **4 248,7 %**, quand leur moyenne vaut **19,5 %**
— et ni l'un ni l'autre n'est la marge du réseau, qui se recalcule à partir de deux montants.

---

## 4. Vocabulaire essentiel

| Terme | Définition | Sur le fil rouge |
|---|---|---|
| **Grain** | ce que porte **une** ligne d'une table de faits | une ligne de ticket, ou un produit par mois |
| **Table de faits** | table qui porte les mesures d'un processus, à un grain unique | `fait_ventes`, **240 000** lignes |
| **Table de dimensions** | table qui décrit les objets du fait (qui, quoi, où) | `dim_client`, `dim_produit`, `dim_magasin` |
| **Clé du grain** | la ou les colonnes qui identifient une ligne de faits | `id_vente` ; `id_produit` + `mois` |
| **Mesure additive** | s'additionne dans l'espace **et** dans le temps | `montant_ttc` |
| **Mesure semi-additive** | s'additionne dans l'espace, pas dans le temps | `stock_moyen_unites` (instantané) |
| **Mesure non additive** | ne s'additionne ni dans l'espace ni dans le temps | `marge_objectif_pct`, `couverture_mois` |
| **Explosion en lignes** | une jointure qui multiplie les lignes d'une table | **237 191** ventes deviennent **10 436 404** |
| **Filtre silencieux** | une jointure qui fait disparaître des lignes sans le dire | CA à **0,36** du chiffre juste |
| **Contrôle négatif** | requête qui doit rendre le même total, pour disculper la jointure | ventes jointes au stock : facteur **1,0** |
| **Agréger** | réduire des lignes à un total, une moyenne, un compte | `GROUP BY` sur `dim_magasin` |
| **Fiche de grain** | la ligne de documentation qui déclare le grain et l'additivité | livrable du mini-projet |

> **Définition.** Le **grain** d'une table de faits est la description, en langage courant, de ce que
> représente une ligne : « une ligne de ticket », « une commande », « un produit par magasin et par
> mois ». Le grain se déclare **avant** l'écriture de la table, s'écrit **dans le modèle**, et se
> prouve **après** le chargement.

> **Définition.** Une mesure est **additive** quand la somme des parties égale le tout, quel que soit
> le découpage. Elle est **semi-additive** quand ce n'est vrai que sur certaines dimensions (le stock,
> additif entre magasins, ne l'est pas entre mois). Elle est **non additive** quand aucune somme n'a
> de sens — un taux, un ratio, une moyenne.

> **Définition.** L'**explosion en lignes** est la multiplication du nombre de lignes d'une table par
> une jointure dont la clé est trop large : chaque ligne de gauche rencontre plusieurs lignes de
> droite, et le total de gauche est répété autant de fois.

> **Définition.** Le **contrôle négatif** est une requête écrite pour **ne rien changer** : on
> volontairement la même jointure, avec la bonne clé, et l'on vérifie que le total est identique. Il
> ne prouve pas que la requête est utile ; il prouve que la jointure n'est pas la coupable.

> **Définition.** La **fiche de grain** est le document d'une page qui déclare, pour chaque table de
> faits : son grain, sa clé, son unité de comptage, son régime d'additivité, les agrégations
> autorisées et interdites, et la requête qui vérifie l'unicité de la clé.

---

## 5. Cours approfondi

### 5.1 Ce que porte une ligne : le grain se dit en une phrase

Un modèle se lit table par table, et chaque table de faits commence par une phrase. Pas un schéma,
pas un diagramme : une phrase, au présent, qui dit ce qu'une ligne représente.

- `fait_ventes` : « une ligne de ticket vendue ».
- `fait_commandes` : « une commande passée ».
- `fait_encaissements` : « une facture encaissée ».
- `fait_stock_mensuel` : « un produit, un mois, un instantané de stock ».
- `fait_ruptures` : « un produit, un magasin, un mois, un nombre de jours de rupture ».
- `fait_logistique` : « un magasin, un mois, un coût de livraison ».
- `fait_objectifs` : « un magasin, un mois, un objectif de chiffre d'affaires ».

Ces sept phrases ne sont pas interchangeables, et c'est tout l'objet du chapitre. Les **7** tables
portent **267 686** lignes en tout, mais ce nombre ne veut rien dire en lui-même : il additionne des
tickets et des instantanés, des commandes et des objectifs. Une table de faits n'est pas « un tableau
de chiffres » ; c'est **un processus**, observé à un grain précis, avec ses clés et ses mesures.

### 5.2 Sept grains, un facteur 1 101

Le grain le plus fin du modèle est la ligne de ticket : **240 000** lignes, **1,64** ligne par ticket
pour **146 161** tickets. Le plus agrégé est l'objectif mensuel par magasin : **218** lignes. Entre les
deux, le rapport est de **1 101**.

Ce facteur n'est pas un détail arithmétique, c'est la raison pour laquelle **deux tables de faits ne
s'additionnent jamais**. Imaginez qu'un rapport présente « le total du modèle » comme la somme des
sept tables : il ajouterait des dinars et des litres. Le résultat serait un nombre à onze chiffres,
affiché en gras dans un tableau de bord, et il ne correspondrait à rien.

La bonne lecture de ces sept tables est **par question**, pas par somme :

| Question | Table | Grain | Mesure à lire |
|---|---|---|---|
| Combien avons-nous vendu ? | `fait_ventes` | ligne de ticket | somme du montant |
| Combien de commandes sont en retard ? | `fait_commandes` | commande | compte, écart de dates |
| Combien avons-nous encaissé ? | `fait_encaissements` | facture | somme encaissée |
| Où est le stock ? | `fait_stock_mensuel` | produit et mois | dernier instantané, moyenne |
| Combien de jours sans vente ? | `fait_ruptures` | produit, magasin, mois | somme des jours |
| Combien coûte la livraison ? | `fait_logistique` | magasin et mois | somme des coûts |
| Sommes-nous dans l'objectif ? | `fait_objectifs` | magasin et mois | montant contre montant de ventes |

### 5.3 Le grain se prouve, il ne se déclare pas

Déclarer un grain est une intention ; le prouver est une mesure. La preuve tient en deux comptages :
**le nombre de lignes** et **le nombre de valeurs distinctes de la clé**. S'ils coïncident, la clé est
unique, donc le grain est celui du chargement — aucune jointure ne l'a multiplié en chemin.

```sql
-- La preuve du grain de fait_ruptures (grain : produit x magasin x mois)
SELECT COUNT(*) AS lignes,
       COUNT(*) AS cles
FROM (SELECT DISTINCT id_produit, id_magasin, mois FROM fait_ruptures);
```

Le socle passe ce contrôle sur les **7** tables de faits : **7** grains sur **7** sont prouvés. Mais
la démonstration la plus utile n'est pas celle qui réussit, c'est celle qui **échoue pour une bonne
raison**. Regardez `fait_objectifs` :

| Clé testée | Valeurs distinctes | Lignes | Conclusion |
|---|---|---|---|
| `id_magasin` + `mois` (numéro de mois) | **60** | **218** | « la table a des doublons » — **faux** |
| `id_magasin` + `annee_mois` (« 2023-01 ») | **218** | **218** | le grain est prouvé |

La colonne `mois` de cette table porte le **numéro** du mois (1 à 12), pas le mois daté : cinq
magasins fois douze numéros de mois donnent **60** valeurs distinctes, et l'on conclurait à tort à des
doublons. Le grain n'était pas faux ; la clé de contrôle l'était.

> **Attention.** Un contrôle d'unicité qui échoue ne prouve pas qu'il y a des doublons : il prouve que
> la clé testée n'est pas celle du grain. Avant de conclure, écrivez la clé en toutes lettres et
> vérifiez qu'elle correspond bien au grain déclaré. Sur le socle, `id_magasin` + `mois` rend **60**
> valeurs pour **218** lignes ; la bonne clé, `id_magasin` + `annee_mois`, en rend **218**.

### 5.4 Trois régimes d'additivité, et la règle qui va avec

Le régime d'additivité d'une mesure détermine ce qu'on a le droit d'écrire dans une requête. Le socle
a été construit pour que les trois régimes soient mesurables.

| Régime | Mesure du socle | Ce qu'on peut faire | Ce qui est interdit |
|---|---|---|---|
| Additif | `montant_ttc`, `quantite`, `jours_rupture` | `SUM` par magasin, par mois, par client | rien, la somme est vraie partout |
| Semi-additif | `stock_moyen_unites`, `colis`, `couverture_mois` | `SUM` **entre** magasins et produits | `SUM` **sur** plusieurs mois |
| Non additif | `marge_objectif_pct`, `taux_remise` | moyenne pondérée, ou recalcul sur les totaux | `SUM`, `AVG` des lignes |

La démonstration, chiffrée sur le fil rouge :

- **additif** — les **44** totaux mensuels des ventes se re-somment au total du modèle, facteur **1,0** ;
- **semi-additif** — les **44** instantanés de stock se somment à **2 034 733** unités au lieu de
  **46 244**, soit **44** fois trop ;
- **non additif** — les **218** taux de marge du plan d'objectifs se somment à **4 248,7 %**, leur
  moyenne vaut **19,5 %**, et la marge du réseau n'est ni l'un ni l'autre.

> **Conseil professionnel.** Quand vous ne savez pas si une mesure s'additionne, faites le test sur
> deux lignes avant de le faire sur deux millions : additionnez deux mois, et demandez-vous si le
> résultat a un sens métier. Deux mois de chiffre d'affaires, oui ; deux mois de stock, non ; deux
> mois de taux de marge, jamais. Ce test prend trente secondes et évite de publier **2 034 733** unités
> de stock au lieu de **46 244**.

### 5.5 Le théorème du grain : ne jamais mélanger les grains

Voici la règle qui tient tout le module : **une table de faits porte un grain unique, et deux tables de
grains différents ne s'additionnent ni ne se joignent sans précaution.**

Ce n'est pas une préférence de style. Le socle en donne la mesure, et elle est spectaculaire. Sur le
schéma fautif livré dans le dossier du module :

| Ce que fait la requête | Résultat | Écart |
|---|---|---|
| ventes + commandes | **22 305 610 960** FCFA | **+ 43,0 %** |
| ventes + commandes + encaissements | **29 474 916 530** FCFA | **+ 89,0 %** |

Le chiffre d'affaires du modèle est de **15 595 154 955** FCFA. La première addition, celle de deux
tables, est déjà fausse de **43** pour cent ; la seconde de **89** pour cent. Et les deux requêtes
s'exécutent : rien n'empêche d'additionner deux colonnes qui portent le même nom — `montant_ttc` — dans
deux tables qui ne mesurent pas la même chose. C'est précisément le piège : le nom est identique, le
grain ne l'est pas.

> **À retenir.** Deux tables de faits ne s'additionnent jamais directement. Si un rapport a besoin de
> chiffres venus de deux processus, il les présente **côte à côte** (une colonne par processus), ou il
> les agrège **séparément** à un grain commun avant de les joindre. L'addition de deux grains
> différents est la faute la plus coûteuse du module : **+ 43,0 %** sur deux tables, **+ 89,0 %** sur
> trois.

### 5.6 Les trois façons de fabriquer un faux total

Il n'y a pas mille manières de produire un total faux. La mesure sur le socle en isole trois, et les
trois rendent un nombre plausible.

**1. Joindre sur une clé trop large.** C'est l'explosion en lignes. Les ventes jointes à la
logistique sur le seul `id_magasin` (au lieu du couple magasin et mois) donnent **10 436 404** lignes et
**686 186 818 020** FCFA, soit **44** fois le chiffre juste. Un magasin a **44** mois d'historique : la
clé trop large fait rencontrer à chaque vente les **44** lignes du magasin.

**2. Joindre sur une clé trop fine, qui filtre sans le dire.** Les ventes jointes aux ruptures sur le
produit et le mois ne gardent que les ventes des produits **en rupture** : **85 126** lignes au lieu de
**237 191**, et **5 558 813 747** FCFA, soit **0,36** du chiffre juste. Ici, aucune ligne n'est
multipliée : ce sont **64** pour cent du chiffre d'affaires qui **disparaissent**, et la requête, elle,
se porte très bien.

**3. Mélanger deux grains dans la même addition.** C'est le §5.5 : **+ 43,0 %** à deux tables,
**+ 89,0 %** à trois.

> **Attention.** Une jointure qui filtre est plus difficile à voir qu'une jointure qui multiplie. Un
> total trop gros se remarque (il dépasse ce qu'on attend) ; un total trop petit a l'air d'une bonne
> nouvelle. Le socle perd **64** pour cent de son chiffre d'affaires avec un `JOIN` parfaitement
> banal entre deux tables auxquelles on fait confiance — les ruptures sont une table **incomplète** :
> un produit-mois sans rupture n'y figure pas.

### 5.7 Le contrôle négatif : la jointure n'est pas toujours la coupable

La réaction naturelle, devant un total faux, est d'accuser la jointure. C'est souvent injuste : la
plupart du temps, la jointure fait exactement ce qu'on lui demande, et c'est la **clé** qui ne dit pas
ce qu'on croit.

Le contrôle négatif tranche la question. On écrit la même requête, sur la même table, avec la clé du
grain cette fois :

| Jointure | Clé | Lignes | Chiffre d'affaires | Facteur |
|---|---|---|---|---|
| Ventes et logistique | `id_magasin` seul | **10 436 404** | **686 186 818 020** FCFA | **44,0** |
| Ventes et stock mensuel | `id_produit` + `mois` | **237 191** | **15 595 154 955** FCFA | **1,0** |

Même intention, même syntaxe, deux résultats que tout sépare. La deuxième requête ne sert à rien
métier — elle ne calcule aucun indicateur utile — et c'est justement pour cela qu'elle est précieuse :
elle **isole la cause**. La jointure multiplie quand la clé est trop large, elle ne multiplie pas quand
la clé est celle du grain. Le défaut n'était donc pas « la jointure » ; il était la clé choisie.

Ce n'est pas la seule forme de filtre silencieux. Le même effet se produit quand la jointure est
pourtant **au bon grain des deux côtés** : joindre deux agrégats mensuels par une jointure interne
fait disparaître le magasin qui n'a aucune vente. Sur le fil rouge, le dépôt central porte **44** mois
de coûts logistiques, **28 893 543** FCFA, et zéro vente : le total des coûts tombe à
**143 816 487** FCFA au lieu de **172 710 030** FCFA. La clé était juste, la jointure aussi, et le
filtre s'est produit quand même — parce que les deux tables ne couvrent pas le même ensemble de
magasins.

> **Conseil professionnel.** Écrivez toujours le contrôle négatif **en même temps** que la requête
> métier, pas après l'incident. Deux requêtes voisines dans le même fichier de livrable : celle qui
> répond à la question, et celle qui prouve que le grain a été respecté. Sur un modèle livré, c'est la
> seconde qu'un relecteur regarde en premier.

### 5.8 La fiche de grain : une page qui évite les trois fautes

Une table de faits sans fiche de grain est une table qu'on interrogera mal. La fiche tient en sept
lignes, une par table, et chacune répond à six questions :

| Colonne | Question à laquelle elle répond |
|---|---|
| Table | de quelle table parle-t-on ? |
| Grain | que porte **une** ligne, en une phrase ? |
| Clé | par quoi identifie-t-on une ligne ? |
| Unité de comptage | une ligne compte **un** quoi ? |
| Additivité | quelles mesures s'additionnent, et dans quel sens ? |
| Agrégations interdites | que ne faut-il **jamais** faire ? |
| Contrôle d'unicité | quelle requête prouve le grain ? |

Pour le fil rouge, les deux premières lignes de cette fiche se lisent ainsi :

- `fait_ventes` — une ligne de ticket ; clé `id_vente` ; compte des tickets ; montant additif,
  quantité additive, taux de remise non additif ; interdit : rien de particulier, c'est le grain le
  plus fin ; contrôle : `COUNT(*) = COUNT(DISTINCT id_vente)`.
- `fait_stock_mensuel` — un produit par mois ; clé `id_produit` et `mois` ; compte des couples ;
  mesures semi-additives ; interdit : sommer plusieurs mois ; contrôle : `COUNT(*) = COUNT(DISTINCT
  id_produit, mois)`.

Cette page est le livrable du mini-projet ci-dessous, et la matière première du livrable P1 du projet
de module.

---

## 6. Exemple concret — six lignes qui expliquent tout le chapitre

La planche de ce chapitre part d'un extrait minuscule : **6** lignes de ventes, deux produits, deux
magasins.

| id_vente | id_produit | id_magasin | quantite |
|---|---|---|---|
| 1 | 12 | 1 | 40 |
| 2 | 12 | 1 | 25 |
| 3 | 7 | 1 | 6 |
| 4 | 12 | 2 | 18 |
| 5 | 7 | 2 | 9 |
| 6 | 31 | 2 | 3 |

**Le grain de cet extrait** est la ligne de ticket : six lignes, six `id_vente` distincts. Le compte
des lignes et le compte des clés coïncident : le grain est prouvé.

**Première lecture, correcte.** Combien de lignes par magasin ? Magasin 1 : trois lignes (1, 2, 3).
Magasin 2 : trois lignes (4, 5, 6). Total : six. Le grain du résultat est « une ligne par magasin »,
et la mesure est un **compte**.

**Deuxième lecture, la bonne clé.** Jointure avec un tableau de stock mensuel de deux lignes (produit
12 et produit 7, tous deux en magasin 1 et 2) sur le couple produit et mois : les six lignes restent
six, la quantité totale est inchangée. C'est le contrôle négatif : facteur **1,0**.

**Troisième lecture, la clé trop large.** Jointure avec un historique de coûts logistiques qui porte
**44** mois par magasin, sur le seul `id_magasin` : chaque ligne de vente rencontre les 44 lignes du
magasin, et six lignes deviennent **264**. Le total de quantité est multiplié par 44 — c'est exactement
ce qui se produit sur le socle, où **237 191** ventes deviennent **10 436 404** lignes.

**Quatrième lecture, la clé trop fine.** Jointure avec un tableau de ruptures qui ne contient qu'un
produit par mois : les ventes de l'autre produit disparaissent. Six lignes deviennent trois, et la
moitié du chiffre d'affaires s'évapore sans que personne ne se plaigne. Sur le socle, la même opération
laisse **64** pour cent du chiffre d'affaires sur le carreau.

Ces quatre lectures, faites sur six lignes, sont les **trois** fautes du §5.6 plus le contrôle qui les
détecte. Vous n'avez pas besoin de deux millions de lignes pour apprendre à les voir ; vous avez besoin
de six lignes et de la bonne question : **quelle est la clé du grain ?**

---

## 7. Démonstration pas à pas — quatre gestes, dans cet ordre

**Étape 1 — écrire le grain en une phrase, avant toute chose.**

```
fait_ventes : une ligne de ticket vendue
```

Cette phrase fixe la clé (`id_vente`), l'unité de comptage (le ticket), et la question à laquelle la
table peut répondre. Elle s'écrit dans le fichier SQL qui crée la table, en commentaire.

**Étape 2 — prouver le grain sur les données chargées.**

```sql
SELECT COUNT(*) AS lignes FROM fait_ventes;
SELECT COUNT(*) AS cles FROM (SELECT DISTINCT id_vente FROM fait_ventes);
```

Si les deux nombres diffèrent, la table ne porte pas le grain annoncé : la cause est une jointure
trop large dans la requête de chargement, ou un doublon dans la source. On corrige **avant** d'écrire
la suite.

**Étape 3 — écrire la règle d'additivité de chaque mesure.**

Pour `fait_ventes` : `montant_ttc`, `montant_ht`, `quantite`, `poids_kg` sont additifs ; `taux_remise`
et `prix_unitaire_ht` sont non additifs (ils se moyennent, ou se recalculent). Pour
`fait_stock_mensuel` : tout est semi-additif — la précision s'écrit une fois, dans la fiche.

**Étape 4 — écrire le contrôle négatif, et le garder.**

```sql
-- Contrôle négatif : la jointure au grain du stock ne doit rien changer au total
SELECT COUNT(*) AS lignes, ROUND(SUM(montant_ttc)) AS ca
FROM fait_ventes;
SELECT COUNT(*) AS lignes, ROUND(SUM(v.montant_ttc)) AS ca
FROM fait_ventes v
JOIN fait_stock_mensuel s
  ON s.id_produit = v.id_produit AND s.mois = strftime(v.date_vente, '%Y-%m');
```

Attendu : le deuxième total est **égal** au premier (facteur **1,0**) — la jointure est disculpée, et
l'on peut passer à la métrique suivante. S'il diffère, la clé n'est pas celle du grain.

---

## 8. Erreurs fréquentes

| Erreur | Ce qu'on observe | La correction |
|---|---|---|
| Joindre sans écrire la clé du grain | **10 436 404** lignes au lieu de **237 191** | nommer le grain, puis la clé, **avant** d'écrire la jointure |
| Croire qu'un `JOIN` qui filtre est un `JOIN` qui garde | **64** pour cent du chiffre d'affaires envolés | `LEFT JOIN`, ou jointure à un grain commun |
| Joindre deux agrégats internes | **143 816 487** FCFA de coûts au lieu de **172 710 030** | jointure externe, et `COALESCE` sur la mesure absente |
| Sommer des instantanés | **2 034 733** unités de stock au lieu de **46 244** | dernier instantané, ou moyenne |
| Sommer des taux | **4 248,7 %** de marge | recalculer sur deux montants, ou moyenner avec un poids |
| Additionner deux tables de faits | **+ 43,0 %** à deux, **+ 89,0 %** à trois | présenter côte à côte, agréger séparément |
| Valider un grain avec la mauvaise clé | **60** valeurs distinctes pour **218** lignes | écrire la clé du grain en toutes lettres |
| Ne tester que le cas qui marche | aucune erreur, aucun avertissement | écrire aussi le contrôle négatif, et celui qui **doit** échouer |

---

## 9. Bonnes pratiques professionnelles

1. **Le grain s'écrit dans la table, pas dans un document à part.** Un commentaire en tête de la
   requête de création, une ligne dans la fiche de grain, et la phrase est la même dans les deux.
2. **Une table de faits, un grain.** Si deux processus se ressemblent, ils font deux tables dont on
   assume qu'elles ne se joignent pas sans agrégation préalable.
3. **Le contrôle d'unicité s'exécute à chaque chargement**, pas une fois pour toutes : il est le
   garde-fou du grain, et il coûte deux requêtes de comptage.
4. **Chaque mesure reçoit sa règle d'additivité**, y compris celles qui ne s'additionnent pas. Écrire
   « non additive : moyenne pondérée » est plus utile que ne rien écrire.
5. **Le contrôle négatif fait partie du livrable.** Une requête qui ne sert à rien métier est une
   requête qui prouve quelque chose.
6. **On nomme les colonnes de résultat avec leur grain** : `nb_lignes_ticket`, `stock_fin_de_mois`,
   `ca_ttc_mois` — le nom du résultat rappelle le grain, et une erreur de lecture devient visible.

---

## 10. Exercice guidé

**Sujet.** Le service logistique publie chaque mois un coût de livraison par magasin : **264** lignes,
un magasin et un mois par ligne. Un rapport demande « le coût logistique par franc de chiffre
d'affaires ». La requête publiée joint les ventes à la logistique sur `id_magasin` et rend un coût
multiplié par **44**. Trouvez la faute, écrivez la requête juste, et prouvez que la nouvelle version
respecte le grain des deux tables.

**Étape 1 — les grains, en deux phrases.** `fait_ventes` : une ligne de ticket (**240 000** lignes,
clé `id_vente`). `fait_logistique` : un magasin par mois (**264** lignes, clé `id_magasin` et `mois`).

**Étape 2 — la faute.** La requête de départ joint sur `id_magasin` seul : la clé de la première table
est plus fine que la clé de la seconde, donc chaque vente rencontre les **44** lignes de son magasin.
Le coût logistique est compté **44** fois ; le chiffre d'affaires est, lui, multiplié par **44** aussi,
ce qui « sauve » le ratio — mais les deux totaux publiés à côté sont faux, et le ratio lui-même perd
son sens dès qu'un magasin a un historique incomplet.

**Étape 3 — la requête juste.** On agrège chaque table **à son propre grain**, puis on joint les deux
résultats sur le grain commun (le mois) — par une jointure **externe**, car le dépôt central n'a
aucune vente :

```sql
WITH ca AS (
  SELECT strftime(date_vente, '%Y-%m') AS mois, id_magasin, ROUND(SUM(montant_ttc)) AS ca
  FROM fait_ventes WHERE est_retour = 0 GROUP BY 1, 2
), logi AS (
  SELECT mois, id_magasin, ROUND(SUM(cout_total)) AS cout FROM fait_logistique GROUP BY 1, 2
)
SELECT logi.mois, logi.id_magasin, logi.cout, COALESCE(ca.ca, 0) AS ca,
       ROUND(logi.cout / NULLIF(COALESCE(ca.ca, 0), 0), 4) AS cout_par_franc
FROM logi LEFT JOIN ca ON ca.mois = logi.mois AND ca.id_magasin = logi.id_magasin
ORDER BY logi.mois, logi.id_magasin;
```

**Étape 4 — la preuve.** Deux contrôles : la somme du chiffre d'affaires de la requête égale le total
du modèle (**15 595 154 955** FCFA), et la somme des coûts logistiques égale le total de la table
logistique, **172 710 030** FCFA — ni multiplié, ni filtré. Avec une jointure **interne**, ce second
contrôle échoue : le total des coûts tombe à **143 816 487** FCFA, et les **28 893 543** FCFA du dépôt
central ont disparu — six magasins portent des coûts, cinq seulement portent des ventes, et le
sixième a précisément **44** mois de dépenses pour zéro vente.

**Barème (15 points) :** les deux grains énoncés (3) · la faute expliquée et chiffrée (4) · la requête
juste, jointure externe comprise (5) · les deux contrôles exécutés (3).

---

## 11. Exercices autonomes

**Exercice 3.1.** Prouvez le grain de `fait_ruptures` (**2 428** lignes) et celui de `fait_objectifs`
(**218** lignes) : écrivez pour chacune la requête d'unicité, puis la même requête avec la **mauvaise**
clé (`id_magasin` et `mois` pour les objectifs), et expliquez en trois lignes pourquoi le second
résultat fait croire à des doublons.

**Exercice 3.2.** Classez ces six mesures du socle en additif, semi-additif ou non additif :
`montant_ttc` (ventes), `stock_moyen_unites` (stock), `marge_objectif_pct` (objectifs),
`jours_rupture` (ruptures), `colis` (logistique), `couverture_mois` (stock). Pour chacune, écrivez
l'agrégation autorisée sur les mois et celle qui est interdite, et donnez la requête qui démontre
l'interdiction sur une des mesures semi-additives.

**Exercice 3.3.** Reproduisez l'explosion en lignes sur un extrait : prenez les **6** lignes de
l'extrait du §6, joignez-les à un tableau de coûts de **44** lignes par magasin sur le seul
`id_magasin`, et vérifiez que vous obtenez **264** lignes. Puis écrivez la jointure corrigée (clé
magasin et mois) et vérifiez que vous retrouvez **6** lignes.

**Exercice 3.4.** Le filtre silencieux : écrivez la requête qui joint les ventes aux ruptures sur le
produit et le mois, mesurez le nombre de lignes et le chiffre d'affaires obtenus, et comparez au total
du modèle (**15 595 154 955** FCFA). Expliquez en cinq lignes pourquoi **64** pour cent du chiffre
d'affaires disparaît, puis proposez **deux** corrections différentes — l'une qui garde toutes les
ventes, l'autre qui assume de ne garder que les produits en rupture, en le déclarant.

**Exercice 3.5.** Écrivez un contrôle négatif pour la requête « chiffre d'affaires par famille de
produits » : proposez une jointure qui doit rendre le total **inchangé** (facteur **1,0**), exécutez-la
et commentez le résultat en trois lignes.

---

## 12. Correction détaillée

**Exercice 3.1.** `fait_ruptures` — les deux comptages coïncident : **2 428** lignes, **2 428** clés
distinctes sur (`id_produit`, `id_magasin`, `mois`) ; le grain est prouvé. `fait_objectifs` — avec la
bonne clé (`id_magasin`, `annee_mois`), **218** lignes et **218** clés : prouvé. Avec la mauvaise clé
(`id_magasin`, `mois`), **60** valeurs distinctes pour **218** lignes : cinq magasins fois douze
numéros de mois font **60** combinaisons possibles, et la table en occupe **218** parce qu'elle couvre
**44** mois. Le contrôle ne révèle donc pas des doublons : il révèle une clé mal choisie.

**Exercice 3.2.** Additifs : `montant_ttc`, `jours_rupture`, `colis`. Semi-additifs :
`stock_moyen_unites`, `couverture_mois`. Non additif : `marge_objectif_pct`. Démonstration du
semi-additif :

```sql
SELECT SUM(stock_moyen_unites) AS somme_des_44_mois
FROM fait_stock_mensuel;   -- 2 034 733 unites
```

à comparer à la lecture correcte, le dernier mois :

```sql
SELECT SUM(stock_moyen_unites) AS stock_du_dernier_mois
FROM fait_stock_mensuel
WHERE mois = (SELECT MAX(mois) FROM fait_stock_mensuel);   -- 45 882 unites
```

La première requête rend **2 034 733** unités, soit **44** fois la seconde : le nombre est
arithmétiquement juste et métier faussement utile.

**Exercice 3.3.** Sur l'extrait : six lignes de ventes, deux magasins, et un tableau de coûts de
**44** lignes par magasin. Jointure sur `id_magasin` seul : 6 fois 44 égale **264** lignes. Jointure
sur (`id_magasin`, `mois`) : les six lignes trouvent chacune leur ligne de coût du mois, et restent
**6**. Le premier résultat n'est pas « plus riche » : il compte 44 fois la même vente.

**Exercice 3.4.** La requête :

```sql
SELECT COUNT(*) AS lignes, ROUND(SUM(v.montant_ttc)) AS ca
FROM fait_ventes v
JOIN fait_ruptures r
  ON r.id_produit = v.id_produit AND r.mois = strftime(v.date_vente, '%Y-%m')
WHERE v.est_retour = 0;
```

Elle rend **85 126** lignes et **5 558 813 747** FCFA, contre **237 191** lignes et **15 595 154 955**
FCFA : facteur **0,36**, soit **64** pour cent du chiffre d'affaires perdu. La raison : `fait_ruptures`
ne contient que les couples produit, magasin et mois **en rupture** ; une vente dont le produit n'était
pas en rupture n'a pas de ligne à rejoindre, et disparaît. Deux corrections : (a) garder toutes les
ventes avec un `LEFT JOIN` et traiter les valeurs manquantes ; (b) assumer le périmètre « ventes de
produits en rupture » et l'écrire dans le titre du rapport, avec le chiffre d'affaires **du périmètre**,
jamais présenté comme le chiffre d'affaires total.

**Exercice 3.5.** Le contrôle négatif :

```sql
SELECT ROUND(SUM(f.montant_ttc)) AS ca_avec_jointure
FROM fait_ventes f
JOIN dim_produit p ON p.id_produit = f.id_produit
WHERE f.est_retour = 0;
```

Résultat : **15 595 154 955** FCFA, identique au total sans jointure — facteur **1,0**. La dimension
produit est au grain du produit (**154** lignes, clé unique), donc chaque vente rencontre exactement
une ligne, et la jointure ne change ni le nombre de lignes ni le total. Ce contrôle est le modèle de
tous les autres : il transforme « je crois que la jointure est bonne » en « je l'ai vérifié ».

---

## 13. Mini-projet de chapitre

**« La fiche de grain du modèle »** (2 h). Produisez, pour les **7** tables de faits du fil rouge, la
fiche de grain complète : une ligne par table, six colonnes comme au §5.8 — table, grain écrit en une
phrase, clé du grain, unité de comptage, régime d'additivité des mesures, agrégations interdites — et
la requête d'unicité qui prouve le grain. Ajoutez une seconde feuille avec les **trois** contrôles
négatifs : celui qui ne change rien (facteur **1,0**), celui qui doit multiplier (facteur **44,0**),
celui qui doit filtrer (facteur **0,36**) — avec, pour chacun, la phrase qui explique ce qu'il prouve.
Ce livrable alimente directement **P1** (MCD et MLD) et **P3** (revue du modèle) du projet de module.

---

## 14. Résumé du chapitre

| Notion | Ce qu'il faut retenir |
|---|---|
| Grain | ce que porte une ligne, écrit en une phrase, prouvé par l'unicité de sa clé |
| Sept grains | de la ligne de ticket (**240 000**) à l'objectif mensuel (**218**), facteur **1 101** |
| Preuve du grain | `COUNT(*)` égal au compte des valeurs distinctes de la clé du grain |
| Bonne clé | sur `fait_objectifs`, (`id_magasin`, `annee_mois`) rend **218** clés ; (`id_magasin`, `mois`) en rend **60** |
| Additif | `montant_ttc` : **44** totaux mensuels se re-somment au total, facteur **1,0** |
| Semi-additif | le stock : **2 034 733** unités sur **44** mois, contre **46 244** pour un mois |
| Non additif | le taux : **4 248,7 %** en somme, **19,5 %** en moyenne, et ni l'un ni l'autre |
| Clé trop large | **10 436 404** lignes et **686 186 818 020** FCFA : facteur **44,0** |
| Clé trop fine | **85 126** lignes et **5 558 813 747** FCFA : facteur **0,36**, **64** pour cent perdus |
| Mélange de grains | ventes plus commandes : **22 305 610 960** FCFA (**+ 43,0 %**) |
| Contrôle négatif | la bonne clé laisse le total intact : facteur **1,0** |
| Filtre par jointure | deux agrégats au même grain, et **28 893 543** FCFA de coûts perdus |
| Fiche de grain | sept lignes de documentation qui évitent les trois fautes |

---

## 15. À retenir

1. **Le grain est une phrase, pas une intuition.** « Une ligne de ticket » se dit, s'écrit, et se
   vérifie par deux comptages.
2. **Le grain se prouve avec la bonne clé.** Un contrôle qui échoue signale parfois une clé mal
   choisie : **60** valeurs distinctes pour **218** lignes ne sont pas des doublons, c'est un numéro
   de mois pris pour un mois daté.
3. **Le filtre silencieux prend deux formes** : la clé trop fine, et la jointure interne entre deux
   ensembles qui ne couvrent pas les mêmes objets — **28 893 543** FCFA du dépôt central disparaissent
   ainsi d'un total de coûts.
4. **Trois régimes, trois règles.** Le montant s'additionne (**facteur 1,0**), le stock s'additionne
   seulement entre magasins (**2 034 733** contre **46 244**), le taux ne s'additionne jamais
   (**4 248,7 %** contre **19,5 %**).
5. **Les trois faux totaux s'exécutent sans erreur** : clé trop large (**44,0**), clé trop fine
   (**0,36**), grains mélangés (**+ 43,0 %**).
6. **Le contrôle négatif fait partie du travail** : il disculpe la jointure et désigne la clé.

> **À retenir.** Un total juste n'est pas un total qui s'exécute : c'est un total dont on peut dire,
> pour chaque ligne lue, ce qu'elle comptait, et pour chaque colonne sommée, dans quel sens elle
> s'additionne.

> **À retenir.** Quand un total paraît étrange, la question n'est pas « la requête est-elle juste ? »
> mais « **quelle est la clé du grain ?** » : dans les trois fautes mesurées du chapitre, la même
> jointure a rendu **44,0** fois trop, **0,36** fois trop peu, et exactement le bon chiffre — selon la
> clé employée.

---

## 16. Évaluation formative

1. Écrivez le grain de `fait_logistique` en une phrase, sans regarder le chapitre.
2. Comment prouve-t-on qu'un grain est respecté ? Donnez les deux comptages et leur lecture.
3. `fait_objectifs` : pourquoi la clé (`id_magasin`, `mois`) rend-elle **60** valeurs pour **218**
   lignes ?
4. Citez une mesure additive, une semi-additive et une non additive du socle, avec leur règle.
5. Les **44** instantanés de stock se somment à **2 034 733** unités. Quelle est la lecture correcte
   sur la période, et pourquoi ?
6. Pourquoi **4 248,7 %** n'est-il pas la marge du réseau, et que faut-il calculer à la place ?
7. Qu'est-ce qu'une explosion en lignes ? Donnez le facteur mesuré sur le socle et sa cause exacte.
8. Pourquoi un `JOIN` qui filtre est-il plus difficile à détecter qu'un `JOIN` qui multiplie ?
9. À quoi sert un contrôle négatif, et que prouve précisément le facteur **1,0** ?
10. Deux tables de faits portent toutes deux une colonne `montant_ttc`. Peut-on les additionner ?
    Justifiez par la mesure du socle.

**Corrigé :** 1. « un magasin, un mois, un coût de livraison » (clé `id_magasin` et `mois`, **264**
lignes). 2. `COUNT(*)` et le compte des valeurs distinctes de la clé du grain : égaux, la clé est
unique, donc aucune jointure n'a multiplié la table. 3. Parce que `mois` y porte le numéro du mois : 5
magasins fois 12 numéros donnent **60** combinaisons, alors que la table couvre **44** mois datés, d'où
**218** lignes avec la clé (`id_magasin`, `annee_mois`). 4. Additive : `montant_ttc` (somme partout) ;
semi-additive : `stock_moyen_unites` (somme entre magasins, jamais entre mois) ; non additive :
`marge_objectif_pct` (moyenne pondérée ou recalcul). 5. Le dernier instantané (**45 882** unités) ou
une moyenne, jamais une somme : sommer des photos de stock ne fait pas un stock. 6. Parce qu'un taux
ne s'additionne pas : la marge du réseau se recalcule à partir du montant de marge et du chiffre
d'affaires, pas en moyennant des taux. 7. C'est la multiplication des lignes d'une table par une clé
trop large : **44,0** sur le socle, parce qu'un magasin possède **44** mois d'historique logistique.
8. Parce qu'un total trop gros attire l'œil, alors qu'un total trop petit ressemble à une bonne
nouvelle : **64** pour cent du chiffre d'affaires peuvent disparaître sans que rien ne paraisse
anormal. 9. À disculper (ou accuser) la jointure : avec la clé du grain, le total est **identique**
(facteur **1,0**), donc la jointure n'est pas la cause du faux total. 10. Non : même nom, grains
différents. Sur le fil rouge, additionner ventes et commandes donne **22 305 610 960** FCFA, soit
**+ 43,0 %** du chiffre d'affaires réel ; deux tables de faits se présentent côte à côte ou s'agrègent
séparément avant d'être jointes.
