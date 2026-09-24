# Projet M07.P — « Trente questions pour la direction commerciale : de la base brute au tableau de bord fiable »

**Module M07 · projet de fin de module · 6 h · barème /20, seuil de passage 13/20**

> **Le cadre réel.** La direction commerciale d'une enseigne de distribution burkinabè vous
> confie sa base `commercial.duckdb` (9 tables, 50 008 ventes sur 2025–2026, 1 200 clients,
> 380 produits, 5 magasins). Elle a 30 questions en tête — et 3 défauts que personne n'a
> encore signalés (8 doublons, 200 retours comptés en positif, 15 dates de remise
> inversées). À vous de répondre aux 30 questions **en détectant les 6 pièges de
> fiabilité** (3 dans les données, 3 dans les requêtes) avant de poser chaque requête.
> C'est la synthèse des huit chapitres : SELECT/FROM (C01), WHERE (C02), ORDER BY/LIMIT
> (C03), agrégats (C04), GROUP BY/HAVING (C05), CASE (C06), jointures (C07), sous-requêtes
> et EXISTS (C08) — chaque bloc de questions en mobilise un, et aucun n'est noté pour
> lui-même : seul le **chiffre juste, obtenu sans se faire piéger** compte.

> **Note de cohérence.** Le dossier est généré de façon déterministe par
> `python3 tools/dossier_M07.py` (graine 44) : qui que vous soyez, vous touchez les mêmes
> 50 008 ventes et la même empreinte BD `df9333ff…a1dde`. `03_exercices/dossier_M07/ATTENDU.json`
> contient les **31 clés** des résultats attendus, **mesurés sur le dossier généré, jamais
> déduits** : vous n'y recourez qu'après avoir produit vos propres nombres, pour comparer,
> pas pour copier. Un candidat qui lit l'`ATTENDU` avant de calculer n'a plus rien à
> rendre. Les chiffres de ce corrigé sont ceux du dossier livré, vérifiables ligne à ligne
> sur `commercial.duckdb`.

---

## 1. Énoncé

### Le matériel

| Élément | Chemin | Ce que c'est |
|---|---|---|
| Base de travail | `03_exercices/dossier_M07/commercial.duckdb` | 9 tables + 1 vue : `vente` (50 008 lignes, **3 défauts** : 8 doublons exacts, 200 retours `est_retour = TRUE` à montant positif, 15 ventes avec `date_vente > date_limite_remise`), `client` (1 200), `produit` (380, dont 18 inactifs), `magasin` (5), `categorie` (8, **5 libellés `rayon` seulement** — les rayons Alimentaire, Bricolage, Jardinage sont doublés), `mode_paiement` (5), `regle_tva` (2), `objectif_magasin` (**vide**), vue `v_ca_mensuel_magasin` (120 lignes) |
| Export SQL | `03_exercices/dossier_M07/commercial.sql` | le `INSERT` complet (4,68 Mo), rechargable dans n'importe quel DuckDB |
| Questions | `03_exercices/dossier_M07/30_questions.sql` | 30 questions métier : 6 faciles (Q01–Q06), 12 moyennes (Q07–Q18), 9 avancées (Q19–Q26), 3 expert (Q27–Q30) |
| Corrigé de référence | `03_exercices/dossier_M07/30_reponses.sql` | les 30 requêtes de référence (à exécuter soi-même pour vérifier) |
| Pièges | `03_exercices/dossier_M07/6_pieges.md` | les 6 pièges de fiabilité : P1 doublon (Q19), P2 retours (Q09), P3 dates (Q14), P4 jointure multiple (Q27), P5 DISTINCT masquant (Q23), P6 EXISTS/IN (Q30) |
| Résultats attendus | `03_exercices/dossier_M07/ATTENDU.json` | 31 clés `m07p_*` : empreintes sha256, totaux, top, pièges |

### Les quatre parties, et ce qu'elles notent

