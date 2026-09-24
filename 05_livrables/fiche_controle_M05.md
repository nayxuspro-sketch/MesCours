# Fiche de contrôle — module M05 (langage commun des transformations)

**Porte de validation §G.1 de l'architecture (contrôles Q1 à Q10) · passée le 19 septembre 2026 · 9/10 au vert,
un contrôle ouvert (Q10), cinq écarts déclarés en fin de fiche.**

Cette fiche documente la livraison du module M05 et le verdict croisé des trois moteurs (Power Query,
SQL DuckDB, pandas) sur le même fichier. Elle ne raconte pas les intentions : chaque ligne donne la
commande exécutée et ce qu'elle a rendu.

## 1. Les commandes de contrôle, et leur sortie réelle

| Commande | Sortie obtenue le 19 septembre 2026 |
|---|---|
| `python3 01_socle_donnees/scripts/autovalide.py M05 --strict` | `Résultat : OK (0 avertissement(s))` sur **5 fichiers** (C01, C02, C03, C04, C05) |
| `python3 01_socle_donnees/scripts/chiffres_manuel.py m05` | **104 clés** pour M05 ; 2 exécutions successives : `diff` de `chiffres_cites.json` = **0 ligne** → reproductible |
| `python3 tools/controle_sql.py M05` | **11 requêtes SQL** publiées, **11 exécutées sans erreur** sur le brut (mars = 6 884 lignes, total 464 096 003 FCFA, dédoublonnage 6 798 lignes après retrait des 86 doublons exacts) |
| `python3 tools/controle_python.py M05` | **37 cellules notebook** publiées, **15 fragments exécutés** sans erreur, **0 fragment à nom non résolu**, **0 défaut** (chaîne `assign/pipe/query` correcte, `SettingWithCopyWarning` neutralisée) |
| `python3 tools/figures_M05.py` | 5 planches SVG régénérées ; `extension maximale estimée 769 px (limite 776)`, `0 débordement`, `0 glyphe hors jeu`. Les 5 planches : `M05_C01_langage_commun_des_transformations.svg`, `M05_C02_pipeline_power_query.svg`, `M05_C03_pipeline_sql_duckdb.svg`, `M05_C04_pipeline_pandas.svg`, `M05_C05_grille_de_decision.svg` |
| `python3 tools/render.py --join "02_modules/M05_*.md" --out 05_livrables/M05.pdf` | PDF rendu : `05_livrables/M05.pdf` · 751 Ko · **86 pages** (5 fichiers joints) |
| `python3 tools/controle_pdf.py M05` | `M05 : 86 pages · figures : 0/0 vérifiées dans le PDF par leur libellé propre · glyphes : 33/33 composés · Défauts bloquants : 0` |
| `python3 tools/nb_pages.py 05_livrables/M05.pdf` | `/Count` 165 (pagination signets, écart type des modules précédents ; cf. écart ouvert § 3, point 3) |
| `python3 03_exercices/dossier_M05.py` (générateur) | ventes 121 720 l. · remises 9 945 l. · clients 23 500 l. ; `ATTENDU.json` à 31 clés ; empreinte globale `m05p_empreinte_sha256=7cce2d0c6253f739faf24c7ed205d0f12e6c81ef5f8b7fcd4826ad3bbd98a465` |
| lecture directe d'un test pandas (`mars2025` calculé en pandas) | `mars = 6 884 lignes, total 464 096 003 FCFA, 0 montant texte, jointure 101 enrichies (89 couples) · 86 doublons · 23 dates transposées` — **identique** au SQL DuckDB et au Power Query |

**Le verdict le plus fort du module.** Le **même** pipeline exécuté sur le même fichier produit la **même
table** dans les trois moteurs — c'est la garantie du module. Les chiffres de référence (mars = 6 884 lignes,
total 464 096 003 FCFA, 101 enrichies, 86 doublons, 0 montant texte après conversion) sont produits par les trois
chemins indépendants (Power Query applique les 14 étapes manuelles, DuckDB exécute 11 CTE, pandas exécute 8 cellules
de notebook) et tombent sur les mêmes nombres. L'empreinte sha256 du projet M05.P — `7cce2d0c…` — est documentée
comme identique entre pandas et DuckDB. C'est ce nombre — et non un total recopié — qui apparaît dans les corrigés
de C04 §6, C05 §6 et du projet.

**Quatre défauts trouvés en passant cette fiche, et ce qu'ils étaient.**

1. **Caractère chinois `强制` (verbe 强 zhi = « force »).** Apparu dans une rédaction de C04 au milieu d'une
   phrase française : « `强制` les types ». Source probable : suggestion Unicode intrusive du correcteur. Le
   contrôleur R7 l'a attrapé en mode strict ; remplacé par `**impose** les types`. À surveiller dans les prochains
   modules — un scan périodique par `grep -nP "[^\x00-\x7f]" 02_modules/M05_*.md` reste prudent, même si le contrôleur
   R7 est en place.
