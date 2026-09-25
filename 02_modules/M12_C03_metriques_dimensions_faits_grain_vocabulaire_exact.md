# Module M12.C03 — Métriques, dimensions, faits, grain : le vocabulaire exact

**Outils : DuckDB 1.5.5 (exécuté), pandas (contrôle croisé, exécuté), Excel (exécuté). Power BI
(cité, non exécuté — règle §1.5). Durée indicative : 5 h. Niveau : N3. Prérequis : M12.C01—C02,
M07 (tables et jointures), M11.C01 (grain d'une requête).**

> **L'idée du chapitre.** Presque tous les débats de chiffres en réunion sont des malentendus de
> **vocabulaire** : on ne parle pas du même grain, du même dénominateur, ou de la même mesure. Ce
> chapitre installe les mots exacts — métrique, dimension, fait, grain, additivité — et les éprouve
> par huit tables du socle, où **tout** se mesure : un chiffre d'affaires qui s'additionne
> parfaitement (**15 595 154 955** FCFA), un comptage de clients qui ne s'additionne **pas**
> (**188 886** au lieu de **23 497**), une moyenne de moyennes qui se trompe de **445** FCFA, et une
> clé oubliée qui multiplie un total par **15,8** sans lever la moindre erreur.

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous savez :

1. **nommer** les quatre objets du vocabulaire — **fait**, **dimension**, **métrique**, **grain** — et
   dire lequel est en cause quand deux personnes obtiennent deux chiffres ;
2. **déterminer le grain** d'une table ou d'un résultat : « que représente **une** ligne ? » — et
   vérifier la réponse par une clé distincte, pas par une impression ;
3. **classer une mesure** en additive, semi-additive ou non additive, et prévoir ce qui se passera si
   on l'additionne quand même ;
4. **distinguer** métrique, indicateur et indicateur clé, puis ranger les indicateurs par **horizon de
   décision** (opérationnel, tactique, stratégique) — trois horizons, trois fréquences, trois publics ;
5. **détecter** les trois pièges mécaniques qui fabriquent de faux totaux : la moyenne de moyennes, le
   comptage distinct additionné, et la jointure à clé incomplète.

---

## 2. Pourquoi cette notion est importante

Vous avez déjà rencontré chacun de ces pièges, séparément : le cumul qui double (**77 975 774 775**
FCFA pour une jointure sans la clé du magasin, M11.C01), la rotation divisée par douze quand on somme
des stocks (M12.C01), le classement instable faute de clé de départage (M11.C02). Ce chapitre les
réunit sous un seul vocabulaire, parce que la cause est toujours la même : **on n'a pas dit de quoi
on parlait**.

En réunion, cela donne une scène qui se répète : le contrôleur de gestion annonce **23 497** clients,
le responsable marketing en annonce **188 886**, et les deux ont raison. Le premier compte des
**clients distincts** ; le second a additionné le nombre de clients de chaque produit, ce qui compte
**un client autant de fois qu'il a de produits**. Le mot manquant n'est pas « client », c'est
**additivité**.

> **À retenir.** Deux chiffres qui diffèrent ne sont pas forcément contradictoires : ils peuvent
> simplement ne pas mesurer la même chose. Le vocabulaire de ce chapitre sert à le **dire avant** la
> réunion, et non à le découvrir pendant.

---

## 3. Explication simple — les briques et le ciment

Un jeu de données bien construit ressemble à un mur de briques. Les **faits** sont les briques : des
événements qui se sont produits — une ligne de vente, une commande, une facture encaissée. Les
**dimensions** sont le ciment et les plans de coupe : le temps, le magasin, le client, le produit,
le canal — les axes selon lesquels on regarde les briques.

Un mur se décrit de trois façons, et confondre les trois fait s'écrouler le devis :

- **combien de briques** — un **comptage**. Il s'additionne tant qu'on ne compte pas deux fois la même
  brique.
- **combien pèse le mur** — un **montant**. Il s'additionne toujours, et c'est ce qui autorise les
  sous-totaux.
- **combien de briques en moyenne par rangée** — une **moyenne**. Elle ne s'additionne jamais, et
  c'est précisément là que les réunions dérapent.

Le **grain**, enfin, répond à une question qu'on oublie de poser : *une brique, c'est quoi ?* Une
ligne de vente ? Un ticket ? Une journée ? Tant que la réponse n'est pas écrite, tout ce qui suit est
une hypothèse.

---

## 4. Vocabulaire essentiel

> **Définition.** Un **fait** est un événement mesurable et daté — une vente, une commande, une
> rupture, un encaissement. Dans une table de faits, chaque ligne enregistre **un** événement à **un**
> niveau de détail donné.

> **Définition.** Une **dimension** est un axe d'analyse stable, par lequel on découpe les faits :
> temps, magasin, client, produit, canal, mode de paiement. Une dimension se décrit par sa
> **cardinalité** — son nombre de valeurs distinctes (`magasin` en a **5**, `produit` en a **154**).

> **Définition.** Une **métrique** est une quantité mesurée sur les faits : un montant, une quantité,
> une durée, un effectif. Une **mesure** est la valeur d'une métrique à un grain donné ; un
> **indicateur** est une mesure **choisie** pour suivre une performance (C01).

> **Définition.** Le **grain** d'une table ou d'un résultat est ce que représente **une ligne** :
> une ligne de vente, un ticket, un couple produit-mois, une commande, une journée. Le grain se
> **prouve** par une clé dont le nombre de valeurs distinctes égale le nombre de lignes.

> **Définition.** Une mesure est **additive** quand elle peut être additionnée sur toutes les
> dimensions (les montants), **semi-additive** quand elle s'additionne sur certaines seulement
> (un stock, qui s'additionne dans l'espace mais pas dans le temps), et **non additive** quand elle ne
> s'additionne nulle part (un taux, une moyenne, un comptage d'éléments distincts).

