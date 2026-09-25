# Module M13.C02 — Normaliser : 1FN, 2FN, 3FN et les quatre anomalies

**Outils : DuckDB 1.5.5 (exécuté) ; pandas (contrôle croisé, exécuté). PostgreSQL et Power BI (cités,
non exécutés — règle §1.5). Durée indicative : 5 h. Niveau : N4. Prérequis : M13.C01 (entités, clés,
cardinalités), M04 (qualité des données), M12.C03 (grain et additivité).**

> **L'idée du chapitre.** Normaliser, c'est retirer d'une table ce qui ne dépend pas de sa clé — et le
> mesurer. Le chapitre ne raisonne pas sur des exemples de manuel : il compare la **même** information
> rangée de deux façons sur le fil rouge. Dans la table plate, le référentiel écrit la même famille de
> produits de **4** façons, si bien que le classement par étiquette brute place la famille la plus
> lourde du réseau en **5e** position — **3 492 592 638** FCFA cachés derrière quatre écritures. Dans le
> modèle, la même requête prend **2** ms au lieu de **4** : normaliser, ici, ne coûte pas une
> milliseconde de lecture. Ce qu'elle coûte, c'est l'écriture et la discipline — et ce chapitre les
> chiffre.

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous savez :

1. **énoncer** les trois premières formes normales sans les réciter : la 1FN interdit les valeurs
   multiples dans un champ, la 2FN interdit qu'un attribut ne dépende que d'une **partie** d'une clé
   composée, la 3FN interdit qu'un attribut dépende d'un autre attribut non clé ;
2. **détecter** une dépendance fonctionnelle dans une table donnée, et l'écrire sous la forme
   `déterminant → dépendant` — c'est le seul outil dont vous avez besoin pour normaliser ;
3. **reconnaître et nommer les quatre anomalies** qu'une table plate fait naître : redondance,
   mise à jour, insertion, suppression — et **mesurer** chacune sur le fil rouge ;
4. **corriger** une table non normalisée sur le socle, en créant la table de correspondance quand la
   donnée source est sale (**16** étiquettes pour **7** familles) plutôt qu'en corrigeant la requête ;
5. **décider quand ne pas normaliser**, et l'assumer par écrit : la dénormalisation volontaire d'une
   dimension de restitution est un choix, la redondance subie est un défaut.

---

## 2. Pourquoi cette notion est importante

Le chapitre C01 a montré qu'un attribut rangé au mauvais endroit rend une question indécidable. Celui-ci
montre ce qui se passe **à l'échelle** : la même faute, répétée sur des milliers de lignes, ne rend plus
seulement les questions indécidables — elle rend les **classements** faux.

Voici ce que le socle du fil rouge produit, mesuré aujourd'hui. Une requête sur la table plate — la
table qui porte les étiquettes de catégorie telles qu'elles sont écrites dans le référentiel — classe
les catégories dans cet ordre : Plomberie **3 418 137 911** FCFA, Electricité **2 469 701 472** FCFA,
Bois & panneaux **1 727 101 681** FCFA. Trois lignes, un classement net, un tableau de bord prêt à
publier. Et ce classement est **faux** : la première famille du réseau, matériaux, n'y figure pas,
parce que son montant est éclaté entre quatre étiquettes — `materiaux`, `Matériaux ` (avec une espace
finale), `Materiaux`, `MATÉRIAUX` — soit **3 492 592 638** FCFA au total.

> **Définition.** Une **dépendance fonctionnelle** `A → B` se lit : « si je connais A, je connais B sans
> regarder le reste de la ligne ». `id_client → nom_client` signifie qu'un identifiant de client
> détermine un nom, quel que soit le reste. Toute la normalisation tient dans une phrase : **un
> attribut ne doit dépendre que de la clé** — ni d'une partie de la clé (2FN), ni d'un autre attribut
> non clé (3FN).

Une table non normalisée ne produit pas d'erreur : elle produit des totaux plausibles et faux. C'est
pourquoi la normalisation n'est pas un exercice d'école, mais le premier contrôle de qualité d'un
système de restitution. Un chiffre éclaté en quatre, additionné sans faire exprès, passe tous les
contrôles techniques — et se fait démolir en réunion par la première personne qui additionne à la main.

