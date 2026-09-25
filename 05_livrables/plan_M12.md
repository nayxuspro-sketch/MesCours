# Plan M12 — Fondamentaux de la Business Intelligence

**Module M12 · phase 4 (Business Intelligence) · 6 chapitres · 30 h · niveau N3 · budget 92 pages
[78, 106] · projet « Le tableau de bord que personne n'ouvrait » · évaluation : quiz 15 Q + 2 exercices
de rédaction de KPI + étude de cas « la direction veut un tableau de bord, elle a déjà tort de le
vouloir comme ça ».**
Rédigé le 24 septembre 2026, avant la rédaction (étape 1 du calque M05—M10).

---

## 1. Cadrage

### 1.1 Position dans l'architecture

M12 est le **deuxième module de la phase 4** (M11 SQL avancé, M12 fondamentaux de la BI, M13
modélisation, M14 Power BI, M15 DAX). Il vient après M11 — qui a livré la **matière** (des requêtes
fiables) — et **avant M13**, qui livrera le **modèle** : c'est M12 qui décide *quoi* mesurer, *pour
qui*, et *à quelle condition un chiffre devient une décision*.

Ce que M12 apporte et qu'aucun module précédent ne pouvait apporter : M11 publie des rapports justes ;
M12 est le premier module du manuel qui demande **pourquoi ce rapport existe**, ce qu'il change dans le
travail de celui qui le lit, et ce qu'on fait quand il vire au rouge. C'est aussi le premier module
dont le livrable principal — la **carte de définition de dix KPI** — sera réutilisé tel quel par M13,
M14, M15 et M21 : le document signature du manuel.

**Aucune compétence technique nouvelle** n'est exigée (c'est la règle de l'architecture pour ce
module) : les indicateurs se calculent sur le socle de M11 avec le SQL de M07—M11, les sorties se
lisent en SQL ou en tableur, et l'effort porte sur la **définition**, la **gouvernance** et
l'**adoption**.