---

## 5. Cours approfondi

### 5.1 La table de faits et la table de dimensions

Le socle de M12 contient huit tables, et le vocabulaire les sépare sans ambiguïté :

| Table | Nature | Ce que représente une ligne |
|---|---|---|
| `ventes` | **faits** | une ligne de vente (ou de retour) |
| `commande` | **faits** | une commande client |
| `encaissement` | **faits** | une facture et son encaissement |
| `rupture` | **faits** | un épisode de rupture, pour un produit, un magasin, un mois |
| `logistique` | **faits** | le coût logistique d'un magasin sur un mois |
| `produit` | **dimension** | un article du catalogue |
| `magasin` | **dimension** | un point de vente ou le dépôt |
| `calendrier` | **dimension** | un jour, avec ses attributs |

> **Attention.** Une table peut être **les deux** selon l'usage : `stock_mensuel` est un **fait**
> (un relevé de stock par produit et par mois) mais se lit comme une **dimension** du produit quand on
> s'en sert pour filtrer. Le vocabulaire ne décrit pas les fichiers, il décrit **ce qu'on en fait** —
> et c'est pour cela qu'il doit être écrit dans le rapport, pas supposé.

### 5.2 Le grain : la question posée huit fois

La même question — « que représente une ligne ? » — posée aux huit tables du socle, avec la preuve par
la clé :

| Table | Lignes | Clés distinctes | Grain prouvé | Unique ? |
|---|---|---|---|---|
| `ventes` | **240 000** | **240 000** | ligne de vente | oui |
| `commande` | **9 000** | **9 000** | commande | oui |
| `encaissement` | **9 000** | **9 000** | facture | oui |
| `stock_mensuel` | **6 776** | **6 776** | produit × mois | oui |
| `rupture` | **2 428** | **2 428** | produit × magasin × mois | oui |
| `logistique` | **264** | **264** | magasin × mois | oui |
| `produit` | **154** | **154** | produit | oui |
| `magasin` | **6** | **6** | magasin | oui |

**8** tables, **8** clés uniques : le socle est propre, et le grain de chacune est **démontré** par le
fait que le nombre de clés distinctes égale le nombre de lignes. C'est le premier contrôle à faire sur
n'importe quel fichier qu'on vous transmet — avant de compter quoi que ce soit, demandez-vous **quelle
colonne est unique**, et vérifiez-le.

