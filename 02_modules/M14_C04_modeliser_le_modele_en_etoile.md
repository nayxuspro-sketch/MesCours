# Module M14.C04 — Modéliser : le modèle en étoile et ses douze relations

**Outils : DuckDB 1.5.5 (exécuté) ; pandas (non requis). Power BI Desktop et sa vue Modèle sont
*cités* — l'outil n'est pas installé dans cet atelier (règle §1.5). Les relations, les cardinalités et
les contrôles de ce chapitre sont **mesurés** sur le socle à chaque exécution de `tools/mesures_M14.py`,
section `modele`.**

![Le modèle du rapport : douze relations actives, deux inactives, et le piège de la colonne non unique (production : `tools/figures_M14.py`)](../figures/M14_C04_modele_etoile_powerbi.svg)

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous savez :

1. **distinguer un modèle en étoile d'un modèle en flocon**, et dire pourquoi le rapport du fil rouge
   garde l'étoile : **12** tables, **5** dimensions, **7** tables de faits, **12** relations ;
2. **déclarer une relation plusieurs à un** et **prouver** la seule condition qu'elle exige —
   l'unicité de la colonne du côté « un » — relation par relation : **12** colonnes vérifiées, **12**
   colonnes uniques ;
3. **expliquer les deux relations inactives** du rapport : la commande porte **trois** dates pour
   **une** seule table de dates, et une seule relation peut porter le filtre ;
4. **refuser un filtrage bidirectionnel** quand il ne se justifie pas : **2** candidats examinés, **2**
   refus argumentés, et la raison écrite ;
5. **contrôler le modèle par sa sortie** : les **10** valeurs du rapport, et les **8** d'entre elles que
   l'instrument compare directement à la mesure opérationnelle de M12 — **0** écart.

---

## 2. Pourquoi cette notion est importante

Une requête peut être parfaite et un rapport faux. L'erreur ne vient pas des données, elle vient du
**modèle** : du dessin des relations qui relient les tables entre elles. Un modèle est un ensemble de
règles qui disent à l'outil comment un filtre posé sur une dimension se propage vers les faits. Ces
règles ne lèvent presque jamais d'erreur : elles se contentent de multiplier les lignes.

Le chapitre précédent a rendu la donnée propre ; celui-ci la rend **cohérente**. Trois enjeux, tous
mesurés sur le fil rouge.

**Le premier est la justesse.** Le mécanisme tient en une phrase : **une clé qui se répète multiplie les
lignes**, et deux cas sont mesurés sur le fil rouge. `annee_mois` compte **44** valeurs distinctes dans
le calendrier, mais **28** à **31** lignes par mois — une par jour : une jointure par `annee_mois`
affiche **474 681 181 861** FCFA au lieu de **15 595 154 955** FCFA, facteur **30,44**. Et deux tables
de faits jointes directement se multiplient l'une par l'autre : `fait_logistique` porte **44** lignes
par magasin, et la jointure ventes × logistique sur le magasin seul rend **10 436 404** lignes et
**686 186 818 020** FCFA — facteur **44,0**, la faute que M13 a mesurée. Dans les deux cas, l'outil
n'affiche **aucune** erreur : il faut un contrôle.

**Le deuxième est la lisibilité.** **12** relations déclarées dans une vue Modèle se relisent en
**deux** minutes ; **12** jointures écrites au fil des visuels se relisent en une heure, et personne ne
le fait. Un modèle est la **carte** du rapport : c'est là qu'on vérifie qu'un filtre de magasin atteint
bien les ventes, les commandes, les ruptures et les encaissements — et qu'il n'en atteint pas d'autres.

**Le troisième est la maintenance.** Les deux relations inactives, les deux filtrages bidirectionnels
refusés, la table de dates marquée : ces décisions ne se devinent pas dans un rapport qui fonctionne.
Elles s'écrivent. Le jour où un nouveau venu ajoute « juste une relation », c'est le document qui
l'empêche de casser le taux de service.

---

## 3. Explication simple — le carrefour et les panneaux

Imaginez un carrefour giratoire.

Au centre, les voitures circulent : ce sont les **lignes de faits** — une vente, une commande, un
encaissement. Elles ne portent que des nombres et des identifiants : un montant, une quantité, un
`id_magasin`.

Autour, aux sorties, des **panneaux** : ce sont les **dimensions** — le magasin, le produit, le client,
le vendeur, la date. Chaque panneau porte ce que les voitures ne transportent pas : le nom du magasin,
la famille du produit, le segment du client.

Une **relation**, c'est la règle du carrefour : « une voiture qui porte le panneau magasin 3 sort au
panneau magasin 3 ». Il y a une seule règle à respecter, et c'est celle qui empêche les accidents : **un
panneau, une sortie**. Si deux sorties portent le mot « magasin 3 », la voiture hésite, et l'outil la
compte deux fois. C'est tout le chapitre : **12** voitures, **12** règles, et la vérification que chaque
panneau est bien unique.

Trois situations se présentent ensuite, et elles font tout le reste du modèle.

**Le panneau qui ne sert pas à cette heure-ci.** La commande porte trois dates — la date de commande,
la date promise, la date de livraison — et il n'y a qu'une seule table de dates autour du carrefour.
Une seule règle peut porter le filtre du rapport ; les deux autres **existent mais restent inactives**,
et s'activent au moment précis où une mesure en a besoin.

**Le panneau qu'on laisse entrer à l'envers.** Rien n'interdit d'écrire une règle qui laisse les
voitures circuler dans les deux sens : un filtre posé sur une table de faits remonterait alors vers la
dimension. C'est parfois utile, souvent dangereux, et le rapport du fil rouge a examiné **deux**
candidats avant de les **refuser**.

**Le panneau qu'on décore.** Autour du carrefour, on peut aussi ajouter un panneau qui **calcule** :
« marge = revenu moins coût ». Ces panneaux-là ne sont pas des dimensions, ce sont les **mesures** —
elles se calculent à la lecture, elles ne se stockent pas, et le chapitre suivant leur est consacré.

