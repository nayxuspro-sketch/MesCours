# Projet M05.P — « Trois chemins, une même table propre »

**Module M05 · projet de fin de module · 6 h · barème /20, seuil de passage 13/20**

> **Le cadre réel.** Un data analyst d'une enseigne de distribution à Ouagadougou reçoit chaque matin
> trois versions du même fichier de ventes (une de la caisse, une du back-office, une de l'intégration
> comptable), et la question qui revient tous les lundis est : *« pourquoi vos trois chiffres ne tombent
> pas juste ? »* Vous rendez la même table propre dans **trois moteurs** (Power Query, SQL DuckDB,
> pandas), vous prouvez qu'ils produisent la **même** empreinte sha256, et vous documentez le **choix
> d'outil** par les 4 critères du C05 §7. C'est la synthèse des cinq chapitres : chaque livrable en
> mobilise un, et aucun n'est noté pour lui-même.

> **Note de cohérence.** Le dossier est généré de façon déterministe par `python3 tools/dossier_M05.py`
> (graine 42) : qui que vous soyez, vous touchez les mêmes 121 720 lignes de ventes. `03_exercices/dossier_M05/ATTENDU.json`
> contient les **31 clés** des résultats attendus, **mesurés sur le dossier généré, jamais déduits** :
> vous n'y recourez qu'après avoir produit vos propres nombres, pour comparer, pas pour copier. Un
> candidat qui lit l'`ATTENDU` avant de calculer n'a plus rien à rendre. Les chiffres de ce corrigé sont
> ceux du dossier livré, vérifiables ligne à ligne.

---

## 1. Énoncé

### Le matériel

| Élément | Chemin | Ce que c'est |
|---|---|---|
| Ventes | `03_exercices/dossier_M05/ventes_2023_2024.csv` | 121 720 lignes, 20 colonnes, encodage UTF-8, séparateur virgule, **9 défauts** à 9 endroits (texte, doublons, dates, jointure, encodage, taille, retours, remise, transposition invisible) |
| Remises | `03_exercices/dossier_M05/remises_2023_2024.xlsx` | 9 942 lignes, 7 colonnes, Excel `.xlsx` (openpyxl) ; 35 couples ressaisis sur 9 907 uniques |
| Clients | `03_exercices/dossier_M05/clients.csv` | 23 500 lignes, 9 colonnes, CSV simple ; 252 clients inconnus côté ventes |
| Résultats attendus | `03_exercices/dossier_M05/ATTENDU.json` | 31 clés — à utiliser **après** le calcul, jamais comme source de copie |
| Outils | trois moteurs — au moins **deux** obligatoires, **trois** pour la note pleine | Power Query (si Excel), SQL DuckDB (Python), pandas (Python) |

Le dossier contient **neuf défauts de natures différentes** ; **quatre** d'entre eux cassent le total
`total_ttc_avant_dedoublonnage` (avant réparation), les **cinq** autres cassent soit une analyse (remises
hors domaine), soit une jointure (clients inconnus), soit un import (taille 28 Mo, encodage), soit une
régression (lignes légitimes mangées par une clé trop agressive). Trouver les neuf, les réparer dans
**deux moteurs** indépendants, prouver que les deux tables sont identiques au byte près (sha256), et
expliquer dans quel cas le troisième moteur est nécessaire : c'est la moitié de la note. L'autre moitié
est la **trace écrite** : le journal, le README, et le verdict de la convergence.

### Les six livrables

**D1 — La grille de diagnostic** (3 points). La grille des 12 points du M04.C01, passée sur
`ventes_2023_2024.csv`. Pour chaque point non nul, le compteur **avec son dénominateur** (« 1 731 sur
121 720 », jamais « 1 731 »). Vous identifiez les 4 défauts qui cassent le total et les 5 qui ne le
cassent pas, et vous écrivez la phrase qui prouve la séparation (cf. C01 §5.1).

