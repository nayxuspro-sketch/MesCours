# État d'avancement du manuel — *La Voie des Données* (Édition 2026)

**Arrêté au 25 septembre 2026, après le push n° 90 (M14 livré de bout en bout).**
**M11 (n° 36 → n° 45), M12 (n° 46 → n° 57) et le kit M01-M12 (n° 65) sont poussés.** M13 est
**livré de bout en bout** : plan n° 58, socle et instrument n° 59, **C01** n° 61, **C02** n° 63,
**C03** n° 69, **C04** n° 72, **C05** n° 74, **C06** n° 77, **C07** n° 78, puis au n° 80 le
**projet**, l'**évaluation** (**75** points, seuil **48**), le **PDF du module** (**107** p., cible
[89, 121]) et la **fiche de contrôle Q1-Q10** (**10/10** au vert, **5** nuances déclarées). Le modèle de
Sahel Distribution compte **14** tables (**7** dimensions, **7** faits), **2** dimensions historisées
(bâties **en SQL**), une dimension de temps de **1 339** jours branchée sur les faits et **4**
contrôles de recette exécutés (**14** tables sur **14**, **7** faits sur **7**, **12** clés
étrangères, **0** orphelin, recette au franc près). **M14 est livré de bout en bout** : dossier
(n° 83), **C01** n° 84, **C02** n° 85, **C03** n° 86, **C04** n° 87, **C05** n° 88, **C06** n° 89,
**C07** et **C08** n° 90, puis le **projet à deux volets** (**20** points chacun, seuil **13**),
l'**évaluation** (**80** points, seuil **51**), le **PDF du module** (**116** p., cible **[99, 135]**,
**− 0,9 %**, **22** signets) et la **fiche de contrôle Q1-Q10** (**10/10**, **5** nuances). Le module
suivant est **M15 — DAX pour la BI**.
Détail : `05_livrables/journal_pushs.md`.

Chiffres pris aux sources du dépôt : `00_architecture/01_architecture_pedagogique.md` (§C.1, §F.2,
§E.3, §E.4, §B.6), `tools/budget_pages.py` (budgets) et `05_livrables/kit_M01_M12.json` (mesures du
kit, refaites à chaque exécution de `tools/kit_exploitation.py`).

---

## 1. Le manuel en une ligne

