# Évaluation M07 — « SQL : interroger, agréger, rejoindre »

**Module M07 · durée totale 3 h · quatre épreuves · seuils : quiz 13/20, exercices 28/35, étude de cas 12/20**

| Épreuve | Durée | Barème | Noté | Ce qui est attendu |
|---|---|---|---|---|
| A · Questions de récupération | 10 min | non noté | non | vérifier qu'on a lu les huit chapitres avant de se tromper cher |
| B · Quiz | 25 min | /20 | oui | vingt questions à réponse unique, cinq blocs |
| C · Exercices chiffrés | 40 min | /35 (auto-corrigé) | oui | trente-cinq chiffres sur `commercial.duckdb`, auto-validés par `tools/controle_exos_M07.py` |
| D · Étude de cas | 75 min | /20, seuil 12 | oui | le rapport de la direction commerciale (6 requêtes + 1 page de synthèse) |

> Le score du module se lit ainsi : **B ≥ 13** et **D ≥ 12** valident le module ; le projet
> M07.P doit atteindre 13/20. Un candidat qui réussit B et échoue à D repasse uniquement D :
> savoir que `HAVING` filtre les groupes ne dispense pas de vérifier que la jointure ne
> double pas les lignes. Tout nombre de cette évaluation est mesuré sur le socle livré
> (`commercial.duckdb`, empreinte `df9333ff…a1dde`) ; les corrections le citent avec leur
> clé `m07_*` / `m07p_*` dans `chiffres_cites.json`.

---

## A · Questions de récupération (non notées)

À traiter sans document, en une ou deux phrases chacune. Elles ne sont pas comptées ; elles
servent à repérer ce qui n'est pas assimilé avant de perdre des points sur un détail.

1. Citez l'**ordre d'exécution** d'une requête SQL complète (C01), et expliquez pourquoi
   `LIMIT 5` sans `ORDER BY` est non déterministe.
2. Quelle est la différence entre `COUNT(*)`, `COUNT(colonne)` et
   `COUNT(DISTINCT colonne)` ? (C04)
3. Où s'écrit un filtre sur un **total** : `WHERE` ou `HAVING` ? Pourquoi ? (C05)
4. Pourquoi un libellé **doublé** est-il dangereux dans un `GROUP BY` ? Donnez l'exemple du
   socle. (C05)
5. Que renvoie `SUM(colonne)` si toutes les valeurs sont `NULL` ? Et comment forcer 0 ? (C04)
6. Quelle est la différence entre `COALESCE` et `NULLIF` ? (C06)
7. Pourquoi la condition du côté droit d'un `LEFT JOIN` doit-elle aller dans l'`ON` ? (C07)
8. Comment écrit-on « les clients qui ont acheté **tous** les produits X » ? (C08)

---

## B · Quiz (20 questions · 20 points)

**Barème : 1 point par question, une seule bonne réponse. Les réponses justifiées en une
ligne rapportent un demi-point de bonus, plafonné à 20.**

### Bloc 1 — Lire et filtrer (C01–C02) (Q1 à Q4)

**Q1.** Dans l'ordre d'exécution, la première clause traitée est : a) `SELECT` · b)
**`FROM`** · c) `WHERE` · d) `ORDER BY`.

**Q2.** L'alias d'une colonne sert à : a) renommer la colonne dans la table · b) **désigner
une colonne ou une table dans la requête (tri, regroupement, lisibilité)** · c) créer un
index · d) éviter les erreurs de type.

**Q3.** `SELECT DISTINCT ville FROM client;` : a) trie les villes · b) **supprime les lignes
de résultats identiques** · c) supprime les colonnes en double · d) limite à une ligne.

**Q4.** `WHERE a = 1 OR b = 2 AND c = 3` équivaut à : a) `(a = 1 OR b = 2) AND c = 3` · b)
**`a = 1 OR (b = 2 AND c = 3)` — `AND` se lie avant `OR`** · c) `(a = 1 OR b = 2)` sans `c` ·
d) une erreur.

### Bloc 2 — Trier et agréger (C03–C04) (Q5 à Q8)

**Q5.** `LIMIT 5` sans `ORDER BY` renvoie : a) les 5 plus petites lignes · b) **5 lignes
arbitraires (l'ordre du stockage, non garanti)** · c) les 5 dernières insérées · d) une
erreur.

**Q6.** `LIMIT 10 OFFSET 10` renvoie : a) les lignes 1 à 10 · b) **les lignes 11 à 20 (la
2ᵉ page)** · c) les lignes 10 à 19 · d) 10 lignes prises au hasard après la 10ᵉ.