**Outils.** DuckDB 1.5.5 (**exécuté** : les dix indicateurs sont calculés en SQL sur le socle M12),
pandas (**exécuté** pour le contrôle croisé d'un indicateur), Excel (**exécuté** : le classeur de la
carte de KPI est écrit puis relu), Power BI (**cité, non exécuté** — aucun chapitre n'ouvre Power BI,
aucune capture n'est publiée), tableurs d'entreprise (**cités**). Règle §1.5 tenue et déclarée à la
fiche de contrôle.

### 1.2 Six compétences de sortie (la matrice de couverture)

| # | Compétence de sortie | Chapitre | Preuve exigée |
|---|---|---|---|
| 1 | Définir la BI et situer son économie réelle dans une PME | C01 | la note de cadrage d'un dispositif, chiffrée sur le socle |
| 2 | Distinguer reporting, BI, entrepôt, lac de données, self-service par le **régime de question** | C02 | les 4 régimes appliqués à 8 questions réelles, classées et justifiées |
| 3 | Employer le vocabulaire exact des données (métrique, dimension, fait, grain) | C03 | un tableau de grain : 6 indicateurs, leur grain, leur source |
| 4 | Concevoir un KPI avec la règle des **6 critères** et une **carte de définition** | C04 | **10** cartes complètes sur le cas de gros du projet |
| 5 | Décrire l'architecture BI de bout en bout, et nommer chaque étage | C05 | le schéma annoté du dispositif, étage par étage, sur le cas de la quincaillerie |
| 6 | Conduire un projet BI : parties prenantes, adoption, et les **10** causes d'échec | C06 | le diagnostic et le plan de reprise du dispositif raté |

### 1.3 Fait du socle (mesuré le 24/09/2026 — à figer en clés `m12_*` à l'étape 2)

Le socle de M12 **étend** celui de M11 : mêmes ventes (**240 000** lignes, **44** mois, **5** magasins
servis, **23 497** clients), plus les **cinq** tables opérationnelles qu'un indicateur exige — coût
d'achat (**154** produits), stock mensuel (**6 776** lignes), ruptures (**2 428** lignes), commandes
clients (**9 000**), encaissements (**9 000**), logistique (**264** lignes) — générées par
`tools/dossier_M12.py` (graine **46**, reproductible au bit près) et lues par un script SQL
(`socle_m12.sql` + `connexion.py`, aucun fichier de base versionné).

**Les dix indicateurs, mesurés** (`tools/kpi_M12.py`) :

| # | Indicateur | Valeur mesurée | La question qu'il ouvre |
|---|---|---|---|
| 1 | CA net | **15 595 154 955** FCFA | et avec les retours : **15 419 985 157**, soit **175 169 798** FCFA d'écart (**1,12 %**) |
| 2 | Marge brute | **3 847 989 780** FCFA (**29,12 %** des ventes HT) | la cible du référentiel est de **18** à **24 %** : l'écart vient des prix, pas d'une performance |
| 3 | Taux de rupture | **7,29 %** (**2 428** couples sur **33 296** servis) | **13 129** jours de rupture, **169 386 812** FCFA de CA **estimé** perdu |
| 4 | Rotation de stock | **9,42** tours par an, couverture **1,27** mois | la même requête écrite sur la **somme** des stocks donne **0,78** tour |
| 5 | Panier moyen | **107 396** FCFA par ticket, **64 243** FCFA en médiane | la ligne moyenne vaut **65 749** FCFA : **38,8 %** sous le panier |
| 6 | Taux de retour | **1,17 %** des lignes, **1,91 %** des tickets | **2 797** tickets concernés, dont **1 848** mixtes et **949** uniquement des retours |
| 7 | Taux de service | **81,0 %** des livrées, **78,2 %** des commandes | **319** annulées changent le dénominateur ; retard médian **5** jours |
| 8 | Taux de recouvrement | **74,0 %** à échéance | **1 272** factures ouvertes, **1 202 550 590** FCFA d'encours, DSO **23,9** jours |
| 9 | Coût logistique unitaire | **3 284** FCFA par colis, **249** FCFA au kilo | **52 596** colis, **50,5 %** du coût en carburant |
| 10 | Part de marché interne | **5** points de vente classés | premier : **Bobo Kibidwé**, **19,9 %** du réseau — le mot « marché » est de trop |

**Les défauts du socle, qui font le module** (mesurés, jamais inventés) :

- **2** produits du référentiel sans prix de vente : la marge brute bouge de **0,05** point selon qu'on
  les écarte ou qu'on reconstitue leur prix (médiane de la sous-catégorie) ;
- **1** magasin — le **dépôt central** — qui n'a **aucune vente** mais **8 766** colis de logistique
  facturés à son nom : un coût sans chiffre d'affaires rattaché ;
- **319** commandes annulées, comptées ou non selon la définition du taux de service ;
- **1 272** factures ouvertes : le taux de recouvrement à échéance (**74,0 %**) et le taux
  d'encaissement (toutes échéances confondues) ne racontent pas la même chose ;
- **13 129** jours de rupture cumulés dont le coût n'est **qu'une estimation** — l'estimation publiée
  comme une mesure est le même défaut que dans le dossier du projet raté.

### 1.4 Le projet M12.P — « Le tableau de bord que personne n'ouvrait »

- **Énoncé.** Une direction régionale a payé **7 940 000** FCFA, sur trois sources discordantes, un
  tableau de bord de **41** indicateurs répartis en **7** onglets ; onze semaines plus tard, il est
  abandonné et la maintenance résiliée. Le dossier complet (**12** pages de pièces) est fourni :
  commande initiale, devis, liste des onglets, courbes d'ouverture, les trois discordances, le coût de
  l'abandon, les questions que le prestataire n'a jamais posées. **Rien n'est inventé sur les
  chiffres** : chaque valeur se recalcule sur le socle M12.
- **Livrables** (grille /20, seuil 13) :
  - **P1 — Le diagnostic** (6 pts, 3 pages) : nommer les causes de l'échec et les **prouver** par le
    socle (une cause sans mesure ne compte pas) ;
  - **P2 — La carte de définition de 10 KPI** (8 pts) : CA, marge brute, taux de rupture, rotation de
    stock, panier moyen, taux de retour, taux de service, taux de recouvrement, coût logistique
    unitaire, part de marché interne — chacun avec **formule, source, granularité, fréquence,
    responsable, seuil d'alerte, contre-KPI**. C'est le document réutilisé en M13, M14, M15 et M21 ;
  - **P3 — Le plan de reprise** (4 pts, 2 pages) : ce qu'on garde, ce qu'on jette, ce qu'on remplace,
    dans quel ordre, avec le coût et le délai de chaque étape ;
  - **P4 — La page « que fait-on quand c'est rouge ? »** (2 pts) : pour chacun des 10 KPI, l'action
    décidée **à l'avance**, avec son responsable — la pièce qui manquait au dispositif raté.
- **Ce que le projet n'évalue pas** : la qualité graphique (c'est M10), le modèle de données (c'est
  M13) ni l'outil (c'est M14). Il évalue la **définition** et l'**action** : un KPI sans définition
  écrite et sans action associée est refusé.

