# Plan M10 — Data visualization

**7 chapitres · 30 h · niveau N3 · prérequis M09 · palier P3 (ouverture de la phase 3) · budget 7 × 12,5 + 17 p. d'appareil = 105 p. (±15 % = [89, 121])**

> **Un écart d'architecture relevé à l'étape 1, arbitré ici et signalé pour correction.**
> Le §E.7 de l'architecture définit la grille de conception comme « **20 points, 4 points par
> famille** » ; or elle énumère **4 familles** — 4 × 4 = **16**, pas 20. Les fiches de module,
> elles, annoncent **18 points** (M10 : « grille d'évaluation visuelle en 18 points » ; M14 :
> « grille de conception en 18 points héritée de M10 et enrichie »). **Arbitrage retenu :
> 18 points en 4 familles** — c'est la seule valeur portée par deux documents sur trois, et la
> seule compatible avec la famille « Décision servie » à 4 points. Le §E.7 est donc à corriger
> en « 18 points, 4 familles (4 + 5 + 5 + 4) », au même titre que les autres erratas relevés
> depuis M01. Tant que le §E.7 n'est pas corrigé, **la grille publiée dans M10 fait foi**.

## 1. Cadrage

### 1.1 Position dans l'architecture

- **Phase** 3 — Communication analytique, **seul module de la phase** (30 h) : après M09 qui
  installe le protocole d'exploration, M10 apprend à **rendre visible** ce qu'on a trouvé.
- **Niveau de sortie N3** : l'apprenant produit un graphique **qui répond à une question** et
  **qui le dit** (titre, axes, annotation), pas un graphique qui décore.
- **Prérequis** : M09 (la question avant le chiffre ; les 5 erreurs d'exploration de C06 §5.2,
  qui sont ici reprises et **étendues** aux 10 erreurs qui tuent la crédibilité) ; **aucun
  prérequis graphique** — le module part de l'œil, pas du logiciel.
- **Outil principal** : `matplotlib` (dépendance minimale, exécuté), `seaborn` (confort,
  exécuté), **Excel** (graphiques natifs, exécuté en M03), **Power BI** (cité, non exécutable
  dans cet atelier — même traitement que Power Query en M05 : documenté pas à pas et
  **déclaré non exécuté**).
- **Suite du parcours** : M11 (SQL avancé), M12 (fondements BI), M14 (Power BI) — tous
  réutilisent la **grille en 18 points** et la démarche « le graphique sert une décision ».