**Q7.** Sur une colonne sans `NULL`, `COUNT(*)` et `COUNT(colonne)` : a) diffèrent toujours
d'1 · b) **renvoient le même nombre** · c) renvoient 0 · d) `COUNT(colonne)` renvoie `NULL`.

**Q8.** `SUM(colonne)` sur une colonne 100 % `NULL` renvoie : a) 0 · b) **`NULL`** · c) une
erreur · d) le nombre de lignes.

### Bloc 3 — Résumer par groupe (C05) (Q9 à Q12)

**Q9.** « Les magasins avec plus de 9 900 ventes » s'écrit avec : a) `WHERE COUNT(*) > 9900`
· b) **`HAVING COUNT(*) > 9900`** · c) `LIMIT 9900` · d) `ORDER BY COUNT(*) > 9900`.

**Q10.** Regrouper par un libellé doublé (ici, `rayon`) : a) produit une erreur · b)
**fusionne silencieusement les groupes (5 rayons au lieu de 8 catégories)** · c) double les
lignes · d) n'a aucun effet.

**Q11.** Le contrôle de cohérence d'un `GROUP BY` est : a) vérifier l'orthographe des alias ·
b) **le nombre de groupes + la somme des agrégats redonne le total global** · c) le temps
d'exécution · d) le nombre de colonnes du `SELECT`.

**Q12.** `COUNT(DISTINCT id_client)` dans un `GROUP BY id_magasin` compte : a) les clients
de tous les magasins · b) **les clients distincts de chaque magasin (une ligne par magasin)**
· c) les ventes de chaque magasin · d) une erreur.

### Bloc 4 — Catégoriser (C06) (Q13 à Q16)

**Q13.** Dans un `CASE WHEN`, les branches sont testées : a) toutes en même temps · b)
**dans l'ordre écrit, la première qui passe gagne** · c) de la plus longue à la plus courte ·
d) dans un ordre aléatoire.

**Q14.** Sans `ELSE`, les lignes non couvertes par un `CASE` renvoient : a) 0 · b) une
erreur · c) **`NULL`** · d) la valeur de la première branche.

**Q15.** `COALESCE(0, 'défaut')` renvoie : a) « défaut » · b) **`0` — il ne regarde que les
`NULL`, pas les zéros** · c) une erreur de type · d) `NULL`.

**Q16.** `NULLIF(5, 0)` renvoie : a) `NULL` · b) 0 · c) **5** · d) une erreur.

### Bloc 5 — Joindre et composer (C07–C08) (Q17 à Q20)

**Q17.** Mettre la condition du côté droit d'un `LEFT JOIN` dans le `WHERE` : a) n'a aucun
effet · b) **transforme le `LEFT JOIN` en `INNER JOIN` (les `NULL` du droit sont éliminés)**
· c) double les lignes · d) produit une erreur de syntaxe.

**Q18.** `CROSS JOIN` entre 5 magasins et 5 modes de paiement produit : a) 10 lignes · b)
**25 lignes (5 × 5, produit cartésien)** · c) 5 lignes · d) 0 ligne.

**Q19.** `WHERE x IN (sous-requête)` signifie : a) « tous les » · b) **« au moins un »** ·
c) « aucun » · d) « exactement un ».

**Q20.** « Les clients qui ont acheté **tous** les produits X » s'écrit avec : a) `IN` ·
b) `COUNT(*)` comparé au total · c) **la double négation `NOT EXISTS (… NOT EXISTS (…))`** ·
d) `CROSS JOIN`.

---

## C · Exercices chiffrés (35 exercices · 35 points · auto-corrigés)

**Consigne.** Sur `commercial.duckdb`, produire le chiffre de chaque exercice (une requête
chacune). 1 point par réponse exacte (tolérance de 0,5 sur les arrondis). Les 35 requêtes de
référence et leurs valeurs attendues sont auto-validées par
`python3 tools/controle_exos_M07.py` — exécutez-le pour vérifier vos réponses ; il rapporte
chaque valeur obtenue. Les valeurs attendues sont mesurées sur le socle livré, jamais
déduites (cf. `chiffres_cites.json`, clés `m07_*`).

