# Fiche de contrôle — module M09 (Analyse exploratoire de données)

**Porte de validation §G.1 de l'architecture (contrôles Q1 à Q10) · passée le 20 septembre 2026 · 10/10 au
vert, zéro écart bloquant, deux nuances déclarées en fin de fiche (tiret demi-cadratin absent du jeu de
police composé ; correctif de composition appliqué à tout le corpus).**

Cette fiche documente la livraison du module M09 — *Analyse exploratoire de données* — six chapitres
(N3, 30 h) qui installent le **protocole en 10 étapes** sur quatre jeux de données : le fil rouge
commercial de M07/M08, un centre de santé, un établissement scolaire, et un fichier projet « que
personne n'a regardé ». Elle ne raconte pas les intentions : chaque ligne donne la commande exécutée et
ce qu'elle a rendu.

## 1. Les commandes de contrôle, et leur sortie réelle

| Commande | Sortie obtenue le 20 septembre 2026 |
|---|---|
| `python3 01_socle_donnees/scripts/autovalide.py M09 --strict` | `Résultat : OK (0 avertissement(s))` sur **8 fichiers** (C01 à C06 + projet + évaluation) |
| `python3 01_socle_donnees/scripts/chiffres_manuel.py M09` | **130 clés** `m09_*` / `m09p_*` / `m09v_*` ; 2 exécutions successives : `diff` de `chiffres_cites.json` = **0 ligne** → reproductible ; la croisée pandas/génération est **intégrée** : toute divergence lève une `ValueError` |
| `python3 tools/dossier_M09.py` (venv, duckdb 1.5.5) | Dossier `03_exercices/dossier_M09/` régénéré : quincaillerie (réexport M07/M08), santé (18 818 consultations, défauts `manquants_motif` 23 / `doublons_stock` 7 / `consultations_date_future` 1 / `stocks_negatifs` 4), scolaire (`notes_hors_bornes` 6 / `doublons_eleves` 2 / `absences_jour_ferie` 4 / `absents_not_t2` 3), projet (`doublons_tx_ref` 14 / `montants_negatifs` 5 / `montants_enormes` 2 / `commissions_manquantes` 30) ; **`diff -rq` = 0** (dossier byte-identique avant/après) ; empreinte `026d39a6f167b74c…` ; corrélation scolaire `-0.232`, ruptures `{M01: 3, M02: 5, M04: 2}` |
| `python3 tools/figures_M09.py` | 6 planches SVG régénérées ; extensions max **728 / 750 / 746 / 733 / 767 / 722 px** (limite 776), `0 débordement`, `0 glyphe hors jeu`. Tailles 8,7 / 5,1 / 7,6 / 6,0 / 8,3 / 10,7 Ko → total **46,4 Ko**, sous le quota module de 80 Ko |
| `python3 tools/render.py "02_modules/M09_*.md" --join --out 05_livrables/M09.pdf` | PDF rendu : `05_livrables/M09.pdf` · 645 Ko · **82 pages** (6 fichiers joints + couverture + sommaire) |
| `python3 tools/controle_pdf.py M09` | `M09 : 82 pages · figures : 6/6 vérifiées dans le PDF par leur libellé propre · glyphes : 36/36 composés · Défauts bloquants : 0` |
| `python3 tools/controle_exos_M09.py` | **Bilan : 15/15 réponses conformes · tout est vert** — l'épreuve C de l'évaluation (15 blocs pandas « prédisez la sortie », dont les 12 valeurs du **variant 12 mois** de l'étude de cas), mesurés sur le dossier livré |
| `python3 tools/budget_pages.py --mesure` | `mesure M09 : 6 fichiers · 34 318 mots · budget 92 p. · composé 82 p. → dérive -11 % ; 12.5 p./chapitre (calibre 12.5)` ; budget additif et conforme à l'architecture (aucune erreur sur les 22 modules) |
| SQLite exécuté (contrôle de la fiche, `sqlite3` natif Python 3.13, base en mémoire) | `vente.csv` chargé (**50 008** lignes) : CA brut = **7908259732**, CA propre = **7876320164** (centimes entiers), doublons 12-tuple = **8**, retours = **208**, max montant = **594363** — **concordance exacte** avec les clés pandas. `consultation.csv` : **18 818** consultations, **731** jours distincts, **1** date au-delà du 2026-12-31, **23** motifs vides ; **variant 12 mois** : **9 450** consultations sur **365** jours, moyenne/jour **25.89** |
| `python3 -c "import pypdfium2 as pdfium; print(len(pdfium.PdfDocument('05_livrables/M09.pdf')))"` | `82` — confirme le contrôleur |

**Le verdict le plus fort du module.** Les deux moteurs d'accord sur le même socle : SQLite et pandas
(**centimes entiers**) donnent les mêmes totaux au FCFA près (CA brut 7908259732, CA propre 7876320164,
8 doublons, 208 retours, max 594363) et les mêmes formes sur la santé (18 818 consultations, 731 jours,
23 motifs vides, 1 date future) comme sur le variant 12 mois (9 450 / 365 / 25.89). Aucun chiffre du
module n'est « illustratif » : les 130 clés sont reproductibles (diff = 0 à la double exécution), le
dossier de travail est **byte-identique** à chaque régénération (diff = 0), la croisée lève une erreur à
la moindre divergence, et les 15 exercices de l'épreuve C sont auto-validés par script (15/15).

## 2. Les dix contrôles Q1 à Q10

### Q1 — Plan posé avant rédaction
- **Verdict : OK.** `05_livrables/plan_M09.md` rédigé avant la rédaction : 6 chapitres C01–C06
  (30 h, N3), budget PDF 92,5 pages ± 15 % → **[79, 106]**, 6 figures (une par chapitre), les
  3 études de cas (quincaillerie / santé / scolaire) + le fichier projet, projet M09.P (3 h
  chronométrées, 4 livrables, /20 seuil 13), évaluation (quiz 15 Q + étude de cas « qualité des
  questions » + corrigés) et la règle §1.5 (DuckDB et SQLite **exécutés**, PostgreSQL cité sans
  exécuté). Les 3 jeux satellites sont **plantés** de défauts chiffrés dès la génération.

### Q2 — Socle de données reproductible
- **Verdict : OK.** `tools/dossier_M09.py` régénère les **4 jeux** (graine 45) : le réexport de la
  quincaillerie M07/M08 (50 008 ventes × 13 colonnes, 8 doublons, 208 retours), le centre de santé
  (18 818 consultations, 8 767 lignes de stock, 12 médicaments), l'établissement scolaire (402 élèves,
  6 000 notes, 1 687 absences) et le fichier projet (10 014 lignes × 10 colonnes). **`diff -rq` = 0**
  entre deux exécutions, empreinte dossier `026d39a6f167b74c…` ; les défauts plantés sortent
  **identiques** à la génération et à la mesure (23 / 7 / 1 / 4 en santé, 6 / 2 / 4 / 3 en scolaire,
  14 / 5 / 2 / 30 en projet) — la croisée intégrée à `chiffres_manuel.py M09` lève une `ValueError`
  sinon.

