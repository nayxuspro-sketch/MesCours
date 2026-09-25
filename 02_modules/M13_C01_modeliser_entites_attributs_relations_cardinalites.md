# Module M13.C01 — Modéliser : entités, attributs, relations, cardinalités

**Outils : DuckDB 1.5.5 (exécuté) ; pandas (contrôle croisé, exécuté) ; le script
`03_exercices/dossier_M13/socle_m13.sql` (exécuté à chaque ouverture du socle). PostgreSQL et Power BI
(cités, non exécutés — règle §1.5). Durée indicative : 5 h. Niveau : N3 → N4. Prérequis : M06
(tables, clés, relations), M11 (SQL avancé), M12 (indicateurs et architecture).**

> **L'idée du chapitre.** Un modèle n'est pas un rangement : c'est un **plan**. Le module M12 a appris à
> choisir les indicateurs ; celui-ci apprend à construire la structure qui les rend calculables. Le
> point de départ du fil rouge tient en un fichier plat de **18 lignes** — et le défaut y est déjà
> visible : le nom du client y est recopié **278** caractères pour **92** caractères utiles, et le
> client 41 y porte déjà **2** villes différentes. À l'échelle du socle, le même défaut recopie
> **2 826 394** caractères de noms de clients là où **239 599** suffisent. Ce chapitre remplace la
> recopie par un plan : **5** entités, **7** associations, **12** clés étrangères, **12** tables.

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous savez :

1. **distinguer** les trois niveaux de lecture d'un modèle — **conceptuel** (ce que le métier décrit),
   **logique** (tables, clés, colonnes) et **physique** (le code exécuté par un moteur) — et dire
   lequel vous êtes en train d'écrire quand vous dessinez ou quand vous tapez du SQL ;
2. **nommer** les objets d'un modèle : *entité*, *attribut*, *occurrence*, *identifiant*, *relation*,
   *cardinalité*, *clé primaire*, *clé étrangère*, *clé technique*, *clé métier* ;
3. **lire une cardinalité de trois façons** — la phrase métier, la notation `0,N` / `1,N`, et la
   traduction en clés — et vérifier chacune par une mesure sur le socle, plutôt que par une intuition ;
4. **choisir entre clé technique et clé métier**, et **justifier** ce choix par un cas du fil rouge
   (la ligne de vente a les deux : `id_vente` et `id_ticket`) ;
5. **passer d'un fichier plat au modèle** et **mesurer** ce que le passage rapporte : lignes à
   modifier, caractères recopiés, et surtout le **faux total** qu'un mauvais niveau de relation
   fabrique — les ventes jointes aux commandes sur le client valent **× 0,31**, soit
   **4 804 233 057** FCFA au lieu de **15 595 154 955** FCFA.

---

## 2. Pourquoi cette notion est importante

Vous avez déjà vu ce qu'un modèle mal conçu produit comme dégâts, séparément : un chiffre d'affaires
multiplié par **15,8** pour une clé oubliée (M12.C03), une rotation divisée par douze pour une somme de
stocks (M12.C01), une vente attribuée au mauvais magasin parce que la clé qui décide ce qu'est « une
ligne » n'était pas dans la jointure (M11.C01). Ce chapitre remonte d'un cran : il ne corrige plus la
requête, il construit la **structure** qui rend la faute visible.

La scène est toujours la même. Un commercial demande « la fiche du client 41 ». On lui répond en ouvrant
le fichier de ventes : 4 lignes, deux villes — Ouagadougou pour les ventes de 2023, Bobo-Dioulasso
ensuite. Aucune des deux n'est fausse : c'est le **modèle** qui est ambigu. La ville n'est pas un
attribut de la vente, c'est un attribut du **client**, et un attribut du client rangé dans la table des
ventes n'a plus de valeur unique dès que le client déménage.

> **Définition.** Un **modèle de données** est la description, écrite et vérifiable, des objets dont
> parle une entreprise (les *entités*), de leurs caractéristiques (les *attributs*) et des liens qui
> les unissent (les *relations*) — y compris le nombre d'occurrences que chaque lien autorise (les
> *cardinalités*). « Vérifiable » est le mot qui compte : un modèle dont on ne peut pas prouver les
> affirmations n'est pas un modèle, c'est un schéma d'intention.

Le coût d'un modèle absent ne se paie pas en élégance, il se paie en heures et en chiffres faux. Sur le
socle du fil rouge, la même information — le nom du client — coûte **2 826 394** caractères quand elle
est recopiée sur chaque ligne de vente, contre **239 599** quand elle est rangée une fois par client :
**× 11,8**. Et le jour où un client change de ville, il faut modifier ses **20** lignes dans le fichier
plat, contre **1** ligne dans la dimension — en espérant ne pas en oublier une, ce qui est exactement le
défaut que ce chapitre supprime.

> **Attention.** Un fichier plat ne « marche pas » par hasard : il marche **jusqu'au premier
> changement**. Une vente ne change pas ; un client change. Tant que les clients sont stables, le
> fichier plat rend les mêmes totaux que le modèle — c'est pour cela que le défaut survit des années.
> Le modèle ne se justifie pas par les totaux d'aujourd'hui, mais par les totaux du jour où quelque
> chose bouge.

---

## 3. Explication simple — le plan et les matériaux