Quand aucune colonne n'est unique, le grain est une **combinaison** : c'est le cas de `rupture`
(produit + magasin + mois) et de `stock_mensuel` (produit + mois). Deux tables, deux grains différents
— et c'est cette différence qui explique le piège du §5.7.

### 5.3 Les dimensions du socle et leur cardinalité

| Dimension | Valeurs distinctes | Ce qui la rend utile — ou piégeuse |
|---|---|---|
| `magasin` | **5** | peu de valeurs : les tableaux croisés restent lisibles |
| `ville` | **4** | moins de villes que de magasins : deux magasins partagent Ouagadougou |
| `quartier` | **5** | même cardinalité que `magasin`, mais ce n'est pas la même dimension |
| `vendeur` | **22** | trop de valeurs pour un tableau croisé complet |
| `mode_paiement` | **5** | — |
| `canal` | **3** | **15** couples canal × mode : toutes les combinaisons existent |
| `produit` | **154** | à croiser par famille, jamais en clair |
| `categorie` (libellé brut) | **16** | **16** libellés pour **7** familles réelles : la dimension est **sale** |
| `sous_categorie` | **12** | niveau intermédiaire, utile pour ne pas croiser 154 produits |
| `client` | **23 497** | une dimension à part entière : elle porte le RFM (M11.C04) |
| `mois` | **44** | la dimension temps, au grain du suivi |
| `jour` | **1 339** | le grain le plus fin disponible |

Deux leçons de vocabulaire dans ce tableau :

1. **Une dimension doit être propre.** Les **16** libellés de catégorie pour **7** familles réelles
   (M11.C05) sont un défaut de dimension : tant qu'il n'est pas corrigé, tout croisement par catégorie
   est faux — non pas par erreur de requête, mais par **défaut de référentiel**.
2. **La cardinalité décide de la forme du tableau.** **5** magasins se croisent à l'écran ; **154**
   produits se regroupent d'abord par famille ; **23 497** clients ne se croisent jamais en clair.

### 5.4 Additif, semi-additif, non additif

Trois familles, et pour chacune une mesure du socle qui **prouve** la règle :

| Famille | Exemple | Le test | Résultat mesuré |
|---|---|---|---|
| **Additive** | chiffre d'affaires | somme par magasin = total ? | **15 595 154 955** FCFA des deux côtés : oui |
| **Additive** | effectif de lignes | somme par magasin = total ? | **240 000** des deux côtés : oui |
| **Semi-additive** | stock en unités | dernier mois contre somme des 44 mois | **45 882** contre **2 034 733** (**× 44,30**) |
| **Non additive** | clients distincts | somme par produit contre total | **188 886** contre **23 497** (**× 8,04**) |
| **Non additive** | clients distincts | somme par magasin contre total | **90 242** contre **23 497** (**× 3,84**) |
| **Non additive** | panier moyen | moyenne des moyennes contre vraie moyenne | **107 840** contre **107 396** FCFA |

**L'additivité n'est pas une propriété du chiffre, c'est une propriété du couple chiffre-dimension.**
Le comptage de ruptures s'additionne par magasin (**2 428** des deux côtés) parce qu'une rupture
appartient à un seul magasin ; le comptage de clients ne s'additionne pas par produit, parce qu'un
client achète **8,04** produits en moyenne. La différence entre les deux cas n'est pas la mesure :
c'est la **dimension**.

> **Attention.** Un tableau croisé peut être juste ligne par ligne et faux en bas à droite. Additionner
> la colonne « clients » d'un croisement par produit donne **188 886** : le total général du tableau
> est alors **huit fois** le nombre réel de clients. La règle : **le total d'une colonne non additive se
> recalcule, il ne s'additionne pas.**

### 5.5 Le piège de la moyenne de moyennes, chiffré

Le tableau du §5.3 se lit ligne à ligne. Le panier moyen par magasin vaut :

| Magasin | Panier moyen par ticket |
|---|---|
| Kaya | **111 447** FCFA |
| Koudougou | **108 035** FCFA |
| Ouaga 2000 | **107 374** FCFA |
| Gounghin | **106 621** FCFA |
| Bobo Kibidwé | **105 724** FCFA |

