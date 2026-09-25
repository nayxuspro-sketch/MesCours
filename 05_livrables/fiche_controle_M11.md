# Fiche de contrôle — module M11 (SQL avancé pour la BI)

**Porte de validation §G.1 de l'architecture (contrôles Q1 à Q10) · passée le 24 septembre 2026 ·
10/10 au vert, zéro écart bloquant, quatre nuances déclarées en fin de fiche (mesure de performance
gelée plutôt que relue à l'horloge ; corrections de chiffres assumées en cours de rédaction ; errata
de palier §C.3 ; partitionnement cité et non exécuté).**

Cette fiche documente la livraison du module M11 — *SQL avancé pour la BI* — sept chapitres
(N3 → N4, 30 h) qui font passer l'écriture SQL de la question simple au **rapport défendable** :
fenêtres et partitions, rangs et cumuls, séries temporelles, cohortes et RFM, requêtes avancées, plans
d'exécution, style et tests de non-régression. Elle ne raconte pas les intentions : chaque ligne donne
la commande exécutée et ce qu'elle a rendu.

## 1. Les commandes de contrôle, et leur sortie réelle

| Commande | Sortie obtenue le 24 septembre 2026 |
|---|---|
| `python3 01_socle_donnees/scripts/autovalide.py M11 --strict` | `Résultat : OK (0 avertissement(s))` sur **9 fichiers** (C01 à C07 + projet + évaluation) |
| `python3 01_socle_donnees/scripts/chiffres_manuel.py M11` | **301 clés** `m11_*` / `m11p_*` / `m11e_*` ; deux exécutions successives : `diff` de `chiffres_cites.json` = **0 ligne** → reproductible |
| `python3 tools/dossier_M11.py` | Socle régénéré : `socle_m11.sql` **3 595** octets, empreinte `sha256[:16]` = `447c7abdafd3ac14`, **identique** avant/après ; **5** tables + **2** vues ; **0** orphelin ; **1** client de vente absent du référentiel (le client **0**, documenté) ; `aucun fichier .duckdb : le socle est un script, il ne pèse rien en dépôt` |
| `python3 tools/figures_M11.py` | **2** planches produites, **2/2** déterministes (deux productions, même empreinte), **2/2** citées par leur chapitre : `M11_C01_carte_des_fenetres.svg` **609 px** et `M11_C04_matrice_retention.svg` **686 px** (limite 776) ; texte réel dans le SVG (`svg.fonttype = none`) |
| `python3 tools/render.py "0[234]_*/M11_*.md" --join --out 05_livrables/M11.pdf` | PDF rendu : `05_livrables/M11.pdf` · **1 042 Ko** · **97 pages** (**9** fichiers joints — les **7** chapitres, le projet et l'évaluation — + couverture + sommaire) ; les chapitres seuls en occupent **85** |
| `python3 tools/controle_pdf.py M11` | `M11 : 97 pages · figures : 2/2 vérifiées dans le PDF par leur libellé propre · glyphes : 29/29 composés · Défauts bloquants : 0` |
| `python3 tools/controle_sql_M11.py` (nouveau) | `18 controles sur 18 : OK — le socle et le fichier publie disent la meme chose.` Chaque ligne compare une requête exécutée **à l'instant** à une valeur **publiée** plus tôt : deux chemins indépendants, un verdict par ligne, code de sortie |
| `python3 tools/perf_M11.py --figer` | Mesures **gelées** (médiane de **5** exécutions, DuckDB 1.5.5, **24/09/2026**) : vue **142** ms / table **1** ms ; `SELECT *` **581** ms / trois colonnes **96** ms ; fenêtre **150** ms / sous-requête scalaire **292** ms ; index client **0,6** → **0,5** ms, plan `SEQ_SCAN` |
| `python3 tools/budget_pages.py --mesure` | `M11 : 9 fichiers · budget 105 p.` — module composé **97 p.** pour **105 p.** (**−7,6 %**) ; chapitres seuls **85 p.** pour une allocation de **81 p.** de matière (**+4,9 %**) ; fourchette **[89, 121] p.** respectée |
| `python3 tools/poids.py` | `atelier : 119,0 Mo persistés sur 128 · 327 fichiers · marge +9,0 Mo` — le socle M11 n'ajoute aucun fichier de données (script de **3 595** octets) |
| `python3 tools/render.py "03_exercices/M11_projet.md" --out /tmp/projet_M11.pdf` puis `"04_evaluations/M11_evaluation.md"` | projet **7 p.** · évaluation **9 p.** — la base de la comparaison au budget de Q6 |
| `python3 -c "from pypdf import PdfReader; print(len(PdfReader('05_livrables/M11.pdf').pages))"` | `97` — confirme le contrôleur |

**Le verdict le plus fort du module.** Les **18** contrôles rejouent le socle et retrouvent **les
valeurs publiées** — y compris les plus piégeuses : **23 444** pour le rang maximal des clients par
nombre de tickets (contre **21** en `DENSE_RANK`), **1,65** pour le rapport saisonnier, **47** lignes
de `GROUPING SETS`, **42 658** lignes du client **0**. Et l'instrument a **trouvé deux erreurs — les
siennes** : il comptait d'abord **43 161** lignes pour le client **0** (retours compris, là où la
valeur publiée est en ventes nettes) et lisait **23 497** au lieu de **23 444** parce qu'il avait
réécrit l'ordre de tri de la requête. Les deux corrections sont publiées dans C07 (§5.6 et « Dans les
faits »), pas cachées : c'est exactement ce qu'un contrôle croisé doit faire.