- **Artefacts hérités du module** : la **grille de conception visuelle en 18 points**
  (utilisée ensuite en M14, M17, M21) et la **carte de définition des métriques** (artefact
  signature du manuel, objectif 10 de l'architecture, co-signé M10 + M18).

### 1.2 Sept compétences de sortie (la matrice de couverture)

1. **Choisir un graphique par question** — la table des 16 graphiques (11 de la liste + 5 utiles),
   chaque ligne portant sa question, son usage et son piège (§5.1).
2. **Appliquer l'ordre perceptuel** — position > longueur > angle > surface > couleur : ce que
   l'œil lit juste et ce qu'il lit faux, et donc **ce que ça prescrit** dans le choix d'un
   encodage (§5.1 ; C01).
3. **Colorer juste** — palette séquentielle / divergente / catégorielle, contraste et
   **daltonisme** (≈ 8 % des hommes), culture locale des couleurs (§5.3 ; C03).
4. **Écrire un graphique** — titre qui **affirme**, axes **honnêtes**, légende qui ne double pas
   le titre, annotation qui dit le chiffre clé, ordre des barres **trié**, hiérarchie visuelle
   (§5.4 ; C04).
5. **Reconnaître et corriger les 10 erreurs** qui tuent la crédibilité — axe tronqué, double
   axe, 3D, camembert à 9 parts, cumul de pourcentages, couleur qui signifie tout et rien,
   surcharge, zéro manquant, ordre alphabétique, échelle log surprise (§5.5 ; C05).
6. **Composer une séquence de storytelling visuel** — écran → insight → décision, une idée par
   écran, la question du décideur en tête (§5.6 ; C06).
7. **Mettre en œuvre** — le même constat en `matplotlib`, en Excel et dans Power BI ; choisir
   le support, la résolution et le format d'export (§5.7 ; C07).

### 1.3 Fait du socle (à mesurer à l'étape 2 — `chiffres_manuel.py M10`)

Le socle de M10 est **la refonte d'un rapport existant** : `tools/dossier_M10.py` (graine 46)
produit un dossier `03_exercices/dossier_M10/` composé de :

- **5 graphiques volontairement ratés** (`rapport_avant/` : 5 SVG + le code qui les produit) et
  des **2 pages de rapport** qu'ils illustrent — chacun portant **un défaut dominant**
  (axe tronqué, double axe, camembert surchargé, cumul de %, 3D/surcharge) ;
- **les données de la refonte** : le fil rouge commercial (réexport M07/M08/M09, empreinte
  `b9a8d973119342ec…`) + le centre de santé + l'établissement scolaire — le module ne crée
  **aucune donnée nouvelle**, il change le **regard** ;
- **`rapport_apres/`** : la version corrigée de référence (5 SVG), à ne consulter qu'après ;
- **`ATTENDU.json`** : les mesures des défauts (l'amplitude **réelle** face à l'amplitude
  **affichée** de chaque graphique raté, la somme des parts du camembert, la part cumulée du
  graphique en cumul, etc.), toutes sourcées dans `chiffres_cites.json` (clés `m10p_*`).

**Le fait du socle à mesurer, et qui porte le module** : pour chaque graphique raté, l'écart
**entre ce que l'œil croit lire et ce que les données disent** — c'est la mesure la plus utile
du module, et elle est déjà chiffrable sur les défauts de M09 (axe 310-350 M sur un CA plat,
nuage sans n, barres de rapport 8). Objectif : **≈ 30 clés `m10_*`/`m10p_*`**, 2 runs `diff` = 0.

### 1.4 Le projet M10.P — « La refonte » (3ᵉ pièce du portfolio)

- **Énoncé.** Reprendre les **5 graphiques ratés** du rapport fourni, les **corriger**, et
  **expliquer chaque choix** ; produire **deux versions du même constat** : une version
  **« direction »** (1 écran, l'idée et la décision) et une version **« équipe opérationnelle »**
  (les détails, les ordres de grandeur, les libellés exacts).
- **Livrables** (grille /20, seuil 13) :
  - **P1 — Le diagnostic des 5 défauts** (5 pts) : pour chaque graphique, **nommer** le défaut,
    **mesurer** l'écart qu'il crée, et dire **quelle décision il ferait prendre à tort**.
  - **P2 — Les 5 graphiques corrigés** (6 pts) : le bon graphique pour la question, titre qui
    affirme, axes honnêtes, annotation du chiffre clé, couleur justifiée.
  - **P3 — Les deux versions** (5 pts) : direction (1 écran, hiérarchie évidente) et équipe
    opérationnelle (le même constat, plus fin, sans contradiction de chiffres entre les deux).
  - **P4 — La grille en 18 points, auto-évaluée** (4 pts) : l'apprenant note sa propre refonte,
    puis la note est **revue par un pair** (deux notes, l'écart commenté).
- **Règle du module.** Une refonte qui **change le chiffre** en changeant le graphique est
  **rejetée** : les totaux des versions avant/après doivent être **identiques** (contrôle
  automatique par `tools/controle_refonte_M10.py`).

### 1.5 Évaluation M10

- **Quiz** 15 Q (dont 5 « prédisez l'effet » : on donne un graphique raté, l'apprenant **prédit**
  la conclusion fausse que le lecteur en tire, avant la correction).
- **Exercices argumentés** (3, type E3 du §E.4) : « choisissez le graphique, justifiez par la
  question » — **la justification pèse plus que le choix**.
- **Étude de cas notée** : « **ce graphique a déclenché une décision fausse** » — un axe tronqué
  a fait voter une réorganisation ; l'apprenant reconstitue la chaîne
  (défaut → lecture fausse → décision) et propose la version qui ne l'aurait pas permis.
- **Grille visuelle en 18 points** : fournie, auto-évaluée, puis utilisée **dans tous les
  dashboards du parcours** (M14, M17, M21) — c'est un artefact réutilisable, pas un barème jetable.

### 1.6 Règles d'exécution (cadence héritée de M06—M09)

- **1 push par chapitre validé `--strict`** (7 pushes) + plan + socle + figures/PDF + clôture.
- Push forcé autorisé ; **token re-testé via curl avant chaque push** ; **bundle avant
  `rm -rf .git`** ; le `.git` local est supprimé après chaque push.
- **Tous chiffres ≥ 4 chiffres sourcés** dans `chiffres_cites.json` (section `M10`, clés
  majuscules) ; les **bornes** en mots ; **tables non exemptées**.
- **Règles typographiques** : glyphes du jeu latin-1 étendu (chaque glyphe du `.md` doit sortir
  dans le PDF — `controle_pdf.py`) ; anglicismes avec couple français au premier emploi
  (**« nuage de points »**, **« carte de chaleur »**, **« axe tronqué »**, « tableau de bord »
  plutôt que *dashboard* — la règle du manuel).
- **§1.5** : `matplotlib`/`seaborn`/Excel **exécutés** ; **Power BI cité sans exécuté** (déclaré
  dans les encadrés « Dans les faits »).
- **Leçon PATCH_6** : avant toute clôture, vérifier l'**existence nommée** (ls) de chaque
  livrable du plan, pas l'affirmation de la fiche.

### 1.7 Les 16 graphiques (liste de référence — le fil du module)

Les **11 de la liste fondatrice** : histogramme · barres · courbe · camembert · nuage de points ·
boîte à moustaches · carte de chaleur · carte géographique · cascade (*waterfall*) · entonnoir
(*funnel*) · graphique combiné. Les **5 autres utiles** : aire empilée · treemap · jauge et
graphique à puces (*bullet*) · petits multiples (*small multiples*) · diagramme de flux (Sankey).

**Le tableau complet (16 lignes × 5 colonnes) est le cœur du chapitre C02** : question servie,
encodage perceptuel dominant, usage métier, piège, et **le chiffre du socle** qui l'illustre.

## 2. Vocabulaire du module (à définir au premier emploi)

| Terme (français) | Équivalent anglais | Définition en une phrase |
|---|---|---|
| **ordre perceptuel** | *perceptual order* | La hiérarchie de précision de l'œil : position > longueur > angle > surface > couleur — ce que ça prescrit dans le choix d'un codage. |
| **encodage** | *encoding* | La traduction d'une variable en un attribut visuel (position, longueur, couleur, surface). |
| **axe tronqué** | *truncated axis* | Axe des ordonnées qui ne part pas de zéro sans le déclarer : la variation paraît plus forte qu'elle n'est. |
| **carte de chaleur** | *heatmap* | Matrice d'intensités (souvent un tableau croisé) : la couleur code la valeur, la lecture se fait par ligne et par colonne. |
| **petits multiples** | *small multiples* | La même figure répétée sur des facettes de comparaison : la forme se compare, l'échelle reste commune. |
| **palette séquentielle / divergente / catégorielle** | *sequential / diverging / categorical* | Trois usages de la couleur : une progression, un écart à un centre, des groupes sans ordre. |
| **charte de graphique** | *chart style* | Les règles d'une maison (couleurs, titres, unités, source) appliquées à **tous** ses graphiques. |
| **grille de conception (18 points)** | *design checklist* | La grille d'auto-évaluation du module (décision servie, justesse, lisibilité, utilisation), réutilisée en M14/M17/M21. |
| **carte de définition des métriques** | *metrics definition sheet* | Une ligne par indicateur : nom, formule, unité, source, fréquence, propriétaire, piège de lecture. |

## 3. Découpage en 7 chapitres

### C01 — Comment l'œil lit un graphique : l'ordre perceptuel et ce qu'il prescrit (4 h)

**Contenu** : la hiérarchie position > longueur > angle > surface > couleur, vérifiée par des
lectures comparées (le même chiffre codé de 5 façons, et ce que le lecteur en retient) ; les
3 questions de la perception (position relative, longueur, intensité) ; pourquoi un camembert
(angle + surface) est intrinsèquement moins précis qu'une barre (longueur) ; pourquoi une carte
de chaleur se lit par ligne ; les illusions (l'ordre des barres, la pente, l'aire) ; **ce que ça
prescrit** : l'encodage se choisit **après** la question et **avant** le logiciel.
**Sortie** : un graphique exécuté + une lecture comparée chiffrée ; première version de la
**grille en 18 points**.

### C02 — Le tableau question → graphique : les 16 graphiques du manuel (6 h)

**Contenu** : le **tableau des 16** (§1.7), ligne à ligne, chacune illustrée par un graphique
**exécuté sur le socle** : question servie, encodage, usage, piège, chiffre de référence ;
les trois familles de questions (comparer, évoluer, distribuer) et leurs graphiques naturels ;
le graphique qui **ment** sans être faux (camembert à 9 parts, cascade sur des flux qui ne
s'additionnent pas) ; le combiné et le double axe (annoncé ici, condamné en C05) ; les 5
graphiques « utiles » que la liste fondatrice n'avait pas (aire, treemap, bullet, petits
multiples, Sankey) ; le cas du **tableau** comme concurrent d'un graphique (quand un tableau
gagne) ; **la carte de définition des métriques** (artefact signature) : un indicateur sans
définition est un chiffre qui circulera faux.
**Sortie** : 16 graphiques exécutés + la carte des métriques remplie sur le fil rouge.

### C03 — Couleurs, palettes, accessibilité et culture locale (4 h)

**Contenu** : les 3 familles de palettes et le choix par type de variable ; la contrainte de
contraste (le gris sur blanc, le jaune sur blanc) ; le **daltonisme** (≈ 8 % des hommes) et les
palettes qui résistent ; la redondance comme amulette (couleur **+** forme **+** libellé) ; la
couleur qui signifie deux choses (le rouge = retour **et** alerte) ; FCFA et formats numériques
(le séparateur de milliers, la devise, les décimales qu'on ne publie pas) ; la culture locale des
couleurs et la lisibilité à l'écran comme au vidéoprojecteur.
**Sortie** : une charte de graphique de 1 page, appliquée aux 5 graphiques du projet.

### C04 — Écrire un graphique : titres qui affirment, axes honnêtes, annotations (4 h)

**Contenu** : le titre **qui affirme** (« le CA est plat depuis 24 mois ») opposé au titre
**qui étiquette** (« évolution du CA ») ; l'axe honnête (zéro, ou déclaré) et le cas des
données de niveau ; la légende qui ne double pas le titre ; l'**annotation** qui porte le
chiffre clé et **désigne** le point (le pic, la rupture, le plateau) ; l'**ordre des barres**
(trié, jamais alphabétique) ; la hiérarchie visuelle (un chiffre principal, le reste en appui) ;
la source, la date, l'unité dans le graphique (le réflexe qui évite 3 corrections) ; les
5 secondes du décideur.
**Sortie** : les 5 graphiques du projet réécrits (titre, axes, annotation, ordre, source).

### C05 — Les 10 erreurs qui tuent la crédibilité (4 h)

**Contenu** : les **10 erreurs** — axe tronqué, double axe, 3D, camembert surchargé, cumul de
pourcentages qui dépasse 100, couleur qui signifie tout et rien, surcharge (le graphique à
5 séries et 3 axes), zéro volontairement manquant/ajouté, ordre alphabétique des catégories,
échelle logarithmique surprise — chacune avec son **effet mesuré** sur le socle (l'axe 310-350 M
sur un CA plat, la moyenne contre la médiane, l'écart de 2.4 % présenté comme une hiérarchie) ;
**la règle du module** : une erreur n'est pas un péché, c'est une **décision** — elle est
légitime si elle est **déclarée** (axe non zéro annoncé, échelle log annoncée) ; comment
**relire** un graphique en 60 secondes (la lecture qui cherche le défaut, pas la beauté).
**Sortie** : le diagnostic des 5 défauts du rapport fourni, chiffré.

### C06 — Storytelling visuel : composer une séquence (4 h)

**Contenu** : la structure **écran → insight → décision** ; une idée par écran (le contraire du
dashboard-mille-feuilles) ; la séquence qui **répond aux objections d'avance** (le chiffre, le
doute, la limite, la décision) ; le graphique qui prépare le suivant (le zoom en 3 écrans vs
le même écran chargé) ; la version **direction** (1 écran, l'idée et la décision) contre la
version **équipe** (le détail et les libellés) ; la **honnêteté de la séquence** (montrer ce
qui contredit la recommandation — l'héritage direct de M09 : la limite se déclare).
**Sortie** : la séquence de 3 écrans du projet, dans les deux versions.

### C07 — Mettre en œuvre : matplotlib, Excel, Power BI, support et export (6 h)

**Contenu** : `matplotlib` (le geste complet, exécuté : figure, axes, titre, annotation,
sauvegarde, résolution) et le thème maison ; `seaborn` pour le confort (déjà vu en M09.C06, ici
en production : palettes, facettes, styles) ; **Excel** (le graphique natif, les styles, le
graphique combiné, la mise en forme de série) ; **Power BI** (cité, **non exécuté** : la
hiérarchie des visuels, les formats, la page d'aide — documenté et déclaré) ; le **choix du
support** (écran, vidéoprojecteur, PDF, impression noir et blanc — le test) et de la
**résolution** (300 dpi pour l'impression, la lisibilité du texte, le poids du fichier) ;
l'**export** (SVG/PDF vectoriel contre PNG) ; la **charte** appliquée aux trois moteurs pour
que le même constat se reconnaisse.
**Sortie** : le même graphique produit dans les trois outils, avec les écarts documentés.

## 4. Budget pages

| Élément | Calcul | Pages |
|---|---|---|
| Chapitres | 7 × 12,5 | **87,5 → 88 p.** |
| Appareil de module | ouverture, bilan, projet, évaluation | **17 p.** |
| **Total M10** | | **105 p.** |
| Fourchette ±15 % | | **[89, 121] p.** |

**Répartition des 88 p. de chapitres** : C01 12 · C02 14 · C03 12 · C04 12 · C05 13 · C06 12 ·
C07 13 (le tableau des 16 en C02 et le geste des trois outils en C07 sont les deux chapitres les
plus longs ; contrôle final par `tools/budget_pages.py`).

## 5. Chiffres cibles (à mesurer dans `chiffres_manuel.py M10`)

- **Forme du socle** : 5 graphiques ratés (5 défauts dominants distincts), 5 corrigés, 2 pages de
  rapport, 16 graphiques de la table, 18 points de la grille, 4 familles.
- **L'écart qui porte le module** : pour chaque défaut, l'écart mesuré entre **ce que l'œil lit**
  et **ce que les données disent** (en % de variation affichée contre réelle) — mesuré sur le fil
  rouge : un CA plat (320-337 M, ±2,6 %) tracé sur un axe 320-337 affiche une pente qui suggère
  une croissance de plusieurs dizaines de pourcents.
- **Les chiffres déjà disponibles à réutiliser** (aucune donnée nouvelle) : CA mensuel 307-348 M
  et moyenne glissante 320-337 M ; montant max 594 363 × 6 ; panier par mode 156 150-159 959
  (2.4 %) pour des n de 2 552 à 20 175 ; corrélation 0.552 → 0.001 ; segments 123 / 208 / 69 →
  11.13 / 10.51 / 9.76 ; saison santé 857.3 / 770.7 pour un intra-été de 24.03.
- **Objectif** : ≈ 30 clés `m10_*`/`m10p_*`, 2 runs `diff` = 0.

## 6. Risques et parades

| Risque | Parade |
|---|---|
| Le module devient un catalogue de « jolis graphiques » | La règle est écrite dès C02 : **un graphique sans question est un échec**, et la table des 16 porte la **question servie** en première colonne. |
| La couleur traitée comme décoration | C03 la traite comme **contrainte d'accès** (daltonisme, contraste) et la mesure (palettes testées). |
| Power BI non exécutable fait dérailler la règle « tout est exécuté » | Le module **déclare** : `matplotlib`/`seaborn`/Excel exécutés, Power BI cité — encadré « Dans les faits » par chapitre concerné, comme le §1.5 le prévoit. |
| Le projet recopie des corrections « de goût » | P1 impose de **mesurer** l'écart de chaque défaut : la refonte se juge sur l'écart, pas sur l'esthétique. |
| La refonte change les chiffres en passant | **Contrôle automatique** : les totaux avant/après sont identiques, sinon le projet est rejeté (`tools/controle_refonte_M10.py`). |
| La grille en 18 points devient un barème jetable | Elle est l'**artefact** du module : auto-évaluée en M10, revue par un pair, **réutilisée** en M14, M17, M21. |

## 7. Étapes de production (calque M05—M09)

1. **Étape 1 — Plan** (ce document).
2. **Étape 2 — Socle** : `tools/dossier_M10.py` (graine 46) : `rapport_avant/` (5 SVG ratés + le
   code qui les produit + 2 pages de rapport), `rapport_apres/` (5 SVG corrigés),
   `ATTENDU.json` (≈ 20 clés `m10p_*`) ; `chiffres_manuel.py M10()` (≈ 30 clés, 2 runs `diff` = 0) ;
   **les données de la refonte sont celles du socle M07/M08/M09** (aucune génération nouvelle).
3. **Étape 3 — Rédaction** : 7 chapitres, cadence **1 push par chapitre validé `--strict`**
   (7 pushes), chacun avec sa planche de référence et son tableau des graphiques exécutés.
4. **Étape 4 — Figures** : `tools/figures_M10.py` (7 planches, une par chapitre : ordre perceptuel,
   table des 16, palettes et daltonisme, anatomie du graphique, les 10 erreurs, la séquence
   écran → insight → décision, les 3 outils) — extension ≤ 776 px, jeu latin-1 étendu.
5. **Étape 5 — PDF** : `tools/render.py --join "02_modules/M10_*.md"` → `M10.pdf`
   (budget 105 p. ±15 % = [89, 121]) + `tools/controle_pdf.py M10`.
6. **Étape 6 — Fiche de contrôle** : `05_livrables/fiche_controle_M10.md` Q1-Q10.
7. **Étape 7 — Projet + évaluation** : `03_exercices/M10_projet.md` (« La refonte », 4 livrables
   /20 seuil 13) + `04_evaluations/M10_evaluation.md` (quiz 15 Q + 3 exercices argumentés +
   étude de cas « ce graphique a déclenché une décision fausse » + **grille en 18 points**) +
   `tools/controle_refonte_M10.py` + **`05_livrables/grille_visuelle_18_points.md`** (l'artefact
   réutilisé par M14, M17, M21) + `README.md` (mise à jour) + push final.
8. **L'errata du §E.7** (« 20 points, 4 par famille » → « 18 points, 4 familles ») est reporté au
   fichier d'architecture **dans le push de clôture de M10**, avec la mention d'errata.
