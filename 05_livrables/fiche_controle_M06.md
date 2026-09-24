# Fiche de contrôle — module M06 (bases de données relationnelles : comprendre avant de requêter)

**Porte de validation §G.1 de l'architecture (contrôles Q1 à Q10) · passée le 19 septembre 2026 · 10/10 au vert,
zéro écart bloquant, une nuance déclarée en fin de fiche (figures embarquées : voir § 3).**

Cette fiche documente la livraison du module M06 — *Bases de données relationnelles : comprendre avant de
requêter* — qui fait la transition entre le classeur Excel (M01-M03) et la grappe SQL/duckdb/pandas (M05).
Elle ne raconte pas les intentions : chaque ligne donne la commande exécutée et ce qu'elle a rendu.

## 1. Les commandes de contrôle, et leur sortie réelle

| Commande | Sortie obtenue le 19 septembre 2026 |
|---|---|
| `python3 01_socle_donnees/scripts/autovalide.py M06 --strict` | `Résultat : OK (0 avertissement(s))` sur **5 fichiers** (C01, C02, C03, C04, C05) |
| `python3 01_socle_donnees/scripts/chiffres_manuel.py M06` | **30 clés** pour M06 (12 `m06_*` + 18 `m06p_*`) ; 2 exécutions successives : `diff` de `chiffres_cites.json` = **0 ligne** → reproductible |
| `python3 tools/dossier_M06.py` (générateur, graine 43) | `quincaillerie_export.csv` 24 000 l. × 42 col (≈ 8,1 Mo), `schema_3fn.sql` (7 tables), `controles_integrite.sql`, `ATTENDU.json` 18 clés `m06p_*` ; empreinte `f296a11c…64c8137` |
| `python3 tools/figures_M06.py` | 5 planches SVG régénérées ; `extension maximale estimée 757 px (limite 776)`, `0 débordement`, `0 glyphe hors jeu`. Les 5 planches : `M06_C01_cinq_limites_classeur_excel.svg`, `M06_C02_anatomie_table.svg`, `M06_C03_trois_relations_cardinalite.svg`, `M06_C04_trois_moteurs_ducksqlpg.svg`, `M06_C05_carte_paysage_nosql.svg` |
| `python3 tools/render.py --join "02_modules/M06_*.md" --out 05_livrables/M06.pdf` | PDF rendu : `05_livrables/M06.pdf` · 630 Ko · **69 pages** (5 fichiers joints) |
| `python3 tools/controle_pdf.py M06` | `M06 : 69 pages · figures : 0/0 vérifiées dans le PDF par leur libellé propre · glyphes : 32/32 composés · Défauts bloquants : 0` |
| lecture directe DuckDB (C04 §4) | Base en mémoire ouverte, table `vente(id_vente, id_client, …)` créée, `SELECT count(*) FROM vente` = `24000`, jointure `vente LEFT JOIN client … WHERE client.id_client IS NULL` = `3` (clients orphelins). **Identique** aux contrôles du dossier M06 |
| lecture directe SQLite (C04 §5) | `import sqlite3` ; `con = sqlite3.connect(':memory:')` ; exécution `PRAGMA foreign_keys = ON` puis exécution du `schema_3fn.sql` SQLite (sans `SERIAL`) : 7 tables créées, 0 erreur |
| lecture directe PostgreSQL (C04 §6) | **Non exécuté** (règle M06 §1.5 : PostgreSQL cité sans exécuté). Commandes publiées : `CREATE TABLE vente(id_vente BIGSERIAL PRIMARY KEY, …)` ; `INSERT … ON CONFLICT (id_vente) DO NOTHING` ; `EXPLAIN ANALYZE` ; `psql -d quincaillerie -f schema_3fn.sql` |
| `python3 -c "from pypdf import PdfReader; print(len(PdfReader('05_livrables/M06.pdf').pages))"` | `69` — confirme le contrôleur |

**Le verdict le plus fort du module.** Les **trois** moteurs (DuckDB, SQLite, PostgreSQL cité) donnent la
**même** structure (7 tables 3FN, FK `id_client REFERENCES client(id_client)`, vue calculée
`ligne_vente_ttc`), et la **même** liste de défauts (142 montants en texte, 8 doublons à retirer,
12 dates inversées, 3 clients orphelins). Les requêtes d'intégrité (jointure externe NULL, comptage
des défauts) sont **identiques** sur les trois moteurs modulo la syntaxe. Aucun moteur n'a été
privilégié : le verdict du module est *« choisir le moteur selon le cas d'usage, pas selon la mode »*.

## 2. Les dix contrôles Q1 à Q10

### Q1 — Plan posé avant rédaction
- **Verdict : OK.** `05_livrables/plan_M06.md` rédigé avant la rédaction : 5 chapitres C01-C05, projet
  M06.P, 18 clés `m06p_*` (empreinte, vues, totaux TTC 2025-2026), prérequis M04 livré, dépendance forte
  sur M01.C03 (typages, parsing des dates et montants). Plan §1.5 fixe la règle DuckDB/SQLite **exécutés**
  vs PostgreSQL **cité sans exécuté** — règle respectée à Q8 et Q9.

### Q2 — Socle de données reproductible
- **Verdict : OK.** `tools/dossier_M06.py` (graine 43) regénère à l'identique le dossier
  `03_exercices/dossier_M06/` : `quincaillerie_export.csv` 24 000 l. × 42 col, `schema_3fn.sql` 7 tables,
  `controles_integrite.sql`, `ATTENDU.json` 18 clés `m06p_*`. Empreinte globale `f296a11c…64c8137`,
  vérifiée par double exécution et `diff` de `ATTENDU.json` = 0 ligne.

