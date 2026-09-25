# Plan M13 — Modélisation des données

**Sept chapitres · 30 h · niveau N3 → N4 · budget 105 pages [89, 121] · projet « Le modèle de Sahel
Distribution » (4 livrables, **4e** pièce du portfolio) · évaluation 75 points (quiz 15 Q, 2 exercices de
normalisation, étude de cas « trois tableaux reliés donnent un CA faux de 40 % »).**

**Position dans le parcours.** M13 est le **premier module de la phase « construire »** après les
fondamentaux : M11 a donné la matière et les requêtes, M12 a donné les indicateurs et leur carte — M13
**bâtit la structure** qui fait tenir les deux. Le module ne se contente pas de dessiner : il produit un
**modèle exécutable**, vérifié par des contrôles de clés, de grain et d'orphelins, et il mesure lui-même
les défauts qu'il dénonce — **× 44** de chiffre d'affaires pour une jointure oubliée, **− 36 %** de
chiffre d'affaires pour une jointure qui filtre sans le dire, **+ 43 %** pour un modèle qui additionne
deux tableaux de montants.

---

## 1. Cadrage

### 1.1 Position dans l'architecture

| Source | Ce qui est repris tel quel |
|---|---|
| `00_architecture/01_architecture_pedagogique.md` §M13 | **7** chapitres de **5/5/5/5/4/3/3** h (30 h), N3 → N4, prérequis M06, M11, M12 ; les **9** illustrations prévues ; le projet « Le modèle de Sahel Distribution » ; l'évaluation (quiz 15 Q, **2** exercices de normalisation, étude de cas « **3** tableaux reliés donnent un CA faux de **40 %** ») |
| §B.6 | barème : quiz 22 modules (seuil **14/20**), étude de cas 21 (seuil **12**), projet (seuil **13**) |
| §E.3, §E.4 | **30** projets et **180** exercices du manuel : M13 apporte **9** exercices autonomes et **1** projet |
| `tools/budget_pages.py` | **7** × 12,5 = **88** p. de matière + **17** p. d'appareil = **105** p. ; fourchette ± 15 % = **[89, 121]** |
| Avis de la direction du manuel | **Ne pas refaire M12.C05** : C05 **nomme** les sept étages de la chaîne BI ; M13 **construit** l'étage 4 — le modèle — et prépare l'étage 5 dont la carte des **10** KPI existe déjà |
| Décision M12 (à ne pas défaire) | les ventes restent celles de M01—M03 ; M12 a ajouté **5** sources opérationnelles ; M13 n'en ajoute que **2**, et uniquement de l'**historique**, parce qu'un SCD de type 2 ne se démontre pas sans histoire |

### 1.2 Sept compétences de sortie (la matrice de couverture)

| # | Compétence | Chapitre | Ce qui la prouve dans le module |
|---|---|---|---|
| 1 | Passer d'un besoin à un modèle conceptuel, logique puis physique | C01 | MCD des **5** entités du fil rouge, MLD, puis `CREATE TABLE` exécuté |
| 2 | Normaliser jusqu'à la **3FN** et savoir pourquoi | C02 | la table plate des ventes (**240 000** lignes) ramenée à **6** tables sans perte |
| 3 | Reconnaître et éviter les **4** anomalies | C02, C07 | démonstration sur **12** lignes : mise à jour, insertion, suppression, jointure |
| 4 | Choisir le **grain** d'une table de faits et le tenir | C03 | trois grains dans le même schéma, jamais mélangés |
| 5 | Construire un **schéma en étoile** et le rendre conforme | C04 | **5** dimensions, **7** tables de faits, dimensions conformes partagées |
| 6 | Gérer les **changements lents** (SCD 0/1/2/3) | C04 | **1 120** mouvements clients, **616** révisions tarifaires |
| 7 | Construire un **calendrier** juste et un modèle **vérifié** | C06, C07 | **1 339** jours, **18** fériés, **15** points de revue passés sur le modèle du projet |

### 1.3 Fait du socle (mesuré le 25/09/2026 — à figer en clés `m13_*` à l'étape 2)

**Les dimensions du fil rouge, telles qu'elles existent déjà** (aucune donnée inventée) :