### 1.5 Évaluation M12

- **Quiz 15 Q** (seuil **11/15**, §B.6 appliqué au prorata de 14/20) : 5 questions de vocabulaire
  exact (métrique, dimension, fait, grain, semantic layer), 5 questions de diagnostic (« ce dispositif
  affiche ceci, quelle est la cause ? »), 5 questions de méthode (« quelle question poser à celui qui
  demande cet indicateur ? »).
- **2 exercices de rédaction de KPI** : l'un sur un indicateur **piégeux** (le taux de rupture du
  socle, dont le dénominateur change la valeur), l'autre sur un indicateur **qui n'existe pas encore**
  (la part des clients non identifiés — le **18,3 %** du socle M11 — avec sa source manquante à
  déclarer) : la rédaction pèse plus que le calcul.
- **Étude de cas notée** — « la direction veut un tableau de bord, elle a déjà tort de le vouloir comme
  ça » : on lui demande d'abord **la décision** qu'elle prendra, puis l'indicateur. L'apprenant
  produit (a) les **3** questions qui remplacent la commande, (b) **5** indicateurs maximum avec leur
  définition, (c) le **contre-KPI** de chacun, (d) la phrase de refus argumenté qu'un analyste doit
  pouvoir écrire.
- **Auto-évaluation outillée** : `tools/kpi_M12.py` recalcule les **10** indicateurs et les compare aux
  valeurs publiées du module (sorte de contrôle croisé, comme `controle_sql_M11.py` pour M11).

### 1.6 Règles d'exécution (cadence héritée de M06—M11)

1. **Un push par chapitre validé `--strict`** (le jeton GitHub est actuellement refusé : les pushs M11
   sont en attente, ceux de M12 suivront dans le même rattrapage).
2. **R8 compte les encadrés** : **4** « Définition » et **2** « Attention » minimum par chapitre, dès
   la première rédaction (leçon PATCH_13).
3. **Tout nombre ≥ 4 chiffres est sourcé** dans `chiffres_cites.json` (bloc M12), y compris dans les
   tableaux, le projet et l'évaluation (PATCH_12) ; les identifiants collés vont en `code inline`.
4. **Typographie** : le tiret demi-cadratin (U+2013) est **interdit** — `—` (U+2014) partout.
5. **§1.5 : DuckDB, pandas et Excel exécutés** ; Power BI **cité** ; aucun chiffre présenté comme
   mesuré dans Power BI.
6. **Une affirmation de cours se mesure** (PATCH_16) : le socle M12 fournit déjà deux pièges à traiter
   en exercice — la **somme** des stocks au lieu de leur moyenne (**0,78** contre **9,42** tours) et le
   dénominateur du taux de service (**78,2 %** ou **81,0 %**).

### 1.7 Les dix indicateurs et leur contre-KPI (le fil du module)

