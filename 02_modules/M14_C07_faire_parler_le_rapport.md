# Module M14.C07 — Faire parler le rapport

**Outils : DuckDB 1.5.5 (exécuté) ; pandas (non requis). Power BI Desktop est *cité* — l'outil n'est pas
installé dans cet atelier (règle §1.5). Les filtres de ce chapitre sont **mesurés** sur le socle à chaque
exécution de `tools/mesures_M14.py`, section `filtres` : les deux côtés d'un taux sous filtre, la
profondeur d'exploration et le coût d'un visuel.**

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous savez :

1. **poser un filtre au bon niveau** — rapport, page ou visuel — et savoir ce qu'un filtre croisé
   ajoute sans qu'on l'ait demandé ;
2. **voir qu'un filtre change les deux côtés d'un taux** : le panier moyen du réseau vaut **107 396**
   FCFA, et il n'est le panier d'aucune des **7** familles, qui vont de **40 879** à **128 958** FCFA
   (**3,15** fois) ;
3. **repérer un changement de périmètre** : le taux de rupture affiché (**7,29 %**) compte **6** magasins
   au numérateur et **5** au dénominateur ; à périmètre égal, il tombe à **6,03 %** ;
4. **régler les interactions et l'exploration** : les **4** segments et leur synchronisation, le
   surlignage contre le filtrage, la descente du magasin (**5**) à la famille (**7**) puis au produit
   (**154**) ;
5. **écrire des info-bulles utiles et surveiller la performance** : une carte coûte **1** ms, la matrice
   **4** ms, et la même donnée relue depuis le fichier source environ **143** ms.

---

## 2. Pourquoi cette notion est importante

Un rapport sans filtre est une photographie ; un rapport filtrable est un instrument. C'est aussi
l'endroit où les chiffres se mettent à mentir **sans qu'aucun calcul ne soit faux** — le sujet le plus
coûteux du métier, et celui que ce chapitre mesure.

**Le premier mensonge est le dénominateur.** Ajoutez un segment « famille » sur le rapport : le panier
moyen devient un panier **par famille**, calculé sur les tickets de cette famille seulement. Les
**7** familles totalisent **215 995** tickets quand le réseau n'en compte que **145 212** : **70 783**
tickets sont comptés deux fois ou plus, soit **48,7 %** de majoration. Personne n'a triché ; le
dénominateur a simplement suivi le filtre.

**Le deuxième est le périmètre.** Le taux de rupture du rapport vaut **7,29 %** — **2 428** couples en
rupture sur **33 323** couples servis. Mais le dépôt central, qui n'a aucune vente, porte **418** de ces
ruptures (**17,2 %**) et **zéro** couple servi. Le même mot — « taux de rupture » — décrit donc deux
choses selon le filtre posé, et rien dans le rapport ne le dit. Ce chapitre apprend à l'écrire.

**La troisième est le confort du lecteur.** Un rapport qui répond en trois clics se consulte ; un
rapport qui oblige à demander se contourne — quelqu'un ouvrira le fichier source, refera le calcul, et
les deux versions circuleront. Le coût d'un visuel, lui, est mesuré : **1** ms pour une carte, **4** ms
pour la matrice, **143** ms pour la même donnée relue à la source. La réactivité n'est pas un luxe
d'ingénieur, c'est ce qui décide si le rapport sera ouvert demain matin.

---

## 3. Explication simple — un filtre est une phrase

Un filtre est une phrase qu'on ajoute à la question. « Quel est le chiffre d'affaires ? » devient
« quel est le chiffre d'affaires **du magasin de Bobo** **sur les douze derniers mois** ». Trois
conséquences, faciles à retenir :

- la phrase **réduit** le périmètre : moins de lignes, un chiffre plus petit — sauf pour les
  pourcentages, qui ne suivent pas cette règle ;
- la phrase **change le sens** de certains indicateurs : un panier moyen par famille n'est pas une part
  du panier moyen du réseau ;
- la phrase **doit s'écrire** dans le rapport, sinon le lecteur croit lire un total alors qu'il lit une
  tranche.

Le test qui tranche tout : avant de publier un rapport filtrable, posez-vous la question « si un
collègue filtre sur un seul magasin, quels chiffres deviennent incomparables avec ceux d'hier ? ». Ce
qui apparaît dans la réponse doit être écrit sur la page d'aide.

---

## 4. Vocabulaire essentiel