Pour construire une maison, on distingue trois choses : ce que le client demande (« trois chambres,
une cuisine qui donne sur la cour »), le plan de l'architecte (murs, ouvertures, cotes), et les
matériaux posés (parpaings, ciment, tôles). Personne ne confond les trois — et personne ne construit
une maison en empilant des parpaings là où ça tombe bien.

| Vous demandez | Plan | Matériaux |
|---|---|---|
| « 240 000 lignes de ventes, 23 912 clients » | le modèle : 5 entités, 7 associations, 12 clés étrangères | `socle_m13.sql` exécuté sur DuckDB |
| Entités : client, produit, magasin, vendeur, temps | la table des cardinalités | les lignes de `dim_client` |
| Le sujet d'une ligne | le grain écrit sous chaque table | `COUNT(*) = COUNT(DISTINCT clé)` |

Un modèle se dessine **deux fois** : une fois avec les mots du métier, une fois avec des clés. La
première version, tout le monde la comprend et personne ne peut l'exécuter. La seconde version,
personne ne la comprend sans effort et la machine l'exécute sans discuter. Le travail de modélisation
consiste à passer de l'une à l'autre **sans perdre d'information** — et à écrire, à chaque étape, ce
qu'on a perdu volontairement.

---

## 4. Vocabulaire essentiel

| Terme | Définition | Sur le fil rouge |
|---|---|---|
| **Entité** | Ce dont on garde la trace, au singulier, indépendamment des événements | un client, un produit, un magasin, un vendeur, un jour |
| **Occurrence** | Un exemplaire d'une entité — une ligne d'une dimension | le client 41, le magasin 6 (le dépôt) |
| **Attribut** | Une caractéristique de l'entité, qui dépend d'elle seule | la ville d'un client, la désignation d'un produit |
| **Identifiant** | L'attribut (ou la combinaison) qui désigne une occurrence et une seule | `id_client`, et pour un stock : produit × mois |
| **Relation** | Un lien entre deux entités, décrit par une phrase du métier | « un client passe plusieurs commandes » |
| **Cardinalité** | Le nombre d'occurrences autorisées de part et d'autre d'une relation | un magasin → `0,N` ventes ; une vente → `1,1` magasin |
| **MCD** | Modèle conceptuel : les entités et les relations, sans clés ni types | le dessin du §5.4 |
| **MLD** | Modèle logique : les tables, les colonnes, les clés | les 12 tables du socle |
| **MPD** | Modèle physique : le code exécuté par un moteur, avec ses types | `socle_m13.sql` sous DuckDB |
| **Clé primaire** | L'identifiant déclaré d'une table (`PRIMARY KEY`) | `dim_client(id_client)` |
| **Clé étrangère** | Une colonne qui pointe vers la clé primaire d'une autre table (`FOREIGN KEY`) | `fait_ventes.id_produit → dim_produit.id_produit` |
| **Clé technique** | Un identifiant fabriqué par le système, sans sens métier (*surrogate key*) | `id_vente` : 1 à 240 000 |
| **Clé métier** | Un identifiant venu du métier, stable pour l'utilisateur | `id_ticket` : `T01-230101-000000` |

> **Définition.** Une **clé technique** (*surrogate key*) est un nombre créé par le système, sans
> signification pour le métier, qui sert à désigner une ligne de façon stable. Une **clé métier** est
> un identifiant qui vient du métier — un numéro de ticket, un code produit — et qui peut changer,
> être reformaté, ou se répéter d'un millésime à l'autre. Un modèle sérieux porte **les deux** : la
> technique pour les jointures, la métier pour parler aux utilisateurs.

---

## 5. Cours approfondi

### 5.1 Trois niveaux de lecture : MCD, MLD, MPD

Le **modèle conceptuel** (MCD) décrit le métier : des entités, des relations, des cardinalités. Il ne
parle ni de type de donnée, ni de clé, ni de moteur. Sa qualité se juge à une question : *un
gestionnaire de Sahel Distribution reconnaît-il sa propre entreprise dans ce dessin ?*

Le **modèle logique** (MLD) descend d'un cran : chaque entité devient une table, chaque relation devient
une clé étrangère placée du côté « plusieurs », et chaque table reçoit un grain écrit. C'est le document
de travail des équipes : c'est lui qu'on relit en revue.

Le **modèle physique** (MPD) est le code : les types, les index, les contraintes, le moteur. C'est le
seul des trois qui s'exécute, et donc le seul dont la vérité se **mesure**.

> **Définition.** Une **cardinalité** décrit combien d'occurrences d'une entité peuvent être reliées à
> une occurrence de l'autre. On l'écrit par deux nombres : le minimum (`0` ou `1`) et le maximum (`1`
> ou `N`). `0,N` se lit « de zéro à plusieurs » : l'entité n'est pas obligée d'apparaître. `1,1` se lit
> « exactement une » : le lien est obligatoire et unique.

### 5.2 Entité, attribut, occurrence, identifiant

Le test qui sépare une entité d'un attribut tient en une phrase : **si l'information peut changer sans
qu'aucun autre objet ne change, elle appartient à son propre objet**. Une ville de client change sans
que la vente change : la ville est un attribut du client, pas de la vente. Une désignation de produit
change sans que la vente change : même conclusion.

