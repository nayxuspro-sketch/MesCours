# La Voie des Données — atelier de production du manuel

Formation professionnelle complète : **analyse de données appliquée & Business Intelligence**, du débutant absolu à l'expert.
Ce dépôt contient le manuel en cours de production. Il sert à la fois de **source** (fichiers Markdown), d'**atelier**
(données du fil rouge, scripts de vérité terrain, autovalidation) et d'**imprimerie** (moteur de composition PDF).

## État d'avancement

| Étape | Objet | État |
|---|---|---|
| 1 | Architecture pédagogique (22 modules + 3 options, 143 chapitres, référentiels) | ✅ **validée** — `00_architecture/01_architecture_pedagogique.md` (1 180 l.) + son PDF de 48 p. |
| 1.5 | Socle technique : générateur déterministe, vérité terrain, base DuckDB, chiffres cités, figures | ✅ livré — voir « Chaîne de production » |
| 2 | Rédaction des modules | ⏳ **M01, M02, M03 et M04 rédigés intégralement** — M01 : 11 fichiers, composés en **110 p.** · M02 : 10 fichiers, **113 p.** · M03 : 10 fichiers (C01→C08, projet, évaluation), autovalidés `--strict`, composés en **121 p.** pour un budget de 117 (+3 %) · **M04 rédigé intégralement** : plan `05_livrables/plan_M04.md`, **276 clés `m04_*`/`m04p_*`** mesurées sur les fichiers livrés, C01→C06 + projet + évaluation (24 à 29 titres par chapitre, 6 planches SVG auditées, tableaux de 5 colonnes au plus), rendu de contrôle des six chapitres : **72 p.** soit 12,0 p./chapitre pour un calibre de 12,5, 6 figures sur 6 et 46 glyphes sur 46 au contrôle du PDF, `autovalide M04 --strict` muet (0 avertissement sur les 8 fichiers) ; le projet tourne sur un dossier pourri régénéré par `tools/dossier_M04.py` (24 clés `m04p_*`), et la correction du `rapport_defauts.json` est apportée au générateur (le socle livré conserve la clé d'origine, objet d'étude du point 12 de C01) · **M05 intégralement rédigé le 19/09/2026** : plan `05_livrables/plan_M05.md` (5 chapitres, budget 80 p.). Étapes 1-2 d'ouverture (dossier projet + 87 clés `m05_*`/`m05p_*`) puis 3-7 (C01-C05 + projet + évaluation, 5 planches SVG auditées, `M05.pdf` à 86 p., `controle_pdf.py M05` 0 défaut bloquant, `fiche_controle_M05.md` Q1-Q10 9/10 au vert). Trois moteurs exercés : Power Query documenté (M code 14 étapes, non exécutable dans cet atelier), SQL DuckDB exécuté (11/11), pandas exécuté (15/15). Verdict croisé : pandas `≡` DuckDB, empreinte `7cce2d0c6253f739faf24c7ed205d0f12e6c81ef5f8b7fcd4826ad3bbd98a465`. Cadence 1 push par chapitre : `90d79af` puis `fe001a5` puis `55ca57a` puis `26cba3b` puis `6bdcffa` puis `5fffc60` (HEAD) — mêmes lignes, mêmes sommes, même empreinte) et 87 clés `m05_*`/`m05p_*` mesurées dans `chiffres_manuel.py` (990 clés au total, 2 runs `diff` nul) · **M06 intégralement rédigé le 19/09/2026** : plan `05_livrables/plan_M06.md` (5 chapitres, budget 80 p.). Étapes 1-2 d'ouverture (dossier `tools/dossier_M06.py` graine 43 + `quincaillerie_export.csv` 24 000 l. × 42 col + `schema_3fn.sql` 7 tables + `controles_integrite.sql` + `ATTENDU.json` 18 clés `m06p_*` ; `chiffres_manuel.py M06` 30 clés reproductibles) puis 3-7 (C01-C05 + projet + évaluation, 5 planches SVG auditées extension ≤ 776 px, `M06.pdf` à 69 p., `controle_pdf.py M06` 0 défaut bloquant, `fiche_controle_M06.md` Q1-Q10 10/10 au vert). Trois moteurs : DuckDB **exécuté** (jointure externe NULL = 3 orphelins), SQLite **exécuté** (`PRAGMA foreign_keys = ON`, 7 tables 3FN créées, 0 erreur), PostgreSQL **cité sans exécuté** (règle §1.5). Cadence 1 push par chapitre : `0f8c1a3` (C01), `a3b0b4f` (C02), `9e3b62b` (C03), `b380ee9` (C04), `ff9000f` (C05)  · **M07 intégralement rédigé le 19/09/2026** : plan `05_livrables/plan_M07.md` (8 chapitres, 30 h, budget 117 p. ±15 %). Étapes 1-2 d'ouverture (dossier `tools/dossier_M07.py` graine 44 : `commercial.sql` 4 679 074 o, `commercial.duckdb` 12 333 056 o — 9 tables 3FN + vue `v_ca_mensuel_magasin`, 50 008 ventes dont 8 doublons, 200 retours, 15 dates inversées ; `ATTENDU.json` 31 clés `m07p_*` ; `chiffres_manuel.py M07` 188 clés reproductibles, 2 runs `diff` nul) puis 3-7 (C01-C08 + projet 30 questions + 6 pièges + évaluation 20 Q quiz / 35 exercices auto-validés / étude de cas, 8 planches SVG auditées extension ≤ 776 px total 45,5 Ko, `M07.pdf` à 109 p. dans [99, 135], `controle_sql.py M07` 179/0, `controle_exos_M07.py` 35/35, `controle_pdf.py M07` 0 défaut bloquant, `fiche_controle_M07.md` Q1-Q10 10/10 au vert). DuckDB **exécuté** (179 requêtes des chapitres), PostgreSQL **cité sans exécuté** (règle §1.5 héritée). Cadence 1 push par chapitre : `685eca7` (C01), `281c15e` (C02), `30445fd` (C03), `6dc617d` (C04), `f77828f` (C05), `3df1d2f` (C06), `d07c987` (C07), `323ab91` (C08)) · **M08 intégralement rédigé le 20/09/2026** : plan `05_livrables/plan_M08.md` (8 chapitres, 30 h, budget 117 p. ±15 %). Étapes 1-2 d'ouverture (dossier `tools/dossier_M08.py` : réexport **déterministe** de la base M07 figée en 8 CSV — diff = 0 à la double exécution, empreinte `b9a8d973119342ec…` — + `ATTENDU.json` côté SQL de la croisée ; `chiffres_manuel.py M08` **76 clés** `m08_*`/`m08p_*` reproductibles, diff = 0) puis 3-7 (C01-C08 + projet M08.P + évaluation, 8 planches SVG auditées extension ≤ 776 px total 55,2 Ko, `M08.pdf` à **119 p.** dans [99, 135], `controle_pdf.py M08` 0 défaut bloquant — **8/8 figures embarquées et vérifiées dans le PDF** par leur libellé, 36/36 glyphes, `03_exercices/M08_projet.md` + `04_evaluations/M08_evaluation.md`
livrés (`controle_exos_M08.py` **15/15**, étude de cas « le script du stagiaire » 3 erreurs
typées + un total faux), `fiche_controle_M08.md` Q1-Q10 10/10 au vert). Colonne vertébrale : la **croisée SQL/pandas** (25 valeurs, comptages exacts, totaux ± 2 FCFA, divergence = `ValueError`) — DuckDB exécuté (côté SQL), SQLite exécuté (centimes entiers, concordance exacte avec pandas), PostgreSQL hors module (zéro mention, règle §1.5 à sa forme la plus stricte) ; 12 écritures obsolètes pandas 3.x reproduites verbatim en venv 3.0.6 (4 `AttributeError`, copie-on-écriture silencieuse, `resample('M')` → `ValueError`), 4 écarts 2.2.3/3.0.6 reproduits et chiffrés. Le script du projet est **commité** (`03_exercices/dossier_M08/analyse_commerciale_modele.py`) et exécuté bout en bout (6 sections, 4 PNG, classeur 4 feuilles, sorties publiées). Cadence 1 push par chapitre : `e08cb12` (C01), `705635a` (C02), `c5575f8` (C03), `e4a6958` (C04), `3d0e348` (C05), `c929aaf` (C06), `45aa211` (C07), `294d5e9` (C08), puis le commit final de livraison (PDF module, fiche de
contrôle, README, embarquement de la figure C01, retrait pyc du remote, `.gitignore`) · **M09 intégralement rédigé le 20/09/2026** : plan `05_livrables/plan_M09.md` (6 chapitres, 30 h, N3, budget 92,5 p. ±15 % = [79, 106]). Étapes 1-2 d'ouverture (dossier `tools/dossier_M09.py` graine 45 **déterministe** : quincaillerie réexportée byte-identique à M08, centre de santé 18 818 consultations, scolaire 402 élèves / 6 000 notes / 1 687 absences, fichier projet 10 014 × 10 — 15 défauts plantés comptables, `diff -rq` = 0, empreinte `026d39a6f167b74c…` ; `chiffres_manuel.py M09` **130 clés** `m09_*`/`m09p_*`/`m09v_*`, diff = 0) puis 3-7 (C01-C06 + projet M09.P + évaluation, 6 planches SVG auditées extension ≤ 776 px total 46,4 Ko, `M09.pdf` à **82 p.** dans [79, 106], `controle_pdf.py M09` 0 défaut bloquant — **6/6 figures vérifiées dans le PDF**, 36/36 glyphes —, `controle_exos_M09.py` **15/15**, `03_exercices/M09_projet.md` et `04_evaluations/M09_evaluation.md` livrés, `fiche_controle_M09.md` Q1-Q10 10/10 au vert). Quatre jeux, une seule exigence : **une étape se déclare, elle ne se saute pas**. La corrélation scolaire (−0.232) est démontée en trois fausses causes chiffrées (contrôle par bandes −0.206 → −0.145 / −0.085 / +0.163 ; régression vers la moyenne 7.01 → 7.21 et 14.93 → 14.61 ; sens non départagé), et le scale est démasqué (0.552 en FCFA contre 0.001 en taux). DuckDB **exécuté** (réexport + parallèle SQL/pandas), SQLite **exécuté** (contrôle de la fiche : centimes entiers, concordance exacte), PostgreSQL **zéro mention**. Cadence 1 push par chapitre : `b82cc73` (C01), `8d8d1f8` (C02), `74991c5` (C03), `46912cb` (C04), `2d068c3` (C05), `695f70e` (C06), `293d5c3` (figures + PDF + **correctif de composition** de tout le corpus), puis le commit de clôture (projet, évaluation, fiche, README) |
  `controle_sql.py M04` et `controle_python.py M04` rendent 0 bloc : le module reste outillé tableur et système de fichiers, comme décidé à l’ouverture.