**D2 — Le pipeline de réparation** (4 points). La séquence canonique du C01 §5.5 appliquée au brut
donne un DataFrame final `df_final` à **120 000 lignes** (cible `lignes_final`), **total TTC
7 145 910 735 FCFA** (cible `total_ttc_final`). Cette cible est *mesurée* sur le dossier généré, pas
*visée* aveuglément. Les 1 720 doublons retirés (`doublons_a_retirer`) s'écrivent dans le journal avec
leur motif : 1 680 copies exactes (5 colonnes identiques : ticket + produit + quantité + TTC + heure —
`ventes_copies_ressaisies`) et 40 variantes qui ne modifient qu'un seul champ (la date — `ventes_resaisies_date`).
Le piège est qu'une règle « drop_duplicates » sans tri préalable rate la moitié des défauts, et qu'une
règle trop agressive (« clé = id_ticket seul », sans regarder `id_produit`, `quantité`, `montant_ttc` ou
`heure`) mange 3 lignes légitimes (`lignes_legitimes_mangees_cle_sans_heure` dans l'`ATTENDU`) et tombe
à un total inférieur à la cible — vous écrivez ce que cette règle a mangé, et vous chiffrez l'écart.

**D3 — Les trois pipelines et leurs verdicts** (4 points). Trois exécutions, une empreinte sha256
unique : `7cce2d0c6253f739faf24c7ed205d0f12e6c81ef5f8b7fcd4826ad3bbd98a465`. Vous rendez :
- (a) la requête SQL DuckDB **exécutée** sur le brut (vérifiable par `python3 tools/controle_sql.py M05`) ;
- (b) le notebook pandas **exécuté** sur le brut (vérifiable par `python3 tools/controle_python.py M05`) ;
- (c) le script Power Query **documenté** (M code étape par étape, *non exécutable* dans cet atelier — c'est
  la limite de la règle 7 du plan M05 §3).

La mesure est : `df_final` pandas ET la table DuckDB, sérialisés en Parquet avec `sort_values(id_vente)`,
produisent la même empreinte sha256. Le candidat qui n'a qu'un seul moteur ne peut pas produire cette preuve :
il rend une table propre, mais il ne prouve pas la robustesse.

**D4 — Le journal des transformations et le README du dossier** (3 points). Six lignes au format du C06
(date, fichier, opération, règle, compteur avant → après), couvrant au minimum : (1) la conversion des 1 731
montants texte (`"1 200 FCFA"` → `1200`), (2) la transposition des 493 dates jour-mois (`dates_transposees_reparees`),
(3) le dédoublonnage 1 720 (1 680 copies exactes + 40 variantes de date), (4) la jointure clients avec
clé complète (1 714 enrichies `lignes_jointure_cle_complette` contre 41 716 naïves `lignes_jointure_naive_id_client`),
(5) l'export Parquet (empreinte sha256 notée), (6) le verdict croisé (les 3 moteurs produisent la même
empreinte). Le README (4 sections, 40 lignes de cible) : scénario, tables avec leur grain, défauts constatés,
ce qui manque volontairement. Il justifie **par les 4 critères du C05 §7** (taille, fréquence, compétences,
gouvernance) le choix de DuckDB en première intention et pandas en repli.

**D5 — Le contrôle final avec ses résidus attendus** (3 points). La grille des 12 points du M04.C01 sur
`df_final`, avec les **résidus attendus écrits avant** le contrôle : 0 montant non numérique, 0 remise
hors [0 ; 0,3] (à condition d'avoir traité les 488 remises en points `remises_hors_domaine`), 0 date hors
plage [2023-01-01 ; 2024-12-31], 0 groupe de doublon, 0 client inconnu (252 ramenés à 0 par la jointure clé
complète). La convergence est écrite avec l'écart : votre total `7 145 910 735 FCFA` contre l'`ATTENDU.json`
`total_ttc_final`, écart 0. **L'écart est le chiffre à énoncer**, pas le total.

**D6 — L'arbitrage DuckDB / pandas / Power Query pour le dossier** (3 points). Pour les 4 critères
(taille, fréquence, compétences, gouvernance) du C05 §7, vous écrivez le verdict **de votre équipe**
(qui n'est pas forcément celle de l'énoncé) et la **règle de bascule** : « si le critère X change de
valeur, on change d'outil et on documente le changement ». Le piège est de justifier le choix sans
l'avoir **mesuré** : un test pandas + DuckDB sur 121 720 lignes est attendu (les chiffres du C05 §5.3
sont là pour ça — pandas ≈ 1,4 × DuckDB sur 120 000 lignes).

---

## 2. Ce qui est noté, ce qui est piégé

