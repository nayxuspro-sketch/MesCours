# Projet M13.P — « Le modèle de Sahel Distribution »

**Module : M13 — Modélisation des données · 4 livrables · 20 points · seuil de réussite 13 · environ
10 h de travail.**

**Le mandat.** Sahel Distribution publie ses chiffres depuis un fichier plat de **240 000** lignes qui
porte tout : la vente, le client, le produit, le magasin et le vendeur dans la même ligne. Trois
rapports de la même semaine affichent trois chiffres d'affaires différents (**22 305 610 960**,
**29 474 916 530** et **15 595 154 955** FCFA), et personne ne sait lequel est le bon. La direction
vous mandate pour **construire le modèle** qui remplace ce fichier. Sa consigne, textuelle : « un
modèle, pas un fichier ; une table par sujet ; des clés déclarées ; et la preuve que le total est le
même qu'avant. »

**Le modèle attendu** compte **7** dimensions et **7** faits, **127** colonnes, **1 339** jours de
calendrier, et sa recette doit tomber au franc près sur **15 595 154 955** FCFA.

---

## 1. Énoncé

### Le matériel fourni

| Pièce | Contenu |
|---|---|
| `ventes_propres.csv` | le fichier plat : **240 000** lignes, **11** colonnes, **26,8** Mo |
| `brut/clients.csv` `brut/produits.csv` `brut/magasins.csv` `brut/vendeurs.csv` | les quatre référentiels, tels qu'ils sortent du système de caisse (**2** prix manquants, des libellés écrits de plusieurs façons) |
| `brut/objectifs_de_ca.csv` | **218** lignes d'objectifs, au grain magasin et mois, séparateur point-virgule |
| `dim_date.csv` | **1 339** jours de calendrier, du 2023-01-01 au 2026-08-31 |
| `mouvements_clients.csv` | **1 120** mouvements de clients, à ranger en changements lents |
| `tarifs_produits.csv` | **616** versions de tarifs, à ranger de la même façon |
| `socle_m13.sql` et `connexion.py` | la base de travail et son ouverture, identiques à ceux des chapitres |
| `ATTENDU.json` | les mesures de référence, pour vérifier vos calculs |

### Les huit totaux de contrôle

Aucun livrable ne peut passer un total faux. Ces huit valeurs sont votre recette ; elles se
recalculent sur le modèle que vous construisez.

| Contrôle | Valeur attendue |
|---|---|
| chiffre d'affaires net | **15 595 154 955** FCFA |
| chiffre d'affaires toutes lignes | **15 419 985 157** FCFA |
| lignes de vente | **240 000**, dont **237 191** hors retours et **2 809** retours |
| dimensions | clients **23 913** · produits **154** · magasins **6** · vendeurs **22** · jours **1 339** |
| faits | ventes **240 000** · commandes **9 000** · encaissements **9 000** · objectifs **218** · logistique **264** · ruptures **2 428** · stock mensuel **6 776** |
| enjeu de la recette | le modèle doit rendre le **même** total que le fichier plat |
| contrôles de recette | **4** (unicité, grain, orphelins, total), tous au vert |
| versions historisées | **24 893** versions de clients et **616** versions de produits |

---

## 2. Les quatre livrables

### P1 — Le modèle conceptuel et le modèle logique (6 points)

| Attendu | Détail |
|---|---|
| Modèle conceptuel | les **5** entités du fil rouge (client, produit, magasin, vendeur, temps) avec leurs attributs et leurs **cardinalités** écrites, y compris le plusieurs à plusieurs entre tickets et produits |
| Modèle logique | les **7** dimensions et les **7** faits, chaque table portant sa **clé** et son **grain écrit sous le nom de la table** |
| Cardinalités justifiées | pour chaque relation : un à plusieurs, plusieurs à plusieurs, ou aucun, avec l'exemple du socle qui le prouve |
| Grain des faits | écrit en une phrase par fait, sans le mot « détail » : par exemple « une ligne de ticket » |

**Ce qui est éliminatoire.** Un fait dont le grain n'est pas écrit, ou une relation plusieurs à
plusieurs dessinée sans passer par une table.

### P2 — Le script de création exécutable (6 points)

| Attendu | Détail |
|---|---|
| Script rejouable | `CREATE TABLE` puis les chargements, exécutés deux fois de suite sans erreur et sans doublon |
| Clés | clés primaires et étrangères déclarées, ou bien contrôlées explicitement si votre moteur ne les impose pas |
| Contraintes d'intégrité | ce qui doit être refusé est refusé : un identifiant en double, une clé sans référentiel |
| Les 4 contrôles | unicité des clés, égalité des grains, absence d'orphelins, recette — exécutés et rendus avec leur sortie |
| Preuve | le rapport d'exécution joint : les **4** contrôles au vert, et le total du modèle affiché |

**Le test que nous appliquerons.** Votre script sera relancé sur une base vide, puis les **4**
contrôles seront exécutés sans que vous soyez là. Un modèle qui ne se reconstruit pas ne se corrige
pas.

