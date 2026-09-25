# Plan M14 — Construire un tableau de bord avec Power BI : de l'import à la publication

**Huit chapitres · 30 h · niveau N4 · budget 117 pages [99, 135] · deux projets (« Dashboard commercial
professionnel » — *tableau de bord* — puis « Version 2, après les retours des utilisateurs », **20** points chacun, seuil
**13**) · évaluation **80** points (quiz **15** Q, **4** exercices pratiques, étude de cas « le client
ne comprend pas le tableau de bord »).**

**Position dans le parcours.** M14 est le module qui **outille** ce que M13 a modélisé. M12 a nommé les
**10** indicateurs et leur carte, M13 a bâti le modèle **14** tables et l'a prouvé par **4** contrôles :
M14 prend ce modèle, l'importe dans un outil de restitution, le publie et le fait vivre. Le module
s'arrête **au seuil du DAX** : il écrit les mesures de survie d'un rapport et laisse le langage complet
à M15, parce qu'un rapport juste se construit d'abord avec un bon modèle.

**La contrainte d'atelier, dite tout de suite.** Power BI Desktop **n'est pas installable** dans cet
atelier : aucun chapitre n'exécute l'outil. Chaque geste est donc écrit **pas à pas**, avec son libellé
exact dans l'interface, et ce qui peut être mesuré l'est **en SQL** — les **10** valeurs que le tableau
de bord doit afficher sont calculées par `tools/mesures_M14.py` et deviennent la référence de contrôle
de l'apprenant. Déclaration §1.5 : **Power BI cité, non exécuté ; DuckDB 1.5.5 et pandas exécutés.**

---

## 1. Cadrage

### 1.1 Position dans l'architecture

| Source | Ce qui est repris tel quel |
|---|---|
| `00_architecture/01_architecture_pedagogique.md` §M14 | **8** chapitres de **4/4/4/4/4/4/4/2** h (30 h), N4 ; prérequis M05.C02, M10, M12, M13 ; les **2** projets ; l'évaluation (quiz 15 Q, exercices pratiques dont « ce tableau de bord affiche un total double », étude de cas « le client ne comprend pas le tableau de bord ») |
| §E.7 | la **grille de conception en 18 points**, répartition **4 / 5 / 5 / 4** en quatre familles (décision servie, justesse, lisibilité, utilisation), avec sa version auto-évaluée **et** sa version relue par un pair ; le module l'**enrichit** de **6** sous-questions (performance, cohérence des totaux, accessibilité, légende, granularité, gestion des vides) **sans changer le total de 18** — chaque ajout entre dans une case existante |
| §B.6 | quiz **20** points seuil **14** ; projet **20** points seuil **13** (M14 en porte **2**, comme prévu) ; étude de cas **30** points seuil **18**, barème du manuel |
| §E.3 | les **30** projets du manuel : M14 en apporte **2**, les deux seuls du parcours avec M18 |
| `tools/budget_pages.py` | **8** × 12,5 = **100** p. de matière + **17** p. d'appareil = **117** p. ; fourchette ± 15 % = **[99, 135]** |
| Décisions de M12 et M13 (à ne pas défaire) | le modèle importé est celui de M13 (**14** tables, **7** faits) ; les **10** indicateurs sont ceux de la carte M12 ; le taux d'actualisation, les segments et le grain ne sont **pas** rediscutés |
| Frontières de modules | M14 ne réenseigne **pas** Power Query (M05.C02), ni la perception graphique (M10), ni la définition d'un KPI (M12), ni la modélisation (M13), ni le DAX (M15), ni l'automatisation hors outil (M17). Il **traduit** les quatre premiers dans l'outil et s'arrête avant les deux derniers |

### 1.2 Huit compétences de sortie (la matrice de couverture)

