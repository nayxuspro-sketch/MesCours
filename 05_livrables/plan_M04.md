# Plan de production — module M04 (Qualité, préparation et documentation des données)

**6 chapitres · 30 h · niveau N2 · prérequis M02 et M03 (C01–C06) · budget 6 × 12,5 + 17 p. d'appareil = 92 p.**
Source d'autorité : `00_architecture/01_architecture_pedagogique.md`, §« M04 » (l. 439-456).

## 1. Ce que le module doit produire, et sur quoi il travaille

M04 est le seul module dont la matière est **le socle entier** : `ventes_brutes.csv`, 243 360 lignes × 20 colonnes,
28 516 920 octets. Les chiffres cités viennent des **88 clés `m04_*`** publiées par `chiffres_manuel.py` (section
`m04()`, ajoutée le 18/09/2026), toutes mesurées sur les fichiers livrés — dont trois recoupements avec
`verites_terrain.csv` (240 000 lignes · 15 419 985 157 FCFA).

Faits mesurés qui structurent le module (ils sont la colonne vertébrale des six chapitres) :

| Mesure | Valeur | Chap. |
|---|---|---|
| montants `montant_ttc` non numériques dans le brut | 3 421 | C01, C05 |
| écart du total naïf (ce que `SOMME` rate) vs vérité terrain | 2 111 789 FCFA | C01, C04 |
| lignes en collision sur la clé métier (ticket + produit + quantité) | 3 440 | C03 |
| lignes retirées au passage brut → propre | 3 360 | C03 |
| `id_vente` distincts (la clé primaire, elle, est propre) | 243 360 | C03 |
| remises saisies en points de % (> 1) et montant HT incohérent | 973 et 973 | C04 |
| lignes de vente sur un `id_client` absent des clients | 486 (372 clients distincts) | C02, C06 |
| villes absentes dans `clients.csv` | 1 911 | C02 |
| quasi-doublons clients retirés (nom + chiffres du téléphone) | 412 — la règle « sur le nom seul » en retirait 11 570 | C03 |
| dates postérieures au 31/08/2026 (règle de gestion du socle) | 51, max 2026-12-06 | C01, C04 |
| lignes de retour dont le montant n'est pas un nombre | 47 | C04 |
| quantités physiques négatives dans `stocks_quotidiens.csv` | 1 800 sur 60 000, écart maximal 532 | évaluation, étude de cas |
| fichier fournisseur : bruit avant l'en-tête, encodage, décimales | 3 lignes · cp1252 (95 octets hors ASCII, UTF-8 casse à l'octet 73) · 38 prix à la virgule · 1 conditionnement pour 38 lignes | C05 |
| `rapport_defauts.json` (corrigé enseignant) vs fichier mesuré | 3 360 annoncés / 3 421 mesurés · 2 640 dates mixtes annoncées / 0 · 1 880 villes / 1 911 · 61 catégories / 44 | C01, C06 |

**Décision de corpus prise à l'ouverture du module.** Le `rapport_defauts.json` livré dans `data/reference/` est le
*plan d'injection* des défauts, pas une mesure : il est faux sur quatre de ses huit lignes. Il n'est pas réécrit
avant la fin de la rédaction — M04 s'en sert comme objet d'étude (point 12 du diagnostic : « et votre rapport,
il est mesuré ? ») et la correction interviendra à l'étape 4 avec `generation_socle.py`, pour que le corrigé
enseignant sorte de la mesure du fichier. Consignée ici pour que la décision ne se perde pas.

**Issue de la décision, consignée le 18/09/2026.** La correction est apportée au générateur : le bloc « corrigé
enseignant » de `main()` ne recopie plus le plan d'injection, il relit les fichiers livrés après l'écriture et
recompte les dix valeurs — testé isolé sur les données actuelles, il reproduit exactement les valeurs que le
module cite (3 421 · 0 · 3 360 · 973 · 486 · 44 · 1 911 · 412 · 243 360 · 240 000). La version du socle livrée
dans l'atelier **conserve** la clé d'origine : elle est l'objet d'étude du point 12 de C01 et de l'exercice E4 de
l'évaluation, et c'est voulu. La prochaine régénération du socle (événement de release) produira le corrigé
mesuré, sans toucher aux chapitres.

## 2. Les six chapitres, une ligne chacun