### Q3 — Chiffres cités traçables
- **Verdict : OK.** `chiffres_manuel.py M09` produit **130 clés** reproductibles (diff = 0 à la double
  exécution). Aucune valeur chiffrée ≥ 4 chiffres dans les **8 fichiers** du module n'est hors
  `chiffres_cites.json` (porte `autovalide --strict`) — **y compris dans le projet et l'évaluation**,
  dont les 15 valeurs de l'épreuve C et les 15 clés du **variant 12 mois** (`m09v_*`) sont mesurées,
  pas déduites. Les totaux canoniques sont ceux de l'**addition en centimes entiers** :
  `m09p_q_ca_brut = 7908259732`, `m09p_q_ca_propre = 7876320164`, `m09p_q_panier_moyen = 158140`,
  `m09p_q_montant_max = 594363`, `m09p_sc_correlation_absent_notes = -0.232`.

### Q4 — `autovalide.py --strict` 0 avertissement
- **Verdict : OK.** Les 8 fichiers .md passent avec **0 avertissement**. Compte-rendu :
  `Résultat : OK (0 avertissement(s))`. Rythme respecté : 1 push par chapitre validé (C01 `b82cc73`,
  C02 `8d8d1f8`, C03 `74991c5`, C04 `46912cb`, C05 `2d068c3`, C06 `695f70e`), puis le push des
  figures et du PDF (`293d5c3`) et le push de clôture (projet, évaluation, fiche, README).
  Deux fautes ont été corrigées **avant** publication, par le même garde-fou : un identifiant d'élève
  écrit dans le corps du texte (extrait en nombre « introuvable ») et le littéral `pd.DataFrame`
  détecté comme anglicisme sans couple français par le scanner — le contrôle a mordu, la correction
  est dans le chapitre poussé.

