# Évaluation M05 — « Le langage commun des transformations »

**Module M05 · durée totale 2 h 30 · quatre épreuves · seuils : quiz 11/15, exercices 14/20, étude de cas 12/20**

| Épreuve | Durée | Barème | Noté | Ce qui est attendu |
|---|---|---|---|---|
| A · Questions de récupération | 15 min | non noté | non | vérifier qu'on a lu les cinq chapitres avant de se tromper cher |
| B · Quiz | 25 min | /15 | oui | quinze questions à réponse unique, cinq blocs |
| C · Exercices pratiques | 50 min | /20 (auto-corrigé) | oui | quatre exercices menés jusqu'au chiffre sur le dossier du projet |
| D · Étude de cas | 60 min | /20, seuil 12 | oui | un dossier en quatre pages : « un pipeline, trois moteurs — qui dit la même chose ? » |

> Le score du module se lit ainsi : **B ≥ 11** et **D ≥ 12** valident le module ; le projet M05.P doit atteindre 13.
> Un candidat qui réussit B et échoue à D repasse uniquement D : savoir ce qu'est un pipeline portable ne
> dispense pas de dire si deux moteurs produisent la même table au byte près.
> Tout nombre de cette évaluation est mesuré sur le socle livré ; les corrections le citent avec leur clé
> `m05_*`/`m05p_*` dans `chiffres_cites.json`.

---

## A · Questions de récupération (non notées)

À traiter sans document, en une ou deux phrases chacune. Elles ne sont pas comptées ; elles servent à repérer ce
qui n'est pas assimilé avant de perdre des points sur un détail.

1. Citez les **10 opérations** du langage commun de C01 et la classe (M, Opérateur, Paramètre, Agrégation) de chacune.
2. Donnez les **14 étapes** du pipeline Power Query du C02 (sommaire, en groupes : source → typage → réparation →
   jointure → sortie).
3. Citez les **11 tables temporaires** (v1 à v6 du corrigé) du pipeline SQL DuckDB de C03, et la règle de transition
   entre deux tables consécutives.
4. Donnez les **8 cellules** du notebook pandas de C04 (en-têtes sans code) et la chaîne de méthodes canonique
   `assign` → `sort_values` → `drop_duplicates`.
5. Citez les **4 critères** du choix d'outil de C05, et pour chacun le seuil indicatif qui fait basculer le choix
   (par exemple : < 100 000 lignes pour la taille).
6. Pourquoi la séquence « dédoublonner **avant** la conversion des montants texte » est-elle fausse dans 50 %
   des cas du projet ?
7. Quelle est la différence entre le verdict du fil rouge (mars 2025 = 6 884 lignes) et l'empreinte sha256 du
   projet M05.P (`7cce2d0c…`) ? Pourquoi les deux sont-ils nécessaires ?

---

## B · Quiz (15 questions · 15 points)

**Barème : 1 point par question, une seule bonne réponse. Les réponses justifiées en une ligne rapportent un
demi-point de bonus, plafonné à 15.**

### Bloc 1 — Le langage commun (Q1 à Q3)

**Q1.** Le pipeline Power Query, SQL DuckDB et pandas partagent une grammaire commune. Le verbe « promote headers »
appartient à : a) la classe M · b) la classe Opérateur · c) la classe Paramètre · d) la classe Agrégation.

**Q2.** L'opération `TRY_CAST(REPLACE(REPLACE(montant_ttc, ' FCFA', ''), ' ', '') AS BIGINT)` se traduit en pandas par :
a) `df['montant_ttc'].astype(int)` · b) `pd.to_numeric(df['montant_ttc'].str.replace(' FCFA', '', regex=False).str.replace(' ', '', regex=False), errors='coerce')` · c) `df.assign(montant_ttc=int)` · d) une boucle `for` sur les lignes.

**Q3.** Le paramètre `MoisCible = 3` lit en réalité la cellule `B1` du fichier `parametres.xlsx`. Ce mécanisme :
a) permet de rejouer le pipeline sans modifier le code · b) est le seul moyen de passer une constante en M ·
c) ne sert à rien en pandas · d) force l'utilisation de Power Query exclusivement.

### Bloc 2 — Power Query (C02) (Q4 à Q6)

**Q4.** Power Query applique automatiquement le typage « colonne entière » au chargement. Quand l'erreur apparaît :
a) au moment de l'ouverture · b) au moment où une étape downstream utilise la colonne dans un type différent ·
c) au moment de l'enregistrement · d) jamais, l'auto-typage est sans erreur.

