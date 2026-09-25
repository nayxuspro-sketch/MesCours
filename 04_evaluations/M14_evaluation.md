# Évaluation M14 — « Power BI : de l'import à la publication »

**Module : M14 · 80 points · seuil de réussite 51 · environ 3 h · barème : quiz 20 · exercices 24 ·
étude de cas 30 · auto-évaluation 6.** Un instrument séparé, la **grille de conception en 18 points**,
se remplit en plus des 80 points — elle est notée à part et sert à la revue par un pair.

**Ce qui est évalué.** Cinq compétences du module, dans l'ordre où les chapitres les ont construites :
importer et transformer la donnée, déclarer un modèle étoile, écrire des mesures justes, dessiner des
visuels qui se lisent, et publier un rapport qui tient en production.

**Les outils.** DuckDB **exécuté** ; Power BI Desktop et le Service **cités** et non installés dans
l'atelier (règle §1.5). Les questions qui portent sur l'outil se répondent donc par écrit, en décrivant
les gestes et les valeurs de contrôle — jamais par une capture d'écran.

---

## A · Questions de récupération (non notées)

Répondez de mémoire, en une ligne, avant de commencer. Ces questions servent à retrouver les ordres de
grandeur du module ; elles ne sont pas notées.

1. Combien de tables le modèle du rapport importe-t-il, et combien de lignes en tout ?
2. Quelles sont les deux valeurs qui encadrent le panier moyen — par ticket et par ligne ?
3. Pourquoi la rotation des stocks n'est-elle pas filtrable par magasin ?
4. Combien de visuels portent les trois pages de fond du rapport, et comment se répartissent-ils ?
5. Quelles fonctions DAX emploie-t-on pour compter des tickets distincts et pour diviser sans erreur ?

---

## B · Quiz (15 questions · 20 points)

### Bloc 1 — Définir (Q1 à Q5, **1** point chacune)

**Q1.** Un rapport affiche le même jour deux chiffres différents sur deux pages : les totaux sont plus
élevés sur la seconde. Quel est l'ordre des vérifications ?

**Q2.** Qu'est-ce qui distingue un modèle **Import** d'un **DirectQuery**, en une phrase, du point de vue
du lecteur ?

**Q3.** Qu'est-ce qu'une colonne **masquée** dans un modèle, et pour quoi fait-elle ce qu'elle fait ?

**Q4.** Qu'est-ce qu'un **signet** dans un rapport ?

**Q5.** Qu'est-ce que la **sécurité au niveau des lignes**, et sur quoi s'applique-t-elle ?

### Bloc 2 — Mesurer (Q6 à Q10, **1** point chacune)

**Q6.** Le taux de rupture du rapport vaut **7,29 %**. Citez les deux populations qui composent ce taux,
et la phrase qui manque à côté du visuel.

**Q7.** Le panier moyen du réseau vaut **107 396** FCFA. À quoi ressemblerait-il filtré sur une famille,
et pourquoi le chiffre ne se compare-t-il plus au premier ?

**Q8.** Une jauge graduée de 0 à 100 % sur une mesure qui atteint **259,1 %** : quelles sont les trois
issues acceptables ?

**Q9.** Un rapport de cinq visuels s'ouvre en quelques millisecondes par visuel, mais la page du voisin
met quarante secondes. Citez deux causes probables et la mesure qui tranche.

**Q10.** La table de stock ne peut pas être filtrée par magasin. Dites la conséquence, et les deux
décisions possibles.

### Bloc 3 — Construire (Q11 à Q15, **2** points chacune)

**Q11.** Écrivez la mesure du chiffre d'affaires net et celle du panier moyen, en indiquant pourquoi la
seconde emploie `DISTINCTCOUNT` et `DIVIDE`.

**Q12.** Un rapport a deux pages de détail et une page d'aide. Décrivez ce que la synchronisation des
segments doit faire de la page d'aide, et pourquoi.

**Q13.** Une matrice magasin × famille affiche **42** cases, dont **7** vides. Rédigez la légende des
vides et la ligne du dossier qui justifie un zéro écarté.

**Q14.** Décrivez les **7** tests de mise en production, dans l'ordre où vous les passeriez.

**Q15.** Vous recevez le retour « ajoutez le chiffre d'affaires par heure de la journée ». Rédigez la
réponse professionnelle : le constat, la raison, la sortie.