> **Attention.** La normalisation n'a jamais pour but d'« économiser de la place ». Sur le fil rouge,
> la table plate recopie les noms de clients pour **2 826 394** caractères là où la dimension en range
> **239 599** — mais l'argument sérieux n'est pas là. L'argument est que la version plate rend le
> classement du paragraphe précédent faux. **La place est un symptôme ; la justesse est le sujet.**

---

## 3. Explication simple — le vestiaire et les étiquettes

Imaginez un vestiaire où chaque veste porte sa propre étiquette : le nom du propriétaire, sa taille,
sa ville. Deux vestes du même propriétaire, et le nom est écrit deux fois. Le manteau change de
propriétaire : il faut découdre l'étiquette et la recoudre — et si vous en oubliez une, la même
personne devient deux personnes.

Le modèle fait l'inverse : une fiche par personne (**la dimension**), un numéro cousu sur chaque veste
(**la clé étrangère**). Changer de propriétaire demande de modifier **une** fiche ; connaître le
propriétaire d'une veste demande une recherche par numéro — la jointure.

| Question | Vestiaire à étiquettes (table plate) | Vestiaire à fiches (modèle) |
|---|---|---|
| Où est la ville du client ? | sur chaque veste | sur la fiche, une fois |
| Mettre à jour une ville | autant de décousues que de vestes | **1** fiche |
| Ajouter un client sans veste | impossible | une fiche, et c'est tout |
| Retirer la dernière veste | le client disparaît | la fiche reste |

Les quatre lignes du bas sont exactement les **quatre anomalies** du §5.5. Elles ne sont pas
théoriques : chacune se mesure sur le socle.

---

## 4. Vocabulaire essentiel

| Terme | Définition | Sur le fil rouge |
|---|---|---|
| **Dépendance fonctionnelle** | `A → B` : connaître A suffit à connaître B | `id_produit → designation` |
| **Dépendance partielle** | `A → B` où A n'est qu'une partie de la clé | `id_produit → designation` quand la clé est (produit × mois) |
| **Dépendance transitive** | `A → B → C`, avec B non clé | `id_produit → libellé → famille` |
| **1FN** | Chaque champ porte **une** valeur atomique | une étiquette de catégorie, jamais une liste |
| **2FN** | 1FN **et** aucun attribut ne dépend d'une partie de la clé | `fait_stock_mensuel` (produit × mois) |
| **3FN** | 2FN **et** aucun attribut ne dépend d'un attribut non clé | la famille ne se range pas dans les faits |
| **Anomalie de redondance** | la même information écrite plusieurs fois | **2 826 394** caractères recopiés |
| **Anomalie de mise à jour** | une modification à faire en plusieurs endroits | **4** lignes pour un client de l'extrait |
| **Anomalie d'insertion** | impossible d'enregistrer une occurrence seule | **416** clients sans vente |
| **Anomalie de suppression** | supprimer une ligne efface une information unique | le client 84 de l'extrait |
| **Table de correspondance** | table qui porte une règle de traduction du référentiel | **16** étiquettes → **7** familles |
| **Dénormalisation** | redondance **choisie** et documentée | la famille recopiée dans `dim_produit` |

> **Définition.** Une **forme normale** est une propriété d'une table, pas d'une base : une table est en
> 1FN, en 2FN ou en 3FN — et elle peut l'être sans que ses voisines le soient. On dit d'un modèle qu'il
> est « en 3FN » quand **chacune** de ses tables l'est, ce qui n'est presque jamais le cas des modèles
> en étoile : leurs dimensions de restitution sont volontairement dénormalisées.

---

## 5. Cours approfondi

### 5.1 La 1FN — une valeur par champ

La première forme normale demande une chose simple : **un champ, une valeur**. Pas de liste dans une
cellule, pas de « et », pas de virgule qui sépare deux valeurs. Ce n'est pas une règle de style : c'est
la condition pour qu'une requête puisse filtrer, grouper et compter.

> **Définition.** Une table est en **première forme normale** (1FN) quand chaque champ contient une
> valeur **atomique** — indivisible du point de vue du modèle — et quand il n'existe ni colonne
> répétitive (« produit 1 », « produit 2 », « produit 3 ») ni valeur composite rangée dans un seul
> champ (« Ciment, Tôle »). Une clé, elle, peut être composée : c'est la **valeur** qui doit être
> atomique, pas la clé.