| 3 | Vérification par module (autovalidation R1–R8 + porte de contrôle Q1–Q10 de l'architecture §G.1) | ✅ **M01 → M11 au vert** en mode `--strict` (0 avertissement) · **fiches de contrôle Q1–Q10 publiées** : `05_livrables/fiche_controle_M01_M02.md`, `05_livrables/fiche_controle_M03.md`, `05_livrables/fiche_controle_M05.md` (9/10 vert, 5 écarts), `05_livrables/fiche_controle_M06.md` (10/10 vert, 0 écart bloquant), `05_livrables/fiche_controle_M07.md` (10/10 vert, 2 nuances déclarées), `05_livrables/fiche_controle_M08.md` (10/10 vert, 2 nuances déclarées), `05_livrables/fiche_controle_M09.md` (10/10 vert, 2 nuances déclarées), `05_livrables/fiche_controle_M10.md` (10/10 vert, 3 nuances déclarées), `05_livrables/fiche_controle_M11.md` (10/10 vert, 4 nuances déclarées) |
| 4 | Assemblage, glossaire, index | ⏳ assemblage par module disponible (`render.py --join`) |
| 5 | Composition du manuel PDF (A4, couverture, mise en page éditeur) | ✅ moteur au point — `05_livrables/M01.pdf` (**117 p.**), `M02.pdf` (**122 p.**), `M03.pdf` (**126 p.**), `M04.pdf` (**92 p.**), `M05.pdf` (86 p.), `M06.pdf` (**69 p.**, budget 80 ±15 % = 68-92, OK), `M07.pdf` (**109 p.**, budget 117 ±15 % = 99-135, OK), `M08.pdf` (**119 p.**, budget 117 ±15 % = 99-135, OK), `M09.pdf` (**82 p.**, budget 92,5 ±15 % = [79, 106], OK) `M10.pdf` (**106 p.**, budget 105 ±15 % = [89, 121], OK) et `M11.pdf` (**97 p.**, budget 105 ±15 % = [89, 121], OK — projet et évaluation joints, **9** fichiers) ; les HTML de contrôle, régénérables en 20 s, ont été supprimés le 24/09/2026 pour tenir le quota de l'atelier (165,0 → 127,0 Mo) — les paginations M01-M04 et M08 ont été mesurées **après** le correctif de composition du 20/09/2026 (`img { max-width: 100 % }` : les planches 780 px n'étaient plus rognées à droite) |
| 6 | Revue finale + errata | ⏳ |

## Kit d'exploitation — M01 à M12 (25/09/2026)

Les douze modules publiés (81 chapitres, 1 207 pages de cours, 366 exercices autonomes) étaient
diffusables mais pas utilisables seuls : douze PDF séparés, douze projets et douze évaluations en
Markdown, aucun index général. Le kit comble cet écart, et il est **généré**, jamais recopié :

- **`05_livrables/La_Voie_des_Donnees_M01-M12.pdf`** — **1 395 pages**, 14,0 Mo : couverture,
  sommaire général paginé, les douze modules, les deux cahiers (projets, évaluations), l'index ;
  **124 signets** PDF pour naviguer.
- **`05_livrables/guide_apprenant_M01_M12.md`** — le mode d'emploi de l'apprenant : ce qu'il a,
  dans quel ordre le lire, ce qu'il produit, comment il est corrigé, où sont les fichiers.
- **`05_livrables/index_glossaire_M01_M12.md`** — index des notions (**488** entrées, chacune avec
  les chapitres où elle est traitée), glossaire (**367** définitions), index des planches (**69**),
  des instruments (**48**) et des jeux de données (**10** dossiers) : 855 entrées, triées.
- **`05_livrables/kit_M01_M12.json`** — les mesures du kit, seule source des chiffres du guide.
- **`requirements.txt`** — l'environnement de travail, versions vérifiées le 25/09/2026 :
  duckdb 1.5.5, pandas 2.2.3, numpy 2.3.5, matplotlib 3.10.9, seaborn 0.13.2, openpyxl 3.1.5,
  markdown 3.10.3, weasyprint 70.0, pypdf 6.19.0.
- **`tools/kit_exploitation.py`** — le générateur : mesure, index, puis livre assemblé (sommaire
  auto-paginé par itération, signets repris module par module). `--mesures-seules` mesure en 2 s
  sans composer le livre.