## 2. Les dix contrôles Q1 à Q10

### Q1 — Plan posé avant rédaction
- **Verdict : OK.** `05_livrables/plan_M11.md` (≈ **3 900** mots) poussé **avant** le socle et la
  rédaction : 7 chapitres (C01 → C07, 30 h, N3 → N4), budget **105 p.** [**89**, **121**], projet
  « Les **12** rapports SQL de la cellule commerciale » — **4** livrables notés **8 + 5 + 4 + 3 = 20**
  points, seuil **13** : P1 les **12** requêtes, P2 le jeu de tests, P3 la note de lecture de **2**
  pages, P4 la fiche de reprise de **3** rapports —, évaluation (quiz **20** Q en **4** familles de **5**
  + **5** exercices dont **2** de type E4 sur requêtes erronées + étude de cas + **18** requêtes
  auto-testées), **2** figures, **20** requêtes de référence.
- **Sortie :** plan poussé au push n° **36**, socle et instruments au n° **37**, chapitre C01 au
  n° **38**. Le projet et l'évaluation livrés **suivent la structure du plan** (livrables, barème et
  familles de questions identiques) : une évaluation qui s'écarte de son plan au moment du rendu ne
  mesure plus ce qui a été annoncé.

### Q2 — Socle de données reproductible
- **Verdict : OK.** Le socle du module est un **script SQL** (`03_exercices/dossier_M11/socle_m11.sql`,
  **3 595** octets, empreinte `447c7abdafd3ac14`) accompagné de `connexion.py` (`ouvrir(materialiser=
  False|True)`). Il **ne crée aucune donnée** : **5** tables de référence (produit **154**, magasin
  **6**, vendeur **22**, objectif_mois **218**, calendrier **1 339** jours) et **2** vues `read_csv_auto`
  sur les CSV déjà versionnés (**240 000** lignes de vente, **23 912** clients référencés).
- **Contrôles d'intégrité :** **0** orphelin sur `id_magasin`, `id_vendeur`, `id_produit` ; **1**
  client de vente absent du référentiel (le client **0**, fait central du module) ; rejeu du DDL en
  **0,25 s**.
- **Contrainte de poids, mesurée et expliquée :** un fichier DuckDB contenant **154** lignes pèse
  **536 576** octets — un plancher fixe. Le socle reste donc un script, et les démonstrations de
  volume (C06) passent par une **matérialisation en mémoire**, jamais par un second fichier de base.