| Piège du dossier | Où il se cache | Ce qu'il enseigne |
|---|---|---|
| 1 731 montants en texte (« 1 200 FCFA ») | `ventes_2023_2024.csv`, colonne M (`montants_en_texte`) | la somme directe rate 1 731 lignes ; la conversion par TRY_CAST Pandas/Power Query ne suffit pas, il faut d'abord normaliser l'espace et la devise |
| 1 720 doublons (1 680 exacts + 40 variantes) | `ventes_2023_2024.csv` (`doublons_a_retirer`) | les doublons *apparaissent* après conversion : avant, « 1 200 FCFA » ≠ « 1200 » ; les 40 variantes ne diffèrent que d'un champ (la date), pas 5 — la règle « drop_duplicates sur 5 colonnes » les attrape |
| 493 dates transposées (jour-mois) | `ventes_2023_2024.csv`, colonne C (`dates_transposees_reparees`) | le tri chronologique et la coupe à la date sont faux tant que les deux écritures cohabitent ; c'est l'objet du M04 erratum §7 (945 sur tout le fichier, 493 dans la fenêtre projet) |
| 252 clients inconnus (id_client ≥ 900 000) | `ventes_2023_2024.csv` (jointure) `clients.csv` | la jointure naïve sur `id_client` donne 41 716 enrichissements faux (`lignes_jointure_naive_id_client`) au lieu de 1 714 (`lignes_jointure_cle_complette`) — un facteur 24 × |
| 488 remises hors domaine (saisies 12/18/25…) | `ventes_2023_2024.csv`, colonne K (`remises_hors_domaine`) | la division par 100 est un test, pas une réparation universelle |
| 1 510 retours (montants négatifs) | `ventes_2023_2024.csv` (`retours`) | la conversion les fait passer en valeurs négatives ; le filtre « montant < 0 » les isole |
| Encodage UTF-8 + 121 720 lignes (≈ 14 Mo) | tout le fichier | Excel ouvre le fichier mais le **recalcule** sur 14 Mo est lent (> 30 s) — borderline par rapport à la règle 100k de C05 §5.1 |
| 3 lignes légitimes perdues si clé = id_ticket seul | `ventes_2023_2024.csv` (`lignes_legitimes_mangees_cle_sans_heure`) | la clé juste est 5 colonnes : id_ticket + id_produit + quantité + TTC + heure ; sans l'heure, deux lignes du même ticket (heures différentes) sont mangées |
| 3 défauts non visibles au format (transpositions pures) | `ventes_2023_2024.csv` colonne C | le contrôle de format passe, le contrôle de valeur échoue — c'est la leçon de l'E4 de M04 |

---

## 3. Barème et seuil

- **D1** : 3 points — grille complète avec dénominateurs (1) · les 9 défauts en 2 natures (1) · la phrase de
  séparation des totaux (1).
- **D2** : 4 points — total `7 145 910 735 FCFA` obtenu par votre méthode (1,5) · les 1 720 doublons motivés
  ligne à ligne (1) · le verdict `try_cast()` vs `TRY_CAST SQL` (1,5).
- **D3** : 4 points — pandas **et** DuckDB exécutés, sha256 identique (2) · Power Query documenté mais non
  exécutable, comparaison par le total (1) · le verdict croisé (1).
- **D4** : 3 points — six lignes au format complet (1) · chaque ligne se referme par son écart (1) · README
  + arbitrage par les 4 critères (1).
- **D5** : 3 points — résidus attendus écrits avant le contrôle (1) · grille du `df_final` avec convergence
  écrite (1) · écart 0 contre `total_ttc_final` (1).
- **D6** : 3 points — les 4 critères **mesurés** sur le dossier (1) · règle de bascule explicite (1) ·
  comparaison avec les 5 chiffres du C05 §5.3 (1).

**Seuil de validation : 13/20.** Un livrable dont un compteur manque son dénominateur perd 0,5 point par
compteur, sans plafond : la précision du dénominateur est la matière du module, pas une coquille.

---

## 4. Correction des points d'attention

- **D1, séparation des totaux.** La somme directe sur la colonne M convertie rate ~1 731 lignes sur le brut
  (`montants_en_texte`), soit 0 sur le total de référence ; après conversion, le total `total_ttc_avant_dedoublonnage`
  = `7 242 884 579 FCFA`. Les doublons la faussent en double comptant 1 680 copies (les 40 variantes se
  neutralisent par les conversions). Les 493 dates transposées ne touchent pas au total TTC mais déplacent
  493 lignes entre mois — la *coupe à la date* est alors fausse, mais le *total global* est juste. Les 252
  clients inconnus ne touchent pas au total TTC mais faussent la jointure. La phrase attendue : « Quatre
  défauts touchent au total — 1 731 montants en texte non sommés, 1 720 doublons dont 1 680 copies exactes,
  252 clients inconnus que la jointure naïve gonfle, et 493 dates transposées qui déplacent des lignes entre
  mois ; les cinq autres — 488 remises en points, 1 510 retours, encodage, 121 720 lignes, 3 lignes légitimes
  mangées par une clé trop courte — faussent chacun une lecture différente du fichier sans toucher à la
  somme globale. »
