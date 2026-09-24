# Projet M01.P — « Un petit fichier de ventes, une première fois »

**Module M01 · projet de fin de module · 5 h · à rendre avant le module 2 · barème /20, seuil de passage 13/20**

> **Le cadre réel.** Vous êtes engagé(e) comme analyste junior chez *Sahel Distribution SA*, grossiste en matériaux et quincaillerie, 5 magasins et 1 dépôt. Le service informatique est une personne, qui cumule avec la maintenance. Vous n'avez ni base de données, ni licence, ni mode d'emploi : vous avez un poste, un fichier CSV reçu par messagerie, et l'obligation de produire un chiffre que le directeur ne pourra pas contester. C'est exactement une première semaine de stage — et c'est la raison pour laquelle ce projet est noté, pas seulement « fait ».

---

## 1. Énoncé

### Le matériel

| Élément | Chemin | Ce que c'est |
|---|---|---|
| Fichier de travail | `01_socle_donnees/data/projection/ventes_magasin5_2025.csv` | extrait des ventes du magasin 5, année 2025 : **489 lignes × 13 colonnes** |
| Fichier du fournisseur | `01_socle_donnees/data/brut/tarif_fournisseur_peinture.csv` | grille de prix Peinture Saaba SARL : **42 lignes**, dont 38 utiles |
| Corrigé de référence | `01_socle_donnees/data/reference/ventes_magasin5_2025_ATTENDU.csv` | **480 lignes**, à ne pas ouvrir avant le rendu |
| Vos outils | tableur (Excel ou LibreOffice) + éditeur de texte + un traitement de texte | rien d'autre n'est requis ni autorisé |

### Les quatre livrables

**L1 — Fiche d'identité du fichier** (1 page). Les six phrases du chapitre C03 (nom et source · objet · grain · clé · mesures et attributs · étendue), suivies d'un tableau de **contrôles** : pour chacune des 13 colonnes, le type constaté, le nombre de valeurs distinctes, les bornes ou les modalités notables, et les défauts visibles. Vous devez avoir **compté** les défauts, pas les avoir devinés.

**L2 — Trois questions que l'on peut poser à ce fichier** (une demi-page). Chacune formulée en **question analytique complète** (objet, unité + définition, comparaison, périmètre, critère de réussite), plus une ligne « ce que ce fichier ne permet pas de répondre » par question.

**L3 — Une réponse chiffrée, sans autre outil que le tri et le filtre du tableur** (1 page). Vous choisissez **une** des trois demandes ci-dessous, vous y répondez avec un chiffre juste, et vous annexez la méthode en cinq lignes maximum (aucune formule complexe, aucune macro, aucun autre logiciel) :

- **a)** « Quelle catégorie de produits pèse le plus dans le chiffre d'affaires du magasin 5 en 2025, et à quelle hauteur ? » *(réponse attendue en L3-a du corrigé)*
- **b)** « Quel vendeur arrive en tête, et avec quel total ? » *(réponse attendue en L3-b)*
- **c)** « Quel mois a été le plus fort, et de combien par rapport au plus faible ? » *(réponse attendue en L3-c)*

**L4 — « Ce que je ne sais pas encore faire »** (1 page, à écrire **après** L1-L3, sans tricher). La liste honnête des opérations que vous avez vues faire (par un collègue, dans un forum, dans ce manuel) et que vous ne maîtrisez pas, classées en trois colonnes : *ce dont j'aurai besoin tout de suite · ce dont j'aurai besoin dans trois mois · ce qui n'est pas mon besoin*. Trois lignes minimum par catégorie.

### Contraintes de rendu