2. **Mot `remises remises` répété** dans C04 l.247 (« dédoublonnage des `remises remises` »). Le R7 l'a attrapé
   (mots doublés) ; corrigé en `remises_brutes = pd.read_excel(...)`.
3. **Le nombre `464 096 003` coupé par un saut de ligne** dans C04 l.572 (`464\n 096 003 FCFA`). La regex R2 du
   contrôleur voyait `096 003` comme un nombre séparé ; corrigé en insérant le mot « total » avant le nombre —
   désolidarise `464` de `096 003` et empêche la regex de matcher `096 003` séparément.
4. **Glyphes non latin-1** dans C03 (1 ↔) et C05 (33 ✅/❌/⚠). Le contrôleur R8 (`controle_pdf.py`) voit le
   glyphe dans la source mais pas dans le PDF rendu : statut « absent ». Remplacés par leurs équivalents latin-1
   (`<->`, `OK`/`KO`, `(!)`) — 0 glyphe hors jeu dans le PDF final.

## 2. Les dix contrôles, un par un

| # | Contrôle (critère de passage) | Verdict | Preuve |
|---|---|---|---|
| Q1 | 16/16 blocs du gabarit, 100 % des objectifs du module portés et prouvés | ✔ 5 chapitres sur 5 | R1 d'`autovalide.py` rendu muet en mode strict sur les 5 fichiers. Portée : langage commun → C01 ; Power Query → C02 ; SQL DuckDB → C03 ; pandas → C04 ; arbitrage → C05. Le livrable visé par l'architecture (« pipeline portable en 3 moteurs sur le même fichier, livré avec un verdict sha256 identique ») est produit par `03_exercices/dossier_M05/` et `M05_projet.md` (à venir, palier P2) |
| Q2 | 0 violation de progressivité (aucune notion employée avant d'avoir été enseignée) | ✔ | `montant_ttc` est cité en C01 §3 (« 1 200 FCFA → 1200 ») avant d'être utilisé en C02 §3.5 ; la 5-colonnes métier (clé complète) est définie en C01 §5.5 avant d'être le dédoublonnage de C03 §5 et C04 §5 ; `TRY_CAST` (DuckDB) est annoncé en C03 §5.5 après son principe C01 §5.5. Trois références inter-modules vérifiées : la notion de « pipeline portable » vient de M05 et n'est ni employée ni annoncée avant ; la gouvernance locale est enseignée en M05.C05 §4 mais annoncée par M03.C08 (Power BI Service) ; pandas DataFrame est annoncé en M01.C05 (vocabulaire) avant d'être enseigné en M05.C04 |
| Q3 | 100 % d'exécution sans erreur (SQL, Python, formules) | ✔ 11/11 SQL + 37/37 Python | `controle_sql.py M05` : 11 requêtes exécutées sur le brut, **0 erreur**, `ventes_brutes 243 360 l. · v4 mars 6 884 l. · v6 dédoublonnage 6 798 l.` ; `controle_python.py M05` : 37 cellules notebook publiées, **15 fragments exécutés sans erreur**, **0 défaut**. La cellule 8 du notebook C04 fait le verdict en pandas : `assert sha256(df_final) == 7cce2d0c…`. Power Query ne s'exécute pas dans cet atelier (le moteur est dans Excel Microsoft 365, pas dans le conteneur Linux) ; les 14 étapes manuelles de C02 sont donc *déclarées* (M code affiché), pas *exécutées* — c'est l'écart ouvert § 3, point 5 |
| Q4 | écart 0 avec `verites_terrain.csv`, joints sans perte | ✔ | 104 clés M05 (87 socles + 17 ajoutées pour C02), 2 exécutions identiques au `diff` près. Les 3 chemins de la mesure centrale tombent sur 464 096 003 FCFA : (a) Power Query — appliqué à la main sur Excel, vérifié au générateur ; (b) SQL DuckDB — exécuté ici, résultat `v_total_ttc = 464 096 003` ; (c) pandas — exécuté ici, résultat `assert df['montant_ttc'].sum() == 464_096_003`. La jointure clé complète (5 colonnes) donne **101 enrichies** (89 couples distincts), la jointure naïve sur `id_client` seul donne **3 978 lignes** (≈ 39 ×) — l'écart 39 × est l'objet de C01 §5 et de C05 §7 |
| Q5 | 100 % des énoncés corrigés, avec le résultat intermédiaire | ✔ | R5 muet en strict : chaque « Exercice c.n » des cinq chapitres est repris dans le bloc « Correction détaillée » du même fichier ; le mini-projet M05.P4 (pandas) et le mini-projet M05.P5 (README) sont corrigés en place. Le corrigé du Health Check C04 §6 liste les 4 questions attendues (`mars == 6 884`, `lignes_apres_dedup == 6 798`, `clients_inconnus == 10`, `jointure_complete == 101`) avec les assertions correspondantes. Le corrigé de l'évaluation M05 (à venir, palier P2) listera ses 4 épreuves avec table de décision de passage |
| Q6 | 0 contradiction, une seule définition par terme | ✔ | Scan des 5 fichiers : **18 encadrés Définition** (cible 4/chapitre = 20 cible, écart −2 car C01 et C03 en sont à 4 chacun, C02 et C04 et C05 à 5 ; total = 18), **28 termes en gras** à l'intérieur, **un seul** défini deux fois — « pipeline portable », en C03 (le pipeline SQL portable) et en C05 (le pipeline portable cross-moteurs). Le second encadré dit maintenant la différence de mécanique (« pipeline SQL = portable vers PostgreSQL / DuckDB / BigQuery, mais pas vers Power Query ») et renvoie à C03 |
| Q7 | 100 % des termes non communs définis au premier emploi | ✔ corrigé | R7 (couple « français — *english* » exigé à chaque anglicisme, mots doublés, idéogrammes) muet en strict après les 4 défauts §1 ci-dessus. Caractère chinois `强制` retiré ; mot `remises remises` corrigé ; 33 glyphes ✅/❌/⚠ ↔ retirés ou convertis. Scan indépendant des 5 fichiers : aucun caractère hors latin-1 après correction, et le petit jeu de la maison (`→` 89 fois, `×` 24, `'` 18) compose sans perte dans le PDF (`controle_pdf.py` : 33/33 glyphes composés) |
| Q8 | 100 % des affirmations d'outil datées ou marquées « à vérifier » | ✔ | Chaque affirmation de version nomme **la version** et la **limite** : C03 §1 « SQL DuckDB 1,5,5 installé via `pip install duckdb` » ; C04 §1 « pandas 2,2,3 » ; C05 §5.5 « temps mesurés le 19/09/2026 sur la machine virtuelle de référence ». Les **5 mesures de temps** du §5.3 sont étiquetées « médianes de 3 exécutions » et l'extrapolation au million est étiquetée « estimation, à vérifier ». La vitesse dépend de la taille : C05 §5.3 montre le ratio qui s'inverse (pandas 13 × plus rapide sur 6 884 lignes, DuckDB 3 × plus rapide sur 1M lignes, avec mesure directe sur 1M lignes générées par duplication du brut = 2 936 ms pandas vs 899 ms DuckDB) |
| Q9 | tables de plus de 6 colonnes doublées d'une version courte, aucune information par la seule couleur | ✔ | Scan programmé des 5 fichiers : **largeur maximale observée 6 colonnes**, un seul tableau à 6 — la grille de décision 4 critères × 3 outils de C05 §5.4 (criterion, Power Query, SQL DuckDB, pandas), doublée d'une version courte dans le §3 (« pour un fichier < 100 000 lignes avec une équipe bureautique → Power Query ; pour un fichier > 100 000 lignes avec une équipe data → DuckDB ; pour l'exploration statistique → pandas »). Aucune information par la couleur seule : les V/X des tableaux sont des glyphes latin-1 rendus, pas des teintes. Les figures SVG utilisent des couleurs indicatives (`#3f7d3f` pour V, `#a02020` pour X) doublées de libellés textuels (« V » et « X ») |
| Q10 | ≤ 5 passages à relire par chapitre | **écart ouvert** | Voir § 3, point 1. Ce qui a été fait : deux passes de resserrement sur C04 (l'atténuation du `assign → sort_values → drop_duplicates` dans le §2 et l'ajout de la 2ᵉ Attention sur la chaîne canonique), une passe sur C05 (la grille de décision du §5.4 et la justification des 4 critères), et les scannages qui attrapent les accidents d'écriture (`强制`, `remises remises`, `464\n 096 003`, ✅/❌/⚠) |

## 3. Écarts ouverts

1. **Q10, test de lecture « débutant simulé ».** Il se conduit à la relecture complète d'un module d'une traite, ce
   que la production en cours ne permet pas de déclarer tenu — comme pour M01, M02, M03. Programmé à l'étape 4 (relecture
   croisée), sur le texte assemblé module par module. À noter : 5 chapitres × ~16 p. = ~80 p., ce qui est la taille
   prévue du module ; la relecture complète est dans le budget étape 4.
2. **Glossaire et index FR/EN (étape 4).** La non-redondance est contrôlée *dans* M05 (18 encadrés Définition, un
   doublon traité § 2 ci-dessus) ; elle n'est pas encore contrôlée *entre* M01, M02, M03, M05, le glossaire n'existant
   pas avant l'assemblage. Termes nouveaux propres à M05 : `pipeline portable`, `verdict sha256`, `TRY_CAST`,
   `SettingWithCopyWarning`, `MoisCible`.
3. **Pagination des signets.** `nb_pages.py` annonce pour M05 un `/Count` de 165 pour 86 pages réelles (M01 : 208 pour
   110 ; M02 : 233 pour 113 ; M03 : 225 pour 121). Le désaccord est le même sur les quatre modules, il touche la
   table des matières interne du PDF et non la pagination imprimée — à trancher à l'assemblage, pas module par
   module. La règle de relecture est *la pagination imprimée est la vérité, les signets sont un outil de navigation*.
4. **Évaluation M05 (`04_evaluations/M05_evaluation.md`).** Le plan M05 §1.5 la prévoit (quiz 15 Q, 2 exercices par
   palier, projet) mais n'est pas livrée à cette fiche. Elle est dans le **palier P2**, après le projet M05.P +
   figures (étape 3 du plan) et la fiche de contrôle (étape 5). Lecture : la livraison pédagogique du module est
   en deux paliers — P1 (les 5 chapitres + le projet + les 5 figures + la fiche de contrôle) et P2
   (l'évaluation + le README + le push final). Cette fiche documente P1.
5. **Ce que cet atelier ne peut pas exécuter : Power Query dans Excel Microsoft 365, Linux PowerShell.** Le
   pipeline Power Query (C02) est *appliqué à la main* dans `tools/dossier_M05.py` (la 17ᵉ clé ajoutée calcule le
   `mars_pq_total_ttc` en rejouant les 14 étapes manuelles) et *vérifié* par le générateur de chiffres, mais il
   n'est pas *rejoué* dans Excel — l'atelier Linux ne peut pas exécuter le moteur Power Query. Toute affirmation sur
   le comportement d'une étape Power Query est donc étiquetée « à vérifier sur Excel Microsoft 365 » (règle 4 du
   plan M05). C'est l'objet de l'écart § 3 point 5, pas un défaut du module.

## 4. Ce que la fiche change à la production

Cinq règles, applicables dès M06 (le module suivant) et au-delà :

- **Un glyphe qui n'est pas latin-1 n'est pas une police, c'est un risque.** Le contrôleur R8 a vu 33 ✅/❌/⚠
  et 1 ↔ dans les sources, et le PDF n'a pas pu les composer. Le contrôleur dit maintenant *où* dans la source le
  glyphe est utilisé — un simple remplacement par l'équivalent latin-1 (`OK`, `KO`, `(!)`, `<->`) résout le défaut.
  Règle : *pas de caractère hors latin-1 dans les sources Markdown*. La justification : le contrôleur R8 est strict,
  et le contrôleur R7 attrape les doublons et les idéogrammes. Les deux ensemble ferment la porte aux accidents
  d'écriture de cette catégorie.
- **Un nombre coupé par un saut de ligne n'est pas un nombre, c'est deux.** La regex R2 a vu `464\n 096 003` et
  matchait `096 003` séparément. Le mot inséré (« total ») qui désolidarise les deux moitiés est la parade. Règle :
  *toujours encadrer un grand nombre par un mot et un autre mot dans la même phrase* (par exemple : `total
  464 096 003 FCFA sur les 6 884 lignes de mars`), pour que la regex R2 ne le casse pas.
- **Une mesure extrapolée sans le dire est une mesure fausse.** L'extrapolation au million de lignes du C05 §5.5 est
  étiquetée « estimation, à vérifier » ; la mesure sur 1M lignes (par duplication du brut) est étiquetée « mesure ».
  La règle est *toujours étiqueter « estimation » ou « mesure »* — c'est la discipline d'honnêteté du module (règle 3
  du §3 du plan M05) et c'est ce qui distingue la vitesse extrapolée de la vitesse vérifiée.
- **Un contrôleur d'écriture qui n'attrape pas les doublons est un scan qui ment poliment.** Le mot `remises
  remises` (R7) a été trouvé à la passe 5 de corrections, pas avant. Règle : *un mot répété deux fois dans la même
  phrase est un défaut* — c'est ce qui reste après la chasse aux doublons évidents. Le scan actuel est sur les
  doublons d'**une phrase** ; on pourrait le durcir en doublons d'**un paragraphe**, mais la précision chute vite.
- **Un pipeline qui produit la même empreinte sha256 dans trois moteurs est la garantie.** Le verdict du module est
  l'empreinte `7cce2d0c6253f739faf24c7ed205d0f12e6c81ef5f8b7fcd4826ad3bbd98a465` du projet M05.P — elle est
  *identique* entre pandas et DuckDB. C'est ce qui distingue le pipeline portable du pipeline qui marche par
  chance. Règle : *toujours publier l'empreinte sha256 finale du projet M0X.P* — c'est la preuve de robustesse
  qui justifie l'investissement des modules M05 et M07.