---

## 4. Vocabulaire essentiel

| Terme | Ce qu'il désigne sur le fil rouge |
|---|---|
| **Table de faits** | une table d'événements mesurables : `fait_ventes` (**240 000** lignes), `fait_commandes`, `fait_encaissements`, `fait_ruptures`, `fait_stock_mensuel`, `fait_objectifs`, `fait_logistique` |
| **Table de dimension** | une table d'attributs qui décrivent les événements : `dim_client` (**23 913** lignes), `dim_produit` (**154**), `dim_magasin` (**6**), `dim_vendeur` (**22**), `dim_date` (**1 339**) |
| **Grain** | ce que représente **une ligne** d'une table : un ticket, une ligne de vente, un couple produit-magasin-mois |
| **Clé étrangère** | la colonne du fait qui pointe vers une dimension : `id_magasin`, `id_produit`, `date_vente` |
| **Clé unique** | la colonne de la dimension qui ne se répète pas : c'est la condition de la relation |
| **Cardinalité** | le rapport entre le nombre de lignes de chaque côté : **plusieurs à un** dans tout ce chapitre |
| **Direction du filtre** | le sens dans lequel un filtre se propage : de la dimension vers le fait (simple), ou dans les deux sens (bidirectionnel) |
| **Relation active / inactive** | une relation déclarée qui filtre le rapport (active), ou qui existe sans filtrer (inactive) |
| **`USERELATIONSHIP`** | la fonction qui active une relation inactive **à l'intérieur d'une mesure**, et nulle part ailleurs |
| **Table de dates** | la dimension du temps, unique, continue et marquée comme telle : `dim_date`, **1 339** jours du 2023-01-01 au 2026-08-31, **44** mois |
| **Schéma en étoile** | les faits au centre, les dimensions autour, une seule jointure entre les deux |
| **Schéma en flocon** | des dimensions découpées en sous-tables reliées entre elles — le socle porte `dim_client_scd` et `dim_produit_scd`, héritage de M13 |
| **Sécurité au niveau des lignes — *row-level security*** | le filtre posé sur le **modèle**, qui restreint chaque utilisateur à son périmètre : ici, son magasin |

> **Définition.** Une **relation** est un couple de colonnes — une du côté « plusieurs », une du côté
> « un » — accompagné de trois propriétés : la **cardinalité**, la **direction du filtre** et son
> **état** (active ou inactive). Une relation n'est donc jamais un simple trait : c'est une décision en
> trois parties.

> **Définition.** Le **grain** d'une table est le sens d'une de ses lignes. Un fait au grain du ticket
> et un fait au grain du mois ne s'additionnent pas entre eux : ils se lisent séparément, et c'est le
> modèle qui garantit qu'aucun visuel ne les mélange.

> **Définition.** Un **modèle en étoile** met les tables de faits au centre et les dimensions autour,
> avec une seule jointure entre elles, **jamais** de jointure entre deux faits ni entre deux
> dimensions. Un **flocon** découpe une dimension en plusieurs tables reliées ; il économise de la
> place et coûte une jointure de plus à chaque lecture.

> **Définition.** Le **filtrage bidirectionnel** autorise un filtre à remonter d'une table de faits vers
> une dimension. **L'ambiguïté de relation** naît quand deux chemins de filtrage mènent d'une table à
> une autre : l'outil ne sait plus quel chemin suivre, et le résultat devient dépendant de l'ordre des
> déclarations.

> **Définition.** Une **mesure** est un calcul évalué au moment où un visuel s'affiche ; une **colonne
> calculée** est un calcul évalué au moment de l'actualisation, et **stocké** dans le modèle. La
> première suit les filtres, la seconde est figée dans la table.

---

## 5. Cours approfondi

### 5.1 Pourquoi l'étoile, et pas le flocon

Le modèle de M13 est déjà en étoile : les tables de faits au centre, les dimensions autour. En M14,
l'outil importe ce modèle **tel quel** — **12** tables, **5** dimensions, **7** faits — et le travail ne
consiste pas à le redessiner, mais à **déclarer les relations** que le dessin suppose.

Le flocon existe pourtant dans le socle : `dim_client_scd` (**24 893** lignes) et `dim_produit_scd`
(**616** lignes) sont des versions historisées des dimensions. Elles ne sont pas importées dans le
rapport, et il faut comprendre pourquoi : ce sont des tables **au grain de la version**, où un client
apparaît plusieurs fois — **900** clients y portent plusieurs versions. Une table où la clé se répète ne
peut pas être le côté « un » d'une relation plusieurs à un. Ce n'est pas un défaut de la table, c'est un
autre usage : elle sert à relire un attribut **au moment du fait**, travail de M13, pas à filtrer un
tableau de bord.

> **Attention.** Un flocon n'est pas une faute : c'est un **coût**. Chaque niveau de découpage ajoute une
> jointure à chaque visuel, et une jointure mal placée est l'endroit exact où un filtre se perd. La
> question n'est jamais « est-ce plus joli ? », mais « qui lit cette table, et avec quel filtre ? ».

### 5.2 Les douze relations du rapport, une par une

Les **12** relations ne viennent que de **4** des **7** tables de faits. C'est une propriété du socle, et
elle se lit : tout ce qui est filtrable par une dimension se rattache à ces quatre tables.

