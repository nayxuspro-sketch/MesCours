# Fiche de contrôle — module M08 (Python pour l'analyse de données)

**Porte de validation §G.1 de l'architecture (contrôles Q1 à Q10) · passée le 20 septembre 2026 · 10/10 au
vert, zéro écart bloquant, deux nuances déclarées en fin de fiche (versions pandas ; figure C01 embarquée
au commit final).**

Cette fiche documente la livraison du module M08 — *Python pour l'analyse de données* — huit chapitres
(N2 → N3, 30 h) qui re-chaussent en pandas le socle commercial M07 et font tenir le parallèle
SQL/pandas jusqu'à la centaine de FCFA. Elle ne raconte pas les intentions : chaque ligne donne la
commande exécutée et ce qu'elle a rendu.

## 1. Les commandes de contrôle, et leur sortie réelle

| Commande | Sortie obtenue le 20 septembre 2026 |
|---|---|
| `python3 01_socle_donnees/scripts/autovalide.py M08 --strict` | `Résultat : OK (0 avertissement(s))` sur **8 fichiers** (C01 à C08) |
| `python3 01_socle_donnees/scripts/chiffres_manuel.py M08` | **76 clés** `m08_*`/`m08p_*` ; 2 exécutions successives : `diff` de `chiffres_cites.json` = **0 ligne** → reproductible ; la croisée SQL/pandas est **intégrée** : toute divergence lève une `ValueError` |
| `python3 tools/dossier_M08.py` (venv, duckdb 1.5.5) | Réexport déterministe du dossier `03_exercices/dossier_M08/` (8 CSV dont `objectif_magasin.csv` 0 ligne, `00_brief.md`, `ATTENDU.json`) ; **diff = 0 ligne** à la double exécution ; empreinte dossier `b9a8d973119342ec…` ; côté SQL : CA brut 7908259731, CA propre 7876320163, écart retours 31939568, doublons 8, retours 208/200, dates naïves 21406, deadlines 18/15, manquants 0 |
| `python3 tools/figures_M08.py` | 8 planches SVG régénérées ; extensions max **776 / 767 / 738 / 686 / 690 / 740 / 719 / 616 px** (limite 776), `0 débordement`, `0 glyphe hors jeu`. Tailles 5,7 / 8,4 / 6,8 / 6,6 / 4,7 / 5,0 / 11,7 / 6,3 Ko → total **55,2 Ko**, sous le quota module de 80 Ko |
| `python3 tools/render.py "02_modules/M08_*.md" --join --out 05_livrables/M08.pdf` | PDF rendu : `05_livrables/M08.pdf` · 1097 Ko · **119 pages** (8 fichiers joints + couverture + sommaire) |
| `python3 tools/controle_pdf.py M08` | `M08 : 119 pages · figures : 8/8 vérifiées dans le PDF par leur libellé propre · glyphes : 36/36 composés · Défauts bloquants : 0` |
| `python3 tools/controle_exos_M08.py` | **Bilan : 15/15 réponses conformes · tout est vert** — l'épreuve C de l'évaluation (15 blocs pandas « prédisez la sortie »), valeurs mesurées sur le dossier livré |
| Croisée SQL/pandas (intégrée à `chiffres_manuel.py M08`) | `m08p_croisee_sql_pandas = OK (25 valeurs : comptages exacts, totaux ± 2 FCFA)` ; dérive `float` **mesurée** : 1 FCFA sur chacun des 5 totaux (clés `m08p_ecart_somme_float_ca_brut/_ca_sans_retours/_ca_2025/_ca_2026/_ca_categorie_top` = 1) |
| SQLite exécuté (contrôle de la fiche, `sqlite3` natif Python 3.13, base en mémoire) | `vente.csv` chargé (50 008 lignes) ; `SUM(ROUND(montant_ttc*100))` en entiers puis `/ 100` : CA brut = **7908259732**, CA propre = **7876320164** — **concordance exacte** avec le côté pandas (centimes entiers) |
| `python3 03_exercices/dossier_M08/analyse_commerciale_modele.py` (venv pandas 3.0.6, exécuté le 19/09/2026) | Script du projet **exécuté d'une traite** : 6 sections S1–S6, 4 PNG, classeur 4 feuilles ; sorties publiées au §13 de C08 (CA brut 7908259732, CA propre 7876320164, panier 158140, top magasin 4 = 1596813264, top catégorie 7 = 1236006464, plus gros mois magasin 3 2025-08 = 78965529) |
| `python3 -c "from pypdf import PdfReader; print(len(PdfReader('05_livrables/M08.pdf').pages))"` | `119` — confirme le contrôleur |