Le module a rencontré cette faute dans son **propre** fichier, et c'est instructif. L'extrait
`03_exercices/dossier_M13/table_plate.csv` contient deux lignes dont la désignation produit est
`Cable electrique 2,5 mm`. La virgule, écrite sans guillemets, compte pour un séparateur de colonne :
ces deux lignes portent **13** champs au lieu de **12**, et le fichier ne se lit plus — le moteur
refuse de deviner. Le défaut était invisible à l'œil nu, aucun total ne s'en plaignait, et il a fallu
**essayer d'ouvrir le fichier** pour le trouver.

### 5.2 La 2FN — dépendre de la clé entière

La deuxième forme normale ne concerne que les tables dont la clé est **composée**. Elle demande qu'aucun
attribut ne dépende d'une partie seulement de cette clé.

Le fil rouge fournit l'exemple parfait : le relevé de stock mensuel a pour clé (produit × mois) et
compte **6 776** lignes pour **154** produits. Si l'on recopiait la désignation du produit dans chaque
ligne du relevé, cette désignation dépendrait du **produit** seul — une partie de la clé. Recopier la
désignation coûterait **196 328** caractères contre **4 462** rangés une fois, soit **× 44,0**.

> **Définition.** Une table est en **deuxième forme normale** (2FN) quand elle est en 1FN et qu'aucun
> attribut non clé ne dépend d'une **partie** d'une clé composée. Corollaire pratique : une table dont
> la clé est simple est automatiquement en 2FN — la question ne se pose que pour les clés composées,
> c'est-à-dire pour les tables de faits dont le grain est une combinaison.

### 5.3 La 3FN — dépendre de la clé, et d'elle seule

La troisième forme normale interdit les dépendances **transitives** : `A → B → C`, avec B non clé.

Le référentiel produit du fil rouge porte **16** étiquettes de catégorie pour **7** familles réelles.
L'étiquette détermine la famille (`libellé → famille`) et la famille ne détermine pas l'étiquette :
c'est une dépendance transitive, donc une violation de la 3FN si l'on range la famille dans la même
table que la vente. Le modèle a fait un choix précis : `dim_produit` porte **à la fois** l'étiquette
d'origine (`libelle_source`, **16** valeurs) et la famille corrigée (**7** valeurs) — c'est une
**dénormalisation assumée**, justifiée par le fait qu'une dimension de restitution se lit, alors qu'une
table de faits s'additionne. Ce choix est discuté au §5.6, et il n'est pas gratuit.

> **Définition.** Une table est en **troisième forme normale** (3FN) quand elle est en 2FN et qu'aucun
> attribut non clé n'en détermine un autre. On dit parfois qu'un attribut doit dépendre « de la clé,
> de toute la clé, et de rien d'autre que la clé » — c'est la formule à retenir, à condition de se
> souvenir qu'elle parle de **chaque** table séparément.

### 5.4 Les quatre formes et la quatrième, citée

Au-delà de la 3FN existent la **forme normale de Boyce-Codd** (BCNF, une variante plus stricte de la
3FN pour les clés multiples) et les formes 4 et 5, qui traitent des dépendances multivaluées. Le module
les **cite** sans les démontrer : les modèles en étoile du programme vivent en 3FN, et la seule
question qui se pose en pratique est de savoir **quand** une dénormalisation est un choix. Un cours qui
s'arrête à la 3FN n'est pas un cours incomplet ; c'est un cours qui sait où il s'arrête.

### 5.5 Les quatre anomalies, mesurées sur le fil rouge

| Anomalie | Ce qu'elle est | La mesure du fil rouge |
|---|---|---|
| **Redondance** | la même information écrite plusieurs fois | **2 826 394** caractères de noms recopiés contre **239 599** rangés une fois (**× 11,8**) ; **278** contre **92** sur l'extrait (**× 3,0**) |
| **Mise à jour** | une modification à répéter partout | **4** lignes pour changer la ville du client 41 dans l'extrait ; **20** lignes pour le client le plus actif du socle |
| **Insertion** | impossible de créer une occurrence seule | **416** clients du référentiel n'ont aucune vente : le fichier plat ne peut pas les porter |
| **Suppression** | effacer une ligne efface une information unique | le client 84 (« SARL Nabonswendé ») tient sur **2** lignes : supprimer ses deux ventes le fait disparaître du fichier |