### P3 — La revue du modèle en 15 points (5 points)

| Attendu | Détail |
|---|---|
| La grille remplie | les **15** points du chapitre C07, chacun avec sa **preuve** : une requête, un compte ou un nom |
| Les défauts trouvés | la liste des défauts restants dans votre propre modèle, chiffrés, et la décision prise pour chacun (corrigé, assumé, reporté) |
| Les exceptions déclarées | ce que le modèle ne sait pas dire, écrit noir sur blanc : l'absence d'heure dans le fait de ventes, le client non identifié, les jours fériés travaillés |
| La signature | la revue est datée, et vous dites quel point vous n'avez pas pu vérifier |

**Rappel de méthode.** Les points **6** à **10** de la grille ne se voient pas à l'exécution : ils
demandent de compter, de comparer et de nommer. Un point sans preuve s'écrit « non revu », jamais
« conforme ».

### P4 — La note de choix (3 pages, 3 points)

| Attendu | Détail |
|---|---|
| Étoile ou flocon | la variante retenue pour la hiérarchie produit, et la mesure qui tranche |
| Type de changement lent | le type retenu pour les clients et pour les tarifs, et ce que le type 3 aurait coûté |
| Dénormalisations assumées | ce que vous avez recopié exprès, combien de fois, et ce que vous y gagnez |
| Refus argumentés | ce que vous avez **refusé** de faire, et pourquoi : deux calendriers, un objectif sur la ligne de vente, un montant dans une table de pont |
| Le goût du socle | une phrase sur ce que vous changeriez si la direction acceptait un jour de casser le modèle |

**Budget.** Trois pages, pas quatre. Une note de choix qui dépasse son format est une note qui n'a
pas choisi.

---

## 3. Le barème

| Livrable | Points |
|---|---|
| **P1** — modèle conceptuel et modèle logique | **6** |
| **P2** — script exécutable et **4** contrôles | **6** |
| **P3** — revue en **15** points | **5** |
| **P4** — note de choix, **3** pages | **3** |
| **Total** | **20** |

Le seuil de réussite est fixé à **13** points sur **20**. Les **4** points d'écart entre le barème et
le seuil sont votre marge : vous pouvez perdre un livrable entier et réussir le projet, à condition
que le modèle se reconstruise et que la recette tombe juste.

---

## 4. Ce qui fait rejeter un livrable

1. **Le modèle ne se reconstruit pas** : le script exécuté deux fois donne deux fois plus de lignes.
2. **La recette ne tombe pas juste** : le total du modèle diffère de celui du fichier plat, quel que
   soit l'écart.
3. **Un fait n'a pas de grain écrit**, ou son grain est faux.
4. **Une table additionne deux grains** : un objectif posé sur la ligne de vente, un montant recopié
   dans une table de pont.
5. **Une clé étrangère n'a pas de référentiel** et aucune ligne inconnue ne la rattrape.
6. **La revue est signée « conforme » sans preuve** : chaque point de la grille demande un chiffre ou
   un nom.
7. **Une historisation dont les jointures oublient la date** : lire l'attribut d'aujourd'hui sur une
   vente d'avant-hier.
8. **La note de choix décrit le modèle au lieu de le justifier** : nous voulons les décisions, pas le
   sommaire.

---

## 5. Déroulé conseillé (4 séances, environ 10 h)

| Séance | Durée | Travail | Livrable visé |
|---|---|---|---|
| 1 | 2 h | lecture du fichier plat, relevé des **8** totaux de contrôle, entités, cardinalités | P1, modèle conceptuel |
| 2 | 3 h | modèle logique, grains écrits, clés, chargements des **7** dimensions | P1 et P2 |
| 3 | 3 h | les **7** faits, les **4** contrôles, la recette, la reconstruction | P2 |
| 4 | 2 h | la grille des **15** points sur son propre modèle, puis la note de choix | P3 et P4 |

---

## 6. Comment vous corriger vous-même

1. **Les huit totaux** du §1 tombent juste, sur votre modèle et non sur le fichier plat.
2. **Chaque grain est écrit** en une phrase, sous le nom de chaque table de faits.
3. **Les 4 contrôles sont exécutés** et vous pouvez montrer leur sortie, pas seulement leur code.
4. **Chaque point de la grille porte une preuve** : un point sans preuve se note « non revu ».
5. **Les défauts restants sont chiffrés** et la décision est écrite, y compris la décision de ne pas
   corriger.
6. **La note de choix tient en 3 pages** et chaque décision porte une mesure ou un refus argumenté.
7. **Le modèle se reconstruit à l'identique** deux fois de suite, sans intervention de votre part.

**Le test final.** Donnez votre modèle et vos **4** contrôles à quelqu'un qui ne connaît pas le
dossier, en lui demandant de refaire la recette. S'il y arrive sans vous poser de question, le projet
est réussi : vous avez livré un modèle possédable, et non un fichier explicable.