### Q5 — Figures SVG auditées
- **Verdict : OK.** Les 6 planches sont sous le seuil d'extension : 728 / 750 / 746 / 733 / 767 /
  722 px (limite 776 px). Aucune n'a de glyphe hors jeu (audit du contenu `<text>`, jeu latin-1
  étendu — l'accent circonflexe `â` du mot « bâche » a été **ajouté au jeu publié** plutôt que
  contourné). Tailles 8,7 / 5,1 / 7,6 / 6,0 / 8,3 / 10,7 Ko → total **46,4 Ko**, sous le quota module
  de 80 Ko. Les 6 planches sont **embarquées** dans les chapitres, une par chapitre.

### Q6 — PDF budget pages respecté
- **Verdict : OK.** `M09.pdf` = **82 pages**, budget 92,5 ± 15 % → intervalle **[79, 106]** ;
  82 est à **-11 %** du budget central, dans l'intervalle. Le calibre par chapitre est exact :
  **12,5 p./chapitre** (calibre 12,5) pour 34 318 mots. Le module est dans la fourchette admise
  sans réserve.

### Q7 — `controle_pdf.py` 0 défaut bloquant
- **Verdict : OK.** Sortie : `M09 : 82 pages · figures : 6/6 vérifiées dans le PDF par leur libellé
  propre · glyphes : 36/36 composés · Défauts bloquants : 0`. Convention M09 (héritée de M08) : les
  .md **embarquent** leurs planches par `![…](../figures/…)`, donc le contrôleur retrouve chaque
  libellé SVG dans le PDF.

### Q8 — Moteurs exécutés
- **Verdict : OK.** **pandas 2.2.3 exécuté** (numpy 2.3.5, Python 3.13) : les 6 chapitres, le projet
  et l'évaluation ne citent que des sorties exécutées. **DuckDB exécuté** : le parallèle SQL/pandas
  du module (23 mentions, activé à C02) s'appuie sur les requêtes DuckDB du socle M07, dont le
  réexport quincaillerie est **régénéré par `tools/dossier_M09.py`** (duckdb 1.5.5, diff = 0).
  **SQLite exécuté** (contrôle de cette fiche, `sqlite3` natif en mémoire) : 50 008 lignes chargées,
  CA brut 7908259732 / CA propre 7876320164 en **centimes entiers**, 8 doublons, 208 retours, max
  594363 — concordance **exacte** avec pandas ; santé et variant 12 mois concordants au jour près
  (18 818 / 731 / 23 / 1 puis 9 450 / 365 / 25.89). **`matplotlib` 3.10.9 et `seaborn` 0.13.2
  exécutés** : les 5 graphiques du chapitre C06 (courbe + bâche, barres + n, boxplot, nuage + n,
  heatmap) ont été produits dans l'atelier avant publication.