**Contrôles du kit** : 81 chapitres attendus par l'architecture, 81 trouvés ; **366** exercices
autonomes, **0** sans reprise au corrigé ; 2 chapitres de M06 portent leur section d'exercices au
§13 au lieu du §11, ce que l'index signale au lecteur. Deux erreurs de comptage corrigées au
passage : le total de « 243 exercices » annoncé le 25/09 venait d'un artefact de comptage (quatre
mises en forme d'exercices cohabitent dans le manuel), et le fichier d'ouverture `M01_C00`
(1 375 mots) était compté comme un chapitre. Mesure juste : **509 252 mots de cours** dans les 81
chapitres (510 627 avec l'ouverture).

## Dernier module livré — M12 *Fondamentaux de la Business Intelligence* (25/09/2026)

**6 chapitres · 30 h · N3 · budget 92 p. [78, 106].** Le module apprend à choisir **quoi** mesurer,
pour **qui**, et à quelle condition un chiffre devient une décision. Les **6** chapitres sont poussés :
**C01** (définition de la BI, ce qu'elle n'est pas, le coût d'une décision sans donnée),
**C02** (reporting vs BI, les **4** régimes de question : quoi, pourquoi, quoi demain, que faire) et
**C03** (métriques, dimensions, faits, grain — le vocabulaire exact et ses pièges chiffrés) et
**C04** (concevoir un KPI : six critères, carte de définition de sept champs, contre-KPI et effets
pervers — avec les six définitions mesurées du taux de retour, de **1,12 %** à **1,91 %**), **C05**
(l'architecture en sept étages et la panne typique de chacun) et **C06** (les dix causes d'échec d'un
projet BI et la conduite de la reprise). **35 712** mots, **82** pages, **255** clés recalculées, fiche
de contrôle **10/10**, PDF `05_livrables/M12.pdf`.
Le **socle** ajoute au fil rouge six tables déterministes (**1,36 Mo**, graine **46**) : coût d'achat,
stock, ruptures, commandes, encaissements, logistique — les sources qu'un indicateur exige. L'**instrument**
`tools/kpi_M12.py` mesure les **10** KPI du mandat de reprise (CA, marge, rupture, rotation, panier,
retour, service, recouvrement, logistique, part interne) **avec leur définition imprimée à côté du
chiffre** : c'est la thèse du module, appliquée à lui-même.

* Chiffres du module : marge **29,12 %** pour une cible de **18** à **24 %** (cause mesurée : prix de
  vente **+25,0 %**) · rotation **9,42** tours contre **0,78** si l'on somme les stocks · taux de
  service **81,0 %** ou **78,2 %** selon le dénominateur · **1 155** factures de plus de 90 jours
  (**90,8 %** de l'encours) · clients : **188 886** si l'on additionne des comptages distincts pour
  **23 497** réels · une clé oubliée multiplie un total par **15,8** sans lever d'erreur.
* Matériel du projet : `03_exercices/dossier_M12/etude_avant.md` — les **12** pages d'un dispositif raté
  (**41** indicateurs, **7** onglets, **7 940 000** FCFA, **4** ouvertures le premier jour, abandon en
  **11** semaines) ; le livrable attendu est la **carte de définition de 10 KPI**, réutilisée en M13,
  M14, M15 et M21.
* Publication : plan n° **46**, socle n° **47**, C01 n° **48**, C02 n° **49**, C03 n° **50**, C04
  n° **52**, C05 n° **55**, C06 n° **56**, puis la clôture — `05_livrables/journal_pushs.md`.

## Module précédent — M11 *SQL avancé pour la BI* (clôturé le 24/09/2026, poussé le 25/09/2026)

**7 chapitres · 30 h · N3 → N4 · 97 pages composées (budget 105, dérive −8 %) · 42 410 mots · 301 clés
de valeurs publiées.** Le module ouvre la **phase 4** (Business Intelligence) et fait passer l'écriture
SQL de la question simple au **rapport défendable** : fenêtres et partitions, rangs et cumuls, séries
temporelles (calendrier, année sur année, moyennes mobiles), cohortes, rétention et RFM, requêtes
avancées (CTE, `PIVOT`, `UNNEST`, `QUALIFY`, `ROLLUP`), vues, index et plans d'exécution, style et tests
de non-régression. Chiffres du module : rang maximal **23 444** (`RANK`) contre **21** (`DENSE_RANK`) ;
rétention pondérée **15,8 %** à M+1 contre **16,4 %** en moyenne simple ; comparaison 2026/2025
**−28,9 %** sur périmètres inégaux, **+15,4 %** à périmètre égal ; **2** mois sans objectif du magasin 4
pour **93 749 490** FCFA de ventes sans référence ; top 10 % des clients = **38,1 %** du CA
(**24,2 %** hors client non identifié) ; `SELECT *` **581** ms contre trois colonnes **96** ms.

* **Le socle n'est pas une base mais un script.** Un fichier DuckDB de **154** lignes pèse **536 576**
  octets — un plancher mesuré, incompatible avec le quota de 128 Mo. `03_exercices/dossier_M11/`
  contient donc `socle_m11.sql` (**3 595** octets, empreinte `447c7abdafd3ac14`, deux exécutions
  identiques) et `connexion.py` (`ouvrir(materialiser=True)` pour les mesures de volume de C06) :
  **5** tables de référence, **2** vues, **0** orphelin, **1** client de vente absent du référentiel
  (le client **0**, fait central du module). Coût en dépôt : **0,004 Mo**.
* **L'instrument le plus réutilisable du manuel** : `tools/controle_sql_M11.py` rejoue **18** requêtes
  et les confronte aux valeurs publiées — `18 controles sur 18 : OK`, **code de retour** utilisable en
  chaîne. Il a trouvé **deux erreurs, les siennes** (client **0** compté retours compris ; ordre de tri
  réécrit dans le test, **23 497** au lieu de **23 444**), toutes deux **publiées** dans C07.
* **La mesure ne se relit pas à l'horloge** : `tools/perf_M11.py --figer` gèle les médianes de **5**
  exécutions dans `PERF_M11.json` (**24/09/2026**, DuckDB 1.5.5) et `chiffres_manuel.py` **relit** ce
  fichier ; le protocole est imprimé à côté de chaque temps.
* **Deux moteurs croisés** : DuckDB et SQLite sont **exécutés** (SQLite transforme `SCAN ventes_t` en
  `SEARCH … USING INDEX`, mais DuckDB garde `SEQ_SCAN` : l'index n'apporte rien) ; PostgreSQL et SQL
  Server sont **cités** (tableau de compatibilité C05 : `QUALIFY` et `PIVOT` absents ailleurs) — règle
  §1.5. Le partitionnement est **cité, non exécuté**, et déclaré comme tel.
* **Corrections assumées** : le top 3 par famille passe de **18** à **21** lignes et le catalogue de
  **6** à **7** familles (**16** libellés → **9** écritures → **7** familles) après mesure du
  référentiel produits ; les chapitres concernés ont été repatchés et la clé partagée corrigée.
* **Livrables** : `05_livrables/plan_M11.md`, `02_modules/M11_C01…C07`, `03_exercices/M11_projet.md`
  (« Les **12** rapports SQL de la cellule commerciale », 4 livrables **8 + 5 + 4 + 3 = 20**,
  seuil 13),
  `04_evaluations/M11_evaluation.md` (**70** points : quiz 20 Q, 5 exercices, auto-test 18 requêtes,
  étude de cas /20 seuil 12), `tools/controle_sql_M11.py`, `tools/perf_M11.py`, `tools/figures_M11.py`,
  `figures/M11_C01_carte_des_fenetres.svg` (**609** px) et `figures/M11_C04_matrice_retention.svg`
  (**686** px), `03_exercices/dossier_M11/`, `05_livrables/fiche_controle_M11.md`,
  `05_livrables/M11.pdf` (**97** p.).
* **Publication : complète.** **10 pushs** (n° 36 → n° 45) du plan à la clôture, un par chapitre, puis
  l'appareil du module ; le jeton fourni le 25/09/2026 a été validé avant tout envoi, et la file
  d'attente a été vidée en une passe. Détail : `05_livrables/journal_pushs.md`. Dépôt : **363**
  fichiers, **0** `.pyc`, **18** PDF, procédure en **ajout seul** (jamais `git add -A`).

## Module précédent — M10 *Data visualization* (clôturé le 24/09/2026)

**7 chapitres · 30 h · N3 · 106 pages composées (budget 105, dérive +1 %).** Le module apprend à
**relire** un graphique avant de le produire : ordre perceptuel (position > longueur > angle >
surface > couleur), table des **16** graphiques, couleurs et accessibilité, écriture (titres, axes,
annotations), les **10** erreurs avec leur effet **mesuré**, la séquence de trois écrans, et la
sortie (matplotlib, Excel, Power BI). Chiffres du module : axe tronqué **× 7,0** d'amplitude
apparente pour **5,4 %** réels ; corrélation **affichée +0,35** par le double axe ; **0,17°** entre
deux parts de camembert ; **5,4 %** de totaux masqués par un cumul à 100 % ; masse passant de
**42,1 %** à **93,5 %** de largeur en échelle logarithmique.

* Livrables : `05_livrables/plan_M10.md`, `02_modules/M10_C01…C07` (**325** clés `m10_*`, diff = 0),
  `03_exercices/dossier_M10/` (5 graphiques ratés + 5 corrigés + `ATTENDU.json`, `diff -rq` = 0),
  `tools/dossier_M10.py`, `perception_M10.py`, `seize_graphiques_M10.py`, `couleurs_M10.py`,
  `ecriture_M10.py`, `erreurs_M10.py`, `sequence_M10.py`, `outils_M10.py`, `figures_M10.py`,
  `controle_refonte_M10.py`, `03_exercices/M10_projet.md` (« La refonte », 4 livrables /20 seuil 13),
  `04_evaluations/M10_evaluation.md` (65 points), `05_livrables/grille_visuelle_18_points.md`,
  `05_livrables/fiche_controle_M10.md`, `05_livrables/M10.pdf` (106 p.).
* **Le contrôle du projet** (`controle_refonte_M10.py`, 4 couches) accepte le dossier de référence
  (`CONFORME`) et **rejette** une copie dont les totaux avant/après diffèrent — il a aussi trouvé un
  défaut réel dans le matériel livré (`g5_corrige.svg`, 806 px → **768** px).
* **Power BI est cité, non exécuté** (9 clics décrits) ; matplotlib, seaborn et Excel sont exécutés
  (classeur écrit **puis relu** : écart **0,00** FCFA sur **24** valeurs) — règle §1.5.
* L'errata du §E.7 de l'architecture (**20** points « 4 par famille » → **18** points, familles
  **4 / 5 / 5 / 4**) est reporté dans le fichier d'architecture à cette clôture.

## Arborescence réelle

```
formation-data-bi/
├── README.md                         ← ce fichier
├── requirements.txt                  ← environnement de travail (versions vérifiées le 25/09/2026)
├── 00_architecture/                  ← étape 1 : plan directeur validé (+ son PDF)
├── 01_socle_donnees/
│   ├── data/brut/                    ← 243 360 lignes de ventes brutes, défauts compris (20 fichiers)
│   ├── data/reference/               ← référentiels propres, vérité terrain, ATTENDU du projet M01,
│   │                                    NOTICE.md, stats_generation.json, rapport_defauts.*, chiffres_cites.{json,md}
│   ├── data/projection/              ← le fichier reçu par l'apprenant de M01 (489 lignes de données × 13 colonnes)
│   ├── data/sahel.duckdb             ← la base du fil rouge (schéma, contraintes, vue de contrôle)
│   └── scripts/
│       ├── generation_socle.py       ← générateur déterministe (graine 20260917) : bruts + propres + ATTENDU
│       ├── chiffres_manuel.py        ← SOURCE UNIQUE des chiffres cités dans le manuel → data/reference/
│       └── autovalide.py             ← contrôle qualité R1–R8 d'un module rédigé
├── 02_modules/                       ← M01_C00…C07 + M01_bilan · M02_C01…C08 · M03_C01…C08 (16 blocs par chapitre, calibre 12,5 p.)
├── 03_exercices/                     ← M01_projet.md, M02_projet.md, M03_projet.md : énoncé, matériel, six livrables,
│                                       barème détaillé, corrigé pas à pas
├── 04_evaluations/                   ← M01_evaluation.md (quiz 15 Q) · M02_evaluation.md (quiz 20 Q) · M03_evaluation.md
│                                       (quiz 15 Q, 4 exercices, étude de cas) : récupération, exercices,
│                                       étude de cas, corrigés, décision d'orientation
├── 05_livrables/                     ← PDF assemblés par module (M01.pdf 117 p. … M12.pdf 82 p.), fiches de
│                                       contrôle Q1–Q10, plans de module, et le KIT D'EXPLOITATION :
│                                       La_Voie_des_Donnees_M01-M12.pdf (1 395 p., 124 signets), guide_apprenant,
│                                       index_glossaire, kit_M01_M12.json (mesures). Le HTML de contrôle n'y est
│                                       pas stocké : 6,6 Mo par module, `render.py` le rend en 20 s au besoin
├── figures/                          ← SVG des planches : 7 pour M01, 4 pour M02, 9 pour M03, citées en ../figures/… depuis 02_modules/
└── tools/                            ← render.py (Markdown → HTML → PDF), kit_exploitation.py (le kit M01-M12),
│                                       poids.py (garde-fou de quota),
│                                       figures_M01.py, figures_M02.py,
│                                       figures_M03.py, classeur_M03.py (le classeur d'atelier de M03),
│                                       budget_pages.py, nb_pages.py, controle_sql.py, controle_python.py et
│                                       controle_formules.py (porte §G.1 : tout ce qui est publié dans un chapitre
│                                       est exécuté — formules de tableur comprises, recalculées par `formulas`),
│                                       controle_pdf.py (le seul contrôle qui lit le fichier composé),
│                                       fonts/ (instances statiques)
```

## Chaîne de production d'un module (dans cet ordre, sans raccourci)

```bash
cd /home/user/formation-data-bi

# 1. (une fois) générer le socle de données et ses fichiers d'attendus
python3 01_socle_donnees/scripts/generation_socle.py

# 2. recalculer TOUS les chiffres cités après un changement de socle ou de générateur
python3 01_socle_donnees/scripts/chiffres_manuel.py                # → data/reference/chiffres_cites.{json,md}
#    Lancer SANS argument régénère les cinq sections. Depuis le 18/09/2026, un appel restreint
#    (`… M04` seul) fusionne avec le fichier existant au lieu de l'écraser : un relevé partiel
#    publié fait tomber la règle n°2 de tous les autres chapitres (mesuré : 55/190/97 erreurs).
#    (`pypdfium2` installé : `budget_pages.py --mesure` lit le PDF composé ; sinon il le dit et estime par les mots)

# 3. rédiger les fichiers Markdown (02_modules/, 03_exercices/, 04_evaluations/)

# 4. autovalider le module — bloquant — et vérifier le budget de pages
python3 01_socle_donnees/scripts/autovalide.py M01 --strict
python3 tools/budget_pages.py --mesure

# 5. assembler le PDF du module (couverture, TOC paginée, en-têtes/pieds, encadrés)
python3 tools/render.py "02_modules/M01_*.md" --join \
    --out 05_livrables/M01.pdf \
    --titre "Module M01 — Fondamentaux de la donnée" \
    --sous-titre "Phase 1 · Lire les données et comprendre le métier de l'analyse"
#    (le --joint prend aussi 03_exercices/M01_*.md et 04_evaluations/M01_*.md : glob large ou liste explicite)
#    (à la fin, ne garder que le PDF : `rm 05_livrables/*.html` — 6,6 Mo par module, et le HTML se refait)

# 6. garder l'œil sur le quota persistant (128 Mo) — liste des artefacts et leur remède
python3 tools/poids.py --strict
python3 tools/render.py 02_modules/M01_C01_…md            # un seul fichier : --html-only | --no-toc | --no-cover | --batch "…"
```

**Ce que vérifie `autovalide.py`** (règles opposables, exécutées sur les chapitres **et** sur le projet et l'évaluation) :

| Règle | Contrôle |
|---|---|
| R1 | les 16 blocs du gabarit §B.3 sont présents **et dans l'ordre** |
| R2 | tout nombre de 4 chiffres et plus cité dans le module est sourcé : `chiffres_cites.json`, statistiques de génération, fichiers du socle lus sur disque, année, multiple/somme/différence de nombres du socle, ou nombre d'un énoncé d'exercice |
| R3 | chaque figure `.svg` citée existe |
| R4 | chaque chemin de fichier cité en dur existe |
| R5 | chaque « Exercice c.n » a sa reprise dans le bloc « Correction détaillée » |
| R6 | les barèmes tombent juste (total = somme des lignes du tableau) **et** toute égalité écrite en l'est réellement (`12 × 40 = 480`, précédence des ×, séparateurs de milliers) |
| R7 | aucun idéogramme parasite, aucun mot doublé, aucun anglicisme sans son couple « français — English » |
| R8 | la fréquence des six encadrés pédagogiques respecte le §B.4 (4–8 Définition, 2–4 À retenir, 2–5 Attention, 1–3 Conseil professionnel, 1–2 Dans les faits, 1 Boîte à outils par section-outil) |

> **Un corrigé n'est pas une mesure (décision du 18/09/2026, module M04).** Le fichier
> `01_socle_donnees/data/reference/rapport_defauts.json`, livré comme corrigé enseignant du socle, annonce 3 360
> montants texte, 2 640 dates au format mixte, 1 880 villes absentes et 61 catégories hétéroclites ; le fichier
> livré mesure 3 421, **0**, 1 911 et 44. C'est le plan d'injection des défauts, pas l'état du fichier. Il n'est
> pas réécrit avant la fin de la rédaction de M04 : le module s'en sert comme objet d'étude (point 12 du
> diagnostic de `M04_C01`), et la correction passera par `generation_socle.py` + un recalcul du seul JSON, pour ne
> pas réécrire 54 Mo de CSV. **Appliqué le 18/09/2026 à la fin de la rédaction** : le générateur recompte le
> corrigé sur les fichiers livrés (testé isolé : il reproduit exactement les valeurs citées par le module) ;
> la version du socle livrée dans l'atelier conserve la clé d'origine, qui est l'objet d'étude du point 12
> de `M04_C01` et de l'exercice E4 de l'évaluation — c'est voulu. Détaillé dans `05_livrables/plan_M04.md`, §1.

## Hygiène du dépôt de travail (quota d'espace persistant)

L'atelier est borné à **128 Mo persistés**. La source éditable du manuel — Markdown, SVG, scripts,
`chiffres_cites.json` — ne pèse que **1,7 Mo** : tout le reste est des artefacts, et un artefact s'il est
regénérable ne doit pas être gardé. Mesuré le 18/09/2026 après application des règles du tableau :
**70,6 Mo comptés pour 128, marge +57,4 Mo, 110 fichiers (mesuré le 18/09/2026, après trois chapitres de M04)** (`python3 tools/poids.py` le rend à tout moment).
Avant ce nettoyage : 128,9 Mo, bloqué.

| Règle | Gain mesuré | Comment la rendre effective |
|---|---|---|
| Ne pas laisser le HTML de composition à côté du PDF | 6,6 Mo par module | `rm 05_livrables/*.html` après chaque rendu (il se refait en 20 s) |
| Ne pas persister les instances de polices | 7,5 Mo | `render.py` les recrée en 3 s depuis les 4 variables (`serif.ttf`, `serif-it.ttf`, `sans.ttf`, `mono.ttf`) ; seuls ces quatre fichiers sont la source |
| Ne pas réinstaller les paquets sans purger le cache | ~9 Mo par tour | `pip install --no-cache-dir markdown weasyprint pypdfium2 fonttools` (le cache atterrit dans `~/.cache/pip`) |
| La base DuckDB est dérivée, pas source | 21,3 Mo | **fait le 18/09/2026** : `data/sahel.duckdb` n'est plus persisté. Vérifié sans elle : les 9 blocs SQL de M02 passent (`9 réussites, 0 échec`), les 123 contrôles de formules aussi, `autovalide --strict` muet sur les trois modules. Elle se rend par `python3 01_socle_donnees/scripts/generation_socle.py` (graine `20260917`) quand un chapitre veut l'interroger (M02.C01, étape 7) |
| Les deux gros CSV du socle | 39 Mo **abandonnés, à dessein** | gzip les ferait passer de 27,2 + 26,8 à 7,6 + 7,4 Mo, mais ils sont **cités par leur nom dans 12 fichiers du manuel** (M01.C00→C07, M02.C01/C07/C08, la NOTICE, l'architecture) : les renommer rendrait fausses des pages enseignées. On ne les touche pas |

À terme (19 modules restants), les PDF composés représentent ~1,4 Mo × module, soit **27 Mo** : si le quota
devient gênant, les pousser dans `.cache/livrables/` — dossier exclu du snapshot — et ne conserver dans
`05_livrables/` que le module en cours et les fiches de contrôle.

## Volumétrie mesurée des modules composés

### M01 — assemblage `05_livrables/M01.pdf`, 110 pages

| Partie | Pages | Observations |
|---|---|---|
| C00 Ouverture du module | 3 | carte des chapitres, méthode, livrables attendus |
| C01 Se repérer dans un ordinateur de travail | 12 | |
| C02 Donnée, information, connaissance, décision | 11 | |
| C03 La table : lignes, colonnes, clés | 12 | |
| C04 Types de données | 12 | |
| C05 Structurées / qualitatives / quantitatives | 13 | |
| C06 Cycle de vie d'une donnée | 12 | |
| C07 Métiers + anatomie d'une analyse | 14 | chapitre-pivot du module |
| Bilan de compétences | 3 | |
| Projet M01.P (énoncé + barème + corrigé) | 5 | |
| Évaluation (quiz 15 Q + étude de cas + corrigés) | 6 | |
| **Total** | **110** | 7 p. de couverture, TOC et sauts de section |

Chiffres de matière des sept chapitres : **42 044 mots**, **88 encadrés** (40 Définition, 14 À retenir,
16 Attention, 7 Conseil professionnel, 7 Dans les faits, 4 Boîte à outils), **37 exercices autonomes — chacun
avec sa correction détaillée et son barème** —, 7 mini-projets `M01.P1…P7`, 7 évaluations formatives
auto-corrigées, 7 planches SVG (une par chapitre).

### M02 — assemblage `05_livrables/M02.pdf`, 113 pages

| Partie | Pages | Observations |
|---|---|---|
| C01 Population, échantillon, variables, fréquences | 11 | aucune ouverture de module répétée : M02 reprend le fil de M01 |
| C02 Centres : moyenne, médiane, mode | 11 | le chapitre que tout le monde croit connaître |
| C03 Dispersion : étendue, IQR, écart type | 11 | |
| C04 Positions : quartiles, déciles, percentiles | 12 | quatre méthodes de percentile, un chiffre, une règle annoncée |
| C05 Formes : histogramme, asymétrie | 11 | 46,9 % du chiffre d'affaires dans une seule classe : la leçon du graphique raté |
| C06 Relations : covariance, corrélation, causalité | 12 | contrôle de confusion chiffré avant/après |
| C07 Hasard, échantillonnage, biais | 13 | biais de couverture mesuré (médiane −14,3 %) |
| C08 Décider : intervalles, tests, limites | 13 | t-test, permutation, rangs, chi², puissance, six comparaisons non concluantes |
| Projet M02.P (6 livrables + barème + corrigé) | 6 | |
| Évaluation (récupération, quiz 20 Q, exercices, étude de cas, corrigés) | 6 | |
| **Total** | **113** | 7 p. de couverture, TOC et sauts de section |

Chiffres de matière des huit chapitres : **49 149 mots**, **97 encadrés** (40 Définition, 16 À retenir, 16 Attention,
9 Conseil professionnel, 8 Dans les faits, 8 Boîte à outils), **40 exercices autonomes — cinq par chapitre, chacun avec
sa correction détaillée et son barème** —, 4 mini-projets `M02.P1…P4` dont P4 est noté sur deux volets, 8 évaluations
formatives auto-corrigées, 4 planches SVG (C04, C05, C07, C08), et un test de comparaison entre deux magasins conduit
au tableur **puis** en Python dans le projet.

### M03 — assemblage `05_livrables/M03.pdf`, 121 pages

| Partie | Pages | Observations |
|---|---|---|
| C01 Interface, classeur, feuille, cellule | 13 | les six réflexes avant toute formule ; la feuille `Aidez-moi` du classeur |
| C02 Formats et saisie | 11 | le même montant, trois chiffres selon la voie d'import : 0 · 2 444 · 36 073 185 |
| C03 Tableau structuré, tri, filtres, doublons | 11 | `TableVentes`, portée vérifiée à chaque import, dédoublonnage conduit sur la clé |
| C04 Formule, adresses, erreurs | 12 | récurrences relative et absolue, les sept erreurs nommées une par une |
| C05 Agrégats et fonctions conditionnelles | 12 | `NB` contre `NBVAL` : le contrôle qui ferme la porte au total faux |
| C06 Recherches et assemblage | 13 | le piège de `RECHERCHEV`, la voie `RECHERCHEX`, le repli `INDEX/EQUIV` pour 2019 |
| C07 Dates, périodes, matricielles | 13 | 424 dates en format international, 65 en texte, les deux voies du calendrier |
| C08 TCD, puissance du modèle, protection | 13 | le TCD écrit à la main, sa limite, le modèle de données, les garde-fous |
| Projet M03.P (six livrables + barème + corrigé) | 6 | classeur de pilotage, 20 points, seuil 13 |
| Évaluation (récupération 9 Q, quiz 15 Q, 4 exercices, étude de cas) | 6 | corrigés chiffrés, table de décision d'orientation |
| **Total** | **121** | 11 p. de couverture, TOC et sauts de section — la somme des parties rend 110 p. |

Chiffres de matière des huit chapitres : **53 486 mots**, **104 encadrés** (33 Définition, 29 À retenir, 17 Attention,
10 Conseil professionnel, 9 Dans les faits, 6 Boîte à outils), **43 exercices autonomes — cinq ou six par chapitre,
chacun avec sa correction détaillée et son barème —**, huit exercices guidés notés sur 10 (le § 10 de chaque
chapitre), 8 évaluations formatives auto-corrigées, 9 planches SVG (une par chapitre, deux pour C08), et le
classeur d'atelier de 11 feuilles `01_socle_donnees/data/projection/m03_classeur_atelier.xlsx`, dont la feuille
`Calculs` s'auto-contrôle en 28 fiches et dont les 123 contrôles sont recalculés par `tools/controle_formules.py`.

> **Densité mesurée.** M02 compose 113 pages pour 55 264 mots (compteur du contrôle de budget), soit **489 mots par page** contre 457 à M01 : les
> chapitres de statistiques embarquent plus de tableaux de bornes et de sorties de calcul : ces blocs remplissent la
> page avec moins de mots, et ils sont exactement ce qu'on ne veut pas couper. Le budget additif de l'architecture (117 p.) est tenu à **−3 %**, et le contrôle `budget_pages.py --mesure`
> reste au vert. Chaque chapitre mesure de 11 à 13 pages, dans la fourchette de calibre (10 à 16).

### M05 -- assemblage `05_livrables/M05.pdf`, 86 pages

| Partie | Pages | Observations |
|---|---|---|
| C01 Le langage commun des transformations | 14 | les 10 opérations, les 4 classes (M, Opérateurs, Paramètres, Agrégations), les 3 moteurs |
| C02 Power Query : sources, étapes, types | 17 | 14 étapes manuelles (M code), `MoisCible` paramétré lisant `parametres.xlsx` |
| C03 SQL DuckDB : 11 CTE, le verdict du fil rouge | 16 | requête SQL **exécutée** sur le brut (mars = 6 884 l. → 6 798 l. après dedup) |
| C04 pandas 2.2.3 : 8 cellules de notebook | 17 | chaîne canonique `assign` -> `sort_values` -> `drop_duplicates`, verdict sha256 |
| C05 Arbitrer un outil par situation | 12 | grille 4 critères (taille, fréquence, compétences, gouvernance) × 3 outils, mesures sur 3 tailles |
| Projet M05.P (énoncé + barème + corrigé) | 6 | 6 livrables, 9 défauts, empreinte sha256 `7cce2d0c...` |
| Évaluation (récupération 7 Q, quiz 15 Q, 4 exercices, étude de cas) | 6 | corrigés chiffrés, 4 critères de l'arbitrage en Q13-Q15 |
| **Total** | **86** | 8 p. de couverture, TOC et sauts de section |

Chiffres de matière des cinq chapitres : **35 750 mots**, **95 encadrés** (18 Définition, 15 À retenir, 10 Attention,
16 Conseil professionnel, 9 Dans les faits, 7 Boîte à outils), **33 exercices autonomes** (4 à 7 par chapitre),
**15 fragments Python exécutés** (`controle_python.py M05` rend 0 défaut), **11 requêtes SQL DuckDB exécutées**
(`controle_sql.py M05` rend 0 erreur), 5 planches SVG (une par chapitre), et le verdict croisé : pandas ≡ DuckDB
sur la même empreinte sha256 `7cce2d0c6253f739faf24c7ed205d0f12e6c81ef5f8b7fcd4826ad3bbd98a465`. C'est la garantie
de **portabilité** du pipeline M05 : le même fichier brut produit la même table dans deux moteurs indépendants.

> **Densité mesurée de M05.** M05 compose 86 pages pour 35 750 mots, soit **416 mots par page** -- en-dessous
> des 489 de M02 et des 457 de M01, parce que les chapitres pipeline (C02/C03/C04) embarquent beaucoup de blocs
> code et de figures SVG qui remplissent la page avec moins de mots. Le budget additif de l'architecture (80 p.)
> est tenu à **+8 %**, dans la tolérance ±15 % contrôlée par `python3 tools/budget_pages.py --mesure`. Chaque
> chapitre mesure de 12 à 17 pages, dans la fourchette de calibre (10 à 16) ; C02 (Power Query) et C04 (pandas)
> à 17 sont les deux plus denses, parce qu'ils portent la matière du `TRY_CAST` (C04) et de la fonction paramétrée
> (C02). Si l'étape 4 doit revenir au calibre 12,5, les deux coupes naturelles sont C02 §5 (les 14 étapes, qui
> peuvent devenir un tableau récapitulatif d'une page) et C04 §5 (la chaîne pandas, déjà très compacte) --
> décision reportée, pas un défaut.

> **Calibre en vigueur (décision du 17 septembre 2026, actée après mesure de M01).**> **Calibre en vigueur (décision du 17 septembre 2026, actée après mesure de M01).** Un chapitre = **12,5 pages** :
> 7 pages de matière (blocs 1 à 9 et 14 à 16 du gabarit) et 5,5 pages d'exercices embarqués (blocs 10 à 13), plus
> **17 pages d'appareil de module** (ouverture 3, bilan 3, projet 5, évaluation 6). M01 est composé à 110 pages pour
> un budget de 105 : **+5 %**, dans la tolérance de ±15 % contrôlée par `python3 tools/budget_pages.py --mesure`.
> Le budget de l'architecture (§F.4), les totaux annoncés (**≈ 2 455 pages** en intégral, 1 692 en condensé, 747 à la
> fin de M07) et le sous-titre de couverture ont été rebasés en conséquence. **Le contenu ne se réduit pas pour rentrer
> dans un format** : si un module dérive au-delà de ±15 %, on corrige la rédaction là où c'est du remplissage, sinon on
> recalcule le budget — jamais l'inverse.

### M06 -- assemblage `05_livrables/M06.pdf`, 69 pages

| Partie | Pages | Observations |
|---|---|---|
| C01 Pourquoi une base (et pas un classeur Excel) | 12 | les 5 limites du classeur (volumétrie, intégrité, concurrence, types, atomicité) et la solution SGBD |
| C02 Table, colonne, schéma, type, contrainte | 13 | anatomie d'une table, 1NF/2NF/3NF, types stricts `INTEGER`/`DECIMAL`/`VARCHAR`, contraintes `CHECK`, vue calculée `ligne_vente_ttc` |
| C03 Clés et relations (primaire, étrangère, 1-N, N-M) | 14 | règle d'or FK du N vers le 1, `ON DELETE` (RESTRICT/CASCADE/SET NULL), jointure externe NULL = 0 |
| C04 Vivre avec DuckDB / SQLite / PostgreSQL | 16 | DuckDB **exécuté** (`pip install duckdb --no-cache-dir`, `read_csv_auto`, jointure externe NULL = 3) ; SQLite **exécuté** (`PRAGMA foreign_keys = ON`, schéma 3FN) ; PostgreSQL **cité sans exécuté** (règle §1.5) |
| C05 Paysage NoSQL, datalake, entrepôt | 14 | 4 familles NoSQL (document, clé-valeur, graphe, colonnes), DWH/lac/lakehouse, 5 mots (sharding, replication, CAP, ACID/BASE, ETL/ELT), verdict 80 % SQL / 20 % NoSQL |
| Projet M06.P (énoncé + barème + corrigé) | — | 5 livrables, 4 défauts (142 montants texte, 8 doublons, 12 dates inversées, 3 orphelins), barème /20 seuil 13 |
| Évaluation (récupération 10 Q, quiz 15 Q, 2 exercices, étude de cas) | — | corrigés chiffrés, règle DuckDB/SQLite exécutés vs PostgreSQL cité en Q12 |
| **Total** | **69** | 8 p. de couverture, TOC et sauts de section |

Chiffres de matière des cinq chapitres : **30 clés `m06_*`/`m06p_*`** (12 mesures `m06_*` + 18 livrables `m06p_*`), dossier généré par `tools/dossier_M06.py` graine 43 (empreinte `f296a11cee7b239df27e0f2b16d21bb8714242127d907abdd58309dfe64c8137`), 5 planches SVG (une par chapitre, extension max 757 px ≤ 776, 0 glyphe hors jeu, total 28,7 Ko). `autovalide M06 --strict` muet (0 avertissement sur les 7 fichiers : C01→C05 + projet + évaluation). `controle_pdf.py M06` : 69 pages, 0 défaut bloquant, 32/32 glyphes composés.

> **Densité mesurée de M06.** M06 compose 69 pages pour ~ 30 000 mots, soit **≈ 435 mots par page** -- proche des 416 de M05 et des 489 de M02, dans la fourchette de calibre. Le budget additif (80 p.) est tenu à **−14 %**, dans la tolérance ±15 % contrôlée par `python3 tools/budget_pages.py --mesure`. La densité des planches SVG (28,7 Ko) est conforme à la convention modules antérieurs (M01-M05 : < 80 Ko par module). Si l'étape 4 doit revenir au calibre 12,5, l'annexe paysages NoSQL/DWH (C05 §7) peut absorber une page supplémentaire sans casser la cohérence éditoriale -- décision reportée, pas un défaut.

### M07 -- assemblage `05_livrables/M07.pdf`, 109 pages

| Partie | Pages | Observations |
|---|---|---|
| C01 Le premier contact : SELECT, FROM, alias, DISTINCT, LIMIT, l'ordre réel d'exécution | 13 | ordre d'exécution FROM → WHERE → SELECT → GROUP BY → HAVING → ORDER BY → LIMIT, alias, `DISTINCT` |
| C02 Filtrer : WHERE, opérateurs, IN, BETWEEN, LIKE, IS NULL | 13 | foncteurs booléens, priorité `AND`/`OR`, `IN`/`BETWEEN`/`LIKE`/`IS NULL`, les 6 valeurs NULL |
| C03 Trier, limiter, paginer : ORDER BY, multi-clés, ASC/DESC, NULLS FIRST/LAST | 12 | multi-clés, `LIMIT`/`OFFSET`, `LIMIT 1` pour le top, LIMIT sans ORDER BY non déterministe |
| C04 Agréger : COUNT, SUM, AVG, MIN, MAX, NULL | 12 | N lignes → 1 valeur, `COUNT(*)` vs `COUNT(colonne)` vs `COUNT(DISTINCT)`, les agrégats igno-rent les NULL (`SUM` vide = NULL), contrôle total |
| C05 Résumer par groupe : GROUP BY, HAVING, le piège du libellé doublé | 13 | clé vs libellé (rayon 5 vs catégories 8), WHERE avant / HAVING après, contrôle somme des groupes, `COUNT(DISTINCT)` dans un groupe |
| C06 Catégoriser : CASE, COALESCE, NULLIF, trancher les montants | 13 | ordonnancement top-down des branches, `ELSE`, tranches, `COALESCE` ne remplace que le NULL, `NULLIF` |
| C07 Joindre : INNER, LEFT, FULL, CROSS, la jointure étoile et celle qui double | 12 | les 4 jointures, condition dans l'`ON` pas dans le `WHERE`, jointure étoile 4 tables = 50 008, la jointure qui double = 2 131 064 |
| C08 Sous-requêtes, CTE, vues, EXISTS vs IN, « tous les » et la double négation | 13 | CTE multi-ligne, vue `v_ca_mensuel_magasin` (120 lignes), EXISTS vs IN, la double négation (0 client sur « tous les ») |
| Projet M07.P (énoncé + barème + corrigé mesuré) | — | 30 questions (194 lignes de SQL attendues), 6 pièges P1–P6 chiffrés, barème /20 seuil 13 |
| Évaluation (récupération 8 Q, quiz 20 Q, 35 exercices auto-validés, étude de cas) | — | `controle_exos_M07.py` 35/35 ; seuils 13/20, 28/35, 12/20 |
| **Total** | **109** | 8 p. de couverture et TOC, 101 p. de contenu (12-13 p./chapitre) |

Chiffres de matière : **188 clés `m07_*`/`m07p_*`** (mesures DuckDB live + socle + `ATTENDU.json` 31 clés),
dossier généré par `tools/dossier_M07.py` graine 44 (empreintes `cdb12cee…56b0b` SQL / `df9333ff…a1dde` BD),
8 planches SVG (une par chapitre, extension max 765 px ≤ 776, 0 glyphe hors jeu, total 45,5 Ko).
`autovalide M07 --strict` muet (0 avertissement sur les 8 chapitres) ; `controle_sql.py M07` : **179 requêtes
exécutées sur `commercial.duckdb`, 0 échec** (dont 6 démos d'erreurs `-- ERREUR ATTENDUE` qui échouent
comme prévu) ; `controle_exos_M07.py` : **35/35** ; `controle_pdf.py M07` : 109 pages, 0 défaut bloquant,
34/34 glyphes composés. Règle §1.5 héritée de M06 : DuckDB exécuté, PostgreSQL cité sans exécuté
(« Dans les faits » de C04 §13, C06 §13, C07 §13, C08 §13).

> **Densité mesurée de M07.** M07 compose 101 pages de contenu pour ~ 41 000 mots, soit
> **≈ 406 mots par page** — dans la fourchette de calibre (M05 : 416, M06 : ≈ 435, M02 : 489).
> Le budget (117 p. ±15 % = [99, 135]) est tenu à **−7 %**. Le fil rouge du module tient :
> la jointure étoile 4 tables compte 50 008 ventes comme la table seule, et la jointure qui
> double en compte 2 131 064 — la différence est la compétence.
>
> ### M08 -- assemblage `05_livrables/M08.pdf`, 119 pages
>
> | Partie | Pages | Observations |
> |---|---|---|
> | C01 Installer sans stress : Python, pip, environnements virtuels, VS Code et Jupyter | 13 | les 4 couches, venv, `requirements.txt`, le premier script (calculateur de remise) |
> | C02 Les fondations sans données : variables, types, opérateurs, entrées/sorties, erreurs | 12 | les 4 types, la matrice des opérations, les entrées/sorties, lire une `TypeError` |
> | C03 Décider et répéter : if/elif/else, boucles for/while, break/continue, compréhensions | 13 | l'échelle if/elif/else, `for`/`while`, `break`/`continue`, les compréhensions |
> | C04 Ranger : listes, tuples, chaînes, dictionnaires, ensembles, tris | 13 | les 5 conteneurs et leurs équivalents SQL, `sorted`/`sort`, les ensembles |
> | C05 Organiser : fonctions, arguments, portée, docstring, modules, try/except, fichiers | 15 | la signature, la portée, `try/except`, lire une traceback, lire/écrire un fichier |
> | C06 NumPy utile et suffisant : tableaux, vecteurisation, statistiques, NaN, where, broadcasting | 13 | la boucle vs une ligne (**mesurée**), `np.nan`, `np.where`, le broadcasting |
> | C07 pandas I : Series, DataFrame, read_csv/read_excel, loc/iloc, filtres, describe, valeurs manquantes | 17 | Series/DataFrame, `read_csv` des 8 CSV, `loc` vs `iloc` (les 4 cas), `describe`, les valeurs manquantes |
> | C08 pandas II : groupby/agg, transform, merge, pivot_table, dates/resample, apply, export Excel | 17 | `groupby` en centimes entiers, `transform`, `merge` (la table vide → 50 008 `NaN`), la vue M07 reconstruite (120 lignes), `resample('ME')`, `apply` vs vectorisation (**mesuré, 4×**), l'Excel multi-feuilles, la leçon des centimes |
> | Projet M08.P (énoncé + barème + script commité + sorties publiées) | — | 1 script, 6 sections, 4 graphiques, classeur 4 feuilles, barème /20 seuil 13 |
> | Évaluation (quiz 15 Q, 5 exercices rendus, 15 auto-validés) | — | valeurs mesurées sur le socle ; seuil 13/20 |
> | **Total** | **119** | 6 p. de couverture et TOC, 113 p. de contenu (12-17 p./chapitre) |
>
> Chiffres de matière : **76 clés `m08_*`/`m08p_*`** (mesures pandas côté écriture + côté SQL de la
> croisée + environnement), dossier réexporté par `tools/dossier_M08.py` (déterministe, empreinte
> `b9a8d973119342ec…`), 8 planches SVG (une par chapitre, extension max 776 px ≤ 776, 0 glyphe hors
> jeu, total 55,2 Ko). `autovalide M08 --strict` muet (0 avertissement sur les 8 chapitres) ; la
> **croisée SQL/pandas** (intégrée à `chiffres_manuel.py M08`) : 25 valeurs, comptages exacts, totaux
> ± 2 FCFA, dérive `float` mesurée = 1 FCFA sur 5 totaux ; SQLite exécuté en contrôle (centimes
> entiers, concordance exacte) ; `controle_pdf.py M08` : 119 pages, **8/8 figures vérifiées dans le
> PDF**, 0 défaut bloquant, 36/36 glyphes composés. Règle §1.5 : DuckDB et SQLite exécutés,
> PostgreSQL hors module (zéro mention).
>
> **Densité mesurée de M08.** M08 compose 119 pages pour ~ 47 400 mots, soit **≈ 398 mots par
> page** — dans la fourchette de calibre (M05 : 416, M06 : ≈ 435, M07 : ≈ 406, M02 : 489). Le budget
> (117 p. ±15 % = [99, 135]) est tenu à **+1,7 %**. Le fil rouge du module tient : la même base de
> 50 008 ventes, la même vue « sans retours », le même plus gros mois (78 965 529 FCFA, magasin 3,
> 2025-08) requêtée en SQL en M07 et reconstruite en pandas en M08 au FCFA près — et les 3 moteurs
> (DuckDB, SQLite, pandas) d'accord sur les totaux à 1 FCFA près, la dérive mesurée et sourcée.
>
> ## Règles de production (rappel opposable)

1. Toute affirmation sur une version, une licence ou une disponibilité de fonctionnalité porte sa **date de vérification**.
2. Tout SQL est **exécuté** (DuckDB) avant publication ; tout Python est **exécuté** (Python 3.13 / pandas) ; toute formule Excel est **recalculée** dans un classeur généré ; le DAX et les manipulations Power BI, non exécutables ici, sont signalés comme tels avec leurs points de contrôle manuels.
3. **Aucun chiffre du manuel n'est inventé** : il est recopié depuis `data/reference/chiffres_cites.md`, produit par `scripts/chiffres_manuel.py` qui lit les fichiers du socle. Après tout changement de générateur : relancer le script, différer, puis corriger les chapitres — dans cet ordre.
4. Le fichier que l'apprenant doit produire (`…_ATTENDU.csv`) a **exactement** le schéma de l'énoncé : mêmes colonnes, même séparateur, même encodage.
5. Un module n'est déclaré terminé qu'avec `autovalide.py --strict` au vert **et** la porte de contrôle Q1–Q10 de l'architecture §G.1.
6. Un terme non commun est défini à son **premier** emploi, en français — English — sens simple, et ajouté au glossaire (source unique des définitions).

### M09 -- assemblage `05_livrables/M09.pdf`, 82 pages

| Partie | Pages | Observations |
|---|---|---|
| C01 Le protocole en 10 étapes : inspecter sans se fier, la « fiche d'entrée » | 14 | les 10 étapes comme contrat, `shape`/`dtypes`/`head`/`info`, la fiche d'entrée en 30 min |
| C02 L'audit : 3 familles de défauts, statistiques, hypothèses | 13 | doublons / manquants / impossibles, l'audit vide est suspect, l'hypothèse falsifiable |
| C03 Tendances : série, saisonnalité, bruit, périodes comparables | 12 | `resample`, moyenne glissante, le mois partiel qui ment (28 jours), la rupture qui coupe |
| C04 Anomalies et raretés : prouver, décider, écrire au rapport | 11 | les 3 témoins (position, récurrence, métier), les 3 décisions, le plateau 594 363 |
| C05 Relations : corrélation, segments, pièges d'inférence | 13 | 3 fausses causes chiffrées, segments 123 / 208 / 69 → 11.13 / 10.51 / 9.76, le scale 0.552 → 0.001 |
| C06 Visualisations et note d'EDA : les 4 graphiques, la rétro-lecture | 14 | table question → graphique, les 5 erreurs d'exploration, la note d'EDA (source + limite) |
| Couverture + sommaire | 5 | page de titre, table des matières paginée |

> **Ce que la livraison contient.** Quatre jeux de données (`03_exercices/dossier_M09/` : quincaillerie,
> santé, scolaire, projet) et **15 défauts plantés comptables** (23 motifs vides / 7 doublons de stock /
> 1 date future / 4 stocks négatifs — 6 notes hors bornes / 2 doublons d'élèves / 4 absences fériées /
> 3 absents-notés — 14 doublons de transaction / 5 montants négatifs / 2 montants aberrants / 30
> commissions manquantes), tous chiffrés **avec leur définition exacte**. 6 planches SVG (une par chapitre,
> extension max 767 px ≤ 776, 0 glyphe hors jeu, total 46,4 Ko). `autovalide M09 --strict` muet
> (0 avertissement sur les 8 fichiers) ; `controle_pdf.py M09` : 82 pages, **6/6 figures vérifiées dans le
> PDF** par leur libellé, 36/36 glyphes composés ; `controle_exos_M09.py` : **15/15** ; la croisée
> pandas/génération (39 valeurs) est **intégrée** à `chiffres_manuel.py M09` (divergence = `ValueError`).
> Règle §1.5 : DuckDB exécuté (réexport quincaillerie + parallèle SQL/pandas), SQLite exécuté (contrôle de
> la fiche, centimes entiers — concordance exacte), PostgreSQL **zéro mention**.
>
> **Densité mesurée de M09.** M09 compose 78 pages de chapitres pour ~ 34 300 mots, soit **≈ 440 mots par
> page** — la plus dense des modules composés (M05 : 416, M06 : ≈ 435, M07 : 406, M08 : 398) ; le calibre
> est exactement au rendez-vous : **12,5 p./chapitre** pour un calibre de 12,5. Le budget (92,5 p. ±15 % =
> [79, 106]) est tenu à **−11 %**.
>
> **Les deux verrous du module, tenus par les faits.** (1) **Déclarer plutôt que sauter** : les 6 chapitres,
> les 10 étapes, le projet et l'évaluation sont traversés par la même règle — une étape vide se déclare avec
> ses contrôles, une anomalie non prouvée reste un soupçon signalé, une affirmation sans limite est reculée.
> (2) **Le chiffre juste n'est pas la conclusion juste** : 0.552 devient 0.001 quand on passe au taux, un
> écart de panier de 2.4 % sur des groupes de rapport 8 est du bruit de taille, et −0.232 s'effondre par
> bandes (−0.145 / −0.085 / +0.163) — trois pièges, trois contre-exemples chiffrés par le socle.

## Mise en page

Le moteur applique : page de couverture, table des matières paginée (leaders pointillés, `target-counter`),
en-têtes et pieds courants, encadrés éditoriaux colorés, styles de tableaux et de code, veuves et orphelines.
Les polices (Source Serif 4 / Inter / JetBrains Mono) sont matérialisées en **instances statiques à poids fixe** :
les polices variables cassaient la table ToUnicode du PDF (texte non sélectionnable, non cherchable).
Les figures SVG sont citées en relatif (`../figures/MXX_C0y_*.svg`) et converties à la volée.

```markdown
> **Définition.** terme français — Terme anglais — sens simple…      (bandeau bleu)
> **À retenir.** …                                                    (bandeau vert, icône ★)
> **Attention.** …                                                    (bandeau ambre)
> **Conseil professionnel.** …                                         (bandeau gris)
> **Dans les faits.** …                                                (encadré fin, sans fond)
> **Boîte à outils.** …                                                (cadre pointillé, monospace)
```

## Environnement vérifié (17 septembre 2026)

Python 3.13 · pandas 2.2.3 (environnement d'écriture ; le manuel cible pandas 3.x et le signale) · numpy · matplotlib · seaborn · plotly · scikit-learn · openpyxl · python-docx · **DuckDB 1.5.5** · sqlite3 · WeasyPrint 70 · fontTools 4.63 · markdown 3.10 · cairosvg · pypdfium2.
Non disponibles ici : Excel, Power BI, Tableau (d'où la règle 2 ci-dessus).
