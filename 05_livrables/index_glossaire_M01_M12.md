# Index et glossaire — *La Voie des Données*, modules M01 à M12

**Appareil du livre.** Tous les chiffres de ce fichier sont mesurés sur le dépôt par
`tools/kit_exploitation.py` et consignés dans `05_livrables/kit_M01_M12.json` : rien n'est
recopié à la main, rien ne peut être en retard sur le texte.

---

## 1. Les douze modules

| Module | Titre | Chapitres | Heures | Pages | Mots | Exercices | Prérequis |
|---|---|---|---|---|---|---|---|
| **M01** | Lire les données, comprendre le métier | 7 | 30 | 117 | 46 261 | 37 | aucun |
| **M02** | Statistiques appliquées, depuis zéro | 8 | 30 | 122 | 53 806 | 40 | M01 |
| **M03** | Excel pour l'analyse de données | 8 | 30 | 126 | 56 023 | 43 | M01, M02 |
| **M04** | Qualité, préparation, documentation | 6 | 30 | 92 | 41 751 | 29 | M02, M03 |
| **M05** | Chaîne de transformation (M/Q, SQL, pandas) | 5 | 30 | 86 | 35 750 | 20 | M03, M04 |
| **M06** | Bases de données relationnelles | 5 | 30 | 69 | 28 009 | 20 | M04 |
| **M07** | SQL : interroger, agréger, rejoindre | 8 | 30 | 109 | 40 084 | 63 | M06 |
| **M08** | Python pour l'analyse de données | 8 | 30 | 119 | 47 406 | 39 | M05, M07 |
| **M09** | Analyse exploratoire (EDA) | 6 | 30 | 82 | 36 747 | 12 | M02, M08 |
| **M10** | Data visualization | 7 | 30 | 106 | 52 663 | 14 | M09 |
| **M11** | SQL avancé pour la BI | 7 | 30 | 97 | 39 363 | 14 | M07, M08 |
| **M12** | Fondamentaux de la Business Intelligence | 6 | 30 | 82 | 31 389 | 35 | M09, M10 |
| | **Total M01 à M12** | **81** | **360** | **1207** | **509 252** | **366** | |

Le détail chapitre par chapitre, avec les numéros de page du livre assemblé, se trouve
dans le sommaire des trois premières pages de `La_Voie_des_Donnees_M01-M12.pdf`.

---

## 2. Index des notions

Les termes listés sont ceux du bloc « Vocabulaire essentiel » de chaque chapitre : la liste
des mots que le manuel définit lui-même, et où. Un terme cité dans plusieurs chapitres
n'est pas un défaut — c'est un terme qu'on revoit.

