# Module M02.C02 — Les centres : moyenne, médiane, mode ; minimum, maximum, étendue

**Outil de ce chapitre : un tableur d'abord, SQL et Python en vérification.** Durée indicative : 4 h. Niveau : N1.

> **L'idée du chapitre.** Résumer 316 tickets par un seul nombre est une décision, pas un calcul. Ce chapitre
> pose les trois candidats — moyenne, médiane, mode — et les trois bornes — minimum, maximum, étendue — puis
> répond à la seule question qui vaille en entreprise : **lequel montre-t-on, et que cache-t-il ?** Sur le fichier
> du module, le même tableau de ventes donne un panier de 114 156 FCFA en moyenne et de 58 423 FCFA en médiane :
> ce n'est pas une erreur de calcul, c'est la forme des données qui parle.

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous saurez :

1. **Calculer** moyenne, médiane, mode, minimum, maximum et étendue d'une colonne numérique, dans un tableur, en SQL et en Python, et obtenir le même résultat par les trois voies.
2. **Choisir** le centre qui décrit une distribution donnée, en justifiant par sa forme (symétrique, asymétrique, à valeurs extrêmes, bornée).
3. **Annoncer** un centre sans jamais le séparer de son effectif, de son unité et de sa période.
4. **Démasquer** l'abus de moyenne : dire ce qu'elle doit aux valeurs extrêmes, et chiffrer l'écart avec la médiane.
5. **Utiliser** la moyenne pondérée quand les lignes n'ont pas le même poids, et expliquer la différence avec la moyenne simple.

---

## 2. Pourquoi cette notion est importante

**Situation 1 — le directeur et le client moyen.** On vous demande « combien dépense un client ? ». Vous sortez 114 156 FCFA. Le directeur calibre ses stocks sur ce chiffre, et six mois plus tard la moitié des clients repartent avec moins de la moitié de ce panier. Personne n'a menti : la moyenne est juste, mais **le client moyen n'existe pas** — sur les 316 tickets, 227 sont sous la moyenne, soit 71,8 % de l'échantillon. Une moyenne citée comme un cas typique produit une décision fausse à partir d'un chiffre vrai.

**Situation 2 — la comparaison entre vendeurs.** Classement brut du chiffre d'affaires par vendeur : Adama Bationo 11 370 350 FCFA sur 125 lignes, Moussa Ilboudo 6 796 535 FCFA sur 109 lignes. L'écart de total s'explique en grande partie par le nombre de lignes ; ramené à la ligne, Bationo est à 90 963 FCFA, Ilboudo à 62 354 FCFA. Avant de parler de performance, il faut savoir **ce que l'on compare** : un total, une moyenne, une médiane. Le chapitre 8 dira si cet écart est statistiquement défendable ; ici, on apprend déjà à ne pas confondre les trois chiffres.

**Situation 3 — la remise moyenne qui n'est pas la remise consentie.** La moyenne simple de la colonne `remise` vaut 1,85 %. La moyenne pondérée par les montants vaut 1,72 %. Les deux sont justes ; une seule répond à la question du directeur financier (« sur un franc facturé, combien concède-t-on ? »). Un analyste qui ne connaît que la moyenne simple croit que l'entreprise remet plus qu'elle ne le fait.

> **Dans les faits.** L'observation « la moyenne est au-dessus de la médiane sur des montants » est si fréquente
> qu'elle sert de test de cohérence : sur des données de ventes, une moyenne inférieure à la médiane signale
> presque toujours un défaut (retours non isolés, doublons, signe inversé). C'est un réflexe de contrôle, pas une
> loi.

---

## 3. Explication simple

Dix amis vont au restaurant. Neuf consomment un plat à 3 000 FCFA, le dixième commande un plateau à fruits de mer à 60 000 FCFA.

- La **moyenne** de la table est (9 × 3 000 + 60 000) ÷ 10 = 5 700 FCFA. Elle est juste, et elle ne décrit personne : aucun des dix convives n'a dépensé 5 700 FCFA.
- La **médiane** est 3 000 FCFA : c'est ce que paie la moitié de la table, au milieu de la file. Elle décrit la table, mais ne dit rien de l'addition totale.
- Le **mode** est 3 000 FCFA : c'est le montant qui revient le plus souvent.
- Le **minimum** est 3 000, le **maximum** 60 000, l'**étendue** 57 000 FCFA.

L'addition, elle, ne bouge pas : 87 000 FCFA. C'est la leçon du chapitre — **la moyenne porte l'argent, la médiane porte les gens**. Quand on parle de recettes, on prend la moyenne ; quand on parle du comportement habituel d'un client, on prend la médiane ; et l'on dit les deux si l'on ne veut pas être démenti.

---

## 4. Vocabulaire essentiel