La moyenne de ces cinq valeurs vaut **107 840** FCFA. La **vraie** moyenne du panier, calculée sur
l'ensemble des tickets, vaut **107 396** FCFA. Écart : **445** FCFA, soit **0,4 %**.

L'écart est faible ici — parce que les cinq magasins ont des volumes comparables. Mais la **méthode**
est fausse : une moyenne de moyennes ne pondère pas. Si Kaya réalisait 90 % des tickets, la même
méthode produirait un écart de plusieurs milliers de francs. La règle est donc absolue, quelle que
soit la taille de l'erreur observée : **on recalcule la moyenne sur les lignes, on ne moyenne pas des
moyennes**.

### 5.6 Métrique, indicateur, indicateur clé — et les trois horizons

Le vocabulaire se range enfin par **public** :

| Niveau | Question | Fréquence | Exemple mesuré | Public |
|---|---|---|---|---|
| **Opérationnel** | « que se passe-t-il aujourd'hui ? » | jour, heure | **26 933 751** FCFA le 17/03/2026 contre **11 646 867** FCFA en moyenne (**× 2,31**) | chef de rayon, responsable logistique |
| **Tactique** | « où en sommes-nous ce mois ? » | semaine, mois | mois record **2026-03** (**533 572 353** FCFA) | directeur commercial |
| **Stratégique** | « où allons-nous ? » | trimestre, année | **3 443 581 547** FCFA en 2023 → **3 360 553 372** FCFA sur 8 mois de 2026 | direction générale, associés |

Trois remarques qui font la différence entre un tableau de bord et un catalogue :

1. **Un indicateur opérationnel doit être actionnable dans l'heure.** Le chiffre du 17/03/2026
   (**× 2,31**) sert à comprendre *sur le moment* ; publié au trimestre, il ne sert à rien.
2. **Un indicateur tactique compare à une cible**, jamais à lui-même : le mois record ne dit rien sans
   l'objectif du mois.
3. **Un indicateur stratégique accepte une incertitude.** L'exercice 2026 est **partiel** (**8** mois
   sur **12**) : l'annoncer fait partie de l'indicateur, et non de sa légende.

**Métrique, indicateur, indicateur clé** s'emboîtent : la métrique est la quantité (un montant), le
**KPI** est la métrique choisie pour une décision, et l'**indicateur clé** est celui qu'on suit
jusqu'au bout — avec un seuil et une action (C04). Une entreprise a des dizaines de métriques, une
poignée de KPI, et **trois ou quatre** indicateurs clés.

### 5.7 La clé oubliée : le piège qui fabrique un total

Voici la démonstration la plus coûteuse du chapitre. On joint les ventes aux ruptures, en oubliant la
clé du mois :

```sql
SELECT COUNT(*), ROUND(SUM(v.montant_ttc))
FROM ventes v
JOIN rupture r ON r.id_produit = v.id_produit
WHERE v.est_retour = 0;
```

Résultat : **3 808 099** lignes (**× 15,9**) et **246 567 448 121** FCFA (**× 15,8**).

La requête **s'exécute**, ne lève **aucune erreur**, et produit un chiffre d'affaires **quinze fois**
trop élevé. Chaque ligne de vente a été répétée autant de fois que son produit compte de lignes de
rupture. Le grain des deux tables n'était pas le même — `ventes` est au grain *ligne de vente*,
`rupture` au grain *produit × magasin × mois* — et la jointure, faite sur **une seule** des trois clés
du second grain, a **multiplié** au lieu de **filtrer**.

Le contrôle qui rattrape ce genre d'erreur tient en une ligne et devrait être systématique :

```
nombre de lignes AVANT la jointure == nombre de lignes APRÈS ?
```

S'il a changé, la jointure a **dupliqué** : ce n'est pas forcément faux (un fan-out voulu existe), mais
c'est **toujours** une décision à écrire.

### 5.8 Ce que ce chapitre ne couvre pas