| Dimension | Lignes | Attributs | Ce qu'elle apporte au module |
|---|---|---|---|
| `client` | **23 912** | nom, type (**4** valeurs), segment (**3**), ville (**5**), région, date de création, conditions de paiement | **416** clients sans aucune vente : la dimension est plus large que les faits ; **153** noms en doublon : la clé technique n'est pas un luxe |
| `produit` | **154** | désignation, catégorie (**16** libellés), sous-catégorie (**12**), unité, prix, poids, fournisseur, TVA, actif | **16** libellés pour **7** familles : le défaut de dimension déjà mesuré en M11, que M13 corrige par un modèle, pas par une requête |
| `magasin` | **6** | nom, ville, quartier, région, type, surface, responsable, ouverture | **1** magasin sans vente (le dépôt) : dimension incomplète ou fait manquant, il faut choisir |
| `vendeur` | **22** | nom, magasin de rattachement, date d'embauche, statut, secteur | hiérarchie magasin → vendeur, et **0** vendeur sans vente |
| `date` | **1 339** | année, trimestre, mois, semaine ISO, jour, dimanche, férié, événement | **44** mois, **18** jours fériés, **5** événements : la matière de C06 |
| `objectif_mois` | **218** | magasin × mois, objectif de CA, objectif de marge | **6 685 260 000** FCFA d'objectifs, soit **42,9 %** du CA net : un **fait** déguisé en table de référence |

**Les faits, et leurs grains — chacun prouvé par une clé :**

| Fait | Lignes | Grain | Contrôle |
|---|---|---|---|
| ventes | **240 000** | ligne de ticket | `COUNT(*) = COUNT(DISTINCT id_vente)` |
| commandes | **9 000** | commande | clé unique |
| encaissements | **9 000** | facture | clé unique |
| stock mensuel | **6 776** | produit × mois | clé composite unique |
| ruptures | **2 428** | produit × magasin × mois | clé composite unique |
| logistique | **264** | magasin × mois | clé composite unique |

**Les défauts mesurés, qui deviennent la matière des chapitres** :

| Défaut du modèle existant | Mesure | Chapitre qui le traite |
|---|---|---|
| jointure sur la mauvaise clé | ventes × logistique sur le magasin seul : **10 560 000** lignes (**× 44,0**) et **× 44,0** de CA | C03, C05, C07 |
| jointure qui filtre sans le dire | ventes × ruptures sur produit et mois : **86 113** lignes, CA **× 0,36** (les ventes sans rupture disparaissent) | C03 |
| jointure déjà au bon grain | ventes × stock sur produit et mois : **240 000** lignes, **× 1,00** | C03 |
| point de départ à nettoyer | ventes × commandes et ventes × encaissements sur le client : CA **× 0,31** chacun | C01 |
| modèle fautif qui additionne | ventes + commandes : **22 305 610 960** FCFA (**+ 43,0 %**) ; les trois tableaux (avec encaissements) : **29 474 916 530** FCFA (**+ 89,0 %**) | étude de cas |
| modélisation du temps | **1 339** jours, **18** fériés, **5** événements — et **aucune** année fiscale ni semaine commerciale | C06 |
| mise à jour d'un attribut | **153** noms de clients en doublon, **416** clients sans vente | C02, C04 |

### 1.4 Le projet M13.P — « Le modèle de Sahel Distribution »

**Quatre livrables, 20 points, seuil 13** (barème calqué sur M11 et M12) :

| Livrable | Points | Contenu exigé |
|---|---|---|
| **P1 — MCD et MLD** | **6** | modèle conceptuel des **5** entités du fil rouge (client, produit, magasin, vendeur, temps) avec cardinalités ; modèle logique : **5** dimensions, **7** faits, clés, grain écrit sous chaque table |
| **P2 — Script de création exécutable** | **6** | `CREATE TABLE` + `INSERT` rejouables, clés primaires et étrangères, contraintes d'intégrité, et **4** contrôles de recette : unicité des clés, grains, orphelins, totaux |
| **P3 — Revue de modèle en **15** points** | **5** | la grille de C07 passée sur son propre modèle, avec la preuve pour chaque point et les défauts corrigés **listés** |
| **P4 — Note de choix (3 pages)** | **3** | justification de chaque décision : étoile ou flocon, SCD type retenu et pourquoi, dénormalisations assumées, ce qui a été refusé et pourquoi |

**Le livrable est un document de portfolio** : c'est le **4e** des **5** morceaux exigés (après les rapports
SQL de M11, la carte de **10** KPI de M12, et avant la bibliothèque DAX de M15 et le dossier de
soutenance de M19).

### 1.5 Évaluation M13

**75 points au total, seuil de réussite 48.**