| Français — English | Définition simple | Piège à éviter |
|---|---|---|
| **Moyenne arithmétique — mean** | Somme des valeurs divisée par l'effectif. | La présenter comme « le cas typique » ; elle est sensible aux extrêmes. |
| **Médiane — median** | La valeur qui partage la série en deux moitiés d'effectif égal. | Oublier de trier, ou interpoler sans le dire entre deux valeurs. |
| **Mode — mode** | La valeur (ou la modalité) la plus fréquente. | Chercher un mode sur des valeurs presque toutes distinctes : il est then artefact. |
| **Minimum / Maximum** | Les deux valeurs extrêmes observées. | Les confondre avec des bornes autorisées par le métier. |
| **Étendue — range** | Maximum moins minimum. | La résumer à elle seule la dispersion : un seul ticket suffit à l'exploser. |
| **Moyenne pondérée — weighted mean** | Moyenne où chaque valeur pèse selon un poids (montant, effectif). | Confondre poids et valeur : pondérer par la colonne elle-même est parfois ce qu'on veut, parfois une faute. |
| **Valeur extrême — outlier** | Observation très éloignée du reste, à vérifier avant de commenter. | Supprimer « pour que ce soit propre » sans journaliser la décision. |
| **Trimée (moyenne) — trimmed mean** | Moyenne calculée après retrait d'une proportion fixe des extrêmes. | La comparer à la moyenne sans dire quel pourcentage a été retiré. |
| **Centre — measure of central tendency** | Nombre unique situé « au milieu » des données. | En choisir un par habitude de logiciel plutôt que par la forme des données. |
| **Additivité — additivity** | Propriété d'un total à se décomposer en sous-totaux cohérents. | Croire qu'une moyenne se décompose : la moyenne d'un ensemble n'est pas la moyenne des moyennes. |

---

## 5. Cours approfondi

### 5.1 Les formules, sans mystère

Pour une série de *n* valeurs triées $x_1 \le x_2 \le \dots \le x_n$ :

- **Moyenne** : $\bar{x} = \dfrac{1}{n}\sum_{i=1}^{n} x_i$. Elle est **additive** : la somme des valeurs est exactement $n \times \bar{x}$. C'est la raison pour laquelle la moyenne est l'outil de la comptabilité et du budget.
- **Médiane** : valeur au rang $\frac{n+1}{2}$ après tri. Si *n* est pair, on prend la demi-somme des deux valeurs centrales — et on le dit, car ce nombre peut ne correspondre à aucune observation réelle.
- **Mode** : valeur de fréquence maximale. Une série peut n'avoir aucun mode utile (toutes les valeurs distinctes), ou plusieurs (bimodale : deux clientèles distinctes dans le même fichier).
- **Minimum, maximum, étendue** : $x_{min}$, $x_{max}$, $x_{max} - x_{min}$.

> **Définition.** **Moyenne arithmétique** — *arithmetic mean* — le total réparti également. Sa propriété utile :
> multiplier la moyenne par l'effectif redonne le total, au kuru près. Sa propriété dangereuse : un seul individu
> extrême la déplace proportionnellement à sa taille, pas à sa fréquence.

> **Définition.** **Médiane** — *median* — la valeur du milieu après tri. Elle ne se laisse pas déplacer par un
> extrême : doubler le plus gros ticket du fichier ne change pas d'un franc la médiane. C'est ce qui la rend
> lisible pour décrire « le cas courant », et inutilisable pour prévoir une recette.

> **Définition.** **Mode** — *mode* — la valeur la plus fréquente. Seul centre calculable sur une variable
> qualitative (« la catégorie la plus vendue »), il est inexploitable sur une colonne presque continue : nos
> paniers modaux valent 6 797 et 8 260 FCFA, trois fois chacun sur 316 tickets : rien de spécial, sinon d'être
> tombés trois fois — et deux valeurs plutôt qu'une, ce qui est déjà une information (la série est multimodale).

### 5.2 Les trois centres sur le fichier du module : lire les écarts

Sur les 316 tickets de l'extrait nettoyé (480 lignes, magasin 5, 2025) :

| Indicateur | Valeur | Ce qu'il permet de dire |
|---|---|---|
| Moyenne | 114 156 FCFA | le ticket pèse en moyenne ce poids dans la recette totale |
| Médiane | 58 423 FCFA | la moitié des tickets est en dessous, la moitié au-dessus |
| Mode(s) | 6 797 et 8 260 FCFA (3 fois chacun) | deux modes, trois occurrences : aucun exploitable — à écarter explicitement du rapport |
| Minimum | -150 804 FCFA | un ticket de retour, pas une vente : à isoler, pas à commenter comme un client pauvre |
| Maximum | 1 343 666 FCFA | un chantier, pas un ménage |
| Étendue | 1 494 470 FCFA | la série s'étale sur plus de vingt-cinq fois la médiane (rapport max/médiane : 23,0) |

La moyenne dépasse la médiane de 55 733 FCFA — un **rapport de 1,95**. Voilà la phrase à écrire dans une note :
« le panier moyen est près de deux fois le panier médian, ce qui indique une forte concentration de la recette sur
peu de gros tickets ». Et sa conséquence opérationnelle, mesurée aussi : **les 10 % des tickets les plus gros
portent 47,5 % du chiffre d'affaires de l'extrait**. On peut décider de traiter cette frange à part (délai,
acompte, livreur dédié) ; on ne peut plus décider pour toute la clientèle d'après le panier moyen.