Le test qui sépare deux entités d'une seule : **peut-il exister sans l'autre ?** Un vendeur existe même
les jours sans vente ; un magasin existe avant d'ouvrir. En revanche, la ligne de vente n'existe pas
sans le client, le produit, le magasin, le vendeur et le jour : ce n'est pas une entité, c'est une
**association porteuse** — ce que la suite du module appellera une **table de faits**.

> **Définition.** Une **association porteuse** (ou **table de faits**) est une relation entre plusieurs
> entités qui porte elle-même des mesures et des attributs de l'événement — la quantité vendue, le
> montant, l'heure. Sa ligne est un **événement**, pas un objet : on n'y range jamais un attribut
> d'entité, sinon le modèle recopie et fabrique le défaut du §6.

### 5.3 La cardinalité et ses trois lectures

Une même relation se lit de trois façons, et il faut savoir faire les trois :

| Lecture | Exemple sur le fil rouge | Ce qu'on en fait |
|---|---|---|
| **La phrase métier** | « un client passe zéro, une ou plusieurs commandes » | elle se discute avec le métier, pas avec un informaticien |
| **La notation** | client `1,N` commande — ou `0,N` si un client peut ne jamais commander | elle se dessine sur le MCD |
| **La traduction** | la clé `id_client` se pose dans la table `fait_commandes`, jamais dans `dim_client` | elle se code dans le MLD |

La traduction obéit à une règle unique : **la clé étrangère se pose du côté « plusieurs »**. Un magasin
a plusieurs ventes : `id_magasin` va dans les faits. Une vente a un seul magasin : on n'écrit jamais une
colonne `id_vente` dans `dim_magasin` — ce serait admettre qu'un magasin n'a qu'une vente, ou alors
impossible à remplir.

> **Définition.** L'**optionalité** est la moitié gauche d'une cardinalité : elle dit si le lien est
> obligatoire. `0,N` (facultatif côté entité pointée) et `1,N` (obligatoire) se ressemblent dans un
> schéma et ne se ressemblent pas du tout dans un contrôle : une cardinalité `1,N` fausse produit des
> **orphelins**, une cardinalité `0,N` fausse produit des **lignes inutiles**. Sur le socle,
> `fait_ventes.id_vendeur` est obligatoire, `fait_ventes.id_client` ne l'est pas — le client 0 le
> prouve.

### 5.4 Les cinq entités du fil rouge, mesurées

Le socle de Sahel Distribution fournit ses propres réponses. Aucune cardinalité de ce tableau n'est
déduite : la dernière colonne est la mesure qui l'établit, et le §7 la rejoue.

| Entité | Dimension | Occurrences | Cardinalité avec les ventes | La mesure qui l'établit |
|---|---|---|---|---|
| Client | `dim_client` | **23 912** | `0,N` | **23 496** clients achètent, **416** n'ont jamais acheté |
| Produit | `dim_produit` | **154** | `1,N` | de **873** à **2 672** lignes par produit, aucun produit à zéro |
| Magasin | `dim_magasin` | **6** | `0,N` | **5** magasins vendent, le dépôt central ne vend pas |
| Vendeur | `dim_vendeur` | **22** | `1,N` | les **22** vendeurs ont des ventes |
| Temps | `dim_date` | **1 339** | `1,N` | les **1 339** jours portent au moins une vente |

Deux lignes de ce tableau méritent la révision : le magasin à zéro vente et le client à zéro achat.
Dans les deux cas, la bonne réaction n'est pas de supprimer la ligne — c'est de **déclarer
l'optionalité**. Un dépôt qui ne vend pas reçoit des colis : il est indispensable à la table des
livraisons. Un client qui n'a pas encore acheté est un prospect : il est indispensable au suivi
commercial. Un modèle qui les supprime rend deux indicateurs impossibles à calculer.

> **Dans les faits.** L'instrument du module rejoue ces cinq cardinalités à chaque exécution
> (`tools/modele_M13.py`) et publie le verdict des quatre contrôles de recette : **14** tables sur
> **14** ont une clé unique, les **7** tables de faits portent exactement les lignes de leur source,
> **0** orphelin sur les **12** clés étrangères vérifiées, et la recette du modèle égale celle de la
> source : **15 595 154 955** FCFA.

### 5.5 Du MCD au MLD : où se pose la clé étrangère

Le passage du conceptuel au logique suit quatre gestes, toujours les mêmes :

1. **une entité → une table** : `dim_client`, `dim_produit`, `dim_magasin`, `dim_vendeur`, `dim_date` ;
2. **une association porteuse → une table de faits** : `fait_ventes`, `fait_commandes`,
   `fait_encaissements`, `fait_stock_mensuel`, `fait_ruptures`, `fait_logistique`, `fait_objectifs` ;
3. **une relation → une clé étrangère** du côté « plusieurs » : `id_produit` dans `fait_ventes`, et
   jamais `id_vente` dans `dim_produit` ;
4. **un attribut reste là où il dépend de son identifiant** : la ville dans `dim_client`, la quantité
   dans `fait_ventes`.

Le résultat sur le fil rouge : **5** dimensions, **7** tables de faits, **12** tables au total, et
**12** clés étrangères. Ce dernier nombre n'est pas un détail de comptage : c'est la liste des contrôles
d'intégrité que le §7.5 exécute.