Les deux dernières anomalies sont les plus coûteuses en pratique, parce qu'elles sont **silencieuses** :
un client qui n'existe plus ne se voit pas dans un total de chiffre d'affaires. Sur le fil rouge, les
**416** clients sans achat représentent l'avenir commercial de l'entreprise : ce sont des prospects,
et un modèle qui ne peut pas les ranger ne peut pas les suivre.

> **Dans les faits.** Le socle du module **peut** ranger ces quatre cas, et il le prouve : les **416**
> clients sans vente existent dans `dim_client` (anomalie d'insertion abolie) ; une vente peut être
> supprimée sans faire disparaître son client (anomalie de suppression abolie) ; modifier une ville
> touche **1** ligne au lieu de **20** (anomalie de mise à jour abolie) ; et les noms tiennent en
> **239 599** caractères au lieu de **2 826 394** (anomalie de redondance abolie).

### 5.6 Quand ne pas normaliser

Un modèle en étoile n'est **pas** en 3FN, et il a raison de ne pas l'être. Trois cas justifient une
dénormalisation, à condition de l'écrire :

1. **la dimension de restitution** : `dim_produit` porte l'étiquette d'origine **et** la famille
   corrigée, parce qu'un rapport par famille doit pouvoir se comparer au référentiel tel qu'il est
   écrit — **16** étiquettes affichées, **7** lignes publiées ;
2. **la table d'export** : un fichier destiné à un tableur doit être plat, sinon il n'est pas utilisable
   (le socle du module en fournit un : `table_plate.csv`, **18** lignes) ;
3. **le cache de calcul** : une table agrégée par mois et par magasin recopie ce qui a déjà été
   calculé — c'est une redondance de **performance**, pas de modèle, et elle se régénère.

> **Attention.** Une dénormalisation non écrite devient une redondance subie : personne ne sait plus
> laquelle des deux colonnes fait foi, et un jour elles se contrediront. La règle du module : **une
> redondance se déclare, avec sa raison et sa requête de régénération.** Sinon, elle se paiera en
> anomalies — les quatre du §5.5.

### 5.7 Une table de correspondance n'est pas une correction

Les **16** étiquettes pour **7** familles posent une question de gouvernance : où corrige-t-on ?
Trois réponses possibles, et une seule est bonne :

- **dans la requête** : chaque analyste écrit son `CASE`, et deux analystes produisent deux
  classements — c'est ce que fait la table plate, et c'est pour cela que le classement du §2 est faux ;
- **dans la source** : on corrige le fichier du référentiel — la bonne cible, mais elle n'est pas
  toujours accessible, et l'historique reste sale ;
- **dans une table de correspondance du modèle** : la règle est écrite **une fois**, versionnée, et
  applicable à l'historique. C'est le choix du module.

Un **piège technique** accompagne la deuxième solution : deux étiquettes du référentiel portent une
**espace finale** (`Matériaux ` et `Quincaillerie `). Sans le `TRIM` avant la correspondance, la
traduction laisse passer **9** familles au lieu de **7** — la table de correspondance a l'air juste,
et le modèle compte deux familles fantômes. Le module a rencontré ce défaut, l'a mesuré et l'a corrigé.

---

## 6. Exemple concret — le classement qui change de tête

Le chapitre C01 a présenté l'extrait `table_plate.csv` (**18** lignes, **6** clients). Voici la même
question posée de deux façons sur le socle complet : « quelle est la famille de produits qui pèse le
plus ? »

**Réponse par étiquette brute** (table plate, **16** groupes) : Plomberie **3 418 137 911** FCFA,
Electricité **2 469 701 472** FCFA, Bois & panneaux **1 727 101 681** FCFA.

**Réponse par famille corrigée** (**7** groupes) : Materiaux **3 492 592 638** FCFA, Plomberie
**3 418 137 911** FCFA, Electricite **2 469 701 472** FCFA, Quincaillerie **1 891 970 547** FCFA,
Bois et panneaux **1 727 101 681** FCFA, Consommables **1 375 225 530** FCFA, Peinture
**1 045 255 378** FCFA.

La différence n'est pas dans la requête — les deux comptent des ventes — mais dans la **structure**.
Dans la version brute, la famille matériaux est coupée en quatre morceaux :

| Étiquette brute | Chiffre d'affaires |
|---|---|
| `materiaux` | **1 351 022 329** FCFA |
| `Matériaux ` (espace finale) | **929 913 501** FCFA |
| `Materiaux` | **923 055 165** FCFA |
| `MATÉRIAUX` | **288 601 643** FCFA |
| **Total de la famille** | **3 492 592 638** FCFA |

Le plus gros fragment (**1 351 022 329** FCFA) n'apparaît qu'en **5e** position d'un classement par
étiquette. Un analyste qui publie le « top 3 » de ce classement annonce trois familles et en oublie
une — la première. C'est exactement la faute que le module M11 avait chiffrée sur les classements
(publier un classement sans vérifier le libellé), et la parade est la même : **le libellé publié est
celui de la mesure triée**, jamais celui du fichier source.

> **À retenir.** Un mauvais modèle ne se contente pas de ralentir : il **classe faux**. Et un
> classement faux est bien plus difficile à contester qu'un total faux, parce qu'il a l'air d'une
> opinion — « matériaux est un gros poste » — alors que c'est une erreur de structure.

---

## 7. Démonstration pas à pas — quatre étapes de normalisation

### 7.1 Étape 1 — écrire les dépendances fonctionnelles

Avant de toucher aux tables, on écrit les dépendances sur le papier. Sur le fil rouge, la liste
complète des tables de faits tient en quelques lignes :

```
id_client     → nom, ville, segment, conditions_paiement
id_produit    → designation, libelle_source, famille, sous_categorie, unite
id_magasin    → nom, ville, type_magasin, responsable
id_vendeur    → nom_complet, id_magasin, statut
id_vente      → date_vente, id_produit, id_client, id_magasin, id_vendeur, quantite, montant_ttc
(id_produit, mois)             → quantite_en_stock
(id_produit, id_magasin, mois) → est_en_rupture
```

Chaque flèche est une affirmation vérifiable : `id_produit → designation` se contrôle en comptant les
désignations distinctes par produit — **154** produits, **154** désignations.

### 7.2 Étape 2 — chercher les dépendances qui ne partent pas de la clé

On relit la liste en cherchant deux motifs : une flèche qui part d'une **partie** de clé composée
(2FN), et une flèche qui part d'un attribut non clé (3FN). Sur le fil rouge, la table plate en porte
deux :

```sql
-- 3FN : la famille dépend de l'étiquette, pas de la clé de la table
SELECT COUNT(DISTINCT libelle_source) AS etiquettes,
       COUNT(DISTINCT famille)        AS familles
FROM dim_produit;              -- 16 et 7
```

```sql
-- 2FN : la désignation ne dépend que du produit, pas du couple (produit, mois)
SELECT COUNT(*) AS lignes FROM fait_stock_mensuel;      -- 6 776
SELECT COUNT(DISTINCT id_produit) FROM fait_stock_mensuel;  -- 154
```

### 7.3 Étape 3 — mesurer ce que la correction rapporte

Une normalisation se justifie par un écart. Trois écarts mesurés sur le socle :

| Ce qu'on mesure | Table plate | Modèle |
|---|---|---|
| Lignes / colonnes de la table la plus large | **240 000** lignes, **11** colonnes | **240 000** lignes, **17** colonnes dans les faits, **50** colonnes dans les cinq dimensions |
| Caractères de noms de clients | **2 826 394** | **239 599** |
| Caractères de désignations (relevé de stock) | **196 328** | **4 462** |
| Groupes obtenus par catégorie | **16** | **7** |
| Durée de la même requête de groupe | **4** ms | **2** ms |

La dernière ligne mérite qu'on s'y arrête : sur DuckDB, un moteur **en colonnes**, la version
normalisée est **plus rapide** que la version plate, parce qu'elle ne lit que les colonnes utiles et
que la dimension tient en **154** lignes. Le coût de la normalisation n'est donc pas là : il est dans
l'écriture (deux tables à charger au lieu d'une), dans la discipline (une clé à respecter) et dans la
documentation (une correspondance à écrire).