---

## C · Quatre exercices (24 points)

| Exercice | Objet | Points |
|---|---|---|
| **E1** | Contrôler un modèle et ses relations | **6** |
| **E2** | Choisir et régler un visuel | **6** |
| **E3** | Écrire le périmètre d'un taux | **6** |
| **E4** | Diagnostiquer un total doublé | **6** |
| **Total** | | **24** |

### E1 — Contrôler un modèle et ses relations (6 points)

Le modèle du projet contient **12** relations actives et **2** inactives. Trois contrôles sont exigés :
l'unicité de la clé de chaque dimension, le sens du filtre de chaque relation, et la justification des
**2** inactives. Livrez le tableau des **12** relations — table de faits, dimension, cardinalité, sens,
active ou non — et, pour chaque relation inactive, la phrase qui explique pourquoi elle est inactive et
quelle mesure l'utilise. **Attendu : 12 relations justes, 2 inactives expliquées, 0 relation
dupliquée.**

### E2 — Choisir et régler un visuel (6 points)

Quatre questions, quatre visuels à choisir et à régler : « où va l'activité du réseau ? », « quels
magasins font le chiffre d'affaires ? », « comment évolue-t-on mois par mois ? », « où manque-t-on de
stock ? ». Pour chacun : le type de visuel, la mesure, le tri, l'échelle, l'unité, la période, et la
décision qu'il sert. **Attendu : le type se déduit de la question, et l'échelle est justifiée par les
valeurs — de **11,1 %** à **34,1 %** pour les parts des magasins, **199 549 035** à **533 572 353** FCFA
pour la courbe mensuelle.**

### E3 — Écrire le périmètre d'un taux (6 points)

Rédigez la fiche de publication du taux de rupture : définition, numérateur, dénominateur, exclusions,
période, et la phrase qui accompagne le visuel. Puis réconciliez les deux lectures du chiffre —
**7,29 %** pour le rapport, **6,03 %** à périmètre égal — en nommant les lignes qui font l'écart.
**Attendu : les deux populations écrites, l'écart chiffré, et le choix de publication justifié en une
phrase.**

### E4 — Diagnostiquer un total doublé (6 points)

Une page affiche **31 190 309 910** FCFA là où la recette du socle donne **15 595 154 955** FCFA. Les
mesures sont correctes, les filtres sont vides, et la page affiche exactement le double. Décrivez la
démarche de diagnostic — par où vous commencez, ce que vous comptez, ce que vous concluez —, nommez la
cause, et écrivez la correction. **Attendu : la cause trouvée dans le modèle et non dans les mesures, le
compte de lignes qui le prouve, et la correction écrite.**

---

## D · Étude de cas — « le client ne comprend pas le tableau de bord » (30 points · seuil 18)

### La commande

Un client de Sahel Distribution reçoit le tableau de bord commercial publié au trimestre dernier. Trois
semaines plus tard, il écrit ceci, mot pour mot :

> « Votre rapport dit que je vends **34,1 %** du réseau. Mon comptable dit **29 %**. Sur la page des
> stocks, je vois un chiffre qui ne bouge pas quand je choisis mon magasin. Le mardi matin, le chiffre
> d'affaires de la semaine n'est jamais le même que celui du lundi soir. Et je ne comprends pas pourquoi
> mon panier moyen change quand je clique sur une famille de produits. »

### Ce qui est demandé

1. **Le diagnostic** : pour chacune des quatre remarques, la cause probable, la vérification qui la
   confirme, et la définition ou le réglage à corriger.
2. **Le dossier de réponse** : une note au client, lisible par un non-technicien, qui explique chaque
   point en deux ou trois phrases, sans jargon et sans excuse.
3. **La décision de conception** : ce qui se corrige dans le rapport, ce qui se corrige dans la
   documentation, et ce qui se refuse — avec la raison.

### Le résultat attendu (à retrouver, pas à recopier)

- La part du premier magasin est **34,1 %** du réseau ; l'écart avec le comptable vient le plus souvent
  d'un **périmètre** différent — retours inclus ou exclus, dépôt compté ou non — et il se tranche en
  écrivant la définition, pas en changeant le chiffre.
