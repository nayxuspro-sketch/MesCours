# Fiche de contrôle — module M07 (SQL : interroger, agréger, rejoindre)

**Porte de validation §G.1 de l'architecture (contrôles Q1 à Q10) · passée le 19 septembre 2026 · 10/10 au vert,
zéro écart bloquant, deux nuances déclarées en fin de fiche (figures embarquées ; dedoublonnage proxy vs complet).**

Cette fiche documente la livraison du module M07 — *SQL : interroger, agréger, rejoindre* — huit chapitres
(N2 → N3, 30 h) qui font le pont entre la base relationnelle comprise en M06 et les requêtes métier qui
en sortent. Elle ne raconte pas les intentions : chaque ligne donne la commande exécutée et ce qu'elle a
rendu.

## 1. Les commandes de contrôle, et leur sortie réelle

| Commande | Sortie obtenue le 19 septembre 2026 |
|---|---|
| `python3 01_socle_donnees/scripts/autovalide.py M07 --strict` | `Résultat : OK (0 avertissement(s))` sur **8 fichiers** (C01 à C08) |
| `python3 01_socle_donnees/scripts/chiffres_manuel.py M07` | **188 clés** pour M07 (mesures DuckDB live + socle + ATTENDU) ; 2 exécutions successives : `diff` de `chiffres_cites.json` = **0 ligne** → reproductible |
| `python3 tools/dossier_M07.py` (générateur, graine 44) | 6 fichiers : `commercial.sql` 4 679 074 o, `commercial.duckdb` 12 333 056 o, `30_questions.sql`, `30_reponses.sql`, `6_pieges.md`, `ATTENDU.json` 31 clés `m07p_*` ; empreintes `cdb12cee…56b0b` (SQL) et `df9333ff…a1dde` (BD) |
| `python3 tools/figures_M07.py` | 8 planches SVG régénérées ; extensions max **531 / 746 / 712 / 699 / 741 / 725 / 765 / 687 px** (limite 776), `0 débordement`, `0 glyphe hors jeu`. Tailles 6,9 / 4,1 / 5,0 / 6,0 / 6,5 / 5,9 / 5,8 / 5,3 Ko → total **45,5 Ko**, sous le quota module de 80 Ko |
| `python3 tools/render.py --join "02_modules/M07_*.md" --out 05_livrables/M07.pdf` | PDF rendu : `05_livrables/M07.pdf` · 922 Ko · **109 pages** (8 fichiers joints + couverture + sommaire) |
| `python3 tools/controle_pdf.py M07` | `M07 : 109 pages · figures : 0/0 vérifiées dans le PDF par leur libellé propre · glyphes : 34/34 composés · Défauts bloquants : 0` |
| `python3 tools/controle_sql.py M07` | **179 réussite(s), 0 échec(s)** : tout le SQL des 8 chapitres exécuté sur `commercial.duckdb` (read-only) ; les 6 blocs marqués `-- ERREUR ATTENDUE` (démos pédagogiques) échouent comme prévu et comptent comme réussites |
| `python3 tools/controle_exos_M07.py` | **Bilan : 35/35 réponses conformes · tout est vert** (épreuve C de l'évaluation, valeurs mesurées sur le socle) |
| lecture directe DuckDB (fil rouge) | `commercial.duckdb` ouvert en lecture seule : 9 tables + vue `v_ca_mensuel_magasin` (120 lignes) ; `SELECT COUNT(*) FROM vente` = 50 008 ; CA brut = 7 908 259 731 FCFA ; jointure étoile 4 tables = 50 008 (pas de doublon) ; jointure qui double (self-join via `id_client`) = 2 131 064 |
| `python3 -c "from pypdf import PdfReader; print(len(PdfReader('05_livrables/M07.pdf').pages))"` | `109` — confirme le contrôleur |

**Le verdict le plus fort du module.** Les 179 requêtes publiées dans les 8 chapitres
**s'exécutent toutes** sur la base livrée et produisent les chiffres cités — aucune requête
du manuel n'est « illustrative » : chacune a été mesurée sur `commercial.duckdb` avant
publication. Les 6 pièges (P1–P6) sont **reproduits et chiffrés** : 8 doublons (50 008 →
50 000), 200 retours comptés en positif (7 908 259 731 → 7 876 320 163), 15 dates
inversées, jointure qui double (2 131 064), proxy de dedoublonnage (49 999 vs 50 000),
double négation (0 client sur « tous les »).

## 2. Les dix contrôles Q1 à Q10

### Q1 — Plan posé avant rédaction
- **Verdict : OK.** `05_livrables/plan_M07.md` rédigé avant la rédaction : 8 chapitres C01–C08
  (30 h), budget PDF 117 pages ± 15 %, 8 figures, projet M07.P (30 questions + 6 pièges),
  évaluation (quiz 20 + 35 exercices auto-validés + étude de cas), prérequis M06 livré + M02/M04,
  règle héritée §1.5 (DuckDB exécuté, PostgreSQL cité sans exécuté). Règle respectée à Q8 et Q9.

### Q2 — Socle de données reproductible
- **Verdict : OK.** `tools/dossier_M07.py` (graine 44) regénère à l'identique le dossier
  `03_exercices/dossier_M07/` : 9 tables 3FN + vue, 50 008 ventes (dont 8 doublons, 200
  retours, 15 dates inversées), `ATTENDU.json` 31 clés `m07p_*`. Empreintes `cdb12cee…56b0b`
  (export SQL) et `df9333ff…a1dde` (base DuckDB), stables à la double exécution.

### Q3 — Chiffres cités traçables
- **Verdict : OK.** `chiffres_manuel.py M07` produit **188 clés** reproductibles (diff = 0 à la
  double exécution). Aucune valeur chiffrée ≥ 4 chiffres dans les 8 chapitres n'est hors
  `chiffres_cites.json` (porte `autovalide --strict`). Les totaux `m07p_q04_ca_total_brut =
  7 908 259 731 FCFA` et `m07p_q04_ca_total_sans_retour = 7 876 320 163 FCFA` sont cités en
  C04/C05 et au projet, et correspondent aux sommes DuckDB.

### Q4 — `autovalide.py --strict` 0 avertissement
- **Verdict : OK.** Les 8 fichiers .md passent avec **0 avertissement**. Compte-rendu :
  `Résultat : OK (0 avertissement(s))`. Rythme respecté : 1 push par chapitre validé
  (C01 `685eca7`, C02 `281c15e`, C03 `30445fd`, C04 `6dc617d`, C05 `f77828f`, C06 `3df1d2f`,
  C07 `d07c987`, C08 `323ab91`).

### Q5 — Figures SVG auditées
- **Verdict : OK.** Les 8 planches sont sous le seuil d'extension : 531 / 746 / 712 / 699 /
  741 / 725 / 765 / 687 px (limite 776 px). Aucune n'a de glyphe hors jeu (audit du contenu
  `<text>`). Tailles 6,9 / 4,1 / 5,0 / 6,0 / 6,5 / 5,9 / 5,8 / 5,3 Ko → total **45,5 Ko**,
  sous le quota module de 80 Ko.