| Terme | Ce qu'il désigne sur le fil rouge |
|---|---|
| **Filtre de rapport** | le filtre qui s'applique à toutes les pages : la période, par exemple |
| **Filtre de page** | le filtre qui ne quitte pas sa page : le magasin sur la page Commercial |
| **Filtre de visuel** | le filtre qui ne concerne qu'un dessin, souvent le plus mal placé |
| **Segment** | le contrôle visible posé sur la page : le rapport en porte **4** |
| **Synchronisation** | la règle qui rend un segment actif sur plusieurs pages — et jamais sur la page d'aide |
| **Surlignage** | l'interaction douce : le visuel voisin **met en évidence** la part concernée, sans la réduire |
| **Filtrage croisé** | l'interaction dure : le visuel voisin ne montre **que** la part concernée |
| **Exploration** | la descente de niveau : magasin, puis famille, puis produit |
| **Info-bulle** | l'encadré qui s'ouvre au survol, avec les valeurs qui expliquent le point |
| **Q&A** | la question posée en langage courant, traduite par l'outil en requête sur le modèle |
| **Dénominateur** | la population d'un taux — et la première victime d'un filtre mal expliqué |
| **Périmètre** | l'ensemble des lignes couvertes par un chiffre : **6** magasins au numérateur, **5** au dénominateur |
| **Performance** | le temps qu'un visuel met à s'afficher : **1** ms pour une carte, **4** ms pour la matrice |
| **Mode Import** | la copie locale des données : c'est elle qui rend ces temps possibles |

> **Définition.** Un **filtre** réduit l'ensemble des lignes sur lesquelles une mesure est évaluée. Il ne
> modifie jamais la définition de la mesure : c'est pourquoi deux lecteurs qui filtrent différemment
> obtiennent deux chiffres justes, et pourquoi un taux doit dire **sur quelle population** il porte.

> **Définition.** La **synchronisation** des segments est la règle qui décide sur quelles pages un
> segment agit. Elle se règle segment par segment, et elle se documente : un segment qui agit partout
> sans que personne ne l'ait décidé rend la page d'aide dépendante d'un filtre de données.

> **Définition.** L'**exploration** — *drill* — est la descente d'un niveau de détail à un autre :
> magasin, famille, produit. Chaque niveau a **son** dénominateur : le titre du visuel doit dire à quel
> niveau on se trouve, sans quoi deux lecteurs comparent deux niveaux différents.

---

## 5. Cours approfondi

### 5.1 Les trois niveaux de filtre, et celui qu'on choisit

Un filtre peut vivre à trois endroits, et le mauvais choix est une source d'incompréhension garantie :

| Niveau | Portée | Usage sur le fil rouge |
|---|---|---|
| **Rapport** | toutes les pages, toutes les visuels | la période d'analyse, quand tout le rapport parle du même mois |
| **Page** | la page seule | le magasin sur la page Commercial : la page parle d'un réseau |
| **Visuel** | un seul dessin | à éviter, sauf cas d'école : un filtre invisible sur un visuel isolé produit un chiffre que personne ne sait reproduire |

La règle tient en une phrase : **un filtre se pose au niveau le plus large qui convient à la question**.
Un filtre de visuel caché est la cause la plus fréquente des réunions où deux collègues ne trouvent pas
le même total en regardant le même rapport. Et si un filtre de visuel est indispensable, il s'écrit dans
le sous-titre du visuel — pas seulement dans le volet des filtres, que le lecteur ne voit pas.

### 5.2 Les 4 segments et leur synchronisation

Le rapport porte **4** segments : période, magasin, famille de produits, segment de client. Ils sont
synchronisés avec les deux pages de détail — pour qu'un lecteur qui descend sur un magasin n'ait pas à
refaire son choix — et **jamais** avec la page d'aide, qui doit rester stable : une page de définitions
qui change de contenu selon le filtre n'est plus une page de définitions.

Trois règles de conduite :

1. **un segment, une question** : période, magasin, famille, client — pas cinq contrôles pour trois
   idées ;
2. **l'ordre suit la lecture** : période d'abord, puis le territoire, puis le produit, puis le client ;
3. **l'état par défaut s'écrit** : « toutes les familles, tous les magasins, les douze derniers mois » —
   et il se vérifie à l'ouverture, pas au jugé.

> **Dans les faits.** Sur ce socle, le segment « famille » a **7** valeurs, le segment « magasin »
   **6** dont un dépôt sans aucune vente, et le segment « période » en a **44** — un mois par valeur.
   Trois segments qui semblent anodins, et qui décident chacun d'un dénominateur différent.

### 5.3 Le piège du dénominateur, mesuré

Voici le cœur du chapitre. Filtré sur une famille, le panier moyen se recalcule **dans** la famille :
le numérateur baisse, le dénominateur aussi. Le résultat est juste — et pourtant :

| Famille | Panier moyen |
|---|---|
| Plomberie | **128 958** FCFA |
| Bois et panneaux | **108 648** FCFA |
| Électricité | **100 896** FCFA |
| Peinture | **76 278** FCFA |
| Matériaux | **58 026** FCFA |
| Consommables | **51 900** FCFA |
| Quincaillerie | **40 879** FCFA |