- **`#N/A` — not available** — M03.C0
- **`#PROPAGATION!` — #SPILL!** — M03.C0
- **`.backup`** — M06.C0
- **`:memory:`** — M06.C0
- **`assign` — assign** — M05.C0
- **`BIGINT`** — M06.C0
- **`BOOLEAN`** — M06.C0
- **`CHECK`** — M06.C0
- **`COPY ... TO`** — M05.C0
- **`COUNTWHERE … IS NULL`** — M05.C0
- **`CREATE TABLE AS`** — M05.C0
- **`DATE`** — M06.C0
- **`DEFAULT`** — M06.C0
- **`drop_duplicates` — drop_duplicates** — M05.C0
- **`dtype` — dtype** — M05.C0
- **`EXPORT DATABASE`** — M06.C0
- **`EXTRACT`** — M05.C0
- **`GROUP BY`** — M05.C0
- **`groupby` — groupby** — M05.C0
- **`INSERT…SELECT`** — M05.C0
- **`INTEGER`** — M06.C0
- **`LEFT JOIN`** — M05.C0
- **`MATCH FULL` / `MATCH SIMPLE`** — M06.C0
- **`melt` — melt** — M05.C0
- **`merge` — merge** — M05.C0
- **`NOT NULL`** — M06.C0
- **`ON DELETE`** — M06.C0
- **`ON UPDATE`** — M06.C0
- **`pg_dump`** — M06.C0
- **`pgAdmin`** — M06.C0
- **`pip install`** — M06.C0
- **`pipe` — pipe** — M05.C0
- **`pivot_table` — pivot_table** — M05.C0
- **`PRIMARY KEY`** — M06.C0
- **`psql`** — M06.C0
- **`query` — query** — M05.C0
- **`read_csv_auto`** — M05.C0
- **`read_csv` — read_csv** — M05.C0
- **`REFERENCES`** — M06.C0
- **`ROW_NUMBEROVER`** — M05.C0
- **`STRPTIME` / `STRftime`** — M05.C0
- **`TEXT`** — M06.C0
- **`to_csv` / `to_parquet` — to_csv / to_parquet** — M05.C0
- **`TRY_CAST`** — M05.C0
- **`UNIQUE`** — M06.C0
- **`WITH`** — M05.C0
- **Actualiser tout — Refresh All** — M03.C0, M05.C0
- **Actualité — Timeliness / Currency** — M04.C0
- **Additivité — additivity** — M02.C0
- **Adresse absolue / relative — absolute / relative reference** — M03.C0
- **agrégat** — M07.C0
- **agrégat conditionnel** — M11.C0
- **Agrégat conditionnel — conditional aggregate** — M03.C0
- **Agrégat — aggregate** — M03.C0
- **alias de colonne** — M07.C0
- **alias de table** — M07.C0
- **ancienneté** — M11.C0
- **AND** — M07.C0
- **annotation** — M10.C0
- **année sur année** — M11.C0
- **anomalie** — M09.C0
- **anomalie structurelle** — M09.C0
- **Anonymisation** — M04.C0
- **Anonymisation / pseudonymisation** — M01.C0
- **Aplatir — flatten** — M01.C0
- **Appariement tolérant — Fuzzy matching** — M04.C0
- **appel à la décision** — M10.C0
- **Arborescence — tree** — M01.C0
- **arbre de choix** — M10.C0
- **Arrondi d'affichage — display rounding** — M03.C0
- **Arrondi — rounding** — M01.C0
- **ASC** — M07.C0
- **audit** — M09.C0
- **AVG** — M07.C0
- **axe de temps** — M11.C0
- **balayage séquentiel** — M11.C0
- **Barre de formule — formula bar** — M03.C0
- **BETWEEN x AND y** — M07.C0
- **BI analyst — analyste décisionnel** — M01.C0
- **Biais de cadrage** — M01.C0
- **Booléen — boolean** — M01.C0
- **Borne exclusive — exclusive bound** — M03.C0
- **borne métier** — M09.C0
- **bruit** — M09.C0
- **Cadrage — scoping** — M01.C0
- **cadre de fenêtre** — M11.C0
- **canal perceptuel** — M10.C0
- **Cardinalité — cardinality** — M01.C0, M02.C0
- **CASE** — M07.C0, M07.C0
- **Cellule — cell** — M01.C0, M03.C0
- **Centre — measure of central tendency** — M02.C0
- **Champ Valeurs — Values field** — M03.C0
- **Chapeau / pied de page — preamble / footer** — M01.C0
- **chapeau de figure** — M10.C0
- **Chaîne de caractères — string** — M01.C0
- **Chaîne de valeur — value chain** — M01.C0
- **Chemin — path** — M01.C0
- **Chronologie — Timeline** — M03.C0
- **cinq secondes** — M10.C0
- **cité** — M10.C0
- **classement à égalité** — M11.C0
- **Classeur — workbook** — M03.C0
- **client non identifié** — M11.C0
- **client-serveur** — M06.C0
- **Clé candidate — Candidate key** — M04.C0
- **Clé composite — composite key** — M03.C0
- **Clé d'homonymie** — M04.C0
- **clé de départage** — M11.C0
- **clé de jointure** — M07.C0
- **Clé de jointure — Join key** — M05.C0
- **Clé de normalisation — Normalized key** — M04.C0
- **clé de regroupement** — M07.C0
- **Clé métier — Business key** — M04.C0, M04.C0, M05.C0
- **Clé primaire — primary key** — M01.C0, M04.C0
- **Clé étrangère — foreign key** — M01.C0
- **Clé — key** — M03.C0
- **COALESCE** — M07.C0
- **code de sortie** — M11.C0
- **Coercition — coercion / type casting** — M03.C0
- **cohorte** — M11.C0
- **Cohérence — Consistency** — M04.C0
- **Colonne calculée — Calculated column** — M05.C0
- **Colonne mixte — mixed column** — M03.C0
- **Colonne — column / field / variable** — M01.C0
- **Complétude — Completeness** — M04.C0
- **comptage conditionnel** — M07.C0, M07.C0
- **Compétences — Skills** — M05.C0
- **conclusion provisoire** — M09.C0
- **Conformité — Conformity** — M04.C0
- **Connaissance — insight** — M01.C0
- **Contexte de filtre — Filter context** — M03.C0
- **contrôle croisé** — M11.C0
- **Contrôle croisé — Cross-field rule** — M04.C0
- **Contrôle de cohérence final** — M04.C0
- **Convention de nommage** — M04.C0, M11.C0
- **Conversion / coulage — cast** — M01.C0
- **corrélation** — M09.C0
- **corrélé** — M07.C0
- **COUNT** — M07.C0, M07.C0
- **coupe croisée** — M07.C0
- **Coupe à la date — Date filter** — M05.C0
- **coût du `SELECT *`** — M11.C0
- **Critère de réussite** — M01.C0
- **Critère — criteria** — M03.C0
- **CROSS JOIN** — M07.C0
- **cumul** — M11.C0
- **cumul de pourcentages** — M10.C0
- **Cycle de vie — lifecycle** — M01.C0
- **Data analyst** — M01.C0
- **Data engineer — ingénieur données** — M01.C0
- **Data scientist — scientifique des données** — M01.C0
- **DataFrame — DataFrame** — M05.C0
- **densité** — M10.C0
- **DESC** — M07.C0
- **Diagnostic de qualité — Data profiling** — M04.C0
- **Dictionnaire de correspondance — Crosswalk** — M04.C0
- **Dictionnaire de données — data dictionary** — M01.C0
- **Discrète / continue — discrete / continuous** — M01.C0
- **distance Lab** — M10.C0
- **DISTINCT** — M07.C0
- **Donnée brute — raw data** — M01.C0
- **Donnée de référence — master data** — M01.C0
- **Donnée non structurée — unstructured** — M01.C0
- **Donnée semi-structurée — semi-structured** — M01.C0
- **Donnée structurée — structured data** — M01.C0
- **Donnée — data** — M01.C0
- **Dossier — folder / directory** — M01.C0
- **double axe** — M10.C0, M10.C0
- **double négation** — M07.C0
- **Doublon — duplicate row** — M03.C0
- **dpi** — M10.C0
- **décalage** — M11.C0
- **Décision** — M01.C0
- **déclaration** — M10.C0
- **Dédoublonnage — Deduplication** — M04.C0, M05.C0
- **Dépivoter — Unpivot Columns** — M05.C0
- **Développer — Expand** — M05.C0
- **Effectif — count / frequency count** — M02.C0
- **effet 3D** — M10.C0
- **ELSE** — M07.C0
- **Empreinte — checksum / hash** — M01.C0
- **Empreinte— Hash fingerprint** — M05.C0
- **en-tête de requête** — M11.C0
- **En-tête — header** — M01.C0
- **encodage** — M10.C0
- **Encodage — character encoding** — M01.C0
- **Encodage — encoding** — M01.C0
- **Erreur — Error** — M05.C0
- **Estimation — Estimate** — M05.C0
- **ET logique entre conditions — implicit AND** — M03.C0
- **ex æquo** — M11.C0
- **Exactitude — Accuracy** — M04.C0
- **EXISTS** — M07.C0
- **explosion de jointure** — M07.C0
- **export figé** — M10.C0
- **Expression SQL — SQL expression** — M05.C0
- **Extension — extension** — M01.C0
- **famille de produits** — M11.C0
- **Faux anonymisage** — M04.C0
- **Faux négatif silencieux — Silent false negative** — M04.C0
- **Faux positif / faux négatif** — M04.C0
- **fenêtre** — M11.C0
- **Fermer et charger — Close & Load** — M05.C0
- **Feuille — sheet** — M03.C0
- **fiche d'entrée** — M09.C0
- **Fiche de diagnostic — Data quality report** — M04.C0
- **fichier `.duckdb`** — M06.C0
- **fichier `.sqlite`** — M06.C0
- **fil rouge** — M10.C0
- **Filtre automatique — AutoFilter** — M03.C0
- **fonction de fenêtre** — M11.C0
- **Fonction volatile — volatile function** — M03.C0
- **Format** — M01.C0
- **Format de nombre — number format** — M03.C0
- **Format nombre — number format** — M01.C0
- **Format personnalisé — custom format** — M03.C0
- **Formule volatile — volatile** — M03.C0
- **FROM** — M07.C0
- **fréquence** — M11.C0
- **Fréquence — Frequency** — M05.C0
- **Fréquence — relative frequency** — M02.C0
- **FULL OUTER JOIN** — M07.C0
- **Fusionner — Merge** — M05.C0
- **Glissement — rolling window** — M03.C0
- **Gouvernance — Governance** — M05.C0
- **grain** — M11.C0
- **Grain — granularity** — M01.C0
- **Graine — random seed** — M05.C0
- **graphique natif** — M10.C0
- **graphique trompeur** — M10.C0, M10.C0
- **GROUP BY** — M07.C0
- **groupe** — M07.C0
- **HAVING** — M07.C0
- **hiérarchie visuelle** — M10.C0
- **Identifiant direct** — M04.C0
- **Impossible — Invalid** — M04.C0
- **Imputation — Imputation** — M04.C0
- **IN** — M07.C0
- **index** — M11.C0
- **indicateur de regroupement** — M11.C0
- **Indicateur — KPI** — M01.C0
- **Individu — statistical unit / record** — M02.C0
- **Information** — M01.C0
- **INNER JOIN** — M07.C0
- **insight** — M10.C0
- **Invraisemblable — Implausible** — M04.C0
- **IS NULL** — M07.C0
- **jeu de tests** — M11.C0
- **Jeu figé — frozen dataset** — M01.C0
- **jointure en étoile** — M07.C0
- **jointure externe** — M11.C0
- **Jointure — Join** — M05.C0
- **joker `%`** — M07.C0
- **Jour ouvré — business day** — M03.C0
- **Journal de transformation — transformation log** — M01.C0
- **Journal des transformations** — M04.C0
- **Journal — log** — M01.C0
- **lecture en 60 secondes** — M10.C0
- **LEFT JOIN** — M05.C0, M07.C0
- **Licite surprenante — Legitimate extreme** — M04.C0
- **Ligne d'eau — watermark** — M01.C0
- **ligne de synthèse** — M07.C0
- **Ligne de total — totals row** — M03.C0
- **Ligne — row / record** — M01.C0
- **LIKE** — M07.C0
- **LIMIT** — M07.C0
- **liste** — M11.C0
- **Liste d'étapes — Step list** — M05.C0
- **Liste déroulante — drop-down list** — M03.C0
- **Livrable — deliverable** — M01.C0
- **légende** — M09.C0
- **manquant** — M09.C0
- **Marqueur de manque — Missing indicator** — M04.C0
- **matrice de rétention** — M11.C0
- **matérialisation** — M11.C0
- **Mesure — Measure** — M03.C0
- **MIN / MAX** — M07.C0
- **Minimisation — data minimisation** — M01.C0
- **Minimum / Maximum** — M02.C0
- **Mise en forme conditionnelle — conditional formatting** — M03.C0
- **Mise en forme — formatting** — M03.C0
- **Modalité — value / category** — M02.C0
- **Mode — mode** — M02.C0
- **Modèle de données — Data Model** — M03.C0
- **Modèle sémantique — semantic model** — M01.C0
- **montant** — M11.C0
- **Moyenne arithmétique — mean** — M02.C0
- **moyenne mobile** — M11.C0
- **Moyenne pondérée — weighted mean** — M02.C0
- **multi-clés** — M07.C0
- **Mécanisme d'absence — Missing mechanism** — M04.C0
- **médiane de 5** — M11.C0
- **Médiane — median** — M02.C0
- **Métadonnées — metadata** — M01.C0
- **Méthode pandas — pandas method** — M05.C0
- **Métier — business / functional owner** — M01.C0
- **Métrique** — M01.C0
- **Nom de plage — named range** — M03.C0
- **Nombre de série de date — date serial** — M03.C0
- **Nombre à virgule / point — decimal separator** — M01.C0
- **Non applicable — Not applicable** — M04.C0
- **NOT** — M07.C0
- **note d'EDA** — M09.C0
- **null-skipping** — M07.C0
- **NULLIF** — M07.C0
- **NULLS FIRST / NULLS LAST** — M07.C0
- **Numéro de série — serial date** — M01.C0
- **numérotation** — M11.C0
- **objection** — M10.C0
- **OFFSET** — M07.C0, M07.C0
- **ON vs WHERE** — M07.C0
- **opérateur de comparaison** — M07.C0
- **OR** — M07.C0
- **ORDER BY** — M07.C0
- **ordre d'exécution** — M07.C0, M11.C0
- **ordre de fenêtre** — M11.C0
- **ordre métier** — M10.C0
- **ordre perceptuel** — M10.C0
- **pagination par clé** — M07.C0
- **palette catégorielle** — M10.C0
- **palette divergente** — M10.C0
- **palette séquentielle** — M10.C0
- **Paramètre — Parameter** — M05.C0
- **part relative** — M11.C0
- **partition** — M11.C0, M11.C0
- **PATH** — M08.C0
- **Perte par jointure — Join-induced loss** — M04.C0
- **Pipeline — Pipeline** — M05.C0
- **Pivot en SQL — Pivot in SQL** — M05.C0
- **Pivoter — Pivot Column** — M05.C0
- **piège d'inférence** — M09.C0
- **Plage de somme — sum range** — M03.C0
- **Plage nommée — named range** — M03.C0
- **Plage propagée — spill range** — M03.C0
- **Plage — range** — M03.C0, M03.C0
- **plan d'exécution** — M11.C0
- **Politique de valeurs manquantes — Missing data policy** — M04.C0
- **pondération** — M11.C0
- **Population — population** — M02.C0
- **port TCP** — M06.C0
- **projection** — M11.C0
- **Propagation d'erreur — error propagation** — M03.C0
- **Propagation — spill** — M03.C0
- **périmètre** — M11.C0
- **Périmètre — scope** — M01.C0
- **période partielle** — M11.C0
- **quantile** — M11.C0
- **Quartile inclusif / exclusif — QUARTILE.INC / .EXC** — M03.C0
- **Quasi-identifiant** — M04.C0
- **Question analytique** — M01.C0
- **question servie** — M10.C0, M10.C0
- **rang dense** — M11.C0
- **rapport de contraste** — M10.C0
- **rareté légitime** — M09.C0
- **raster** — M10.C0
- **README de données** — M04.C0
- **Recensement — census** — M02.C0
- **Recherche approximative — approximate match** — M03.C0
- **Recherche exacte — exact match** — M03.C0
- **Recherche à gauche — left lookup** — M03.C0
- **redondance** — M10.C0
- **Registre des doublons — Duplicate register** — M04.C0
- **regroupement multi-colonnes** — M07.C0
- **Regrouper — Group By** — M05.C0
- **Rejouabilité — reproducibility** — M01.C0
- **Relation — Relationship** — M03.C0
- **relire un classeur** — M10.C0
- **repliement d'un libellé** — M11.C0
- **Report — fill** — M03.C0
- **Reproductibilité — Reproducibility** — M05.C0, M05.C0
- **Représentativité — representativeness** — M02.C0
- **requête en escalier** — M11.C0
- **requête à l'identique** — M11.C0
- **Requête — Query** — M03.C0
- **Responsable de la donnée — data steward** — M01.C0
- **RFM** — M11.C0
- **ROUND** — M07.C0
- **ROW_NUMBER** — M07.C0
- **Règle de garde — Survivorship rule** — M04.C0
- **Règle univariée — Univariate rule** — M04.C0
- **récapitulatif multi-niveaux** — M11.C0
- **récence** — M11.C0
- **récurrence** — M11.C0
- **récursion** — M11.C0
- **Référence absolue — absolute reference** — M03.C0
- **Référence circulaire — circular reference** — M03.C0
- **Référence mixte — mixed reference** — M03.C0
- **Référence relative — relative reference** — M03.C0
- **Référence structurée — structured reference** — M03.C0, M03.C0
- **résolution utile** — M10.C0
- **rétention** — M11.C0
- **Rétention — retention** — M01.C0
- **saison** — M11.C0
- **saisonnalité** — M09.C0
- **Sauvegarde — backup** — M01.C0
- **Schéma — schema** — M01.C0
- **segment** — M07.C0, M09.C0, M11.C0
- **Segment — Slicer** — M03.C0
- **SELECT** — M07.C0
- **Session en mémoire — In-memory session** — M05.C0
- **soupçon** — M09.C0
- **Source de vérité — system of record** — M01.C0
- **Source — Source** — M05.C0, M05.C0
- **sous-requête de liste** — M07.C0
- **sous-requête scalaire** — M07.C0, M11.C0
- **sous-total** — M11.C0
- **Sous-total visible — SUBTOTAL** — M03.C0
- **SUM** — M07.C0
- **support** — M10.C0
- **surcharge** — M10.C0
- **Système 1904 — 1904 date system** — M03.C0
- **Séparateur / encodage / décimale** — M01.C0
- **Séparateur — delimiter** — M01.C0
- **Séparateur — separator** — M01.C0
- **séquence** — M10.C0
- **Série de dates — date serial** — M03.C0
- **série fabriquée** — M11.C0
- **Série — Series** — M05.C0
- **table calendrier** — M11.C0
- **table d'expression commune** — M11.C0
- **Table de référence — lookup table** — M03.C0
- **table dérivée** — M07.C0
- **table en mémoire** — M11.C0
- **Table — table** — M01.C0
- **tableau croisé** — M11.C0
- **Tableau croisé dynamique — PivotTable** — M03.C0
- **tableau de bord** — M10.C0
- **Tableau— table** — M03.C0
- **Taille — Size** — M05.C0
- **Taux de déclenchement — Alert rate** — M04.C0
- **tendance** — M09.C0
- **test de non-régression** — M11.C0
- **Test de réparation — Repair plausibility check** — M04.C0
- **Texte libre — free text** — M01.C0
- **titre qui affirme** — M10.C0
- **top N par groupe** — M11.C0
- **total de contrôle** — M11.C0
- **Transformation — Transformation** — M05.C0
- **Transposition— Date swap** — M05.C0
- **treemap** — M10.C0
- **tri par alias** — M07.C0
- **tri par position** — M07.C0
- **Tri à plusieurs niveaux — multi-level sort** — M03.C0
- **Trimée— trimmed mean** — M02.C0
- **troncature déclarée** — M10.C0
- **trou de série** — M11.C0, M11.C0
- **Typage / inférence — type inference** — M01.C0
- **Type de données — data type** — M01.C0, M05.C0
- **Unicité — Uniqueness** — M04.C0
- **Valeur aberrante — Outlier** — M04.C0
- **valeur attendue** — M11.C0
- **Valeur de sentiment — Sentinel value** — M04.C0
- **Valeur distincte — distinct value** — M01.C0
- **Valeur extrême — outlier** — M02.C0
- **valeur gelée** — M11.C0
- **Valeur manquante — Missing value** — M04.C0
- **Valeur manquante — null / missing** — M01.C0
- **Validation des données — data validation** — M03.C0
- **Validité — Validity** — M04.C0
- **Variable** — M02.C0, M08.C0
- **Variable qualitative / catégorielle — categorical** — M01.C0
- **Variable quantitative — quantitative variable** — M01.C0
- **vectoriel** — M10.C0
- **Verdict — Verdict** — M05.C0
- **version direction** — M10.C0
- **version équipe** — M10.C0
- **Versionnage — versioning** — M01.C0, M01.C0
- **Volets figés — frozen panes** — M03.C0
- **vue** — M07.C0, M11.C0
- **WHERE** — M07.C0, M07.C0
- **Zone de données** — M04.C0
- **Zone de nom — name box** — M03.C0
- **zéro ajouté** — M10.C0
- **écart expliqué** — M11.C0
- **Échantillon — sample** — M02.C0
- **échelle de décision** — M08.C0
- **Échelle de gravité — Severity ladder** — M04.C0
- **Échelle de mesure — measurement scale** — M01.C0
- **échelle logarithmique** — M10.C0
- **éclatement** — M11.C0
- **écran** — M10.C0
- **Éditeur Power Query** — M03.C0
- **Éditeur Power Query — Power Query Editor** — M05.C0
- **étage** — M11.C0
- **Étape appliquée — Applied step** — M05.C0
- **Étape— Step** — M05.C0
- **Étendue — range** — M02.C0
- **étiquette** — M07.C0

---

## 3. Glossaire

La première phrase de chaque encadré « Définition » du manuel, dans l'ordre des chapitres.

