# Journal des pushs — M11, M12 et M13

**Dernier push : `fce6e58` (n° 61 — M13.C01).** Le jeton du 25 septembre 2026 a été re-testé avant
**chaque** envoi (`GET /api.github.com/user` → **200**). Le script `pousser.sh` peut afficher « 401 »
sur sa seconde sonde avant un push qui réussit : seuls `push OK` et `ls-remote` font foi (leçon
PATCH_1). M12 est **clos** et poussé de bout en bout (n° 46 → n° 57) ; M13 est **engagé** (plan n° 58,
socle et instrument n° 59).

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
| 60 | `625221b` | Journal des pushs et état au 25/09 (M12 clos, M13 engagé) | contrôles de dépôt mesurés sur un clone neuf |
| 61 | `fce6e58` | **M13.C01** — Modéliser : entités, attributs, relations, cardinalités (6 624 mots) ; socle corrigé (`table_plate.csv` ne se lisait pas : virgule non protégée) ; instrument : lisibilité des fichiers + point de départ mesuré ; relevé `m13_*` (**145** clés) | `autovalide --strict` 0 avertissement ; les 6 requêtes citées ont été exécutées |
| 59 | `2f23ff5` | **Socle M13** — `dossier_M13` (**2** CSV générés ; les **2** dimensions historisées sont construites **en SQL**), `socle_m13.sql` (**12** tables), `modele_M13.py` (**4** contrôles de recette + **5** mesures), relevé `m13_*` (**100** clés), plan corrigé (**5** dimensions + **7** faits) | jointure « au moment du fait » : **240 000** sur **240 000**, **0** doublon ; recette du modèle = recette de la source (**15 595 154 955** FCFA) ; `autovalide` M10, M11, M12 : 0 avertissement |

Chaque envoi a suivi la procédure en **ajout seul** (PATCH_11) : test du jeton → `git init` →
`fetch --depth 1` → `update-ref` → `read-tree` → `git add` **des seuls chemins nommés** → push →
bundle de secours dans `/tmp` → `rm -rf .git`. **Jamais** `git add -A` : les 18 PDF de module vivent
hors du dépôt de travail, et un ajout global les aurait marqués « supprimés ».

**Contrôles de dépôt après le dernier push (n° 61, mesurés sur un clone neuf)** : **386** fichiers ·
**86** fichiers dans `02_modules/` (dont **80** chapitres `.md`) · **68** planches dans `figures/` ·
**0** `.pyc` · **19** PDF · `03_exercices/dossier_M13/` complet (**8** fichiers) · **12** fichiers
`M13` au total · la branche `main` pointe sur `fce6e58`.

## Ce qui reste à pousser pour M13

| Étape | Livrable | État |
|---|---|---|
| Plan | `05_livrables/plan_M13.md` — 7 ch., 30 h, 105 p., 3 planches, 8 décisions | ✅ n° 58 |
| Socle | `03_exercices/dossier_M13/` — 12 tables, 2 dimensions historisées en SQL, instrument `modele_M13.py` | ✅ n° 59 |
| C01 | Modéliser : MCD, MLD, MPD (6 624 mots) | ✅ n° 61 |
| C02 | Normaliser : 1FN → 3FN, les 4 anomalies (16 §) | à écrire |
| C03 | Grain, additivité, table de faits (16 §) + planche | à écrire |
| C04 | Étoile, dimensions conformes, SCD 0/1/2/3 (16 §) + planche | à écrire |
| C05 | Flocon, pont, déchet, faits multiples (15 §) | à écrire |
| C06 | Le temps et le calendrier (15 §) | à écrire |
| C07 | Qualité, documentation, revue en 15 points (16 §) + planche | à écrire |
| Figures | **3** planches (`tools/figures_M13.py`), ≤ 776 px | à produire |
| PDF | `05_livrables/M13.pdf` — cible **[89, 121]** p. | à produire |
| Fiche | `05_livrables/fiche_controle_M13.md` (Q1-Q10) | à écrire |
| Projet | `03_exercices/M13_projet.md` — 4 livrables (**6 + 6 + 5 + 3 = 20** points, seuil **13**) | à écrire |
| Évaluation | `04_evaluations/M13_evaluation.md` — **75** points, seuil **48** | à écrire |
| Clôture | `README.md`, `05_livrables/etat_avancement.md` | à mettre à jour |

## Procédure à rejouer (elle a fonctionné **20** fois de suite, n° 40 → n° 59)

```bash
cd /home/user/formation-data-bi
bash tools/pousser.sh "$JETON" "<message de commit>" <chemin> [<chemin> ...]
```

Le script **teste le jeton avant tout** : si l'API refuse, rien n'est modifié. Le bundle de secours
reste dans `/tmp/mesCours_<commit>.bundle` jusqu'à la fin de la session.