La **fabrication** d'un indicateur — six critères, carte de définition, contre-KPI, effets pervers —
est le chapitre C04 ; l'**architecture** technique (couche sémantique, entrepôt, modèle physique) est le
C05 ; la **modélisation en étoile** proprement dite — tables de faits, tables de dimensions, clés
substituts — appartient à M13. Ce chapitre-ci s'arrête au vocabulaire et à ses pièges : il nomme les
objets et prouve leur comportement sur huit tables.

---

## 6. Exemple concret — le tableau croisé qui se réconcilie

La cellule commerciale demande « le chiffre d'affaires et le nombre de clients par magasin ». Le
tableau se construit en une requête, et se **réconcilie** en trois contrôles.

| Magasin | CA net (FCFA) | Clients distincts | Panier moyen |
|---|---|---|---|
| Ouaga 2000 | **5 312 205 459** | à calculer | **107 374** |
| Kaya Marché | **1 733 230 083** | à calculer | **111 447** |

Les trois contrôles de réconciliation :

1. **Somme des lignes = total** pour le chiffre d'affaires : **15 595 154 955** FCFA des deux côtés —
   l'additivité est vérifiée, le tableau peut porter un total.
2. **Somme des lignes ≠ total** pour les clients : la colonne ne portera **pas** de total, mais un
   renvoi vers le chiffre global (**23 497** clients pour l'enseigne, un client pouvant acheter dans
   plusieurs magasins).
3. **Le panier moyen ne s'additionne pas** : il se recalcule (**107 396** FCFA), et le tableau
   l'indique en note plutôt que d'afficher une moyenne de moyennes à **107 840** FCFA.

**La leçon.** Un tableau de bord professionnel ne se juge pas à ce qu'il affiche mais à ce qu'il
**refuse** d'afficher : un total sur une colonne non additive est une erreur qui se propage à toutes les
décisions prises dessus.

> **Dans les faits.** L'atelier du module passe ce contrôle tout seul : la table des grains
> (**8** tables, **8** clés uniques), l'additivité du chiffre d'affaires, la non-additivité des clients
> et l'écart de la moyenne de moyennes sont recalculés à chaque relevé par `tools/kpi_M12.py`. Un
> chiffre de vocabulaire qui n'est pas mesuré n'est pas une règle : c'est une opinion sur une règle.

---

## 7. Démonstration pas à pas — six étapes sur le socle

### 7.1 Étape 1 — prouver le grain avant de compter

```sql
SELECT COUNT(*) AS lignes, COUNT(DISTINCT id_vente) AS cles FROM ventes;
```

**240 000** et **240 000** : le grain est **une ligne de vente**, et il est prouvé. Refaites le test
sur les huit tables du socle : **8** sur **8** ont une clé unique. Sur un fichier reçu, c'est le
premier contrôle à passer — et le seul qui évite de compter deux fois.

### 7.2 Étape 2 — mesurer une dimension avant de la croiser

```sql
SELECT COUNT(DISTINCT categorie) AS libelles, COUNT(DISTINCT sous_categorie) AS sous_categories
FROM produit;
```

**16** libellés pour **12** sous-catégories — et, après repliement des écritures, **7** familles
réelles (M11.C05). La dimension est **sale** : croiser dessus sans la nettoyer produit des classements
faux. Le nombre de valeurs distinctes est l'indicateur de propreté d'une dimension.

### 7.3 Étape 3 — vérifier l'additivité par la somme

```sql
SELECT ROUND(SUM(montant_ttc)) FROM ventes WHERE est_retour = 0;
```

**15 595 154 955** FCFA — égal à la somme des cinq magasins. Le tableau croisé peut porter un total
général : la mesure est additive.

### 7.4 Étape 4 — constater la non-additivité d'un comptage distinct

```sql
SELECT SUM(n) FROM (SELECT COUNT(DISTINCT id_client) AS n FROM ventes
                    WHERE est_retour = 0 GROUP BY id_produit) t;
```

**188 886** — pour **23 497** clients réels. Un client achète en moyenne **8,04** produits : la somme
des comptages le compte huit fois. **Aucun total ne sera publié sur cette colonne.**

### 7.5 Étape 5 — refuser la moyenne de moyennes