### 5.6 Clé technique, clé métier : deux clés, deux rôles

La ligne de vente du fil rouge porte les deux, et c'est volontaire :

- `id_vente`, entier de **1** à **240 000** : la **clé technique**. Elle sert aux jointures, elle est
  courte, stable, et personne au métier ne la connaît ;
- `id_ticket`, texte du type `T01-230101-000000` : la **clé métier**. Elle porte du sens — le magasin
  (T01), la date (230101), un compteur — et c'est celle que le service client cite au téléphone.

> **Attention.** La clé métier n'est pas une clé primaire fiable pour autant. `T01-230101-000000`
> contient la **date** : une facture antidatée, un ticket corrigé, et le numéro ne correspond plus à
> rien. Pire, un magasin qui change de code rend les anciens numéros ambigus. La règle du module : **la
> clé métier peut être unique, elle n'est jamais la clé de jointure** ; les **240 000** lignes de vente
> se joignent par `id_vente`, et les **146 161** tickets se regroupent par `id_ticket`.

Un ticket n'est pas une ligne : **146 161** tickets portent **240 000** lignes, soit **1,64** ligne par
ticket (de **1** à **4**). Confondre les deux donne un panier moyen faux d'un facteur 1,64 — le genre
d'erreur que M12 avait déjà chiffrée sur les paniers par jour.

### 5.7 Le MPD : exécuter le modèle et vérifier le total

Le modèle physique du module est écrit dans `03_exercices/dossier_M13/socle_m13.sql` : **12** tables,
**5** dimensions, **7** tables de faits, plus **2** dimensions historisées que le chapitre C04
construira. Le fichier s'exécute à chaque ouverture du socle, et il finit par le contrôle qui compte le
plus :

```sql
-- la recette : le chiffre d'affaires du modèle doit être IDENTIQUE à celui de la source
SELECT ROUND(SUM(montant_ttc))                       AS ca_modele FROM fait_ventes WHERE est_retour = 0;
SELECT ROUND(SUM(TRY_CAST(montant_ttc AS DOUBLE)))   AS ca_source FROM ventes     WHERE est_retour = 0;
```

Ici, les deux nombres sont égaux : **15 595 154 955** FCFA. Ce n'est pas une coquetterie : un modèle
qui ne rend pas le même total que sa source a déplacé ou perdu des lignes, et tout ce qui suit
(indicateurs, tableaux de bord, décisions) hérite de l'erreur.

> **Conseil professionnel.** Ne présentez jamais un modèle sans son contrôle de recette. Une revue de
> modèle qui commence par « combien de tables ? » et non par « combien de chiffre d'affaires ? » finit
> toujours par discuter de style. Le total, lui, ne discute pas.

### 5.8 Ce que ce chapitre ne couvre pas

La normalisation des référentiels est le sujet du chapitre C02 ; le grain et l'additivité sont celui
de C03 ; le schéma en étoile et les changements lents, celui de C04 ; le flocon et les variantes, C05 ;
le temps et le calendrier, C06 ; la qualité, la documentation et la revue, C07. La traduction du modèle
en relations d'un outil de restitution (Power BI) appartient au module M14 : elle est **citée** ici une
fois, jamais exécutée — règle §1.5.

---

## 6. Exemple concret — la fiche client recopiée

Le dossier du module contient un extrait volontairement plat : `03_exercices/dossier_M13/table_plate.csv`.
Ce n'est pas un mauvais fichier, c'est un fichier **d'avant le modèle** : une ligne par vente, tous les
attributs recopiés.

| Ce qu'on y trouve | Mesure |
|---|---|
| Lignes | **18** |
| Clients distincts | **6** |
| Libellés de catégorie distincts | **11** — pour **7** familles réelles (M12) |
| Caractères de noms de clients recopiés | **278** pour **92** caractères utiles |
| Nom le plus répété | « SARL Faso Batiment », **4** fois sur **18** lignes |
| Villes portées par le client 41 | **2** (Ouagadougou, puis Bobo-Dioulasso) |

Deux défauts cohabitent dans ce petit fichier, et ils sont de nature différente :

1. **la redondance** — le nom du client est recopié **4** fois pour « SARL Faso Batiment ». Ce n'est
   pas faux, c'est coûteux : sur le socle complet, la même recopie pèse **2 826 394** caractères contre
   **239 599** rangés une fois (**× 11,8**) ;
2. **l'ambiguïté** — le client 41 a **2** villes. Ici, la question n'est plus le coût mais le **sens** :
   « la ville du client 41 » n'a pas de réponse unique dans ce fichier. Une question simple devient
   indécidable.

Le modèle répond aux deux par un seul geste : une table `dim_client` de **8** colonnes, une ligne par
client, et une clé `id_client` posée dans les **240 000** lignes de ventes. La redondance disparaît par
construction ; l'ambiguïté disparaît parce que la ville n'appartient plus qu'à un seul endroit — et si
elle doit changer dans le temps, c'est le chapitre C04 qui s'en charge, avec une période de validité.

> **À retenir.** Un attribut rangé au mauvais endroit ne provoque pas une erreur : il provoque une
> **question sans réponse**. C'est pour cela qu'un modèle se juge sur les questions qu'il rend
> possibles, pas sur les totaux qu'il rend justes.

---