| # | Table de faits | Colonne | Dimension | Colonne | Cardinalité |
|---|---|---|---|---|---|
| 1 | `fait_ventes` | `id_magasin` | `dim_magasin` | `id_magasin` | plusieurs à un |
| 2 | `fait_ventes` | `id_produit` | `dim_produit` | `id_produit` | plusieurs à un |
| 3 | `fait_ventes` | `id_client` | `dim_client` | `id_client` | plusieurs à un |
| 4 | `fait_ventes` | `id_vendeur` | `dim_vendeur` | `id_vendeur` | plusieurs à un |
| 5 | `fait_ventes` | `date_vente` | `dim_date` | `date` | plusieurs à un |
| 6 | `fait_commandes` | `id_magasin` | `dim_magasin` | `id_magasin` | plusieurs à un |
| 7 | `fait_commandes` | `id_client` | `dim_client` | `id_client` | plusieurs à un |
| 8 | `fait_commandes` | `date_commande` | `dim_date` | `date` | plusieurs à un |
| 9 | `fait_encaissements` | `id_client` | `dim_client` | `id_client` | plusieurs à un |
| 10 | `fait_encaissements` | `date_facture` | `dim_date` | `date` | plusieurs à un |
| 11 | `fait_ruptures` | `id_produit` | `dim_produit` | `id_produit` | plusieurs à un |
| 12 | `fait_ruptures` | `id_magasin` | `dim_magasin` | `id_magasin` | plusieurs à un |

**Trois faits restent sans relation** : `fait_stock_mensuel` (**6 776** lignes), `fait_objectifs`
(**218**) et `fait_logistique` (**264**). Ce n'est pas un oubli. Leur grain est le mois, et la seule
colonne de mois du modèle — `annee_mois` — n'est **pas unique** : elle porte **28** à **31** lignes par
mois. Les rattacher par cette colonne multiplierait leurs lignes par le nombre de jours du mois. Ces
tables se lisent donc pour elles-mêmes, sur les pages qui les concernent ; et surtout, **aucune relation
ne relie deux faits entre eux** : le chemin passe toujours par une dimension, c'est la règle qui empêche
la multiplication mesurée au § 5.6.

**Ce que chaque relation apporte, en une phrase.** Les relations **1** à **5** donnent au rapport de
ventes ses cinq axes de lecture — magasin, produit, client, vendeur, date —, c'est-à-dire les quatre
segments de la page Direction et les deux pages de détail. Les relations **6** à **8** donnent au suivi
des commandes ses trois axes, dont la date promise qui porte le taux de service. Les relations **9** et
**10** donnent aux encaissements le client et la date de facture — sans elles, l'encours de
**1 202 550 590** FCFA n'existe pas. Les relations **11** et **12** donnent aux ruptures le produit et
le magasin, sans quoi le taux de rupture ne se lit qu'au niveau du réseau.

### 5.3 L'unicité, la seule condition

Une relation plusieurs à un n'a **qu'une** exigence : la colonne du côté « un » doit être unique. Si
elle ne l'est pas, chaque ligne du fait trouve plusieurs lignes de dimension, et l'outil doit choisir —
il ne choisit pas, il **multiplie**. La vérification tient en une requête par relation, et elle se
rejoue à chaque évolution du modèle.

```sql
-- la question posée 12 fois : la colonne de dimension est-elle unique ?
SELECT COUNT(*) AS lignes, COUNT(DISTINCT id_client) AS cles FROM dim_client;
--  23 913 | 23 913   ->  oui, un client par ligne
```

Le socle répond oui **12** fois sur **12** : `dim_client` **23 913** valeurs distinctes pour **23 913**
lignes, `dim_produit` **154** pour **154**, `dim_magasin` **6** pour **6**, `dim_vendeur` **22** pour
**22**, `dim_date` **1 339** pour **1 339**. La colonne `date` de `dim_date` est unique, et c'est bien
pour cela que la relation passe par elle, et non par `annee_mois`.

> **Attention.** Un contrôle qui réussit aujourd'hui ne prouve rien pour demain. Le socle de M13 a livré
> des référentiels clients qui **changent** : une version mal chargée peut introduire un doublon de clé,
> et la relation qui tenait se mettra à multiplier les lignes **sans prévenir**. Le contrôle d'unicité
> fait partie des **7** tests avant mise en production.

### 5.4 Le sens du filtre : de la dimension vers le fait

Dans les **12** relations, le filtre circule dans un seul sens : **de la dimension vers le fait**. Un
segment posé sur `dim_magasin` restreint les lignes de `fait_ventes` ; un segment posé sur
`fait_ventes` n'atteint jamais `dim_magasin`. C'est le sens naturel, et c'est aussi le seul qui rende le
résultat prévisible.

Le filtrage bidirectionnel a été examiné **deux** fois, puis refusé **deux** fois.

| Candidat | Ce qu'il apporterait | Pourquoi il est refusé |
|---|---|---|
| `fait_ventes` ↔ `dim_client` | filtrer les clients par les ventes — « les clients qui ont acheté ce mois-ci » | l'ambiguïté de relation : `dim_client` est déjà atteinte par les encaissements et les commandes ; deux chemins de filtrage, deux réponses possibles selon le visuel |
| `fait_ruptures` ↔ `dim_produit` | filtrer le catalogue par les ruptures | le filtre remonte d'un fait vers une dimension **partagée** par trois autres faits : le catalogue se réduirait silencieusement dans toute la page, y compris là où la rupture ne veut rien dire |

> **Définition.** L'**ambiguïté de relation** apparaît quand deux chemins de filtrage relient les mêmes
> tables. L'outil exige alors que l'un des deux soit désactivé ; en pratique, on préfère **ne pas créer**
> le chemin bidirectionnel, et faire porter le besoin par une mesure écrite, lisible et testable.

La règle professionnelle tient en une ligne : **un filtre bidirectionnel est une décision, jamais une
commodité**. S'il faut « voir les clients qui ont acheté », cela se calcule dans une mesure — et cette
mesure se relit.

### 5.5 Les relations inactives, et le cas qui les active

`fait_commandes` porte **trois** dates : la date de commande, la date promise et la date de livraison.
`dim_date` est **une** seule table. Une seule relation peut porter le filtre du rapport : les deux
autres sont déclarées **inactives**.