Moyenne des cinq paniers moyens : **107 840** FCFA. Vraie moyenne sur les tickets : **107 396** FCFA.
Écart **445** FCFA (**0,4 %**) — faible, mais de **méthode** fausse : la règle s'applique
indépendamment de la taille de l'écart observé.

### 7.6 Étape 6 — le contrôle qui rattrape la clé oubliée

```sql
-- avant la jointure
SELECT COUNT(*) FROM ventes;                        -- 240 000
-- après la jointure sur le produit seul
SELECT COUNT(*) FROM ventes v JOIN rupture r ON r.id_produit = v.id_produit;   -- 3 808 099
```

Le nombre de lignes a changé : la jointure a **multiplié**. Le contrôle avant/après est le réflexe
minimum de toute jointure sur un socle qu'on ne connaît pas par cœur.

---

## 8. Erreurs fréquentes

1. **Ne pas écrire le grain.** Un rapport sans grain est un rapport qu'on ne peut pas auditer.
2. **Additionner des comptages distincts.** **188 886** au lieu de **23 497**.
3. **Moyenner des moyennes.** **107 840** au lieu de **107 396** — la méthode est fausse même quand
   l'écart est petit.
4. **Sommer un stock dans le temps.** **2 034 733** unités au lieu de **45 882** (**× 44,30**).
5. **Sommer un taux.** Un taux de rupture par magasin ne s'additionne pas ; il se **recalcule** sur les
   effectifs.
6. **Joindre sans vérifier la clé complète.** **× 15,8** de chiffre d'affaires, sans erreur de moteur.
7. **Croiser une dimension sale.** **16** libellés pour **7** familles : le classement change.
8. **Confondre métrique et indicateur clé** : des dizaines de métriques, **3** ou **4** indicateurs
   clés, pas **41**.
9. **Publier un indicateur opérationnel au rythme stratégique.** Le record du 17/03/2026 n'a de sens
   que le jour même.
10. **Mélanger les horizons** dans un même écran : trois publics, trois fréquences, trois lectures.

---

## 9. Bonnes pratiques professionnelles

- **Écrire le grain en tête de chaque rapport** : « une ligne = un ticket », « une ligne = un couple
  magasin-mois ».
- **Prouver le grain par une clé**, jamais par une intuition : `COUNT(*) = COUNT(DISTINCT clé)`.
- **Marquer chaque mesure** dans la carte de définition (C04) : additive, semi-additive ou non
  additive — c'est ce qui décide si le tableau porte un total.
- **Contrôler le nombre de lignes avant et après chaque jointure.**
- **Recalculer les taux et les moyennes** sur les lignes, jamais sur des agrégats.

> **Conseil professionnel.** Quand deux chiffres s'opposent en réunion, ne cherchez pas qui a tort :
> demandez **le grain** et **l'additivité**. Dans l'immense majorité des cas, les deux chiffres sont
> justes et les deux personnes parlent de deux choses différentes — **23 497** clients et **188 886**
> lignes de clientèle ne se contredisent pas, ils ne mesurent pas la même chose.

---

## 10. Exercice guidé

**Énoncé.** Le responsable marketing publie ce tableau et demande : « pourquoi notre base clients
fond-elle ? ».

| Produit | Clients |
|---|---|
| Ciment CPJ45 50 kg | 4 812 |
| Peinture acrylique 20 l | 3 907 |
| Tôle bac alu 6 m | 3 651 |
| **Total affiché** | **12 370** |

**Étape 1 — identifier le problème.** Le total affiché est la somme d'une colonne de **clients
distincts** : la mesure n'est pas additive. Additionner des comptages distincts compte plusieurs fois
le même client.

**Étape 2 — corriger.** Recalculer le total sur l'ensemble : `SELECT COUNT(DISTINCT id_client)` donne
**23 497** clients pour l'enseigne — bien **plus** que la somme affichée, puisque les trois produits ne
couvrent qu'une partie du catalogue.

**Étape 3 — expliquer.** L'écart ne raconte aucune fuite : il raconte qu'un client achète
**8,04** produits en moyenne, et que la somme des lignes dépasse donc largement le nombre de têtes.