## 7. Démonstration pas à pas — six étapes sur le socle

Toutes les requêtes de cette section s'exécutent sur le socle du module, ouvert ainsi :

```python
import sys
CHEMIN = '03_exercices/dossier_M13'
sys.path.insert(0, CHEMIN)
from connexion import ouvrir
con = ouvrir()          # rejoue M11, puis M12, puis le modèle M13
```

### 7.1 Étape 1 — compter les occurrences avant de dessiner

Une cardinalité se mesure, jamais ne se devine. On commence donc par compter les occurrences des cinq
entités et la façon dont elles se relient aux ventes :

```sql
SELECT (SELECT COUNT(*) FROM dim_client)  AS clients,
       (SELECT COUNT(*) FROM dim_produit) AS produits,
       (SELECT COUNT(*) FROM dim_magasin) AS magasins,
       (SELECT COUNT(*) FROM dim_vendeur) AS vendeurs,
       (SELECT COUNT(*) FROM dim_date)    AS jours;
```

Résultat : **23 913**, **154**, **6**, **22**, **1 339**. Le premier nombre vaut **23 912** clients
du référentiel **plus** la ligne « client non identifié » — une ligne qui n'existe pas dans le
référentiel et que le modèle ajoute exprès (voir l'étape 5).

### 7.2 Étape 2 — prouver l'identifiant

Un identifiant n'est un identifiant que s'il est **unique**. La preuve tient en une ligne, et elle doit
être exécutée sur chaque table :

```sql
-- le grain de chaque table est PROUVÉ, pas supposé
SELECT COUNT(*) AS lignes, COUNT(DISTINCT id_vente) AS cles FROM fait_ventes;
```

**240 000** et **240 000**. Le même contrôle passe sur les **14** tables du modèle : **14** clés
uniques, y compris les deux tables de faits dont le grain est une **combinaison** — le stock (produit ×
mois) et les ruptures (produit × magasin × mois).

### 7.3 Étape 3 — mesurer le coût d'une modification

Combien de lignes faut-il modifier pour changer la ville d'un client ? Dans le fichier plat : toutes ses
ventes. Dans le modèle : une seule ligne.

```sql
-- dans le fichier plat : 4 lignes pour un client de l'extrait
SELECT COUNT(*) FROM read_csv_auto('03_exercices/dossier_M13/table_plate.csv',
                                   header = true, delim = ',') WHERE id_client = 41;

-- dans le modèle : une ligne, et une seule
SELECT COUNT(*) FROM dim_client WHERE id_client = 41;
```

**4** contre **1** sur l'extrait ; **20** contre **1** pour le client le plus actif du socle. Le rapport
n'est pas le sujet : ce qui compte est qu'à **240 000** lignes, la version plate demande une mise à jour
par ligne, et que l'oubli d'une seule ligne recrée le défaut du §6.

### 7.4 Étape 4 — lire la relation au bon niveau

Voici l'erreur que ce chapitre existe pour empêcher. Deux tables parlent du client : `fait_ventes`
(240 000 lignes) et `fait_commandes` (9 000 lignes). Les joindre *par le client* semble naturel :

```sql
-- FAUX : deux tables jointes sur le client, donc au niveau « plusieurs à plusieurs »
SELECT ROUND(SUM(v.montant_ttc)) FROM fait_ventes v
JOIN fait_commandes c ON c.id_client = v.id_client
WHERE v.est_retour = 0;      -- 4 804 233 057 FCFA
```

Le chiffre d'affaires tombe à **4 804 233 057** FCFA, soit **× 0,31**. La requête s'exécute, ne lève
aucune erreur, et le total obtenu a l'air crédible : c'est le pire des cas. La même faute avec les
encaissements donne **4 797 608 252** FCFA, également **× 0,31**.

La cause est une question de modèle, pas de SQL : les deux tables n'ont pas le même sujet de ligne.
Réunir deux grains différents dans une seule jointure oblige le moteur à choisir un appariement — et le
seul appariement disponible (le client) multiplie ou filtre. La correction n'est pas dans la requête,
elle est dans le modèle : **on ne joint pas deux faits ; on les agrège séparément, puis on rapproche
leurs résultats par la dimension commune**, ce que le module M12 faisait déjà pour comparer ventes et
objectifs.

> **Attention.** Un total faux par mauvais niveau de relation est **plus dangereux** qu'un total faux
> par erreur de saisie : il est stable, reproductible, et il se défend en réunion. **4 804 233 057**
> FCFA ne ressemble pas à une faute de frappe — il ressemble à un chiffre.

### 7.5 Étape 5 — écrire le MLD : les douze clés étrangères

Le modèle logique se vérifie en énumérant ses clés étrangères, puis en les testant. Les **12** du
socle, avec le contrôle d'orphelins qui va avec :

| Table de faits | Clé étrangère | Pointe vers | Orphelins |
|---|---|---|---|
| `fait_ventes` | `id_produit`, `id_client`, `id_magasin`, `id_vendeur` | produit, client, magasin, vendeur | **0** |
| `fait_commandes` | `id_client`, `id_magasin` | client, magasin | **0** |
| `fait_encaissements` | `id_client` | client | **0** |
| `fait_stock_mensuel` | `id_produit` | produit | **0** |
| `fait_ruptures` | `id_produit`, `id_magasin` | produit, magasin | **0** |
| `fait_logistique` | `id_magasin` | magasin | **0** |
| `fait_objectifs` | `id_magasin` | magasin | **0** |

Une seule ligne du référentiel ne suffisait pas : le client **0** apparaît dans **43 161** lignes de
vente — **2 852 612 447** FCFA — et n'existe pas dans `dim_client`. Deux solutions sont défendables, et
le module en a choisi une :

- **refuser le chargement** : la clé étrangère proteste, l'ingénieur corrige le référentiel ;
- **créer la ligne « inconnue »** : le modèle accepte le fait et le **déclare** — c'est le choix retenu,
  parce que supprimer **43 161** ventes réelles fausserait tous les totaux de **2 852 612 447** FCFA.

### 7.6 Étape 6 — exécuter le MPD et contrôler le total

Dernier geste : exécuter le modèle et comparer à la source. `tools/modele_M13.py` le fait en quatre
contrôles, dans l'ordre où un modèle se vérifie — **unicité** (le grain), **grain** (les tables de
faits portent les lignes de leur source), **orphelins** (les clés étrangères), **totaux** (la recette) :

