# Plan de production — module M05 (Chaîne de préparation : Power Query, SQL, pandas en miroir)

**5 chapitres · 30 h · niveau N2 · prérequis M04 · palier P1 · budget 5 × 12,5 + 17 p. d'appareil = 80 p.**
Source d'autorité : `00_architecture/01_architecture_pedagogique.md`, §« M05 » (l. 458-474).

## 1. Ce que le module doit produire, et sur quoi il travaille

M05 est le premier module du parcours où **la production est exécutée** : M01-M04 tournaient sur le tableur et le
système de fichiers (0 bloc SQL, 0 bloc Python publiés) ; ici, les chapitres C03 et C04 publient du SQL **exécuté
sur DuckDB 1,5,5** et du pandas **exécuté en Python 3,13 / pandas 2,2,3**, et le contrôleur de la porte Q3 les
relit. Le chapitre C02 (Power Query) reste **non exécutable** dans cet atelier (G.2 : pas d'Excel) : ses blocs M
sont des recettes signalées « non exécuté », avec points de contrôle manuels, et **chaque chiffre qu'ils
affirment est exécuté en SQL et en pandas sur les mêmes données** — c'est la règle qui rend le module honnête.

### 1.1 Le cas fil rouge : un mois de fichier du magasin, trois méthodes, un verdict

Le fil rouge du module (annonce de l'architecture : « 1 fichier → 3 méthodes → 3 livrables → 1 verdict
documenté ») est l'export mensuel de caisse du magasin, **mars 2025**, coupé à la date dans le `ventes_brutes.csv`
livré (aucun fichier d'extraits à fabriquer : la coupe est la première opération enseignée, refaite dans les
trois outils). L'enrichissement croise ce mois avec `remises_manuelles.xlsx`, le fichier tenu à la main par
l'assistante — la « fusion cauchemar » annoncée au §E.1, dont le piège est mesuré : à la bonne clé
(`id_client` × mois) 101 lignes de mars sont enrichies ; la jointure naïve sur `id_client` seul produit
**3 978 lignes, environ 39 fois trop**, sans aucune erreur affichée — c'est la leçon du module.

Le verdict (C05) se referme sur la **robustesse** : le même nettoyage rejoué sans modification sur avril 2025
(6 639 lignes) et mai 2025 (5 530), puis extrapolé au cas du million de lignes.

### 1.2 Les faits mesurés qui structurent le module

Mesurés le 19/09/2026 sur les fichiers livrés (jamais régénérés — décision §1.3). Ils seront publiés en clés
`m05_*` par une section `m05()` ajoutée à `chiffres_manuel.py` avant le premier chapitre.

| Mesure | Valeur | Chap. |
|---|---|---|
| `ventes_brutes.csv`, lignes par année | 60 106 (2023) · 65 873 (2024) · 70 345 (2025) · 47 036 (2026, janv.-août) | C05, projet |
| cas fil rouge (mars 2025, coupé à la date) : lignes | 6 884 (2025-03-01 → 2025-03-31) | C01-C04 |
| idem : total `montant_ttc` de la coupe brute (avant dédoublonnage), après conversion des textes | 464 096 003 FCFA | tous |
| idem : montants en texte (« … FCFA ») · doublons ressaisis (2ᵉ occurrence, hors `id_vente`) · remises > 1 · retours · clients inconnus | 114 · 86 · 32 · 74 · 10 | C02-C04 |
| idem : lignes enrichies à la bonne clé (`id_client` × mois) | 101 lignes (89 couples distincts), 11 620 000 FCFA au total par ligne (10 656 000 par couple) | C03, C04 |
| idem : jointure naïve sur `id_client` seul | 3 978 lignes (≈ 39 × l'enrichissement juste, 0 erreur affichée) | C03 |
| rejouabilité : avril 2025 · mai 2025 | 6 639 lignes · 5 530 lignes | C05 |
| `remises_manuelles.xlsx` | 18 200 lignes × 7 colonnes (558 846 octets) · 1 400 clients × exactement 13 mois · **0** couple (`client`,`annee`,`mois`) en double · total des montants 2 043 692 000 FCFA · 3 000 à 2 213 000 · 5 motifs · 3 `saisi_par` | C02, C03 |
| les 3 360 ressaisies injectées du brut | toutes en fin de fichier (lignes 240 000 → 243 359, `id_vente` 240 001 → 243 360), dates dispersées sur toute la période — une coupe à la date les contient donc **mêlées aux originaux** (mars 2025 : 86, cf. ligne du dessus) ; 3 321 copies exactes de la ligne d'origine (hors `id_vente`), 27 qui modifient aussi `taux_remise`, 12 qui modifient aussi `id_client` (→ 900xxx) ; à part : 6 répétitions intra-ticket *légitimes* dispersées (même ticket, même produit, heures différentes), dont 3 dans la fenêtre du projet — le dédoublonnage qui les retire a tort (leçon M04.C03 reprise) | C03, projet |
| dates mixtes annoncées par le corrigé enseignant / présentes dans le fichier livré | 2 640 / **0** (l'histoire d'E4 de M04, rappelée en un encadré, pas réenseignée — le mécanisme est désormais compris, cf. §1.4 et §5) | C01 |
| dates à mois et jour échangés dans le brut livré (anomalie héritée du socle) | 945 lignes sur tout le fichier, dont 493 dans la fenêtre — toutes détectables par la colonne `mois` (`mois(date_vente) ≠ mois`), toutes des transpositions pures (année cohérente sur 945/945), toutes réparables par transposition | C01, projet |
| fenêtre du projet : 120 000 premières lignes du fichier livré | 2023-01-01 → 2024-12-11 · total `montant_ttc` converti 7 145 910 735 FCFA · 1 710 montants texte · 482 remises > 1 · 247 clients inconnus (211 ids distincts, tous ≥ 900 000) · 1 485 retours · **0 doublon injecté** (tous en fin de fichier) | projet |
| fenêtre × remises (sous-ensemble ≤ 2024 : 9 907 lignes) | 1 371 des 1 400 clients de remises présents · enrichissement juste 1 714 lignes (986 clients) vs 41 716 (jointure naïve sur `id_client` seul, ≈ 24 ×) ; le 76 687 (≈ 45 ×) mesuré à l'ouverture était calculé sur le fichier complet de 18 200 lignes — corrigé ici | projet |

### 1.3 Décisions de corpus prises à l'ouverture

- **Le socle n'est pas régénéré.** `generation_socle.py` n'est pas relancé : la version livrée du
  `rapport_defauts.json` conserve ses clés d'origine (objet d'étude du point 12 de M04.C01 et de l'exercice E4) —
  décision du 18/09/2026 maintenue. M05 travaille sur les fichiers livrés tels quels.
- **La base DuckDB n'est pas un prérequis.** `data/sahel.duckdb` n'est pas persisté et ne sera pas reconstruit :
  la session du contrôleur `controle_sql.py` est **en mémoire**, donc le premier bloc SQL de C03 recrée les tables
  du dossier par `read_csv`/`CREATE TABLE AS` — la leçon « tout ce qui est nommé est créé avant » (fiche M01-M02)
  devient la leçon du chapitre.
- **Les extraits du cas fil rouge ne sont pas des fichiers livrés** : mars/avril/mai 2025 sont des coupes à la date,
  produites par l'apprenant comme première opération. Aucun nouveau fichier dans `data/` (les chiffres cités
  descendent de la mesure sur `ventes_brutes.csv` livré).
- **Le projet a son dossier généré** : `tools/dossier_M05.py` (graine 42, déterministe, même pattern que
  `dossier_M04.py`) écrit `03_exercices/dossier_M05/` — 4 fichiers — et un `ATTENDU.json` **mesuré sur le dossier
  généré**, publié en clés `m05p_*` (jamais déduit du plan d'injection : le défaut de M04.C01 point 12 est
  précisément cette confusion). Le `ATTENDU` est vérifié par deux moteurs indépendants (pandas puis DuckDB) avant
  publication, comme le fut le dossier M04.

### 1.4 Le projet M05.P — « Trois chemins, une même table propre » : le dossier et ses 9 défauts

`ventes_2023_2024.csv` (121 720 lignes = les 120 000 premières lignes du brut livré + 1 720 doublons
injectés en fin de fichier, `id_vente` nouveaux à partir de `300001`) ·
`remises_2023_2024.xlsx` (sous-ensemble ≤ 2024 de `remises_manuelles.xlsx` : 9 942 lignes + 2 lignes de
chapeau avant l'en-tête) ·
`clients.csv` (les 23 500 clients propres, écrits en cp1252) · et l'énoncé. Neuf défauts de natures différentes
(compteurs mesurés par le générateur sur le dossier écrit, publiés dans `ATTENDU.json`) :

1. `montant_ttc` en texte, espace-milliers + suffixe « FCFA » : 1 710 lignes héritées de la fenêtre (1 731 avec
   leurs 21 copies).
2. Doublons exacts ressaisis : N = 1 680 copies de lignes de la fenêtre, ajoutées en fin de fichier — le retrait
   se fait sur la clé métier, jamais sur la position : le piège d'`ATTENDU` de M04 refait en plus grand.
3. Doublons ressaisis à la date + 1 jour : K = 40 lignes (sources sans le 31/12 ; dans la copie, les colonnes
   `mois` et `annee` sont recalculées depuis la nouvelle date, pour que la copie soit auto-cohérente avec la
   règle de réparation) : la clé métier **sans** la date les attrape, celle qui l'inclut les laisse passer.
4. Remises saisies en points de % (12, 18, 25, 30) : 482 lignes héritées (488 avec leurs copies) : la convention,
   pas la valeur, est fausse.
5. `id_client` hors référentiel : 247 lignes héritées (211 ids distincts, tous ≥ 900 000) : la `LEFT JOIN` les
   laisse, la `INNER` les mange — le choix est noté, pas laissé au moteur.
6. P = 35 couples (`client`,`annee`,`mois`) en double dans le xlsx de remises (injectés) : la jointure explose si
   le dédoublonnage ne précède pas la fusion — c'est le 39 × de mars, version projet.
7. Deux lignes de chapeau avant l'en-tête du xlsx (l'export de l'assistante, comme le tarif fournisseur de M04).
8. `clients.csv` en **cp1252** (accents, 3 170 caractères hors ASCII) : les trois outils le lisent différemment
   sans y penser — la colonne `ville` du `df_final` est le contrôle.
9. Les retours (1 485 lignes à montants négatifs, 1 510 avec leurs copies) ne sont pas un défaut : le filtre
   naïf `montant_ttc > 0` qui les retire est le défaut. Quatre des neuf cassent un total si on y va à l'œil —
   les textes que `SOMME` rate (1), les doublons qu'on compte deux fois (2 et 3), la jointure qui explose (6),
   les retours qu'on omet (9) — et le rapport qualité du projet (réinvestissement de M04.P) doit les compter
   chacun.

**Clé de dédoublonnage (mesurée) :** (`id_ticket`, `id_produit`, `quantite`, `montant_ttc`, `heure`) — avec
l'heure : 0 collision dans la fenêtre ; sans elle : 6 lignes en 3 groupes, qui sont des répétitions intra-ticket
*légitimes* (même ticket, même produit, deux lignes à des heures différentes) — la clé à 4 colonnes les mangerait
(`lignes_legitimes_mangees_cle_sans_heure` = 3 dans `ATTENDU.json`). On garde le plus petit `id_vente`.

**Anomalie héritée, documentée, non comptée comme un 10ᵉ défaut :** le brut livré contient 945 dates à mois et
jour échangés (résidu des 2 640 dates « dd/mm » injectées par le socle : les 1 695 à jour > 12 ont été
re-parsées correctement par fallback day-first, les autres sont sorties en ISO mais à la mauvaise valeur). Dans
la fenêtre : 493 lignes, toutes détectables (`mois(date_vente) ≠ mois`), toutes réparables par transposition
(année cohérente sur 493/493). La spécification de `df_final` **inclut la réparation** : si
`mois(date_vente) ≠ mois`, échanger jour et mois, année inchangée. L'erratum M04 (E4) en est la conséquence,
consignée au §5.

**Chiffres mesurés sur le dossier écrit** (`ATTENDU.json`, vérifié à deux moteurs — pandas puis DuckDB — mêmes
lignes, mêmes sommes, même empreinte, sinon le générateur échoue) :

| Mesure | Valeur |
|---|---|
| `df_final` : lignes · total `montant_ttc` | 120 000 · 7 145 910 735 FCFA |
| total avant dédoublonnage (les copies comptées deux fois) | 7 242 884 579 (excès 96 973 844) |
| total avec le filtre naïf `montant_ttc > 0` (retours omis) | 7 233 404 102 (excès 87 493 367) |
| autres totaux de `df_final` : `quantite` · `montant_ht` · `montant_tva` | 787 318 · 6 055 856 518 · 1 090 054 217 |
| lignes enrichies (clé complète) · total `remise_consentie_montant` | 1 714 · 201 682 000 |
| jointure naïve sur `id_client` seul · clé complète sans dédoublonnage préalable des remises | 41 716 lignes (≈ 24 ×) · 1 723 lignes (+9) |
| `ville` NULL dans `df_final` | 21 890 (= 21 643 lignes comptoir `id_client` = 0 + 247 clients inconnus) |
| xlsx de remises : lignes brutes · couples en double · après dédoublonnage | 9 942 · 35 · 9 907 |

**Livrables de M05.P** (grille /20, seuil 13) : requête Power Query, script SQL, notebook pandas — les trois
produisant un `df_final` **identique au centime près** : ventes de la fenêtre dédoublonnées (clé du §1.4),
`montant_ttc` entier, `date_vente` ISO **avec les transpositions réparées** (règle du §1.4), colonne
`remise_consentie_montant` (NULL si aucune remise, vide à l'export CSV), colonne `ville` issue des clients cp1252. Le contrôle automatisé fourni (compteur de lignes, sommes par colonne, empreinte
des lignes triées au format canonique) est celui de l'`ATTENDU.json` du dossier. Le rapport qualité de M04.P est
réinvesti comme cinquième livrable mis à jour (cumulativité des projets, §E.3).

## 2. Les cinq chapitres, une ligne chacun

| Chap. | Fichier | Ce qu'il installe | Figure | H |
|---|---|---|---|---|
| C01 | `M05_C01_le_langage_commun_des_transformations.md` | les 10 opérations avec leur nom dans les 4 outils (tableau Power Query — SQL — pandas — Excel) ; la coupe de mars 2025 comme première opération refaite trois fois ; la promesse « même total, trois moteurs » et son contrôle | 1 (le schéma 1 fichier → 3 méthodes → 1 table) | 5 |
| C02 | `M05_C02_power_query_sources_etapes_types.md` | source, étapes, types, dépivotage, fusion, agrégation, requêtes paramétrées (le paramètre « mois » = la robustesse au fichier du mois suivant), M sans complexe ; le « ETL du pauvre, le plus rentable du parcours » | 1 (l'anatomie d'une requête : les étapes) | 7 |
| C03 | `M05_C03_sql_pour_transformer.md` | `CREATE TABLE AS`, `INSERT…SELECT`, `WITH`, nettoyage dans la requête (`TRY_CAST`, `TRIM`, dédoublonnage par rang), la jointure à la clé complète contre la jointure à la clé partielle, chargement en base | 1 (le pipeline base → table propre) | 7 |
| C04 | `M05_C04_pandas_pour_transformer.md` | chaîne de transformations, `pipe`, `assign`, `query`, `melt`/`pivot`, `merge`, `groupby` ; le notebook du fil rouge exécuté et sa sortie imprimée ; pandas 2,2,3 de l'atelier, 3.x du manuel, les divergences signalées | 1 (la chaîne lue de haut en bas) | 7 |
| C05 | `M05_C05_arbitrer_un_outil_par_situation.md` | tableau de décision « taille × fréquence × compétences × gouvernance → outil » ; les temps mesurés sur 3 tailles réelles (6 884 / 120 000 / 243 360 lignes) ; le cas du million de lignes ; dire « non » à Excel, « pas encore » à Python ; le verdict du fil rouge (temps, robustesse avril/mai, lisibilité) | 1 (la grille de décision) | 4 |

**Les 10 opérations de C01** (sélection/renommage de colonnes, conversion de type, nettoyage de texte, filtre,
tri, dédoublonnage, colonne calculée, jointure, agrégation, pivot/dépivot) : l'architecture annonce « vos 12
opérations » au sommaire et « 10 opérations » au chapitre — le recensement retenu est la table des 10 opérations
du chapitre, **import et export étant les deux opérations-cadres** traitées dans chaque chapitre d'outil :
10 + 2 = les 12 de l'énoncé d'origine. Les six primitives nommées dans les objectifs du module (importer,
pivoter/dépivoter, fusionner, agréger, créer une colonne, charger) sont toutes dans ce recensement.

**Projet** `M05.P` : voir §1.4. **Évaluation** (`04_evaluations/M05_evaluation.md`) : quiz 15 Q ; 2 exercices par
outil (6 au total — les SQL et pandas sont auto-validés par script, les Power Query par résultat attendu chiffré) ;
étude de cas « on me donne 8 Go de logs » (grille /20, seuil 12) ; corrigés. Porte de niveau N2 : « nettoyage livré
avec rapport qualité » — le projet la porte.

## 3. Les règles héritées des fiches de contrôle, appliquées dès le premier chapitre

Les cinq de la fiche M03, sans changement de fond :

1. **Une valeur attendue se mesure sur le fichier livré.** D'où le relevé du §1.2 pris sur les fichiers, et
   l'`ATTENDU.json` du dossier projet mesuré sur le dossier généré (pas sur le plan d'injection).
2. **Un moteur tolérant n'est pas l'outil enseigné.** En M05, les moteurs tolérants s'appellent
   `read_csv_auto` (DuckDB déduit les types et avale 1 710 montants texte sans un mot) et `read_csv` de pandas
   (idem, `dtype` déduit). Chaque conversion publiée est doublée d'un compteur d'échec :
   `errors="coerce"` + `isna().sum()` en pandas, `TRY_CAST` + comptage des NULL en SQL — le compteur est affiché
   dans la sortie, jamais la seule valeur.
3. **Une mesure qui tombe en estimation sans le dire est fausse.** Le générateur du dossier échoue bruyamment si
   une mesure n'est pas possible ; les temps de C05 sont mesurés sur les trois tailles réelles, l'extrapolation au
   million de lignes est étiquetée « extrapolation linéaire, à vérifier » — jamais publiée comme mesure.
4. **Un scan qui ne matche rien ment poliment.** Le contrôle du `df_final` imprimé affiche le dénominateur
   (lignes attendues, sommes par colonne, empreinte) et non seulement le verdict « identique ».
5. **Le contrôle qui lit le fichier rendu est le seul qui prouve l'impression.** `controle_pdf.py M05` comme pour
   M01-M04 ; et, nouveauté de la série, le contrôle du projet **lit les trois sorties des trois moteurs** et les
   compare entre elles, pas seulement à l'`ATTENDU`.

Ajoutées pour M05 :

6. **Un bloc SQL publié sans sa vue est un défaut** (fiche M01-M02) : la session du contrôleur est en mémoire et
   vide, donc tout ce qu'un bloc nomme est créé par un bloc publié antérieur — le premier bloc de C03 recrée les
   tables du dossier par `read_csv`. Les blocs abrégés (contenant `…`) sont sautés par le contrôleur : usage
   rare et signalé dans le texte.
7. **Un bloc M est une recette, pas une exécution.** Signalé « non exécuté » avec ses points de contrôle manuels
   (3 par bloc au plus) ; tout chiffre qu'il affiche est publié en clé `m05_*` mesurée en SQL/pandas sur les mêmes
   données, et le lecteur est renvoyé à ces deux voies pour vérifier.
8. **Un bloc Python publié est exécuté dans un espace de noms partagé** (préambule `controle_python.py` : `pd`,
   `np`, `stats` (scipy), `RACINE`, `df`, `pop`) : un bloc qui s'appuie sur une variable définie deux pages plus
   haut est légitime (c'est le geste de l'apprenant) ; aucune variable en dehors du préambule et des blocs
   précédents.
9. **pandas 2,2,3 dans l'atelier, 3.x dans le manuel** (D11) : chaque pattern publié est testé sur 2,2,3 ; là où
   3.x diffère, un encadré « migration » le dit — sans enseigner la migration (c'est l'annexe de M08). Les
   écritures obsolètes ne sont pas reproduites, sauf dans les encadrés qui les condamnent.

## 4. Ce que M05 ne fait pas (bornes héritées de l'architecture)

- **Pas de cours de SELECT** : le vocabulaire de requête de base (`SELECT`, `WHERE`, `GROUP BY`) a déjà été exécuté
  en M02 (9 blocs DuckDB) ; M05 l'emploie comme outil de transformation (`CREATE TABLE AS`, `WITH`, jointures
  minimales `INNER`/`LEFT` à la clé complète). Le cours complet — `HAVING`, `CASE`, sous-requêtes, les 4 symptômes
  de l'explosion de jointures — est M07 ; chaque usage de M05 y renvoie sans redire.