| Table de faits | Colonne | Dimension | Ce qu'elle sert, et quand elle s'active |
|---|---|---|---|
| `fait_commandes` | `date_promisee` | `dim_date` | la promesse de livraison : s'active **dans la mesure** du taux de service, jamais dans le filtre du rapport |
| `fait_commandes` | `date_livraison` | `dim_date` | la livraison effective : reste inactive, parce que le rapport se lit par date de commande ; c'est une information de suivi |

Le taux de service est exactement le cas d'usage qui justifie une relation inactive : il se lit sur la
**date promise**. Le rapport affiche **81,0 %** de commandes livrées au plus tard à la date promise,
c'est-à-dire **78,2 %** de toutes les commandes. Ces deux valeurs n'existent que si la mesure sait
activer la seconde ligne de dates — et elles ne doivent **pas** changer quand l'utilisateur filtre la
page sur un autre mois que celui qu'il regarde.

> **Dans les faits.** Une relation inactive oubliée est indétectable : le rapport reste juste, la mesure
> rend simplement un autre nombre. Sur le fil rouge, la mesure du taux de service écrite sur la date de
> commande rendrait un pourcentage différent de **81,0 %** sans qu'aucune erreur n'apparaisse. C'est le
> genre d'écart qu'un contrôle de recette attrape, et qu'un œil humain ne voit pas.

> **À retenir.** Trois dates dans un fait, une seule table de dates : **une** relation porte le filtre,
> les autres attendent dans une mesure. Ce n'est pas une limite de l'outil, c'est la manière d'avoir
> trois temps dans un même fait — et de le **dire**.

### 5.6 La table de dates, marquée et unique

`dim_date` compte **1 339** lignes, du 2023-01-01 au 2026-08-31, et sa colonne `date` est unique. Elle
porte le calendrier complet — année, trimestre, mois, semaine, jour — et elle est **marquée comme table
de dates** dans le modèle, ce qui donne aux visuels une échelle de temps continue : un mois sans vente
apparaît à zéro au lieu de disparaître de l'axe.

Trois fautes se ressemblent et n'ont pas le même coût.

**La première est de relier le fait à la table de dates par une colonne de mois** (`annee_mois`,
`mois`). La colonne porte **28** à **31** lignes par mois — une par jour — et la jointure les fait
toutes correspondre.

```sql
-- le premier piège, mesuré : combien de lignes de calendrier pour un mois ?
SELECT COUNT(*) FROM dim_date WHERE annee_mois = '2026-08';
--  31   ->  une jointure par annee_mois multiplie la ligne par le nombre de jours du mois
--  et sur l'ensemble du calendrier : 474 681 181 861 FCFA au lieu de 15 595 154 955 FCFA, facteur 30,44
```

**La deuxième est de joindre deux tables de faits entre elles.** C'est la faute que M13 a mesurée, et
elle coûte plus cher que la précédente : `fait_logistique` porte **264** lignes pour **6** magasins,
soit **44** lignes par magasin. Une jointure ventes × logistique sur le magasin seul rend **10 436 404**
lignes et **686 186 818 020** FCFA, facteur **44,0**.

```sql
-- le second piège, mesuré : deux faits joints directement
SELECT COUNT(*) FROM fait_ventes v JOIN fait_logistique l ON l.id_magasin = v.id_magasin
WHERE v.est_retour = 0;
--  10 436 404 lignes, et 686 186 818 020 FCFA au lieu de 15 595 154 955 FCFA
```

**La troisième est d'utiliser les colonnes de date portées par le fait** dans les visuels : les mois
sans vente disparaissent, les comparaisons d'une année sur l'autre glissent, et le rapport perd sa
continuité sans rien afficher de faux.

> **Attention.** La colonne `annee_mois` de `dim_date` est utile pour **lire** un référentiel
> d'objectifs, jamais pour **joindre**. Une colonne non unique peut vivre dans un modèle ; elle ne peut
> pas être le côté « un » d'une relation — et deux faits ne se joignent jamais entre eux.

### 5.7 La table de mesures, et la seule colonne ajoutée au modèle

Le rapport écrit **onze** mesures, rassemblées dans une table qui ne porte aucune donnée et sert
uniquement à les ranger : c'est la **table de mesures**. Leur code complet figure dans le dossier du
module (`03_exercices/dossier_M14/modele_powerbi.md`, §4) ; le chapitre suivant les écrit une par une.

| Mesure | Ce qu'elle rend |
|---|---|
| `[CA net]` | le chiffre d'affaires hors retours : **15 595 154 955** FCFA |
| `[CA HT]` | le chiffre d'affaires hors taxes, dénominateur de la marge |
| `[Coût HT]` | la quantité vendue multipliée par le coût standard du produit |
| `[Marge brute]` | `[CA HT]` moins `[Coût HT]` : **3 847 989 780** FCFA |
| `[Taux de marge %]` | la marge rapportée au chiffre d'affaires : **29,12 %** |
| `[Panier moyen]` | le chiffre d'affaires net divisé par le nombre de tickets : **107 396** FCFA |
| `[Taux de rupture %]` | **7,29 %**, sur **2 428** couples produit-magasin-mois en rupture |
| `[Taux de retour lignes %]` | **1,17 %** des lignes, **1,91 %** des tickets |
| `[Taux de service %]` | **81,0 %** des commandes livrées, sur la date promise |
| `[Encours client]` | **1 202 550 590** FCFA pour **1 272** factures ouvertes |
| `[Coût logistique par colis]` | **3 284** FCFA pour **52 596** colis |

Une seule **colonne** est ajoutée au modèle par rapport à M13 : le coût d'achat du produit, qui vit
dans la **dimension** et pas dans le fait. Le modèle de ventes de M13 ne le portait pas, parce qu'un
modèle de ventes n'a pas besoin de connaître les coûts ; M14 le fait entrer par une fusion de requêtes
sur le référentiel produit (**154** produits, **237 191** lignes de vente après nettoyage), et c'est la
dimension qui le porte, parce qu'un coût est un attribut du produit, pas de la vente.