| # | Exercice | Réponse attendue |
|---|---|---|
| E01 | Nombre de ventes | **50 008** |
| E02 | CA brut total (FCFA, arrondi) | **7 908 259 731** |
| E03 | Produits actifs | **362** |
| E04 | Clients d'Ouagadougou | **512** |
| E05 | Ventes un dimanche | **7 136** |
| E06 | Panier moyen, toutes ventes (FCFA, arrondi) | **158 140** |
| E07 | Montant maximum (FCFA) | **594 363** |
| E08 | Montant minimum (FCFA, arrondi) | **763** |
| E09 | Top magasin par CA (id) | **4** |
| E10 | CA du top magasin (FCFA) | **1 596 813 264** |
| E11 | Ventes de 2025 | **24 920** |
| E12 | CA de 2026 (FCFA) | **3 983 044 060** |
| E13 | Ventes en Espèces (mode 1) | **20 175** |
| E14 | CA Carte Bancaire (mode 2, FCFA) | **1 944 001 846** |
| E15 | Catégories (par id) avec plus de 6 500 ventes | **4** |
| E16 | Ventes de la catégorie Decoration (id 7) | **6 798** |
| E17 | Clients avec plafond > 100 000 FCFA | **490** |
| E18 | Clients particuliers | **850** |
| E19 | CA des clients entreprises (FCFA) | **1 482 606 616** |
| E20 | Clients de Koudougou | **247** |
| E21 | Ventes de 200 000 FCFA et plus | **15 746** |
| E22 | Ventes de moins de 50 000 FCFA | **12 753** |
| E23 | Ventes du magasin 4 en 2026 | **4 997** |
| E24 | CA des produits inactifs (FCFA) | **471 206 245** |
| E25 | CA du meilleur client (FCFA) | **11 561 026** |
| E26 | Ventes des clients de Bobo-Dioulasso | **18 364** |
| E27 | Ventes uniques, dedoublonnage complet (12 colonnes) | **50 000** |
| E28 | Ventes uniques, proxy 5 colonnes (piège P1) | **49 999** |
| E29 | Couples client × produit distincts (piège P5) | **47 359** |
| E30 | Ventes Bobo × rayon Bricolage, 4 jointures (piège P4) | **4 568** |
| E31 | Clients ayant acheté les 2 produits les plus chers (P6) | **119** |
| E32 | Lignes de la vue `v_ca_mensuel_magasin` | **120** |
| E33 | Plus gros mois de la vue (FCFA, arrondi) | **78 965 529** |
| E34 | Ventes au-dessus du panier moyen | **20 289** |
| E35 | Produits au-dessus du prix moyen de leur rayon | **190** |

> **Lecture des E27/E28.** E27 est le vrai dedoublonnage (toutes les colonnes métier) :
> 50 000. E28 est le proxy sur 5 colonnes : 49 999 — l'écart de 1 est la paire naturelle
> 41 405/41 757 (même client, produit, magasin, date, montant ; **mode et remise
> différents**). Un candidat qui explique l'écart gagne son point même s'il inverse les
> deux ; un candidat qui ne les explique pas et les inverse en perd un.

---

## D · Étude de cas — « Le rapport de la direction commerciale » (75 min · /20, seuil 12)

**Consigne.** La direction commerciale demande un rapport de **une page** avec 4 sections,
produit à partir de `commercial.duckdb`. Le candidat rend : (i) un fichier `rapport.sql`
contenant les 6 requêtes du rapport (exécutées, sorties capturées), et (ii) la page de
synthèse (texte). Barème :

| Section | Contenu | Points |
|---|---|---|
| D1 · Indicateurs globaux | CA brut, CA sans retours (P2), panier moyen, nb de ventes, nb de clients actifs — 1 requête | /4 |
| D2 · Par magasin | CA, nb de ventes, panier moyen par magasin (5 lignes) + détection du top — 1 requête | /4 |
| D3 · Par catégorie | CA et nb de ventes par **catégorie (id, pas rayon)** (8 lignes) + le top — 1 requête | /4 |
| D4 · Risques et pièges | les 3 défauts du socle chiffrés (8 doublons → 50 000 uniques ; 200 retours → CA propre 7 876 320 163 ; 15 dates inversées) + la nuance E27/E28 — 3 requêtes | /4 |
| D5 · Qualité | cohérence croisée (les CA par magasin somment au CA total), alias lisibles, 1 page lisible, chaque chiffre justifié par sa requête | /4 |

**Critères de passage de l'étude de cas (12/20) :**
- D1 sans le CA « gonflé » présenté comme le CA (P2 détecté) ;
- D3 avec 8 lignes (pas 5 — le rayon n'est pas la clé) ;
- D4 avec au moins 2 des 3 défauts chiffrés.

> **L'esprit de l'étude.** Le rapport est réussi quand la direction peut le lire **sans
> avoir à vérifier** : chaque chiffre traceable par sa requête, chaque piège nommé, les
> totaux cohérents entre sections. C'est la compétence finale du module — tout le reste
> (syntaxe, clauses) n'est que le moyen.

---

## Corrigés ligne à ligne

### B · Quiz — réponses

| Q | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| Réponse | b | b | b | b | b | b | b | b | b | b |

| Q | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
|---|---|---|---|---|---|---|---|---|---|---|
| Réponse | b | b | b | c | b | c | b | b | b | c |

Justifications en une ligne (bonus) :
- Q4 : l'ordre de priorité SQL est `AND` avant `OR` (d'où les parenthèses recommandées).
- Q8 : `NULL` — l'absence de valeur s'exprime par `NULL`, pas par 0 ; parade `COALESCE`.
- Q15 : `COALESCE` ne regarde que les `NULL` ; un 0 est une valeur présente.
- Q17 : dans le `WHERE`, `NULL > 0` est `NULL` (ni vrai ni faux) : les lignes orphelines du
  droit sont éliminées, ce qui transforme le `LEFT` en `INNER`.