**Q5.** L'étape « Remplir vers le bas » (down-fill) propage la valeur précédente. Sur la colonne `id_client` du brut
(28 516 920 o), elle s'applique : a) sur 1 911 cellules (vides après la première) · b) sur 0 cellule · c) sur
28 516 920 cellules · d) sur 12 colonnes à la fois.

**Q6.** La fusion (jointure Power Query) entre `ventes_brutes` et `clients.csv` sur `id_client` seul donne
**41 716 lignes enrichies** au lieu de **1 714**. Conclusion : a) le fichier clients est faux · b) la jointure
naïve duplique chaque vente sur tous les clients qui partagent l'`id_client` ; la clé juste inclut `id_client ×
année × mois` · c) Power Query est en cause · d) il faut refaire la fusion sans condition.

### Bloc 3 — SQL DuckDB (C03) (Q7 à Q9)

**Q7.** La fonction `TRY_CAST(montant AS BIGINT)` retourne `NULL` si la conversion échoue, sans lever d'erreur. Par
rapport à `CAST` qui lève : a) `TRY_CAST` est plus rapide · b) `TRY_CAST` rend le défaut silencieux, exactement
comme Excel `SOMME()` ignore le texte · c) `TRY_CAST` n'a aucun avantage · d) `TRY_CAST` est réservé à DuckDB.

**Q8.** La table `v_dedup` est calculée par :
```
WITH cle AS (
  SELECT *, ROW_NUMBER() OVER (
    PARTITION BY id_ticket, id_produit, quantite, ttc_n, heure
    ORDER BY id_vente
  ) AS rn
  FROM v_mars
)
SELECT * EXCLUDE rn FROM cle WHERE rn = 1
```
Le nombre de lignes en sortie sur mars 2025 (`v_dedup`) : a) 6 884 (avant dédoublonnage) · b) 6 798 (86 doublons
retirés) · c) 7 270 (tous les doublons exacts + variantes) · d) 101 (les enrichies).

**Q9.** La session DuckDB étant en mémoire (`:memory:`), chaque bloc SQL d'une même évaluation repart de zéro.
Conséquence : a) le bloc `v_mars` doit être recréé dans chaque SELECT · b) DuckDB ne sait pas garder l'état · c)
DuckDB est plus rapide qu'une session persistante · d) il faut sauvegarder en CSV entre chaque bloc.

### Bloc 4 — pandas (C04) (Q10 à Q12)

**Q10.** La chaîne `df.assign(montant_ttc_n=...).sort_values(['date_vente','id_vente']).drop_duplicates(CLE)` produit
un résultat différent si on intervertit `sort_values` et `drop_duplicates`. Pourquoi ? a) pandas n'a pas de garantie
d'ordre sans tri explicite · b) `sort_values` change les types des colonnes · c) `drop_duplicates` sans tri garde la
dernière occurrence observée, pas la première dans l'ordre chronologique · d) ce n'est pas un problème.

**Q11.** L'`SettingWithCopyWarning` apparaît sur la ligne `df[df['montant_ttc'] > 1000]['ttc_n'] = 0`. La parade :
a) ignorer l'avertissement · b) `df.loc[mask, 'ttc_n'] = 0` (indexeur explicite) · c) reconstruire le DataFrame
à la main · d) utiliser `np.where`.

**Q12.** La cellule 8 du notebook C04 fait le verdict :
```
assert hashlib.sha256(df_final.to_parquet()).hexdigest() == '7cce2d0c…'
```
Ce que cette cellule prouve : a) le notebook s'exécute · b) pandas produit la même table que DuckDB au byte
près après sérialisation Parquet · c) le fichier est valide · d) la fonction sha256 fonctionne.

### Bloc 5 — Arbitrage (C05) (Q13 à Q15)

**Q13.** Sur 6 884 lignes, pandas est **13 × plus rapide** que DuckDB (22 ms vs 283 ms). Sur 1 million de lignes,
DuckDB est **3 × plus rapide**. Le critère pertinent du choix : a) la taille seule · b) la taille **prévisionnelle**
(croît-il ?) · c) la marque du poste · d) le système d'exploitation.

**Q14.** Le verdict « même empreinte sha256 entre pandas et DuckDB » prouve : a) que les deux outils sont les mêmes ·
b) que le pipeline est **portable** (ne dépend pas de l'implémentation) · c) que pandas est plus rapide · d) que
DuckDB est correct.

**Q15.** Une équipe bureautique (Excel, pas de Python) reçoit un fichier de 750k lignes mis à jour quotidiennement.
L'outil adapté : a) pandas, parce que c'est le plus moderne · b) DuckDB, parce que c'est le plus rapide · c) Power
Query (si Microsoft 365) avec orchestration Power Automate · d) aucun, c'est impossible.

### Corrigé du quiz

Q1 **b** — « promote headers » est un Opérateur (transformation de la structure), pas une M (manipulation d'une
seule colonne). Q2 **b** — la traduction pandas est littérale : `str.replace` pour `REPLACE`, `pd.to_numeric`
pour `TRY_CAST`, `errors='coerce'` pour le `NULL` en cas d'échec. Q3 **a** — la constante `MoisCible` externalisée
dans `parametres.xlsx` est l'objet du C02 §5.13. Q4 **b** — Power Query applique le typage *paresseusement* ; l'erreur
survient au recalcul d'une étape en aval. Q5 **a** — 1 911 cellules vides dans `id_client` du brut, toutes remplies
par down-fill (`id_client` en NaN devient la valeur précédente). Q6 **b** — la jointure naïve sur `id_client` seul
duplique chaque vente sur tous les clients qui partagent cet identifiant ; la clé juste inclut `id_client × année ×
mois`. Q7 **b** — `TRY_CAST` rend le défaut silencieux, comme Excel `SOMME` ignore le texte (cf. M04 §5.6). Q8 **b** —
6 798 (= 6 884 − 86), 86 étant `m05_filrouge_mars_doublons`. Q9 **a** — la session `:memory:` repart de zéro ; il
faut recréer les tables dans chaque bloc. Q10 **c** — sans tri explicite, `drop_duplicates(keep='first')` garde
la première occurrence **dans l'ordre de lecture** (par `id_vente`), pas la première dans l'ordre **chronologique**.
Q11 **b** — `df.loc[mask, 'ttc_n'] = 0` est l'indexeur explicite qui neutralise le warning. Q12 **b** — la cellule
fait le **verdict croisé** : pandas et DuckDB produisent la même table au byte près. Q13 **b** — la taille
prévisionnelle, pas la taille courante. Q14 **b** — le verdict prouve la **portabilité** du pipeline. Q15 **c** —
Power Query + Power Automate est la combinaison adaptée à ce profil.

---

## C · Exercices pratiques (50 min · /20)

Tout se fait sur `03_exercices/dossier_M05/` (le dossier du projet ; ATTENDU.json à consulter **après** vos calculs).

**E1 — La grille du diagnostic (5 points).** Passez la grille des 12 points du M04.C01 sur
`ventes_2023_2024.csv`. Note attendue : les **5 compteurs non nuls avec dénominateurs** (1 731 montants texte sur
121 720 ; 1 720 doublons sur 121 720 ; 493 dates transposées ; 252 clients inconnus ; 488 remises hors domaine),
plus la séparation « 4 défauts qui touchent au total / 5 défauts qui faussent chacun une lecture différente ».
1 pt par compteur justifié, 1 pt pour la séparation.

**E2 — Le pipeline pandas complet (5 points).** Produisez le `df_final` à **120 000 lignes, total TTC
7 145 910 735 FCFA**. Note attendue : (a) la conversion des 1 731 montants texte par `assign/TRY_CAST` ; (b) la
transposition des 493 dates par colonne dérivée ; (c) le dédoublonnage 1 720 lignes (1 680 copies + 40
variantes) ; (d) le verdict `assert sha256(df_final) == '7cce2d0c…'`. 2 pts pour le résultat, 2 pour la chaîne
canonique dans l'ordre, 1 pour le verdict sha256.

**E3 — Le pipeline SQL DuckDB équivalent (5 points).** Réécrivez le pipeline E2 en SQL DuckDB (11 tables
temporaires). Note attendue : (a) `v1` source brute ; (b) `v2` typage TRY_CAST ; (c) `v3` réparation des dates ;
(d) `v_mars` coupe `BETWEEN 01-03 et 31-03` ; (e) `v_dedup` ROW_NUMBER sur clé 5-colonnes ; (f) `v_final`
jointure clients clé complète contre 41 716 naïves ; (g) le verdict `empreinte sha256 identique`. 1 pt par
étape, plus 2 pts pour le verdict croisé.

**E4 — L'arbitrage DuckDB / pandas sur 3 tailles (5 points).** Mesurez **sur votre machine** le temps
d'exécution du pipeline sur (a) 6 884 lignes (mars 2025 du brut), (b) 121 720 lignes (projet), (c) 1 million
de lignes (généré par duplication). Le barème : 1,5 pt par mesure × 3, plus 0,5 pt pour la comparaison avec
les 5 chiffres du C05 §5.3. Indication attendue : sur (a), pandas domine (≈ 13 ×) ; sur (b), DuckDB prend un
léger avantage (≈ 1,4 ×) ; sur (c), DuckDB domine (≈ 3 ×). Si vos mesures s'écartent de plus de 50 % des
chiffres de référence du C05, vous *documentez l'écart* (matériel, RAM, SSD vs disque rotatif, etc.) — pas
un défaut, un fait.

---

## D · Étude de cas (60 min · /20, seuil 12) — « Un pipeline, trois moteurs — qui dit la même chose ? »

**Contexte.** Un data engineer d'une enseigne de distribution vous transmet la question : « j'ai trois versions de
la même table propre, faites-en un dossier qui dit si elles disent la même chose — et lequel je garde comme
référence ». Vous rendez un dossier de quatre pages.

**Le matériel.** `03_exercices/dossier_M05/` (121 720 lignes brutes ; 120 000 après réparation ; total
7 145 910 735 FCFA ; 1 714 enrichies ; 31 clés dans `ATTENDU.json`). Trois pipelines dans `02_modules/` :
- (a) `M05_C02` — Power Query, 14 étapes manuelles (M code documenté, *non exécutable* dans cet atelier) ;
- (b) `M05_C03` — SQL DuckDB, 11 CTE (`controle_sql.py M05` rend 11 requêtes exécutées) ;
- (c) `M05_C04` — pandas, 8 cellules de notebook (`controle_python.py M05` rend 15 fragments exécutés).

**Le livrable, en quatre parties :**

1. **Ce que disent les pipelines** (description et grain) : 3 points.
2. **Le verdict croisé, en quatre temps** : (a) même total TTC 7 145 910 735 FCFA (oui) ; (b) même nombre de
   lignes 120 000 (oui) ; (c) même nombre d'enrichies 1 714 (oui) ; (d) même empreinte sha256 `7cce2d0c…` (oui
   entre pandas et DuckDB, *non vérifié* pour Power Query) : 4 points.
3. **L'arbitrage final** : sur les 4 critères du C05 §7 (taille, fréquence, compétences, gouvernance), lequel
   des trois reste **référence** ? Argumentation : 4 points. Indication attendue : DuckDB en première intention
   (portable, plus rapide à l'échelle, schémas SQL centralisés) ; pandas en repli (plus riche en méthodes) ; Power
   Query en vitrine (pour le reporting Excel des commerciaux qui ne font pas de Python).
4. **Trois règles que le prochain projet devrait imposer**, chacune avec son niveau (bloquant / corriger /
   surveiller) et son destinataire : (a) **empreinte sha256 systématique** sur `df_final` à chaque exécution
   (niveau 1, bloquant, contrôleur CI) ; (b) **mesure de temps** sur 3 tailles avant de figer le choix (niveau 2,
   corriger, mainteneur) ; (c) **README du dossier avec les 4 critères** (niveau 3, surveiller, équipe) :
   4 points.

**Grille de qualité (complément des 4 parties, 5 points).** Reproductibilité : 3 points — chaque chiffre du dossier
est reproducible par une formule ou un compteur nommé. Limites : 2 points — ce que les 3 moteurs ne disent pas :
Power Query non exécutable dans cet atelier, lecture manuelle des 14 étapes.

**Ce qui est piégé dans l'étude.** (1) Conclure « oui, ils disent la même chose » sans le **chiffrer** : le verdict
doit être en quatre temps (total, lignes, enrichies, sha256). (2) Donner DuckDB comme référence *par défaut* sans
l'avoir justifié par les 4 critères. (3) Citer une empreinte sha256 sans sa clé `m05p_empreinte_sha256`. (4) Oublier
que la **mesure de temps** est ce qui distingue un choix *réfléchi* d'un choix *par défaut* — c'est la règle 3 du
plan M05 §3 (« mesurer, pas extrapoler »).

---

## Lecture des résultats

- **B ≥ 11 et D ≥ 12** : module validé (le projet M05.P doit, de son côté, atteindre 13/20).
- **B < 11** : le socle des définitions n'est pas acquis ; repasser B et la récupération A, le module reste ouvert.
- **D < 12 avec B ≥ 11** : le candidat sait ce qu'est un pipeline portable mais ne sait pas dire si deux moteurs
  produisent la même table au byte près ; repasser D uniquement.
- Le projet M05.P se note séparément (13/20 de seuil) et pèse sur la validation finale du module.