| # | Partie | Questions | Ce que ça mobilise | Barème |
|---|---|---|---|---|
| P1 | Lecture et volumes | Q01–Q06 | C01, C02, C04 | /4 |
| P2 | Mesures par dimension | Q07–Q18 | C03, C04, C05 | /6 |
| P3 | Requêtes composées et données sales | Q19–Q26 | C05, C06, C08 | /6 |
| P4 | Expert : jointures multiples et « tous les » | Q27–Q30 | C07, C08 | /4 |

> **Règle du projet.** Chaque question piège (Q09, Q14, Q19, Q23, Q27, Q30) est notée sur
> **deux critères** : le chiffre juste **et** la détection du piège (une phrase qui nomme
> le piège et explique pourquoi la réponse naïve est fausse). Un chiffre juste obtenu par
> la requête naïfe (par exemple le CA « gonflé » de Q09 présenté comme le CA) vaut **0**,
> même si le nombre est dans `ATTENDU.json`.

---

## 2. Grille de notation détaillée (/20)

| Partie | Détail | Points |
|---|---|---|
| P1 | Q01–Q06 : 6 réponses justes (≈ 0,5–0,7 chacune) | /4 |
| P2 | Q07–Q18 : 12 réponses justes, dont **Q09** (piège P2 : 0,5 + 0,5 piège) et **Q14** (piège P3 : 0,5 + 0,5 piège) | /6 |
| P3 | Q19–Q26 : 8 réponses justes, dont **Q19** (piège P1 : 1 + 1 piège) et **Q23** (piège P5 : 0,5 + 0,5 piège) | /6 |
| P4 | Q27–Q30 : 4 réponses justes, dont **Q27** (piège P4 : 0,75 + 0,75 piège) et **Q30** (piège P6 : 0,5 + 0,5 piège) | /4 |

**Total : /20. Seuil de passage : 13/20.** Les 6 pièges pèsent au total 5 points :
c'est le cœur du module — *savoir requêter* ne vaut rien si on ne sait pas *vérifier*.

---

## 3. Corrigé-type (à publier après la séance)

> Ce corrigé n'est pas un modèle à recopier : c'est la **référence** à laquelle vous
> comparez vos propres nombres. Les requêtes de référence sont dans `30_reponses.sql` ;
> exécutez-les sur `commercial.duckdb` et comparez. Si un chiffre ne tombe pas à 1 unité
> près, c'est que votre code a un défaut — pas que la référence a tort.

### P1 — Lecture et volumes (Q01–Q06)

| Q | Question | Réponse de référence |
|---|---|---|
| Q01 | Combien de clients ? | **1 200** |
| Q02 | Combien de produits actifs ? | **362** (18 inactifs) |
| Q03 | Combien de magasins ? Dans quelles villes ? | **5** : Ouaga Centre, Ouaga Patte d'Oie (Ouagadougou), Bobo Centre, Bobo Sarfalao (Bobo-Dioulasso), Koudougou |
| Q04 | Montant TTC total de toutes les ventes (sans filtre) ? | **7 908 259 731 FCFA** |
| Q05 | Combien de modes de paiement ? Listez-les. | **5** : Espèces, Carte Bancaire, Mobile Money, Credit 30j, Virement |
| Q06 | Première et dernière vente ? | **2025-01-01** et **2026-12-28** |

### P2 — Mesures par dimension (Q07–Q18)