### Q3 — Chiffres cités traçables
- **Verdict : OK.** **301** clés `m11_*` / `m11p_*` / `m11e_*` dans
  `01_socle_donnees/data/reference/chiffres_cites.json`, produites par `chiffres_manuel.py M11` ;
  tout nombre de quatre chiffres ou plus cité dans les 9 fichiers est couvert par une clé — les
  **quatre** manques détectés par l'autovalidation ont été **sourcés**, pas supprimés :
  `m11_c03_trou_objectif_mois` (**42 514 372** ; **51 235 118** FCFA),
  `m11_c04_inactifs` (**663 520 490** FCFA), `m11_c07_controle_client0` (**43 161** lignes),
  `m11_c02_top3_familles` (**21** lignes).
- **Deux corrections de fond** ont été apportées au fichier publié pendant la rédaction : le rang du
  top 3 par famille (**18** lignes annoncées → **21** mesurées : 3 × **7** familles, et non 3 × **6**)
  et le nombre de familles du catalogue (**6** → **7**), la mesure remplaçant une affirmation.
- **Format :** unités non doublées (le formateur rend déjà « 15 595 154 955 FCFA »), valeurs Python
  vérifiées avant publication.

### Q4 — `autovalide.py --strict` : 0 avertissement
- **Verdict : OK.** `Résultat : OK (0 avertissement(s))` sur **9** fichiers (C01 → C07, projet,
  évaluation). Le seuil §B.4 est tenu **dès la rédaction** pour C02 à C07 (**4** à **5** encadrés
  « Définition », **2** à **3** « Attention », **1** « Conseil professionnel », **1** « Dans les
  faits » par chapitre) ; C01, écrit avant la leçon, a été repatché (**6 722** → **6 747** mots).
- **Leçon consignée :** `--strict` compte les encadrés par chapitre ; un chapitre rédigé sans les
  compter les ajoute après coup — l'autovalidation sert aussi à **écrire**, pas seulement à vérifier.

### Q5 — Figures SVG auditées
- **Verdict : OK.** **2** planches seulement, conformément au plan (module de requêtes, pas de
  graphiques) : `figures/M11_C01_carte_des_fenetres.svg` (**609 px** × 245 px) et
  `figures/M11_C04_matrice_retention.svg` (**686 px** × 425 px) — largeur maximale **686 px** pour une
  limite de **776**.
- **Déterminisme :** `svg.hashsalt` fixé et métadonnée de date neutralisée ; deux productions
  successives rendent la **même empreinte** (`2/2 déterministes`) — c'est le contrôle qui rend une
  figure publiable dans un dépôt.
- **Texte extractible :** `svg.fonttype = "none"` — sans ce réglage, les libellés partent en
  **tracés** et le contrôle du PDF ne peut plus prouver que la figure a été embarquée. Le premier
  rendu, en tracés, a été **refusé** (`figures : 0/2`) ; après correction, `2/2`.