- **Pas de cours de Python** : M08 reconstruit le langage depuis zéro (variables, boucles, fonctions). C04 est
  écrit en recettes sur `DataFrame` — chaque bloc est copiable et exécutable tel quel, la syntaxe du langage est
  expliquée au minimum vital, et le « comment Python fonctionne » est explicitement reporté à M08.
- **Pas d'optimisation** (index, `EXPLAIN`, plans d'exécution) : M11.C06, comme décidé en H.3-2.
- **Pas d'entrepôt, de data lake, de gouvernance outillée** : M06 et M17. M05 installe la préparation reproductible,
  pas l'architecture.
- **Pas de Power BI** : M14. Le Power Query de M05 est celui d'Excel, version de référence Microsoft 365 courant
  (septembre 2026), déclarée comme en M03 ; LibreOffice n'a pas de Power Query (C.5) — un encadré de C02 le dit et
  donne le plan B (Power Query Desktop gratuit, et la voie SQL/pandas du module pour l'attente).
- **Pas de 1 000 000 de lignes fabriquées** : le « cas du million » de C05 est une extrapolation étiquetée depuis
  les mesures sur 6 884 / 120 000 / 243 360 lignes réelles.
- Aucune table de plus de 6 colonnes sans version courte (Q9), aucun nombre de 4 chiffres et plus sans clé
  `m05_*`/`m05p_*` (R2), 16 blocs du gabarit (R1), encadrés dans les quotas (R8), 5 planches SVG auditées comme
  les précédentes (≤ 776 px, jeu de signes latin-1 étendu, pas de `≤`).

## 5. État d'avancement et ordre d'exécution

**Écarts ouverts hérités de M01-M04, publiés ici comme le demande la porte §G.1** (transparence de production) :

1. **Q10, test de lecture « débutant simulé »** — commun aux fiches M01-M04, programmé à l'étape 4 sur le texte
   assemblé. M05 s'y ajoute.
2. **Glossaire et index FR/EN** — non-redondance contrôlée dans chaque module, contrôle inter-modules reporté à
   l'étape 4 (le glossaire n'existe pas avant l'assemblage).
3. **Pagination des signets** — le `/Count` de `nb_pages.py` excède la pagination imprimée sur M01-M04
   (artefact de la table des matières interne) ; à trancher à l'assemblage.
4. **Calibre** — M03 compose 14,7 p./chapitre (M04 : 12,0) ; les deux sont dans la fourchette 10-16, décision
   reportée.
5. **Fiche de contrôle M04 non publiée.** La porte M04 a été passée et son état final est consigné
   (`plan_M04.md` §5, README), mais il n'existe pas de `fiche_controle_M04.md` à côté des deux premières —
   l'écart est posé ici, sa tranche reportée à l'étape 6 (revue finale), où les fiches seront passées en
   ensemble.
6. **Ce que l'atelier ne peut pas exécuter : Excel, LibreOffice, Power BI — et désormais Power Query (M).**
   Conséquence M05 : règle 7 du §3 (blocs M recettes, chiffres exécutés ailleurs).
7. **Erratum M04, exercice E4 (précision, pas refonte).** M04 avait consigné « 2 640 dates de format mixte
   annoncées par le corrigé enseignant, 0 dans le fichier livré ». Le mécanisme est compris depuis le 19/09/2026
   (mesures `scratch2/dev1-dev7.py` avant le dossier) : le socle a bien injecté 2 640 dates « dd/mm » ; dans le
   fichier livré, les 1 695 à jour > 12 ont été re-parsées correctement par fallback day-first et 945 (jour ≤ 12)
   sont sorties en ISO mais à la **mauvaise valeur**, mois et jour échangés (année cohérente sur 945/945,
   transpositions pures). Le fichier ne contient donc pas « zéro défaut de date » : il contient 945 défauts de
   date **invisibles à un contrôle de format** — c'est précisément pourquoi E4 les avait ratés. Les modules M01-M04 sont clos et publiés : rien n'est réédité ; la
   précision est portée par le projet M05 (dont la spécification répare les 493 de la fenêtre) et reprise en
   revue finale (étape 6), quand la fiche M04 manquante (écart 5) sera passée en ensemble avec les autres.

**Fait le 19/09/2026 (ouverture).** Plan posé ; faits du §1.2 mesurés sur les fichiers livrés (pandas 2,2.3,
lecture des 243 360 lignes et du xlsx de remises) ; environnement vérifié : DuckDB 1,5,5 réinstallé et fonctionnel
(non persisté, `pip install --no-cache-dir duckdb` en tête de chaque session de production),
`nbclient` + `ipykernel` exécutent un notebook dans l'atelier (testé : pandas + duckdb importés dans une cellule),
`openpyxl` 3,1,5 lit le xlsx. Socle non régénéré (§1.3).

**Reste, dans l'ordre :**

1. ~~`tools/dossier_M05.py` (graine 42) : le dossier du projet (4 fichiers, §1.4), les compteurs exacts des 9
   défauts mesurés et consignés au §1.4, `ATTENDU.json` mesuré sur le dossier généré et vérifié par deux moteurs
   indépendants avant publication.~~ — **fait le 19/09/2026** : dossier écrit (121 720 + 9 942 + 2 chapeau +
   23 500 lignes), compteurs mesurés et consignés au §1.4, `ATTENDU.json` vérifié pandas/DuckDB (mêmes lignes,
   mêmes sommes, même empreinte).
2. ~~Section `m05()` dans `chiffres_manuel.py` (clés du §1.2 + coupe mars/avril/mai + jointures) et lecture de
   l'`ATTENDU` en clés `m05p_*` ; deux exécutions, `diff` nul.~~ — **fait le 19/09/2026** : 87 clés
   (`m05_*` 56 + `m05p_*` 31), la spécification `df_final` recalculée dans `m05()` et confrontée à
   l'`ATTENDU.json` (échec bruyant en cas d'écart), deux exécutions `diff` nul (990 clés au total).
