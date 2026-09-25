# Projet M14 — « Le tableau de bord commercial », puis « la version 2, après les retours »

**Module : M14 — Power BI : de l'import à la publication · deux projets · 20 points chacun · seuil de
réussite 13 · environ 8 h pour le premier, 6 h pour le second.**

**Le mandat du premier projet.** Sahel Distribution a un modèle de données propre, construit en M13, et
zéro tableau de bord. La direction veut voir, chaque lundi, où va l'activité du réseau. La consigne,
textuelle : « **trois pages**, quatorze visuels, quatre segments, une page d'aide — et je veux pouvoir
dire, pour chaque visuel, à quelle décision il sert. »

**Le mandat du second projet.** Trois semaines après la publication, onze retours arrivent du comité
d'utilisateurs — ils sont fournis avec le dossier du module, dans le désordre, certains contradictoires,
un demande une donnée que l'entreprise ne produit pas. La consigne : « triez, faites, refusez — et
écrivez pourquoi. »

---

## 1. Énoncé du projet P1 — le tableau de bord commercial

### Le matériel fourni

| Pièce | Ce qu'elle contient |
|---|---|
| `modele_powerbi.md` | les **12** relations à déclarer, les **2** inactives, les **15** gestes de transformation, les **11** mesures avec leur code, les **3** pages et les **14** visuels, les **4** signets |
| `rapport_avant.md` | l'état des lieux en **8** points : aucun tableau de bord, quatre extractions manuelles par mois, un fichier partagé par messagerie |
| `grille_conception_M14.md` | la grille en **18** points, enrichie de ses **6** sous-questions |
| `dossier_M14/connexion.py` | la connexion au socle, réutilisable telle quelle |
| `dossier_M14/ATTENDU.json` | les **12** valeurs du rapport et les **15** compteurs du module, à retrouver |

### Les douze valeurs de contrôle

Le rapport doit afficher, sans filtre, les valeurs suivantes — ce sont celles du socle, et elles ne se
discutent pas : chiffre d'affaires net **15 595 154 955** FCFA · taux de marge **29,12 %** · panier moyen
**107 396** FCFA · taux de rupture **7,29 %** · rotation **9,42** · retours **1,17 %** des lignes et
**1,91 %** des tickets · taux de service **81,0 %** des livraisons et **78,2 %** des commandes · encours
client **1 202 550 590** FCFA · coût par colis **3 284** FCFA · premier magasin **34,1 %** du réseau.

**Les quatre livrables.**

### L1 — Le modèle et les mesures (6 points)

Le modèle du rapport : les **12** relations déclarées, les **2** relations inactives justifiées, la table
de dates marquée et la relation active choisie, les **11** mesures écrites avec leur fiche — nom, question,
haut, bas, format, chiffre de contrôle — et les définitions écrites. Attendu : les **12** valeurs de
contrôle retrouvées sans filtre, et les **2** ambiguïtés du socle traitées par une décision écrite.

### L2 — Les trois pages et les quatorze visuels (6 points)

Les **3** pages — Direction (**5** visuels), Commercial (**5**), Approvisionnement (**4**) — plus les deux
pages de détail et la page d'aide. Chaque visuel porte sa question écrite, son tri, son échelle réglée sur
les valeurs, son unité et sa période. Attendu : les **6** erreurs de visuel du chapitre C06 absentes, et
la jauge de l'objectif capable d'afficher un taux de réalisation de **259,1 %**.

### L3 — Les filtres, l'exploration et l'accessibilité (5 points)

Les **4** segments et leur synchronisation, les interactions réglées avec leur direction, l'exploration à
deux niveaux, les info-bulles, et les exigences d'accessibilité — contraste, statuts non portés par la
couleur seule, titres explicites, table de données. Attendu : le périmètre de chaque taux écrit, et la
phrase qui explique pourquoi le panier d'une famille (**128 958** FCFA en plomberie) n'est pas celui du
réseau (**107 396** FCFA).

### L4 — La mise en production et la fiche de vie (3 points)

Les **6** rôles de sécurité, l'actualisation planifiée, l'abonnement et l'alerte, les **7** tests passés,
la grille en **18** points remplie par un pair, et la fiche de vie du rapport — public, propriétaire,
source, fréquence, rôles, revue. Attendu : les **3** écarts possibles du projet P1 traités, et la décision
sur la table que la sécurité ne filtre pas (le stock, **6 776** lignes sans magasin).

---

## 2. Énoncé du projet P2 — la version 2, après les retours

Les **11** retours du comité sont fournis dans `retours_comite.md`, tels qu'ils ont été dits. Ils ne
sont pas tous à prendre : il faut trier, faire, et refuser en écrivant pourquoi.

**Les quatre livrables.**

### V1 — Le tri des retours (5 points)

Un tableau des **11** retours : ce qui est demandé, ce que cela cache, la décision — **faire**,
**reformuler** ou **refuser** — et la raison en une phrase. Attendu : au moins **3** refus argumentés, et
chaque renvoi vers une autre version clairement daté.

### V2 — Ce qui se fait, et la preuve (5 points)