### 5.3 La médiane a un effet de seuil, la moyenne un effet de niveau

Deux propriétés à connaître pour ne pas se faire surprendre en réunion :

- **La médiane ne bouge presque pas** quand une valeur extrême change. Doubler le plus gros ticket du fichier (1 343 666 FCFA) ne déplace pas la médiane d'un franc ; la moyenne, elle, remonte d'environ 4 000 FCFA — 1 343 666 FCFA répartis sur 316 tickets — sans que le comportement habituel de qui
que ce soit ait changé.
- **La moyenne se déplace exactement comme une somme** : si l'on retire du fichier 8 lignes de montants négatifs (les retours, dont le total fait basculer des dizaines de milliers de francs), la moyenne par ligne passe de 75 152 à 77 028 FCFA. C'est un autre calcul sur un autre périmètre, pas une correction du précédent.

D'où la règle de rédaction : **toute moyenne citée s'accompagne du périmètre** (avec ou sans retours, avec ou sans
doublons, sur extrait ou sur fichier complet). Deux chiffres corrects et différents racontent la même réalité sous
deux angles — à condition que l'angle soit nommé.

### 5.4 Moyenne simple, moyenne pondérée : la colonne `remise` le démontre

Sur 480 lignes, la colonne `remise` contient six modalités. Sa moyenne simple vaut 0,0185 : c'est « la remise
moyenne **par ligne** ». La moyenne pondérée par les montants hors taxes vaut 0,0172 : c'est « la remise moyenne
**par franc facturé** ». Le calcul :

$$\text{pondérée} = \frac{\sum_i \text{remise}_i \times |\text{montant\_ht}_i|}{\sum_i |\text{montant\_ht}_i|}$$

L'écart de 0,13 point (7 % en relatif) vient de ce que les grosses lignes sont moins remisées que les petites. Cette
dissymétrie est une information de politique commerciale : si l'on veut protéger la marge sur les gros
chantiers, la moyenne simple — celle que le magasin voit — est trompeuse.

> **Définition.** **Moyenne pondérée** — *weighted mean* — moyenne dans laquelle chaque valeur compte pour un
> poids. À utiliser dès que les individus n'ont pas la même taille économique : prix, taux, remises, délais,
> taux de marge, taux de transformation.

> **Attention.** La moyenne des moyennes n'est pas la moyenne. Reprendre les douze moyennes mensuelles de l'extrait
> et les moyenne-ner donne un chiffre faux dès que les mois n'ont pas le même nombre de lignes. Sur notre extrait,
> le tirage a forcé l'égalité (40 lignes par mois) : c'est le seul cas où l'erreur est invisible. Ne prenez jamais
> cette habitude — agréegez à partir des montants, jamais à partir des pourcentages ou des moyennes intermédiaires.

### 5.5 Le cas d'école : tickets simples contre paniers composés

Les 316 tickets se séparent en 212 tickets d'une ligne et 104 à plusieurs lignes (32,9 %). Les centres explosent
la moyenne générale :

| Population | Effectif | Moyenne | Médiane |
|---|---|---|---|
| Tickets d'une seule ligne | 212 | 80 546 FCFA | 38 084 FCFA |
| Tickets de 2 lignes et plus | 104 | 182 668 FCFA | 130 461 FCFA |

Un « panier moyen de 114 156 FCFA » est donc le mélange de deux comportements différents. La question
professionnelle qui suit immédiatement : *veut-on piloter le mix (faire passer un client de 1 à 3 lignes) ou le
prix (augmenter le panier simple) ?* La réponse change le centre à regarder : pour le mix, la médiane et la
répartition ; pour le prix, la moyenne et son évolution.

> **Conseil professionnel.** Dans une note, présentez le couple **moyenne + médiane** avec une seule phrase
> d'interprétation : « moyenne 114 156 · médiane 58 423 FCFA : la recette est tirée par une frange de gros
> tickets, le comportement courant est à 58 423 FCFA ». Un lecteur qui n'a que la moyenne sur-achète ; un lecteur
> qui n'a que la médiane sous-estime la recette. Les deux ensemble, et l'affirmation devient robuste.

### 5.6 Minimum et maximum ne sont pas des bornes métier

Le minimum de la colonne `montant_ttc`, à la ligne, vaut -150 804 FCFA : c'est un retour, pas une erreur de saisie.
Le maximum de `quantite` vaut 68 dans le fichier nettoyé — et 14 000 dans l'énoncé : ce sont les 7 lignes dont la
quantité a été multipliée par 1 000 à l'enregistrement, corrigées au chapitre M01.C04. Le minimum de `prix_unitaire_ht` est 675 FCFA, le maximum
40 550 FCFA : deux extrêmes plausibles dans un catalogue de quincaillerie, à confronter au fichier fournisseur si
l'on veut en tirer une décision.

La règle : **un extrême se qualifie avant de se résumer.** Trois questions, dans l'ordre : est-ce une erreur de
fabrication (le ×1 000) ? est-ce un autre objet métier (le retour) ? est-ce un cas réel et rare (le chantier à
1 343 666 FCFA) ? Selon la réponse, on corrige, on isole dans un segment, ou on garde et on mentionne.