> **Attention.** Les deux durées ci-dessus sont mesurées dans l'atelier du module, sur ce socle et ce
> moteur. Elles disent une **propriété du moteur** (un moteur en colonnes ne paie pas la jointure),
> pas une loi générale : sur un système ligne à ligne et sans index, la même requête normalisée peut
> coûter cher. La règle qui survit au changement de moteur : **mesurez chez vous, et ne citez pas la
> mesure d'un autre.**

### 7.4 Étape 4 — corriger la donnée, pas la requête

La famille est sale à la source (**16** étiquettes). Le module ne corrige pas le fichier : il écrit la
correspondance **dans le modèle**, une fois, et il compte le résultat.

```sql
SELECT famille, COUNT(*) AS produits, ROUND(SUM(f.montant_ttc)) AS ca
FROM fait_ventes f JOIN dim_produit p ON p.id_produit = f.id_produit
GROUP BY 1 ORDER BY ca DESC;
```

Sept lignes en sortie, contre seize avec l'étiquette brute. Le `TRIM` de l'étape précédente n'est pas
un détail de propreté : sans lui, cette requête rend **9** lignes et le modèle compte deux familles de
plus que la réalité.

---

## 8. Erreurs fréquentes

| Erreur | Ce qu'elle produit | La parade |
|---|---|---|
| Corriger la donnée dans chaque requête | deux analystes, deux classements (**16** contre **7** groupes) | une table de correspondance, écrite une fois |
| Oublier le `TRIM` avant une correspondance | **9** familles au lieu de **7** | trimmer, puis mapper, puis compter |
| Normaliser sans écrire les dépendances | des tables coupées « au feeling », des jointures oubliées | écrire `A → B` avant de couper |
| Croire qu'une table à clé simple est en 3FN | une clé simple n'exempte que de la 2FN | vérifier les dépendances transitives |
| Supprimer la dernière ligne d'un client | le client disparaît, le prospect aussi | une dimension, une ligne par client |
| Dénormaliser sans le dire | deux colonnes qui finiront par se contredire | déclarer, justifier, régénérer |