| Partie | Points | Contenu |
|---|---|---|
| **A. Quiz** | **20** | **15** questions (seuil **11**) sur les cardinalités, les formes normales, le grain, les SCD, le calendrier |
| **B. Deux exercices de normalisation** | **20** | **N1** : partir d'une table plate de **12** lignes et la normaliser en **3FN**, en nommant les **4** anomalies évitées ; **N2** : dénormaliser volontairement une dimension et **chiffrer** le gain et le coût |
| **C. Étude de cas** | **30** | « **trois tableaux reliés donnent un CA faux de 40 %** » : diagnostiquer, mesurer, corriger, prouver (seuil **18**) |
| **D. Auto-test** | **5** | **12** requêtes de contrôle du modèle : clés, grains, orphelins, totaux, historisation |

### 1.6 Règles d'exécution (cadence héritée de M06—M12)

1. **Un push par chapitre** validé `--strict`, plus le plan **avant** le socle, et la clôture à la fin.
2. **Tout chiffre** de quatre chiffres ou plus existe dans `chiffres_cites.json` (bloc `M13`), ou est
   reformulé.
3. **Trois planches** `figures/` : ≤ **776** px, texte réel (`svg.fonttype = none`), déterministes,
   citées par leur chapitre.
4. **PDF** composé après l'autovalide, contrôlé par `controle_pdf.py M13` (glyphes, figures, bloquants).
5. **JPEG ?** Non : le module ne publie que des **SVG** produits par script, comme M08 à M12.

### 1.7 Les huit décisions de modélisation du fil rouge (le fil du module)

Le module ne discute pas dans le vide : il **tranche huit questions** sur le modèle de Sahel Distribution,
et chaque réponse devient une section démontrée.

| # | Question | Décision du module | La mesure qui la justifie |
|---|---|---|---|
| 1 | Une seule grosse table ou un modèle ? | **modèle** : **5** dimensions + **7** faits | **240 000** lignes de ventes à **18** colonnes, contre **12** tables dont chacune ne porte que son sujet |
| 2 | Jusqu'où normaliser ? | **3FN** pour les référentiels, **dénormalisation assumée** pour les dimensions de restitution | **16** libellés pour **7** familles : la correction appartient au référentiel |
| 3 | Quel grain pour les ventes ? | **ligne de ticket** | `COUNT(*) = COUNT(DISTINCT id_vente)` = **240 000** |
| 4 | Faut-il une table de dates ? | **oui, une seule**, et jamais la date du fait | **1 339** jours, **18** fériés, **44** mois |
| 5 | Comment suivre les changements de segment client ? | **SCD type 2**, avec période de validité | **1 120** mouvements générés, **2** statuts par client concerné |
| 6 | Et les changements de tarif ? | **SCD type 2** aussi, parce que la marge dépend du prix **de la période** | **616** révisions, et l'écart de prix réel de M12 (**+ 25,0 %** de **8 219** à **10 271** FCFA) |
| 7 | Étoile ou flocon ? | **étoile** par défaut, **flocon** seulement là où il paie : la hiérarchie produit | **16** libellés → **7** familles : **2** jointures contre **1**, pour une dimension **154** lignes |
| 8 | Quelles dimensions sont conformes ? | le temps, le magasin, le produit, le client : **les mêmes** dans les **7** faits | un seul `dim_magasin` sert les ventes, les ruptures, la logistique et les objectifs |

---

## 2. Vocabulaire du module (à définir au premier emploi)

**Définitions imposées** (encadrés « Définition » des sept chapitres) : *entité*, *attribut*, *relation*,
*cardinalité*, *clé primaire*, *clé étrangère*, *clé technique* (*surrogate key*) et *clé métier*, *modèle
conceptuel* (MCD), *logique* (MLD) et *physique* (MPD), *1FN*, *2FN*, *3FN*, *forme normale de Boyce-Codd*,
*anomalie de mise à jour / d'insertion / de suppression*, *dénormalisation*, *table de faits*, *dimension*,
*grain*, *mesure additive*, *semi-additive* et *non additive*, *schéma en étoile*, *schéma en flocon*,
*dimension conforme*, *hiérarchie*, *changement lent de dimension* (SCD, types **0** à **3**), *table
calendrier*, *année fiscale*, *semaine commerciale*, *table de pont* (*bridge table*), *dimension
déchet* (*junk dimension*), *revue de modèle*.

**Anglicismes** : toujours accompagnés de leur traduction — *surrogate key* → **clé technique**,
*slowly changing dimension* → **changement lent de dimension**, *bridge table* → **table de pont**,
*conformed dimension* → **dimension conforme** ; *star schema* rendu par **schéma en étoile** dans tout
le module, l'anglais n'étant donné qu'à la première occurrence.

---

## 3. Découpage en 7 chapitres