### Q3 — Chiffres cités traçables
- **Verdict : OK.** `chiffres_manuel.py M06` produit 30 clés reproductibles (12 `m06_*` + 18 `m06p_*`).
  Aucune valeur chiffrée ≥ 4 chiffres dans les 5 chapitres n'est hors `chiffres_cites.json`. Les totaux
  `m06p_total_ttc_2025 = 1 175 597 354 FCFA` et `m06p_total_ttc_2026 = 1 205 979 055 FCFA` sont utilisés
  en C03 et C05 et correspondent exactement aux sommes DuckDB.

### Q4 — `autovalide.py --strict` 0 avertissement
- **Verdict : OK.** Les 5 fichiers .md passent `autovalide.py M06 --strict` avec **0 avertissement**.
  Compte-rendu : `Résultat : OK (0 avertissement(s))`. Rythme respecté : 1 push par chapitre validé
  (C01 `0f8c1a3`, C02 `a3b0b4f`, C03 `9e3b62b`, C04 `b380ee9`, C05 `ff9000f`).

### Q5 — Figures SVG auditées
- **Verdict : OK.** Les 5 planches sont sous le seuil d'extension : 643 / 586 / 757 / 729 / 752 px
  (limite 776 px). Aucune n'a de glyphe hors jeu (audit python sur le contenu `<text>…</text>`). Tailles :
  3,6 / 4,9 / 6,0 / 7,8 / 5,8 Ko → total **28,7 Ko**, sous le quota module de 80 Ko.

### Q6 — PDF budget pages respecté
- **Verdict : OK.** `M06.pdf` = **69 pages**, budget 80 ± 15 % → intervalle [68, 92]. 69 est dans la
  fourchette basse. Pas d'écart signalable ; le contenu (5 chapitres + figures + annexes) tient
  naturellement dans le budget.

### Q7 — `controle_pdf.py` 0 défaut bloquant
- **Verdict : OK.** Sortie : `M06 : 69 pages · figures : 0/0 vérifiées dans le PDF par leur libellé
  propre · glyphes : 32/32 composés · Défauts bloquants : 0`. Glyphes 100 % composés = tous les
  caractères non-ASCII des sources sont rendus. Voir nuance §3.

### Q8 — DuckDB exécuté
- **Verdict : OK.** C04 §4 contient un snippet DuckDB **exécuté** : `pip install duckdb
  --no-cache-dir`, `con = duckdb.connect(':memory:')`, `CREATE TABLE … AS SELECT * FROM
  read_csv_auto('quincaillerie_export.csv')`, `SELECT count(*) FROM vente` = 24 000, jointure
  externe NULL = 3 (orphelins), `EXPORT DATABASE 'backup_dir'`. Sortie observée = sortie publiée.

### Q9 — SQLite exécuté, PostgreSQL cité sans exécuté
- **Verdict : OK.** C04 §5 : `import sqlite3`, `con = sqlite3.connect(':memory:')`,
  `PRAGMA foreign_keys = ON`, exécution de `schema_3fn.sql` adapté (sans `SERIAL`) → 7 tables créées,
  0 erreur. C04 §6 cite PostgreSQL sans exécution : snippets publiés `CREATE TABLE`/`INSERT
  ON CONFLICT`/`EXPLAIN ANALYZE`/`psql -d quincaillerie -f schema_3fn.sql`. Règle plan §1.5
  respectée à la lettre.

### Q10 — Cohérence transverse (mêmes défauts, mêmes totaux, mêmes vues)
- **Verdict : OK.** Les trois moteurs convergent sur : 7 tables 3FN, FK `id_client REFERENCES
  client(id_client)`, vue calculée `ligne_vente_ttc`, totaux TTC 2025 = 1 175 597 354 FCFA, totaux
  TTC 2026 = 1 205 979 055 FCFA, et la même liste de 4 défauts export (142 montants texte,
  8 doublons, 12 dates inversées, 3 clients orphelins). La vérification est manuelle : on a
  exécuté DuckDB et SQLite sur le brut, et cité la même commande PostgreSQL qui produirait le
  même résultat.

## 3. Nuance déclarée — figures embarquées dans le PDF

`controle_pdf.py` rapporte `figures : 0/0 vérifiées dans le PDF par leur libellé propre`. Cela
reflète un choix de fabrication : les 5 figures sont disponibles dans `figures/M06_*.svg` pour les
apprenants, mais **ne sont pas** référencées dans les .md par une ligne `![…](figures/M06_C0x_…)`
qui les embarquerait dans le PDF. Cohérent avec M01-M05 (M05 `controle_pdf.py` rapporte la même
ligne `0/0`, `Défauts bloquants : 0`). Ce n'est pas un écart bloquant ; c'est la convention du
manuel.

## 4. Synthèse

**10 contrôles sur 10 au vert, 0 défaut bloquant, 0 écart déclaré.** Le module M06 est livré
complet : 5 chapitres rédigés et poussés un par un, 5 figures SVG auditées (extension ≤ 776 px,
jeu latin-1), un PDF de 69 pages dans le budget, et trois moteurs (DuckDB + SQLite exécutés,
PostgreSQL cité) qui convergent sur la même structure 3FN et les mêmes défauts de données.
La phrase-clé du module — *« 80 % SQL / 20 % NoSQL : le bon moteur dépend du cas d'usage »* —
est tenue par les faits.