| # | Compétence | Chapitre | Ce qui la prouve dans le module |
|---|---|---|---|
| 1 | Comprendre l'écosystème et savoir ce qui se paie | C01 | les **4** surfaces (Desktop, Service, Fabric, Mobile) et les **4** formules de licence chiffrées |
| 2 | Obtenir la donnée et choisir le **mode de connexion** | C02 | les **4** modes comparés sur le fil rouge : coût d'actualisation, taille, fraîcheur |
| 3 | Transformer proprement, en gardant la trace des gestes | C03 | la requête du fil rouge en **15** gestes nommés, rejouable, sans étape orpheline |
| 4 | Monter un **modèle juste** dans l'outil | C04 | les **12** relations du modèle M13, cardinalités et sens du filtre, **2** ambiguïtés guéries |
| 5 | Écrire les **mesures de survie** et refuser les colonnes calculées inutiles | C05 | les **11** mesures du tableau de bord, chacune avec sa définition et son format |
| 6 | Construire des pages lisibles et navigables | C06 | **3** pages, **14** visuels, **1** page d'aide, un thème et **4** signets |
| 7 | Faire parler un rapport : filtres, interactions, exploration | C07 | page, visuel et rapport filtrés ; segment synchronisé ; exploration à deux niveaux |
| 8 | Publier, actualiser, sécuriser et **tester** | C08 | espace de travail, application, permissions, actualisation planifiée, passerelle, sécurité au niveau des lignes, **18** points de grille passés avant publication |

### 1.3 État de l'art logiciel, vérifié en septembre 2026 (les constantes du module)

Le module enseigne un **produit** : ses prix et ses limites doivent être datés et vérifiables. Ces
constantes entrent au relevé sous des clés `m14_prix_*` et seront revérifiées à chaque réédition.