- **D2, le pipeline canonique.** C'est la leçon du C01 §5.5 : convertir **avant** de dédoublonner, parce
  que « 1 200 FCFA » et `1200` sont *égaux* après conversion et *différents* avant. La règle de dédoublonnage
  qui s'applique sur la colonne M *non convertie* rate la moitié des doublons. La séquence qui passe le
  contrôle du contrôleur est : (1) `assign(montant_ttc_n = TRY_CAST(...))`, (2)
  `sort_values(['date_vente','id_vente'])`, (3) `drop_duplicates(CLE, keep='first')` avec
  `CLE = ['id_ticket','id_produit','quantite','montant_ttc_n','heure']`. Réciproquement en SQL : `TRY_CAST`
  *avant* `ROW_NUMBER OVER (PARTITION BY CLE)`.
- **D2, le piège des 3 lignes légitimes.** La règle naïve « clé = id_ticket seul » (sans `id_produit`,
  sans `quantité`, sans `montant_ttc_n`, sans `heure`) tombe à un total inférieur à la cible : les 3
  lignes mangées sont des ventes multi-lignes *légitimes* (même ticket, produits différents, heures
  différentes) — c'est l'objet de la clé `lignes_legitimes_mangees_cle_sans_heure = 3` dans l'ATTENDU.
  La clé juste doit inclure **les 5 colonnes** pour survivre à ces cas. La chute est petite en valeur
  absolue, mais c'est l'écart *caché* : l'apprenti n'a aucun moyen de voir qu'il a perdu 3 lignes
  sans recourir à l'ATTENDU.
- **D3, le verdict sha256.** L'empreinte `7cce2d0c6253f739faf24c7ed205d0f12e6c81ef5f8b7fcd4826ad3bbd98a465`
  est mesurée sur la **sérialisation Parquet** de `df_final.sort_values(['id_vente'])`. Pandas et DuckDB la
  produisent à l'identique au byte près (vérifié par `controle_python.py` et `controle_sql.py`). Power
  Query est exclu parce que l'atelier ne peut pas exécuter Excel — la note tolère cette absence à
  condition que le **total** `7 145 910 735 FCFA` soit annoncé et qu'il soit cohérent avec celui de
  pandas et DuckDB (cohérent *au centime près*).
- **D5, les résidus attendus.** « 0 non numérique, 0 hors domaine, 0 hors plage, 0 groupe de doublon, 0
  client inconnu » — les cinq zéros sont écrits **avant** le contrôle. Un contrôle qui s'attendrait à
  autre chose rejette le bon fichier. La convergence s'écrit avec l'écart (0) — pas avec le total répété.
- **D6, la règle de bascule.** « Si le fichier dépasse 500 000 lignes, on bascule sur DuckDB ; si l'équipe
  ne fait pas de Python, on bascule sur Power Query ; si la gouvernance exige un schéma SQL centralisé, on
  bascule sur DuckDB ». Trois règles, trois critères, et c'est cette réversibilité qui fait que le choix
  n'est pas une opinion, c'est une **décision**.
- **L'arbitrage par les mesures du C05 §5.3.** Sur 121 720 lignes (projet), DuckDB et pandas sont à
  ≈ 1,4 × l'un de l'autre (DuckDB légèrement plus rapide). Sur 740 lignes (mars 2025 du brut, avant
  fenêtrage), pandas reste largement plus rapide (DuckDB pâtit du chargement initial). Le **choix**
  DuckDB/pandas ne dépend donc pas de la taille seule, mais de la *prévision* : si le fichier grossit
  vers 500k+ lignes, DuckDB reste meilleur ; si le fichier reste à 100k lignes, pandas est plus rapide à
  froid. La règle du module est *DuckDB en première intention* (portable, plus rapide à l'échelle), *pandas
  en repli* (plus riche en méthodes, plus rapide à froid).