```
1. unicite   : 14 tables sur 14 ont une cle unique
2. grain     : 7 tables de faits sur 7 portent exactement les lignes de leur source
3. orphelins : 12 cles etrangeres verifiees, 0 orphelin
4. totaux    : 15 595 154 955 FCFA par le modele, 15 595 154 955 FCFA par la source — identiques
```

Un modèle qui passe ces quatre contrôles n'est pas pour autant un bon modèle : il est **juste**. La
qualité — lisibilité, documentation, usage des utilisateurs — se juge au chapitre C07.

---

## 8. Erreurs fréquentes

| Erreur | Ce qu'elle produit | La parade |
|---|---|---|
| Ranger un attribut d'entité dans la table de faits | **2** villes pour un client, une question sans réponse | un attribut n'existe qu'à un seul endroit |
| Poser la clé étrangère du côté « un » | une colonne impossible à remplir, ou un `1,1` faux | la clé se pose du côté « plusieurs » |
| Joindre deux tables de faits au niveau d'une dimension | **× 0,31** de chiffre d'affaires (**4 804 233 057** FCFA) | agréger séparément, rapprocher ensuite |
| Croire qu'une clé métier est une clé primaire | des doublons le jour d'une correction ou d'un antidatage | clé technique pour joindre, clé métier pour parler |
| Confondre ticket et ligne de vente | un panier moyen faux de **× 1,64** | écrire le grain sous chaque table |
| Supprimer une dimension à zéro occurrence | un dépôt sans vente, **416** clients sans achat | déclarer l'optionalité (`0,N`) |

---

## 9. Bonnes pratiques professionnelles

- **Écrivez le grain sous chaque table**, dans le fichier lui-même, au-dessus du `CREATE` : un grain
  écrit se relit, un grain supposé se discute.
- **Vérifiez l'unicité par une requête**, pas par confiance : `COUNT(*) = COUNT(DISTINCT clé)` sur
  chaque table, à chaque chargement.
- **Déclarez la ligne inconnue** quand le référentiel est incomplet : une clé étrangère qui ne pointe
  nulle part est une décision, et une décision non écrite est un défaut.
- **Comptez les clés étrangères** de votre modèle et testez chacune : **12** ici, **0** orphelin — le
  jour où l'une d'elles casse, le contrôle le dit avant l'utilisateur.
- **Terminez par la recette** : le total du modèle contre le total de la source, à l'unité près.

> **Conseil professionnel.** En revue de modèle, la première question n'est pas « combien de tables ? »
> mais **« qu'est-ce qu'une ligne ? »**, posée table par table. Un modèle dont les grains sont écrits
> se relit en vingt minutes ; un modèle sans grains produit trois réunions.

> **À retenir.** Un modèle de données est une **décision écrite**. Chaque clé étrangère est une
> décision (« ce fait appartient forcément à ce magasin »), chaque ligne inconnue en est une autre
> (« nous acceptons des faits non identifiés »). Ce qui n'est pas écrit sera décidé par accident — et
> l'accident, ici, porte un nom : **4 804 233 057** FCFA.

---

## 10. Exercice guidé

**Sujet.** Le service commercial veut une table des clients livrés par magasin : combien de clients
distincts chaque magasin a servis, et combien de lignes de vente il a enregistrées. Objectif : écrire la
requête **au bon niveau**, puis montrer ce que produirait la version fautive.

**Étape 1 — compter les lignes et les clients séparément, par magasin.**

```sql
SELECT id_magasin,
       COUNT(*)                     AS lignes_de_vente,
       COUNT(DISTINCT id_client)    AS clients_servis
FROM fait_ventes
GROUP BY id_magasin
ORDER BY lignes_de_vente DESC;
```

Deux mesures de nature différente cohabitent dans le même `SELECT`, et c'est légitime : `lignes_de_vente`
s'additionne d'un magasin à l'autre, `clients_servis` ne s'additionne pas (un client peut acheter dans
deux magasins). Le magasin 1 sert **81 769** lignes, le magasin 5 en sert **26 496**.