> **Conseil professionnel.** Rangez vos mesures dans une table dédiée et **nommez-les** comme des
> indicateurs, pas comme des formules : `[Taux de rupture %]`, jamais `[somme_ruptures_div].` Un nom de
> mesure est lu par des gens qui ne liront jamais son code.

### 5.8 La sécurité, l'actualisation : deux décisions de modèle

Le retour n° **2** du comité des utilisateurs — « je ne dois voir que mon magasin » — se traite par un
**rôle de sécurité** qui filtre `dim_magasin`, et par rien d'autre. Le socle compte **6** magasins ; le
filtre du modèle restreint chaque personne à son périmètre, y compris dans les visuels que vous n'avez
pas prévus.

La raison est structurelle : un filtre écrit dans **chaque mesure** se contourne en changeant de page, en
exportant, ou en ouvrant le rapport par un autre chemin ; un filtre posé **sur le modèle** s'applique à
tout ce qui sort. Et un filtre de sécurité ne se teste pas à l'œil : il se teste en se connectant avec
le compte d'un utilisateur, sur les trois pages, et en vérifiant que la page d'aide reste lisible.

L'actualisation, elle, n'est pas une décision de visuel : mode (Import), fréquence, passerelle,
responsable, alerte en cas d'échec. Un rapport qui se rafraîchit mal **sans que personne ne le sache**
est plus dangereux qu'un rapport manuel.

---

## 6. Exemple concret — la recette du modèle

Un modèle se contrôle par sa **sortie**. Les **10** valeurs que le rapport doit afficher sont calculées
ici sur l'étoile — la même chaîne de requêtes que celle de l'import — et comparées à ce que M12 avait
mesuré sur les tables opérationnelles.

| # | Valeur | Sur l'étoile de M14 | Contrôle croisé M12 |
|---|---|---|---|
| 1 | Chiffre d'affaires net | **15 595 154 955** FCFA | identique |
| 2 | Marge brute | **3 847 989 780** FCFA (**29,12 %**) | identique |
| 3 | Panier moyen | **107 396** FCFA | identique |
| 4 | Taux de rupture | **7,29 %** | identique |
| 5 | Rotation des stocks | **9,42** | comparée par l'instrument |
| 6 | Taux de retour | **1,17 %** des lignes, **1,91 %** des tickets | identique |
| 7 | Taux de service | **81,0 %** / **78,2 %** | identique |
| 8 | Encours client | **1 202 550 590** FCFA, **1 272** factures | identique |
| 9 | Coût logistique par colis | **3 284** FCFA, **52 596** colis | identique |
| 10 | Premier magasin du réseau | Sahel Distribution — Ouaga 2000, **34,1 %** | identique |

**Le contrôle, écrit noir sur blanc** : **8** des **10** valeurs se comparent directement à la mesure
opérationnelle de M12, et l'écart est de **0**. Deux chemins de calcul différents — les tables
opérationnelles d'un côté, le modèle en étoile de l'autre — donnent le même nombre. C'est exactement ce
qu'un tableau de bord doit rendre, et c'est aussi le seul contrôle de recette qui vaille : un modèle ne
se juge pas au nombre de relations qu'il porte, mais à ce qu'il **reproduit**.

---

## 7. Démonstration pas à pas — les relations, dans l'outil

> **Boîte à outils.** Ce chapitre se rejoue dans **trois** endroits de l'outil — la vue **Modèle** pour
> les relations, la table de **mesures** pour les calculs, la vue **Sécurité** pour le rôle — et il se
> **prouve** ailleurs : dans l'atelier, chaque affirmation du chapitre est vérifiée en SQL sur le socle,
> parce que l'outil n'y est pas installé (règle §1.5). Les gestes sont décrits ; les contrôles sont
> exécutés.

**Avertissement d'exécution.** Rien de ce qui suit n'a été cliqué : Power BI Desktop n'est pas installé
dans cet atelier. Chaque geste est décrit par son libellé et son emplacement, et chaque affirmation est
mesurée par `tools/mesures_M14.py` (section `modele`) sur les mêmes tables.

**Les douze gestes, dans l'ordre.**

1. **Importer le modèle** — les **12** tables du socle de M13, telles quelles : aucune table n'est
   ajoutée, aucune n'est retirée.
2. **Ouvrir la vue Modèle** et disposer les faits au centre, les dimensions autour : le dessin doit
   ressembler à une étoile, sinon la question est de savoir pourquoi.
3. **Glisser la colonne du fait** (`fait_ventes.id_magasin`) **sur la colonne de la dimension**
   (`dim_magasin.id_magasin`) : la relation se crée du côté « plusieurs » vers le côté « un ».
4. **Vérifier la cardinalité** : « plusieurs à un », jamais « plusieurs à plusieurs ».
5. **Vérifier la direction du filtre** : simple, de la dimension vers le fait.
6. **Contrôler l'unicité** de la colonne de dimension — le geste de l'outil ne le fait pas, la
   vérification se fait en SQL, relation par relation : **12** fois la même requête.
7. **Répéter pour les onze autres relations**, en listant à chaque fois le fait, la colonne, la
   dimension et la colonne — c'est cette liste qui deviendra le tableau du § 5.2.
8. **Créer les deux relations sur la date promise et la date de livraison**, puis les **marquer
   inactives** : elles apparaissent en pointillé dans la vue Modèle.
9. **Activer la seconde date dans la mesure** du taux de service, et **seulement** là : la mesure
   rejoue **81,0 %** et **78,2 %**, et l'écart entre les deux reste celui des commandes livrées.
10. **Marquer `dim_date` comme table de dates** sur la colonne `date`, et vérifier qu'aucun visuel ne
    dépend d'une colonne de date portée par un fait.
11. **Créer la table de mesures** et y écrire les **onze** mesures, chacune avec son nom d'indicateur et
    son format.