**Le verdict le plus fort du module.** Les trois moteurs d'accord sur le même socle : DuckDB
(`float`, CA brut 7908259731), SQLite et pandas (centimes **entiers**, CA brut 7908259732) — l'écart de
1 FCFA est la dérive `float` de DuckDB, **mesurée et sourcée**, pas un défaut. Aucun chiffre du manuel
n'est « illustratif » : les 76 clés sont reproductibles (diff = 0 à la double exécution), la croisée
lève une erreur à la moindre divergence, et le script du projet est commité et ses sorties publiées
telles quelles.

## 2. Les dix contrôles Q1 à Q10

### Q1 — Plan posé avant rédaction
- **Verdict : OK.** `05_livrables/plan_M08.md` rédigé avant la rédaction : 8 chapitres C01–C08
  (30 h), budget PDF 117 pages ± 15 %, 8 figures (une par chapitre), projet M08.P (1 script, 6
  sections, 4 graphiques, /20 seuil 13), évaluation (quiz 15 Q + 5 exercices rendus + 15 auto-validés),
  parallèle SQL/pandas comme colonne vertébrale, 12 écritures obsolètes pandas 3.x à reproduire
  verbatim (§1.7), règle héritée §1.5 (DuckDB et SQLite exécutés, PostgreSQL cité sans exécuté).
  Règles respectées aux Q8 et Q9.

### Q2 — Socle de données reproductible
- **Verdict : OK.** `tools/dossier_M08.py` réexporte **déterministement** (aucun tirage aléatoire,
  base M07 figée) le dossier `03_exercices/dossier_M08/` : 8 CSV (50 008 ventes dont 8 doublons,
  208 retours en brut / 200 dédoublonnés, 21 406 dates sous la condition naïve, 15 deadlines
  aberrantes, 0 valeur manquante, `objectif_magasin.csv` 0 ligne), `00_brief.md`, `ATTENDU.json`
  (côté SQL de la croisée). **diff = 0 ligne** entre deux exécutions ; empreinte dossier
  `b9a8d973119342ec…`.

### Q3 — Chiffres cités traçables
- **Verdict : OK.** `chiffres_manuel.py M08` produit **76 clés** reproductibles (diff = 0 à la double
  exécution). Aucune valeur chiffrée ≥ 4 chiffres dans les 8 chapitres n'est hors
  `chiffres_cites.json` (porte `autovalide --strict`). Les totaux canoniques sont ceux de
  l'**addition en centimes entiers** côté pandas : `m08p_ca_brut = 7908259732`,
  `m08p_ca_sans_retours = 7876320164`, `m08p_plus_gros_mois_ca = 78965529` — et correspondent aux
  côtés SQL/SQLite de la croisée (± 1 FCFA sur les totaux `float` de DuckDB, mesuré).

### Q4 — `autovalide.py --strict` 0 avertissement
- **Verdict : OK.** Les 8 fichiers .md passent avec **0 avertissement**. Compte-rendu :
  `Résultat : OK (0 avertissement(s))`. Rythme respecté : 1 push par chapitre validé
  (C01 `e08cb12`, C02 `705635a`, C03 `c5575f8`, C04 `e4a6958`, C05 `3d0e348`, C06 `c929aaf`,
  C07 `45aa211`, C08 `294d5e9`).

### Q5 — Figures SVG auditées
- **Verdict : OK.** Les 8 planches sont sous le seuil d'extension : 776 / 767 / 738 / 686 / 690 /
  740 / 719 / 616 px (limite 776 px). Aucune n'a de glyphe hors jeu (audit du contenu `<text>`,
  jeu latin-1 étendu). Tailles 5,7 / 8,4 / 6,8 / 6,6 / 4,7 / 5,0 / 11,7 / 6,3 Ko → total **55,2 Ko**,
  sous le quota module de 80 Ko.

### Q6 — PDF budget pages respecté
- **Verdict : OK.** `M08.pdf` = **119 pages**, budget 117 ± 15 % → intervalle [99, 135]. 119 est à
  **+1,7 %** du budget central (8 chapitres de 12 à 17 pages + couverture + sommaire) ; pas d'écart
  signalable.

### Q7 — `controle_pdf.py` 0 défaut bloquant
- **Verdict : OK.** Sortie : `M08 : 119 pages · figures : 8/8 vérifiées dans le PDF par leur libellé
  propre · glyphes : 36/36 composés · Défauts bloquants : 0`. Convention M08 (héritée, appliquée à
  8/8) : les .md **embarquent** leurs planches par `![…](../figures/…)`, donc le contrôleur retrouve
  chaque libellé SVG dans le PDF — évolution par rapport au 0/0 déclaré en M07.