| Indicateur | Ce qu'il pousse à faire | Son contre-KPI | Ce que le couple protège |
|---|---|---|---|
| CA net | vendre plus, vite | **taux de retour** | la croissance ne se paie pas en mécontentement |
| Marge brute | monter les prix | **panier moyen** | la marge ne se gagne pas en vidant le panier |
| Taux de rupture | stocker plus | **rotation de stock** | la disponibilité ne se paie pas en trésorerie |
| Rotation | réduire le stock | **taux de rupture** | la trésorerie ne se gagne pas en ruptures |
| Panier moyen | vendre des lots | **marge brute** | le gros panier n'est pas une remise déguisée |
| Taux de retour | contrôler les retours | **taux de service** | un retour est aussi une livraison ratée |
| Taux de service | promettre large | **coût logistique unitaire** | la promesse a un prix, et il se mesure |
| Taux de recouvrement | relancer vite | **CA net** | la trésorerie ne se gagne pas en refusant des clients |
| Coût logistique unitaire | grouper les tournées | **taux de service** | l'économie ne se fait pas sur le dos du client |
| Part de marché interne | défendre son magasin | **part du réseau** | un magasin ne grandit pas en prenant à l'autre |

---

## 2. Vocabulaire du module (à définir au premier emploi)

**Définitions imposées** (encadrés « Définition » des six chapitres) : *Business Intelligence*,
*reporting*, *entrepôt de données* (*data warehouse*), *lac de données* (*data lake*), *self-service*,
*analyse descriptive / diagnostique / prédictive / prescriptive*, *métrique*, *dimension*, *fait*,
*grain*, *indicateur* (opérationnel, tactique, stratégique), *KPI* — *Key Performance Indicators*,
*carte de définition*, *contre-KPI*, *seuil d'alerte*, *couche sémantique* (*semantic layer*),
*adoption*, *cahier des charges*, *gouvernance de la donnée*, *effet pervers*.

**Anglicismes** : toujours accompagnés de leur traduction (« chaîne de calcul » pour *pipeline*,
« tableau de bord » préféré à *dashboard*) ; les termes sans équivalent français (KPI, *semantic
layer*) sont donnés en français avec l'anglais signalé.

---

## 3. Découpage en 6 chapitres

| Ch. | Titre | Contenu | Sections | H | Pages |
|---|---|---|---|---|---|
| **C01** | Qu'est-ce que la BI — et ce qu'elle n'est pas | définition, rôle, décision fondée sur les données, le coût d'une décision sans donnée, l'économie réelle d'un dispositif en PME | 15 | 5 | 12,5 |
| **C02** | Reporting, BI, et les 4 régimes de question | périodicité, exploration, interactivité, gouvernance ; quoi / pourquoi / quoi demain / que faire ; les 4 analyses | 15 | 5 | 12,5 |
| **C03** | Métriques, dimensions, faits, grain | le vocabulaire exact ; indicateur opérationnel, tactique, stratégique ; les sources qu'un indicateur réclame | 15 | 5 | 12,5 |
| **C04** | Concevoir un KPI : les 6 critères et la carte de définition | les 6 critères, la carte (formule, source, grain, fréquence, responsable, seuil), le contre-KPI, les effets pervers | 16 | 5 | 12,5 |
| **C05** | L'architecture BI de bout en bout | source → extraction → stockage → modèle → couche sémantique → visualisation → diffusion ; les 7 étages, leurs pannes, leurs coûts | 15 | 5 | 12,5 |
| **C06** | Réussir le projet BI | parties prenantes, cahier des charges, conduite, adoption, maintenance ; les **10** causes d'échec, et comment les détecter **avant** la livraison | 16 | 5 | 12,5 |

**Progression interne** : C01 pose la définition et le coût ; C02 classe les questions ; C03 donne le
vocabulaire exact ; C04 arme la fabrication d'un indicateur ; C05 replace l'indicateur dans une chaîne
technique ; C06 sort du technique pour le projet et l'adoption. Chaque chapitre réutilise le dossier
du projet raté comme fil rouge — c'est le seul module du manuel dont le matériel est un **échec**.

---

## 4. Budget pages

| Poste | Pages |
|---|---|
| C01 → C06 (6 × 12,5) | 75 |
| Appareil de module (ouverture, bilan, projet, évaluation) | 17 |
| **Total M12** | **92** |

Fourchette de validation **± 15 %** : **[78, 106]** pages. Contrôle : `tools/budget_pages.py --mesure`
puis `tools/render.py` + `tools/controle_pdf.py M12`.

---

## 5. Chiffres cibles (à figer dans `chiffres_manuel.py M12`)