12. **Poser le rôle de sécurité** sur `dim_magasin` — **6** magasins, un périmètre par utilisateur — et
    **relire le diagramme** une dernière fois : **12** relations actives, **2** inactives, **0**
    ambiguïté.

**Les contrôles exécutés, et ce qu'ils rendent.**

| Contrôle | Requête | Résultat |
|---|---|---|
| Relation plusieurs à un, 12 fois | `COUNT(*)` contre `COUNT(DISTINCT cle)` sur chaque dimension | **12** colonnes uniques sur **12** |
| Le grain du calendrier | `SELECT COUNT(*) FROM dim_date WHERE annee_mois = '2026-08'` | **31** lignes pour un mois (**28** à **31** sur l'année) : la colonne n'est pas une clé |
| Le premier piège, en francs | ventes jointes à `dim_date` par `annee_mois` | **474 681 181 861** FCFA, facteur **30,44** |
| Le second piège, en francs | ventes jointes à `fait_logistique` sur le magasin seul | **10 436 404** lignes, **686 186 818 020** FCFA, facteur **44,0** |
| Le fait sans relation | `COUNT(*)` sur `fait_stock_mensuel`, `fait_objectifs`, `fait_logistique` | **6 776**, **218**, **264** lignes, lues pour elles-mêmes |
| La recette du modèle | la chaîne étoile rejoue les **10** valeurs du rapport | **8** comparaisons avec M12, **0** écart |
| La mesure au service de la vérité | taux de service sur la date promise | **81,0 %** des livrées, **78,2 %** des commandes |

---

## 8. Erreurs fréquentes

1. **Relier un fait à la table de dates par une colonne de mois.** La colonne porte **28** à **31**
   lignes par mois : le chiffre d'affaires est multiplié par le nombre de jours du mois — **474 681 181 861**
   FCFA au lieu de **15 595 154 955** — et aucune erreur n'est affichée.
2. **Déclarer une relation plusieurs à plusieurs.** L'outil l'accepte, l'affiche, et n'en fait rien de
   juste : le résultat dépend de l'ordre des lignes.
3. **Laisser une relation inactive sans le dire.** Le rapport reste juste, la mesure rend un autre
   nombre : **81,0 %** devient un pourcentage qui ne veut rien dire.
4. **Activer un filtrage bidirectionnel « pour voir ».** Le filtre remonte, le catalogue se réduit
   silencieusement sur toute la page, et le visuel d'à côté change avec lui.
5. **Poser un filtre de sécurité dans chaque mesure.** Le premier changement de page le contourne.
6. **Se servir de `dim_client_scd` comme dimension du rapport.** **24 893** lignes pour **23 913**
   clients : la clé se répète, la relation multiplie.
7. **Utiliser la colonne de date portée par le fait.** Le mois sans vente disparaît, la comparaison
   annuelle glisse, et personne ne s'en aperçoit avant la réunion.
8. **Joindre deux tables de faits entre elles.** Ventes × logistique sur le magasin seul : **10 436 404**
   lignes et un chiffre d'affaires multiplié par **44,0** — la faute mesurée par M13, et celle que
   l'exercice guidé de ce chapitre fait diagnostiquer.
9. **Ne pas vérifier l'unicité après un rechargement.** Une dimension qui gagne un doublon casse un
   modèle qui fonctionnait hier.

---

## 9. Bonnes pratiques professionnelles

1. **Vérifier l'unicité des douze colonnes avant de déclarer les relations**, pas après avoir constaté
   un total double.
2. **Nommer chaque relation dans le dossier** — fait, colonne, dimension, colonne, cardinalité, sens,
   état. Le tableau du § 5.2 est ce document.
3. **Dire pourquoi une relation est inactive**, en une phrase, à côté de la table qui l'utilise.
4. **Refuser le bidirectionnel par défaut**, et écrire la mesure qui répond au besoin réel.
5. **Marquer la table de dates**, et n'en avoir qu'une.
6. **Ranger les mesures dans une table de mesures**, avec des noms d'indicateurs.
7. **Rejouer la recette après chaque modification du modèle** : les **10** valeurs, les **8**
   comparaisons, l'écart à **0**.

> **À retenir.** Un modèle se juge à sa **sortie**. Tant que la chaîne étoile ne reproduit pas
> **15 595 154 955** FCFA et les **9** autres valeurs du rapport, aucune relation n'est « déclarée » —
> elle est seulement dessinée.

---

## 10. Exercice guidé

**Énoncé.** Le rapport affiche un chiffre d'affaires de **686 186 818 020** FCFA, soit **44** fois le
montant attendu. Trouvez la cause, corrigez-la, et prouvez que le rapport est revenu juste.

**Étape 1 — constater.** Divisez le montant affiché par le montant attendu : le rapport vaut **44,0**.
Un rapport entier et constant n'est jamais un hasard de calcul : c'est un **nombre de lignes**.

**Étape 2 — chercher ce qui vaut 44.** Comptez les lignes du plus petit fait du modèle par magasin :
`fait_logistique` porte **264** lignes pour **6** magasins, soit **44** lignes par magasin. Une table de
faits jointe à une autre table de faits sur la seule dimension qu'elles partagent multiplie donc chaque
ligne de vente par **44**.

**Étape 3 — corriger.** Retirez la relation entre les deux faits : dans le modèle, **deux faits ne se
joignent jamais**. Le coût logistique par colis se lit sur la table logistique, le chiffre d'affaires sur
les ventes, et les deux se rejoignent par la **dimension** magasin — c'est le modèle qui garantit qu'une
ligne de vente reste une ligne de vente.

**Étape 4 — écrire la règle.** Ajoutez au dossier du modèle deux lignes : « aucune relation ne passe par
une colonne non unique » et « aucune relation ne relie deux faits entre eux ». Ce sont ces deux lignes
qui empêcheront la faute de revenir — et le § 5.6 en a mesuré les deux factures : **30,44** et **44,0**.

**Attendu.** Le rapport **44,0** identifié, la requête de comptage écrite, la relation fautive retirée,
et la règle consignée — pas seulement la correction.

---

## 11. Exercices autonomes

**Exercice 4.1.** Reprenez les **12** relations du § 5.2 et écrivez, pour chacune, la requête de
contrôle d'unicité. Combien de requêtes différentes obtenez-vous, et pourquoi ?

**Exercice 4.2.** `fait_commandes` porte **trois** dates pour **une** table de dates. Un collègue
propose de créer trois tables de dates, une par date. Donnez deux conséquences de cette solution, une
bonne et une mauvaise, et dites ce que vous retenez.

**Exercice 4.3.** Écrivez la définition de la mesure du taux de service en précisant qu'elle lit la
**date promise**, et expliquez pourquoi cette activation ne doit pas s'appliquer au reste du rapport.

**Exercice 4.4.** `dim_client_scd` compte **24 893** lignes pour **23 913** clients, dont **900** qui
portent plusieurs versions. Expliquez pourquoi cette table ne peut pas être la dimension du rapport, et
ce qu'il faudrait lui faire pour qu'elle le devienne.

**Exercice 4.5.** Un visuel affiche une rupture par mois, mais les mois sans rupture ont disparu de
l'axe. Écrivez les deux causes possibles dans le modèle, et le contrôle qui permet de trancher.

**Exercice 4.6.** Le rapport affiche **474 681 181 861** FCFA. Écrivez la requête qui prouve que la
cause est la colonne `annee_mois`, et dites pourquoi le facteur trouvé — **30,44** — n'est pas un nombre
entier.

---

## 12. Correction détaillée

**Exercice 4.1.** Une seule requête, répétée **12** fois avec d'autres noms de table et de colonne :
`SELECT COUNT(*) AS lignes, COUNT(DISTINCT <cle>) AS cles FROM <dimension>` — la requête ne change que
par ses identifiants, jamais par sa forme. La comparaison des deux nombres suffit : **23 913** contre
**23 913**, **154** contre **154**, **6** contre **6**, **22** contre **22**, **1 339** contre
**1 339**. Un écart, et la relation ne se déclare pas.

**Exercice 4.2.** Trois tables de dates multiplient les chemins de filtrage : un segment posé sur l'une
n'atteint pas les deux autres, et **l'ambiguïté de relation** apparaît dès que deux dimensions portent
la même information. Le bon côté : chaque date aurait son calendrier complet, et le taux de service
n'aurait plus besoin d'une relation inactive — c'est d'ailleurs la solution retenue par certains
modèles, au prix d'un segment « période » par date. On retient la solution du socle : **une** table de
dates, marquée, et une relation inactive activée dans la mesure, parce qu'un rapport se lit sur **une**
échelle de temps.

**Exercice 4.3.** La mesure compte les commandes livrées au plus tard à la date promise, divisées par les
commandes livrées, et elle active la relation inactive dans son propre calcul :
`DIVIDE([Commandes à l'heure], CALCULATE(COUNTROWS(fait_commandes), fait_commandes[statut] = "livree"))`.
L'activation ne doit pas s'étendre au reste du rapport : si la date promise filtrait la page, un segment
de période posé par l'utilisateur voudrait dire deux choses à la fois — « les commandes passées en
juin » et « les commandes promises en juin » — et le rapport rendrait un nombre juste à une question que
personne n'a posée.

**Exercice 4.4.** Sur **24 893** lignes, **900** clients apparaissent plusieurs fois : la clé n'est pas
unique, donc la table ne peut pas être le côté « un » — l'outil multiplierait les lignes du fait à chaque
version. Pour qu'elle le devienne, il faut la **réduire au grain du client** : garder une ligne par
`id_client`, celle de la version courante, et laisser l'historique aux analyses de M13. Une dimension de
rapport décrit l'état **actuel** ; une table de versions répond à une autre question.

**Exercice 4.5.** Première cause : le visuel s'appuie sur une colonne de date portée par le fait, et le
mois sans rupture n'existe pas dans les données. Deuxième cause : les ruptures sont reliées à une table
de dates marquée dont le filtre se propage par `annee_mois`, et la jointure écrase les mois — ou en
crée. Le contrôle qui tranche : `SELECT COUNT(*) FROM dim_date WHERE annee_mois = '2026-08'` — **31**
lignes signalent la seconde cause ; **1** ligne pour un mois, et le problème est dans le visuel.

**Exercice 4.6.** La requête repose le **premier piège du § 5.6** et compare les deux totaux :
`SELECT SUM(v.montant_ttc) FROM fait_ventes v JOIN dim_date d ON d.annee_mois = strftime(v.date_vente,
'%Y-%m') WHERE v.est_retour = 0` rend **474 681 181 861** FCFA, quand la jointure par `date` rend
**15 595 154 955** FCFA. Le facteur **30,44** n'est pas entier parce que les mois n'ont pas tous le même
nombre de jours : **28** pour février, **31** pour août, et **1 339** jours pour **44** mois — la moyenne
tombe entre les deux, et c'est justement le signe que la multiplication vient du **calendrier**, pas
d'une donnée.

---

## 13. Mini-projet de chapitre — le schéma du modèle

**Énoncé.** Produisez le **schéma du modèle** du rapport : la liste des **12** relations déclarées, les
**2** relations inactives avec leur raison, les **2** filtrages bidirectionnels refusés avec le motif du
refus, et la recette du modèle en **10** valeurs.

**Barème indicatif** : la liste des **12** relations avec cardinalité et sens du filtre (**6** points) ·
les **2** inactives et les **2** refus argumentés (**6** points) · le contrôle d'unicité des colonnes de
dimension, écrit avec ses valeurs (**4** points) · la recette en **10** valeurs avec la comparaison à M12
(**2** points) · sur **18** points.

> **Pourquoi ce mini-projet.** Parce que le schéma est la seule pièce qui explique **pourquoi** le
> rapport est juste. Un rapport qui fonctionne sans schéma écrit est un rapport qu'on ne peut ni
> transmettre, ni corriger, ni auditer — et c'est la troisième pièce qui entrera dans le dossier de
> conception du projet.

---

## 14. Résumé du chapitre

| Notion | Mesure du module | Ce qu'elle enseigne |
|---|---|---|
| Tables du rapport | **12** : **5** dimensions, **7** faits | le modèle vient de M13, il se déclare, il ne se redessine pas |
| Relations actives | **12**, toutes plusieurs à un | la cardinalité n'est pas un détail, c'est la règle |
| Unicité | **12** colonnes uniques sur **12** | la seule condition d'une relation, et elle se vérifie |
| Relations inactives | **2** sur les trois dates de la commande | un fait peut porter trois temps, une table de dates une seule échelle |
| Bidirectionnels | **2** examinés, **2** refusés | un filtre bidirectionnel est une décision, pas une commodité |
| Piège du module, la date | `annee_mois` : **28** à **31** lignes par mois (**44** valeurs, **1 339** jours) | une colonne non unique ne joint pas |
| Piège du module, les faits | deux faits joints : facteurs **30,44** et **44,0** mesurés | deux faits ne se joignent jamais entre eux |
| Recette | **8** comparaisons avec M12, **0** écart | un modèle se juge à sa sortie |

**Instrument.** `python3 tools/mesures_M14.py` vérifie les **12** relations, l'unicité des **12**
colonnes, les **2** inactives, les **2** refus, et rejoue la recette du modèle par
`controle_croise()`. Les gestes, eux, se rejouent devant votre écran.

**Le module en une ligne.** Les trois premiers chapitres ont posé l'outil, sa licence, ses sources et
ses transformations ; celui-ci a posé le **modèle** — et il a montré qu'une relation n'est pas un trait
entre deux tables, mais un choix en trois parties, dont dépend la justesse de tout ce que le rapport
affichera.

---

## 15. À retenir

1. **Une relation, trois décisions** : la cardinalité, la direction du filtre, l'état. Les ignorer, c'est
   dessiner ; les écrire, c'est modéliser.
2. **L'unicité est la seule condition.** **12** colonnes de dimension uniques, **12** relations sûres ;
   une colonne qui se répète — `annee_mois`, **28** à **31** lignes par mois — et le rapport multiplie
   par **30,44**. Deux faits joints entre eux, et il multiplie par **44,0**.
3. **Le modèle se contrôle par sa sortie** : les **10** valeurs du rapport, **8** comparaisons avec la
   mesure opérationnelle de M12, **0** écart. Aucun autre argument ne vaut.

> **À retenir.** Écrivez le schéma du modèle **avant** de dessiner le premier visuel : **12** relations,
> **2** inactives, **2** refus, **11** mesures. Ce document tient sur une page, et c'est lui qui rendra la
> page d'aide du rapport vraie — parce que la page d'aide d'un tableau de bord n'est rien d'autre que le
> modèle expliqué à quelqu'un qui ne l'a pas construit.

---

## 16. Évaluation formative

1. Combien de relations le rapport du fil rouge déclare-t-il, et combien de tables du modèle en sont à
   l'origine ?
2. Quelle est la seule condition d'une relation plusieurs à un ?
3. Pourquoi la relation sur la date promise est-elle inactive, et où s'active-t-elle ?
4. Que se passe-t-il si l'on relie `fait_ventes` à `dim_date` par `annee_mois`, et si l'on relie
   `fait_ventes` à `fait_logistique` ?
5. Citez les deux candidats au filtrage bidirectionnel et la raison de leur refus.
6. Pourquoi `dim_client_scd` ne peut-elle pas servir de dimension au rapport ?
7. À quoi sert de marquer une table comme table de dates ?
8. Où vit le coût d'achat du produit, et pourquoi n'est-il pas dans le fait ?
9. Pourquoi la sécurité au niveau des lignes se pose-t-elle sur le modèle et non dans les mesures ?
10. Comment sait-on qu'un modèle est juste ?

**Corrigé.** 1. **12** relations actives, issues de **4** des **7** tables de faits (**3** faits restent
sans relation). 2. La colonne du côté « un » doit être **unique** — vérifié **12** fois sur **12**.
3. Parce que `fait_commandes` porte **trois** dates pour une seule table de dates : elle s'active dans
la mesure du taux de service, qui lit la promesse de livraison, et jamais dans le filtre du rapport.
4. `annee_mois` porte **28** à **31** lignes par mois : le chiffre d'affaires devient **474 681 181 861**
FCFA, facteur **30,44**. Deux faits joints entre eux — ventes × logistique sur le magasin seul —
donnent **10 436 404** lignes et **686 186 818 020** FCFA, facteur **44,0** : le second piège, mesuré par
M13.
5. `fait_ventes` vers `dim_client` (ambiguïté de relation avec les encaissements et les commandes) et
`fait_ruptures` vers `dim_produit` (le filtre remonterait d'un fait vers une dimension partagée par
trois autres faits). 6. Parce que sa clé n'est pas unique : **24 893** lignes pour **23 913** clients,
dont **900** qui portent plusieurs versions. 7. À donner une échelle de temps continue : un mois sans
vente s'affiche à zéro au lieu de disparaître, et les comparaisons de périodes restent alignées. 8. Dans
la **dimension** produit, apporté par une fusion de requêtes : **154** produits, **237 191** lignes de
vente : un coût est un attribut du produit, pas de la vente. 9. Parce qu'un filtre posé dans une mesure
se contourne en changeant de page, alors qu'un filtre posé sur le modèle s'applique à tout ce qui sort.
10. En rejouant la recette : les **10** valeurs du rapport, **8** comparaisons avec la mesure
opérationnelle de M12, **0** écart.