Le panier du réseau — **107 396** FCFA — n'est le panier d'**aucune** des sept familles, et **5**
familles sur **7** sont sous cette moyenne : les deux familles les plus « panier lourd » la tirent vers
le haut. Un lecteur qui voit « 107 396 » en haut de page puis « 40 879 » après avoir cliqué sur
Quincaillerie ne se demande pas si le chiffre a changé de définition : il se demande lequel des deux est
faux. Ni l'un ni l'autre : c'est la **population** qui a changé.

Et le dénominateur se mesure, lui aussi : les **7** familles totalisent **215 995** tickets, le réseau
**145 212** seulement, soit **70 783** tickets comptés deux fois ou plus — **48,7 %** de majoration. Un
ticket qui contient des matériaux et de la quincaillerie est compté dans les deux familles. Toute
agrégation de pourcentages calculés par famille est donc fausse **par construction**, et cette phrase
appartient à la page d'aide du rapport.

> **Attention.** Deux chiffres calculés sous deux filtres différents ne s'additionnent ni ne se
> moyennent. **48,7 %** de tickets en double dans le seul socle du fil rouge : sur un modèle réel, le
> même piège produit des tableaux de bord entiers dont les colonnes ne totalisent pas la ligne
> « Total ».

### 5.4 Le piège du périmètre, mesuré

Deuxième piège, plus sournois : le numérateur et le dénominateur d'un taux peuvent ne pas couvrir la
même population. Le taux de rupture du rapport vaut **7,29 %** : **2 428** couples produit-magasin-mois
en rupture, sur **33 323** couples servis. Or ces **2 428** ruptures couvrent **6** magasins — dont le
dépôt central, qui a du stock et des ruptures —, tandis que les **33 323** couples servis n'en couvrent
que **5** : le dépôt ne vend pas, donc il ne « sert » aucun couple.

Trois façons de lire ce chiffre, et une seule est professionnelle :

1. **le publier tel quel** : **7,29 %** — c'est la définition héritée de M12, et elle se défend si elle
   est écrite ;
2. **le recalculer à périmètre égal** : **2 010** ruptures sur **33 323** couples servis donnent
   **6,03 %**, un taux dont les deux côtés parlent du même réseau ;
3. **le filtrer sur les magasins qui vendent** : le taux par magasin va alors de **5,73 %** à **6,30 %**
   — une dispersion étroite, donc un réseau homogène, et **418** ruptures du dépôt qui disparaissent
   silencieusement du rapport.

Un tableau de bord professionnel affiche le taux **et** la phrase qui dit son périmètre. Sans elle, un
comité arbitre sur un point de pourcentage qui n'est qu'un effet de filtre.

> **À retenir.** Un taux sans dénominateur écrit est un taux à refaire — la formule du chapitre 5 — et un
> taux dont le numérateur et le dénominateur ne couvrent pas la même population est un taux à **deux**
> phrases.

### 5.5 Les interactions entre visuels

Deux visuels voisins peuvent réagir de deux manières. Le **surlignage** met en évidence la part
concernée et laisse le reste visible : le lecteur garde le total sous les yeux, ce qui est presque
toujours ce qu'il veut. Le **filtrage croisé** ne montre plus que la part : les autres barres
disparaissent, et le total avec elles.

Trois réglages à écrire dans le dossier de conception :

1. **quelle direction** : la matrice magasin × famille filtre-t-elle les barres, ou l'inverse ? Une
   matrice qui reçoit un filtre de barres change de sens, et le lecteur ne le voit pas ;
2. **quels visuels ne réagissent pas** : une carte de total de réseau ne doit pas être filtrée par un
   visuel de détail, sinon elle cesse d'être un total ;
3. **quelles paires sont interdites** : deux visuels qui se filtrent mutuellement créent des boucles
   invisibles, et l'outil en refuse certaines en silence — un réglage non écrit est un réglage perdu.

Sur le fil rouge, les **35** couples magasin × famille servis sont la matière des interactions : cliquer
sur une famille dans la matrice réduit les barres de panier aux magasins qui vendent cette famille, ce
qui est utile — et faux si le lecteur compare ensuite au panier du réseau sans s'en apercevoir.

### 5.6 L'exploration à deux niveaux

Le rapport descend du magasin (**5** qui vendent) à la famille (**7**) puis au produit (**154**). Chaque
descente change la question et le chiffre. L'exploration se mesure en **couples** : **35** couples
magasin × famille portent des ventes, et **770** couples magasin × produit.