- **M01.C0** — **Chemin — path** — l'adresse complète d'un fichier ou d'un dossier.
- **M01.C0** — **Extension** — *file extension* — les lettres placées après le dernier point du nom, qui indiquent le **format** du fichier, donc le logiciel capable de l'ouvrir et ce que ce logiciel va y trouver.
- **M01.C0** — **Arborescence — tree** — l'organisation des dossiers en arbre, depuis un point d'entrée unique.
- **M01.C0** — **Nommage — naming convention** — grammaire écrite des noms de fichiers.
- **M01.C0** — **Rétention** — *retention period* — durée pendant laquelle on conserve un fichier et ses versions.
- **M01.C0** — **Journal — log** — fichier texte horodaté qui enregistre, dans l'ordre, ce qui a été fait sur les données.
- **M01.C0** — **Donnée — data** — un fait enregistré à un instant précis par un système, avec une unité : une valeur de case.
- **M01.C0** — **Information** — une donnée replacée dans son contexte : quoi, qui, quand, combien, dans quelle unité.
- **M01.C0** — **Connaissance — insight** — deux informations comparées plus une explication que l'on peut discuter.
- **M01.C0** — **Décision** — un engagement : une action, un responsable, une date, des conséquences assumées.
- **M01.C0** — **Métrique — measure** — la définition de calcul d'un indicateur, écrite noir sur blanc : ce qui entre, ce qui sort, sur quelle période, comment on additionne.
- **M01.C0** — **Indicateur — KPI (key performance indicator)** — une métrique suivie dans le temps parce qu'elle est rattachée à un objectif et à un seuil qui déclenche quelque chose.
- **M01.C0** — **Table** — un rectangle de données où chaque colonne est une caractéristique mesurée pour tous les enregistrements et chaque ligne un objet du monde réel, au grain choisi.
- **M01.C0** — **Enregistrement — row / record** — la ligne, c'est-à-dire un objet : une ligne de ticket, et non un ticket, non un client, non un mois.
- **M01.C0** — **Grain — granularity** — la phrase qui dit ce que représente une ligne.
- **M01.C0** — **Clé primaire — primary key** — une colonne, ou un couple de colonnes, qui rend chaque ligne unique.
- **M01.C0** — **Clé étrangère — foreign key** — une colonne qui renvoie à la clé d'une autre table.
- **M01.C0** — **Valeur distincte — distinct value** — une valeur comptée une seule fois.
- **M01.C0** — **Type de données — data type** — la nature d'une valeur, qui détermine ce que l'on a le droit d'en faire.
- **M01.C0** — **Typage automatique — type inference** — le mécanisme par lequel un logiciel devine le type de chaque colonne en lisant un échantillon de lignes.
- **M01.C0** — **Séparateur décimal — decimal separator** — le signe qui sépare la partie entière de la partie décimale.
- **M01.C0** — **Valeur manquante — null** — l'absence de valeur.
- **M01.C0** — **Donnée structurée — structured data** — des lignes et des colonnes, un schéma connu d'avance : le format où l'on peut compter, joindre et agréger sans rien interpréter.
- **M01.C0** — **Donnée semi-structurée — semi-structured data** — des étiquettes portées par le fichier lui-même (JSON, XML, journaux applicatifs), mais des enregistrements qui ne se ressemblent pas tous : une clé peut manquer d'un objet à l'autre, et c'est ce manque qui demande un traitement.
- **M01.C0** — **Donnée non structurée — unstructured data** — texte, image, son, vidéo : aucune colonne.
- **M01.C0** — **Encodage de caractères** — *character encoding* — la table qui associe des octets à des signes.
- **M01.C0** — **Variable quantitative — quantitative variable** — une valeur qui se mesure ou se compte, et pour laquelle les calculs ont un sens : quantité, prix, montant, durée.
- **M01.C0** — **Variable qualitative — categorical variable** — une appartenance : famille, catégorie, statut, marque.
- **M01.C0** — **Cardinalité — cardinality** — le nombre de valeurs distinctes d'une colonne.
- **M01.C0** — **Échelle de mesure — measurement scale** — le niveau d'information porté par une colonne : nominale (des noms, sans ordre), ordinale (un ordre, mais des distances qui n'ont pas de sens constant), à rapport (ordre, distances, et un zéro qui veut dire « rien »).
- **M01.C0** — **Source de vérité — system of record** — le système où une information est officiellement détenue : ici, la caisse du magasin.
- **M01.C0** — **Donnée brute — raw data** — l'état exact de ce qui a été reçu, octet pour octet, avant la moindre correction.
- **M01.C0** — **Manifeste de jeu de données** — *dataset manifest* — fiche courte qui accompagne un jeu figé : ce qu'il contient, d'où il vient, quelle version du code l'a produit, quelles empreintes, quelles limites connues, qui a validé, à quelle date.
- **M01.C0** — **Empreinte — checksum / hash** — une signature courte calculée sur le contenu d'un fichier.
- **M01.C0** — **Jeu figé — frozen dataset** — copie verrouillée, nommée, référencée par un identifiant, sur laquelle un chiffre publié a été calculé.
- **M01.C0** — **Chaîne de valeur — value chain** — la suite d'étapes par lesquelles une donnée devient une décision qui rapporte ou qui épargne.
- **M01.C0** — **Cadrage — scoping** — l'accord écrit sur la question, le périmètre, le délai et le critère de réussite.
- **M01.C0** — **Livrable — deliverable** — un objet remis, nommé, daté, avec un destinataire identifié.
- **M01.C0** — **Modèle sémantique — semantic model** — la couche d'un outil de décision où les mesures et les relations sont définies une fois pour toutes.
- **M01.C0** — **Rejouabilité — reproducibility** — pouvoir refaire le même résultat plus tard, avec les mêmes entrées, sans avoir à s'en souvenir.
- **M02.C0** — **Population** — *population* — l'ensemble complet des individus que l'on voudrait décrire.
- **M02.C0** — **Échantillon** — *sample* — la partie réellement observée de la population, sélectionnée par une > règle.
- **M02.C0** — **Tirage — sampling** — la règle, écrite et reproductible, qui a sélectionné les individus de > l'échantillon dans la population.
- **M02.C0** — **Variable** — *variable* — une caractéristique relevée pour **tous** les individus, c'est-à-dire > une colonne dont on peut dire en une phrase ce qu'elle mesure et dans quelle unité.
- **M02.C0** — **Modalité** — *value, category* — une valeur prise par la variable (« Peinture », 0,04, vide).
- **M02.C0** — **Cardinalité — cardinality** — le nombre de modalités distinctes d'une variable.
- **M02.C0** — **Moyenne arithmétique** — *arithmetic mean* — le total réparti également.
- **M02.C0** — **Médiane** — *median* — la valeur du milieu après tri.
- **M02.C0** — **Mode** — *mode* — la valeur la plus fréquente.
- **M02.C0** — **Moyenne pondérée** — *weighted mean* — moyenne dans laquelle chaque valeur compte pour un > poids.
- **M02.C0** — L'**étendue** (*range*) est la différence entre maximum et minimum.
- **M02.C0** — Les **bornes de Tukey** (*Tukey fences*, « moustaches » ou limites externes en français) sont > Q1 − 1,5 × IQR et Q3 + 1,5 × IQR.
- **M02.C0** — Le **coefficient de variation** (*CV*, coefficient of variation) est l'écart-type divisé par la > moyenne, exprimé en pourcentage.
- **M02.C0** — L'**erreur type de la moyenne** (*standard error of the mean*, SE) est l'écart-type divisé par la > racine carrée de l'effectif.
- **M02.C0** — L'**écart absolu médian** (*MAD*, median absolute deviation) est la médiane des valeurs absolues > des écarts à la médiane.
- **M02.C0** — Le **p-ième quantile** d'une série triée est la valeur en dessous de laquelle se trouve la part p > de l'effectif.
- **M02.C0** — La **fréquence cumulée** (*cumulative frequency*) associe à une valeur la proportion > d'observations inférieures ou égales ; sa courbe est la **fonction de répartition** (*CDF*, cumulative > distribution function, *ogive* en français).
- **M02.C0** — La **boîte à moustaches** (*boxplot*) représente cinq nombres : le premier quartile et le > troisième, qui forment la boîte ; la médiane, qui la coupe ; la plus petite et la plus grande observation > restant dans les bornes de Tukey, qui forment les moustaches.
- **M02.C0** — On appelle **concentration** le fait qu'une part donnée des observations porte une part > différente — en général plus grande — du total.
- **M02.C0** — La **distribution** d'une variable décrit comment ses valeurs se répartissent : quelles valeurs, > avec quelles fréquences.
- **M02.C0** — Un **histogramme** (*histogram*) est la représentation en barres jointives des effectifs > tombant dans des intervalles contigus de même amplitude — les **classes**.
- **M02.C0** — L'**asymétrie** (*skewness*, notée γ₁ ou *skew*) mesure le déséquilibre de la distribution autour > de son centre : en simplifiant, la moyenne des écarts au centre élevés au cube, normalisée par le cube de > l'écart-type.
- **M02.C0** — Le **kurtosis** (*kurtosis* ; « aplatissement » en français, bien qu'il ne mesure pas la hauteur > du pic contrairement à une légende tenace) pénalise la présence de valeurs lointaines : moyenne des écarts au > centre élevés à la quatrième puissance, normalisée.
- **M02.C0** — La **covariance** entre deux variables x et y est la moyenne des produits des écarts : pour chaque > observation, (xᵢ − moyenne de x) × (yᵢ − moyenne de y).
- **M02.C0** — Le **coefficient de corrélation linéaire de Pearson** — *Pearson correlation coefficient*, noté > *r* — est la covariance divisée par le produit des deux écarts-types.
- **M02.C0** — La **corrélation de rang de Spearman** — *Spearman rank correlation*, notée ρ — remplace chaque > valeur par son rang dans la série triée, puis calcule la corrélation de Pearson sur ces rangs.
- **M02.C0** — La **régression linéaire simple** — *simple linear regression*, méthode des moindres carrés > (*ordinary least squares*, OLS) — trace la droite qui minimise la somme des carrés des écarts verticaux.
- **M02.C0** — On dit que x **cause** y si agir sur x change y.
- **M02.C0** — Une **variable de confusion** (*confounder*) influence à la fois x et y et fait apparaître un lien > qui n'existe pas entre elles.
- **M02.C0** — La **probabilité** d'un événement est la fréquence vers laquelle se stabilise cette fréquence quand > on répète l'expérience beaucoup de fois.
- **M02.C0** — L'**erreur d'échantillonnage** (*sampling error*) est la dispersion d'une statistique si l'on > refaisait le tirage.
- **M02.C0** — Un **biais d'échantillonnage** (*sampling bias*) est un écart systématique entre la statistique > attendue et la valeur de population, produit par la **méthode de sélection**.
- **M02.C0** — Un **biais de couverture** (*coverage bias*) est le cas où la liste de départ ne contient pas toute > la population.
- **M02.C0** — Un **intervalle de confiance à 95 %** est fabriqué par une méthode qui, appliquée à une infinité de > tirages, enfermerait la vraie valeur dans 95 % des cas.
- **M02.C0** — Le **bootstrap** (*bootstrap*) traite l'échantillon comme une population : on tire 2 000 fois, > **avec remise**, un échantillon de même taille, on recalcule la statistique, et les 2,5ᵉ et 97,5ᵉ percentiles de > ces 2 000 résultats servent d'intervalle.
- **M02.C0** — L'**échantillonnage stratifié** (*stratified sampling*) découpe la population en cases (jour du > mois, catégorie, vendeur, trimestre), tire au sort dans chaque case, puis combine les résultats pondérés par le > poids réel des cases.
- **M02.C0** — Un **test statistique** est une procédure qui compare l'écart observé à ce que le hasard produit > habituellement.
- **M02.C0** — La **puissance statistique** (*statistical power*) d'un test est la probabilité de rejeter H0 > quand l'écart réel vaut une taille donnée ; la **marge de détection** (en anglais *minimum detectable effect*) est > l'écart que le test relève avec 80 % de puissance.
- **M02.C0** — Le **test de Mann-Whitney** (*Mann-Whitney U test*, test de la somme des rangs) classe les > observations des deux groupes de la plus petite à la plus grande et compare les rangs, non les montants : il > éprouve l'égalité des deux distributions, et reste lisible quand la moyenne n'est qu'un point d'ancrage fragile.
- **M02.C0** — Le **test du khi deux d'indépendance** (*chi-squared test of independence*) compare, case par > case, les effectifs observés d'un tableau croisé aux effectifs **attendus** si les deux variables n'avaient aucun > lien ; la statistique additionne les écarts relatifs, et se compare à la loi du khi deux dont les degrés de liberté > valent (nombre de lignes - 1) × (nombre de colonnes - 1).
- **M03.C0** — Une **cellule active** est la seule cellule où l'on tape : elle est encadrée d'un liseré épais et > son adresse est écrite dans la zone de nom.
- **M03.C0** — On dit qu'une cellule est **reconnue comme nombre** quand le tableur y lit un contenu chiffré, > manipulable par `SOMME()`, triable, moyennable.
- **M03.C0** — La **zone utilisée** (*used range*) est le plus petit rectangle contenant toutes les cellules ayant > un contenu **ou** une mise en forme.
- **M03.C0** — Une **conversion** de types change la nature d'un contenu ; une **mise en forme** change son > rendu.
- **M03.C0** — Un **format à sections** s'écrit `positif;négatif;zéro;texte`.
- **M03.C0** — Une date stockée comme date est un **nombre de série** : un compteur de jours, dont l'heure est la > partie décimale.
- **M03.C0** — On parle de **coercition** quand le tableur force un contenu dans un type demandé : > `=CNUM("56 658")` échoue, `=CNUM("56658")` réussit, `=CNUM("")` renvoie `#VALEUR!`.
- **M03.C0** — L'**ancrage** d'une règle de mise en forme conditionnelle est la cellule où l'on se trouvait quand > on l'a écrite : la formule est ensuite reportée *relativement* sur chaque cellule de la plage.
- **M03.C0** — Une **table** se nomme une fois, et ce nom devient une adresse vivante : `TableVentes` désigne > `Feuille![A1:M481]` aujourd'hui, `A1:M521` dans un mois.
- **M03.C0** — La **portée** d'un tableau est l'intervalle qu'il occupe, étendue à chaque ligne ajoutée en > contiguïté.
- **M03.C0** — Un doublon n'existe pas dans les données, il existe **relativement à une clé**.
- **M03.C0** — Une **colonne calculée** d'un tableau est une formule saisie une fois : le tableur la propage à > toutes les lignes et la recompose à chaque ligne nouvelle.
- **M03.C0** — Le **maillage** d'une formule est l'ensemble des cellules qu'elle lit.
- **M03.C0** — Le **sens du report** est la direction où le décalage s'applique : vers le bas pour une colonne de > lignes, vers la droite pour une ligne de mois.
- **M03.C0** — L'**ordre de priorité** est la convention qui range les opérateurs : puissances, puis > multiplications et divisions, puis additions et soustractions, puis comparaisons et concaténation.
- **M03.C0** — Une erreur de tableur est une **valeur réservée**, qui se propage comme les autres le long du > maillage — mais que `SOMME`, `MOYENNE`, `NB` et les filtres **ignorent en silence**.
- **M03.C0** — Un **critère de comparaison** s'écrit entre guillemets, opérateur compris : `">=1000000"`, > `"<>"` (non vide), `"=0"` (vide n'est pas zéro).
- **M03.C0** — Le **dénominateur** d'un agrégat est le nombre de lignes qu'il a réellement regardées.
- **M03.C0** — Une **partition fermée — closed partition** est un découpage dont les morceaux rendent le tout : > les lignes s'additionnent (57 + 143 + 112 + 53 + 57 + 24 + 34 = 480) et les chiffres d'affaires aussi.
- **M03.C0** — Un agrégat **robuste** est un agrégat dont on connaît le périmètre exact : quelles lignes, quels > vides, quelles erreurs, quel filtre.
- **M03.C0** — Une **clé unique** est une valeur qui apparaît une fois et une seule dans la table où l'on > cherche.
- **M03.C0** — Une **clé typée** est une clé du même type des deux côtés.
- **M03.C0** — Un **repli** est la valeur renvoyée quand la recherche échoue : le 4ᵉ argument de `RECHERCHEX`, > contre une fonction `SIERREUR` autour de `RECHERCHEV`.
- **M03.C0** — Une fonction de texte **découpante** (`GAUCHE`, `DROITE`, `STXT`) compte en caractères, pas en > significations : elle ne sait pas que le 4ᵉ caractère est un tiret.
- **M03.C0** — Le **padding** est l'ajout de zéros non significatifs pour que deux écritures d'un même nombre > aient la même longueur de texte.
- **M03.C0** — Une **période ancrée** est une période définie par une formule qui la recalcule > (`=DATE(ANNEE(AUJOURDHUI());1;1)`), par opposition à une période tapée à la main (`>=01/01/2025`).
- **M03.C0** — Une **fonction matricielle dynamique** est une fonction dont le résultat est un tableau de taille > variable : `FILTRE`, `UNIQUE`, `TRIER`, `TRIERPAR`, `SEQUENCE`, `TABLEAU.ALEA`.
- **M03.C0** — `LET(nom1;valeur1;…;calcul)` attache des noms intermédiaires dans une formule.
- **M03.C0** — Un **décalage d'échelle** est l'écart entre la période mesurée et la période dénominateur.
- **M03.C0** — Une **agrégation juste** est une agrégation dont on peut nommer les lignes consommées : la > moyenne des 480 lignes (75 152 FCFA) répond à « par ligne », la moyenne des sept moyennes de catégorie (98 281) > répond à une autre question.
- **M03.C0** — Dans le modèle, une **colonne calculée** ajoute une valeur par ligne, stockée dans la table et > recalculée à l'actualisation — le même mot qu'en C03, où il désigne une formule propagée à la saisie dans le > tableau ; la mécanique change, le mot reste.
- **M03.C0** — **Protéger une feuille** interdit d'écrire dans les cellules verrouillées, sans rien chiffrer ni > cacher ; **chiffrer le classeur** (*Fichier → Informations → Protéger le classeur*) est le seul geste qui empêche > la lecture du fichier.
- **M03.C0** — Une **macro enregistrée** est une retranscription d'actions en VBA dans un classeur `.xlsm` : > elle rejoue des clics à des adresses précises, sans connaître ni les erreurs ni les changements de forme.
- **M04.C0** — Un **encodage** est la table qui associe un octet à un signe.
- **M04.C0** — Une **clé candidate** est un jeu de colonnes dont les valeurs identifient une ligne et une seule.
- **M04.C0** — Un **contrôle croisé** est une vérification qui porte sur deux colonnes au lieu d'une.
- **M04.C0** — On parle d'**intégrité référentielle** quand toute valeur d'une colonne de référence pointe une > ligne existante de la table référencée.
- **M04.C0** — Une **convention de codage** est un choix d'écriture, arbitraire mais *écrit*, qui donne à une > absence un signe visible : `0`, `-1`, la chaîne vide, un enregistrement dédié.
- **M04.C0** — Une **jointure externe** (à gauche, à droite, pleine) conserve les lignes sans correspondance en > laissant le champ complémentaire vide ; une jointure **intérieure** les supprime.
- **M04.C0** — **Imputer par le cas le plus semblable** (*hot-deck*, ou *k plus proches voisins*) consiste à > emprunter la valeur d'une ligne qui ressemble fort à celle qui manque : même produit, même magasin, même mois, > même type de client.
- **M04.C0** — Un **marqueur de manque** est une colonne ajoutée, en général booléenne, qui surviv à la > réparation : `ttc_reconstitue = VRAI` sur les 3 421 lignes.
- **M04.C0** — Un **doublon logique** est une paire de lignes qui décrivent le même fait alors qu'une seule > pourrait le décrire.
- **M04.C0** — Un **doublon structurel** est une répétition que le modèle de données autorise et que le métier > reconnaît : deux lignes d'un même ticket, deux relevés de stock le même jour dans deux magasins.
- **M04.C0** — Le **registre des doublons** est la liste nominative de ce qui a été retiré : une ligne par > groupe, avec les deux identifiants en présence et la règle qui a départagé.
- **M04.C0** — Un **dictionnaire de correspondance** (*crosswalk*) est une table qui relie les identifiants ou les > libellés de deux systèmes.
- **M04.C0** — Une **règle de contrôle** est une affirmation vérifiable sur une donnée, assortie d'une décision et > d'un destinataire : « le prix d'une ligne reste dans la bande négociée du catalogue, sinon la ligne est retournée > au magasin pour validation ».
- **M04.C0** — Un **test de réparation** consiste à appliquer la correction *en simulation* et à repasser la règle > de domaine dessus.
- **M04.C0** — Un **registre de contrôles** est la table qui énonce, pour chaque colonne ou groupe de colonnes : la > règle, son niveau, sa cadence, son destinataire, son taux de déclenchement attendu et sa mesure du jour.
- **M04.C0** — Deux règles sont **redondantes** quand elles signalent exactement le même jeu de lignes.
- **M04.C0** — On appelle **normalisation** toute transformation *bijective à l'identifiant près* appliquée à une > valeur, qui change sa représentation et non sa signification : `+226 77 76 25 98 96` et `+2267776259896` > désignent le même abonné ; `16 638 FCFA` et `16638` désignent la même somme.
- **M04.C0** — Un **contrôle de convergence** fait arriver le même résultat par deux chemins qui n'ont aucune > raison de se ressembler : l'un lit ce que l'opérateur a tapé, l'autre recalcule depuis d'autres colonnes.
- **M04.C0** — Une **conversion d'unité** multiplie une valeur par un facteur fixé par une définition > extérieure au fichier (1 m³ = 1 000 L), et change le nom de la colonne en conséquence : `quantite` devient > `quantite_litres`.
- **M04.C0** — Un **encodage** est une table de correspondance octet → caractère.
- **M04.C0** — Un **README de données** est le document qui répond, sans ouvrir les fichiers : ce que contient > le dossier, à quel grain, sous quelles règles de gestion, et ce qui y est volontairement absent.
- **M04.C0** — Une ligne de **journal des transformations** est une quintuple complète : *date, fichier, > opération, règle, compteur avant → après* (l'auteur faisant la sixième en production).
- **M04.C0** — Un **quasi-identifiant** est une combinaison de colonnes apparemment anonymes qui désigne une > personne dans une part mesurable des cas.
- **M04.C0** — Un **identifiant direct** est une colonne qui désigne une personne sans intermédiaire : le nom, > le numéro de téléphone, l'adresse e-mail.
- **M05.C0** — Une **transformation** est une opération qui modifie une colonne ou une table sans changer > la *source*.
- **M05.C0** — Une **clé candidate** est un jeu de colonnes dont les valeurs identifient une ligne et une > seule dans la table.
- **M05.C0** — Un **compteur d'échec** est un nombre qui dit combien de lignes ont été perdues (ou > marquées en erreur) par une conversion.
- **M05.C0** — Une **empreinte sha256** est une somme cryptographique de 256 bits qui identifie un > contenu au bit près.
- **M05.C0** — Une **requête paramétrée** est une requête qui dépend d'un ou plusieurs **paramètres** > (valeurs nommées, lues dans un fichier externe ou saisies par l'utilisateur).
- **M05.C0** — Le **Gestionnaire de paramètres** (Power Query) est l'interface qui liste tous les > paramètres d'un classeur.
- **M05.C0** — L'**étape de type** est l'étape Power Query qui assigne un type à chaque colonne — > c'est l'équivalent de `dtype=str` (pandas) ou de `CAST(...
- **M05.C0** — Le **verdict** d'une requête paramétrée est l'ensemble des mesures publiées en clés > `m05_*` pour le mois cible.
- **M05.C0** — Une **CTE** (`WITH … AS …`) est une sous-requête nommée, réutilisable dans la > requête principale.
- **M05.C0** — Le **`EXCLUDE`** est une clause DuckDB 1,5,5 (depuis la 0,9) qui permet de retirer > des colonnes du `SELECT` : `SELECT * EXCLUDE (rn, date_vente)` retire `rn` et `date_vente`.
- **M05.C0** — Le **`LPAD`** (left-pad) est la fonction SQL DuckDB qui pad une chaîne à gauche > avec un caractère donné : `LPAD('7', 2, '0')` rend `'07'`.
- **M05.C0** — Le **session variable** est une variable de session DuckDB, créée par `SET nom = > valeur`.
- **M05.C0** — Le **préambule `controle_python.py`** est le bloc de code exécuté en premier dans > chaque cellule du notebook de référence.
- **M05.C0** — Le **`.loc[mask, "col"]`** est l'opérateur pandas d'affectation par masque booléen : > `df.loc[mask, "col"] = nouvelle_valeur` modifie uniquement les lignes où `mask` est `True`.
- **M05.C0** — Le **SettingWithCopyWarning** est un avertissement pandas qui signale qu'une > modification peut ne pas être appliquée (parce qu'on travaille sur une *vue* du DataFrame, pas > une copie).
- **M05.C0** — Le **format Parquet** est un format de stockage tabulaire **typé** et **compressé** > (5-10 × plus compact que CSV).
- **M05.C0** — La **grille de décision** (tableau du §5.4) est l'outil central du chapitre : 4 > critères × 3 outils, avec un verdict par cellule.
- **M05.C0** — Le **critère limitant** est le critère qui, seul, tranche le choix de l'outil.
- **M05.C0** — Le **scheduler** est l'outil qui exécute le pipeline à intervalles réguliers > (`cron` sous Linux, Planificateur de tâches sous Windows, Airflow pour les pipelines complexes).
- **M05.C0** — La **vitesse dépend de la taille** : un outil rapide sur 6 884 lignes peut être > lent sur 1 million, et inversement.
- **M06.C0** — La **base de données relationnelle** est un ensemble de **tables reliées par des > contraintes** (clés étrangères, types, valeurs, contrôles), persisté sur disque et requêtable par > SQL via un SGBD.
- **M06.C0** — Le **SGBD** (système de gestion de base de données) est le **moteur logiciel** qui > gère la base : stockage, indexation, verrouillage, sauvegarde, exécution des requêtes SQL.
- **M06.C0** — La **3FN** (3ᵉ forme normale) est la condition qui dit : *toutes les colonnes > non-clés dépendent de la clé, de toute la clé, rien que de la clé*.
- **M06.C0** — La **clé étrangère** (foreign key, FK) est une **colonne** dont les valeurs sont > contraintes par une **référence** vers la clé primaire d'une autre table.
- **M06.C0** — Une **contrainte** est une **règle** que les données doivent suivre, **portée par > la base elle-même** (pas par le code applicatif).
- **M06.C0** — Le **type SQL** est la **famille** des valeurs qu'une colonne accepte.
- **M06.C0** — La valeur **`NULL`** représente l'**absence de valeur**.
- **M06.C0** — Le **`DDL`** (Data Definition Language) est le sous-ensemble du SQL qui crée, modifie, > et supprime la **structure** : `CREATE TABLE`, `ALTER TABLE`, `DROP TABLE`, `CREATE INDEX`, > `CREATE VIEW`.
- **M06.C0** — Une **clé étrangère** est une **contrainte** qu'on **déclare** dans le DDL et que la > base **fait respecter** à chaque insertion et à chaque suppression.
- **M06.C0** — Une **cardinalité** est le **nombre** de liens entre une ligne source et les lignes > cibles.
- **M06.C0** — Une **table de jointure** matérialise une relation N-M.
- **M06.C0** — Une ligne de la source correspond à 0..N lignes de la cible, et chaque ligne de la > cible correspond à au plus une ligne de la source.
- **M06.C0** — Une ligne de la source correspond à au plus une ligne de la cible, et inversement.
- **M06.C0** — Chaque ligne de la source peut correspondre à 0..N lignes de la cible, et inversement.
- **M06.C0** — Le **SGBD intégré** (in-process) est un moteur SQL qui vit dans le **même > processus** que le programme qui l'appelle.
- **M06.C0** — Le **SGBD serveur** (client-serveur) tourne sur une **machine distante** et les > clients s'y connectent par réseau.
- **M06.C0** — L'**import CSV** est le geste d'alimenter une table à partir d'un fichier plat.
- **M06.C0** — Un **SGBD serveur** (*client-server DBMS*) est un moteur qui tourne sur une > machine *dédiée* et écoute les connexions réseau sur un **port TCP** (par défaut 5432 pour > PostgreSQL).
- **M06.C0** — Le **NoSQL** (*Not only SQL*) est la famille des bases **non-relationnelles**, > optimisées pour des cas où le relationnel est maladroit : documents semi-structurés (MongoDB), paires > clé-valeur ultra-rapides (Redis), graphes de relations (Neo4j), colonnes larges distribuées > (Cassandra).
- **M06.C0** — Le **datawarehouse** (entrepôt) est un SGBD **analytique** où les données > *validées* sont stockées pour les rapports (tableaux de bord, SQL analytique, OLAP).
- **M06.C0** — Le **théorème CAP** (Brewer, 2000) énonce qu'un SGBD **distribué** (sur plusieurs > machines) ne peut pas avoir simultanément **Cohérence**, **Disponibilité**, **Tolérance au > partitionnement**.
- **M06.C0** — Le **modèle ACID** (Atomicity, Consistency, Isolation, Durability — atomique, > cohérent, isolé, durable) est le contrat des transactions SGBDR : chaque transaction est garantie > *atomique* (tout ou rien), *cohérente* (la base reste valide), *isolée* (les autres transactions > ne voient pas l'état intermédiaire), *durable* (la modification survit à un crash).
- **M07.C0** — Une **requête SQL** — *SQL query* — est une instruction adressée au SGBD, qui > retourne un résultat tabulaire (lignes × colonnes).
- **M07.C0** — Une **clause** est un morceau de la requête, qui commence par un mot-clé > (`SELECT`, `FROM`, `WHERE`, …) et se termine par une autre clause ou un point-virgule.
- **M07.C0** — Une **table** est un ensemble de lignes (enregistrements) et de colonnes > (champs), en 3FN (cf.
- **M07.C0** — Un **alias** — *alias* — est un nom temporaire donné à une colonne ou à une > table dans une requête.
- **M07.C0** — L'**ordre d'exécution** — *logical execution order* — est la séquence dans > laquelle le SGBD traite les clauses d'une requête SQL, dans l'ordre : FROM → WHERE → GROUP BY > → HAVING → SELECT → DISTINCT → ORDER BY → LIMIT.
- **M07.C0** — Une **console DuckDB** — *DuckDB CLI* — est l'interface en ligne de commande > du moteur DuckDB.
- **M07.C0** — Le **filtre WHERE** — *WHERE clause* — est la clause SQL qui élimine les > lignes qui ne satisfont pas une condition.
- **M07.C0** — Un **opérateur de comparaison** est un opérateur à 2 opérandes qui retourne > `TRUE`, `FALSE` ou `NULL` : `=`, `<>`, `<`, `>`, `<=`, `>=`.
- **M07.C0** — `EXTRACT(part FROM date)` — *extract* — extrait une partie de la date : année, > mois, jour, heure, minute, seconde, jour de la semaine, etc.
- **M07.C0** — La **logique à trois valeurs** — *three-valued logic* — est la logique du SQL > qui admet trois valeurs de vérité : `TRUE`, `FALSE`, et `NULL` (l'inconnu).
- **M07.C0** — `ORDER BY` — *trier* — est la clause SQL qui range les lignes du résultat > dans l'ordre spécifié.
- **M07.C0** — `NULLS FIRST` — *nulls d'abord* — place les valeurs `NULL` au début du tri ; > `NULLS LAST` les place à la fin.
- **M07.C0** — La **pagination** — *pagination* — est la subdivision d'un résultat en pages > de taille fixe.
- **M07.C0** — Le **tri multi-clés** — *composite sort* — est un tri sur plusieurs colonnes, > appliqué dans l'ordre de citation.
- **M07.C0** — Une **fonction d'agrégat** — *aggregate function* — est une fonction qui > prend un ensemble de valeurs (les lignes d'un groupe) en entrée et produit une **unique > valeur** en sortie.
- **M07.C0** — Le **comptage distinct** — *distinct count* — compte les valeurs uniques > d'une colonne au lieu de toutes les lignes.
- **M07.C0** — Le **panier moyen** — *average order value* (AOV) — est le montant moyen > d'une vente, calculé par `AVG(montant_ttc)`.
- **M07.C0** — L'**ignorance des `NULL`** — *null-skipping* — est le comportement par > défaut des agrégats `SUM`, `AVG`, `MIN`, `MAX` (et `COUNT(colonne)`) : les valeurs > `NULL` ne participent ni à la somme, ni au dénombrement, ni à la comparaison.
- **M07.C0** — La clause **`GROUP BY`** — *grouper par* — subdivise les lignes du > résultat en **groupes** selon les valeurs de la colonne (ou des colonnes) citées : les > lignes qui partagent la même valeur forment un groupe, et chaque fonction d'agrégat du > `SELECT` est calculée **séparément sur chaque groupe**.
- **M07.C0** — Une **clé de regroupement** — *grouping key* — est la colonne (ou la > liste de colonnes) citée dans `GROUP BY`.
- **M07.C0** — La clause **`HAVING`** — *ayant* — est le filtre qui s'applique aux > **groupes** après le calcul des agrégats.
- **M07.C0** — Le **comptage conditionnel** — *conditional count* — est le motif > `SUM(CASE WHEN condition THEN 1 ELSE 0 END)` : il convertit « compter les lignes qui > vérifient la condition » en expression agrégable.
- **M07.C0** — L'expression **`CASE`** — *expression conditionnelle* — est la brique de > logique conditionnelle du `SELECT`.
- **M07.C0** — Une **tranche** — *bucket* — est un intervalle de valeurs découpé par > des `CASE WHEN` successifs (ici `< 50 000`, `< 200 000`, sinon).
- **M07.C0** — La fonction **`COALESCE`** — *coalescer* — renvoie la **première** > valeur de sa liste d'arguments qui n'est pas `NULL`.
- **M07.C0** — La fonction **`NULLIF`** — *nullifier si égal* — renvoie `NULL` quand > ses deux arguments sont égaux, sinon le premier argument.
- **M07.C0** — Une **jointure** — *join* — est l'opération qui met côte à côte les > lignes de deux tables (ou plus) qui **s'accordent sur une clé**, via `ON` (par exemple > `v.id_client = c.id_client`).
- **M07.C0** — La **clé étrangère** — *foreign key* (FK) — est la colonne d'une table > qui pointe vers la clé primaire d'une autre table (`vente.id_client` → > `client.id_client`).
- **M07.C0** — Le **produit cartésien** — *cross product* — est l'ensemble de toutes les > paires (ligne du gauche × ligne du droit), sans condition : `|gauche| × |droit|` lignes.
- **M07.C0** — L'**explosion de jointure** — *join fan-out* — est le gonflement du > nombre de lignes quand une jointure accorde **plusieurs lignes d'un côté à une ligne de > l'autre** (relation `N → N`, ou jointure sur une colonne non unique).
- **M07.C0** — Une **sous-requête** — *subquery* — est une requête SQL **implantée à > l'intérieur** d'une autre requête, dans le `SELECT`, le `WHERE` ou le `FROM`.
- **M07.C0** — Une **sous-requête scalaire** — *scalar subquery* — est une sous-requête > qui doit renvoyer **exactement une valeur** (1 ligne, 1 colonne).
- **M07.C0** — Une **CTE** — *Common Table Expression* — est une sous-requête **nommée**, > déclarée en tête de requête par `WITH nom AS (SELECT …)`, puis référencée comme une table > dans le reste de la requête.
- **M07.C0** — Une **vue** — *view* — est une requête SQL **enregistrée** dans le > schéma de la base, interrogable comme une table (`SELECT … FROM vue`).
- **M07.C0** — **`EXISTS`** teste s'il **existe** au moins une ligne dans sa > sous-requête (généralement **corrélée** : elle référence une colonne de la requête > extérieure).
- **M07.C0** — Le **pattern de double négation** — *double negation* — est l'écriture > `NOT EXISTS (SELECT … WHERE NOT EXISTS (SELECT …))` qui exprime « **tous les** » : on > nie l'existence d'un contre-exemple.
- **M08.C0** — **interpréteur** — *interpreter* — le programme qui lit le code Python et l'exécute > ligne à ligne, sans phase de « compilation » préalable visible : le fichier `.py` est lu, exécuté, > relu si vous le modifiez.
- **M08.C0** — **environnement virtuel** — *virtual environment* — une copie isolée de l'interpréteur > + ses paquets, limitée à un projet : les installations dans le venv n'affectent pas le Python système > ni les autres venvs.
- **M08.C0** — **exigence** — *requirement* — la ligne `paquet==version` d'un fichier > `requirements.txt` : la liste figée des paquets (et versions) qu'un projet a besoin, qui permet à > `pip install -r requirements.txt` de reconstruire **exactement** le même environnement sur une autre > machine.
- **M08.C0** — **noyau** — *kernel* — le processus d'exécution derrière Jupyter : il exécute chaque > cellule demandée et **conserve l'état** (variables, imports) entre les exécutions.
- **M08.C0** — **variable** — *variable* — un nom qui pointe vers une valeur : `prix = 1500` > colle l'étiquette « prix » sur le nombre 1 500 ; réaffecter (`prix = 2000`) re-colle l'étiquette, > sans copier quoi que ce soit.
- **M08.C0** — **type** — *type* — la famille d'une valeur, qui autorise (ou interdit) les > opérations : `int` (entier), `float` (nombre à virgule), `str` (texte), `bool` (vrai/faux).
- **M08.C0** — **f-string** — *f-string* — une chaîne précédée de `f` où chaque `{…}` est > remplacé par la valeur : `f"Total : {total:,.2f}"` affiche le total avec 2 décimales.
- **M08.C0** — **traceback** — *traceback* — le rapport d'erreur de Python : il donne le chemin > parcouru (la pile d'appels, du haut vers le bas), la **ligne fautive** (le numéro et le texte), > la **flèche** qui souligne le coupable, et le **message** (le type d'erreur + une phrase).
- **M08.C0** — **échelle de décision** — *if/elif/else* — une suite d'échelons testés **dans > l'ordre** : la première condition vraie exécutera son bloc, et le reste est sauté ; `else` > attrape ce que personne n'a pris.
- **M08.C0** — **itération** — *iteration* — un tour de boucle : le corps de la `for` > s'exécute une fois par élément, dans l'ordre, sans sauter ni revenir.
- **M08.C0** — **boucle infinie** — *infinite loop* — une boucle dont la condition ne devient > jamais fausse (ou qu'aucun `break` ne coupe) : la machine se répète sans fin.
- **M08.C0** — **compréhension** — *list comprehension* — `[expr for x in it if cond]` : une > liste construite en **une** ligne, lisible de gauche à droite comme une phrase.
- **M08.C0** — **séquence** — *sequence* — un contenant ordonné, lisible par index : > liste, tuple, chaîne.
- **M08.C0** — **immuable** — *immutable* — un objet qu'on ne peut pas modifier en place > (tuple, chaîne, nombre) : pour « changer » une valeur, on **construit** un nouvel objet > (`surface + (210,)`, pas `surface[5] = 210`).
- **M08.C0** — **méthode de chaîne** — *string method* — un verbe attaché à une chaîne > (`s.strip()`, `s.split(" ")`) : elle **renvoie une nouvelle** chaîne sans toucher à > l'originale (la chaîne est **immutable**, §5.2) — d'où l'enchaînement `s.strip().replace(…)`.
- **M08.C0** — **clé** — *key* — l'étiquette d'une case de dictionnaire : `d[clé]` > lit, `d[clé] = valeur` écrit, `clé in d` teste.
- **M08.C0** — **valeur unique** — *unique value* — une valeur qui ne compte qu'une > fois : `set(villes)` passe la liste au tamis (5 éléments → 3), `len(set(…))` compte les > uniques.
- **M08.C0** — **tranche** — *slice* — `l[a:b]` : les éléments de l'index **a** à > l'index **b − 1** (la fin **est exclue**) ; `l[::2]` tous les deux ; `l[::-1]` l'inverse.
- **M08.C0** — **fonction** — *function* — un bloc nommé de code, appelé par son nom > avec des arguments, qui **renvoie une valeur** avec `return`.
- **M08.C0** — **argument par défaut** — *default argument* — la valeur prise quand > l'appel ne précise pas l'argument : `calculer_remise(1500)` prend `taux=0.10`.
- **M08.C0** — **portée** — *scope* — la zone de visibilité d'une variable : **locale** > (née et morte dans la fonction), **globale** (le fichier tout entier).
- **M08.C0** — **docstring** — *docstring* — la chaîne en **tête** de fonction, entre > triples guillemets, lue par `help(f)` et récupérable par `f.__doc__`.
- **M08.C0** — **exception** — *exception* — une erreur **levée** à l'endroit où le > problème arrive, qui remonte la pile jusqu'au premier `except` qui la **nomme**.
- **M08.C0** — **tableau** — *ndarray* — un bloc de mémoire **contigu** de valeurs > **homogènes** : un seul `dtype` pour tout le tableau, une forme (`shape`) qui dit > combien de valeurs.
- **M08.C0** — **vecteurisation** — *vectorization* — l'application d'une opération > à **tout** un tableau d'un seul geste, sans boucle Python : `montants * 1.19` > multiplie les 50 008 valeurs, `np.sum(montants)` les additionne.
- **M08.C0** — **nan** — *nan* (« not a number ») — la valeur **absente** du > monde des nombres : elle **se propage** (`nan + 1 = nan` — l'absence contagieuse), > elle **contamine** les agrégats (`np.sum` renvoie `nan`), et elle se **détecte** > (`np.isnan`) ou se **contourne** (`np.nansum` = 3500,0 : la somme regarde autour > du trou).
- **M08.C0** — **diffusion** — *broadcasting* — la règle de forme de NumPy : deux > tableaux peuvent s'opérer s'ils sont **de même forme**, ou si l'un est un > **scalaire**, ou si leurs formes sont **compatibles** (du plus court au plus > long, dimensions égales ou 1).
- **M08.C0** — **tableau de données** — *DataFrame* — un tableau à deux > dimensions de **colonnes nommées** (une table SQL en Python), l'objet central > de pandas : `shape` donne lignes × colonnes, `columns` les noms, `dtypes` la > famille de chaque colonne.
- **M08.C0** — **série** — *Series* — une **colonne** : un index (les > étiquettes de lignes) + des valeurs.
- **M08.C0** — **index** — *index* — l'étiquette de chaque ligne (par défaut > 0, 1, 2, …) : la poignée par laquelle `loc` et `iloc` attrapent les lignes.
- **M08.C0** — **masque** — *mask* — le résultat d'une comparaison sur une > colonne : une Série de `True`/`False` **par ligne** (28 065 `True` sur > `montant_ttc > 100000`), posée dans les crochets du DataFrame pour ne garder > que les lignes vraies : `v[masque]` est le `WHERE` de M07.
- **M08.C0** — **transformation** — *transform* — l'opération qui calcule > une valeur **par groupe** et la **repose sur chaque ligne** du groupe : la > table de départ garde sa forme (50 008 × 14), chaque ligne portant l'agrégat > de son groupe.
- **M08.C0** — **jointure** — *merge* — l'alignement de **deux DataFrames** > sur une **clé commune explicite** (`on="id_magasin"`), avec le mode de > conservat des lignes (`how=`) : le `JOIN` de M07, où la clé est une > information **métier** et non un détail de syntaxe.
- **M08.C0** — **table pivotée** — *pivot_table* — la réorganisation > **lignes ↔ colonnes** d'une table autour d'une clé (ici magasin × mois) et > d'une valeur agrégée (le CA) : la vue « tableau croisé » de M07, en un > geste pandas.
- **M08.C0** — **addition en centimes** — *cent-based summation* — la > conversion des montants en **centimes entiers** > (`(colonne * 100).round().astype("int64")`) avant toute somme : le centime > est le plus petit multiple **exact** de FCFA, l'entier ne dérive pas, et le > total final se convertit en FCFA par une seule division (`// 100`).
- **M09.C0** — **analyse exploratoire de données** — *exploratory data analysis (EDA)* — l'examen > systématique d'un jeu de données inconnu pour en dégager des structures, des problèmes et des > pistes, **avant** de modéliser.
- **M09.C0** — **audit** — le passage du protocole qui cherche les défauts du jeu (doublons, > manquants, valeurs impossibles) *avant* de mesurer quoi que ce soit.
- **M09.C0** — **fiche d'entrée** — le document de cadrage d'une analyse : variables (sens, > unité, source), questions autorisées, durée prévue.
- **M09.C0** — **conclusion provisoire** — une affirmation posée **avec** ses limites > (période, échantillon, variables absentes), révisable aux données suivantes.
- **M09.C0** — **borne métier** — une limite dictée par le métier, pas par la > statistique : un stock ≥ 0, une note entre 0 et 20, une date dans la période de > l'export.
- **M09.C0** — **iqr** — *interquartile range* — Q3 − Q1 : la largeur du « cœur » de la > distribution (le milieu des 50 %), indépendante des extrêmes.
- **M09.C0** — **manquant** — une valeur absente, sous deux formes : le `NaN` que > `isna()` compte, et la **chaîne vide** codée en clair que `isna()` laisse passer.
- **M09.C0** — **point aberrant** — *outlier* — une observation au-delà d'une borne > définie **avant** de chercher : Q3 + 1,5 × iqr (Tukey), une borne métier (stock ≥ 0, note > ≤ 20), ou la comparaison à la période.
- **M09.C0** — **tendance** — la pente de fond de la série : ce qui reste quand on a > retiré les cycles.
- **M09.C0** — **moyenne glissante** — *moving average* — la moyenne calculée sur une > **fenêtre glissante** (ici 3 mois) : chaque point résume sa fenêtre, les vagues > s'effacent, le lit et les crues restent.
- **M09.C0** — **bruit** — la variabilité **sans cycle** : ce que la moyenne glissante > lisse.
- **M09.C0** — **saisonnalité** — *saisonnalité* — la variation **régulière et > prévisible** liée au cycle (saison, mois, jour de semaine, heure) : elle revient **au > même endroit du cycle**, c'est ce qui la rend exploitable pour la prévision.
- **M09.C0** — **anomalie** — *anomalie* — une observation qui s'écarte d'une borne > **définie avant** de chercher : iqr (position dans la distribution), borne métier > (limite du domaine) ou période (écart au cycle attendu).
- **M09.C0** — **récurrence** (du flux) — la règle de continuité d'une série de > stock : `hier + entrées − sorties = aujourd'hui`.
- **M09.C0** — **soupçon** — le stade d'une anomalie **non prouvée** : un signal > (position, borne, période) sans aucun des 3 témoins.
- **M09.C0** — **anomalie structurelle** — un défaut qui révèle un **mécanisme** > (export, saisie, génération) plutôt qu'une erreur ponctuelle : les 8 doublons du > fil rouge (clé métier redite, `id_vente` distinct), les 4 stocks négatifs déductibles.
- **M09.C0** — **corrélation** — *corrélation* — la mesure d'association entre deux > variables ; Pearson mesure le lien **linéaire**, de −1 (opposé) à +1 (proportionnel), > 0 = pas de lien linéaire.
- **M09.C0** — **piège d'inférence** — le saut interdit de l'**association** à la > **cause**, sous ses 3 formes mesurées : variable **tierce** (la troisième variable > qui cause les deux — contrôlée, la corrélation résiduelle est le lien direct), > **régression vers la moyenne** (les extrêmes retournent vers le milieu sans cause), > **sens inversé** (B cause A, on affirme A cause B).
- **M09.C0** — **segment** — un groupe défini **avant** de regarder les résultats : > les bornes sont **métier** (< 2, 2 à 5, ≥ 6 jours d'absence), pas statistiques, et > s'écrivent dans le rapport **avant** les chiffres.
- **M09.C0** — **variable tierce** — *confond* — la troisième variable qui **cause > les deux** variables observées : ici, le niveau d'origine (proxy : la note du T1) > pousse l'absence **et** la note du T2.
- **M09.C0** — **tableau croisé** — *tableau de contingence* — la fréquence (ou la > moyenne) d'un **couple de modalités** : matière × trimestre ici, 5 × 3 cases.
- **M09.C0** — **légende** — le bloc texte du graphique : la **question** posée > (dans le titre), la **source** (la sortie exécutée), la **taille d'échantillon** (n) > et **l'axe** quand il ne part pas de zéro.
- **M09.C0** — **graphique** — *chart* — la traduction visuelle d'une sortie vers un > lecteur.
- **M09.C0** — **biais de sélection** — *biais d'échantillonnage* — l'écart entre > la population **étudiée** (le fichier) et la population **visée** (le métier) : les > 1 200 clients du fil rouge ne sont pas **tous** les clients du groupe, les 400 > élèves ne sont pas **tous** les élèves de l'établissement.
- **M09.C0** — **note d'EDA** — le livrable de **fin** d'exploration : 1 page par > jeu, où chaque affirmation porte sa **source** (la sortie exécutée, **re-jouable**) > et sa **limite** (ce qu'elle **ne** dit pas, **remplie**).
- **M10.C0** — Le **budget de lecture** est le temps qu'un lecteur accorde réellement à un > graphique dans un dossier ou une réunion : de l'ordre de quelques secondes.
- **M10.C0** — Un graphique est un **argument visuel** : il affirme une chose (« ces huit parts se > ressemblent », « cette courbe se retourne ») et son lecteur la croit sans calculer.
- **M10.C0** — L'**ordre perceptuel** est le classement des tâches de lecture par précision > moyenne.
- **M10.C0** — On appelle **facteur de conversion** d'un canal la quantité de ce canal qui > correspond à un point de pourcentage de données : 8,5 mm sur un axe large comme la page, 3,6° sur > un camembert, une variation relative pour une aire, une différence de clarté L\* pour une couleur.
- **M10.C0** — La **grille de conception** n'est pas une grille d'esthétique : chaque point est une > **question fermée** à laquelle on répond par oui ou non, en montrant la preuve (« axe : zéro, oui », > « ordre : trié par chiffre d'affaires décroissant, oui »).
- **M10.C0** — L'**arbre de choix** est une procédure en cinq étapes, parcourue **avant** > d'ouvrir l'outil : (1) écrire la question, (2) nommer le symptôme, (3) choisir la famille, > (4) choisir le graphique précis, (5) choisir l'outil et le support.
- **M10.C0** — On appelle **corrélation affichée** la valeur du coefficient de corrélation entre > deux séries **telles que le graphique les présente** — c'est-à-dire après le choix des deux > échelles.
- **M10.C0** — On appelle **graphique-tableau** (ou tableau enrichi) un tableau dont les cellules > portent un codage visuel : barres intégrées, échelle de couleurs, flèches de variation.
- **M10.C0** — Une **mesure** est un nombre calculé sur des données (« 7 876 320 164 FCFA de > CA net en 24 mois »).
- **M10.C0** — La **palette de la maison** (ou palette de référence) est le jeu de couleurs figé > par la charte, avec un rôle par couleur.
- **M10.C0** — Une palette est **appariée** quand sa famille (catégorielle, séquentielle, > divergente) correspond à la structure de la variable affichée.
- **M10.C0** — La **lisibilité en niveaux de gris** est la propriété d'un graphique qui reste > entièrement compréhensible une fois la couleur retirée : chaque série garde un signe distinctif > (libellé, forme, position).
- **M10.C0** — On appelle **précision affichée** le nombre de chiffres significatifs décidés à > l'affichage, par opposition à la précision du calcul.
- **M10.C0** — Un **titre qui affirme** énonce un constat que les données soutiennent, en une > phrase citable telle quelle.
- **M10.C0** — Un axe est **honnête** quand le lecteur connaît ses bornes sans les chercher.
- **M10.C0** — On appelle **hauteur occupée** la part de la hauteur d'axe réellement couverte > par les données (11,8 % pour notre chiffre d'affaires sur un axe à zéro, 82,4 % sur l'axe tronqué).
- **M10.C0** — La **hiérarchie visuelle** est l'ordre de lecture imposé à l'œil : titre, chiffre > principal, appuis, graphique, source.
- **M10.C0** — L'**annotation** est le texte qui désigne un point de la figure et donne sa > valeur.
- **M10.C0** — L'**échelle logarithmique** place les graduations sur les puissances d'un facteur > (× 10 en général) : chaque décade occupe la même hauteur.
- **M10.C0** — La **relecture en 60 secondes** est un rituel, pas un talent : six questions, un > minuteur, et la règle que tout défaut trouvé s'écrit soit dans la figure (déclaration), soit dans la > liste des corrections (refonte).
- **M10.C0** — Le **diagnostic mesuré** est la première étape notée du projet « La refonte » : il > nomme les défauts d'un rapport, **mesure** leur effet sur les données, et écrit la décision fausse > que chacun peut déclencher.
- **M10.C0** — On appelle **faux citable** la phrase fausse qu'un lecteur pourrait prononcer devant > une figure exacte (« la volatilité explose », « les retours suivent le CA »).
- **M10.C0** — L'**appel à la décision** est la phrase, écrite sur le troisième écran, qui nomme la > décision demandée, son destinataire, son montant et son indicateur de suivi.
- **M10.C0** — La **densité d'un écran** est le nombre de chiffres, de lignes et de figures qu'il > porte.
- **M10.C0** — On appelle **restitution** l'ensemble formé par la séquence et ses annexes.
- **M10.C0** — La **couverture des objections** est le rapport entre le nombre d'objections > anticipées et le nombre d'objections auxquelles la restitution répond explicitement.
- **M10.C0** — On appelle **contrat d'outil** l'ensemble des trois questions auxquelles un outil > répond dans une chaîne de production : *qui le modifie ?*, *à quelle fréquence ?*, *sur quel support > arrive-t-il ?* Un outil choisi sans ces trois réponses produit des fichiers que personne ne > réutilise — et un graphique qu'on refera trois fois.
- **M10.C0** — Un outil est dit **cité** (ou « non exécuté ») quand sa procédure est décrite sans > avoir été mise en œuvre dans l'atelier.
- **M10.C0** — La **résolution utile** d'une figure est le nombre de pixels disponibles par unité > de donnée : **25** px par mois en 96 dpi, **79** px par mois en 300 dpi, pour le même graphique de > **24** mois.
- **M10.C0** — Un **export** est la conversion d'une figure vers un fichier destiné à un usage > précis (écran, impression, retouche, diffusion).
- **M11.C0** — Une **fonction de fenêtre** — *window function* — est un calcul qui prend en entrée un > **ensemble de lignes** (la fenêtre) et rend **une valeur par ligne**.
- **M11.C0** — La **partition** — *partition* — est la subdivision de la fenêtre en groupes **indépendants > les uns des autres**.
- **M11.C0** — Le **cadre de fenêtre** — *window frame* — précise **quelles lignes** autour de la ligne > courante la fonction voit : `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` (les deux précédentes et la > courante), `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` (depuis le début), `ROWS BETWEEN UNBOUNDED > PRECEDING AND UNBOUNDED FOLLOWING` (toute la partition).
- **M11.C0** — Une **sous-requête scalaire** — *scalar subquery* — est une sous-requête placée dans une > expression et qui rend **une seule valeur** (une ligne, une colonne) : `SUM(x) / (SELECT SUM(y) FROM t)`.
- **M11.C0** — Les trois fonctions de rang répondent à trois questions différentes sur la même mesure : > « **donne-moi un numéro unique** » (`ROW_NUMBER`), « **quelle place mérite-t-elle ?** » (`RANK`), > « **combien de niveaux de performance y a-t-il jusqu'ici ?** » (`DENSE_RANK`).
- **M11.C0** — Une **clé de départage** — *tie-breaker* — est une colonne ajoutée après la mesure dans > l'`ORDER BY` d'une fenêtre (presque toujours la clé primaire de la table) pour que deux exécutions du même > code produisent **le même** résultat.
- **M11.C0** — Un **quantile** — *quantile* — est une frontière qui coupe une population ordonnée en > parties de taille comparable : les tiers (`NTILE(3)`), les déciles (`NTILE(10)`), les centiles > (`NTILE(100)`).
- **M11.C0** — Un **trou de série** — *series gap* — est une ligne dont le décalage n'a pas de > prédécesseur : le premier mois d'une série, ou le premier mois après un filtre trop zélé.
- **M11.C0** — Une **table calendrier** — *date dimension* — est la table de référence du temps : une > ligne par jour (ici **1 339**), avec ses attributs calculés une fois pour toutes (année, mois, trimestre, > libellé du jour, indicateur de férié).
- **M11.C0** — Le **périmètre** — *scope* — d'une comparaison est l'ensemble des lignes effectivement > comparables : mêmes mois, même nombre de jours, mêmes magasins, mêmes exclusions.
- **M11.C0** — Un **trou de série** — *series gap* — est une période de l'axe de temps pour laquelle > il n'existe **aucune** donnée : soit parce que rien ne s'est produit (un dimanche sans vente), soit parce > que la mesure n'a pas été faite (un mois sans objectif).
- **M11.C0** — Le **cadre de fenêtre** — *window frame* — est la partie de la partition réellement prise > en compte autour de la ligne courante.
- **M11.C0** — Une **cohorte** est un ensemble de clients réunis par un **événement daté** commun — et > l'événement doit être choisi avec soin.
- **M11.C0** — La **rétention** est la part d'une cohorte encore active après N périodes.
- **M11.C0** — La **pondération** consiste à donner à chaque cohorte un poids proportionnel à son > effectif.
- **M11.C0** — Le **RFM** n'a pas de frontières intrinsèques : les coupures en trois blocs égaux sont un > choix de méthode (égalité des effectifs), pas une vérité métier.
- **M11.C0** — Une **table d'expression commune** — *CTE* — est un bloc `WITH nom AS (requête)` placé > avant la requête principale.
- **M11.C0** — Le **repliement d'un libellé** consiste à ramener plusieurs graphies d'une même valeur à > une seule écriture.
- **M11.C0** — Un **récapitulatif multi-niveaux** est une agrégation qui produit, dans **une** requête, > le détail et les sous-totaux.
- **M11.C0** — Le **grain** d'un jeu de lignes est ce que représente **une** ligne.
- **M11.C0** — Le **plan d'exécution** est la description, par le moteur, de ce qu'il va faire : les > opérateurs, leur ordre d'enchaînement et les colonnes lues.
- **M11.C0** — Une **vue** ne stocke pas de données : c'est une requête à laquelle on a donné un nom.
- **M11.C0** — Un **index** est une structure de recherche par valeur, qui évite de parcourir toutes les > lignes.
- **M11.C0** — Le **coût du `SELECT *`** est le travail de lecture des colonnes qui ne serviront pas à la > sortie.
- **M11.C0** — Un **test de non-régression** est un contrôle qui rejoue une requête **publiée** et > compare son résultat à une **valeur attendue**.
- **M11.C0** — Un **contrôle croisé** vérifie une même grandeur par deux chemins **indépendants** : > deux moteurs (DuckDB et SQLite), deux outils (SQL et pandas), ou deux socles (le socle M11 et celui de > M09).
- **M11.C0** — Le **code de sortie** d'un contrôle est le signal qu'il rend au système : zéro si tous les > contrôles passent, non nul sinon.
- **M11.C0** — La **valeur attendue** d'un test est la valeur **publiée** — ici, celle du fichier > `chiffres_cites.json` — et non la valeur qu'on vient de lire à l'écran.
- **M12.C0** — La **Business Intelligence** (BI) est l'ensemble organisé des moyens — données, > définitions, modèles, outils, responsabilités — qui permet à une organisation de **décider avec des > chiffres partagés** : les mêmes définitions pour tous, disponibles au bon moment, avec une action > décidée d'avance quand ils passent un seuil.
- **M12.C0** — Un **indicateur clé** — KPI, *Key Performance Indicators* — est une mesure > **choisie** pour suivre une performance et **déclencher une décision**.
- **M12.C0** — Une **décision fondée sur les données** — *data-driven* — est prise en s'appuyant > sur des mesures définies **avant** la décision, et vérifiables **après**.
- **M12.C0** — La **couche sémantique** — *semantic layer* — est l'endroit — table, vue, modèle — > où les définitions d'indicateurs sont **écrites une fois** pour toute l'organisation.
- **M12.C0** — Le **reporting** est la production périodique de résultats standardisés, à > définition figée, destinés à être **lus** — tableau de bord mensuel, état des ventes, balance âgée.
- **M12.C0** — La **BI** (Business Intelligence) est l'ensemble des moyens qui permettent > d'**explorer** les données pour répondre à des questions non prévues à l'avance, gouvernées par des > définitions partagées.
- **M12.C0** — Un **entrepôt de données** — *data warehouse* — est un stockage structuré, > historisé et modélisé (M13), alimenté par les sources opérationnelles, dans lequel la BI vient lire.
- **M12.C0** — Le **service en autonomie** — *self-service* — désigne le fait de laisser un utilisateur métier construire ses > propres vues à partir d'une couche sémantique gouvernée.
- **M12.C0** — Les **quatre régimes de question** sont le descriptif (« que s'est-il passé ? »), le > **diagnostique** (« pourquoi ? »), le **prédictif** (« que se passera-t-il ? ») et le **prescriptif** > (« que faire ? »).
- **M12.C0** — Un **fait** est un événement mesurable et daté — une vente, une commande, une > rupture, un encaissement.
- **M12.C0** — Une **dimension** est un axe d'analyse stable, par lequel on découpe les faits : > temps, magasin, client, produit, canal, mode de paiement.
- **M12.C0** — Une **métrique** est une quantité mesurée sur les faits : un montant, une quantité, > une durée, un effectif.
- **M12.C0** — Le **grain** d'une table ou d'un résultat est ce que représente **une ligne** : > une ligne de vente, un ticket, un couple produit-mois, une commande, une journée.
- **M12.C0** — Une mesure est **additive** quand elle peut être additionnée sur toutes les > dimensions (les montants), **semi-additive** quand elle s'additionne sur certaines seulement > (un stock, qui s'additionne dans l'espace mais pas dans le temps), et **non additive** quand elle ne > s'additionne nulle part (un taux, une moyenne, un comptage d'éléments distincts).
- **M12.C0** — Un **indicateur clé** — **KPI**, *Key Performance Indicators* — est une métrique > **choisie** pour suivre une performance qui compte, dotée d'une carte de définition complète et d'un > responsable nommé.
- **M12.C0** — Une **carte de définition** est la fiche d'identité d'un indicateur : formule, source, > granularité, fréquence, responsable, seuil d'alerte, contre-KPI.
- **M12.C0** — Un **seuil d'alerte** est la valeur à partir de laquelle l'indicateur déclenche une > **action** écrite.
- **M12.C0** — Un **contre-KPI** — *indicateur de contrepartie* — est l'indicateur qui mesure ce > qu'on **dégrade** en améliorant le premier.
- **M12.C0** — Un **effet pervers** est une conséquence non voulue d'un indicateur devenu objectif : > les personnes pilotées par la mesure agissent sur ce qu'elle mesure — pas sur ce qu'elle devait > mesurer.
- **M12.C0** — Une **chaîne de calcul** — *pipeline* — est la suite d'étapes qui transforme les > sources brutes en indicateurs publiés : extraction, nettoyage, stockage, modélisation, définition, > visualisation, diffusion.
- **M12.C0** — Une **source de vérité** est l'endroit unique où une information est tenue à jour pour > un usage donné.
- **M12.C0** — La **gouvernance des données** désigne les règles explicites qui décident qui crée, > qui modifie, qui valide et qui publie une donnée ou un indicateur.
- **M12.C0** — L'**adoption** est l'usage réel du dispositif par ses destinataires : nombre de > lecteurs réguliers, fréquence d'ouverture, décisions citant le dispositif.
- **M12.C0** — La **diffusion** est le dernier étage : le choix du support, de la fréquence et du > moment où l'indicateur atteint son lecteur — courriel, réunion, écran partagé — avec la personne qui > répond du rendez-vous.
- **M12.C0** — Un **cahier des charges** est l'écrit qui fixe, avant le début des travaux, les > décisions à éclairer, les destinataires, la fréquence, les définitions attendues, les critères de > réception et le budget de maintenance.
- **M12.C0** — Le **commanditaire** — *sponsor* — est la personne qui finance le dispositif, le > défend dans l'organisation et arbitre les désaccords.
- **M12.C0** — Une **partie prenante** est toute personne qui influe sur le projet ou le subit : > destinataires, producteurs de données, informaticiens, comptables, contrôleurs.
- **M12.C0** — La **recette** — *réception* — est l'étape où le commanditaire vérifie le dispositif > contre les critères du cahier des charges : chaque indicateur existe, sa valeur est reproductible, sa > définition est publiée, son responsable est nommé, son seuil déclenche une action.
- **M12.C0** — La **maintenance** couvre deux activités distinctes : la **maintenance corrective**, qui > répare (**1 200 000** FCFA par an dans le dossier raté, soit **23 077** FCFA par semaine), et la > **maintenance évolutive**, qui retire ce qui n'est plus lu et ajoute ce qui manque.

---

## 4. Index des planches

Chaque planche est citée par le chapitre qui l'affiche. Toutes sont en SVG, sous 776 px,
avec du texte réel : elles se lisent à l'écran, s'impriment et se régénèrent.

| Planche | Chapitre |
|---|---|
| `M01_C01_chemins.svg` | M01.C0 |
| `M01_C02_chaine.svg` | M01.C0 |
| `M01_C03_table.svg` | M01.C0 |
| `M01_C03_table.svg` | M01.C0 |
| `M01_C04_types.svg` | M01.C0 |
| `M01_C05_classer.svg` | M01.C0 |
| `M01_C06_cycle.svg` | M01.C0 |
| `M01_C07_metiers.svg` | M01.C0 |
| `M02_C04_boxplot.svg` | M02.C0 |
| `M02_C05_histogramme.svg` | M02.C0 |
| `M02_C07_distribution_echantillonnage.svg` | M02.C0 |
| `M02_C08_foret_comparaisons.svg` | M02.C0 |
| `M03_C01_fenetre_excel.svg` | M03.C0 |
| `M03_C02_formats_saisie.svg` | M03.C0 |
| `M03_C03_structure_tableur.svg` | M03.C0 |
| `M03_C04_adresses_erreurs.svg` | M03.C0 |
| `M03_C05_agregats_conditionnels.svg` | M03.C0 |
| `M03_C06_recherches_assemblage.svg` | M03.C0 |
| `M03_C07_dates_periodes.svg` | M03.C0 |
| `M03_C08_tcd_et_modele.svg` | M03.C0 |
| `M03_C08_chemin_donnees.svg` | M03.C0 |
| `M04_C01_diagnostic_en_douze_points.svg` | M04.C0 |
| `M04_C02_cinq_mecanismes_cinq_traitements.svg` | M04.C0 |
| `M04_C03_quatre_niveaux_de_doublon.svg` | M04.C0 |
| `M04_C04_quatre_familles_de_regles.svg` | M04.C0 |
| `M04_C05_trois_niveaux_deux_preuves.svg` | M04.C0 |
| `M04_C06_boite_a_donnees.svg` | M04.C0 |
| `M08_C01_quatre_couches_environnement_python.svg` | M08.C0 |
| `M08_C02_types_operations_matrice.svg` | M08.C0 |
| `M08_C03_decider_repetir_flux.svg` | M08.C0 |
| `M08_C04_cinq_conteneurs.svg` | M08.C0 |
| `M08_C05_lire_traceback.svg` | M08.C0 |
| `M08_C06_boucle_vs_vecteur.svg` | M08.C0 |
| `M08_C07_loc_vs_iloc_4_cas.svg` | M08.C0 |
| `M08_C08_groupby_sql_pandas.svg` | M08.C0 |
| `M09_C01_protocole_dix_etapes_3_jeux.svg` | M09.C0 |
| `M09_C02_audit_matrice_3_familles.svg` | M09.C0 |
| `M09_C03_tendance_saisonnalité_bruit.svg` | M09.C0 |
| `M09_C04_boite_a_outils_preuve_4_cas.svg` | M09.C0 |
| `M09_C05_trois_fausses_causes_chiffrees.svg` | M09.C0 |
| `M09_C06_table_question_graphique.svg` | M09.C0 |
| `M10_C01_cinq_encodages.svg` | M10.C0 |
| `M10_C02_seize_graphiques.svg` | M10.C0 |
| `M10_C03_palette_testee.svg` | M10.C0 |
| `M10_C04_ecriture_titre_axe_annotation.svg` | M10.C0 |
| `M10_C05_mur_des_10_erreurs.svg` | M10.C0 |
| `M10_C06_sequence_trois_ecrans.svg` | M10.C0 |
| `M10_C07_meme_graphique_trois_outils.svg` | M10.C0 |
| `M11_C01_carte_des_fenetres.svg` | M11.C0 |
| `M11_C04_matrice_retention.svg` | M11.C0 |
| `M12_C05_carte_des_sept_etages.svg` | M12.C0 |
| `M12_C06_matrice_des_dix_couples.svg` | M12.C0 |

---

## 5. Index des instruments

Les scripts qui font tourner le manuel : tous s'exécutent sur le socle livré, sur un poste
ordinaire, sans service payant.

| Instrument | Ce qu'il fait |
|---|---|
| `tools/budget_pages.py` | Budget de pages du manuel : le recalculer, le mesurer, ne jamais le laisser « à l'œil ». |
| `tools/classeur_M03.py` | classeur_M03.py — fabrique le classeur d'atelier du module M03 (Excel). |
| `tools/controle_exos_M07.py` | Auto-validation des 35 exercices de l'évaluation M07 (épreuve C). |
| `tools/controle_exos_M08.py` | Auto-validation des 15 exercices de l'évaluation M08 (épreuve C). |
| `tools/controle_exos_M09.py` | Auto-validation des 15 exercices de l'évaluation M09 (épreuve C). |
| `tools/controle_formules.py` | controle_formules.py — Q3 de la porte §G.1, côté tableur. |
| `tools/controle_pdf.py` | Contrôle final du PDF composé d'un module — le seul contrôle qui lit le fichier rendu. |
| `tools/controle_python.py` | Contrôle Q3 (porte §G.1) côté Python : les blocs ```python publiés sont exécutés. |
| `tools/controle_refonte_M10.py` | controle_refonte_M10.py — le controle automatique du projet M10.P (« La refonte »). |
| `tools/controle_sql.py` | Contrôle Q3 de la porte de module (§G.1) : tout le SQL publié est exécuté. |
| `tools/controle_sql_M11.py` | controle_sql_M11.py — les tests de non-regression du module M11 (chapitre C07). |
| `tools/couleurs_M10.py` | couleurs_M10.py — la mesure du chapitre C03 : contraste, daltonisme, palettes. |
| `tools/dossier_M04.py` | dossier_M04.py — le « dossier pourri » du projet M04.P, généré de façon déterministe. |
| `tools/dossier_M05.py` | dossier_M05.py — le dossier du projet M05.P « Trois chemins, une même table propre ». |
| `tools/dossier_M06.py` | dossier_M06.py — le dossier du projet M06.P « La base de la quincaillerie ». |
| `tools/dossier_M07.py` | dossier_M07.py — le dossier du projet M07.P « La base commerciale d'une chaîne de 5 magasins ». |
| `tools/dossier_M08.py` |  |
| `tools/dossier_M09.py` |  |
| `tools/dossier_M10.py` | dossier_M10.py — le socle du module M10 (Data visualization). |
| `tools/dossier_M11.py` | dossier_M11.py — construit le socle SQL du module M11 (SQL avance pour la BI). |
| `tools/dossier_M12.py` | dossier_M12.py — construit le socle du module M12 (Fondamentaux de la Business Intelligence). |
| `tools/dossier_M13.py` | dossier_M13.py — construit le socle du module M13 (Modelisation des donnees). |
| `tools/ecriture_M10.py` | ecriture_M10.py — la mesure du chapitre C04 : titres, axes, annotations, ordre. |
| `tools/erreurs_M10.py` | erreurs_M10.py — le mur des 10 erreurs du chapitre C05, chacune mesuree sur le socle. |
| `tools/figures_M01.py` | Figures SVG du module M01. Style unique, texte en DejaVu Sans (police système du PDF). |
| `tools/figures_M02.py` | Figures SVG du module M02. Style identique à tools/figures_M01.py, texte en DejaVu Sans. |
| `tools/figures_M03.py` | figures_M03.py — les planches SVG du module M03 (Excel). |
| `tools/figures_M04.py` | figures_M04.py — les planches SVG du module M04 (qualité des données). |
| `tools/figures_M05.py` | figures_M05.py — les planches SVG du module M05 (langage commun des transformations). |
| `tools/figures_M06.py` | figures_M06.py — les planches SVG du module M06 (bases de données relationnelles). |
| `tools/figures_M07.py` | figures_M07.py — les planches SVG du module M07 (SQL : interroger, agreger, rejoindre). |
| `tools/figures_M08.py` | figures_M08.py — les planches SVG du module M08 (Python pour l'analyse de donnees). |
| `tools/figures_M09.py` | figures_M09.py — les planches SVG du module M09 (Analyse exploratoire de données). |
| `tools/figures_M10.py` | figures_M10.py — la recette des 7 planches du module M10 (Data visualization). |
| `tools/figures_M11.py` | figures_M11.py — les 2 planches du module M11 (SQL avance pour la BI). |
| `tools/figures_M12.py` | figures_M12.py — les 2 planches du module M12 (fondamentaux de la BI). |
| `tools/kit_exploitation.py` | kit_exploitation.py — le kit d'exploitation du manuel (M01 à M12 a ce jour). |
| `tools/kpi_M12.py` | kpi_M12.py — les 10 indicateurs du module M12, mesurés sur le socle. |
| `tools/modele_M13.py` | modele_M13.py — l'instrument du module M13 : le modele de Sahel Distribution, controle. |
| `tools/nb_pages.py` | Compte les pages d'un PDF produit par WeasyPrint. |
| `tools/outils_M10.py` | outils_M10.py — le meme graphique dans trois outils (C07) : matplotlib, Excel, Power BI. |
| `tools/perception_M10.py` | perception_M10.py — la mesure de l'etape 1 de C01 : le meme jeu de valeurs code |
| `tools/perf_M11.py` | perf_M11.py — l'instrument de mesure du chapitre C06 (requêtes lentes et plans). |
| `tools/poids.py` | poids.py — garde-fou de quota de l'atelier (128 Mo persistés). |
| `tools/render.py` |  |
| `tools/seize_graphiques_M10.py` | seize_graphiques_M10.py — le catalogue des 16 graphiques du manuel, exécuté sur le socle. |
| `tools/sequence_M10.py` | sequence_M10.py — la sequence de 3 ecrans du chapitre C06, en deux versions (direction, equipe). |
| `tools/pousser.sh` | publier le dépôt : contrôle d'abord, poussée ensuite |

---

## 6. Index des jeux de données

| Dossier | Contenu |
|---|---|
| `03_exercices/dossier_M04/` | 4 fichiers : `ATTENDU.json`, `clients_2026.csv`, `commandes_2026.csv`, `tarif_fournisseur.csv` |
| `03_exercices/dossier_M05/` | 4 fichiers : `ATTENDU.json`, `clients.csv`, `remises_2023_2024.xlsx`, `ventes_2023_2024.csv` |
| `03_exercices/dossier_M06/` | 4 fichiers : `ATTENDU.json`, `controles_integrite.sql`, `quincaillerie_export.csv`, `schema_3fn.sql` |
| `03_exercices/dossier_M07/` | 6 fichiers : `30_questions.sql`, `30_reponses.sql`, `6_pieges.md`, `ATTENDU.json`, `commercial.duckdb`, `commercial.sql` |
| `03_exercices/dossier_M08/` | 11 fichiers : `00_brief.md`, `ATTENDU.json`, `analyse_commerciale_modele.py`, `categorie.csv`, `client.csv`, `magasin.csv`, `mode_paiement.csv`, `objectif_magasin.csv` … |
| `03_exercices/dossier_M09/` | 6 fichiers : `00_brief.md`, `ATTENDU.json`, `projet`, `quincaillerie`, `sante`, `scolaire` |
| `03_exercices/dossier_M10/` | 5 fichiers : `00_brief.md`, `ATTENDU.json`, `exports`, `rapport_apres`, `rapport_avant` |
| `03_exercices/dossier_M11/` | 3 fichiers : `PERF_M11.json`, `connexion.py`, `socle_m11.sql` |
| `03_exercices/dossier_M12/` | 11 fichiers : `ATTENDU.json`, `__pycache__`, `commandes_clients.csv`, `connexion.py`, `cout_produits.csv`, `encaissements.csv`, `etude_avant.md`, `logistique_mensuelle.csv` … |
| `03_exercices/dossier_M13/` | 9 fichiers : `ATTENDU.json`, `__pycache__`, `connexion.py`, `modele_fautif.sql`, `mouvements_clients.csv`, `revue_modele.md`, `socle_m13.sql`, `table_plate.csv` … |

---

## 7. Mode d'emploi de l'appareil

- **Le cours** : les douze modules du livre assemblé, dans l'ordre, du sommaire général.
- **S'entraîner** : chaque chapitre porte ses exercices autonomes (section 11, ou 13 dans
  deux chapitres de M06) et leur correction détaillée juste après. **366** exercices, tous
  repris au corrigé — le contrôle est dans `kit_M01_M12.json`.
- **Un livrable de portfolio** : douze projets de module (partie II, premier cahier),
  chacun avec ses livrables et son barème.
- **Se faire évaluer** : douze évaluations (partie II, second cahier), avec seuils.
- **Exécuter** : `01_socle_donnees/scripts/chiffres_manuel.py` rejoue tous les chiffres du
  manuel ; `03_exercices/dossier_*/connexion.py` ouvre chaque dossier d'exercices.

Le sommaire de chaque module, à l'intérieur du livre, garde la pagination du module seul :
pour convertir en pages du livre, ajoutez le début de plage donné par le sommaire général,
moins un.