| Chap. | Fichier | Ce qu'il installe | Figure | H |
|---|---|---|---|---|
| C01 | `M04_C01_diagnostic_en_douze_points.md` | la grille de 12 points, reproductible en 45 min sur un fichier inconnu ; l'échelle (un script, pas l'œil) ; le rapport de diagnostic comme livrable | 1 (la grille) | 6 |
| C02 | `M04_C02_absences_mecanismes_et_choix.md` | 5 mécanismes d'absence (non-applicable, non-collecté, non-répondu, perte à l'import, convention `0`/vide) ; 5 traitements ; `id_client = 0` n'est pas un manque | 1 | 5 |
| C03 | `M04_C03_doublons_cles_et_correspondances.md` | vrai/faux doublon, clé candidate, clé métier, dictionnaire de correspondance, appariement tolérant | 1 | 5 |
| C04 | `M04_C04_aberrantes_regles_de_controle.md` | seuils métier, IQR, z-score, règles croisées, le contrôle qui doit rendre une décision et non un nombre | 1 | 5 |
| C05 | `M04_C05_normaliser_rendre_comparable.md` | casse, accents, espaces, séparateurs de milliers, virgule de décimale, encodages, dates locales, découpage/fusion | 1 | 4 |
| C06 | `M04_C06_documenter_nommer_proteger.md` | arborescence, nommage, README de données, journal des transformations, contrôle de cohérence final, données personnelles et anonymisation | 1 | 5 |

Projet `M04.P` (`03_exercices/M04_projet.md`) : « le dossier de données » — six livrables sur 20, seuil 13, sur un
dossier volontairement pourri (7 défauts de natures différentes, dont les deux qui cassent les totaux : les 3 421
montants texte et les 3 360 lignes en collision). Évaluation (`04_evaluations/M04_evaluation.md`) : récupération
non notée, quiz 15 Q, 3 exercices dont un E4 « trois chiffres faux », étude de cas « le stock indiqué est-il
crédible ? » sur les 60 000 lignes de `stocks_quotidiens.csv`, grille qualité notée sur 20.

## 3. Les cinq règles héritées de la fiche de contrôle M03, appliquées ici dès le premier chapitre

1. **Une valeur attendue se mesure sur le fichier livré.** D'où le relevé ci-dessus, pris sur les fichiers, et non
   sur `rapport_defauts.json`.
2. **Un moteur tolérant n'est pas l'outil enseigné.** Dans M04, le piège s'appelle `pandas` : `read_csv` déduit
   les types ligne par ligne et avale « 3 421 montants texte » sans rien dire, là où Excel les laisse en texte.
   Chaque conversion publiée dans un chapitre est doublée d'un compteur d'échec (`errors="coerce"` + `isna().sum()`).
3. **Une mesure qui tombe en estimation sans le dire est fausse.** Le générateur de clés échoue bruyamment : si
   une mesure ne peut pas être faite, elle n'est pas publiée (et `autovalide` R2 refuse le nombre dans le chapitre).
4. **Un scan qui ne matche rien ment poliment.** Les compteurs du chapitre sont écrits pour imprimer leur dénominateur
   (3 440 sur 243 360), jamais le seul numérateur, et le contrôleur de figures imprime la largeur maximale observée.
5. **Le contrôle qui lit le fichier rendu est le seul qui prouve l'impression.** `tools/controle_pdf.py` s'appliquera
   au PDF de M04 comme à ceux de M01-M03 (figures retrouvées par leur libellé propre, glyphes composés).

