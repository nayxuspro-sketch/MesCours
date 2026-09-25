# Reprise de publication — M11 (à jouer dès qu'un jeton valide est fourni)

**Situation au 24 septembre 2026, 23 h 30.** Le module M11 est **terminé et validé** : `autovalide
M11 --strict` sur **9** fichiers → `0 avertissement` ; `chiffres_manuel.py M11` → **301** clés,
`diff` = 0 entre deux exécutions ; PDF **97** p. composées (`controle_pdf` : `2/2` figures,
`28/28` glyphes, **0** défaut bloquant) ; `controle_sql_M11.py` → **18/18 OK**.

Le jeton GitHub refusé par l'API le 24/09/2026 (`401 Bad credentials`) bloque **5 pushs**. Le dépôt
distant est **public** : lecture anonyme possible, écriture non.

> **Règle de reprise (PATCH_11).** Jamais `git add -A` : les **11** PDF de module vivent dans `/tmp`
> et apparaissent en « D » — un `-A` les effacerait du dépôt. `tools/pousser.sh` refait un
> `fetch --depth 1` → `update-ref` → `read-tree`, n'indexe **que les chemins nommés**, pousse, produit
> le bundle de secours dans `/tmp`, puis supprime `.git`. **Le jeton est testé avant tout** : s'il est
> refusé, rien n'est modifié.

## Les 5 commandes

```bash
cd /home/user/formation-data-bi

# 1 · C02 — le chapitre rattrapé (rang, cumuls, décalages) : 6 213 mots
bash tools/pousser.sh "$JETON" "M11.C02 rang, cumuls, decalages (6 213 mots, 22 cles mesurees)" \
  02_modules/M11_C02_rang_cumuls_decallages_row_number_rank_ntile_lag_lead.md

# 2 · C04 — cohortes, rétention, récurrence, RFM : 5 957 mots
bash tools/pousser.sh "$JETON" "M11.C04 cohortes, retention, recurrence, RFM (5 957 mots)" \
  02_modules/M11_C04_cohortes_retention_recurrence_rfm.md

# 3 · C05 — CTE, PIVOT, UNNEST, QUALIFY, ROLLUP : 5 225 mots
bash tools/pousser.sh "$JETON" "M11.C05 requetes avancees CTE, PIVOT, UNNEST, QUALIFY, ROLLUP" \
  02_modules/M11_C05_requetes_avancees_cte_pivot_unnest_qualify_rollup.md

# 4 · C06 — vues, index, plans, SELECT *, partitions : 4 938 mots
bash tools/pousser.sh "$JETON" "M11.C06 rapport lent : vues, index, plans, SELECT *, partitions" \
  02_modules/M11_C06_rapport_lent_vues_index_plans_select_etoile_partitions.md

# 5 · C07 — style, tests de non-régression, contrôle entre deux sources : 4 883 mots
bash tools/pousser.sh "$JETON" "M11.C07 style, tests de non-regression, controle entre deux sources" \
  02_modules/M11_C07_style_tests_non_regression_controle_entre_deux_sources.md
```

## Puis la clôture (un seul push)

```bash
bash tools/pousser.sh "$JETON" "M11 cloture : instruments, projet, evaluation, fiche, PDF, errata" \
  tools/controle_sql_M11.py tools/perf_M11.py tools/figures_M11.py tools/pousser.sh \
  tools/dossier_M11.py \
  figures/M11_C01_carte_des_fenetres.svg figures/M11_C04_matrice_retention.svg \
  03_exercices/dossier_M11/socle_m11.sql 03_exercices/dossier_M11/connexion.py \
  03_exercices/dossier_M11/PERF_M11.json \
  03_exercices/M11_projet.md 04_evaluations/M11_evaluation.md \
  01_socle_donnees/scripts/chiffres_manuel.py \
  01_socle_donnees/data/reference/chiffres_cites.json \
  05_livrables/M11.pdf 05_livrables/fiche_controle_M11.md 05_livrables/plan_M11.md \
  05_livrables/etat_avancement.md 05_livrables/README.md README.md \
  00_architecture/01_architecture_pedagogique.md
```

*(`03_exercices/dossier_M11/__pycache__/` n'est jamais nommé : le dossier est couvert par
`.gitignore` (`__pycache__/`, `*.pyc`) — leçon PATCH_5.)*

## Ce que ces pushs apportent, en une ligne chacun