- La page des stocks affiche la **rotation**, et la table qui la porte — **6 776** lignes de produit ×
  mois — ne porte aucun magasin : le filtre de sécurité et le filtre de page n'ont rien à filtrer. Deux
  décisions possibles : garder l'indicateur au niveau du réseau et le dire, ou descendre la colonne
  magasin dans la table.
- Deux chiffres différents le lundi soir et le mardi matin signalent une **actualisation** : fréquence,
  heure, et ce qui se passe en cas d'échec. Le rapport doit afficher la date de la dernière actualisation
  réussie.
- Le panier moyen change quand on clique sur une famille parce que le **dénominateur** suit le filtre :
  le panier d'une famille n'est pas une part du panier du réseau. Les **7** familles totalisent
  **215 995** tickets pour **145 212** tickets distincts : deux pourcentages calculés sous deux filtres
  ne s'additionnent ni ne se moyennent.

### Barème de l'étude de cas

| Critère | Points |
|---|---|
| Diagnostic des quatre remarques, cause et vérification | **10** |
| Note au client, lisible et sans jargon | **8** |
| Décisions de conception : corriger, documenter, refuser | **8** |
| Chiffres justes et sourcés dans le dossier | **4** |
| **Total** | **30** |

Le seuil de l'étude de cas est fixé à **18** points sur **30** : une réponse qui trouve les causes mais
n'écrit aucune décision ne l'atteint pas.

---

## E · Auto-évaluation (6 points)

Notez-vous honnêtement, un point par item tenu, et indiquez la preuve pour chacun :

1. je sais **importer, transformer et relier** les tables du rapport sans aide ;
2. je sais **écrire une mesure** avec sa fiche — nom, question, haut, bas, format, chiffre de contrôle ;
3. je sais **choisir un visuel** à partir de la question, et régler son échelle sur les valeurs ;
4. je sais **écrire le périmètre** d'un taux, et reconnaître un pourcentage qui ne s'additionne pas ;
5. je sais **publier** : droits, actualisation, alertes, et les **7** tests de mise en production ;
6. je sais **répondre à un retour** d'utilisateur : faire, reformuler, ou refuser par une mesure.

---

## F · La grille de conception en 18 points (instrument séparé, hors des 80 points)

La grille se remplit **deux fois** : par l'auteur avant publication, puis par un pair qui n'a pas
construit le rapport. Elle ne s'ajoute pas aux 80 points : elle conditionne la publication.

| Famille | Points | Ajouts du module |
|---|---|---|
| **1. La décision servie** | **4** | aucun |
| **2. La justesse** | **5** | cohérence des totaux · granularité · gestion des vides |
| **3. La lisibilité** | **5** | accessibilité · légende |
| **4. L'utilisation** | **4** | performance |
| **Total** | **18** | **6** sous-questions ajoutées, sans changer le total |

---

## Correction détaillée

### A · Réponses de récupération

1. **12** tables, **293 120** lignes. 2. **107 396** FCFA par ticket, **65 749** FCFA par ligne.
3. Parce que la table qui porte la rotation ne porte pas de magasin : **6 776** lignes de produit × mois,
   sans `id_magasin`. 4. **14** visuels : **5** + **5** + **4**. 5. `DISTINCTCOUNT` pour compter les
   tickets distincts, `DIVIDE` pour diviser sans erreur.

### B · Corrigé du quiz

**Q1.** Vérifier d'abord si les deux pages lisent la **même** table de faits, puis si l'une d'elles
filtre les retours, puis si une relation est dupliquée ou active des deux côtés : un écart de totaux
entre deux pages vient du modèle ou d'une définition, jamais d'un arrondi. **Q2.** En **Import**, le
lecteur travaille sur une copie locale, disponible hors ligne et aussi fraîche que la dernière
actualisation ; en **DirectQuery**, chaque affichage interroge la source, donc la donnée est vivante mais
le rapport dépend du réseau et de la source. **Q3.** Une colonne masquée existe dans le modèle mais
n'apparaît pas dans le volet des champs : elle sert aux relations, au tri et aux clés techniques — le
rapport ne propose donc pas au lecteur une colonne qui n'a pas de sens pour lui. **Q4.** Un signet est un
état mémorisé du rapport — page, filtres, visuels visibles — rappelé par un bouton : les **4** signets du
rapport couvrent vue d'ensemble, focus magasin, détail produit et aide. **Q5.** C'est le filtre qui
restreint les lignes visibles par un lecteur donné ; il s'applique au **modèle**, pas au visuel, et il se
vérifie table par table.

