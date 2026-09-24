# État d'avancement du manuel — *La Voie des Données* (Édition 2026)

**Arrêté au 24 septembre 2026, après la clôture de M10 (push n° 34).**
Chiffres pris aux sources du dépôt : `00_architecture/01_architecture_pedagogique.md` (§C.1, §F.2,
§F.4, §E.3, §E.4, §B.6) et `tools/budget_pages.py` (budget recalculé, conforme).

---

## 1. Le manuel en une ligne

| Agrégat | Prévu | Réalisé | Restant |
|---|---|---|---|
| Modules obligatoires | **22** (M01 → M22) | **10** (M01 → M10) | **12** |
| Chapitres | **143** | **68** (48 %) | **75** (52 %) |
| Heures du parcours | **660 h** | **300 h** | **360 h** |
| Pages (module par module) | **2 226 p.** | **1 028 p. composées** (budget 1 022) | **1 204 p.** |
| Appareil du livre (ouverture + fin) | **229 p.** | **0 p.** | **229 p.** |
| **Total manuel** | **2 455 p.** | **≈ 1 028 p. (42 %)** | **≈ 1 432 p. (58 %)** |
| Exercices (180) | 180 | 101 | 79 |
| Projets (30) | 30 | 10 | 20 |
| Quiz de module (22) | 22 | 10 | 12 |
| Études de cas (21) | 21 | 10 | 11 |
| Épreuves de palier (4) | 4 | 2 (P1, P2) | 2 (P4, P5) |
| Soutenances (2 : M19, M21) | 2 | 0 | 2 |
| Options M23–M25 (hors obligatoire) | 14 ch. · 50 h · 226 p. | 0 | **14 ch.** |

> **Lecture.** Le manuel est rédigé à **≈ 42 %** de son volume et à **45 %** de ses modules ; les
> phases 0 à 3 sont **terminées** (M01 → M10), et **12 modules sur 22** restent à écrire, sans compter
> l'appareil du livre qui n'a pas commencé.

## 2. Ce qui est livré (M01 → M10) — phases 0 à 3 complètes

| Module | Ch. | Pages composées | Budget | Écarts |
|---|---|---|---|---|
| M01 Lire les données, comprendre le métier | 7 | 117 | 105 | +11 % |
| M02 Statistiques appliquées, depuis zéro | 8 | 122 | 117 | +4 % |
| M03 Excel pour l'analyse de données | 8 | 126 | 117 | +8 % |
| M04 Qualité, préparation, documentation | 6 | 92 | 92 | 0 % |
| M05 Chaîne de transformation (M/Q → SQL → pandas) | 5 | 86 | 80 | +7 % |
| M06 Bases de données relationnelles | 5 | 69 | 80 | -14 % |
| M07 SQL : interroger, agréger, rejoindre | 8 | 109 | 117 | -7 % |
| M08 Python pour l'analyse de données | 8 | 119 | 117 | +2 % |
| M09 Analyse exploratoire (EDA) | 6 | 82 | 92 | -11 % |
| **M10 Data visualization** | 7 | **106** | 105 | **+1 %** |
| **Total** | **68** | **1 028** | **1 022** | **+0,6 %** |

Chaque module livré compte : plan (`plan_Mxx.md`), socle de données régénéré, chapitres autovalidés
`--strict` (1 push par chapitre), planches SVG auditées ≤ 776 px, PDF composé dans son budget,
fiche de contrôle Q1-Q10, projet de module et évaluation avec corrigés. **10 fiches de contrôle
sur 10 au vert.** M10 ajoute ce que les modules précédents n'avaient pas : un **contrôle automatique
du projet** (`tools/controle_refonte_M10.py`, 4 couches) qui refuse une refonte dont les totaux
avant/après diffèrent, et une **grille visuelle en 18 points** réutilisée en M14, M17 et M21.

## 3. Ce qui reste — 12 modules, 75 chapitres, 360 h, 1 204 p.

### Phase 3 — Communication analytique — **LIVRÉE** (M10 : 7 ch. · 30 h · 106 p.)

