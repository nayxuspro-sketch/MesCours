# Journal des pushs — M11 et M12

**Dernier push : `0bc2360` (M12.C03).** Le jeton fourni le 25 septembre 2026 a été validé avant tout
envoi (`GET /api.github.com/user` → **200**, `permissions.push = true`, `info/refs?service=`
`git-receive-pack` → **200**) : la file d'attente constituée pendant le blocage a été vidée **en une
passe**, sans perte.

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

Chaque envoi a suivi la procédure en **ajout seul** (PATCH_11) : test du jeton → `git init` →
`fetch --depth 1` → `update-ref` → `read-tree` → `git add` **des seuls chemins nommés** → push →
bundle de secours dans `/tmp` → `rm -rf .git`. **Jamais** `git add -A` : les 18 PDF de module vivent
hors du dépôt de travail, et un ajout global les aurait marqués « supprimés ».

**Contrôles de dépôt après le dernier push** : **363** fichiers · **85** fichiers dans `02_modules/`
(**75** chapitres) · **0** `.pyc` · **18** PDF · `figures/M11_C01_carte_des_fenetres.svg` et
`M11_C04_matrice_retention.svg` présents · `03_exercices/dossier_M12/` complet (**10** fichiers).

## Ce qui reste à pousser pour M12

| Étape | Livrable | État |
|---|---|---|
| C05 | L'architecture BI de bout en bout (7 étages) | à écrire |
| — | **C04 fait** : poussé n° 52 (6 007 mots, `--strict` OK) | ✅ |
| C06 | Réussir le projet BI : 10 causes d'échec | à écrire |
| Figures | 2 planches (`tools/figures_M12.py`) | à produire |
| PDF | `05_livrables/M12.pdf` — cible [78, 106] p. | à produire |
| Fiche | `05_livrables/fiche_controle_M12.md` (Q1–Q10) | à écrire |
| Projet | `03_exercices/M12_projet.md` — les 10 cartes de KPI, 4 livrables /20 | à écrire |
| Évaluation | `04_evaluations/M12_evaluation.md` — quiz 15 Q + 2 rédactions + étude de cas | à écrire |
| Clôture | `README.md`, `05_livrables/etat_avancement.md` | à mettre à jour |

## Procédure à rejouer (elle a fonctionné 11 fois de suite)

```bash
cd /home/user/formation-data-bi
bash tools/pousser.sh "$JETON" "<message de commit>" <chemin> [<chemin> ...]
```

Le script **teste le jeton avant tout** : si l'API refuse, rien n'est modifié. Le bundle de secours
reste dans `/tmp/mesCours_<commit>.bundle` jusqu'à la fin de la session.