Le plus gros produit du réseau pèse **2,25 %** du chiffre d'affaires — **351 651 755** FCFA : au niveau
du détail, aucun produit ne décide de l'avenir du réseau, et un rapport qui ne montre que le produit
donne une impression de dispersion alors que la concentration est au niveau des magasins. La règle est
donc la suivante : **le niveau affiché s'écrit dans le titre**, et l'exploration se limite à la
profondeur utile — ici deux descentes : magasin, puis famille, puis produit.

### 5.7 Les info-bulles personnalisées

L'info-bulle répond à la question que le lecteur se pose **au moment où il survole un point** :
« pourquoi ce point est-il là ? ». Sur une barre de magasin, une info-bulle utile porte six valeurs —
chiffre d'affaires, panier moyen, taux de marge, taux de rupture, taux de retour, rotation — et pas une
seule de plus. Trois règles :

> **Définition.** Une **info-bulle** est un visuel miniature qui s'ouvre au survol d'un point, et qui
> répond à la question « pourquoi ce point est-il là ? ». Elle n'est pas un tiroir de données : elle
> porte ce qui explique le point, et rien de plus.

1. **ce qui explique le point**, pas tout ce que le modèle sait ;
2. **le format dans l'info-bulle aussi** : pourcentage à une décimale, montants en FCFA ;
3. **la définition quand le mot est ambigu** : dans l'infobulle du taux de retour du rapport, on écrit
   **1,17 %** des lignes et **1,91 %** des tickets, parce que les deux existent.

### 5.8 Q&A, et ce que le langage naturel ne fera pas

Le Q&A traduit une question écrite en langage courant en requête sur le modèle. Il fonctionne mieux sur
un modèle propre — noms de tables lisibles, mesures nommées, synonymes déclarés — et il ne fera jamais
trois choses :

- **inventer une mesure** : il ne peut répondre qu'avec les **11** mesures et les colonnes du modèle ;
- **deviner un périmètre** : « les ventes du mois » ne lui dit pas si les retours sont dedans ;
- **remplacer la page d'aide** : la question « pourquoi 107 396 et pas 128 958 ? » se répond par une
  phrase écrite, pas par une requête.

Un Q&A se prépare donc comme le reste : synonymes des noms de magasins, définitions des mesures, et une
page d'aide qui rappelle que le langage naturel ne lève pas une ambiguïté — il la déplace.

> **Attention.** Une réponse du Q&A n'est pas une mesure du rapport : elle n'a ni définition écrite, ni
> chiffre de contrôle, ni périmètre déclaré. Elle se vérifie donc toujours contre la page qui porte la
> mesure — **107 396** FCFA pour le panier du réseau, **1 202 550 590** FCFA pour l'encours — avant
> d'être citée en réunion.

### 5.9 La performance du rapport

Chaque visuel est une requête, et un rapport qui met quinze secondes à s'ouvrir sera remplacé par un
export Excel. Le socle permet de chiffrer l'ordre de grandeur : une carte coûte **1** ms, les barres par
magasin **1** ms, la matrice magasin × famille **4** ms, un panier filtré avec jointure **3** ms.

La comparaison décisive est ailleurs : les mêmes données relues intégralement depuis le fichier source
coûtent environ **143** ms, soit une centaine de fois le coût d'un visuel. C'est précisément ce que le
mode **Import** achète — une copie locale compressée — et ce que **DirectQuery** paie à chaque
affichage, à chaque filtre, pour chaque lecteur. Cinq causes de lenteur, et leurs remèdes :

1. **trop de visuels sur une page** : **14** visuels sur **3** pages, cinq par page au maximum ;
2. **trop de lignes ramenées** : une matrice qui affiche un produit par ligne sur **44** mois ;
3. **colonnes calculées inutiles** : le chapitre 5 l'a chiffré — facteur **1 558,4** sur une colonne de
   marge mal placée ;
4. **filtres posés au niveau du visuel** un par un, au lieu d'un segment synchronisé ;
5. **modèles de mesures oubliés** : les mesures les plus lourdes se calculent d'abord, une fois.

### 5.10 Trois clics, et le rapport est utilisé

Un rapport se juge à ce qu'un lecteur peut faire **sans aide** en trois clics : filtrer sur son magasin,
descendre d'un niveau, et revenir à l'état d'ensemble. C'est la raison d'être des signets, des segments
synchronisés et du bouton de retour — et c'est aussi la raison pour laquelle l'état par défaut doit être
**décrit** sur la page d'aide : « à l'ouverture : tous les magasins, toutes les familles, les douze
derniers mois, retours exclus ».

### 5.11 Les 6 erreurs de filtre qui se voient