### Q6 — PDF : budget de pages respecté
- **Verdict : OK.** `05_livrables/M11.pdf` : **97** pages, **1 042 Ko**, **9** fichiers joints (les
  **7** chapitres, le projet en **7 p.** et l'évaluation en **9 p.**) + couverture + sommaire.
- **Comparaison au budget :** **97 p.** composées pour **105 p.** de budget, soit **−7,6 %** — la
  fourchette **[89, 121] p.** est tenue. Prise isolément, la matière des chapitres (**85 p.**) dépasse
  de **+4,9 %** son allocation de **81 p.** (**13 · 13 · 11 · 11 · 11 · 13 · 9**) : la composition est
  dense, et le solde du budget va au projet et à l'évaluation.

### Q7 — `controle_pdf.py` : 0 défaut bloquant
- **Verdict : OK.** `97 pages · figures : 2/2 vérifiées dans le PDF par leur libellé propre ·
  glyphes : 29/29 composés · Défauts bloquants : 0`.
- **Typographie :** l'audit de glyphes ne trouve aucun caractère non composable ; le tiret
  demi-cadratin (U+2013) est **absent** des sept chapitres (contrôle `s.count("\u2013") == 0` avant
  chaque écriture) — il revient par les plages de dates, et deux chapitres de M02/M07 en portent
  encore, hors périmètre de ce module.

### Q8 — DuckDB exécuté
- **Verdict : OK.** Tous les chiffres SQL du module sont produits par des requêtes **exécutées** sur
  DuckDB 1.5.5 au-dessus du socle : fenêtres (**23 444** de rang maximal, **21** de `DENSE_RANK`),
  séries (**1 339** jours de calendrier, **2** trous d'objectif, **93 749 490** FCFA sans référence),
  cohortes (**44** cohortes, **15,8 %** de rétention pondérée à M+1), requêtes avancées (**47** lignes
  de `GROUPING SETS`, **21** lignes de top 3 sur les familles repliées).
- **Contrôle croisé d'un second moteur :** SQLite (natif Python, exécuté) porte la démonstration
  d'index de C06 — même réponse (**14** lignes et **5 578 688** FCFA pour le client **15676**), plan
  qui passe de `SCAN ventes_t` à `SEARCH ventes_t USING INDEX idx_ventes_client (id_client=?)`.
- **Contrôle croisé d'un second outil :** pandas recalcule le CA net et le compare à DuckDB
  (**15 595 154 955** FCFA des deux côtés) ; l'écart déclencherait une exception, il n'est pas toléré
  par arrondi complaisant.

### Q9 — PostgreSQL cité sans exécuté
- **Verdict : OK.** La mention figure en tête des **7** chapitres et dans le tableau §5.7 de C05
  (`QUALIFY` absent en PostgreSQL, `PIVOT` en SQL Server avec `FOR … IN`, `UNNEST` selon la source,
  `WITH RECURSIVE` sans le mot-clé en SQL Server). Aucun plan d'exécution PostgreSQL n'est publié,
  aucune sortie « PostgreSQL » n'est reproduite.
- La note de méthode de C06 (§5.8) publie explicitement ce qui **n'a pas** été mesuré : partitions,
  PostgreSQL, SQL Server — la même honnêteté que la fiche Q9 de M07.

### Q10 — Cohérence transverse (mêmes totaux, mêmes pièges, mêmes clés)
- **Verdict : OK.** Les **7** chapitres, le projet et l'évaluation publient les **mêmes** totaux de
  socle : **15 595 154 955** FCFA net, **237 191** lignes hors retours, **145 212** tickets,
  **23 497** clients de vente, **5** magasins, **44** mois, **1 339** jours de calendrier.
- **Les mêmes pièges traversent le module** et se répondent d'un chapitre à l'autre : le client **0**
  (**18,3 %** du CA, **38,1 %** → **24,2 %** de concentration), l'égalité modale des **3 316**
  clients à **8** tickets (**14,1 %**, qui rend tout `NTILE` instable sans départage), les **2**
  trous d'objectif du magasin 4, et la période partielle 2026 (**−28,9 %** contre **+15,4 %**).
- **Les deux socles sont comparés, jamais additionnés :** M11 (**240 000** lignes) et celui de
  M07/M09 (**50 008** lignes, **7 908 259 732** FCFA bruts) ; le chapitre C07 et le rapport **R12**
  du projet documentent l'écart (périmètre, période, retours) au lieu de le masquer.
- **Clés stables entre modules :** le relevé `chiffres_manuel.py` est rejoué deux fois et son fichier
  de valeurs est **identique** (`diff` = **0** ligne) ; le socle régénéré est **identique** au fichier
  versionné (empreinte `447c7abdafd3ac14`).

## 3. Nuances déclarées

1. **La performance se lit dans un fichier gelé, pas à l'horloge.** Les temps de C06 sont des
   **médianes de 5 exécutions** figées le **24/09/2026** dans `PERF_M11.json` par
   `tools/perf_M11.py --figer` ; `chiffres_manuel.py` **relit ce fichier** et ne mesure rien à
   l'horloge. Conséquence assumée : deux relevés donnent le même document, et une machine plus lente
   ne fait pas dériver le manuel. Contrepartie : les valeurs publiées ne décrivent pas l'ordinateur du
   lecteur, et le protocole est imprimé à côté de chaque chiffre.
2. **Quatre chiffres ont été corrigés en cours de route, dont deux de l'instrument lui-même.** Le top 3
   par famille (**18** → **21** lignes) et le nombre de familles (**6** → **7**) viennent d'une
   relecture du référentiel produits ; le comptage du client **0** (**43 161** → **42 658**) et le rang
   maximal (**23 497** → **23 444**) viennent du contrôle automatique, qui avait respectivement oublié
   d'exclure les retours et réécrit l'ordre de tri. Les quatre corrections sont **publiées** dans les
   chapitres concernés : un module qui cache ses corrections apprend au lecteur à s'en méfier.
3. **Errata d'architecture à porter à la clôture.** Le §C.3 de
   `00_architecture/01_architecture_pedagogique.md` étiquette M11 et M12 en palier **P3**, alors que
   le §C.1 place **M11 à M15** en **phase 4**. L'arbitrage retenu : **§C.1 fait foi** ; le correctif du
   §C.3 est appliqué au push de clôture, comme l'errata §E.7 l'a été pour M10.
4. **Le partitionnement est cité, non exécuté** (C06 §5.7). L'atelier n'a ni le volume ni le disque
   pour qu'une mesure soit interprétable ; aucun plan de partition n'est donc publié. C'est la règle
   §1.5 appliquée sans exception : on ne montre pas un plan qu'on n'a pas lu.

## 4. Synthèse

| Point | Vérification | Verdict |
|---|---|---|
| Q1 | Plan posé avant rédaction (n° **36**) | **OK** |
| Q2 | Socle reproductible : script de **3 595** octets, `447c7abdafd3ac14`, **0** orphelin | **OK** |
| Q3 | Chiffres traçables : **301** clés, **4** manques sourcés, **2** corrections mesurées | **OK** |
| Q4 | `autovalide --strict` : 0 avertissement sur **9** fichiers | **OK** |
| Q5 | Figures : **2/2** déterministes, **609** et **686** px, **2/2** citées | **OK** |
| Q6 | PDF : **97** p. de module pour **105** p. (**−7,6 %**), chapitres **85** p. (**+4,9 %** de leur allocation) | **OK** |
| Q7 | `controle_pdf` : **29/29** glyphes, **0** défaut bloquant | **OK** |
| Q8 | DuckDB exécuté ; SQLite et pandas en contrôle croisé | **OK** |
| Q9 | PostgreSQL et SQL Server cités, jamais exécutés | **OK** |
| Q10 | Mêmes totaux, mêmes pièges, deux socles comparés | **OK** |

**Ce que le module apporte au manuel.** Sept chapitres, **42 410** mots, **97** pages composées avec le projet et l'évaluation, **301**
clés de valeurs et **2** planches. Surtout : un **instrument de contrôle réutilisable**
(`tools/controle_sql_M11.py`, **18** requêtes) et une chaîne de mesure **honnête** — le protocole
imprimé à côté des temps, les corrections publiées, et l'instrument qui se corrige lui-même. Le module
M11 est le premier du manuel dont le livrable principal n'est pas un document mais un **jeu de
requêtes vérifiables** : chaque chiffre qu'il publie peut être rejoué par le lecteur, et le module dit
comment.

**État de publication.** Chapitres C01 à C03 poussés (jusqu'au push n° **38**, HEAD `62cd315`, puis
`9da71b4` pour C03) ; **C04 à C07**, le projet, l'évaluation et cette fiche sont validés et prêts —
leur poussée est en attente du jeton GitHub, refusé par l'API le 24/09/2026 (`401 Bad credentials`).
Le dépôt distant reste à **331** fichiers, **0** pyc, **17** PDF, sans perte : procédure de reprise en
ajout seul (`git fetch --depth 1` → `update-ref` → `read-tree` → `git add` nommé), jamais de
`git add -A`.