1. Les fichiers sont déposés dans une arborescence conforme à la convention du module 1 (`01_brut` en lecture seule, `02_propre`, `03_analyse`, `04_livrables`, `90_journal`).
2. Le **journal de transformation** compte au moins **8 entrées** datées, chacune avec les nombres avant/après.
3. Le livrable L1-L4 est un seul document PDF nommé `2026-09-17_projet_M01_P_votre_nom.pdf`, plus le classeur de travail.
4. **Interdits** : copier un total du corrigé sans montrer la manipulation qui y mène ; utiliser un tableau croisé dynamique ou une requête pour L3 (l'exercice porte sur le tri et le filtre) ; modifier le fichier brut.

---

## 2. Barème détaillé

| # | Critère | Pts | Ce qui fait perdre les points |
|---|---|---|---|
| 1 | Fiche d'identité : six phrases justes | 4 | grain exprimé en « c'est du mensuel » (ce n'est pas un grain) ; clé donnée comme `n_ticket` seul |
| 2 | Contrôles par colonne : **tous les comptages exacts** | 5 | un seul nombre faux = −0,5 ; un nombre non vérifié (pas de formule, pas de commande) = −1 |
| 3 | Trois questions : cinq composants, réfutabilité | 3 | adjectif non mesurable resté dans la question ; critère de réussite absent |
| 4 | Réponse chiffrée L3 : valeur exacte + méthode reproductible | 4 | chiffre juste obtenu par un moyen interdit ; ou juste mais sans méthode |
| 5 | Journal + arborescence + nommage | 2 | écart de total non expliqué ; fichier brut touché |
| 6 | L4 : lucidité de l'autoportrait | 2 | liste de vœux au lieu d'une liste d'outils/gestes précis |
| | **Total** | **20** | seuil de passage en M02 : **13** |

---

## 3. Correction pas à pas (corrigé enseignant)

Cette correction est rédigée comme un compte-rendu de travail, parce que c'est ce qui est noté. Elle s'appuie sur les valeurs réellement produites par le fichier livré ; si votre fichier diffère, régénérez (`python3 01_socle_donnees/scripts/generation_socle.py`) avant de vous comparer.

### 3.1 — Réponse L1 : la fiche d'identité, telle qu'elle doit être rendue

**Nom et source.** `ventes_magasin5_2025.csv`, export de la caisse du magasin 5 pour l'année 2025, reçu par messagerie le 17/09/2026 ; 489 lignes, 32 Ko, en-tête sur 1 ligne, séparateur point-virgule, encodage UTF-8.

**Objet.** Les articles facturés au magasin 5 sur l'année 2025.

**Grain.** Une ligne = un article d'un ticket de caisse. *Ni une vente, ni un jour, ni un client.*

**Clé.** Aucune colonne n'est unique : `n_ticket` identifie le ticket et se répète (1 à 4 lignes par ticket). L'unicité de la ligne est assurée par le couple (`n_ticket`, `produit`).

**Mesures et attributs.** Mesures : `quantite`, `prix_unitaire_ht`, `remise`, `montant_ht`, `montant_ttc`. Attributs : `date`, `heure`, `magasin`, `vendeur`, `client`, `produit`, `categorie`. Identifiants : `n_ticket`, `client`, `produit`.

**Étendue.** 489 lignes · 316 tickets distincts · 31 jours avec des ventes (l'extrait contient 40 lignes par mois, tous certains jours ne sont donc pas représentés) · 4 vendeurs · 145 produits distincts · 7 catégories · 372 identifiants clients distincts · 18 lignes sans client · période couverte 2025-01-01 → 2025-12-31.

**Tableau des contrôles** (le cœur du point 2 du barème) :

| Colonne | Type constaté | Distincts | Bornes / modalités | Défaut constaté | Comment je l'ai compté |
|---|---|---|---|---|---|
| `n_ticket` | texte | 316 | `T05-25…-…`, 17 caractères | 9 lignes en double (489 − 480) | `=SOMMEPROD(1/NB.SI(...))` ou tri + comptage manuel |
| `date` | texte | 55 | 2025-01-01 → 2025-12-31 | **65 lignes** en `JJ/MM/AAAA` | `=NB.SI(B:B;"?*/*/*")` |
| `heure` | texte | 356 | 07:01 → 18:57 | — | — |
| `magasin` | texte | 1 | « Magasin 5 — Kaya Marché » | — | — |
| `vendeur` | texte | 4 | Ilboudo, Sankara, Ouédraogo, Bationo | — | — |
| `client` | nombre **ou** vide | 372 | `0` = comptoir | **18 vides** (`=NB.EUILL`) | vides ≠ 0 : deux choses distinctes |
| `produit` | texte | 145 | « … — réf N » dans le libellé | deux infos dans une cellule | — |
| `categorie` | texte | 7 | Matériaux 146 · Quincaillerie 115 · Consommables 58 · Plomberie 57 · Electricité 54 · Peinture 34 · Bois & panneaux 25 | — | tri + comptage |
| `quantite` | nombre | 37 | -13 (retours) → **14 000** | **7 lignes > 500** | `=MAX()`, `=NB.SI(I:I;">500")` |
| `prix_unitaire_ht` | nombre | 323 | 675 → 40 550 | — | `=MIN()`, `=MAX()` |
| `remise` | nombre | 6 | 0 → 0,11 (proportion) | aucune valeur > 0,4 ici | contrôle de plage |
| `montant_ht` | nombre | 456 | total = à recalculer | cohérent avec `quantite × prix × (1 − remise)` | `=SOMME()` |
| `montant_ttc` | **texte** | 456 | — | **486 lignes non numériques** | `=NBVAL(M:M)-NB(M:M)` |

**Le point qui distingue un bon rendu d'un rendu moyen** : la ligne `quantite`. Le candidat solide écrit « 7 lignes suspectes, montant cohérent, donc doute sur l'unité de saisie → à voir avec le métier, pas à supprimer ». Le candidat pressé supprime les 7 lignes et perd 1 point au contrôle des totaux.

### 3.2 — Réponse L2 : les trois questions, avec leurs limites

**Question 1 (mix de catégories).** « En 2025, au magasin 5, quelle catégorie de produits représente la part la plus élevée du CA TTC (somme de `montant_ttc`, retours inclus avec leur signe, après retrait des doublons), et cette part dépasse-t-elle 20 % du total ? »
*Critère de réussite* : la somme des 7 catégories doit redonner le total de l'extrait nettoyé, **36 073 185 FCFA** ; la réponse est une part en pourcentage à ±0,1 pt.
*Ce que ce fichier ne permet pas de répondre* : la rentabilité de la catégorie (aucun coût d'achat dans ce fichier — il est dans `couts_achat.csv`, module 13) et la comparaison aux autres magasins (extrait limité au magasin 5).

**Question 2 (saisonnalité).** « Quel mois de 2025 présente le CA TTC le plus éloigné de la médiane des douze mois, et de combien de fois le mois le plus faible ? »
*Critère* : ratio meilleur mois / pire mois = **4,2** (décembre 5 292 517 FCFA, mai 1 258 801 FCFA).
*Limite* : l'extrait contient 40 lignes par mois, **tous les mois ne sont donc pas complets** : ce ratio décrit l'extrait, pas la réalité commerciale. Cette phrase est obligatoire dans un rendu correct ; l'omettre vaut une note plafonnée à 15/20, quel que soit le reste.

**Question 3 (qualité avant tout).** « Combien de lignes de cet extrait ne peuvent pas être sommées telles quelles, et quel est l'effet chiffré de leur correction sur le total annuel ? »
*Critère* : 486 montants en texte, 9 doublons, écart de total = **266 132 FCFA**, soit **+0,74 %** sur le total non nettoyé (36 339 317 → 36 073 185).
*Limite* : le fichier ne dit pas si les doublons viennent de la caisse ou de l'export ; seule la caisse (ou le journal d'export) tranche.

### 3.3 — Réponse L3 : la méthode par tri et filtre, et les trois résultats

**Préparation commune (autorisée : tri, filtre, `=SOMME()` sur la colonne filtrée).**

1. Import assisté, toutes colonnes en texte, puis une colonne auxiliaire `ttc_num = CBI(SUPPRESPACE(SUBSTITUE(...)))` — 486 conversions, 0 échec. *(Oui, une formule de conversion est autorisée : sans elle, aucun total n'est possible ; ce qui est interdit, c'est le TCD et la requête.)*
2. Tri sur `n_ticket` puis suppression des doublons stricts par la commande du tableur → 480 lignes. Contrôle : `=SOMME(ttc_num)` = **36 073 185**.

**L3-a (catégorie dominante).** Filtre sur `categorie` = Plomberie, `=SOMME()` sur la colonne filtrée → **8 754 982 FCFA**, soit **24,3 %** du total. Réponse : « la catégorie la plus lourde du CA 2025 du magasin 5 est la **Plomberie**, à 24,3 % ». Suit le classement complet, à exiger d'un rendu sérieux :

| Catégorie | CA TTC (extrait nettoyé) | Part |
|---|---|---|
| Plomberie | 8 754 982 FCFA | 24,3 % |
| Matériaux | 6 519 357 FCFA | 18,1 % |
| Electricité | 6 311 645 FCFA | 17,5 % |
| Bois & panneaux | 4 844 758 FCFA | 13,4 % |
| Quincaillerie | 4 203 121 FCFA | 11,7 % |
| Peinture | 2 938 358 FCFA | 8,1 % |
| Consommables | 2 500 964 FCFA | 6,9 % |
| **Total** | **36 073 185 FCFA** | 100 % |

Attention au piège classique, et il est là pour cela : le **nombre de lignes** ne suit pas le CA. La catégorie la plus fréquente en lignes est Matériaux (146 lignes), pas Plomberie (57 lignes). Un rendu qui confond fréquence et montant perd le point 4 intégralement, parce que la phrase de conclusion serait fausse.

**L3-b (vendeur en tête).** Bationo : **11 370 350 FCFA** · Sankara 9 423 281 · Ouédraogo 8 483 019 · Ilboudo 6 796 535. Somme des quatre = 36 073 185 FCFA ✔ (le contrôle croisé fait partie de la réponse attendue).

**L3-c (mois extrêmes).** Décembre 2025 = **5 292 517 FCFA** ; mai 2025 = **1 258 801 FCFA** ; ratio **4,2**. Le détail complet des douze mois figure dans le chapitre C04 §5.3 ; un candidat doit pouvoir en retrouver au moins quatre sur demande orale du correcteur.

### 3.4 — Réponse L4 : ce à quoi ressemble un autoportrait utile

Exemple de rendu recevable (extrait) :

| J'en aurai besoin tout de suite | Dans trois mois | Ce n'est pas mon besoin |
|---|---|---|
| tableaux croisés (M03-M05) | jointures SQL sur la base de l'entreprise (M07) | entraîner un modèle de prédiction (M19-M21) |
| `RECHERCHEX` pour relier les noms de produits (M06) | script Python pour rejouer le nettoyage (M08) | gestion de cluster (M24) |
| mettre un format de date fiable (déjà fait ici, à consolider M04) | publier un tableau de bord Power BI (M13-M18) | configuration d'un entrepôt (M15) |

Un autoportrait qui écrit « je veux devenir meilleur en data » est noté 0/2 : ce n'est pas une liste de besoins, c'est une intention.

### 3.5 — Le fichier du fournisseur, traité à part (bonus +1, pas obligatoire)

Le point n'est pas dans l'énoncé, mais il revient toujours en entretien de stage : **importez `tarif_fournisseur_peinture.csv` proprement** et donnez le nombre de références, le prix moyen et le prix le plus élevé. Réponse : 38 lignes utiles (42 − 3 de chapeau − 1 d'en-tête), encodage **Windows-1252**, séparateur `;`, décimale **virgule**, TVA 0,18 sur toutes les lignes. Un rendu qui écrit « le fichier est corrompu » perd le bonus ; un rendu qui écrit « il faut lire en cp1252 avec 3 lignes à ignorer » le gagne.

---

## 4. Grille d'auto-évaluation avant rendu

À cocher soi-même, honnêtement, avant d'envoyer. Sept cases manquantes = rendez-vous dans deux jours.

- [ ] Chaque nombre cité dans L1 et L3 est le résultat d'une formule ou d'une commande que je peux rejouer devant quelqu'un.
- [ ] J'ai écrit le grain en une phrase, sans le mot « mensuel ».
- [ ] J'ai distingué les 9 doublons (à retirer) des 7 quantités suspectes (à signaler).
- [ ] J'ai dit « vide ≠ 0 » pour la colonne `client`, et je l'ai justifié par la règle métier du comptoir.
- [ ] Mes trois questions L2 ont chacune cinq composants, et aucune ne contient d'adjectif non chiffré.
- [ ] Dans L2, j'ai écrit explicitement que l'extrait est un échantillon de 40 lignes par mois.
- [ ] Mon total nettoyé est 36 073 185 FCFA, et mon journal explique pourquoi le brut affichait 36 339 317 FCFA.
- [ ] Le brut est en lecture seule, et aucun de ses octets n'a changé (vérifié par empreinte).

---

## 5. Ce que le correcteur regardera en premier

Pas les chiffres — ils sont vérifiables en dix secondes. La première chose qu'un évaluateur expérimenté regarde, dans un dossier de ce niveau, est **l'ordre des opérations** : le candidat a-t-il documenté avant de corriger, ou corrigé puis justifié ? Le second regard va aux **limites écrites spontanément** (« l'extrait n'est pas la population ») : c'est le meilleur prédicteur de la capacité à travailler sans supervision. Le troisième, le nom des fichiers. Les chiffres viennent ensuite, et ils sont la partie facile.