3. ~~C01 (la table des 10 opérations sert aux quatre autres chapitres) → C02 → C03 → C04 → C05, autovalidation
   `autovalide.py M05 --strict` après chaque chapitre ; `controle_sql.py M05` après C03 (avec `--verif` sur le
   total du `df_final`), `controle_python.py M05` après C04 ; les blocs M de C02 ne sont pas testables : leur
   vérification est la concordance des clés `m05_*`.~~ — **C01 à C05 faits le 19/09/2026** :
   `02_modules/M05_C0{1..5}_*.md` (5 fichiers, ~13–17 p. chacun, total ≈ 75 p.) —
   `autovalide.py M05 --strict` **0 erreur, 0 avertissement** sur les 5 chapitres, quotas R8 respectés
   (4 Définition par chapitre, 2 Attention, 3 À retenir, 2 Conseil, 2 Dans les faits, 1 Boîte à outils) ;
   tous les chiffres de 4 chiffres et plus sourcés en clés `m05_filrouge_mars_*` ou reformulés.
   `controle_sql.py M05` rend **11 requêtes exécutées, 0 erreur** (mars = 6 884 l., v6 dédoublonnage = 6 798 l.) ;
   `controle_python.py M05` rend **15 fragments exécutés, 0 défaut** (notebook 8 cellules C04, verdict sha256
   identique au DuckDB). Poussés sur `main` : C01 → `90d79af`, C02 → `fe001a5`, C03 → `55ca57a`, C04 → `26cba3b`,
   C05 → `6bdcffa`.
4. `M05_projet.md` (barème sommant 20, seuil 13) et `M05_evaluation.md` (quiz 15 Q, 2 exercices par outil, étude
   de cas 8 Go, corrigés).
5. ~~`tools/figures_M05.py` (5 planches auditées), `render.py "0[234]*/M05_*.md" --join` → `M05.pdf`
   (budget 80 p., tolérance ±15 %), `controle_pdf.py M05`, `fiche_controle_M05.md` (Q1-Q10 + écarts), mise à jour
   du README et de ce plan, `poids.py --strict` (quota 128 Mo).~~ — **fait le 19/09/2026** :
   5 planches SVG (`M05_C0{1..5}_*.svg`, `extension maximale 769 px, 0 débordement, 0 glyphe hors jeu`) ;
   `M05.pdf` rendu via `--join` (5 fichiers joints, 751 Ko, **86 p.** — budget 80 ±15 % = 68-92, **OK**) ;
   `controle_pdf.py M05` rend `0 défaut bloquant, 33/33 glyphes composés` ;
   `fiche_controle_M05.md` rédigée (Q1-Q10, 9/10 au vert, 5 écarts déclarés) ; `plan_M05.md` mis à jour ;
   contrôle `poids.py --strict` à passer à l'étape 7.