| Ch. | Titre | Contenu | Sections | H | Pages |
|---|---|---|---|---|---|
| **C01** | Modéliser : entités, attributs, relations, cardinalités | MCD, MLD, MPD ; le passage du tableur au modèle ; les **5** entités du fil rouge ; les **3** niveaux de lecture d'une relation | 15 | 5 | 12,5 |
| **C02** | Normaliser : 1FN, 2FN, 3FN, et les **4** anomalies | formes normales ; **4** anomalies démontrées sur **12** lignes ; quand **ne pas** normaliser ; le coût mesuré de la normalisation | 16 | 5 | 12,5 |
| **C03** | La dimension analytique : grain, additivité, faits | grain unique par table ; additif, semi-additif, non additif ; le théorème du « ne jamais mélanger les grains » ; les **3** façons de fabriquer un faux total | 16 | 5 | 12,5 |
| **C04** | Le schéma en étoile et les changements lents | dimensions conformes, attributs, hiérarchies ; SCD **0/1/2/3** sur les clients et les tarifs ; la requête « comme c'était au moment des faits » | 16 | 5 | 12,5 |
| **C05** | Le schéma en flocon et ses variantes | flocon, hiérarchies partagées, **table de pont** pour le N-M, **dimension déchet**, faits multiples ; quand dénormaliser exprès | 15 | 4 | 12,5 |
| **C06** | Temps et calendrier | `dim_date` complète ; année fiscale, semaine commerciale, jours fériés locaux ; la règle « une seule table date par modèle » ; les **6** pièges de dates | 15 | 3 | 12,5 |
| **C07** | Qualité du modèle, documentation, revue en 15 points | contrôles automatiques (clés, grains, orphelins, totaux) ; documentation du schéma ; impacts sur les performances et sur la justesse des calculs ; **grille de revue en 15 points** | 16 | 3 | 12,5 |

**Progression interne** : C01 pose les objets et les cardinalités ; C02 nettoie le tableau de départ ;
C03 installe le grain et l'additivité, qui sont la grammaire de tout le reste ; C04 construit l'étoile et
gère le temps qui passe dans les dimensions ; C05 complète quand l'étoile ne suffit pas ; C06 traite le
temps du modèle ; C07 vérifie, documente et fait relire le modèle par une grille.

**Le fil rouge du module** est le **modèle lui-même** : chaque chapitre ajoute une pièce, et le projet
livre l'ensemble. À la fin, le modèle de Sahel Distribution existe en SQL exécutable, avec ses contrôles.

---

## 4. Budget pages

| Poste | Pages |
|---|---|
| C01 → C07 (7 × 12,5) | 88 |
| Appareil de module (ouverture, bilan, projet, évaluation) | 17 |
| **Total M13** | **105** |

Fourchette de validation **± 15 %** : **[89, 121]** pages. Contrôle : `tools/budget_pages.py --mesure`
puis `tools/render.py` + `tools/controle_pdf.py M13`.

**Trois planches prévues** (sur les **9** illustrations de l'architecture, celles qui gagnent à être
dessinées) :

1. `M13_C03_grain_et_explosion.svg` — les **3** grains du fil rouge et l'explosion en lignes (**× 44**),
   sur six lignes de données.
2. `M13_C04_frise_scd.svg` — les **4** types de SCD sur la frise d'un changement de tarif, avec
   l'attribut « comme au moment des faits ».
3. `M13_C07_grille_revue.svg` — la grille de revue en **15** points, avec les **5** défauts à trouver
   annotés sur le modèle fautif.

Les **6** autres illustrations de l'architecture (étoile contre flocon, anomalie avant/après, architecture
complète, tickets → table plate → étoile) seront **décrites en tableaux et en texte** : le manuel tient
sa règle de ne pas multiplier les images sans nécessité pédagogique.

---

## 5. Chiffres cibles (à figer dans `chiffres_manuel.py M13`)

- **Le socle de dimensions** : client **23 912** (dont **416** sans vente, **153** noms en doublon,
  **3** segments, **4** types, **5** villes) · produit **154** (**16** libellés, **12** sous-catégories,
  **7** familles) · magasin **6** (dont **1** dépôt sans vente) · vendeur **22** · date **1 339** jours
  (**44** mois, **18** fériés, **5** événements).
- **Les faits** : ventes **240 000** lignes (**237 191** hors retours) · commandes **9 000** ·
  encaissements **9 000** · stock **6 776** · ruptures **2 428** · logistique **264**.
- **Les défauts mesurés** : jointure sur le magasin seul **× 44,0** (**10 560 000** lignes) · jointure
  qui filtre **× 0,36** (**86 113** lignes) · jointure correcte **× 1,00** · deux tableaux de montants
  additionnés **+ 43,0 %** (**22 305 610 960** FCFA) · trois tableaux **+ 89,0 %**
  (**29 474 916 530** FCFA).
