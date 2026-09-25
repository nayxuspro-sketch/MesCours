# Journal des pushs — M11, M12, M13 et le kit d'exploitation M01-M12

**Dernier push : `3da3c55` (n° 72 — M13.C04, étoile et changements lents).** Le jeton du 25 septembre
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
| 67 | `88ea9d5` | **Correctif du livre assemblé** : le guide (partie I) n'était pas compté dans les plages du sommaire — **décalage de 4 pages** sur les douze modules ; **guide livré en PDF autonome** (`guide_apprenant_M01_M12.pdf`, 6 p.) ; pagination alignée (journal, état, README) | M01 **9–125** · guide **5–8** · M12 **1134–1215** · index **1364–1395**, vérifiés sur le PDF composé |
| 68 | `2901a38` | Journal des pushs (n° 66 et 67) et état au 25/09 | — |
| 70 | `1cc33ff` | Journal des pushs (n° 68 et 69) et état au 25/09 : M13 à **3/7** | — |
| 72 | `3da3c55` | **M13.C04** — Le schéma en étoile et les changements lents (**6 636** mots, 16 §) : les dimensions conformes **mesurées** (`dim_magasin` sert **5** faits, `dim_date` **0** — trou déclaré, C06 le fermera), les **4** types de SCD (**980** versions / **140** corrections / **24 892** versions de clients / **4** clients à **3** villes), la jointure « au moment du fait » et ses **deux trous** (**43 161** + **28 784** = **71 945** lignes de ticket), l'écart de répartition de **102 917 580** FCFA, le tarif historisé (**9,1 %** d'écart de prix moyen) ; planche `M13_C04_frise_scd.svg` (**662** px) ; **25** clés `m13_c04_*` au relevé | `autovalide --strict` 0 avertissement ; les **6** blocs SQL du chapitre exécutés sur le socle ; planche en latin-1 strict, texte extractible du PDF |
| 71 | `b942f05` | **Correction des compteurs du dépôt** dans le journal : la ligne du n° 69 annonçait **401** fichiers et **20** PDF, écrits de mémoire ; la mesure par `ls-tree` donne **397** fichiers et **21** PDF | compteurs relevés sur le dépôt : **397** fichiers · **91** dans `02_modules/` (dont **86** `.md`, soit **84** chapitres) · **70** planches · **49** instruments · **21** PDF · **41** pièces dans `05_livrables/` · **0** `.pyc` |
| 69 | `1158f0d` | **M13.C03** — Grain, additivité et tables de faits (**7 089** mots, 16 §) : les **3** faux totaux mesurés (clé trop large **44,0** ; clé trop fine **0,36** ; grains mélangés **+ 43,0 %**), le piège de la mauvaise clé de contrôle (**60** valeurs pour **218** lignes), le **filtre silencieux par jointure d'agrégats** (**28 893 543** FCFA du dépôt central, trouvé en écrivant l'exercice guidé) ; planche `M13_C03_grain_et_explosion.svg` et instrument `tools/figures_M13.py` ; **37** clés `m13_c03_*` au relevé | `autovalide --strict` 0 avertissement ; les 9 requêtes citées ont été exécutées une par une ; planche **623** px, texte extractible du PDF |

Chaque envoi a suivi la procédure en **ajout seul** (PATCH_11) : test du jeton → `git init` →
`fetch --depth 1` → `update-ref` → `read-tree` → `git add` **des seuls chemins nommés** → push →
bundle de secours dans `/tmp` → `rm -rf .git`. **Jamais** `git add -A` : les PDF de module vivent
hors de l'atelier, et un ajout global les aurait marqués « supprimés » dès que la place manque.

**Contrôles de dépôt après le n° 72 (mesurés sur le dépôt lui-même, chemins sans échappement)** :
**397** fichiers · **91** dans `02_modules/` (dont **86** `.md` : **84** chapitres, l'ouverture
`M01_C00` et le bilan de M01, plus **5** PDF de chapitres M05) · **70** planches dans `figures/` ·
**49** instruments dans `tools/` · **0** `.pyc` · **21** PDF · **41** pièces dans `05_livrables/` ·
`03_exercices/dossier_M13/` complet (**8** fichiers) · la branche `main` pointe sur `3da3c55`.
Écart atelier / dépôt : **381** fichiers locaux, **0** absent du dépôt (les 16 de plus au dépôt sont
les PDF que l'atelier ne garde pas, plus les fichiers du kit).

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

## Ce qui reste à pousser pour M13

| Étape | Livrable | État |
|---|---|---|
| Plan | `05_livrables/plan_M13.md` — 7 ch., 30 h, 105 p., 3 planches, 8 décisions | ✅ n° 58 |
| Socle | `03_exercices/dossier_M13/` — 12 tables, 2 dimensions historisées en SQL, instrument `modele_M13.py` | ✅ n° 59 |
| C01 | Modéliser : MCD, MLD, MPD (6 624 mots) | ✅ n° 61 |
| C02 | Normaliser : 1FN → 3FN, les 4 anomalies (5 577 mots) | ✅ n° 63 |
| C03 | Grain, additivité, table de faits (16 §) + planche | ✅ n° 69 |
| C04 | Étoile, dimensions conformes, SCD 0/1/2/3 (16 §) + planche | ✅ n° 72 |
| — | **Le chapitre C03 a révélé un défaut de plus du socle** : le filtre silencieux par jointure d'agrégats (dépôt central, **28 893 543** FCFA) — corrigé dans le chapitre et l'instrument | ✅ n° 69 |
| C05 | Flocon, pont, déchet, faits multiples (15 §) | à écrire |
| — | **Le chapitre C04 a rouvert un trou du modèle, déclaré et mesuré** : `dim_date` existe mais **aucun fait** ne pointe dessus par clé — à fermer en C06 | ⏳ C06 |
| C06 | Le temps et le calendrier (15 §) | à écrire |
| C07 | Qualité, documentation, revue en 15 points (16 §) + planche | à écrire |
| Figures | **2** planches livrées sur **3** (`M13_C03`, `M13_C04`) ; reste celle de C07 | 2/3 |
| PDF | `05_livrables/M13.pdf` — cible **[89, 121]** p. | à produire |
| Fiche | `05_livrables/fiche_controle_M13.md` (Q1-Q10) | à écrire |
| Projet | `03_exercices/M13_projet.md` — 4 livrables (**6 + 6 + 5 + 3 = 20** points, seuil **13**) | à écrire |
| Évaluation | `04_evaluations/M13_evaluation.md` — **75** points, seuil **48** | à écrire |
| Clôture | `README.md`, `05_livrables/etat_avancement.md` | à mettre à jour |

## Procédure à rejouer (elle a fonctionné **33** fois de suite, n° 40 → n° 72)

```bash
cd /home/user/formation-data-bi
bash tools/pousser.sh "$JETON" "<message de commit>" <chemin> [<chemin> ...]
```

Le script **teste le jeton avant tout** : si l'API refuse, rien n'est modifié. Le bundle de secours
reste dans `/tmp/mesCours_<commit>.bundle` jusqu'à la fin de la session.