| Q | Question | Réponse de référence |
|---|---|---|
| Q07 | CA TTC par magasin (sans retours), décroissant | Magasin 4 en tête (**1 592 496 610 FCFA** sans retours), puis 1, 2, 5, 3 |
| Q08 | Ventes par mois, 2025 | 12 mois, de 2 058 (janvier) à environ 2 100/mois |
| **Q09** | **PIÈGE P2** — CA total sans filtrer les retours | Le chiffre de référence (7 908 259 731) **inclut 200 retours à montant positif** : le CA « propre » est **7 876 320 163 FCFA** (`WHERE est_retour = FALSE`). Le piège : les retours sont comptés **en positif** dans le brut |
| Q10 | Panier moyen (sans retours) | **158 159 FCFA** (158 140 avec les retours — cf. C04) |
| Q11 | 10 produits les plus vendus (quantité) | Produit 98 en tête (**939 unités**), puis 107, 58… |
| Q12 | 5 meilleurs clients par CA | Client 73 en tête (**11 561 026 FCFA**), puis 930 (10 647 641), 614 (10 602 339)… |
| Q13 | Clients distincts par magasin | 1 199 / 1 199 / 1 200 / 1 200 / 1 199 (couverture quasi totale) |
| **Q14** | **PIÈGE P3** — CA par mois, `date_vente` vs `date_limite_remise` | 24 mois si on filtre `date_vente <= date_limite_remise` (15 ventes inversées écartées). Le piège : **15 ventes** ont une `date_vente` postérieure à leur `date_limite_remise` — les attribuer au mois de la vente ou au mois de la remise change le CA mensuel |
| Q15 | Ventes un dimanche ? | **7 136** |
| Q16 | Taux de retour par rayon | 0,4 % à 0,5 % par rayon (les retours sont rares et uniformes) |
| Q17 | Délai moyen entre début de mois et vente | **15,9 jours** (ventes réparties sur le mois) |
| Q18 | Clients avec plafond > 100 000 FCFA | **490** |

### P3 — Requêtes composées et données sales (Q19–Q26)

| Q | Question | Réponse de référence |
|---|---|---|
| **Q19** | **PIÈGE P1** — dedoublonnage exact | **50 000** ventes uniques (50 008 − 8 doublons exacts). Nuance de vérification : le `DISTINCT` sur les 5 colonnes métier (client, produit, magasin, date, montant) renvoie **49 999** — une paire de ventes **naturelle** (id 41 405 et 41 757 : même client, produit, magasin, date et montant, mais **mode de paiement et remise différents**) se projette en une seule ligne. Le dedoublonnage juste porte sur **toutes** les colonnes métier, pas sur une projection choisie à l'œil |
| Q20 | Clients ayant acheté dans ≥ 3 magasins | 1 200 (tous — la couverture multi-magasins est quasi complète) |
| Q21 | Top 1 produit par magasin (CA) | 5 lignes (une par magasin) via `ROW_NUMBER() OVER (PARTITION BY id_magasin)` |
| Q22 | Remise moyenne par mode de paiement | 0,0 % (Espèces) à 1,5 % (Carte Bancaire) — les remises suivent le mode |
| **Q23** | **PIÈGE P5** — couples client×produit distincts | **47 359** couples (`SELECT COUNT(*) FROM (SELECT DISTINCT id_client, id_produit FROM vente) t`). Le piège : un `COUNT(DISTINCT …)` « répare » visuellement une jointure qui double — il faut **vérifier le `COUNT(*)` de la jointure nue** avant de conclure |
| Q24 | Écart CA réalisé / objectif par magasin | 0 ligne — la table `objectif_magasin` est **vide** : la jointure `JOIN objectif_magasin` ne renvoie rien. La bonne réponse est de l'expliquer (pas de données d'objectif), pas de renvoyer 0 |
| Q25 | Évolution du CA 2025→2026 par rayon | Jardinage en tête (**+39 020 518 FCFA**), puis Bricolage (+21 770 291), Alimentaire (+19 250 569)… |
| Q26 | Produits au-dessus du prix moyen **de leur rayon** | **190 produits** (sous-requête corrélée sur `id_categorie`) |

### P4 — Expert : jointures multiples et « tous les » (Q27–Q30)