- **Les objectifs** : **218** lignes, **5** magasins × **44** mois, **6 685 260 000** FCFA, soit
  **42,9 %** du CA net — le piège du « fait déguisé en référentiel ».
- **Les SCD** : **1 120** mouvements de clients (segment et ville), **616** révisions tarifaires
  (**154** produits × **4** dates), **2** types de changement à distinguer (correction ou histoire).
- **Le modèle cible** : **5** dimensions (client, produit, magasin, vendeur, temps), **7** tables de
  faits, **12** tables, **4** contrôles de recette (unicité, grain, orphelins, totaux), **12** clés
  étrangères vérifiées, **15** points de revue.

---

## 6. Risques et parades

| Risque | Parade |
|---|---|
| Un module de modélisation qui reste théorique | **Tout** le modèle du module est **exécutable** : `socle_m13.sql` crée les **12** tables, et `tools/modele_M13.py` rejoue **4** contrôles (clés, grains, orphelins, totaux) et publie le verdict |
| Refabriquer les données du fil rouge | M13 n'ajoute **que de l'historique** — **1 120** mouvements de clients et **616** révisions tarifaires — parce qu'un SCD de type 2 ne se démontre pas sans histoire ; tout le reste sort des sources existantes |
| Recouvrir M12.C05 (architecture) | Frontière écrite : M12 **nomme** les sept étages et leurs pannes ; M13 **construit** l'étage « modèle » et le prouve par des contrôles |
| Recouvrir M14 (Power BI) | M13 s'arrête au modèle **logique** et à sa traduction SQL ; la traduction en relations d'outil, la cardinalité et le sens du filtrage sont **cités** une fois, dans C07, et **outillés** en M14 |
| Un chapitre C05 (flocon) qui paraît optionnel | Chaque variante (pont, déchet, faits multiples) est présentée **avec son cas d'usage manqué** : ce qu'on n'aurait pas pu modéliser sans elle — les retours (faits multiples), les campagnes multi-produits (pont), les statuts hétérogènes (déchet) |
| Les exercices de normalisation qui se ressemblent | N1 part d'une table plate et **monte** vers la 3FN ; N2 part d'une dimension propre et **redescend** volontairement — deux directions, deux barèmes |
| Le modèle du projet devient un dessin invérifiable | P2 exige un script **exécutable** et **4** contrôles, dont le contrôle d'orphelins ; P3 exige la preuve par point |

---

## 7. Étapes de production (calque M05—M12)

1. **Étape 1 — Plan** : ce fichier (poussé avant toute rédaction).
2. **Étape 2 — Socle et instruments** : `tools/dossier_M13.py` construit le dossier
   `03_exercices/dossier_M13/` : `socle_m13.sql` (**12** tables : **5** dimensions, **7** faits),
   `mouvements_clients.csv` (**1 120** lignes), `tarifs_produits.csv` (**616** lignes),
   `table_plate.csv` (l'extrait dénormalisé de **18** lignes pour C02), `modele_fautif.sql` (les trois
   requêtes fautives : **+ 43,0 %**, **+ 89,0 %**, **× 44,0**), `connexion.py`, `ATTENDU.json` (les mesures de référence),
   `revue_modele.md` (le modèle annoté des **5** défauts à trouver) ;
   `tools/modele_M13.py` : **4** contrôles automatiques (unicité, grain, orphelins, totaux), la mesure
   des SCD et le compte de la grille de revue ; bloc `m13_*` dans `chiffres_manuel.py`.
3. **Étape 3 — Rédaction** : C01 → C07, un push par chapitre validé `--strict`.
4. **Étape 4 — Figures** : **3** planches (`tools/figures_M13.py`) — grain et explosion, frise des SCD,
   grille de revue ; largeur ≤ **776** px, texte réel, déterministes, citées par leur chapitre.
5. **Étape 5 — PDF** : `tools/render.py "0[234]_*/M13_*.md" --join --out 05_livrables/M13.pdf` puis
   `tools/controle_pdf.py M13` — viser **[89, 121]** pages, 0 défaut bloquant.
6. **Étape 6 — Fiche de contrôle** : `05_livrables/fiche_controle_M13.md` (Q1—Q10).
7. **Étape 7 — Projet + évaluation + clôture** : `03_exercices/M13_projet.md` (**4** livrables, seuil
   **13**), `04_evaluations/M13_evaluation.md` (**75** points, seuil **48**), `README.md`,
   `05_livrables/etat_avancement.md`, `05_livrables/journal_pushs.md`, et le **contrôle final d'existence
   nommée** de chaque livrable (PATCH_6).