1. **le filtre de visuel invisible** — le chiffre ne se reproduit pas ailleurs ;
2. **le segment non synchronisé** — le lecteur refait son choix à chaque page, puis se trompe ;
3. **le pourcentage moyenné** — **48,7 %** de tickets comptés deux fois dès qu'on divise par famille ;
4. **le périmètre implicite** — **7,29 %** publié sans dire les **6** magasins et les **5** ;
5. **la carte de total filtrée** par un visuel de détail, qui n'est plus un total ;
6. **l'info-bulle muette** — le lecteur survole, ne comprend pas, et appelle.

> **Conseil professionnel.** Testez chaque page en posant trois filtres extrêmes : un seul magasin,
> l'ensemble des magasins, une famille vide de ventes dans ce magasin. Ce sont ces trois états qui
> révèlent le périmètre caché, la division par zéro et la case vide mal expliquée — et ils se testent en
> trois minutes, pas en réunion.

---

## 6. Exemple concret — la page Commercial sous trois filtres

| Filtre posé | Ce qui change | Le piège à écrire |
|---|---|---|
| Aucun | panier réseau **107 396** FCFA | le périmètre est « tous les magasins » |
| Segment magasin : Ouaga 2000 | **34,1 %** du chiffre d'affaires du réseau | comparer au réseau reste licite, les deux périmètres s'emboîtent |
| Segment famille : Plomberie | panier **128 958** FCFA | le panier a changé de **population**, pas de formule |
| Exploration : famille → produit | **154** produits, le premier à **2,25 %** | indiquer le niveau dans le titre |
| Ruptures, tous filtres ouverts | taux **7,29 %** (**2 428** / **33 323**) | numérateur **6** magasins, dénominateur **5** |

Ce tableau est ce qu'on attend d'un dossier de conception pour les filtres : chaque filtre, ce qu'il
déplace, et la phrase qui l'explique. Il se relit en cinq minutes et évite l'essentiel des malentendus
d'un rapport en production.

---

## 7. Démonstration pas à pas — poser les filtres dans l'outil

L'outil n'est pas installé dans cet atelier : ces gestes se rejouent devant votre écran.

1. **Créez les 4 segments** — période, magasin, famille, segment de client — et placez-les en haut de
   page, dans l'ordre de lecture.
2. **Réglez la carte** du chiffre d'affaires en **total de réseau** : elle ne doit réagir à aucun visuel
   de détail. Contrôle : **15 595 154 955** FCFA sur les **44** mois.
3. **Synchronisez** les quatre segments avec les deux pages de détail, et décochez la page d'aide.
   Contrôle : la page d'aide affiche les mêmes définitions quels que soient les filtres.
4. **Réglez l'interaction** de la matrice magasin × famille vers les barres de panier : surlignage par
   défaut, filtrage si vous l'écrivez dans le dossier.
5. **Ajoutez l'exploration** sur la matrice : magasin, famille, produit. Contrôle : **35** couples
   magasin × famille avant descente, **154** produits au dernier niveau.
6. **Créez l'info-bulle** d'une barre de magasin avec six valeurs : chiffre d'affaires, panier, marge,
   rupture, retour, rotation.
7. **Ajoutez le bouton de retour** sur les deux pages de détail, et vérifiez qu'il ramène à l'état
   d'ensemble — signet compris.
8. **Écrivez la page d'aide** : l'état par défaut, la définition des **11** mesures, les exclusions, et
   la phrase sur le périmètre du taux de rupture.
9. **Testez trois filtres extrêmes** : un magasin, tous les magasins, une famille sans vente dans le
   magasin choisi. Contrôle : la case vide reste blanche, le taux ne provoque aucune erreur.
10. **Mesurez l'ouverture** de chaque page et notez le temps : le seuil de confort d'un rapport de
    gestion se situe sous trois secondes, tout compris.
11. **Contrôlez les pourcentages** : aucun pourcentage ne doit être additionné ou moyenné entre deux
    filtres. Contrôle : **48,7 %** de tickets en double dès qu'on totalise par famille.
12. **Rangez les réglages** dans le dossier : segments, synchronisation, interactions, exploration,
    info-bulles — c'est ce dossier qui permet à un successeur de modifier le rapport sans le casser.

---

## 8. Erreurs fréquentes

1. **Croire qu'un filtre réduit toujours les chiffres.** Un taux peut monter sous filtre, et un panier
   moyen passer de **107 396** à **128 958** FCFA sans qu'aucune donnée ne change.
2. **Oublier de dire le périmètre.** Le taux de rupture **7,29 %** n'a pas le même sens selon qu'on
   inclut le dépôt — **418** ruptures, **17,2 %** du total — ou non.
3. **Moyenner des pourcentages.** Les **7** familles totalisent **215 995** tickets pour **145 212**
   tickets distincts : la moyenne des paniers par famille n'est pas le panier du réseau.