> **Attention.** Supprimer les extrêmes pour « nettoyer » détruit l'additivité de la moyenne : le total de
> l'entreprise ne change pas, mais la moyenne que vous citez ne correspond plus à aucun chiffre du système de
> caisse, et plus personne ne peut la retrouver. Si une moyenne sans extrêmes est utile (moyenne trimée), elle se
> cite **avec** sa règle de retrait et avec le total d'origine. Sur le fichier du module, la moyenne trimée des
> tickets (25 tickets hors borne supérieure de Tukey) tombe à 71 463 FCFA, la médiane à 54 044 FCFA : les deux
> se resserrent, c'est exactement ce que l'on attend d'un retrait d'extrêmes — et c'est ce qu'il faut écrire.

### 5.7 Calculer les six nombres dans les trois outils

| Nombre | Tableur (Excel / LibreOffice Calc) | SQL (DuckDB) | Python (pandas) |
|---|---|---|---|
| Moyenne | `=MOYENNE(M2:M481)` | `AVG(montant_ttc)` | `df.montant_ttc.mean()` |
| Médiane | `=MEDIANE(M2:M481)` | `MEDIAN(montant_ttc)` | `df.montant_ttc.median()` |
| Mode | `=MODE.UNI(M2:M481)` (Excel) · `=MODE(...)` (Calc) | `MODE(montant_ttc) WITHIN GROUP (ORDER BY montant_ttc)` | `df.montant_ttc.mode()` |
| Minimum | `=MIN(M2:M481)` | `MIN(montant_ttc)` | `df.montant_ttc.min()` |
| Maximum | `=MAX(M2:M481)` | `MAX(montant_ttc)` | `df.montant_ttc.max()` |
| Étendue | `=MAX(...)-MIN(...)` | `MAX(...)-MIN(...)` | `df.montant_ttc.max()-df.montant_ttc.min()` |
| Nombre de valeurs | `=NB(M2:M481)` | `COUNT(montant_ttc)` | `df.montant_ttc.count()` |

Un détail qui fait perdre une heure : en SQL, la fonction de médiane est une **fonction d'agrégat ordonnée** —
là où `AVG` accepte n'importe quoi, la médiane exige de dire dans quel ordre on cherche le milieu. Et dans les
deux tableurs, le mode s'appelle différemment selon la version et la suite (Excel 2021+ : `MODE.UNI`,
`MODE.MULT` pour les modes multiples ; LibreOffice 24.8 : `MODE`, `MODE.MULT`) : vérifiez le nom dans l'assistant
de fonction avant de l'écrire dans une procédure destinée à durer.

> **Boîte à outils.** Le contrôle minimal de tout centre : (1) `=NB()` doit redonner l'effectif attendu — sinon
> des valeurs texte sont silencieusement ignorées, et votre moyenne porte sur 478 lignes au lieu de 480 ; (2) la
> moyenne fois l'effectif doit redonner la somme, `=MOYENNE(range)*NB(range)` contre `=SOMME(range)` ; (3) pour la
> médiane, vérifier que l'effectif des valeurs strictement inférieures et celui des supérieures diffèrent d'au
> plus un ; (4) si un seul de ces contrôles échoue, le problème est dans la colonne, pas dans la formule.

---

## 6. Exemple concret : le même indicateur, quatre énoncés

Voici ce que produit un analyste pressé : « panier moyen : 114 156 FCFA ». Le même fait, rédigé pour durer :

1. **Sur quoi** : 316 tickets du magasin 5, exercice 2025, extrait de 480 lignes sur 240 000 du fichier complet.
2. **Combien** : moyenne 114 156 FCFA ; médiane 58 423 FCFA ; mode non retenu (6 797 FCFA, aucune fréquence
   exploitable sur cette colonne continue).
3. **Forme** : moyenne 1,95 fois la médiane ; les 10 % de tickets les plus gros portent 47,5 % du chiffre
   d'affaires de l'extrait ; 227 tickets (71,8 %) sont sous la moyenne.
4. **Décision** : piloter le prix sur la moyenne, piloter l'expérience client sur la médiane, et traiter à part
   les 25 tickets au-dessus de la borne haute (295 445 FCFA).

Quatre lignes, aucun chiffre inventé, et plus de place pour le « ce n'était pas ce que je voulais dire ».

---

## 7. Démonstration pas à pas : les six nombres, trois outils, un contrôle

**Étape 1 — Le bon fichier, le bon périmètre.** `01_socle_donnees/data/reference/ventes_magasin5_2025_ATTENDU.csv`,
480 lignes, séparateur `;`. On travaillera sur deux objets : la colonne `montant_ttc` **par ligne** et le
**montant par ticket** (somme par `n_ticket`). Notez-le : deux séries, donc six nombres chacun.

**Étape 2 — Construire la série « ticket » dans le tableur.** Colonne N : la clé de ticket. Colonne O :
`=SOMME.SI(N:N;N2;M:M)` somme les montants du même ticket. Colonne P : `=SI(NB.SI($N$2:$N$481;N2)=1;O2;"")` ne
garde que la première occurrence de chaque ticket. Une colonne auxiliaire, un compteur, et la série des 316
paniers est prête. C'est long de dix minutes et c'est exactement ce que le tableur sait faire ; au chapitre
suivant, le même travail tiendra en une requête.