### Q8 — Moteurs exécutés
- **Verdict : OK.** Portée maximale : la **croisée SQL/pandas** (25 valeurs) passe — comptages
  exacts, totaux monétaires ± 2 FCFA, toute divergence lève une `ValueError` dans
  `chiffres_manuel.py M08`. DuckDB **exécuté** (côté SQL, `tools/dossier_M08.py`, 1.5.5) ; SQLite
  **exécuté** (contrôle de la fiche : 50 008 lignes en mémoire, CA brut et CA propre en centimes
  entiers = concordance **exacte** avec pandas) ; pandas **exécuté** en 2.2.3 (environnement
  d'écriture, totaux canoniques) et en **3.0.6** (venv de référence : les 12 écritures obsolètes
  reproduites verbatim — `iteritems`, `applymap`, `mad`, `reindex_axis` en `AttributeError`, la
  copie-on-écriture **silencieuse**, `resample('M')` en `ValueError` — et les 4 écarts 2.2.3/3.0.6
  reproduits et chiffrés : cellules vides 103 → 85, modalités 373 → 372, lignes champ vide 18 → 0,
  colonnes object 7 → 0). Le script du projet est exécuté bout en bout (6 sections, 4 PNG, 4
  feuilles).

### Q9 — PostgreSQL cité sans exécuté
- **Verdict : OK.** Règle §1.5 : DuckDB et SQLite exécutés (Q8) ; PostgreSQL tient la règle à sa
  forme la plus stricte — **zéro mention** dans les 8 chapitres d'un module centré sur Python :
  aucune requête PostgreSQL n'est présentée, ni comme exécutée ni comme citée.

### Q10 — Cohérence transverse (mêmes totaux, mêmes défauts, mêmes clés)
- **Verdict : OK.** Les trois niveaux convergent : les 8 chapitres, le projet (script commité,
  sorties publiées) et l'évaluation (dont les 15 exercices « prédisez la sortie » sont
  auto-validés par script, 15/15) citent les **mêmes** totaux (CA brut 7908259732 en centimes —
  7908259731 côté `float` de DuckDB, CA propre 7876320164, panier 158140, 50 008 ventes, 1 200
  clients, plus gros mois 78965529) et les **mêmes** 4 défauts du socle chiffrés (8 doublons,
  208/200 retours, 21 406 dates naïves + 15 deadlines, 1 table vide). Le parallèle M07 tient :
  la même base (50 008 ventes), la même vue « sans retours », le même plus gros mois — M07 l'a
  requêtée en SQL, M08 la reconstruit en pandas au FCFA près. Les clés `m08_*`/`m08p_*` de
  `chiffres_cites.json` sont le seul référentiel : 76 clés, reproductibles (diff = 0).

## 3. Nuances déclarées

1. **Deux versions de pandas, un seul référentiel de chiffres.** L'environnement d'écriture est
   pandas **2.2.3** (numpy 2.3.5, Python 3.13) ; le comportement de référence publié dans les
   chapitres est celui de **3.0.6** (venv dédié, numpy 2.5.3, testé le 19/09/2026) : 12 écritures
   obsolètes, copie-on-écriture, `resample('ME')`. Les totaux canoniques sont mesurés côté 2.2.3 —
   identiques aux deux versions car l'addition se fait **en centimes entiers** (aucun arrondi
   intermédiaire). Les 4 écarts 2.2.3/3.0.6 de comportement (cellules vides, modalités, lignes
   champ vide, colonnes object) sont **publiés et chiffrés** dans le module, pas masqués.
2. **Figure C01 embarquée au commit final.** Le chapitre C01 (poussé `e08cb12`) mentionnait sa
   planche dans le corps sans ligne d'embarquement ; l'embarquement a été ajouté au commit final de livraison (PDF
   recomposé), après le push de C08. Le 8/8 de `controle_pdf.py` est celui du PDF final.

## 4. Synthèse

**10 contrôles sur 10 au vert, 0 défaut bloquant, 2 nuances déclarées.** Le module M08 est livré
complet : 8 chapitres rédigés et poussés un par un (8 commits), 8 figures SVG auditées (extension
≤ 776 px, jeu latin-1 étendu, 55,2 Ko), un socle de 8 CSV réexporté déterministement de la base M07
figée, un PDF de 119 pages dans le budget [99, 135], un projet dont le script est **commité** et
exécuté bout en bout, une évaluation dont les 15 exercices de l'épreuve C sont
**auto-validés par script (15/15)** et dont l'étude de cas porte sur 3 erreurs
typées (`NameError`, `KeyError`, `SettingWithCopyWarning`) + un total faux mesuré. La phrase-clé du module —
*« la donnée est la même, le moteur change, le total ne doit pas changer de plus de 2 FCFA, et
l'écart doit être mesuré, sourcé et documenté »* — est tenue par les faits : 25 valeurs croisées,
0 divergence, 1 FCFA d'écart `float` mesuré sur 5 totaux, 3 moteurs d'accord (DuckDB, SQLite,
pandas).