**Étape 2 — vérifier l'additivité avant de publier un total.** Additionnez les `clients_servis` des
cinq magasins : **90 679**, contre **23 496** clients réels. Le total dépasse le réel de près de quatre
fois, parce qu'un client achète dans plusieurs magasins. C'est la démonstration, vue en M12.C03, que ce
total ne se publie pas : il se **recalcule** par un `COUNT(DISTINCT)` général.

**Étape 3 — écrire la version fautive et l'expliquer.** Joindre les ventes aux clients (`dim_client`)
puis aux commandes multiplie les lignes : le `COUNT(*)` n'a plus aucun sens, et un `SUM(montant_ttc)`
tombé à **× 0,31** non plus. La règle à écrire dans le rapport : **une requête qui change le nombre de
lignes doit être annoncée et justifiée.**

---

## 11. Exercices autonomes

**Exercice 1.1.** Écrivez la phrase métier des **5** cardinalités du §5.4 en français, sans symbole, et
vérifiez chacune par une requête sur le socle. Une des cinq comporte un `0` qui n'est pas une erreur :
laquelle, et pourquoi faut-il la garder ?

**Exercice 1.2.** Le client 41 de `03_exercices/dossier_M13/table_plate.csv` porte **2** villes.
Écrivez la requête qui montre l'ambiguïté, puis celle qui, sur le modèle, répond sans ambiguïté. Que
faudrait-il de plus pour répondre à la question « quelle était sa ville le 14 février 2023 » ?

**Exercice 1.3.** Choisissez trois tables du modèle et écrivez, pour chacune, la requête qui prouve son
grain. Deux d'entre elles ont un grain composé : nommez-les et dites ce qui se passerait si l'on
omettait une des deux colonnes de la clé.

**Exercice 1.4.** Un stagiaire propose de supprimer `dim_magasin` et d'écrire directement le nom du
magasin dans `fait_ventes` : « cela évite une jointure ». Rédigez une réponse de dix lignes qui
chiffre le coût de cette décision (lignes à modifier, cas du dépôt, cas du magasin qui change de
responsable) et concluez.

---

## 12. Correction détaillée

**Exercice 1.1.** 1) « un client peut passer zéro, une ou plusieurs ventes » — **23 496** clients
achètent, **416** n'achètent pas : `0,N`. 2) « un produit du catalogue peut être vendu une ou plusieurs
fois » — de **873** à **2 672** lignes, aucun produit à zéro : `1,N` (la cardinalité est obligatoire
**parce que** le catalogue ne contient que des produits vivants ; si le catalogue admettait un article
jamais vendu, elle deviendrait `0,N`). 3) « un magasin peut vendre zéro, une ou plusieurs fois » — le
dépôt central ne vend pas : `0,N`. 4) « un vendeur vend une ou plusieurs fois » — les **22** vendeurs
ont des ventes : `1,N`. 5) « un jour du calendrier porte une ou plusieurs ventes » — les **1 339** jours
en portent au moins une : `1,N`. Le `0` à conserver est celui du **magasin** : le dépôt reçoit des
colis, donc il appartient au modèle — le supprimer rendrait la table logistique incomplète.

**Exercice 1.2.** L'ambiguïté se montre en comptant les villes distinctes par client :

```sql
SELECT id_client, COUNT(DISTINCT ville_client) AS villes
FROM read_csv_auto('03_exercices/dossier_M13/table_plate.csv', header = true, delim = ',')
GROUP BY id_client HAVING COUNT(DISTINCT ville_client) > 1;
```

Le modèle répond sans ambiguïté parce que la ville n'est écrite qu'une fois :
`SELECT ville FROM dim_client WHERE id_client = 41` donne **une** ligne. Pour répondre « au 14 février
2023 », il faut plus que le modèle de ce chapitre : il faut une **période de validité** sur l'attribut
— c'est exactement la dimension historisée de type 2 du chapitre C04 (**24 892** versions client).

**Exercice 1.3.** `dim_client` : `COUNT(*) = COUNT(DISTINCT id_client)` — **23 913** lignes, **23 913**
clés. `dim_date` : la clé est la date elle-même, **1 339** = **1 339**. Les deux grains composés sont
`fait_stock_mensuel` (**produit × mois**) et `fait_ruptures` (**produit × magasin × mois**). Omettre
`mois` dans le premier ferait de la clé un produit : **154** clés pour **6 776** lignes, donc **6 776**
lignes pour un même produit — le grain serait faux et la somme des stocks par produit multiplierait le
résultat.

**Exercice 1.4.** Réponse attendue : écrire le nom du magasin dans les faits recopie **1** valeur sur
**240 000** lignes ; corriger un nom demande **240 000** modifications, une par ligne ; le dépôt central
(**1** magasin sur **6**) n'a aucune vente, il disparaîtrait donc du modèle — et avec lui la table
logistique de M12 (**264** lignes) ; et un magasin qui change de responsable changerait d'identité ou
garderait l'ancienne selon les lignes. Conclusion : la jointure économisée coûte **240 000** recopies
pour économiser une jointure sur une table de **6** lignes. La bonne réponse n'est pas « c'est plus
lent », c'est « c'est indécidable ».

---

## 13. Mini-projet de chapitre