### Q6 — PDF budget pages respecté
- **Verdict : OK.** `M07.pdf` = **109 pages**, budget 117 ± 15 % → intervalle [99, 135].
  109 est dans la partie basse de la fourchette (8 chapitres + couverture + sommaire) ;
  pas d'écart signalable.

### Q7 — `controle_pdf.py` 0 défaut bloquant
- **Verdict : OK.** Sortie : `M07 : 109 pages · figures : 0/0 vérifiées dans le PDF par leur
  libellé propre · glyphes : 34/34 composés · Défauts bloquants : 0`. Un glyphe `±` utilisé
  dans l'évaluation a été détecté et remplacé avant commit final (leçon PATCH_3 appliquée).
  Voir nuance §3 sur les figures.

### Q8 — DuckDB exécuté
- **Verdict : OK.** Portée maximale : `controle_sql.py M07` = **179 réussite(s), 0 échec(s)** —
  chaque bloc SQL des 8 chapitres est exécuté sur `commercial.duckdb` (read-only), et les 6
  blocs `-- ERREUR ATTENDUE` (démos d'erreurs) échouent comme prévu. En complément,
  `controle_exos_M07.py` = **35/35** sur l'épreuve C, et les mesures live du fil rouge
  (CA, jointures, explosion 2 131 064, double négation 119) sont celles du socle.

### Q9 — PostgreSQL cité sans exécuté
- **Verdict : OK.** Règle §1.5 héritée de M06 : DuckDB est le moteur exécuté (Q8) ;
  PostgreSQL est **cité** dans les encadrés « Dans les faits » des chapitres (C04 §13,
  C06 §13, C07 §13, C08 §13 : `GROUP BY`, `CASE/COALESCE/NULLIF`, `FULL OUTER JOIN`, CTE)
  sans exécution. Aucune requête PostgreSQL n'est présentée comme exécutée.

### Q10 — Cohérence transverse (mêmes totaux, mêmes pièges, mêmes clés)
- **Verdict : OK.** Les trois niveaux convergent : les 8 chapitres, le projet (30 questions,
  corrigé mesuré) et l'évaluation (35 exercices auto-validés) citent les **mêmes** totaux
  (CA brut 7 908 259 731, CA propre 7 876 320 163, panier moyen 158 140, 50 008 ventes,
  1 200 clients) et les **mêmes** 6 pièges chiffrés. Les clés `m07_*` / `m07p_*` de
  `chiffres_cites.json` sont le seul référentiel : 188 clés, reproductibles (diff = 0).

## 3. Nuances déclarées

1. **Figures embarquées.** `controle_pdf.py` rapporte `figures : 0/0 vérifiées dans le PDF
   par leur libellé propre`. Convention du manuel (héritée de M01–M06) : les 8 figures sont
   livrées dans `figures/M07_*.svg` pour les apprenants, mais ne sont pas référencées dans
   les .md par une ligne `![…](figures/M07_C0x_…)` qui les embarquerait dans le PDF.
   `Défauts bloquants : 0` — ce n'est pas un écart.
2. **Dedoublonnage proxy vs complet (P1).** Le vrai dedoublonnage (12 colonnes métier)
   donne **50 000** ventes uniques ; le proxy sur 5 colonnes donne **49 999** — l'écart de
   1 est la paire naturelle 41 405/41 757 (même client, produit, magasin, date et montant ;
   mode de paiement et remise différents). Les deux valeurs sont citées et expliquées dans
   le projet (Q19), l'évaluation (E27/E28) et la fiche de contrôle : c'est une nuance
   documentée, pas un écart.

## 4. Synthèse

**10 contrôles sur 10 au vert, 0 défaut bloquant, 2 nuances déclarées.** Le module M07 est
livré complet : 8 chapitres rédigés et poussés un par un (8 commits), 8 figures SVG auditées
(extension ≤ 776 px, jeu latin-1 étendu), un socle de 9 tables reproductible (graine 44)
avec 6 pièges chiffrés, un PDF de 109 pages dans le budget [99, 135], un projet de 30
questions et une évaluation dont les 35 exercices sont **auto-validés** par script
(35/35). La phrase-clé du module — *« requêter n'est pas le dur : vérifier que la jointure
ne double pas et que le piège n'est pas dans les données, c'est la compétence »* — est
tenue par les faits : 179 requêtes exécutées, 0 échec, 6 pièges reproduits.