**Étape 3 — Les six nombres par ticket.** Sur la colonne des paniers : `=MOYENNE(...)` → 114 156 ;
`=MEDIANE(...)` → 58 423 ; `=MODE.UNI(...)` → 6 797 ; `=MIN(...)` → -150 804 ; `=MAX(...)` → 1 343 666 ;
`=MAX(...)-MIN(...)` → 1 494 470. Écrivez-les dans un tableau à deux colonnes : *valeur*, *unité* (FCFA).

**Étape 4 — Les six nombres par ligne.** Même opération directement sur `montant_ttc` : moyenne 75 152 FCFA,
médiane 37 966 FCFA, minimum -150 804 FCFA, maximum 1 229 678 FCFA. Le fait que la moyenne par ligne soit
inférieure à la moyenne par ticket est normal et attendu : une ligne est une fraction de ticket (1,52 ligne par
ticket).

**Étape 5 — Le contrôle d'additivité.** `=MOYENNE(M2:M481)*NB(M2:M481)` doit donner 36 073 185 FCFA, soit le
total de la colonne. Si l'écart dépasse un franc, vous avez un souci de périmètre (filtre actif, ligne texte
ignorée), pas une erreur d'arrondi.

**Étape 6 — La version SQL, en une requête.**

```sql
WITH paniers AS (
    SELECT n_ticket, SUM(montant_ttc) AS panier, COUNT(*) AS nb_lignes
    FROM read_csv('01_socle_donnees/data/reference/ventes_magasin5_2025_ATTENDU.csv', sep=';')
    GROUP BY n_ticket
)
SELECT COUNT(*)                                    AS tickets,
       ROUND(AVG(panier))                          AS moyenne,
       ROUND(MEDIAN(panier))                       AS mediane,
       MIN(panier)                                 AS minimum,
       MAX(panier)                                 AS maximum,
       MAX(panier) - MIN(panier)                   AS etendue,
       SUM(CASE WHEN nb_lignes = 1 THEN 1 ELSE 0 END) AS tickets_simple
FROM paniers;
```

**Pour la suite du module : figez ces deux relations.** Ouvrez DuckDB **à la racine du dépôt** (commande `duckdb`,
sans argument) et créez deux vues. Les chapitres C03 à C06 écriront leurs requêtes contre `lignes_ventes` et
`paniers`, et ils ne fonctionneront qu'après ces deux lignes.

```sql
-- une fois pour toutes dans la session, pour tout le module M02
CREATE OR REPLACE VIEW lignes_ventes AS
  SELECT * FROM read_csv('01_socle_donnees/data/reference/ventes_magasin5_2025_ATTENDU.csv', sep=';');

CREATE OR REPLACE VIEW paniers AS
  SELECT n_ticket, SUM(montant_ttc) AS panier, COUNT(*) AS nb_lignes
  FROM lignes_ventes
  GROUP BY n_ticket;
```

Un `CREATE VIEW` ne duplique pas les données : il enregistre une question. Vous gagnez trois choses — des requêtes
courtes, un point unique où le fichier est nommé, et un signal immédiat le jour où le fichier change de nom ou de
séparateur, parce que la vue refusera de se créer. Vérifiez une fois, tout de suite : `SELECT COUNT(*),
ROUND(AVG(panier)) FROM paniers;` doit rendre 316 et 114 156.

**Étape 7 — La version Python, et la moyenne pondérée.**

```python
import pandas as pd
d = pd.read_csv("01_socle_donnees/data/reference/ventes_magasin5_2025_ATTENDU.csv", sep=";")
pan = d.groupby("n_ticket").montant_ttc.sum()
print(pan.agg(["count", "mean", "median", "min", "max"]))
pond = (d.remise * d.montant_ht.abs()).sum() / d.montant_ht.abs().sum()
print("remise simple %.4f · pondérée %.4f" % (d.remise.mean(), pond))
```

Sortie attendue : 316 tickets · moyenne 114 156 · médiane 58 423 · -150 804 · 1 343 666 ; remise 0,0185 et
0,0172. Les trois outils tombent d'accord, la note est défendable.

**Étape 8 — Les catégories, sans y passer la journée.** `GROUP BY categorie` sur les lignes : moyenne et médiane
par catégorie, en une colonne de plus. Bois & panneaux donne 201 865 FCFA de moyenne pour 77 904 FCFA de médiane :
cette catégorie est tirée par ses gros chantiers. Peinture : 86 422 contre 68 738 — les deux sont proches, la
distribution est régulière. Voilà comment, en trente secondes, un classement de catégories devient une
interprétation.

**Étape 9 — Écrire le commentaire.** Deux phrases, pas plus : une sur la position (« le panier médian est à
58 423 FCFA »), une sur la concentration (« la moyenne, 114 156 FCFA, est tirée par 10 % de tickets qui font
47,5 % du CA »).