| Fait | Valeur retenue (septembre 2026) | Conséquence pour le module |
|---|---|---|
| Power BI Desktop | **gratuit**, création et analyse locales | tout le module se fait sans licence ; seul le **partage** en exige une |
| Power BI Pro | **14** USD par utilisateur et par mois (engagement annuel) ; inclus dans certaines offres Microsoft 365 | le partage dans un espace de travail : c'est la formule d'une PME |
| Premium Per User | **24** USD par utilisateur et par mois (annuel) | modèles jusqu'à **100** Go, **48** actualisations par jour, rapports paginés |
| Capacité Fabric | à partir de **F64** (**64** unités de capacité, équivalent de l'ancien P1) : les lecteurs en licence **gratuite** consultent ; en dessous de F64, chaque lecteur paie | c'est le seuil qui change l'économie : **1** payeur contre des centaines de lecteurs |
| Anciennes capacités **P** | plus commercialisées, migrées vers les offres **F** | le module dit quoi faire d'un contrat en cours, et ne l'enseigne pas comme un choix neuf |
| Limites par formule | Pro : modèle **1** Go, **8** actualisations par jour ; PPU : **100** Go, **48** | la taille du fil rouge (**240 000** ventes) tient largement dans la formule gratuite : le module le **prouve** |
| Taux de conversion retenu | **1** USD = **600** FCFA, taux pédagogique fixe | **14** USD ≈ **8 400** FCFA · **24** USD ≈ **14 400** FCFA — tous les prix sont donnés dans les deux monnaies |

**Ce que le module ne prétend pas.** Aucun chapitre ne produit de capture d'écran de l'outil : la
consigne de l'atelier interdit d'inventer une interface. Chaque geste est décrit par son libellé, son
emplacement et son effet vérifiable, et le module publie ce qu'il peut mesurer — les **valeurs** que le
tableau de bord doit rendre.

### 1.4 Les deux projets

**M14.P1 — « Dashboard commercial professionnel »** (*tableau de bord commercial
professionnel*) — **20** points, seuil **13**.

| Élément | Exigence |
|---|---|
| Pages | **3** : Direction, Commercial, Approvisionnement |
| Visuels | **14** au total, dont **3** cartes d'indicateur et **1** matrice |
| Segments | **4** : période, magasin, famille de produits, segment de client |
| Détail | **2** pages d'exploration (détail magasin, détail produit) + **1** page d'aide à la lecture |
| Mesures | **10**, nommées selon la règle du manuel, chacune avec sa définition écrite |
| Habillage | **1** thème personnalisé (couleurs et polices du manuel), **1** page d'aide, navigation par boutons |
| Actualisation | documentée : fréquence, mode, passerelle ou absence de passerelle, qui la surveille |
| Validation | la **grille de conception en 18 points** (auto-évaluation **et** relecture par un pair) |

**Barème P1 : 20 points = les 18 points de la grille (4 + 5 + 5 + 4) + 2 points de dossier** (thème et
actualisation documentés). Le module ne double pas les barèmes : la grille **est** la note.

**M14.P2 — « Version 2, après les retours des utilisateurs »** — **20** points, seuil **13**.

Le manuel fournit **11** retours d'un comité d'utilisateurs, tels qu'ils arrivent dans la vraie vie :
mélangés, contradictoires, certains hors périmètre. L'apprenant doit **arbitrer, prioriser et
justifier**, refus compris.

| Les **11** retours du comité | Ce qu'ils obligent à décider |
|---|---|
| 1. « Le chiffre de la page Direction n'est pas celui de la page Commercial. » | chercher la cause dans le **modèle**, pas dans le visuel |
| 2. « Je ne devrais voir que mon magasin. » | sécurité au niveau des lignes, ou filtre par défaut |
| 3. « Ajoutez le chiffre d'affaires par heure de la journée. » | donnée absente : refus argumenté |
| 4. « Mon équipe travaille en anglais. » | traductions des libellés |
| 5. « Les montants en dollars, personne ne les lit ici. » | devise et format |
| 6. « Mettez les **12** indicateurs de la carte sur la première page. » | densité : refus partiel chiffré |
| 7. « Envoyez-le en PDF chaque lundi matin. » | abonnement à un rapport, ou refus assumé |
| 8. « Je veux le détail d'une vente en cliquant sur un magasin. » | exploration par clic, page de détail |
| 9. « Le total des retours est négatif, c'est faux. » | convention de signe, définie et écrite |
| 10. « Il met **40** secondes à s'ouvrir. » | performance : mesure, cause, remède |
| 11. « Je veux la couverture de stock en semaines, pas en ruptures. » | mesure nouvelle, hors du périmètre de M14 |

### 1.5 Évaluation M14 — **80** points, seuil **51**

| Partie | Points | Contenu |
|---|---|---|
| **A. Récupération** | non notée | **5** questions de prérequis (grain, additivité, dimensions conformes, KPI, perception) |
| **B. Quiz** | **20** | **15** questions (seuil **14**) : écosystème et licences, modes de connexion, Power Query, relations, mesures contre colonnes, visuels, filtres, publication |
| **C. Quatre exercices pratiques** | **24** | E1 monter le modèle (**12** relations) · E2 écrire les **11** mesures de survie · E3 lire un plan de requête de l'outil · **E4 « ce tableau de bord affiche un total double »** — diagnostiquer la relation qui duplique |
| **D. Étude de cas** | **30** | « le client ne comprend pas le tableau de bord » : **8** pages décrites, la grille en **18** points passée, puis la première page refaite avec les **3** chiffres justes (seuil **18**) |
| **E. Auto-évaluation** | **6** | la grille de conception remplie sur son propre P1, preuve à l'appui pour chaque point |

**Erratum d'architecture, déclaré.** le §M14 annonce « **3** exercices pratiques (dont un E4 …) » : la
numérotation prouve qu'il y en a **4**. Le plan retient **4** et le signale ici, comme l'erratum des
**18** points du §E.7.

### 1.6 Règles d'exécution (cadence héritée de M06—M13)

1. **Un push par chapitre** validé `--strict`, plus le plan **avant** le socle, et la clôture à la fin.
2. **Tout chiffre** de quatre chiffres ou plus existe dans `chiffres_cites.json` (bloc `M14`), ou est
   reformulé ; les prix de licence sont des **constantes documentaires** datées, jamais des mesures.
3. **Quatre planches** `figures/` : ≤ **776** px, texte latin-1 sans accent, `svg.fonttype = none`,
   déterministes, citées par leur chapitre.
4. **Aucune capture d'écran, aucun faux bouton** : le module décrit les libellés, il ne les dessine pas.
5. **Déclaration §1.5** en tête de chaque chapitre : Power BI cité non exécuté ; DuckDB et pandas
   exécutés ; toute mesure du module porte son origine.
6. **PDF** composé après l'autovalide, contrôlé par `controle_pdf.py M14` (glyphes, planches, bloquants).

### 1.7 Les huit décisions du module (le fil du module)

| # | Question | Décision du module | La mesure ou le fait qui la justifie |
|---|---|---|---|
| 1 | Faut-il une licence pour apprendre ? | **non** : Desktop est gratuit, seul le partage se paie | **14** USD par utilisateur et par mois pour Pro, **0** pour la création locale |
| 2 | Import ou DirectQuery ? | **Import** pour le fil rouge, DirectQuery **cité** avec son cas d'usage | **240 000** lignes de ventes : l'import tient dans un modèle de **1** Go, et **8** actualisations par jour suffisent |
| 3 | Power Query avant ou après le modèle ? | **avant**, et la trace des gestes est une **documentation** | **15** gestes nommés, rejouables, sans étape orpheline |
| 4 | Combien de relations, et dans quel sens ? | les **12** du modèle M13, filtrage à sens unique, sauf **2** exceptions justifiées | un modèle de **14** tables ne se lit pas sans ses cardinalités |
| 5 | Mesure ou colonne calculée ? | **mesure** dès qu'il s'agit d'un calcul de rapport | une colonne calculée se stocke et se rafraîchit ; une mesure se calcule à la lecture |
| 6 | Combien de visuels sur une page ? | **5** au maximum sur la page Direction | la grille en **18** points, famille lisibilité |
| 7 | Qui voit quoi ? | permissions d'espace de travail **et** sécurité au niveau des lignes pour le retour 2 | **6** magasins, dont **1** dépôt sans vente |
| 8 | Quand un rapport est-il publiable ? | quand il passe les **18** points, dont les **6** ajouts du module | le module est le seul à donner la grille complète et sa version relue par un pair |

---

## 2. Vocabulaire du module (à définir au premier emploi)

**Définitions imposées** (encadrés « Définition » des huit chapitres) : *écosystème Power BI*, *espace
de travail* (*workspace*), *application* (*app*), *modèle sémantique* (*semantic model*, ex-jeu de
données), *rapport*, *tableau de bord* (au sens du service), *connecteur*, *mode d'import*, *DirectQuery*,
*connexion directe* (*live connection*), *Direct Lake*, *passerelle* (*gateway*), *actualisation*,
*paramètre de requête*, *requête combinée*, *relation*, *cardinalité*, *sens du filtrage*,
*relation ambiguë*, *table de dates marquée*, *mesure*, *colonne calculée*, *DAX*, *signet* (*bookmark*),
*segment* (*slicer*), *interaction*, *exploration par clic* (*drill-through*), *info-bulle personnalisée*,
*thème*, *abonnement* (*subscription*), *sécurité au niveau des lignes* (*RLS*), *TMDL*, *fonction
utilisateur DAX* (*UDF*), *calendriers améliorés*, *grille de conception*.

**Anglicismes** : toujours appariés — *dashboard* → **tableau de bord**, *pipeline* → **chaîne de
calcul**, *self-service* → **service en autonomie**, *bookmark* → **signet**, *slicer* → **segment**,
*gateway* → **passerelle**, *drill-through* → **exploration par clic**, *refresh* → **actualisation**.
Le mot « dashboard » n'apparaît **jamais** seul dans le module, y compris en titre de projet.

**Ce que le module refuse d'employer.** « Modèle en étoile » reste la traduction de *star schema* ;
« dataset » disparaît au profit de **modèle sémantique** ; « dataflow » n'est cité qu'une fois, à
l'étage de Fabric, parce que M12 l'a déjà nommé.

---

## 3. Découpage en 8 chapitres

| Ch. | Titre | Contenu | Sections | H | Pages |
|---|---|---|---|---|---|
| **C01** | Installer et comprendre l'écosystème | les **4** surfaces (Desktop, Service, Fabric, Mobile) ; ce qui est gratuit et ce qui se paie ; les **4** formules de licence chiffrées ; alternatives sans licence ; ce que Fabric change (et ce qu'il ne change pas) | 16 | 4 | 12,5 |
| **C02** | Obtenir la donnée : connecteurs et modes | les connecteurs du fil rouge (CSV, Excel, dossier, SQL) ; **Import**, **DirectQuery**, **connexion directe**, **Direct Lake** ; la stratégie du cache ; actualisation et passerelle ; erreurs de connexion typiques | 16 | 4 | 12,5 |
| **C03** | Transformer avec Power Query | les **15** gestes sur les données du fil rouge ; types et locale ; colonne conditionnelle ; paramètres et fonctions ; requêtes combinées ; les **3** défauts de requête qui coûtent des performances ; nommer ses étapes | 16 | 4 | 12,5 |
| **C04** | Modéliser : relations, cardinalité, sens du filtre | les **12** relations du modèle M13 dans l'outil ; direction du filtrage et ses **2** exceptions ; dates marquées et la table de dates unique ; intégrité référentielle ; **2** ambiguïtés guéries ; colonnes masquées, tri par colonne | 16 | 4 | 12,5 |
| **C05** | Mesures ou colonnes, et le premier DAX | mesure contre colonne calculée, mesuré sur un cas ; les **11** mesures de survie (`SUM`, `COUNTROWS`, `DISTINCTCOUNT`, `DIVIDE`, `CALCULATE` d'un seul usage) ; formatage ; nommage ; traduction des libellés ; ce que M15 prendra en charge | 16 | 4 | 12,5 |
| **C06** | Construire les visuels | les **3** pages du rapport commercial ; carte, jauge, matrice, barres, courbe ; mise en page et hiérarchie ; **4** signets et la navigation par boutons ; thème et charte ; accessibilité ; les **6** erreurs de visuel qui se voient | 16 | 4 | 12,5 |
| **C07** | Faire parler le rapport | filtres de page, de visuel et de rapport ; **4** segments et leur synchronisation ; interactions entre visuels ; exploration à **2** niveaux et par clic ; info-bulles personnalisées ; Q&A ; performance du rapport | 16 | 4 | 12,5 |
| **C08** | Publier, actualiser, faire vivre | espace de travail et application ; permissions ; actualisation planifiée et passerelle ; modèles réutilisables ; sécurité au niveau des lignes ; abonnements et alertes ; **grille de conception en 18 points enrichie** ; les **7** tests avant mise en production | 16 | 2 | 12,5 |

**Progression interne.** C01 ouvre l'outil et règle la question d'argent ; C02 fait entrer la donnée ;
C03 la nettoie ; C04 la relie ; C05 la calcule ; C06 la dessine ; C07 la fait explorer ; C08 la publie
et la maintient. Chaque chapitre **ajoute une pièce au même rapport** : à la fin, le rapport du fil
rouge existe et passe la grille.

**Le fil rouge du module.** Le rapport « Ventes Sahel Distribution » construit pas à pas : **12**
relations importées du modèle M13, **11** mesures, **3** pages, **14** visuels, **4** segments, **2**
pages de détail, **1** page d'aide. Les **8** chapitres produisent chacun une partie de ce rapport.

---

## 4. Budget pages

| Poste | Pages |
|---|---|
| C01 → C08 (8 × 12,5) | 100 |
| Appareil de module (ouverture, bilan, 2 projets, évaluation) | 17 |
| **Total M14** | **117** |

Fourchette de validation **± 15 %** : **[99, 135]** pages. Contrôle : `tools/budget_pages.py --mesure`
puis `tools/render.py` + `tools/controle_pdf.py M14`.

**Quatre planches prévues** (aucune capture d'écran : uniquement des schémas produits par script) :

1. `M14_C01_ecosysteme_et_licences.svg` — les **4** surfaces et les **4** formules, avec le seuil
   **F64** et les lecteurs gratuits.
2. `M14_C02_quatre_modes_de_connexion.svg` — les **4** modes comparés : où vit la donnée, ce que coûte
   une actualisation, ce qui est disponible hors ligne.
3. `M14_C04_modele_etoile_powerbi.svg` — les **12** relations du modèle M13, cardinalité et sens du
   filtre, avec le cas d'ambiguïté avant et après guérison.
4. `M14_C08_grille_conception_enrichie.svg` — la grille en **18** points (4 + 5 + 5 + 4) avec ses **6**
   ajouts logés dans les cases existantes.

Les autres illustrations du module (anatomie d'une page, cycle d'actualisation, arborescence de
l'espace de travail) sont **décrites en tableaux**, pour ne pas multiplier les images.

---

## 5. Chiffres cibles (à figer dans `chiffres_manuel.py M14`)

**Le modèle importé — repris de M13, jamais recalculé au hasard** : **14** tables (**7** dimensions,
**7** faits) · **12** relations · `dim_client` **23 913** lignes · `dim_produit` **154** · `dim_magasin`
**6** (dont **1** dépôt sans vente) · `dim_vendeur` **22** · `dim_date` **1 339** jours · fait de ventes
**240 000** lignes · ruptures **2 428** · stock mensuel **6 776** · objectifs **218**.

**Les dix valeurs que le tableau de bord doit afficher** (calculées par l'instrument, en SQL, et
comparables à l'écran) : chiffre d'affaires net **15 595 154 955** FCFA · marge **29,12 %** · panier
**107 396** · taux de retour **1,17 %** / **1,91 %** · rupture **7,29 %** · rotation **9,42** tours ·
service **81,0 %** / **78,2 %** · encours **1 202 550 590** · part du magasin de Ouaga 2000 **34,1 %**.

**Les faits d'outil, datés septembre 2026** : Pro **14** USD ≈ **8 400** FCFA par utilisateur et par
mois · PPU **24** USD ≈ **14 400** FCFA · capacité **F64** = **64** unités de capacité, équivalent de
l'ancien P1, à partir de laquelle les lecteurs en licence gratuite consultent · modèle Pro **1** Go et
**8** actualisations par jour · PPU **100** Go et **48** actualisations par jour.

**Les mesures du module** : **15** gestes de Power Query · **12** relations dont **2** exceptions de
sens · **11** mesures · **3** pages, **14** visuels, **4** segments, **2** pages de détail, **1** page
d'aide · **4** signets · **18** points de grille dont **6** ajouts · **11** retours de comité et **7**
tests avant mise en production.

---

## 6. Risques et parades

| Risque | Parade |
|---|---|
| Un module sur un outil absent de l'atelier | tout ce qui peut être mesuré l'est **en SQL** : les **10** valeurs du rapport sont calculées et publiées, et deviennent la référence de contrôle ; les gestes sont écrits **pas à pas** avec leur libellé exact ; la déclaration §1.5 est en tête de chaque chapitre |
| Une documentation qui invente l'interface | interdiction de capture d'écran et de faux bouton dans tout le module ; les planches ne montrent que des schémas de **données** et de **décisions**, jamais des fenêtres |
| Recouvrir M05.C02 (Power Query) | le module ne réexplique pas Power Query : il l'**exerce** sur les données du fil rouge, avec les **15** gestes et les **3** défauts de performance, qui ne sont pas dans M05 |
| Recouvrir M10 et M12 | la perception graphique et la définition d'un KPI sont **citées** avec leur renvoi ; la grille en **18** points est réutilisée, pas réécrite ; les **6** ajouts du module sont explicitement listés |
| Empiéter sur M15 (DAX) | frontière écrite : M14 écrit les **11** mesures de survie et **refuse** les fonctions temporelles ; `CALCULATE` n'est employé qu'une fois, pour montrer qu'il existe, et la bibliothèque de mesures appartient à M15 |
| Deux projets qui se ressemblent | P1 **construit** et se note à la grille ; P2 **arbitre** des retours contradictoires et se note au raisonnement ; le barème de P2 interdit de tout accepter (**3** refus argumentés exigés) |
| Un tableau de bord qui « marche » mais se trompe | l'étude de cas et l'exercice E4 visent exactement la panne la plus fréquente du parcours : les totaux incohérents aux **3** niveaux, dont M13 a déjà mesuré la cause (**× 44,0** pour une jointure trop large) |
| Le prix des licences qui vieillit | ils sont **datés** dans le texte (« vérifié en septembre 2026 »), rangés sous des clés `m14_prix_*`, et le module apprend la démarche : aller chercher le tarif officiel, ne pas le citer de mémoire |

---

## 7. Étapes de production (calque M05—M13)

1. **Étape 1 — Plan** : ce fichier (poussé avant toute rédaction).
2. **Étape 2 — Socle et instruments** : `tools/dossier_M14.py` construit
   `03_exercices/dossier_M14/` : les **12** tables du modèle M13 exportées en CSV d'import
   (`modele_import/`), `modele_powerbi.md` (les **12** relations à déclarer, les **15** gestes de
   requête, les **11** mesures avec leur code, les **3** pages), `retours_comite.md` (les **11**
   retours), `rapport_avant.md` (les **8** pages du cas), `grille_conception_M14.md` (**18** points
   et **6** ajouts, questions fermées), `connexion.py`, `ATTENDU.json` ; `tools/mesures_M14.py` :
   export du modèle, contrôle du dossier, les **10** valeurs attendues (exécutées), la grille en
   **18** points imprimable, les poids d'import ; bloc `m14_*` dans `chiffres_manuel.py`.
3. **Étape 3 — Rédaction** : C01 → C08, un push par chapitre validé `--strict`.
4. **Étape 4 — Figures** : **4** planches (`tools/figures_M14.py`), largeur ≤ **776** px, texte réel,
   déterministes, citées par leur chapitre.
5. **Étape 5 — PDF** : `tools/render.py "0[234]_*/M14_*.md" --join --out 05_livrables/M14.pdf` puis
   `tools/controle_pdf.py M14` — viser **[99, 135]** pages, 0 défaut bloquant.
6. **Étape 6 — Fiche de contrôle** : `05_livrables/fiche_controle_M14.md` (Q1—Q10).
7. **Étape 7 — Projets + évaluation + clôture** : `03_exercices/M14_projet.md` (**2** projets, **20**
   points chacun, seuil **13**), `04_evaluations/M14_evaluation.md` (**80** points, seuil **51**),
   `README.md`, `05_livrables/etat_avancement.md`, `05_livrables/journal_pushs.md`, et le **contrôle
   final d'existence nommée** de chaque livrable (PATCH_6).
