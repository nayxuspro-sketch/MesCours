# Journal des pushs — M11, M12, M13 et le kit d'exploitation M01-M12

**Dernier push : `4391dd1` (n° 78 — M13.C07, qualité et revue ; M13 complet à 7/7).** Le jeton du 25 septembre
2026 a été re-testé avant **chaque** envoi (`GET /api.github.com/user` → **200**). Le script
`pousser.sh` peut afficher « 401 » sur sa seconde sonde avant un push qui réussit : seuls
`push OK` et `ls-remote` font foi (leçon PATCH_1). M11 et M12 sont **clos** et poussés de bout en
bout (n° 36 → n° 57) ; M13 est **engagé** (plan n° 58, socle n° 59, C01 n° 61, C02 n° 63) ; le
**kit d'exploitation** des douze modules publiés est en ligne (n° 65).

## Ce qui a été poussé

| # | Commit | Contenu | Vérification |
|---|---|---|---|
| 40 | `6d9ab04` | **M11.C02** — rangs, cumuls, décalages (6 213 mots) | `autovalide --strict` |
| 41 | `db17066` | **M11.C04** — cohortes, rétention, récurrence, RFM (5 957 mots) | `autovalide --strict` |
| 42 | `5e966ec` | **M11.C05** — CTE, `PIVOT`, `UNNEST`, `QUALIFY`, `ROLLUP` (5 225 mots) | `autovalide --strict` |
| 43 | `c026341` | **M11.C06** — vues, index, plans, `SELECT *`, partitions (4 938 mots) | `autovalide --strict` |
| 44 | `20b6580` | **M11.C07** — style, tests de non-régression, deux sources (4 883 mots) | `autovalide --strict` |
| 45 | `bb3e63e` | **Clôture M11** — instruments, projet, évaluation, fiche Q1-Q10, PDF 97 p., 2 figures, errata §C.3 | `controle_sql_M11.py` 18/18 · `controle_pdf.py` 0 défaut |
| 46 | `370f9a0` | **Plan M12** — Fondamentaux de la BI (6 ch., 92 p.) | plan poussé avant rédaction |
| 47 | `b7af997` | **Socle et instruments M12** — `dossier_M12` (6 CSV, graine 46), `kpi_M12.py`, relevé `m12_*` | diff = 0 à la seconde exécution |
| 48 | `0403087` | **M12.C01** — définition de la BI, ce qu'elle n'est pas | `autovalide --strict` |
| 49 | `0e12715` | **M12.C02** — reporting, BI, les 4 régimes de question | `autovalide --strict` |
| 50 | `0bc2360` | **M12.C03** — métriques, dimensions, faits, grain | `autovalide --strict` |
| 51 | `460d3c7` | État au 25/09 + journal des pushs | — |
| 52 | `c8f2255` | **M12.C04** — concevoir un KPI : 6 critères, carte de définition, contre-KPI (6 007 mots) + instruments mis à jour | `autovalide --strict`, relevé `m12_*` diff = 0 |
| 53 | `d7bfb82` | `chiffres_cites.md` régénéré (bloc M12 : **239** clés) | — |
| 54 | `77ba622` | Journal des pushs et état au 25/09 | — |
| 55 | `8a194d7` | **M12.C05** — architecture en 7 étages (5 098 mots) + planche | `autovalide --strict`, figure déterministe |
| 56 | `eecb80e` | **M12.C06** — les 10 causes d'échec (4 901 mots) + planche des 10 couples ; C05 aligné sur **255** clés | `autovalide --strict`, figures 2/2 |
| 57 | `0c6c26c` | **Clôture M12** — projet, évaluation, fiche Q1-Q10, `M12.pdf` (**82** p., **585 751** o), **2** planches, README et état réalignés | `controle_pdf.py` : 0 défaut bloquant ; PATCH_6 : **29** livrables nommés vérifiés ; `autovalide` M11 **et** M12 OK |
| 58 | `b035e5f` | **Plan M13** — Modélisation des données (7 ch., 30 h, **105** p., **3** planches, **8** décisions) | plan poussé avant toute rédaction |
| 59 | `2f23ff5` | **Socle M13** — `dossier_M13` (**2** CSV générés ; les **2** dimensions historisées sont construites **en SQL**), `socle_m13.sql` (**12** tables), `modele_M13.py` (**4** contrôles de recette + **5** mesures), relevé `m13_*` (**100** clés), plan corrigé (**5** dimensions + **7** faits) | jointure « au moment du fait » : **240 000** sur **240 000**, **0** doublon ; recette du modèle = recette de la source (**15 595 154 955** FCFA) ; `autovalide` M10, M11, M12 : 0 avertissement |
| 60 | `625221b` | Journal des pushs et état au 25/09 (M12 clos, M13 engagé) | contrôles de dépôt mesurés sur un clone neuf |
| 61 | `fce6e58` | **M13.C01** — Modéliser : entités, attributs, relations, cardinalités (6 624 mots) ; socle corrigé (`table_plate.csv` ne se lisait pas : virgule non protégée) ; instrument : lisibilité des fichiers + point de départ mesuré ; relevé `m13_*` (**145** clés) | `autovalide --strict` 0 avertissement ; les 6 requêtes citées ont été exécutées |
| 62 | `86954dc` | Journal des pushs et état au 25/09 (M13.C01 poussé) | contrôles de dépôt mesurés sur un clone neuf |
| 63 | `f28598d` | **M13.C02** — Normaliser : 1FN, 2FN, 3FN et les quatre anomalies (5 577 mots) ; **2e défaut du socle corrigé** (`dim_produit` rendait **9** familles au lieu de **7** : deux étiquettes à espace finale → `TRIM`) ; instrument : la normalisation est **mesurée** (**16** étiquettes → **7** familles, lecture **4** ms contre **2** ms) ; relevé `m13_*` : **167** clés | `autovalide --strict` 0 avertissement ; les requêtes citées ont été exécutées |
| 64 | `d60d198` | Journal des pushs et état au 25/09 (M13.C02 en ligne, **2/7**) | compteurs mesurés sur un clone neuf |
| 65 | `e6d7ad8` | **Kit d'exploitation M01 à M12** — guide de l'apprenant (**1 886** mots : **6** p. autonome, **4** p. dans le livre), index et glossaire (**488** notions, **367** définitions, **855** entrées), **livre assemblé** `La_Voie_des_Donnees_M01-M12.pdf` (**1 395** p., **124** signets, 14,1 Mo : guide en partie I, les 12 modules, les 2 cahiers, l'index), mesures `kit_M01_M12.json`, `requirements.txt`, générateur `tools/kit_exploitation.py`, README (section kit + arborescence) | 81 chapitres attendus = 81 trouvés ; **366** exercices autonomes, **0** sans reprise au corrigé ; **1 395** = 4 (front) + **4** (guide) + **1 207** (modules) + **65** + **83** (cahiers) + **32** (index), plages vérifiées page par page ; `autovalide M13 --strict` OK |
| 66 | `90fd18a` | Journal des pushs (n° 65) et état au 25/09 : kit en ligne, M13 à **2/7** ; `--mesures-seules` ne perd plus les pages du livre | local = distant, vérifié par `ls-remote` |
| 67 | `88ea9d5` | **Correctif du livre assemblé** : le guide (partie I) n'était pas compté dans les plages du sommaire — **décalage de 4 pages** sur les douze modules ; **guide livré en PDF autonome** (`guide_apprenant_M01_M12.pdf`, 6 p.) ; pagination alignée (journal, état, README) | M01 **9—125** · guide **5—8** · M12 **1134—1215** · index **1364—1395**, vérifiés sur le PDF composé |
| 68 | `2901a38` | Journal des pushs (n° 66 et 67) et état au 25/09 | — |
| 69 | `1158f0d` | **M13.C03** — Grain, additivité et tables de faits (**7 089** mots, 16 §) : les **3** faux totaux mesurés (clé trop large **44,0** ; clé trop fine **0,36** ; grains mélangés **+ 43,0 %**), le piège de la mauvaise clé de contrôle (**60** valeurs pour **218** lignes), le **filtre silencieux par jointure d'agrégats** (**28 893 543** FCFA du dépôt central, trouvé en écrivant l'exercice guidé) ; planche `M13_C03_grain_et_explosion.svg` et instrument `tools/figures_M13.py` ; **37** clés `m13_c03_*` au relevé | `autovalide --strict` 0 avertissement ; les 9 requêtes citées ont été exécutées une par une ; planche **623** px, texte extractible du PDF |
| 70 | `1cc33ff` | Journal des pushs (n° 68 et 69) et état au 25/09 : M13 à **3/7** | — |
| 71 | `b942f05` | **Correction des compteurs du dépôt** dans le journal : la ligne du n° 69 annonçait **401** fichiers et **20** PDF, écrits de mémoire ; la mesure par `ls-tree` donne **397** fichiers et **21** PDF | compteurs relevés sur le dépôt : **397** fichiers · **91** dans `02_modules/` (dont **86** `.md`, soit **84** chapitres) · **70** planches · **49** instruments · **21** PDF · **41** pièces dans `05_livrables/` · **0** `.pyc` |
| 72 | `3da3c55` | **M13.C04** — Le schéma en étoile et les changements lents (**6 636** mots, 16 §) : les dimensions conformes **mesurées** (`dim_magasin` sert **5** faits, `dim_date` **0** — trou déclaré, C06 le fermera), les **4** types de SCD (**980** versions / **140** corrections / **24 892** versions de clients / **4** clients à **3** villes), la jointure « au moment du fait » et ses **deux trous** (**43 161** + **28 784** = **71 945** lignes de ticket), l'écart de répartition de **102 917 580** FCFA, le tarif historisé (**9,1 %** d'écart de prix moyen) ; planche `M13_C04_frise_scd.svg` (**662** px) ; **25** clés `m13_c04_*` au relevé | `autovalide --strict` 0 avertissement ; les **6** blocs SQL du chapitre exécutés sur le socle ; planche en latin-1 strict, texte extractible du PDF |
| 73 | `fabb777` | Journal des pushs (n° 70 à 72) et état au 25/09 : M13.C04 en ligne, **4/7** | compteurs mesurés sur le dépôt : **399** fichiers · **71** planches · **21** PDF |
| 74 | `fd04f86` | **M13.C05** — Le schéma en flocon et ses variantes (**6 264** mots, 16 §) : étoile contre flocon **mesurés** (**154** → **173** lignes, **1** → **3** jointures, **3** → **4** ms, résultat **identique**), le N-M du ticket (**240 000** lignes / **146 161** tickets / **1,64** par ticket) et son **facteur de répétition de 2,01** (**31 298 080 184** FCFA au lieu de **15 595 154 955**), la **dimension déchet** de **30** combinaisons toutes occupées, les **faits multiples** et les **2 809** retours à montants négatifs (**175 169 798** FCFA) ; **35** clés `m13_c05_*` au relevé | `autovalide --strict` 0 avertissement ; les **8** requêtes citées exécutées, dont la lecture par la dimension déchet (Magasin **10 295 255 849** FCFA) qui somme exactement au total du modèle |
| 75 | `d4d97d6` | Journal des pushs (n° 65 à 74, remis dans l'ordre) et état au 25/09 : M13.C05 en ligne, **5/7** | compteurs mesurés sur le dépôt |
| 76 | `519a053` | **Correctif** : **4** compteurs du journal écrits de mémoire remplacés par la mesure (**93** fichiers dans `02_modules/`, **88** `.md`, **86** chapitres, **71** planches), et la leçon du n° 75 consignée | comptage sur les **bases de noms uniques** : les chapitres de M05 comptent double en `.md` et `.pdf` sinon |
| 77 | `7f320f4` | **M13.C06** — Le temps et le calendrier (**7 154** mots, 16 §) : le trou déclaré en C04 fermé (**1 339** lignes de calendrier, **240 000** lignes sur **240 000**), les **2** contrôles de complétude (**0** jour sans vente, **0** date de vente hors calendrier, mais **13** dates de livraison pour **46** commandes et **32 772 075** FCFA), les attributs lus dans la dimension (**18** fériés, dimanche **5,32 %**, 4ᵉ trimestre **29,7 %**), les deux calendriers (semaine normalisée **52** contre commerciale **53**), l'exercice fiscal décalé (**725** jours), la comparaison bornée (**− 28,9 %** contre **+ 15,4 %**, soit **44,3** points) et le cumul glissant (**+ 16,2 %**) | **94** clés `m13_c06_*` au relevé |
| 78 | `4391dd1` | **M13.C07** — Qualité, documentation et revue en **15** points (**6 080** mots, 16 §) : les **4** contrôles de recette (**14** tables sur **14**, **7** faits sur **7**, **12** clés étrangères et **0** orphelin, **15 595 154 955** FCFA des deux côtés), ce que le script déclare (**315** lignes dont **99** de commentaire, **0** clé et **0** commentaire de colonne) et ce qui reste à documenter (**127** colonnes), la grille de revue dont **5** points échouent sur le modèle fautif (**2 826 394** caractères recopiés au lieu de **239 599**, deux temps, un objectif posé sur la vente à **+ 42,9 %**, **0** clé, **16** libellés pour **7** familles), et les **3** modèles fautifs qui s'exécutent sans erreur (**+ 43,0 %**, **+ 89,0 %**, **44** fois) | **3ᵉ planche** `M13_C07_grille_revue.svg` (**609** px) ; les durées de lecture des chapitres C02, C04 et C05 réalignées sur la dernière mesure |
| 79 | `91a7d24` | Journal des pushs (n° 74 à 78 remis dans l'ordre) et état au 25/09 : M13 à **7/7** | compteurs mesurés sur le dépôt : **403** fichiers · **95** dans `02_modules/` · **72** planches |
| 80 | `2871fd7` | **Clôture M13** — projet « Le modèle de Sahel Distribution » (**20** pts, seuil **13**, **8** totaux de contrôle), évaluation (**75** pts, seuil **48** : quiz **20**, normalisation **20**, étude de cas **30**, auto-test **5**), `05_livrables/M13.pdf` (**107** p., **774** Ko, **3/3** planches, **27/27** glyphes), `05_livrables/fiche_controle_M13.md` (**10/10** au vert, **5** nuances), et **2** correctifs : signe moins perdu **9** fois dans le chapitre C06 (`**, 28,9 %**` → `**− 28,9 %**`), déclaration d'exécution §1.5 ajoutée en tête des **5** chapitres qui ne l'avaient pas | `autovalide M13 --strict` **0** avertissement sur **9** fichiers · `controle_pdf.py M13` **0** défaut bloquant · PDF **107** p. pour **105** (fourchette [89, 121]) · socle reconstruit à l'empreinte près (`739e4ba68297bff8`) |

Chaque envoi a suivi la procédure en **ajout seul** (PATCH_11) : test du jeton → `git init` →
`fetch --depth 1` → `update-ref` → `read-tree` → `git add` **des seuls chemins nommés** → push →
bundle de secours dans `/tmp` → `rm -rf .git`. **Jamais** `git add -A` : les PDF de module vivent
hors de l'atelier, et un ajout global les aurait marqués « supprimés » dès que la place manque.

**Contrôles de dépôt après le n° 80 (mesurés sur un clone neuf, `ls-tree -z`)** :
**407** fichiers · **95** dans `02_modules/` (dont **90** `.md` : **88** chapitres rédigés, l'ouverture
`M01_C00` et le bilan de M01, plus **5** PDF de chapitres M05) · **72** planches dans `figures/` ·
**49** instruments dans `tools/` · **0** `.pyc` · **22** PDF · **43** pièces dans `05_livrables/` ·
`03_exercices/dossier_M13/` complet (**8** fichiers) · la branche `main` pointe sur `2871fd7`.

**M13 est complet : 7 chapitres sur 7.** Le module passe de **86** à **88** chapitres rédigés (81
publiés pour M01-M12, **7** pour M13), soit **62 %** des **143** chapitres du manuel.

**Leçon du n° 75.** La première rédaction de ces lignes portait **92** fichiers dans `02_modules/`,
**87** `.md`, **85** chapitres et **70** planches : quatre nombres écrits **de mémoire**, donc faux,
et repérés en confrontant la copie locale à `ls-tree -z`. C'est la troisième fois que ce type d'erreur
apparaît (n° 71, n° 75, et la ligne du n° 69) : un compteur ne se rédige **jamais** avant d'avoir été
mesuré par la commande qui le concerne. Le compte des chapitres se fait sur les **bases de noms
uniques**, sans quoi les chapitres de M05 comptent double (`.md` et `.pdf`).

## Kit d'exploitation M01 à M12 (n° 65)

Les douze modules publiés (12 modules, 81 chapitres, 1 207 pages de cours, 366 exercices) étaient
diffusables mais pas utilisables seuls. Le kit les rend utilisables, et il est **généré** :

- `05_livrables/guide_apprenant_M01_M12.md` — le mode d'emploi de l'apprenant (**1 886** mots) ;
- `05_livrables/index_glossaire_M01_M12.md` — index des notions (**488**), glossaire (**367**),
  planches (**69**), instruments (**48**), jeux de données (**10**) ;
- `05_livrables/kit_M01_M12.json` — les mesures, **seule source** des chiffres du guide ;
- `05_livrables/La_Voie_des_Donnees_M01-M12.pdf` — **1 395** pages, **124** signets ;
- `requirements.txt` et `tools/kit_exploitation.py` (mesure, index, livre ; `--mesures-seules` en
  2 s, `--telecharger-modules` pour reconstruire depuis le dépôt seul).

Trois corrections que la mesure a imposées, et qui changent des chiffres déjà publiés :

1. **366** exercices autonomes, pas **243** : quatre mises en forme cohabitent dans le manuel
   (`**Exercice n.n.**`, `**Exercice n …**`, `### Exercice n —`, `**En —**`, liste numérotée).
   L'ancien total venait d'un artefact de comptage. Contrôle : **0** exercice sans reprise.
2. **509 252** mots de cours dans les 81 chapitres (**510 627** avec l'ouverture `M01_C00`, que
   l'ancien total comptait comme un chapitre).
3. Les **barèmes d'évaluation ne sont pas uniformes** (M01 : quiz 14/20 et étude de cas 12/20 ;
   M07 : quiz 13/20, exercices 28/35 ; M12 : 70 points, seuil 45). Le guide donne le barème réel
   des douze modules, au lieu d'un format supposé.

## M13 — état de livraison (clos au n° 80)

| Étape | Livrable | État |
|---|---|---|
| Plan | `05_livrables/plan_M13.md` — 7 ch., 30 h, 105 p., 3 planches, 8 décisions | ✅ n° 58 |
| Socle | `03_exercices/dossier_M13/` — 12 tables, 2 dimensions historisées en SQL, instrument `modele_M13.py` | ✅ n° 59 |
| C01 | Modéliser : MCD, MLD, MPD (6 644 mots) | ✅ n° 61 |
| C02 | Normaliser : 1FN → 3FN, les 4 anomalies (5 577 mots) | ✅ n° 63 |
| C03 | Grain, additivité, table de faits (7 089 mots) + planche | ✅ n° 69 |
| C04 | Étoile, dimensions conformes, SCD 0/1/2/3 (6 656 mots) + planche | ✅ n° 72 |
| C05 | Flocon, pont, déchet, faits multiples (6 291 mots) | ✅ n° 74 |
| C06 | Le temps et le calendrier (7 154 mots) | ✅ n° 77 |
| C07 | Qualité, documentation, revue en 15 points (6 080 mots) + planche | ✅ n° 78 |
| Défaut révélé par C03 | le filtre silencieux par jointure d'agrégats (dépôt central, **28 893 543** FCFA) — corrigé dans le chapitre et l'instrument | ✅ n° 69 |
| Trou ouvert par C04 | `dim_date` existait sans qu'aucun fait ne pointe dessus — déclaré et mesuré, fermé en C06 | ✅ n° 77 |
| Figures | **3** planches : C03 **623** px, C04 **668** px, C07 **609** px (limite 776) | ✅ 3/3 |
| PDF | `05_livrables/M13.pdf` — **107** p., cible [89, 121] (**+ 1,9 %**), 9 fichiers joints, 20 signets | ✅ n° 80 |
| Fiche | `05_livrables/fiche_controle_M13.md` — Q1-Q10 **10/10**, 5 nuances déclarées | ✅ n° 80 |
| Projet | `03_exercices/M13_projet.md` — 4 livrables (**6 + 6 + 5 + 3 = 20** points, seuil **13**) | ✅ n° 80 |
| Évaluation | `04_evaluations/M13_evaluation.md` — **75** points, seuil **48** | ✅ n° 80 |
| Veille de clôture | signe moins perdu **9** fois dans C06 restauré ; déclaration d'exécution §1.5 ajoutée en tête de C03 → C07 | ✅ n° 80 |

**Rien ne reste à pousser pour M13.** Le module suivant est **M14 — Power BI** (*Restituer et
modéliser*, phase 4), dont le dossier sera documenté pas à pas et **déclaré non exécuté** (règle §1.5,
aucun Power BI dans cet atelier).

## M14 — état de livraison (clos au n° 90)

| Étape | Ce qui est livré | Statut |
|---|---|---|
| Plan | `05_livrables/plan_M14.md` — 8 ch. · 30 h · N4 · 117 p. [99, 135] · 2 projets · éval 80/51 · 4 planches | ✅ n° 82 |
| Socle et dossier | `03_exercices/dossier_M14/` — **7** pièces : `modele_powerbi.md` (12 relations, 2 inactives, 15 gestes, **11** mesures, 3 pages, 14 visuels, 4 signets, RLS), `retours_comite.md` (11), `rapport_avant.md`, `grille_conception_M14.md` (18 pts + 6 ajouts), `connexion.py`, `modele_import/LISEZ_MOI.md`, `ATTENDU.json` | ✅ n° 83 |
| Chapitre C01 | écosystème, 4 surfaces, 4 formules de licence chiffrées | ✅ n° 84 |
| Chapitre C02 | connecteurs, 4 modes, cache, passerelle | ✅ n° 85 |
| Chapitre C03 | Power Query : **15** gestes, 240 000 → 33 323 lignes | ✅ n° 86 |
| Chapitre C04 | **12** relations, **2** inactives, la recette 10/8/0, et le complément §5.9 (intégrité, colonnes masquées, tri) | ✅ n° 87 |
| Chapitre C05 | mesures contre colonnes, **11** mesures, **8** fonctions DAX | ✅ n° 88 |
| Chapitre C06 | **3** pages, **14** visuels, tri, échelles, jauge à **259,1 %**, **6** erreurs de visuel | ✅ n° 89 |
| Chapitre C07 | filtres, dénominateur, périmètre, exploration, performance | ✅ n° 90 |
| Chapitre C08 | publication, **6** rôles testés, actualisation, alertes, **7** tests, grille en **18** points | ✅ n° 90 |
| Instrument | `tools/mesures_M14.py` — **12** sections, **277** clés `m14_*`, **3 003** clés au total ; contrôle croisé M12 : **8** appariements, **0** écart | ✅ n° 90 |
| Figures | **4** planches : C01 **609** px · C02 **609** px · C04 **638** px · C08 **681** px (limite 776), empreinte `3841e32e46d8d13c` | ✅ 4/4 |
| PDF | `05_livrables/M14.pdf` — **116** p., cible [99, 135] (**− 0,9 %**), 10 fichiers joints, 22 signets | ✅ |
| Fiche | `05_livrables/fiche_controle_M14.md` — Q1-Q10 **10/10**, 5 nuances déclarées | ✅ |
| Projets | `03_exercices/M14_projet.md` — **2** projets, **20** points chacun (seuil **13**) : P1 le tableau de bord, P2 la version 2 après les **11** retours | ✅ |
| Évaluation | `04_evaluations/M14_evaluation.md` — **80** points, seuil **51** (quiz 15 Q/20 · **4** exercices/24 dont E4 le total doublé · étude de cas 30/18 · auto-évaluation 6) | ✅ |
| Veille de clôture | compte des mesures tranché à **11** contre les **10** du plan ; piège `annee_mois` rechiffré (**30,44**) ; section `visuels` puis `filtres`, `publication`, `évaluation` ajoutées à l'instrument | ✅ |

**Rien ne reste à pousser pour M14.** Le module suivant est **M15 — DAX avancé** (calculs de temps,
`ALL`, itérateurs), dont la frontière est écrite au chapitre C05 : ce que M14 n'enseigne pas
volontairement.

## Procédure à rejouer (elle a servi les pushs n° 40 à n° 90) (elle a fonctionné **37** fois de suite, n° 40 → n° 80)

```bash
cd /home/user/formation-data-bi
bash tools/pousser.sh "$JETON" "<message de commit>" <chemin> [<chemin> ...]
```

Le script **teste le jeton avant tout** : si l'API refuse, rien n'est modifié. Le bundle de secours
reste dans `/tmp/mesCours_<commit>.bundle` jusqu'à la fin de la session.