4. **Synchroniser un segment avec la page d'aide.** Une définition qui dépend d'un filtre cesse d'être
   une définition.
5. **Laisser un filtre de visuel sans sous-titre.** Le chiffre existe, le lecteur ne le retrouve pas.
6. **Ne pas tester l'ouverture.** Un rapport lent est un rapport mort : **143** ms pour relire la source
   contre **1** ms pour interroger la copie importée, et c'est le mode Import qui fait la différence.

---

## 9. Bonnes pratiques professionnelles

1. **Un filtre au niveau le plus large qui convient** : rapport, page, puis visuel — et le filtre de
   visuel s'écrit dans le sous-titre.
2. **Un segment, une question**, dans l'ordre de lecture : période, magasin, famille, client.
3. **Écrire le périmètre de chaque taux** : population, exclusions, période. Une phrase par indicateur,
   sur la page d'aide.
4. **Interdire l'addition de pourcentages** entre deux filtres, et le dire dans la page d'aide.
5. **Limiter la profondeur d'exploration** à ce que le modèle sait expliquer : deux descentes suffisent
   ici.
6. **Six valeurs au maximum dans une info-bulle**, toutes formatées.
7. **Mesurer l'ouverture** des pages avant publication, et noter la mesure dans le dossier.
8. **Tester les trois filtres extrêmes** — un magasin, tous, une combinaison vide — avant chaque mise en
   production.

> **Boîte à outils.** Quatre contrôles avant de publier un rapport filtrable : le **périmètre** de chaque
> taux est écrit · les **segments** sont synchronisés **sauf** sur la page d'aide · aucun **pourcentage**
> n'est additionné entre deux filtres · chaque page **s'ouvre en moins de trois secondes**. Quatre
> contrôles, et le rapport cesse d'être une source de désaccord.

---

## 10. Exercice guidé

**Énoncé.** Le comité compare deux tableaux : le taux de rupture du rapport (**7,29 %**) et le taux
affiché par le responsable du réseau sur son propre tableau (**6,03 %**). Les deux ont raison. Expliquez
pourquoi, et décidez ce que le rapport doit afficher.

**Étape 1 — retrouver les deux calculs.** **7,29 %** est le taux publié : **2 428** couples en rupture
sur **33 323** couples servis. **6,03 %** est le même calcul à périmètre égal : **2 010** ruptures sur
les mêmes **33 323** couples servis.

**Étape 2 — identifier l'écart.** Les **418** ruptures manquantes — **17,2 %** du total — appartiennent
au dépôt central, qui ne vend pas et n'apparaît donc pas dans les couples servis. Le numérateur couvre
**6** magasins, le dénominateur **5**.

**Étape 3 — choisir la définition.** Le rapport affiche **7,29 %** parce que la rupture concerne tout
l'approvisionnement, dépôt compris — c'est la définition de M12, et elle reste la référence. La phrase
du périmètre est ajoutée sous le visuel.

**Étape 4 — décider.** Aucun des deux chiffres ne se supprime : le rapport garde **7,29 %**, et le taux
par magasin — de **5,73 %** à **6,30 %** — est publié à côté. Un comité peut alors arbitrer sur des
chiffres qui disent leur population.

**Attendu.** Les deux périmètres chiffrés, la réconciliation par les **418** ruptures du dépôt, la
définition retenue, et la phrase ajoutée au visuel.

---

## 11. Exercices autonomes

**Exercice 7.1.** Un lecteur filtre le rapport sur la famille Plomberie et lit un panier moyen de
**128 958** FCFA. Rédigez la note de trois lignes qui explique pourquoi ce chiffre n'est pas comparable
au panier du réseau.

**Exercice 7.2.** Vous devez poser trois filtres sur la page Commercial : période, magasin, famille.
Pour chacun, dites le niveau — rapport, page, visuel — et pourquoi.

**Exercice 7.3.** Le rapport affiche **7,29 %** de rupture et **418** ruptures appartiennent au dépôt.
Proposez deux formulations du titre du visuel, dont une seule est professionnelle, et dites pourquoi.

**Exercice 7.4.** Un collègue veut afficher le panier moyen par famille **et** le panier moyen du
réseau sur la même page. Dites ce qu'il faut écrire pour que les deux lectures ne se contredisent pas,
et le chiffre qui mesure le risque.

**Exercice 7.5.** La page Direction met quatre secondes à s'ouvrir. Citez **3** causes probables de
lenteur et la mesure qui permet de trancher pour chacune.

---

## 12. Correction détaillée