**Q6.** **2 428** couples produit-magasin-mois en rupture d'un côté, **33 323** couples servis de
l'autre — mais le numérateur couvre **6** magasins et le dénominateur **5**, le dépôt central portant
**418** ruptures sans aucune vente. La phrase manquante dit le périmètre : « dépôt central inclus »
(**7,29 %**) ou « magasins qui vendent seuls » (**6,03 %**). **Q7.** Filtré sur une famille, le panier
devient celui des tickets de cette famille : de **40 879** FCFA en quincaillerie à **128 958** FCFA en
plomberie. Il ne se compare plus au panier du réseau parce que la **population** a changé, pas la
formule — **5** familles sur **7** sont sous la moyenne du réseau. **Q8.** Régler le maximum sur la
donnée — jusqu'à **300 %** —, ajouter une cible à **100 %** pour que le dépassement se voie, ou changer
de visuel pour une barre avec repère d'objectif ; laisser une aiguille en butée n'en fait pas partie.
**Q9.** Deux causes probables : trop de visuels sur la page, ou une mesure lourde recalculée à chaque
affichage — et un mode de connexion inadapté à la source. La mesure qui tranche est un chronomètre par
visuel dans l'outil ; sur le socle du module, une carte coûte **1** ms et la matrice **4** ms.
**Q10.** La conséquence : la rotation affichée est celle du réseau entier, pour tous les lecteurs, quel
que soit leur rôle. Deux décisions : garder l'indicateur comme indicateur de réseau — et le dire —, ou
descendre `id_magasin` dans la table de stock et refaire le modèle pour ce besoin.

**Q11.** `[CA net] = CALCULATE(SUM(fait_ventes[montant_ttc]), fait_ventes[est_retour] = 0)` et
`[Panier moyen] = DIVIDE([CA net], DISTINCTCOUNT(fait_ventes[id_ticket]))`. `DISTINCTCOUNT` parce que la
question porte sur la visite, et qu'un ticket contient plusieurs lignes — **237 191** lignes pour
**145 212** tickets : les compter en lignes donnerait **65 749** FCFA au lieu de **107 396**. `DIVIDE`
parce qu'un dénominateur peut être nul — **44** des **264** combinaisons magasin × mois du socle sont
vides — et qu'un rapport qui affiche une erreur perd son lecteur. **Q12.** La synchronisation doit
**exclure** la page d'aide : une page de définitions qui change avec un filtre de données n'est plus une
définition, et deux lecteurs y liraient deux contenus — c'est exactement ce qu'une page d'aide doit
empêcher. **Q13.** Légende : « une case blanche signale une famille non référencée dans ce magasin ;
aucune vente n'existe sur cette combinaison ». Un zéro serait un contresens parce qu'il affirme une
mesure nulle là où il n'y a aucune ligne : il ferait croire à une demande insatisfaite — **7** cases sur
**42** — et enverrait le comité chercher une cause commerciale à un trou de référencement. **Q14.**
Totaux aux trois niveaux · grain affiché · vides expliqués · dates cohérentes · deux définitions
déclarées · ouverture mesurée sous trois secondes · relecture par un pair avec la grille en **18**
points. **Q15.** Le constat : le chiffre d'affaires horaire n'existe pas dans le socle, la table de
ventes portant une date sans heure. La raison : une donnée absente ne s'invente pas — l'estimer
produirait **24** chiffres faux par jour. La sortie : la demande est refusée pour ce trimestre, et elle
est transmise comme besoin de collecte — un horodatage à la caisse — avec une échéance écrite.

### C · Corrigé des quatre exercices

**E1.** Le tableau attendu porte les **12** relations : **5** partant des ventes (magasin, produit,
client, vendeur, date), **3** des commandes, **2** des encaissements, **2** des ruptures ; chaque
dimension a une clé unique, et le filtre va du côté « un » vers le côté « plusieurs ». Les **2**
inactives se justifient par une seconde relation entre les mêmes tables — deux dates d'un même fait, par
exemple — et chaque inactive est employée par au moins une mesure ou une intention écrite. Un modèle qui
déclare une relation au hasard produit un total faux, pas une erreur visible.