**« Le MCD des cinq entités, mesuré »** (2 h). Produisez, pour le fil rouge : (1) le **MCD** des
**5** entités et de leurs associations, avec les cardinalités écrites en clair ; (2) le **MLD** en
tableaux, chaque table portant son grain écrit au-dessus ; (3) la **liste des 12 clés étrangères** avec,
pour chacune, la requête d'orphelins correspondante ; (4) la **phrase métier** de chaque cardinalité,
relue à voix haute. Livrable : deux pages et les requêtes exécutées. Ce travail est directement la
matière de P1 du projet de module.

---

## 14. Résumé du chapitre

| Notion | Ce qu'il faut retenir |
|---|---|
| Trois niveaux | MCD (le métier), MLD (les clés), MPD (le code exécuté) |
| Entités du fil rouge | client **23 912**, produit **154**, magasin **6**, vendeur **22**, temps **1 339** |
| Cardinalités | `0,N` client ( **416** sans achat), `0,N` magasin (le dépôt), `1,N` produit et vendeur |
| Associations | **7** tables de faits, **5** dimensions, **12** clés étrangères |
| Clés | technique pour joindre ( `id_vente` ), métier pour parler ( `id_ticket` ) |
| Ticket contre ligne | **146 161** tickets, **240 000** lignes, **1,64** ligne par ticket |
| Redondance | **2 826 394** caractères recopiés contre **239 599** rangés une fois (**× 11,8**) |
| Mauvais niveau | ventes × commandes sur le client : **× 0,31**, soit **4 804 233 057** FCFA |
| Recette | **15 595 154 955** FCFA, modèle = source |

## 15. À retenir

> **À retenir.** Modéliser, c'est décider **ce qu'est une ligne** — et l'écrire. Les trois niveaux
> (conceptuel, logique, physique) ne sont pas trois documents à produire : ce sont trois façons de
> relire le même objet, pour trois publics différents.

- **Une cardinalité se mesure** : **416** clients sans achat, **1** dépôt sans vente, **22** vendeurs
  actifs — ces trois nombres sont écrits dans le modèle, pas observés après coup.
- **La clé étrangère se pose du côté « plusieurs »** ; l'inverse produit des colonnes impossibles à
  remplir.
- **Deux tables de faits ne se joignent pas** : elles s'agrègent séparément — **× 0,31** et
  **4 804 233 057** FCFA sont le prix de l'oubli.
- **La ligne inconnue est une décision** : **43 161** ventes non identifiées (**2 852 612 447** FCFA)
  restent dans les totaux parce que le modèle a choisi de les déclarer.
- **Tout modèle se termine par une recette** : **15 595 154 955** FCFA des deux côtés, ou le modèle
  n'est pas prêt.

## 16. Évaluation formative

1. Donnez la définition d'une **entité**, d'un **attribut** et d'une **association porteuse**, avec un
   exemple du fil rouge pour chacune.
2. Quelle est la différence entre le MCD, le MLD et le MPD ? Lequel s'exécute ?
3. Écrivez la cardinalité client → ventes en notation, puis en phrase métier, puis en clés.
4. Pourquoi la clé étrangère ne se pose-t-elle jamais du côté « un » ?
5. Combien de clients du socle n'ont jamais acheté, et que fait-on de leur ligne ?
6. Quelle est la différence entre `id_vente` et `id_ticket` ? Laquelle utilise-t-on pour joindre, et
   pourquoi ?
7. **146 161** tickets pour **240 000** lignes : qu'est-ce que cela change pour un panier moyen ?
8. Joindre ventes et commandes sur le client donne **4 804 233 057** FCFA. Expliquez la cause et
   proposez la correction.
9. Pourquoi le nom de client est-il recopié **11,8** fois dans le fichier plat, et que coûte cette
   recopie ?
10. Quels sont les quatre contrôles de recette du modèle, et que vérifie chacun ?

**Corrigé :** 1. Entité : le client ; attribut : sa ville ; association porteuse : la ligne de vente, qui
porte la quantité et le montant. 2. Le conceptuel décrit le métier, le logique les tables et les clés,
le physique le code ; seul le **physique** s'exécute. 3. `0,N` ; « un client peut passer zéro, une ou
plusieurs ventes » ; `id_client` se pose dans `fait_ventes`. 4. Parce qu'elle obligerait à écrire une
ligne unique dans la table « un » pour chaque ligne de la table « plusieurs » : impossible à remplir.
5. **416** ; on garde leur ligne, sinon la relation devient obligatoire et les prospects disparaissent
du suivi. 6. `id_vente` est technique ( **1** à **240 000** ), `id_ticket` est métier
( `T01-230101-000000` ) ; on joint par la technique, parce que la métier porte une date et peut devenir
ambiguë. 7. Il ne faut pas compter les tickets comme des lignes : **1,64** ligne par ticket, donc un
panier calculé sur les lignes est faux d'un facteur **1,64**. 8. Les deux tables n'ont pas le même
sujet de ligne ; la jointure se fait au niveau du client et multiplie ou filtre : on agrège séparément,
puis on rapproche par la dimension commune. 9. Parce que la ville du client n'est pas un attribut de la
vente ; la recopie coûte **2 826 394** caractères contre **239 599**, et le jour du déménagement elle
coûte une mise à jour par ligne. 10. Unicité (le grain), grain (les lignes de la source), orphelins (les
**12** clés étrangères) et totaux (la recette de **15 595 154 955** FCFA).