- **Socle** : 240 000 lignes · 237 191 hors retours · 44 mois · 5 magasins servis + 1 dépôt · 154
  produits · 23 497 clients · **6 776** lignes de stock · **2 428** ruptures · **9 000** commandes ·
  **9 000** factures · **264** lignes de logistique · **5** tables ajoutées par M12.
- **Les dix KPI** : les valeurs du tableau §1.3, plus les mesures de leurs pièges (somme/moyenne des
  stocks, dénominateur du taux de service, deux taux de retour, écart CA net / CA brut, effet des deux
  prix manquants, marge de **29,12 %** contre une cible de **18** à **24 %**).
- **Le dossier du projet** : **41** indicateurs, **7** onglets, **7 940 000** FCFA, **11** semaines,
  **14** destinataires, **4** ouvertures le premier jour, **2** questions de discorde, **3** sources,
  **6** questions jamais posées, **10** KPI exigés au mandat de reprise.
- **Le contre-KPI** : les **10** couples du §1.7, chacun avec sa valeur mesurée sur le socle.

---

## 6. Risques et parades

| Risque | Parade |
|---|---|
| Un module « concepts » sans chiffres, donc invérifiable | **Toutes** les valeurs du module se recalculent avec `tools/kpi_M12.py` et se figent dans `chiffres_cites.json` ; aucun chapitre ne publie un chiffre qui ne vient pas du socle |
| Le projet devient un devoir de français | La grille exige des **preuves mesurées** : chaque cause du diagnostic doit être chiffrée sur le socle (une cause sans mesure ne compte pas) |
| Le socle M12 alourdit le dépôt | Le socle pèse **1,3 Mo** (six CSV déterministes) et **aucun** fichier de base : le script se rejoue en **0,8 s** ; la marge du quota reste positive et sera mesurée par `tools/poids.py` |
| Les KPI paraissent arbitraires (« pourquoi 6 critères ? ») | Chaque critère est **montré sur un échec** du dossier du projet : le critère manquant est celui qui a fait tomber l'indicateur |
| Le chapitre C05 (architecture) déborde sur M13/M14 | Frontière écrite : C05 **nomme** les étages et leurs pannes, M13 **construit** le modèle, M14 **outille** la publication ; aucune capture Power BI en C05 |
| Un chiffre de Power BI paraît mesuré | Power BI est **cité** partout, jamais exécuté ; la fiche de contrôle Q9 le déclare |

---

## 7. Étapes de production (calque M05—M11)

1. **Étape 1 — Plan** : ce fichier (poussé avant toute rédaction).
2. **Étape 2 — Socle et instruments** : `tools/dossier_M12.py` (**fait** : six CSV + `socle_m12.sql` +
   `connexion.py` + `etude_avant.md` + `ATTENDU.json`), `tools/kpi_M12.py` (**fait**), bloc `m12_*` dans
   `chiffres_manuel.py`.
3. **Étape 3 — Rédaction** : C01 → C06, un push par chapitre validé `--strict`.
4. **Étape 4 — Figures** : **2** planches (`tools/figures_M12.py`) — la **carte des 7 étages** de
   l'architecture BI et la **matrice des 10 couples indicateur / contre-KPI** — largeur ≤ 776 px,
   texte réel dans le SVG (`svg.fonttype = "none"`), déterministes, citées par leur chapitre.
5. **Étape 5 — PDF** : `tools/render.py "0[234]_*/M12_*.md" --join --out 05_livrables/M12.pdf` puis
   `tools/controle_pdf.py M12` — viser **[78, 106]** pages, 0 défaut bloquant.
6. **Étape 6 — Fiche de contrôle** : `05_livrables/fiche_controle_M12.md` (Q1—Q10).
7. **Étape 7 — Projet + évaluation + clôture** : `03_exercices/M12_projet.md` (**10** cartes de
   définition, 4 livrables /20 seuil 13), `04_evaluations/M12_evaluation.md` (quiz 15 Q + 2 exercices
   de rédaction + étude de cas), `README.md`, `05_livrables/etat_avancement.md`, et **le contrôle final
   d'existence nommée** de chaque livrable (PATCH_6).