- Q20 : « tous les » = « aucun contre-exemple » = double négation ; `IN` dit « au moins un ».

### C · Exercices — valeurs de référence (clés de traçabilité)

| # | Valeur | Clé `chiffres_cites.json` |
|---|---|---|
| E01 | 50 008 | `m07p_ventes_brutes` |
| E02 | 7 908 259 731 | `m07p_q04_ca_total_brut` |
| E03 | 362 | `m07p_q02_produits_actifs` |
| E04 | 512 | `m07_clients_ouagadougou` |
| E05 | 7 136 | `m07_ventes_dimanche` |
| E06 | 158 140 | `m07_panier_moyen` |
| E07 | 594 363 | `m07_top_montant_ttc` |
| E08 | 763 | `m07_min_montant` |
| E09 | 4 | `m07_top_magasin_id` |
| E10 | 1 596 813 264 | `m07_ca_mag_4` |
| E11 | 24 920 | `m07_ventes_2025` |
| E12 | 3 983 044 060 | `m07_ca_2026` |
| E13 | 20 175 | `m07_ventes_mode_1` |
| E14 | 1 944 001 846 | `m07_ca_mode_2` |
| E15 | 4 | mesuré (HAVING > 6 500 : catégories 1, 4, 7, 8) |
| E16 | 6 798 | `m07_ventes_cat_7` |
| E17 | 490 | `m07p_q18_plafond_sup_100k` |
| E18 | 850 | `m07_clients_particuliers` |
| E19 | 1 482 606 616 | `m07_ca_type_entreprise` |
| E20 | 247 | `m07_clients_koudougou` |
| E21 | 15 746 | `m07_tranche_sup_200k` |
| E22 | 12 753 | `m07_tranche_inf_50k` |
| E23 | 4 997 | `m07_ventes_mag4_2026` |
| E24 | 471 206 245 | `m07_ca_produit_inactif` |
| E25 | 11 561 026 | `m07_top_client_ca` |
| E26 | 18 364 | `m07_ventes_ville_bobodioulasso` |
| E27 | 50 000 | `m07p_q19_nb_ventes_uniques` |
| E28 | 49 999 | `m07p_q19_distinct_5col` |
| E29 | 47 359 | `m07p_q23_couples_distincts` |
| E30 | 4 568 | `m07p_q27_nb_ventes_bobo_bricolage` |
| E31 | 119 | `m07_clients_tous_2_plus_chers` |
| E32 | 120 | `m07_vue_mensuelle_lignes` |
| E33 | 78 965 529 | `m07_vue_plus_gros_mois` |
| E34 | 20 289 | `m07_ventes_sup_moyenne` |
| E35 | 190 | `m07p_q26_produits_sup_moyenne_rayon` |

### D · Étude de cas — points de repère du corrigé

- **D1** : CA brut 7 908 259 731 ; CA sans retours 7 876 320 163 (200 retours, écart
  31 939 568) ; panier moyen 158 140 (158 159 sans retours) ; 50 008 ventes ; 1 200 clients.
- **D2** : 5 lignes (magasin 4 en tête : 1 596 813 264 FCFA / 10 061 ventes / 158 713 de
  panier moyen ; magasin 3 en queue : 1 564 937 883 / 9 873 / 158 507).
- **D3** : 8 lignes par id (Decoration en tête : 1 236 006 465 FCFA / 6 798 ventes ;
  Bricolage-Outillage en queue : 699 533 080 / 5 381). Si 5 lignes apparaissent, le
  candidat a groupé par `rayon` (le piège C05) : -2 sur D3.
- **D4** : 50 008 → 50 000 uniques (8 doublons ; proxy 5 colonnes : 49 999, paire 41 405 /
  41 757) ; CA propre 7 876 320 163 (P2) ; 15 ventes avec `date_vente > date_limite_remise`
  (P3).
- **D5** : les CA des 5 magasins somment à 7 908 259 731 (avec retours) — incohérence =
  jointure qui double (P4) ; chaque chiffre de la page pointe sa requête dans
  `rapport.sql`.