**Exercice 7.1.** Note possible : « **128 958** FCFA est le panier moyen des **tickets qui contiennent
au moins une ligne de plomberie**, calculé sur les tickets distincts de cette famille ; le panier du
réseau vaut **107 396** FCFA sur l'ensemble des tickets. Les deux chiffres portent sur des populations
différentes : **5** familles sur **7** sont sous la moyenne du réseau, et les deux familles à panier
lourd la tirent vers le haut. » Un lecteur averti ne compare plus les deux chiffres : il sait ce qu'ils
mesurent.

**Exercice 7.2.** La **période** se pose au niveau du **rapport**, quand toutes les pages parlent de la
même fenêtre d'analyse. Le **magasin** se pose au niveau de la **page** Commercial — c'est le sujet de
cette page. La **famille** se pose au niveau de la **page** également, et se synchronise avec le détail
produit ; un filtre de visuel n'est justifié que pour un cas d'école, et il s'écrit alors dans le
sous-titre du visuel concerné.

**Exercice 7.3.** Formulation professionnelle : « Taux de rupture du réseau — **2 428** couples en
rupture sur **33 323** couples servis, dépôt central inclus ». Formulation à écarter : « Taux de rupture :
**7,29 %** ». La première dit son périmètre, ce qui permet de réconcilier le chiffre avec celui du
responsable du réseau — **6,03 %**, soit **2 010** ruptures sur le même dénominateur — et d'expliquer
l'écart par les **418** ruptures du dépôt. La seconde invite au débat sur le chiffre au lieu du sujet.

**Exercice 7.4.** Il faut écrire deux choses : le panier du réseau est un **total**, le panier par
famille est calculé **dans** chaque famille, et les deux ne se comparent pas ligne à ligne ; et il faut
afficher les deux côte à côte pour que le lecteur voie l'écart. Le chiffre qui mesure le risque est la
majoration du dénominateur : **215 995** tickets additionnés pour **145 212** tickets distincts, soit
**48,7 %** — c'est la preuve que les lignes ne s'additionnent pas.

**Exercice 7.5.** Trois causes probables : **trop de visuels** sur la page — le rapport en compte
**14** sur **3** pages, et cinq par page est un maximum raisonnable ; **une mesure lourde** recalculée à
chaque affichage, comme un panier filtré avec jointure (**3** ms ici, mais un ordre de grandeur à
surveiller sur un modèle réel) ; **un mode de connexion inadapté** — la même donnée relue à la source
coûte environ **143** ms, contre **1** ms pour la copie importée. La mesure qui tranche est un chronomètre
par visuel, dans l'outil, sur la page ouverte sans filtre.

---

## 13. Mini-projet de chapitre — le protocole de filtres du rapport

**Énoncé.** Produisez le **protocole de filtres** du rapport : les **4** segments et leur niveau, leur
synchronisation page par page, les interactions entre visuels avec leur direction, la profondeur
d'exploration retenue, le contenu des info-bulles, et le périmètre écrit de chaque taux.

**Barème indicatif** : les **4** segments avec niveau et synchronisation (**5** points) · les
interactions et l'exploration documentées, direction comprise (**5** points) · le périmètre de chaque
taux écrit, avec les **418** ruptures du dépôt réconciliées (**5** points) · la page d'aide complétée —
état par défaut, définitions, interdiction d'additionner les pourcentages (**3** points) · sur
**18** points.

> **Pourquoi ce mini-projet.** Parce qu'un rapport filtrable sans protocole écrit produit des chiffres
> incomparables, et que la réunion d'après se passe à réconcilier des calculs au lieu d'arbitrer. Le
> protocole est la pièce qui rend un rapport **utilisable par quelqu'un qui ne l'a pas construit** — la
> définition même du travail fini.

---

## 14. Résumé du chapitre

| Notion | Mesure du module | Ce qu'elle enseigne |
|---|---|---|
| Niveaux de filtre | rapport, page, visuel | un filtre se pose au niveau le plus large qui convient |
| Segments | **4**, synchronisés sauf sur la page d'aide | une page de définitions ne dépend pas d'un filtre |
| Dénominateur | **215 995** tickets pour **145 212** distincts (**48,7 %**) | un pourcentage ne s'additionne pas entre deux filtres |
| Panier par famille | **40 879** à **128 958** FCFA (**3,15**) | le panier du réseau n'est le panier d'aucune famille |
| Périmètre | **2 428** / **33 323** = **7,29 %**, ou **2 010** / **33 323** = **6,03 %** | un taux se publie avec sa population |
| Exploration | **5** magasins, **7** familles, **154** produits | le niveau affiché s'écrit dans le titre |
| Performance | **1** ms, **4** ms, **143** ms | le mode Import achète la réactivité du rapport |
| Trois clics | filtrer, descendre, revenir | un rapport se juge à ce qu'on fait sans aide |