**Étape 4 — écrire la règle.** Dans le rapport : « clients **uniques** par produit ; le total n'est pas
la somme des lignes (un client peut acheter plusieurs produits) ». C'est cette phrase, et non le
tableau, qui empêche la mauvaise conclusion.

---

## 11. Exercices autonomes

1. **Le grain des huit tables.** Reproduisez le tableau du §5.2 : pour chaque table, le nombre de
   lignes, la clé testée, et la conclusion. Combien de tables ont une clé unique ?
2. **Cardinalités.** Listez les **12** dimensions du §5.3 avec leur cardinalité, puis dites lesquelles
   sont croisables telles quelles dans un tableau lisible.
3. **Additivité.** Prenez cinq mesures du socle (CA, quantité, tickets, clients, stock) et remplissez
   pour chacune le test d'additivité sur trois dimensions (magasin, mois, produit).
4. **La moyenne de moyennes.** Calculez le panier moyen par canal, puis la moyenne de ces trois
   valeurs, puis la vraie moyenne : mesurez l'écart et expliquez sa cause.
5. **La clé oubliée.** Joignez `ventes` et `stock_mensuel` sur le produit seul, puis sur produit et
   mois ; comparez les deux comptages de lignes et les deux totaux.
6. **Les trois horizons.** Pour un même sujet (les ruptures), proposez un indicateur opérationnel, un
   tactique et un stratégique, avec leur fréquence et leur public.

---

## 12. Correction détaillée

**Exercice 1.** **8** tables sur **8** ont une clé unique (voir le tableau du §5.2) : `ventes` par
`id_vente`, `commande` par `id_commande`, `encaissement` par `id_facture`, `stock_mensuel` par
produit × mois, `rupture` par produit × magasin × mois, `logistique` par magasin × mois, `produit` par
`id_produit`, `magasin` par `id_magasin`.

**Exercice 2.** Croisables telles quelles : `magasin` (**5**), `ville` (**4**), `quartier` (**5**),
`canal` (**3**), `mode_paiement` (**5**), `mois` (**44**). À regrouper d'abord : `produit` (**154**,
par famille), `sous_categorie` (**12**), `vendeur` (**22**). À ne jamais croiser en clair :
`client` (**23 497**), `jour` (**1 339**).

**Exercice 3.** Additives : CA, quantité, effectifs de lignes. Non additives : clients distincts,
tickets distincts (additifs ou non selon la dimension), panier moyen, taux. Semi-additive : le stock
(additif dans l'espace, jamais dans le temps).

**Exercice 4.** Trois canaux (Magasin, Livraison, Téléphone) : moyenne de leurs paniers contre la vraie
moyenne. L'écart est ici faible parce que les volumes sont proches ; il grandirait si un canal portait
la majorité des tickets. C'est la **pondération** qui manque à la moyenne de moyennes.

**Exercice 5.** Sur le produit seul : **3,8** millions de lignes (fan-out), total multiplié. Sur
produit **et** mois : les lignes ne sont conservées que lorsqu'un stock existe pour ce mois — le
comptage change à nouveau, sans erreur. Les deux versions ont un sens différent, et seule la seconde
répond à la question posée.

**Exercice 6.** Opérationnel : nombre de références en rupture aujourd'hui, fréquence quotidienne,
public : chef de rayon. Tactique : taux de rupture du mois par famille, fréquence mensuelle, public :
directeur commercial. Stratégique : **13 129** jours de rupture cumulés par an et coût **estimé**
(**169 386 812** FCFA), fréquence annuelle, public : direction, pour arbitrer le budget de stock.

---

## 13. Mini-projet de chapitre

**« La fiche de vocabulaire d'un jeu de données »** (2 h). Choisissez un jeu de données (le vôtre, ou
le socle M12) et produisez une page qui contient : (1) la table des grains, prouvée par une clé ;
(2) la liste des dimensions avec leur cardinalité ; (3) la liste des mesures avec leur additivité ;
(4) les **3** jointures possibles du jeu et le contrôle de lignes avant/après pour chacune ;
(5) une phrase de règle par mesure non additive. Ce document est la moitié de la carte de définition du
chapitre C04 : il en fournit les colonnes « source » et « granularité ».