| Agrégat | Prévu | Réalisé | Restant |
|---|---|---|---|
| Modules obligatoires | **22** (M01 → M22) | **14** clos (M14 livré au n° 90) | **8** |
| Chapitres | **143** | **96** (88 publiés + 8 de M14) | **47** |
| Heures du parcours | **660 h** | **420 h** livrées | **240 h** |
| Pages de module | **2 226 p.** | **1 430 p.** composées et vérifiées | **796 p.** |
| Appareil du livre | **229 p.** | **36 p.** (guide 4 p. + index 32 p.), assemblés dans le livre | **193 p.** |
| **Total manuel** | **2 455 p.** | **1 395 p.** dans un seul livre assemblé (M01 → M12) | — |
| Exercices autonomes (mesurés) | — | **440** dans les 96 chapitres, **0** sans reprise au corrigé | — |
| Exercices (unité de l'architecture, 180) | 180 | unité différente : l'architecture compte des exercices types, le manuel écrit des énoncés | — |
| Projets de module | 30 | 15 | 15 |
| Quiz de module | 22 | 14 | 8 |
| Études de cas | 21 | 14 | 7 |
| Épreuves de palier | 4 | 2 (P1, P2) | 2 (P4, P5) |
| Soutenances (M19, M21) | 2 | 0 | 2 |
| Options M23—M25 (hors obligatoire) | 14 ch. · 50 h · 226 p. | 0 | 14 ch. |

> **Lecture.** Le manuel est rédigé à **67 %** de ses chapitres (96 sur 143) et **64 %** de ses
> modules (14 sur 22) ; les phases 0 à 3 sont **terminées** (M01 → M10) et la phase 4 est **en
> cours** (M11, M12, M13 et M14 livrés). Deux mesures valent d'être notées : le livre assemblé
> retombe **page par page** sur la somme de ses parties (**1 395 p.** = sommaire, guide, 12 modules,
> 2 cahiers, index), et la mesure des exercices donne **366** exercices autonomes là où l'ancien
> comptage en annonçait **243** — l'unité de l'architecture (180) compte des exercices *types*, pas
> les énoncés réellement écrits.

## 2. Ce qui est livré et vérifié (M01 → M14)

| Module | Thème | Ch. | Pages | Planches | Statut |
|---|---|---|---|---|---|
| M01 | Lire les données, comprendre le métier | 7 | 117 | 7 | clos, poussé |
| M02 | Statistiques appliquées, depuis zéro | 8 | 122 | 4 | clos, poussé |
| M03 | Excel pour l'analyse de données | 8 | 126 | 9 | clos, poussé |
| M04 | Qualité, préparation, documentation | 6 | 92 | 6 | clos, poussé |
| M05 | Chaîne de transformation (M/Q, SQL, pandas) | 5 | 86 | 5 | clos, poussé |
| M06 | Bases de données relationnelles | 5 | 69 | 5 | clos, poussé |
| M07 | SQL : interroger, agréger, rejoindre | 8 | 109 | 8 | clos, poussé |
| M08 | Python pour l'analyse de données | 8 | 119 | 8 | clos, poussé |
| M09 | Analyse exploratoire (EDA) | 6 | 82 | 6 | clos, poussé |
| M10 | Data visualization | 7 | 106 | 7 | clos, poussé |
| M11 | SQL avancé pour la BI | 7 | 97 | 2 | clos, poussé |
| M12 | Fondamentaux de la Business Intelligence | 6 | 82 | 2 | clos, poussé |

**Le kit d'exploitation (n° 65)** rend ces douze modules utilisables par un apprenant seul :
`guide_apprenant_M01_M12.md` (1 886 mots, 4 p.), `index_glossaire_M01_M12.md` (488 notions, 367
définitions, 69 planches, 48 instruments, 10 jeux de données), `kit_M01_M12.json` (les mesures),
`requirements.txt` (l'environnement), `tools/kit_exploitation.py` (le générateur) et le **livre
assemblé de 1 395 pages avec 124 signets**, où le guide ouvre la partie I.

**Ce que M13 a livré** (poussé au n° 80) : le **projet** « Le modèle de Sahel Distribution »
(**20** points, seuil **13**, **4** livrables, **4**ᵉ pièce du portfolio) ; l'**évaluation**
(**75** points, seuil **48** — quiz **20**, deux normalisations **20**, étude de cas **30**, auto-test
**5**) ; le **PDF du module** (**107** p. pour une cible de **[89, 121]**, **+ 1,9 %**, **9** fichiers
joints, **20** signets, **3/3** planches retrouvées dans le PDF, **27/27** glyphes) ; la **fiche de
contrôle Q1-Q10** (**10/10** au vert, **5** nuances déclarées) ; et **2** correctifs de veille : le
signe moins perdu **9** fois dans le chapitre C06, et la déclaration d'exécution §1.5 ajoutée en tête
des **5** chapitres qui ne l'avaient pas.

**Ce qui reste à faire pour M13** : l'entrée dans le **kit d'exploitation** (le guide est aujourd'hui
bâti sur les **12** évaluations de M01 à M12 ; il passera à **14** lors de la clôture de M15) et
l'**appareil du livre** (le livre assemblé s'arrête à M12).

**Ce que M14 a livré** (poussé aux n° 82 à 90) : un **dossier de conception à 7 pièces** — les **12**
relations, les **2** inactives, les **15** gestes de transformation, les **11** mesures avec leur code,
les **3** pages et les **14** visuels, les **4** signets, la sécurité ligne à ligne et les **11**
retours du comité —, **8** chapitres qui construisent le rapport pas à pas, **4** planches, un
instrument de **277** clés en **12** sections, **2** projets (**20** points, seuil **13** chacun), une
évaluation de **80** points (seuil **51**) et la grille de conception en **18** points enrichie de **6**
sous-questions. La règle §1.5 est déclarée en tête des huit chapitres : DuckDB **exécuté**, Power BI
Desktop, le Service et Fabric **cités**.

**Ce qui reste à faire pour M14** : la même chose que pour M13 — l'entrée dans le **kit d'exploitation**
et l'**appareil du livre**, à la clôture de M15.

**Ce que les chapitres ont établi, en une phrase par chapitre.** C01 : ce que le modèle remplace, et
ce qu'il coûte de le remplacer (**2 826 394** caractères de noms recopiés contre **239 599**). C02 :
la normalisation ne se justifie pas par l'intuition mais par la mesure, et les **16** libellés du
fichier plat deviennent **7** familles. C03 : le grain est la grammaire du modèle, et une clé trop
large multiplie le chiffre d'affaires par **44**. C04 : l'étoile et ses changements lents, au prix de
**9,1 %** d'écart entre l'attribut lu au moment du fait et le même lu aujourd'hui. C05 : le flocon,
le pont et le déchet se choisissent en mesurant, pas en principe. C06 : le temps est la seule
dimension qu'on remplit d'avance, et une borne mal choisie vaut **44,3** points d'écart. C07 : ce qui
rend un modèle livrable tient en **4** contrôles et **15** points de revue.

## 3. Ce qui reste — 9 modules, 55 chapitres, 270 h

### Phase 4 — Business Intelligence (5 modules · 35 ch.)

**En cours.** M11, M12, M13 et M14 sont livrés ; il reste **M15** (*DAX pour la BI*, 7 ch. · 30 h ·
105 p. [89, 121]) — comme M14, **documenté pas à pas, non exécutable dans cet atelier, et déclaré
comme tel**. La phase se termine par l'**épreuve de palier P4**.

### Phase 5 — Performance et autonomie (4 modules · 24 ch. · 120 h)

M16 (*Tableau et autres outils BI*, 5 ch.), M17 (*Automatisation du reporting*, 6 ch.), M18
(*Analyses sectorielles*, 7 ch.), M19 (*Prévision, segmentation, scoring*, 6 ch.) — avec la
**soutenance de M19** (8 minutes, enregistrée).

### Phase 6 — Professionnalisation (3 modules · 16 ch. · 90 h)

M20 (*Data storytelling et communication*, 6 ch.), M21 (*Projets professionnels complets*, 6 ch.,
avec sa carte de 10 KPI héritée de M12), M22 (*Portfolio, emploi, feuille de route*, 4 ch.).

### Appareil du livre — 229 p., dont 36 p. livrées

Le **guide de l'apprenant** et l'**index avec glossaire** sont écrits et assemblés (n° 65). Restent
l'ouverture générale, les annexes, la feuille de route, la bibliographie et la conclusion : à
écrire **en fin de parcours**, quand les 620 termes du glossaire existent vraiment (l'extraction est
mécanique — `tools/kit_exploitation.py` la fait déjà pour les 488 notions des douze modules publiés).

### Options M23—M25 — hors périmètre obligatoire

*R pour l'analyse* (5 ch.), *Data engineering appliqué* (5 ch.), *Données ouvertes et cartographie*
(4 ch.) : 14 chapitres, 50 h, 226 p. À n'ouvrir que lorsque le parcours obligatoire est clos.

## 4. Cadence observée, et ce qu'elle implique

- **≈ 2 pushs par chapitre** : un pour le chapitre validé `--strict`, un pour le journal et l'état.
  S'y ajoutent le plan, le socle, les figures avec le PDF et la clôture (**≈ 10 à 12 pushs par
  module**).