**E2.** « Où va l'activité du réseau ? » : une carte du chiffre d'affaires net — **15 595 154 955** FCFA —
et la courbe mensuelle, qui porte la tendance. « Quels magasins font le chiffre d'affaires ? » : des
barres **ordonnées**, de **34,1 %** à **11,1 %**, parce que le classement est le message. « Comment
évolue-t-on mois par mois ? » : la même courbe, axe partant de zéro, **44** mois, de **199 549 035** à
**533 572 353** FCFA. « Où manque-t-on de stock ? » : des barres de rupture par famille, et la matrice
magasin × mois ; le nuage couverture × rotation sert la décision d'approvisionnement, pas le classement.

**E3.** Fiche : définition — part des couples produit-magasin-mois servis ayant connu au moins un jour de
rupture ; numérateur — **2 428** couples en rupture ; dénominateur — **33 323** couples servis ;
exclusions — aucune ; période — les **44** mois du socle. La phrase du visuel : « dépôt central inclus
dans les ruptures, non compté dans les couples servis ». Réconciliation : l'écart vient des **418**
ruptures du dépôt — **17,2 %** du total — et le taux à périmètre égal tombe à **6,03 %**. Le choix de
publication est défendable dans les deux sens ; ce qui ne l'est pas, c'est de publier **7,29 %** sans la
phrase.

**E4.** Démarche : partir de la mesure — elle est juste — puis **compter les lignes** de la table de
faits avant de regarder le total. Le socle en porte **240 000** ; une table qui en compte **480 000**
signale deux copies de la même source. La cause : deux requêtes pointant sur le même fichier, deux tables
dans le modèle, deux relations actives, chaque ligne de vente existant deux fois — le total passe à
**31 190 309 910** FCFA, soit exactement **2,00** fois le chiffre juste. La correction : supprimer la
seconde requête, ou la transformer en référence plutôt qu'en copie, puis refaire la recette et la
comparer au contrôle **15 595 154 955** FCFA. Un total doublé ne vient jamais d'une mesure : il vient du
modèle, et il se trouve en comptant les lignes.

### D · Corrigé de l'étude de cas

Le diagnostic attendu, remarque par remarque : **la part du magasin** — vérifier le périmètre du
dénominateur, retours et dépôt, avant de toucher au chiffre ; **la page des stocks** — constater que la
table de rotation ne porte pas de magasin — **6 776** lignes produit × mois — et décider si l'indicateur
reste un indicateur de réseau ; **les deux chiffres du lundi et du mardi** — vérifier la fréquence et
l'heure de l'actualisation, et afficher la date de la dernière actualisation réussie ; **le panier
moyen** — expliquer que **7** familles totalisent **215 995** tickets pour **145 212** tickets distincts,
donc qu'un panier par famille n'est pas une part du panier du réseau. La note au client reprend ces
quatre points sans jargon, dit ce qui se corrige dans le rapport, ce qui se corrige dans la
documentation — la définition des taux, la mention du périmètre — et ce qui se refuse : publier un
pourcentage par famille additionnable, par exemple, parce que cela produirait un total faux de plus.

### E · Corrigé de l'auto-évaluation

L'auto-évaluation ne se corrige pas : elle se **prouve**. Un point n'est acquis que si vous pouvez
montrer la pièce — la mesure avec sa fiche, le visuel avec sa question, la fiche de publication du taux,
le dossier de mise en production. Un item coché sans pièce vaut zéro, et c'est la règle la plus utile de
cette page : dans un projet réel, personne ne vous croira sur parole, et vous demanderez la même chose à
vos collègues.

### F · Corrigé de la grille

La grille se remplit par la réponse à **18** questions fermées. Deux façons de la rater, toutes deux
fréquentes : répondre « oui » partout — une grille sans aucun « non » n'a pas été remplie sérieusement —,
et la remplir seul. Le second passage, par un pair qui n'a pas construit le rapport, est celui qui
trouve : le titre qui ne dit rien, l'unité absente, la case vide non expliquée, la légende manquante. Les
**6** ajouts du module — cohérence des totaux, granularité, gestion des vides, accessibilité, légende,
performance — sont les six questions qui manquaient à la grille héritée de M10.