| Push | Contenu | Contrôle qui l'autorise |
|---|---|---|
| C02 | **22** clés `m11_c02_*` — `RANK` **23 444** vs `DENSE_RANK` **21**, top 3 sur **7** familles = **21** lignes | `autovalide --strict` + 3 clés partagées repatchées |
| C04 | **24** clés — rétention pondérée **15,8 %** à M+1, RFM **2 151** clients / **31,7 %**, client **0** **18,3 %** | `autovalide --strict` |
| C05 | **18** clés — `QUALIFY` **7** lignes contre **16**, `ROLLUP` **41** lignes, total **15 595 154 955** | `autovalide --strict` |
| C06 | **10** clés — plancher DuckDB **536 576** o, `SCAN` → `SEARCH` en SQLite, vue **142** ms vs table **1** ms | `perf_M11.py --figer` (médianes de 5) |
| C07 | **3** clés — **18/18** contrôles, **23 444** contre **23 497** (test réécrit) | `controle_sql_M11.py` |
| clôture | projet (**12** rapports, 4 livrables **8 + 5 + 4 + 3 = 20**, seuil 13), évaluation (**70** pts), fiche Q1-Q10, PDF **97** p., errata §C.3 | `controle_pdf.py` **0** défaut |

## M12 — ce qui s'ajoute à la file d'attente (en cours de rédaction)

Le module M12 a démarré pendant que les pushs M11 attendent : **plan**, **socle et instruments**,
**chapitre C01** sont écrits et validés `--strict`. Ils s'ajouteront à la file, dans l'ordre de la
cadence (un push par chapitre).

```bash
# plan M12 + socle et instruments + C01 (à répartir comme pour M11)
bash tools/pousser.sh "$JETON" "M12 plan : Fondamentaux de la BI (6 ch., 92 p.)" \
  05_livrables/plan_M12.md
bash tools/pousser.sh "$JETON" "M12 socle et instruments : dossier deterministe, 10 KPI mesures" \
  tools/dossier_M12.py tools/kpi_M12.py \
  03_exercices/dossier_M12/socle_m12.sql 03_exercices/dossier_M12/connexion.py \
  03_exercices/dossier_M12/ATTENDU.json 03_exercices/dossier_M12/etude_avant.md \
  03_exercices/dossier_M12/cout_produits.csv 03_exercices/dossier_M12/stock_mensuel.csv \
  03_exercices/dossier_M12/ruptures.csv 03_exercices/dossier_M12/commandes_clients.csv \
  03_exercices/dossier_M12/encaissements.csv 03_exercices/dossier_M12/logistique_mensuelle.csv \
  01_socle_donnees/scripts/chiffres_manuel.py \
  01_socle_donnees/data/reference/chiffres_cites.json
bash tools/pousser.sh "$JETON" "M12.C01 definition de la BI, ce qu'elle n'est pas" \
  02_modules/M12_C01_definition_de_la_bi_ce_qu_elle_n_est_pas_cout_decision_sans_donnee.md
bash tools/pousser.sh "$JETON" "M12.C02 reporting, BI et les quatre regimes de question" \
  02_modules/M12_C02_reporting_bi_quatre_regimes_de_question.md
bash tools/pousser.sh "$JETON" "M12.C03 metriques, dimensions, faits, grain : le vocabulaire exact" \
  02_modules/M12_C03_metriques_dimensions_faits_grain_vocabulaire_exact.md
```

## Vérification finale, à rejouer après le dernier push

```bash
python3 01_socle_donnees/scripts/autovalide.py M11 --strict      # attendu : OK (0 avertissement), 9 fichiers
python3 01_socle_donnees/scripts/chiffres_manuel.py M11 && git diff --stat  # attendu : aucune modification
python3 tools/controle_sql_M11.py                               # attendu : 18 controles sur 18 : OK
python3 tools/figures_M11.py                                    # attendu : verdict OK (2 planches, déterministes, citées)
python3 tools/render.py "0[234]_*/M11_*.md" --join --out 05_livrables/M11.pdf
python3 tools/controle_pdf.py M11                               # attendu : 97 pages, 0 défaut bloquant
python3 tools/poids.py                                          # attendu : ~120 Mo sur 128, marge positive
```

**Après le dernier push, deux vérifications de dépôt** (elles ont valeur de contrôle final) :

```bash
curl -s https://api.github.com/repos/nayxuspro-sketch/MesCours/contents/02_modules | grep -c '"name"'   # attendu : 75 chapitres
curl -s "https://api.github.com/repos/nayxuspro-sketch/MesCours/git/trees/main?recursive=1" | grep -c '\.pyc'  # attendu : 0
```