**Étape 10 — Journaliser.** Une ligne dans `06_analyse/journal_transformations.txt` : la source, les six
nombres, l'outil, la date. Ce qui prend vingt secondes aujourd'hui vous évitera trois quarts d'heure de fouille
en janvier.

---

## 8. Erreurs fréquentes

| Symptôme | Cause | Correction |
|---|---|---|
| « Notre client moyen » n'existe nulle part | la moyenne prise pour le cas typique | citer moyenne **et** médiane, et dire laquelle porte la décision |
| La moyenne change quand on ajoute une ligne, la décision change avec | aucun contrôle de la forme de la distribution | regarder le rapport moyenne/médiane avant de commenter ; ici 1,95 |
| Le mode affiché est une valeur unique apparue deux fois | mode calculé sur une colonne quasi continue | réserver le mode aux variables qualitatives ou aux colonnes à faible cardinalité |
| Deux services n'ont pas la même moyenne, aucune erreur de calcul | périmètres différents (retours, doublons, extrait) | nommer le périmètre dans l'intitulé de la cellule, pas en note de bas de page |
| `=MEDIANE()` renvoie une erreur ou un texte | valeurs non numériques dans la plage | `=NB()` contre `=NBVAL()` ; la différence compte les lignes texte |
| L'étendue explose après un correctif | minimum négatif non expliqué (retour) | séparer retours et ventes avant de résumer, et le dire |

---

## 9. Bonnes pratiques professionnelles

- Un centre sans effectif n'est pas une statistique : `114 156 FCFA (n = 316 tickets)`, toujours.
- Citez l'unité et la période dans le nom de la colonne du tableau, pas dans la légende du graphique.
- Sur des montants, partez du principe que la moyenne sera au-dessus de la médiane ; vérifiez, et commentez le rapport.
- Ne supprimez jamais un extrême sans écrire la règle, le nombre de lignes retirées et le total perdu.
- Pour une variable à 4 ou 5 valeurs (un vendeur, un type de client), le mode et l'effectif par modalité disent plus qu'une moyenne.
- Gardez une colonne « moyenne pondérée » dans vos modèles quand la variable est un taux ou un prix.
- Conservez dans le journal la requête qui a produit les nombres : une note sans requête est une opinion datée.

---

## 10. Exercice guidé — le trio moyenne / médiane / mode, ensemble

**Consigne.** Sur la série des 316 paniers, produisez le tableau des six nombres, puis écrivez les deux phrases
de commentaire. Comptez 30 minutes, dont 20 de tableur.

**Étape 1 — Isoler la série.** Vous sommez par ticket et vous ne gardez qu'une occurrence par ticket, comme en §7
étape 2. Contrôle : `=NB()` sur la colonne obtenue doit faire 316. Si vous trouvez 480, la déduplication n'a pas
fonctionné et tout ce qui suit sera faux — c'est le moment de le découvrir, pas après la note.

**Étape 2 — Les six nombres.** Vous les placez dans un tableau à trois colonnes : indicateur, valeur, unité. Vous
obtenez 114 156 · 58 423 · 6 797 · -150 804 · 1 343 666 · 1 494 470 FCFA.

**Étape 3 — Le mode, et sa mise à l'écart.** Le tableur renvoie 6 797 FCFA, et la fonction des modes multiples en ajoute un second à 8 260 FCFA. Vous
demandez « combien de fois ? » : `=NB.SI()` répond trois fois sur 316, pour l'un comme pour l'autre. Décision écrite : mode non retenu, avec sa raison. C'est une
compétence, pas une résignation.

**Étape 4 — Le rapport qui parle.** `=114156/58423` → 1,95. Commentaire : « la moyenne est près de deux fois la
médiane : la recette est concentrée ». Vous cherchez la concentration : triez décroissant, additionnez les 32
premiers tickets (10 % de 316 arrondi), divisez par le total → 47,5 %. Voilà l'indicateur que le directeur gardera
en tête, pas le panier moyen.

**Étape 5 — Le retournement.** Refaites la moyenne en excluant le plus gros ticket : vous voyez la moyenne
descendre nettement, la médiane presque pas. Écrivez cette phrase dans la note : elle explique à elle seule
pourquoi deux services peuvent avoir raison avec des chiffres différents.