---

## 14. Résumé du chapitre

| Notion | Ce qu'il faut retenir |
|---|---|
| Fait / dimension | l'événement daté contre l'axe stable ; **8** tables, **12** dimensions sur le socle |
| Grain | ce que représente une ligne — **prouvé** par une clé : **8** clés uniques sur **8** tables |
| Cardinalité | **5** magasins, **154** produits, **16** libellés pour **7** familles, **23 497** clients |
| Additif | CA **15 595 154 955** FCFA : somme des lignes = total |
| Semi-additif | stock : **45 882** unités contre **2 034 733** si on somme les **44** mois |
| Non additif | clients : **188 886** (produit) contre **23 497** réels ; panier : **107 840** contre **107 396** |
| Clé oubliée | **× 15,8** de CA (**246 567 448 121** FCFA) sans aucune erreur du moteur |
| Horizons | opérationnel (jour, **26 933 751** le 17/03/2026), tactique (mois, **533 572 353** en 2026-03), stratégique (année) |

## 15. À retenir

> **À retenir.** Le vocabulaire n'est pas un ornement de cours : c'est l'outil qui empêche deux personnes
> justes de se contredire. **Grain** et **additivité** règlent la majorité des désaccords de chiffres —
> et se prouvent chacun par une requête d'une ligne.

- **Le grain se prouve** : `COUNT(*)` = `COUNT(DISTINCT clé)` — **8** tables sur **8** sur ce socle.
- **L'additivité est une propriété du couple mesure-dimension**, pas du chiffre : compter des clients
  par produit ne s'additionne pas, compter des ruptures par magasin s'additionne.
- **Une dimension sale fait échouer un croisement juste** : **16** libellés pour **7** familles.
- **Toute jointure change le nombre de lignes ? C'est une décision**, pas un détail : écrivez-la.

## 16. Évaluation formative

1. Qu'est-ce qu'un fait ? Qu'est-ce qu'une dimension ? Donnez un exemple de chacun sur le socle.
2. Quelles sont les deux tables du socle dont le grain est une **combinaison** de colonnes ?
3. Comment **prouve**-t-on le grain d'une table, en une requête ?
4. Classez ces mesures : chiffre d'affaires, clients distincts, stock, panier moyen.
5. Que vaut la somme des clients par produit, et pourquoi ne publie-t-on pas ce total ?
6. Quel est l'écart entre la moyenne des paniers moyens et la vraie moyenne ? Est-il grave ?
7. Pourquoi le comptage des ruptures par magasin s'additionne-t-il, contrairement aux clients ?
8. Que se passe-t-il quand on joint `ventes` et `rupture` sur le produit seul ?
9. Citez un indicateur opérationnel, un tactique et un stratégique du socle, avec leur fréquence.
10. Combien de métriques, de KPI et d'indicateurs clés une entreprise doit-elle avoir, en ordre de
    grandeur ?

**Corrigé :** 1. Fait : une ligne de vente ; dimension : un magasin. 2. `stock_mensuel` (produit ×
mois) et `rupture` (produit × magasin × mois). 3. `COUNT(*) = COUNT(DISTINCT clé)`. 4. Additive,
non additive, semi-additive, non additive. 5. **188 886** ; parce qu'un client achète **8,04** produits
et serait compté plusieurs fois. 6. **445** FCFA (**0,4 %**) : faible ici, mais la **méthode** est
fausse — la moyenne de moyennes ne pondère pas. 7. Parce qu'une rupture appartient à **un seul**
magasin : la dimension partitionne l'ensemble. 8. Les lignes sont multipliées (**3 808 099**, × **15,9**)
et le chiffre d'affaires avec elles (**× 15,8**), sans erreur de moteur. 9. Opérationnel : CA du jour
(**26 933 751** FCFA le 17/03/2026) ; tactique : CA du mois (**533 572 353** FCFA en 2026-03) ;
stratégique : CA annuel. 10. Des dizaines de métriques, une poignée de KPI, **3** ou **4** indicateurs
clés — pas **41**.