M10 est clos le 24 septembre 2026 : 7 chapitres poussés un par un (n° 24 → n° 31), l'appareil
(recette des 7 planches, PDF de 106 pages, fiche Q1-Q10) poussé n° 33, la clôture (grille en
18 points, errata §E.7 de l'architecture) n° 34. Cette phase ne laisse aucun reste.

<details><summary>Ce que la phase annonçait (pour mémoire)</summary>

| Module | Chap. | Budget | Contenu attendu |
|---|---|---|---|
| **M10 Data visualization** | C01–C07 | 105 p. | ordre perceptuel ; table question → graphique (11 + 5) ; couleurs, daltonisme, formats FCFA ; titres, axes, annotations ; les erreurs qui tuent la crédibilité ; storytelling visuel ; mise en œuvre Excel / matplotlib / Power BI. **Projet « la refonte »** (5 graphiques ratés corrigés, version direction + version technique), grille visuelle 18 points. |

</details>

> **M10 était le module à enchaîner** : la transition est déjà écrite dans M09.C06 §5.1 et §15
> (*« Vos résultats sont justes. S'ils sont illisibles, ils ne serviront à rien. »*), et son
> emprunt le plus direct est la table question → graphique posée au C06.

### Phase 4 — Business Intelligence (5 modules · 35 ch. · 150 h · 524 p.)

| Module | Chap. | Budget | Contenu attendu |
|---|---|---|---|
| M11 SQL avancé pour la BI | 7 | 105 p. | cohortes, classements, fenêtres, CTE — DuckDB / PostgreSQL / SQL Server |
| M12 Fondamentaux de la Business Intelligence | 6 | 92 p. | chaîne brut → décision, carte de KPI, gouvernance |
| M13 Modélisation des données | 7 | 105 p. | étoile, flocon, MCD complet (dbdiagram, Power Pivot, SQL) |
| M14 Power BI, de l'import à la publication | 8 | 117 p. | **2 projets** ; validation de dashboard |
| M15 DAX pour la BI | 7 | 105 p. | bibliothèque de 40 mesures |

### Phase 5 — Performance et autonomie (4 modules · 24 ch. · 120 h · 369 p.)

| Module | Chap. | Budget | Contenu attendu |
|---|---|---|---|
| M16 Tableau et autres outils BI | 5 | 80 p. | même dashboard dans 3 outils + arbitrage ; étude comparative notée |
| M17 Automatisation du reporting | 6 | 92 p. | rapport hebdo sans intervention, tâches planifiées |
| M18 Analyses sectorielles | 7 | 105 p. | dossier sectoriel au choix (3 pistes) |
| M19 Analyse avancée : prévision, segmentation, scoring | 6 | 92 p. | rapport d'incertitude + **1ʳᵉ soutenance** |

### Phase 6 — Professionnalisation (3 modules · 16 ch. · 90 h · 311 p.)

| Module | Chap. | Budget | Contenu attendu |
|---|---|---|---|
| M20 Data storytelling & communication décideur | 6 | 92 p. | deck, soutenance, posture |
| M21 Projets professionnels complets | 6 | **152 p.** | 8 projets dont la **mission finale** (≈ 130 p. de rendus annotés) |
| M22 Portfolio, emploi, feuille de route | 4 | 67 p. | portfolio v1, CV, lettre, revue notée |

### Appareil du livre — 229 p., intégralement à écrire

| Bloc | Volume | Contenu |
|---|---|---|
| Ouverture | **39 p.** | couverture 2, page de titre 1, préface 3, objectifs de formation 4, parcours pédagogique 9, sommaire 20 (**généré automatiquement** par `render.py`) |
| Glossaire | **80 p.** | 620 termes au format imposé + 3 index (français, anglais, fonctions) |
| Feuille de route professionnelle | 14 p. | débutant → junior → confirmé → BI Analyst → BI Developer |
| Portfolio | 12 p. | 14 fiches de projet, modèles, critères de relecture |
| Ressources complémentaires | 8 p. | documentation par outil, données ouvertes, livres, communautés |
| Bibliographie / webographie | 8 p. | ≈ 90 références avec date de consultation |
| Conclusion générale | 8 p. | ce que vous savez faire, les 5 erreurs qui restent, les 6 mois suivants |
| Annexes | **60 p.** | raccourcis Excel, antisèches SQL et DAX, 9 checklists, dictionnaire de données, scripts d'auto-validation, licence, **errata** |

### Instruments d'évaluation restants — 2 épreuves, 2 soutenances, 12 quiz, 11 études de cas

| Instrument | Prévu | Fait | Reste |
|---|---|---|---|
| Quiz de module (15–20 Q) | 22 | 10 (M01–M10) | **12** (M11 → M22) |
| Étude de cas notée | 21 | 10 | **11** |
| Projet de module | 22 (+ pistes M18) | 10 | **12** |
| Épreuve de validation de palier | 4 (fin P1, P2, P4, P5) | 2 (`P1_epreuve_validation.md`, `P2_epreuve_validation.md`) | **2** (P4, P5) |
| Soutenance | 2 (M19, M21) | 0 | **2** |
| Projets du parcours (§E.3) | 30 | 10 | **20** (dont les 8 de M21 et le portfolio M22) |

> **Le retard d'instruments, résorbé en partie.** L'épreuve de palier **P1** (fin de phase 1, après
> M03) était due depuis la clôture de M03 — elle est livrée (`04_evaluations/P1_epreuve_validation.md`,
> 90 min, /20, seuil 14) en même temps que la clôture de M10. Reste **P4** (fin de phase 4, après M15),
> qui n'est pas encore due : la phase 4 n'est pas commencée.

## 4. Options de spécialisation (hors périmètre obligatoire)

| Module | Chap. | Heures | Volume |
|---|---|---|---|
| M23 R pour l'analyse | 5 | 15 h | ≈ 80 p. |
| M24 Data engineering appliqué (ETL/ELT, DuckDB, orchestration) | 5 | 20 h | ≈ 80 p. |
| M25 Données ouvertes, géomatique et cartographie décisionnelle | 4 | 15 h | ≈ 66 p. |
| **Total options** | **14** | **50 h** | **226 p.** |

Si elles sont activées : **157 chapitres · 710 h · 2 681 p.**

## 5. Cadence observée, et ce qu'elle implique

- **≈ 10 pushs par module** : plan (1) → socle (1) → un push par chapitre validé `--strict`
  (5 à 8) → figures + PDF (1) → clôture projet/évaluation/fiche/README (1).
- M08 : 8 chapitres, 10 pushs. **M09 : 6 chapitres, 10 pushs** (`b82cc73` → `5e0ce4e`).
- À cette cadence, les **13 modules restants représentent ≈ 130 pushs**, plus l'appareil du livre
  (≈ 8 à 10 pushs : glossaire, annexes, feuille de route, portfolio, biblio, conclusion, ouverture).
- Le coût dominant n'est pas la rédaction mais le **socle** de chaque nouveau thème : un module qui
  s'appuie sur le fil rouge existant (M10, M12, M20) se livre plus vite qu'un module qui exige un
  nouveau jeu de données et un nouvel outil exécutable (M14 Power BI, M16 Tableau, M17
  automatisation — outils **non exécutables dans cet atelier**, à traiter comme Power Query l'a été
  en M05 : documentés pas à pas, non exécutés, et **déclarés** comme tels).

## 6. Ordre recommandé pour la suite

1. **M11 → M15** — la phase 4 (SQL avancé, fondements BI, modélisation, Power BI, DAX).
2. **Épreuve de palier P4** — à la fin de M15, comme prévu par l'architecture.
3. **M16 → M19** (+ soutenance M19), puis **M20 → M22** (mission finale et portfolio).
4. **Appareil du livre** — glossaire, annexes, feuille de route, portfolio, biblio, conclusion,
   ouverture : de préférence **en fin de parcours**, quand les 620 termes du glossaire existent
   vraiment (leur extraction est mécanique à ce stade).
5. **Options M23–M25** — seulement si le parcours obligatoire est clos.