**Instrument.** `python3 tools/mesures_M14.py` recalcule les paniers par famille, la majoration du
dénominateur, la rupture avec et sans le dépôt, la profondeur d'exploration et le coût des visuels
(médianes de sept exécutions). Les réglages d'interaction, eux, se posent devant votre écran.

**Le module en une ligne.** Le chapitre 6 a décidé ce que le lecteur voit ; celui-ci a décidé **ce qu'il
peut demander** — et il a montré qu'un filtre ne change pas la vérité du chiffre, mais souvent sa
population, ce qui est une information à écrire au même titre qu'un calcul.

---

## 15. À retenir

1. **Un filtre change les deux côtés d'un taux.** Les **7** familles totalisent **215 995** tickets pour
   **145 212** tickets distincts : le dénominateur a suivi le filtre, et deux pourcentages ne
   s'additionnent pas.
2. **Un taux se publie avec son périmètre.** **7,29 %** compte **6** magasins au numérateur et **5** au
   dénominateur ; à périmètre égal, **6,03 %**. La phrase qui le dit vaut mieux que le chiffre qui le
   cache.
3. **Un rapport se juge à trois clics.** Filtrer, descendre d'un niveau, revenir — et une page d'aide
   qui ne dépend d'aucun filtre.

> **À retenir.** Ce qui distingue un rapport professionnel d'un rapport d'essai n'est pas le nombre de
> visuels : c'est ce qui est **écrit** à côté d'eux. Périmètre, population, état par défaut, exclusions —
> quatre phrases qui font qu'un lecteur ne peut pas se tromper tout seul.

---

## 16. Évaluation formative

1. Citez les trois niveaux de filtre et donnez un usage du fil rouge pour chacun.
2. Pourquoi un segment ne doit-il pas être synchronisé avec la page d'aide ?
3. Le panier moyen passe de **107 396** à **128 958** FCFA après un filtre de famille : pourquoi aucun
   des deux chiffres n'est-il faux ?
4. Quel chiffre prouve qu'un pourcentage calculé par famille ne s'additionne pas ?
5. Quelle est la différence entre le surlignage et le filtrage croisé ?
6. Pourquoi le taux de rupture vaut-il **7,29 %** dans le rapport et **6,03 %** sur le tableau du
   responsable du réseau ?
7. Combien d'explorations le rapport prévoit-il, et de quel niveau à quel niveau ?
8. Que contient une info-bulle utile, et combien de valeurs au maximum ?
9. Que le Q&A ne peut-il pas faire, et pourquoi ?
10. Trois causes probables d'un rapport lent, et la mesure qui tranche pour chacune.

**Corrigé.** 1. **Rapport** — la période commune à toutes les pages ; **page** — le magasin sur la page
Commercial ; **visuel** — un cas d'école, à écrire dans le sous-titre. 2. Parce qu'une définition qui
change selon un filtre de données n'est plus une définition : la page d'aide doit rester stable, sinon
deux lecteurs y lisent deux contenus. 3. Parce que la **population** a changé : **128 958** FCFA est le
panier des tickets de la famille Plomberie, **107 396** celui de tous les tickets ; **5** familles sur
**7** sont sous la moyenne du réseau. 4. La somme des tickets par famille — **215 995** — contre les
**145 212** tickets distincts, soit **48,7 %** de majoration : un ticket peut appartenir à deux
familles. 5. Le **surlignage** met en évidence la part concernée en gardant le total visible ; le
**filtrage croisé** réduit le visuel à cette part et fait disparaître le total. 6. Parce que les deux
calculs n'ont pas le même périmètre : **7,29 %** compte **2 428** ruptures sur **6** magasins pour
**33 323** couples servis sur **5** — les **418** ruptures du dépôt, **17,2 %**, sont au numérateur sans
être au dénominateur ; à périmètre égal, **2 010** sur **33 323** donnent **6,03 %**. 7. **Deux** :
magasin (**5** qui vendent), famille (**7**), puis produit (**154**). 8. Ce qui explique le point
survolé — au maximum six valeurs, formatées, avec la définition des indicateurs ambigus comme les deux
taux de retour, **1,17 %** des lignes et **1,91 %** des tickets. 9. Il ne peut ni inventer une mesure
absente du modèle, ni deviner un périmètre, ni remplacer une définition écrite : il traduit une question
en requête, il ne lève pas une ambiguïté. 10. Trop de visuels sur la page — **14** sur **3** pages ;
une mesure lourde recalculée à chaque affichage — **3** ms pour un panier filtré avec jointure sur ce
socle ; un mode de connexion inadapté — environ **143** ms pour relire la source contre **1** ms pour la
copie importée. La mesure qui tranche est un chronomètre par visuel, dans l'outil, sur la page ouverte.