---

## 9. Bonnes pratiques professionnelles

- **Écrivez les dépendances fonctionnelles** de chaque table, en clair, avant tout `CREATE` : c'est le
  document de travail de la normalisation.
- **Cherchez les flèches qui ne partent pas de la clé** : partie de clé → 2FN, attribut non clé → 3FN.
- **Ne corrigez jamais une étiquette dans une requête** : une règle de traduction s'écrit une fois.
- **Contrôlez le nombre de groupes** après chaque correspondance : **16** étiquettes devenues **7**
  familles se vérifient en une ligne ; **9**, c'est un défaut.
- **Mesurez le coût de vos choix** : une dénormalisation se justifie par un chiffre, pas par une
  intuition (ici, **4** ms contre **2** ms).

> **Conseil professionnel.** Quand un référentiel est sale, la tentation est de le nettoyer
> « plus tard ». Le module propose l'inverse : **consignez la saleté dans une table de correspondance**,
> publiez avec la correspondance, et nettoyez la source quand vous en aurez les moyens. Un modèle qui
> attend un référentiel propre ne sort jamais.

> **À retenir.** Normaliser n'est pas ranger, c'est **décider de qui dépend de quoi**. Une table plate
> ne ment pas sur les totaux : elle ment sur les **classements** — Plomberie en tête au lieu de
> matériaux, et **3 492 592 638** FCFA invisibles dans le tableau.

---

## 10. Exercice guidé

**Sujet.** La table ci-dessous vient d'un service commercial. Elle n'est pas en 3FN. Trouvez les
dépendances, nommez les violations, proposez le découpage, et chiffrez le gain.

| id_vente | id_produit | designation | categorie | famille | id_client | ville_client | quantite |
|---|---|---|---|---|---|---|---|
| 1 | 12 | Ciment CPJ45 50 kg | Materiaux | Materiaux | 41 | Ouagadougou | 40 |
| 2 | 12 | Ciment CPJ45 50 kg | MATÉRIAUX | Materiaux | 41 | Ouagadougou | 25 |
| 3 | 7 | Peinture acrylique 20 l | PEINTURE | Peinture | 41 | Bobo-Dioulasso | 6 |

**Étape 1 — écrire les dépendances visibles.**

```
id_vente   → id_produit, id_client, quantite
id_produit → designation, categorie, famille
id_client  → ville_client
categorie  → famille
```

**Étape 2 — nommer les violations.** `id_produit → designation` viole la 3FN si ces colonnes sont
rangées dans une table dont la clé est `id_vente` : la désignation dépend d'un attribut non clé.
`categorie → famille` est une dépendance transitive. Et les deux lignes du produit 12 montrent la
conséquence : **2** étiquettes différentes pour la même famille, donc un classement par étiquette qui
créera deux groupes.