**Étape 6 — Vérification croisée.** Relancez la requête SQL de l'étape 6. Les six nombres doivent être identiques
au franc près (aux arrondis d'affichage près). S'ils diffèrent, c'est l'encodage ou le séparateur, pas la
statistique.

---

## 11. Exercices autonomes

**Exercice 2.1 (★) — Le tableau de base.** Calculez les six nombres de la série des paniers, et le même tableau
pour la colonne `montant_ttc` par ligne. *(attendu : 114 156 · 58 423 · 6 797 · -150 804 · 1 343 666 · 1 494 470
FCFA ; par ligne 75 152 · 37 966 FCFA, minimum -150 804, maximum 1 229 678)*

**Exercice 2.2 (★) — Combien sous la moyenne.** Comptez les tickets strictement inférieurs à la moyenne, donnez
leur part. Concluez en une phrase sur l'expression « client moyen ». *(attendu : 227 tickets sur 316, 71,8 %)*

**Exercice 2.3 (★★) — Simples contre composés.** Séparez les 212 tickets d'une ligne des 104 autres ; moyenne et
médiane de chaque groupe. Rédigez la phrase que vous diriez au directeur des ventes. *(attendu : 80 546 / 38 084
FCFA et 182 668 / 130 461 FCFA ; conclusion : deux clientèles, un seul fichier)*

**Exercice 2.4 (★★) — Pondérée, pas simple.** Moyenne simple et moyenne pondérée par le `montant_ht` de la
colonne `remise`, puis la même paire restreinte aux lignes dont la catégorie est « Matériaux ». Expliquez ce que
dit la différence. *(attendu sur l'ensemble : 0,0185 et 0,0172 ; la pondérée est inférieure : les fortes lignes
sont moins remisées)*

**Exercice 2.5 (★★★) — Le chiffre qui change sans raison.** Recalculez la moyenne des paniers en incluant les
lignes de retour (montants négatifs), puis en les isolant dans un segment « avoirs ». Donnez les deux moyennes, la
médiane dans les deux cas, et écrivez la règle métier que vous avez suivie. *(attendu : la moyenne baisse quand
on inclut les retours, la médiane quasiment pas ; règle écrite = les retours ne sont pas des ventes, ils sont un
objet à part, et le total reste celui de la caisse)*

---

## 12. Correction détaillée

**Exercice 2.1.** Tableaux attendus, avec l'effectif affiché à chaque ligne : paniers *n* = 316 — moyenne
114 156, médiane 58 423, modes 6 797 et 8 260 (non retenus : 3 occurrences chacun), min -150 804, max 1 343 666, étendue 1 494 470 FCFA ; lignes
*n* = 480 — moyenne 75 152, médiane 37 966 FCFA. Contrôle d'additivité sur les lignes : la moyenne multipliée par l'effectif doit retomber sur le total de
la colonne, 36 073 185 FCFA, à l'arrondi d'affichage près — c'est la raison pour laquelle on calcule avec
deux décimales et on affiche en entiers.

**Exercice 2.2.** `=NB.SI(O:O;"<114156")` → 227, soit 227 ÷ 316 = 71,8 %. Commentaire attendu : « dans une
distribution asymétrique, la majorité des observations est sous la moyenne ; parler de "client moyen" pour décrire
le client courant est un contresens — le client courant est à 58 423 FCFA ». Le point de méthode noté : avoir
vérifié que 316 − 227 = 89 tickets sont au-dessus (les 28,2 % qui portent la recette), et l'avoir écrit.

**Exercice 2.3.** Moyennes 80 546 et 182 668 FCFA ; médianes 38 084 et 130 461 FCFA. Ratio interne : dans le
groupe des tickets simples, la moyenne est 2,11 fois la médiane — le déséquilibre n'a pas disparu en découpant, il
s'est déplacé. Phrase attendue : « le panier moyen de 114 156 FCFA mélange deux objets : un achat simple à
80 546 FCFA et un panier composé à 182 668 FCFA ; si l'objectif est de faire passer un client d'un article à
plusieurs, l'indicateur de pilotage est la part des tickets composés (32,9 %), pas le panier moyen ».

**Exercice 2.4.** Ensemble : simple 0,0185, pondérée 0,0172 (formule `=SOMMEPROD(remise;|montant_ht|)/SOMME(|montant_ht|)`).
Sur « Matériaux » : les deux se resserrent, la catégorie étant peu remisée et de montants homogènes. Lecture
attendue : « la moyenne simple surestime la remise réelle de 1,3 point relatif, parce que les petites lignes sont
les plus remisées ; la politique de remise touche donc les petits clients, pas les chantiers ». Cette phrase est
une décision possible : baisses de remise sur les petites lignes, marge préservée.

**Exercice 2.5.** Avec retours inclus, la moyenne des paniers est celle annoncée (§5.2) : 114 156 FCFA — elle
contient trois tickets négatifs, dont un à -150 804 FCFA. En isolant les avoirs, la moyenne des ventes se
resserre et la médiane reste à 58 423 FCFA, pratiquement inchangée : la médiane ne « voit » pas les trois cas
extrêmes, la moyenne les absorbe. Règle attendue, écrite en une phrase : « un avoir n'est pas une vente : il est
compté à part, et le total de caisse reste le total de caisse ». Le barème valorise la règle, pas le calcul.

---

## 13. Mini-projet M02.P2 — « Deux pages, six nombres, une décision » (45 min)

**Commande.** Pour la direction commerciale du magasin 5, produisez deux pages : (1) le tableau des six nombres,
sur les paniers et sur les lignes, avec effectifs, unités et périmètre ; (2) une page de décision qui utilise
moyenne, médiane et concentration pour trancher **une** question au choix : faut-il augmenter le seuil de
livraison gratuite ? faut-il un tarif dédié aux tickets au-dessus de 300 000 FCFA ? faut-il recentrer la remise
sur les petites lignes ?

**Livrables numérotés.** (1) tableau ; (2) page de décision avec le chiffre retenu, celui qui est écarté et
pourquoi ; (3) la requête SQL ou le classeur de calcul en annexe ; (4) la ligne de journal.

**Barème (20 points, seuil 13).** Six nombres exacts et sourcés (5) · périmètre et unité écrits partout (3) ·
choix du centre justifié par la forme, pas par l'habitude (4) · chiffre de concentration calculé et non recopié
(3) · décision datée avec un destinataire (3) · annexe rejouable (2) — total 20.

---

## 14. Résumé du chapitre

Trois centres, trois usages : la moyenne porte l'argent et se multiplie par l'effectif pour retrouver le total ;
la médiane porte les gens et résiste aux extrêmes ; le mode ne sert que sur du discret. Deux bornes et une
étendue disent l'étalage, pas la fréquence : le minimum de notre série est négatif parce que les retours sont là,
et le maximum est un chantier, pas un client. Le rapport moyenne/médiane est votre premier diagnostic de forme —
ici 1,95, donc asymétrie marquée, donc 71,8 % des tickets sous la moyenne. La moyenne pondérée est obligatoire
dès qu'une variable est un taux ou un prix. Enfin, aucun centre ne se cite sans effectif, unité, période et
périmètre : c'est ce qui rend un chiffre défendable quand deux services le calculent chacun de leur côté.

---

## 15. À retenir

> **À retenir.**
> 1. **Moyenne × effectif = total** : c'est sa définition et sa seule promesse. Ne lui demandez pas de décrire le
>    cas courant.
> 2. **Médiane = la moitié, pas le milieu du total** : 58 423 FCFA ici, insensible au ticket géant de
>    1 343 666 FCFA.
> 3. **Regardez le rapport, pas les valeurs seules** : moyenne ÷ médiane = 1,95 annonce la concentration
>    (47,5 % du CA sur 10 % des tickets).
> 4. **Mode uniquement sur du discret** : 6 797 FCFA est une valeur, pas une information.
> 5. **Taux et prix → moyenne pondérée** : 1,72 % de remise réelle contre 1,85 % de moyenne simple.

> **À retenir.** La formulation qui protège. Dans toute note : « moyenne *X* FCFA, médiane *Y* FCFA, sur *n*
> *objets*, périmètre *…* ». Celui qui écrit cette ligne ne se fait plus reprendre sur le sens d'un chiffre.

---

## 16. Évaluation formative (auto-correction, 10 min)

1. Un tableau de bord affiche « panier moyen : 114 156 FCFA » et « panier médian : 58 423 FCFA ». Un directeur
   conclut : « la moitié de nos clients dépensent plus de 100 000 FCFA ». Qu'y a-t-il à reprendre ?
2. Calculez de tête le nombre de tickets sous la moyenne si 28,2 % sont au-dessus, et dites ce que ce déséquilibre
   implique pour une politique de prix.
3. Pourquoi le mode est-il écarté de ce chapitre sur la colonne des montants, et sur quelle colonne du même fichier
   serait-il pertinent ?
4. Moyenne simple 0,0185, moyenne pondérée 0,0172. Lequel des deux chiffres un directeur financier doit-il
   entendre, et lequel un chef de magasin ?
5. On retire les 25 tickets dépassant la borne de 295 445 FCFA. Que deviennent la moyenne, la médiane et le
   total ? Lequel de ces trois changements doit être signalé dans la note ?

---

**Corrigé de l'évaluation formative.**

1. Deux erreurs. D'abord une confusion de centre : la médiane (58 423 FCFA) est le seuil de la moitié, pas la
   moyenne. Et le seuil des 100 000 FCFA n'est pas
   davantage une moitié : 30,4 % des tickets le dépassent (96 tickets sur 316), 28,2 % dépassent la moyenne.
2. 316 × (1 − 0,282) ≈ 227 tickets sous la moyenne. Conséquence : fixer un tarif ou un seuil de service « sur la
   moyenne » exclut sept tickets sur dix ; les paliers se calibrent sur des percentiles (chapitre 4).
3. Parce que 316 montants presque tous distincts produisent un mode sans signification : deux valeurs, 6 797 et
   8 260 FCFA, trois occurrences chacune. Sur `categorie` ou `remise`, le mode est utile : « Matériaux » avec 143 lignes sur 480, ou remise
   0,04 avec 110 lignes sur 480.
4. Le directeur financier entend la **pondérée** (1,72 %), parce qu'elle dit ce que coûte la remise sur chaque
   franc facturé. Le chef de magasin entend la **simple** (1,85 %), parce qu'elle dit ce qui se pratique sur une
   ligne — et donc ce qu'il doit rappeler aux vendeurs.
5. La moyenne baisse nettement (vers 71 463 FCFA sur les tickets restants), la médiane descend à 54 044 FCFA, le
   total du fichier, lui, baisse de tout ce qui a été retiré. C'est **le total** qui doit être signalé : une
   moyenne sans extrêmes est un outil de description, pas un élément de compte de résultat ; écrire l'un sans
   l'autre, c'est créer un chiffre que la comptabilité ne reconnaîtra pas.