- **Mesuré sur le dépôt** : 393 fichiers, 90 dans `02_modules/`, 69 planches, 48 instruments,
  20 PDF, 0 `.pyc` — dont le livre assemblé de 14,1 Mo.
- **Coût dominant : le socle**, pas la rédaction. Un module qui réutilise le fil rouge (M10, M12,
  M13, M20) se livre plus vite qu'un module qui exige un outil non exécutable ici (M14 Power BI,
  M16 Tableau, M17 automatisation) : ceux-là se traitent comme Power Query en M05 — documentés pas
  à pas, **non exécutés**, et déclarés comme tels.
- **Trois instruments ont changé de statut avec M13** : `tools/modele_M13.py` (4 contrôles de
  recette + 5 mesures de modèle), `tools/kit_exploitation.py` (l'appareil du livre, mesuré et
  généré) et `01_socle_donnees/scripts/autovalide.py` (R1-R8, inchangé mais étendu à M13).

## 5. Ordre recommandé pour la suite

1. **Faire M15** — plan, socle, chapitres C01 → C07, figures, PDF, fiche, projet, évaluation.
2. **Clore la phase 4** — kit d'exploitation étendu à M01 → M15, appareil du livre, puis **épreuve de
   palier P4**.
3. **M16 → M19** (+ soutenance M19), puis **M20 → M22** (mission finale et portfolio).
4. **Appareil du livre** — l'ouverture, les annexes et la fin, une fois les 22 modules écrits.
5. **Options M23—M25** — seulement si le parcours obligatoire est clos.

*Mise à jour du 25 septembre 2026 — remplace l'état arrêté après la clôture de M12. Les compteurs
de dépôt de ce fichier sont ceux du push n° 67 (`88ea9d5`).*