**Étape 3 — proposer le découpage.** Trois tables : `dim_produit(id_produit, designation, categorie,
famille)`, `dim_client(id_client, ville_client)`, `fait_ventes(id_vente, id_produit, id_client,
quantite)`. La correspondance `categorie → famille` reste un choix à documenter : dans la dimension
(choix du module) ou dans une table dédiée.

**Étape 4 — chiffrer.** Sur le fil rouge complet, cette même correction fait passer la recopie du nom
de client de **2 826 394** à **239 599** caractères, la recopie de la désignation de **196 328** à
**4 462**, et le nombre de groupes publiés de **16** à **7**.

---

## 11. Exercices autonomes

**Exercice 2.1.** Écrivez la liste complète des dépendances fonctionnelles de `dim_magasin` (**6**
lignes, **10** colonnes), puis dites, en justifiant, si la table est en 3FN. Une colonne pose
question : `responsable` — dépend-elle du magasin, ou d'autre chose ?

**Exercice 2.2.** Construisez, à partir du socle, une table plate de **20** lignes environ qui contient
la vente, le client, le produit et le magasin, puis appliquez-lui les quatre anomalies du §5.5 en
donnant pour chacune la requête qui la démontre.

**Exercice 2.3.** Le référentiel écrit la famille « matériaux » de **4** façons, pour un total de
**3 492 592 638** FCFA. Écrivez la requête qui le prouve, puis celle qui produit le classement correct.
Combien de groupes obtient-on avant, combien après ?

**Exercice 2.4.** Un service vous livre un fichier de **1 200** lignes où la colonne `telephone`
contient parfois deux numéros séparés par un point-virgule. Dites quelle forme normale est violée,
écrivez la requête qui compte les lignes concernées, et proposez la correction : deux colonnes, ou une
table de téléphones ?

---

## 12. Correction détaillée

**Exercice 2.1.** Dépendances : `id_magasin → nom, ville, quartier, region, type_magasin,
surface_m2, ouverture` et `id_magasin → responsable`. La table est en 3FN **parce que** tout dépend de
la clé et de rien d'autre : `responsable` dépend du magasin (un magasin a un responsable à la fois),
et non d'un attribut intermédiaire. La question à se poser est celle du temps : si le responsable
change chaque année et qu'on veut l'historique, `responsable` devient un attribut **variable** et
appelle une dimension historisée — c'est le sujet du chapitre C04.