Les corrections retenues, appliquées et prouvées : la cause du chiffre d'affaires divergent entre les
pages (retour n° **1**), le rôle de sécurité au niveau des lignes (n° **2**), la traduction des libellés
(n° **4**), la devise portée par le visuel (n° **5**), l'exploration par clic (n° **8**), la convention de
signe des retours écrite (n° **9**), la lenteur mesurée et corrigée (n° **10**). Attendu : pour chaque
correction, l'avant, l'après, et la mesure qui le prouve.

### V3 — Ce qui se refuse, et pourquoi (5 points)

Les refus, chiffrés : la donnée horaire que le socle ne produit pas (n° **3**), les douze indicateurs sur
une page (n° **6**), la couverture en semaines hors périmètre (n° **11**), et tout ce que vous jugez
disproportionné — un refus se défend par une mesure, pas par un avis.

### V4 — La version 2, publiée et documentée (5 points)

La nouvelle version publiée — pages, mesures, filtres, rôles — avec sa note de changement : ce qui
change, ce qui ne change pas, et ce que la ligne de base devient. Attendu : la grille en **18** points
repassée, et la phrase qui dit ce qui ne sera **pas** fait dans le trimestre.

---

## 3. Le barème des deux projets

| Projet | Livrable | Points |
|---|---|---|
| **P1** | L1 — modèle et mesures | **6** |
| **P1** | L2 — trois pages et **14** visuels | **6** |
| **P1** | L3 — filtres, exploration, accessibilité | **5** |
| **P1** | L4 — mise en production et fiche de vie | **3** |
| **P1** | **Total** | **20** |
| **P2** | V1 — tri des **11** retours | **5** |
| **P2** | V2 — corrections et preuves | **5** |
| **P2** | V3 — refus chiffrés | **5** |
| **P2** | V4 — version 2 publiée et documentée | **5** |
| **P2** | **Total** | **20** |

Le seuil de réussite est de **13** points sur **20** pour chacun. Les **7** points d'écart sont votre
marge : un projet se réussit avec un livrable manquant, à condition que le rapport s'ouvre, que les
chiffres de contrôle tombent juste et que les décisions soient écrites.

---

## 4. Ce qui fait rejeter un livrable

1. **Un chiffre de contrôle faux.** **15 595 154 955** FCFA, **107 396** FCFA, **29,12 %** : un écart,
   même petit, invalide le livrable qui le porte.
2. **Un visuel sans question écrite.** Il ne se défend pas, donc il ne compte pas.
3. **Un taux sans périmètre.** Publier **7,29 %** sans dire les **6** magasins du numérateur et les
   **5** du dénominateur, c'est publier un chiffre qui sera contesté en réunion.
4. **Une sécurité déclarée mais non testée.** Un rôle qui n'a pas été ouvert avec un compte de test n'a
   pas été livré.
5. **Un refus sans mesure.** « Trop de visuels » n'est pas un refus : « douze indicateurs sur une page,
   alors que le rapport tient **14** visuels sur **3** pages et que la page s'ouvre en quelques
   millisecondes par visuel » en est un.
6. **Une donnée inventée.** Le retour n° **3** demande un chiffre d'affaires horaire : la table de ventes
   porte une date sans heure. Une donnée absente se collecte, elle ne s'approxime pas.
7. **Un rapport qui ne s'ouvre pas dans le temps imparti**, ou dont l'actualisation échoue sans que
   personne ne soit prévenu.

---

## 5. Déroulé conseillé

**Projet P1 — environ 8 h, en 4 séances.**

| Séance | Ce qui se fait | Ce qui se livre |
|---|---|---|
| 1 (2 h) | import, transformation, relations, table de dates | modèle posé, relations contrôlées |
| 2 (2 h) | les **11** mesures et leurs fiches | les **12** valeurs de contrôle au vert |
| 3 (2 h) | les **3** pages, les visuels, les échelles, le thème | pages dessinées, questions écrites |
| 4 (2 h) | filtres, exploration, sécurité, actualisation, tests | dossier de mise en production |

**Projet P2 — environ 6 h, en 3 séances.**

| Séance | Ce qui se fait | Ce qui se livre |
|---|---|---|
| 5 (2 h) | lecture des **11** retours, tri, décisions | tableau de tri daté |
| 6 (2 h) | corrections appliquées et mesurées | avant/après pour chaque correction |
| 7 (2 h) | refus rédigés, version 2 publiée, grille repassée | note de changement, ligne de base |

Total du module : environ **14 h** de projet, sur les **30 h** que compte M14.

---

## 6. Comment vous corriger vous-même

Avant de rendre, passez les **7** tests de mise en production du chapitre C08, puis la grille en
**18** points — deux fois : une fois seul, une fois en la faisant remplir par quelqu'un qui n'a pas
construit le rapport. Trois vérifications terminales :

1. **les chiffres** : `python3 tools/mesures_M14.py` puis comparaison avec `ATTENDU.json` — les **12**
   valeurs du rapport doivent tomber au même arrondi ;
2. **la cohérence** : le chiffre d'affaires net est-il identique sur les trois pages, au visuel et dans le
   détail ? Un écart signale deux définitions, et le retour n° **1** du comité porte exactement sur ce
   cas ;
3. **les décisions** : chaque visuel a sa question, chaque taux son périmètre, chaque refus sa mesure.
   Ce qui n'est pas écrit n'a pas été décidé.
