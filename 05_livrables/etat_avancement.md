# État d'avancement du manuel — *La Voie des Données* (Édition 2026)

**Arrêté au 25 septembre 2026, après le push n° 69 (kit d'exploitation livré, M13 à 3 chapitres sur 7).**
**M11 (n° 36 → n° 45), M12 (n° 46 → n° 57) et le kit M01-M12 (n° 65) sont poussés.** M13 est
**engagé** : plan n° 58, socle et instrument n° 59, **C01** n° 61, **C02** n° 63, **C03** n° 69 — **3 chapitres sur
7**. Le modèle de Sahel Distribution compte **12** tables (**5** dimensions, **7** faits), **2**
dimensions historisées (bâties **en SQL**) et **4** contrôles de recette exécutés. Détail :
`05_livrables/journal_pushs.md`.

Chiffres pris aux sources du dépôt : `00_architecture/01_architecture_pedagogique.md` (§C.1, §F.2,
§E.3, §E.4, §B.6), `tools/budget_pages.py` (budgets) et `05_livrables/kit_M01_M12.json` (mesures du
kit, refaites à chaque exécution de `tools/kit_exploitation.py`).

---

## 1. Le manuel en une ligne

| Agrégat | Prévu | Réalisé | Restant |
|---|---|---|---|
| Modules obligatoires | **22** (M01 → M22) | **12** clos (M01 → M12) · M13 engagé (2 ch.) | **10** |
| Chapitres | **143** | **84** (81 publiés + 3 de M13) | **59** |
| Heures du parcours | **660 h** | **360 h** livrées (+ 30 h engagées en M13) | **270 h** |
| Pages de module | **2 226 p.** | **1 207 p.** composées et vérifiées | **1 019 p.** |
| Appareil du livre | **229 p.** | **36 p.** (guide 4 p. + index 32 p.), assemblés dans le livre | **193 p.** |
| **Total manuel** | **2 455 p.** | **1 395 p.** dans un seul livre assemblé | — |
| Exercices autonomes (mesurés) | — | **366** dans les 81 chapitres, **0** sans reprise au corrigé | — |
| Exercices (unité de l'architecture, 180) | 180 | unité différente : l'architecture compte des exercices types, le manuel écrit des énoncés | — |
| Projets de module | 30 | 12 | 18 |
| Quiz de module | 22 | 12 | 10 |
| Études de cas | 21 | 12 | 9 |
| Épreuves de palier | 4 | 2 (P1, P2) | 2 (P4, P5) |
| Soutenances (M19, M21) | 2 | 0 | 2 |
| Options M23—M25 (hors obligatoire) | 14 ch. · 50 h · 226 p. | 0 | 14 ch. |

> **Lecture.** Le manuel est rédigé à **59 %** de ses chapitres (84 sur 143) et **55 %** de ses
> modules (12 sur 22) ; les phases 0 à 3 sont **terminées** (M01 → M10) et la phase 4 est **en
> cours** (M11 et M12 livrés, M13 à 3/7). Deux mesures valent d'être notées : le livre assemblé
> retombe **page par page** sur la somme de ses parties (**1 395 p.** = sommaire, guide, 12 modules,
> 2 cahiers, index), et la mesure des exercices donne **366** exercices autonomes là où l'ancien
> comptage en annonçait **243** — l'unité de l'architecture (180) compte des exercices *types*, pas
> les énoncés réellement écrits.

## 2. Ce qui est livré et vérifié (M01 → M12)

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

**Ce qui reste à pousser pour M13** (3 chapitres sur 7 sont en ligne) : les chapitres **C04**
(étoile, dimensions conformes, SCD 0/1/2/3, 16 § + 1 planche), **C05** (flocon, pont, déchet, faits
multiples, 15 §), **C06** (le temps et le calendrier, 15 §) et **C07** (qualité, documentation, revue
en 15 points, 16 § + 1 planche), puis le PDF cible **[89, 121]** p., la fiche Q1-Q10, le projet
(**20** points, seuil **13**), l'évaluation (**75** points, seuil **48**) et la clôture.

**C03 a rendu un défaut de plus, trouvé en écrivant l'exercice guidé** : joindre deux agrégats
mensuels au bon grain, mais par une **jointure interne**, fait disparaître le dépôt central — **44**
mois de coûts logistiques, **28 893 543** FCFA, pour zéro vente. La mesure est entrée au socle
(`m13_c03_logistique_perdue`) et le chapitre l'enseigne : le filtre silencieux ne vient pas toujours
d'une clé trop fine.

## 3. Ce qui reste — 10 modules, 60 chapitres, 270 h

### Phase 4 — Business Intelligence (5 modules · 35 ch.)

**En cours.** M11 et M12 sont livrés ; M13 (**7 ch. · 30 h · 105 p. [89, 121] · 3 planches**) est à
**2 chapitres sur 7**. Restent M14 (*Power BI, de l'import à la publication*, 8 ch.) et M15 (*DAX
pour la BI*, 7 ch.) — **documentés pas à pas, non exécutables dans cet atelier, et déclarés comme
tels**. La phase se termine par l'**épreuve de palier P4**.

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

1. **Finir M13** — C03 → C07, puis figures, PDF, fiche, projet, évaluation.
2. **M14 → M15** — Power BI puis DAX (documentés, non exécutés), puis **épreuve de palier P4**.
3. **M16 → M19** (+ soutenance M19), puis **M20 → M22** (mission finale et portfolio).
4. **Appareil du livre** — l'ouverture, les annexes et la fin, une fois les 22 modules écrits.
5. **Options M23—M25** — seulement si le parcours obligatoire est clos.

*Mise à jour du 25 septembre 2026 — remplace l'état arrêté après la clôture de M12. Les compteurs
de dépôt de ce fichier sont ceux du push n° 67 (`88ea9d5`).*