### Q9 — PostgreSQL cité sans exécuté
- **Verdict : OK.** Règle §1.5 : DuckDB et SQLite **exécutés** (Q8) ; PostgreSQL tient la règle à sa
  forme la plus stricte — **zéro mention** dans les 6 chapitres d'un module centré sur l'exploration
  (le terme n'apparaît nulle part dans les fichiers du module) : aucune requête PostgreSQL n'est
  présentée, ni comme exécutée ni comme citée.

### Q10 — Cohérence transverse (mêmes totaux, mêmes défauts, mêmes clés)
- **Verdict : OK.** Les trois niveaux convergent : les 6 chapitres, le projet (corrigé-type avec
  sorties réelles) et l'évaluation (dont les 15 exercices « prédisez la sortie » sont auto-validés,
  15/15) citent les **mêmes** chiffres — CA brut 7908259732, CA propre 7876320164, panier 158140,
  max 594363 × 6, corrélation scolaire -0.232, segments 123 / 208 / 69 → 11.13 / 10.51 / 9.76,
  taux de succès projet 81.15 %, variant 12 mois 9 450 / 365 / 25.89 / 882 / 678 — et les **mêmes**
  défauts chiffrés (8 doublons quincaillerie, 23 motifs vides + 7 doublons + 4 négatifs + 1 date
  future en santé, 6 notes hors bornes + 2 doublons + 4 absences fériées + 3 absents-notés en
  scolaire, 14 + 5 + 2 + 30 en projet). Le fil rouge tient entre M07, M08 et M09 : **la même base**,
  le même CA propre, le même montant maximum — M07 l'a requêtée, M08 l'a recalculée en pandas, M09
  l'a **explorée** et n'en a rien conclu de plus que ce que le fichier dit.

## 3. Nuances déclarées

1. **Le tiret demi-cadratin était absent du PDF de M08 (corrigé, mesuré).** `controle_pdf.py M08`
   signalait **1 glyphe** dans les sources et pas dans le PDF (`–`, présent dans 2 fichiers
   d'exercices/évaluation M08). Le contrôle de police du module M09 a confirmé que ce caractère ne
   sort pas du jeu composé (DejaVuSerif) ; les 4 fichiers M08 concernés ont été passés au **tiret
   cadratin** (`—`, présent partout) et le PDF a été recomposé : **36/36 glyphes** désormais.
   La règle « chaque glyphe du .md apparaît dans le PDF » est tenue sur les 9 modules composés.
2. **Correctif de composition appliqué à tout le corpus (mesuré).** Le rendu CSS n'avait **aucune**
   règle de largeur sur les images : les planches SVG (780 px = 585 pt) dépassaient la justificative
   de 170 mm et étaient **rognées à droite** dans **tous** les PDF déjà publiés (M08 compris : le
   contrôle `controle_pdf.py` vérifiait le **libellé**, pas la géométrie). Une règle
   `img { max-width: 100 % }` a été ajoutée à `tools/render.py`, et les modules **M01, M02, M03,
   M04, M08 et M09** ont été recomposés : les planches tiennent maintenant dans les marges. Effet
   mesuré sur la pagination : M01 110 → **117** p., M02 113 → **122** p., M03 121 → **126** p.,
   M04 87 → **92** p., M08 119 p. (inchangé), M09 83 → **82** p. ; `controle_pdf.py` repasse les
   **9 modules** avec 0 défaut bloquant, et `budget_pages.py --mesure` reste dans les tolérances
   (± 15 %) sur les 9 modules mesurés.

## 4. Synthèse

**10 contrôles sur 10 au vert, 0 défaut bloquant, 2 nuances déclarées.** Le module M09 est livré
complet : 6 chapitres rédigés et poussés un par un (6 commits), 6 figures SVG auditées (extension
≤ 776 px, jeu latin-1 étendu, 46,4 Ko), un socle de **4 jeux** régénéré déterministement (graine 45,
diff = 0, empreinte `026d39a6…`), un PDF de 82 pages dans le budget [79, 106], un projet de 3 h
chronométrées (4 livrables, /20 seuil 13) dont le corrigé-type publie ses sorties réelles, une
évaluation dont les 15 exercices de l'épreuve C sont **auto-validés par script (15/15)** et dont
l'étude de cas est **délibérément inversée** (la qualité de la question passe avant la réponse). La
phrase-clé du module — *« une étape se déclare, elle ne se saute pas ; une corrélation n'est pas une
cause ; et un chiffre sans limite est une affirmation qui déborde »* — est tenue par les faits :
130 clés reproductibles, 2 moteurs d'accord à l'unité près, 15 défauts chiffrés **avec leur définition
exacte**, et 3 fausses causes contrôlées par bandes (−0.206 → −0.145 / −0.085 / +0.163).