Hygiène de production, rappel : ne pas persister le HTML de composition ni les instances de polices ; `pip install
--no-cache-dir` ; `python3 tools/poids.py --strict` à la fin de chaque module (quota 128 Mo, 70,4 Mo occupés à
l'ouverture de M04).

## 4. Ce que M04 ne fait pas (bornes héritées de l'architecture)

- **Pas de Power Query** (M05), **pas de SQL** (M05 en miroir, M07 le cours), **pas de Python de production** (M08) :
  les fragments `pandas` n'apparaissent que comme *contrepoids* mesurés, jamais comme procédure à reproduire. Le
  contrôleur `controle_python.py M04` doit donc rendre 0 bloc publié, comme en M03 — si un bloc s'y glisse, c'est
  qu'un chapitre a débordé.
- Pas de mise en place d'entrepôt ni de gouvernance outillée (M06, M17-M19) : M04 installe les **réflexes** et les
  artefacts texte (README, journal, dictionnaire), pas les outils.
- Aucun nombre de 4 chiffres et plus sans clé `m04_*`/`m02_*`/`m03_*` existante, aucun chemin cité sans existence
  vérifiée (R2, R4), aucune table de plus de 6 colonnes sans version courte (Q9).

## 5. État d'avancement et ordre d'exécution

**Fait le 18/09/2026.** Les 92 clés `m04_*` sont publiées et reproductibles (deux exécutions, `diff` nul). C01 est
rédigé : 16 blocs, 6 391 mots, 8 tableaux de 4 colonnes au plus, 5 exercices autonomes corrigés, `autovalide M04
--strict` muet. Sa planche `figures/M04_C01_diagnostic_en_douze_points.svg` est générée par `tools/figures_M04.py`
et auditée (extension maximale estimée 736 px pour 776 utiles). Rendu de contrôle : chapitre seul en **12 pages**
(calibre 12,5), `controle_pdf.py M04` → 1 figure sur 1 retrouvée par son libellé, 34 glyphes sur 34 composés, 0
défaut bloquant — le PDF de contrôle a été supprimé après mesure, le module n'étant pas achevé. `controle_sql.py
M04` et `controle_python.py M04` rendent 0 bloc, comme attendu pour un module tableur.

**Fait aussi le 18/09/2026, dans la même session.** C02 (absences) et C03 (doublons, clés, correspondances) sont
rédigés et validés : 135 clés `m04_*` publiées au total, reproductibles à l'octet près. Rendu des trois chapitres
ensemble : **34 pages** dont 12 pour C01 (mesuré seul), 3 planches sur 3 retrouvées dans le PDF par leur libellé,
37 glyphes sur 37 composés, 0 défaut bloquant — le PDF et le HTML de contrôle ont été supprimés après mesure, et les
instances de polices avec eux. Le module reste outillé tableur : `controle_sql.py M04` et `controle_python.py M04`
rendent 0 bloc.

**Fait encore le 18/09/2026, dans la même session.** C04 (valeurs aberrantes et règles de contrôle) et C05
(normaliser et rendre comparable) sont rédigés et validés : **206 clés `m04_*`** publiées, soit 34 de plus qu'à la
fin de C03, toutes mesurées sur les fichiers livrés et reproductibles (`diff` nul entre deux exécutions). Rendu des
cinq chapitres ensemble : **60 pages** soit 12,0 p./chapitre pour un calibre de 12,5 (M03 : 14,7), 5 planches sur 5
retrouvées dans le PDF par leur libellé, 46 glyphes sur 46 composés, 0 défaut bloquant ; `controle_formules.py` tient
à 123 contrôles conformes et 0 écart, `poids.py --strict` et `budget_pages.py --mesure` au vert (le contrôle de
budget du module est reporté à son achèvement). Le PDF et le HTML de contrôle ont été supprimés après mesure.

**Deux corrections apportées aux chapitres déjà validés, parce qu'une mesure les contredisaient.** (1) C01 §5.7 et
§5.8 : la réparation des 973 remises à 12, 18, 25, 30 n'est pas une division par 100 — testée, elle laisse 258
lignes hors du plafond contractuel et jusqu'à 377 634 FCFA de résidu ; le générateur injecte la valeur aberrante
*après* calcul des montants (génération_socle.py, lignes 334-338), donc **les montants sont justes et seule la
colonne de taux est fausse**, état qui se documente comme tel. (2) C03 §5.7 : l'anatomie des 412 doublons clients a
été réétablie sur les couples formés par la clé et non sur les homonymes — les quatre autres colonnes concordent dans
412 couples sur 412, les lignes retirées forment un bloc continu à partir de la ligne 23 501 et portent toutes les
deux anomalies d'écriture (0 ligne conservée ne les porte) ; le chiffre de 307 de concordance de ville, cité un
instant, mesurait autre chose. Une clé publiée a été retirée pour la même raison : `mois` à un chiffre dans
`objectifs_de_ca.csv` n'est pas un défaut de format mais l'écriture normale des mois 1 à 9.

**Reste, dans l'ordre :**

1. C01, C02, C03, C04, C05 ✔ (la grille de C01 sert aux cinq autres chapitres)
2. C06 (documenter, nommer, protéger) — seul chapitre encore à écrire
3. `M04_projet.md` (avec le dossier pourri généré par un `tools/dossier_M04.py` dédié, et son `ATTENDU` mesuré)
4. `M04_evaluation.md`
5. `controle_formules.py`/`controle_python.py`/`controle_sql.py` sur M04, `render.py --join`, `controle_pdf.py M04`,
   `fiche_controle_M04.md`, mise à jour du README

**Fait encore le 18/09/2026 (fin de module).** Le projet `03_exercices/M04_projet.md` et l'évaluation
`04_evaluations/M04_evaluation.md` sont rédigés et validés. Le projet tourne sur un dossier pourri généré par
`tools/dossier_M04.py` (graine 41, déterministe) : 160 lignes, 7 défauts de natures différentes, dont les deux qui
cassent les totaux (17 montants texte, 8 doublons dont 1 resaisie à la date), 9 groupes en collision dont 1
multi-ligne légitime qui doit survivre ; le `ATTENDU.json` du dossier est mesuré sur le dossier généré et publié
en 24 clés `m04p_*` (total réparé : 8 209 940 FCFA, 152 lignes). L'évaluation (2 h 30, quatre épreuves) reprend
les 15 questions du quiz, les quatre exercices dont E4 « les trois chiffres faux », et l'étude de cas « le stock
indiqué est-il crédible ? » sur les 60 000 lignes de `stocks_quotidiens.csv` (1 800 négatifs = exactement les
1 800 alertes ; 118 écarts au-dessus de 100 ; maximum 532 sur une moyenne de 2,77). La correction du
`rapport_defauts.json` est apportée au générateur (voir §1) ; le socle livré conserve la clé d'origine, objet
d'étude du module. État final : 8 fichiers du module autovalidés `--strict` (0 avertissement), 276 clés `m04_*`
publiées et reproductibles, 72 p. composées pour les six chapitres (12,0 p./chapitre, calibre 12,5), 6 planches
sur 6 et 46 glyphes sur 46 au contrôle du PDF de contrôle (supprimé après mesure).