| Q | Question | Réponse de référence |
|---|---|---|
| **Q27** | **PIÈGE P4** — ventes Bobo-Dioulasso × rayon Bricolage (4 jointures) | **4 568**. Le piège : la jointure 4 tables en **étoile** (vente→client, vente→produit→categorie) est ici `N → 1` partout — `COUNT(*)` = `COUNT(DISTINCT id_vente)` = 4 568, **pas de doublon**. Le piège se referme si on joint une table qui multiplie (cf. C07 §5.7 : 2 131 064 lignes) — d'où le contrôle systématique |
| Q28 | Segmentation RFM des 1 200 clients | 1 200 lignes segmentées (`champion` / `fidele` / `occasionnel` / `perdu` / `nouveau`) via `WITH` + `CASE` |
| Q29 | Tableau de bord mensuel 2025 avec `LAG` | 12 lignes : CA, nb ventes, panier, retours, et `LAG(ca)` (janvier en `NULL`) |
| **Q30** | **PIÈGE P6** — clients ayant acheté **TOUS** les produits « Bricolage-Outillage » | **0 client** : la double négation `NOT EXISTS (… NOT EXISTS (…))` ne renvoie personne (aucun client n'a acheté les 55 produits du rayon Outillage). Le piège : `IN` renverrait les clients ayant acheté **au moins un** (très nombreux) — le sens « tous » exige la double négation |

---

## 4. Les 6 pièges de fiabilité (rappel et vérification)

| Piège | Type | Question | La faute | La correction | Chiffre de contrôle |
|---|---|---|---|---|---|
| **P1** | données | Q19 | `COUNT(*)` naïf = 50 008 (8 doublons inclus) | dedoublonnage sur **toutes** les colonnes métier | 50 000 uniques (proxy 5 colonnes : 49 999) |
| **P2** | données | Q09 | CA avec retours comptés en positif | `WHERE est_retour = FALSE` | 7 908 259 731 (gonflé) vs 7 876 320 163 (propre) |
| **P3** | données | Q14 | 15 ventes avec `date_vente > date_limite_remise` | filtrer `date_vente <= date_limite_remise` (ou documenter la convention) | 24 mois filtrés |
| **P4** | requête | Q27 | jointure qui double (relation `N → N` oubliée) | étoile `N → 1` + contrôle `COUNT(*)` = `COUNT(DISTINCT id_vente)` | 4 568 |
| **P5** | requête | Q23 | `DISTINCT` qui masque un mauvais `JOIN` | contrôler `COUNT(*)` sur la jointure **nue** avant l'agrégat | 47 359 couples |
| **P6** | requête | Q30 | `IN` (« au moins un ») pour une question « tous les » | double négation `NOT EXISTS … NOT EXISTS` | 0 client |

> **Règle du projet.** Un piège non détecté **annule** la note de la question, même si le
> chiffre tombe juste (cas P2 : le chiffre « gonflé » est bien dans `ATTENDU.json` — c'est
> la version piège). La détection se note par une **phrase** : nom du piège + pourquoi la
> réponse naïve est fausse + la requête corrigée.

---

## 5. Critères de passage

| Critère | Condition |
|---|---|
| Note totale | ≥ 13/20 |
| Pièges | au moins 4 des 6 pièges détectés et corrigés |
| Exécution | les requêtes **exécutées** sur DuckDB (sortie capturée), pas juste écrites |
| Vérification | chaque partie contrôlée par un total cohérent (ex. P2 : la somme des CA par magasin = 7 876 320 163 sans retours) |

> **L'esprit du projet.** On ne note pas la syntaxe (DuckDB la corrige) : on note le
> **chiffre juste, obtenu proprement, avec les pièges nommés**. Un candidat qui écrit 30
> requêtes correctes mais qui livre le CA « gonflé » de Q09 sans le signaler **n'a pas
> réussi le module** — c'est exactement l'erreur qu'un analyste commet en production, et
> c'est elle que ce module apprend à empêcher.