**Exercice 2.2.** La table plate se construit par jointure des faits et des dimensions ; les quatre
anomalies se démontrent ainsi : **redondance** — comparer `SUM(LENGTH(nom_client))` sur **240 000**
lignes et sur la dimension ; **mise à jour** — compter les lignes du client 41 dans la table plate
(**4** dans l'extrait, **20** pour le client le plus actif du socle) ; **insertion** — chercher un
client du référentiel sans vente (**416** cas) : il n'apparaît dans aucune ligne de la table plate ;
**suppression** — supprimer les lignes du client 84 de l'extrait (**2** lignes) et constater que le
client disparaît entièrement du fichier.

**Exercice 2.3.** La requête de preuve groupe par étiquette brute en filtrant sur le motif
`MAT%` : quatre lignes, dont la plus grosse vaut **1 351 022 329** FCFA ; leur somme vaut
**3 492 592 638** FCFA. Le classement correct groupe par `famille` : **7** groupes, avec Materiaux en
tête. Avant : **16** groupes. Après : **7**.

**Exercice 2.4.** La 1FN est violée : un champ contient **deux** valeurs. La requête compte les lignes
où le séparateur apparaît (`WHERE telephone LIKE '%;%'`) ; la correction dépend de l'usage : **deux
colonnes** si la seconde valeur est toujours de même nature (bureau, mobile), une **table de
téléphones** si le nombre de numéros est variable — c'est alors une entité à part entière, reliée au
client par une cardinalité `1,N`.

---

## 13. Mini-projet de chapitre

**« La table de correspondance du référentiel »** (2 h). Produisez, pour le fil rouge : (1) la liste
des **16** étiquettes de catégorie avec leur famille cible et le nombre de produits concernés ;
(2) la ou les dépendances fonctionnelles qui justifient cette correspondance ; (3) la requête qui
prouve que la correspondance donne **7** groupes et non **9** (attention au `TRIM`) ; (4) une phrase
de règle : « quand une nouvelle étiquette apparaît, elle doit être ajoutée à la correspondance, sinon
elle produit une famille fantôme ». Ce livrable est la matière de P4 (note de choix) du projet.

---

## 14. Résumé du chapitre

| Notion | Ce qu'il faut retenir |
|---|---|
| 1FN | une valeur par champ — la virgule non protégée du fichier plat l'a démontré |
| 2FN | pas de dépendance à une partie de la clé composée (**6 776** lignes de stock) |
| 3FN | pas de dépendance entre attributs non clés (`catégorie → famille`) |
| Anomalies | redondance (**× 11,8**), mise à jour (**20** lignes), insertion (**416** clients), suppression (**2** lignes) |
| Correspondance | **16** étiquettes → **7** familles, avec `TRIM` (sinon **9**) |
| Classement juste | Materiaux **3 492 592 638** FCFA en tête, pas Plomberie en tête |
| Coût mesuré | **4** ms contre **2** ms : normaliser ne ralentit pas la lecture |
| Dénormalisation | décidée, écrite et régénérable — jamais subie |

## 15. À retenir

> **À retenir.** Normaliser, c'est écrire **de quoi chaque attribut dépend**. Les trois formes normales
> ne sont que trois questions posées à chaque table : tes valeurs sont-elles atomiques ? dépendent-elles
> de toute la clé ? dépendent-elles d'autre chose que la clé ?

- **La 1FN se contrôle par un compte de champs** : deux lignes à **13** champs dans un fichier à
  **12** colonnes suffisent à rendre un fichier illisible.
- **La 2FN ne concerne que les clés composées** : stock (**6 776** lignes) et ruptures.
- **La 3FN interdit les chaînes** : `catégorie → famille` doit être traitée une fois, dans une
  correspondance.
- **Les quatre anomalies se mesurent** : redondance **2 826 394** caractères, mise à jour **20** lignes,
  insertion **416** clients, suppression **2** lignes d'un client.
- **Une étiquette non corrigée classe faux** : **3 492 592 638** FCFA invisibles derrière **4**
  écritures de la même famille.

## 16. Évaluation formative

1. Énoncez la 1FN sans utiliser le mot « normaliser », et donnez un exemple de violation.
2. Qu'est-ce qu'une dépendance fonctionnelle ? Écrivez-en deux sur `dim_client`.
3. Pourquoi la 2FN ne concerne-t-elle que les tables à clé composée ?
4. Donnez un exemple de dépendance transitive sur le fil rouge, et la correction retenue.
5. Nommez les quatre anomalies et la mesure qui les illustre sur le socle.
6. Pourquoi le classement par étiquette brute est-il faux, et quel chiffre est caché ?
7. Combien de groupes obtient-on sans le `TRIM` de la correspondance, et pourquoi ?
8. Normaliser coûte-t-il du temps de lecture ? Que dit la mesure faite sur ce moteur ?
9. Citez trois cas où la dénormalisation est un bon choix, et la condition à remplir.
10. Une table à clé simple peut-elle violer la 3FN ? Justifiez par un exemple.

**Corrigé :** 1. Chaque champ contient une valeur indivisible ; une violation : une colonne
`produits` contenant `Ciment, Tôle`. 2. `id_client → nom`, `id_client → ville`. 3. Parce qu'une clé
simple ne comporte pas de partie : il n'y a rien dont un attribut pourrait dépendre « à moitié ».
4. `catégorie → famille` (**16** étiquettes pour **7** familles) ; correction : une table de
correspondance appliquée dans la dimension, `TRIM` compris. 5. Redondance (**2 826 394** contre
**239 599** caractères), mise à jour (**20** lignes pour le client le plus actif), insertion (**416**
clients sans achat), suppression (le client 84, **2** lignes). 6. Parce que la même famille est écrite
de **4** façons : Materiaux pèse **3 492 592 638** FCFA et n'apparaît pas dans un top trois par
étiquette. 7. **9** groupes au lieu de **7**, à cause de deux étiquettes portant une espace finale.
8. Non : **2** ms pour la version normalisée contre **4** ms pour la table plate, sur ce moteur en
colonnes. 9. Dimension de restitution, table d'export, cache de calcul — à condition de l'écrire et de
pouvoir la régénérer. 10. Oui : une table de ventes à clé `id_vente` qui porterait `categorie` et
`famille` violerait la 3FN, la famille dépendant de la catégorie.
