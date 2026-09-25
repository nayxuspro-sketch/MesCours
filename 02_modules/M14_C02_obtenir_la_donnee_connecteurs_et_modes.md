# Module M14.C02 — Obtenir la donnée : connecteurs et modes de connexion

**Outils : DuckDB 1.5.5 (exécuté) ; pandas (non requis). Power BI Desktop, Service, Fabric et Mobile
sont *cités* — l'outil n'est pas installé dans cet atelier (règle §1.5). Les poids, les ratios et le
delta de ce chapitre sont **mesurés** sur le socle à chaque exécution de `tools/mesures_M14.py`.**

![Les quatre modes de connexion, ce que chacun copie, à quelle vitesse il se rafraîchit et ce qu'il coûte à l'actualisation (production : `tools/figures_M14.py`)](../figures/M14_C02_quatre_modes_de_connexion.svg)

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous savez :

1. **brancher les quatre familles de sources** d'un projet courant — un fichier texte, un dossier de
   fichiers, un classeur et une base de données — et reconnaître à l'écran le geste de chaque
   branchement ;
2. **choisir un mode de connexion sur des mesures**, pas sur une préférence : sur le fil rouge,
   **240 000** lignes, dont **5 063** pour le seul mois de **2026-08** (**2,11 %** du total), et un
   fichier qui passe de **26,06** Mo à **6,13** Mo une fois rangé au format colonne ;
3. **alléger un import sans perdre une mesure** : le fait de ventes porte **17** colonnes, le rapport
   en utilise **11** et en ignore **6** — garder les **11** fait perdre **37,5 %** du poids ;
4. **programmer une actualisation** et savoir ce qu'elle exige : un mode d'import, une fréquence,
   quelqu'un qui surveille l'échec, et une passerelle si la source est derrière le mur du réseau
   interne ;
5. **diagnostiquer les cinq erreurs de connexion** les plus fréquentes, à partir de leur message
   exact, et non en cliquant au hasard.

---

## 2. Pourquoi cette notion est importante

Un rapport est un objet qui **vieillit dès qu'il est publié**. La donnée qu'il affiche a été lue un
jour, à une heure, depuis une source précise. Trois questions décident de la qualité du résultat, et
elles se posent avant le premier visuel : d'où vient la donnée, sous quelle forme entre-t-elle, et
comment se rafraîchit-elle ?

Ces trois questions ont une réponse chiffrée sur le fil rouge. **240 000** lignes de ventes, **12**
tables, **293 120** lignes au total, **4 489 143** cellules. Ce n'est ni petit ni énorme : c'est
exactement la taille d'un projet réel de PME, celle où l'on hésite entre « on copie tout et on
respire » et « on interroge la source à chaque clic ». Le chapitre tranche avec des mesures, et la
mesure la plus utile est celle-ci : **la table de ventes pèse 88,9 %** du fichier d'import, et ses
**6** colonnes inutiles pèsent à elles seules **9,78** Mo. Un modèle, c'est presque toujours **une**
table qui coûte cher.

Le reste du chapitre traite ce que personne n'aime préparer et que tout le monde subit : la
**connexion qui tombe**. Une source déplacée, un fichier renommé, une passerelle éteinte, un compte
dont le mot de passe a expiré — quatre pannes silencieuses qui transforment un rapport juste en un
rapport vide, sans que personne ne s'en aperçoive avant la réunion. Apprendre à lire ces messages fait
partie du métier.

---

## 3. Explication simple — la bouteille, le robinet, la citerne

Il y a trois façons d'avoir de l'eau chez soi, et l'outil de restitution les connaît toutes les trois.

**La bouteille** : on va au magasin, on remplit des bouteilles, on les range dans le placard. Elles
sont là, elles ne dépendent de personne, on les ouvre sans réseau — et elles ne se remplissent pas
toutes seules. C'est le mode **import** : la donnée est **copiée** dans le modèle, rangée, compressée,
et disponible hors ligne. Quand on veut la rafraîchir, il faut refaire le trajet : c'est
l'**actualisation**.

**Le robinet** : on l'ouvre, et l'eau arrive tant que le réseau fonctionne. Rien à ranger, rien à
remplir, mais si la canalisation casse, on reste sec — et chaque verre d'eau coûte un peu de réseau.
C'est la **connexion directe** : chaque visuel interroge la source au moment où on le regarde. La
donnée est toujours fraîche, et le rapport ne fonctionne que si la source répond.

**La citerne** : elle est chez vous, elle est pleine, et elle se remplit par un mécanisme qui ne
dépend pas du réseau. C'est le mode de la plateforme : la copie vit dans l'infrastructure, et l'outil
la lit sur place, sans requête et sans trajet.

Ce qui décide entre les trois n'est ni la mode ni la taille du fichier : c'est la **fraîcheur
attendue**. Un rapport de direction qui se lit le lundi à partir des ventes de la semaine n'a pas
besoin de la seconde près ; un écran de suivi d'entrepôt, si. Et une fois qu'on a dit cela, le choix
tombe tout seul — ce que le reste du chapitre démontre.

---

## 4. Vocabulaire essentiel

| Terme | Ce qu'il désigne exactement | Où il se règle |
|---|---|---|
| **Connecteur** | le module qui sait parler à un type de source : fichier, dossier, classeur, base, service | écran d'obtention des données |
| **Mode de connexion** | la façon dont le rapport obtient la donnée : copie, requête directe, modèle partagé, lecture de fichiers | paramètres de la source |
| **Import** | la donnée est copiée et rangée dans le modèle | par défaut |
| **DirectQuery** | chaque visuel interroge la source, sans copie | choix explicite |
| **Connexion directe** | le rapport se branche sur un modèle sémantique déjà construit ailleurs | choix explicite |
| **Direct Lake** | lecture des fichiers de la plateforme, sans copie ni requête | plateforme |
| **Actualisation** | la recharge planifiée ou manuelle du modèle | service ou poste |
| **Passerelle** | le pont entre le nuage et une source du réseau interne | serveur |
| **Paramètre** | une valeur nommée (un chemin, une date, un identifiant) qui entre dans la requête | éditeur de requête |
| **Requête combinée** | une requête construite à partir d'autres requêtes | éditeur de requête |
| **Requête orpheline** | une requête qui n'alimente rien et qui n'a jamais été interrogée | éditeur de requête |
| **Delta** | la part des lignes qui ont changé depuis le dernier chargement | source ou requête |

> **Définition.** Un **connecteur** est le module qui sait lire un type de source et le transformer en
> table. Le même bouton, « obtenir des données », ouvre une liste : c'est cette liste qui distingue
> une connexion à un fichier — qui passe par une copie — d'une connexion à un service, qui peut
> s'interroger à la demande.

> **Définition.** Le **mode de connexion** décrit **où vit la donnée pendant que le rapport
> l'affiche** : dans une copie rangée dans le modèle (import), dans sa source d'origine (connexion
> directe), ou dans un modèle construit par quelqu'un d'autre (connexion à un modèle partagé). C'est
> la décision la plus structurante du chapitre, et elle se prend table par table.

> **Définition.** L'**actualisation** est l'opération qui relit la source et remet la copie à jour.
> Elle a trois paramètres qui comptent : **quand** elle tourne, **combien de temps** elle prend, et
> **qui** est prévenu quand elle échoue. Un rapport dont l'actualisation échoue en silence affiche des
> chiffres d'avant-hier avec l'assurance d'un chiffre du jour.

> **Définition.** Une **passerelle** est un service installé sur le réseau de l'organisation, qui
> reçoit les demandes du nuage et va chercher la donnée à l'intérieur. Elle est nécessaire dès que la
> source n'est pas accessible depuis l'extérieur — un serveur de fichiers interne, une base dont
> l'accès est restreint — et son état de marche est la première chose à vérifier quand une
> actualisation échoue.

> **Définition.** Un **paramètre** est une valeur nommée qui entre dans une requête : un chemin de
> dossier, une date de début, un identifiant de société. Il transforme une requête figée en requête
> réutilisable, et il évite le défaut le plus courant des rapports qui vieillissent mal : le chemin
> écrit à la main, à dix endroits différents.

> **Attention.** Une source de type fichier — texte, classeur, dossier — vit **sur une machine**. Si
> cette machine n'est pas allumée, ou si le fichier change de dossier, l'actualisation échoue. Sur un
> projet réel, on déplace la donnée vers la base ou vers une bibliothèque partagée dès que le rapport
> devient utile à quelqu'un d'autre que son auteur.

> **Attention.** Le mode « connexion directe » n'est pas un mode « plus puissant » : c'est un mode
> **plus exigeant**. Chaque visuel devient une requête, chaque clic un aller-retour, et la source doit
> savoir répondre vite. Une source mal indexée donne un rapport qui met trente secondes à s'ouvrir,
> quel que soit le soin apporté aux visuels.

> **Dans les faits.** Sur le fil rouge, la décision se lit en trois nombres mesurés : **240 000**
> lignes, dont **5 063** pour le dernier mois complet (**2,11 %** du total), et **6,13** Mo une fois
> le fait rangé au format colonne — contre **26,06** Mo en fichier texte. Un rapport qui bouge une fois
> par nuit n'a aucune raison d'interroger une source à chaque clic.

---

## 5. Cours approfondi

### 5.1 Les quatre familles de sources du fil rouge

| Source | Ce qu'elle contient | Le geste | Ce qu'il faut anticiper |
|---|---|---|---|
| **Fichier texte** | les **12** tables du modèle, en CSV | obtenir des données, puis texte ou CSV | l'encodage, le séparateur, la ligne d'en-tête |
| **Dossier** | les extractions successives d'une même table | obtenir des données, puis dossier | le nom des fichiers, et la requête transformée en fonction |
| **Classeur** | le référentiel de coûts, tenu par le contrôle de gestion | obtenir des données, puis classeur | la feuille, la plage, et la ligne d'en-tête noyée dans un titre |
| **Base de données** | les mêmes ventes, côté serveur | obtenir des données, puis base | les droits de lecture, le mode de connexion, la passerelle |

Deux remarques valent pour les quatre.

**Un fichier texte se relit mal.** Le point-virgule et la virgule décimale existent dans la
francophonie, l'encodage peut être UTF-8 avec ou sans marque d'ordre, et une ligne vide en fin de
fichier crée une ligne fantôme. C'est pour cela que les fichiers du dossier d'import portent
**UTF-8 avec marque d'ordre**, un séparateur unique et des dates au format international : ce n'est
pas de l'esthétique, c'est ce qui évite trois écrans de réglages.

**Un dossier vaut mieux qu'un fichier.** Un rapport alimenté par un dossier survit à l'arrivée d'un
nouveau fichier mensuel : celui qui alimente un fichier unique doit être changé à la main chaque mois,
et c'est exactement le genre de tâche qu'on oublie. La transformation d'une requête en **fonction**
appliquée à chaque fichier du dossier est le geste professionnel de cette section.

### 5.2 Les quatre modes de connexion, comparés

| Critère | Import | Connexion directe | Modèle partagé | Lecture de fichiers |
|---|---|---|---|---|
| Où vit la donnée | copie dans le modèle | dans la source | dans le modèle d'un autre | dans les fichiers de la plateforme |
| Fraîcheur | celle de l'actualisation | à la seconde | celle du modèle consommé | à la seconde |
| Fonctionne hors ligne | oui | non | non | non |
| Coût d'une actualisation | relire la source | aucune | aucune | aucune |
| Coût d'un clic | nul | une requête | une requête | une lecture de fichier |
| Quand le choisir | volumétrie modérée, rapport qui bouge lentement | besoin de temps réel, source rapide et indexée | plusieurs rapports sur un même modèle | plateforme déjà en place |

Sur le fil rouge, l'arbitrage se fait en trois calculs, tous mesurés.

**Premier calcul — le poids.** Le fait de ventes pèse **26,06** Mo en fichier texte, et **88,9 %** du
fichier d'import complet (**29,32** Mo). Une seule table décide donc du confort du modèle : le reste —
les **11** autres — pèse **3,26** Mo à elles toutes.

**Deuxième calcul — la compression.** Le même fait, rangé au format colonne, tombe à **6,13** Mo, soit
un facteur **4,3**. C'est ce que fait l'import : il range la donnée en colonnes compressées, et c'est
la raison pour laquelle **240 000** lignes tiennent dans une limite de **1** Go sans discussion.

**Troisième calcul — le delta.** Une actualisation qui relit tout parcourt **240 000** lignes ; le
dernier mois complet en compte **5 063**, soit **2,11 %**. Autrement dit, **97,89 %** du travail
consiste à relire des lignes qui n'ont pas changé. C'est précisément ce que la connexion directe
évite… au prix d'une requête par visuel. La conclusion du chapitre est donc nuancée, et c'est la
bonne : **l'import est le bon choix ici**, non parce qu'il est simple, mais parce que la fraîcheur
exigée — une fois par nuit — laisse le temps de tout relire.

### 5.3 La stratégie du cache

L'import ne se contente pas de copier : il **range**. Trois conséquences pratiques.

- **La compression n'est pas magique** : elle dépend du nombre de valeurs distinctes par colonne. Un
  identifiant de ticket très varié se compresse mal ; un drapeau de retour, très bien. C'est pourquoi
  la colonne la plus coûteuse d'un modèle est souvent un identifiant, et non un montant.
- **Une colonne inutile coûte deux fois** : une fois à l'actualisation, une fois à l'ouverture. Les
  **6** colonnes que le rapport n'utilise pas pèsent **9,78** Mo de fichier, soit **37,5 %** de la
  table : les retirer est un geste de performance, pas de propreté.
- **Les limites de formule se lisent au modèle**, pas au rapport : **1** Go et **8** actualisations
  par jour en formule simple, **100** Go et **48** en formule avancée. Un rapport qui doit se
  rafraîchir toutes les heures dans la journée n'a pas sa place en formule simple, quelle que soit sa
  taille.

> **À retenir.** Un modèle peut mélanger les modes : **importer** l'historique, qui ne bouge plus,
> et **interroger** en direct la seule table qui change en temps réel. Choisir un mode unique pour tout
> un rapport, c'est se priver de la seule liberté que la question offrait.

> **Conseil professionnel.** Avant de brancher une source, écrivez ce qu'elle vaut : qui la produit,
> à quelle fréquence, et ce qui se passe si elle disparaît. Cette fiche prend dix minutes et se relit
> dix fois ; l'absence de fiche coûte une réunion à chaque incident.

### 5.4 L'actualisation, la passerelle, et ce qui se passe quand ça casse

L'actualisation a un cycle en quatre temps, et chaque temps a son mode de panne.

| Temps | Ce qui se passe | La panne typique | Le message |
|---|---|---|---|
| Déclenchement | le service demande au modèle de se recharger | la planification est mal réglée, ou le fuseau est faux | aucune erreur : l'actualisation n'a simplement pas eu lieu |
| Récupération | la source est relue | la source a bougé, ou la passerelle est éteinte | source introuvable, identifiants refusés |
| Transformation | les requêtes s'exécutent | un type a changé dans le fichier, une colonne renommée | erreur de conversion, colonne manquante |
| Publication | la nouvelle copie remplace l'ancienne | la mémoire manque sur le modèle | dépassement de capacité |

Trois règles de terrain valent mieux qu'un long discours.

1. **Personne ne surveille une actualisation qu'il ne sait pas qu'il faut surveiller.** Le rapport doit
   porter, sur sa page d'aide, la fréquence d'actualisation et le nom de celui qui reçoit l'alerte.
2. **Une passerelle s'installe sur une machine qui ne s'éteint pas.** Une passerelle installée sur le
   poste d'un collègue qui part en congé est une panne programmée.
3. **Le test d'échec fait partie de la mise en service.** On débranche volontairement la source, on
   regarde ce que le rapport affiche, et l'on décide : message clair pour le lecteur, ou rapport
   refusé. Ce qui ne va pas, c'est l'affichage silencieux de chiffres périmés.

### 5.5 Les cinq erreurs de connexion les plus fréquentes

| Message lu à l'écran | Ce qui s'est passé | Le geste juste |
|---|---|---|
| « Le fichier est introuvable » | le fichier a été déplacé ou renommé | passer au paramètre de chemin, ou réparer la source |
| « Les identifiants sont refusés » | mot de passe changé, ou compte désactivé | vérifier le compte de connexion, pas celui de l'auteur |
| « La passerelle n'est pas disponible » | le service local est arrêté | redémarrer la passerelle, et prévenir celui qui l'héberge |
| « La colonne n'a pas été trouvée » | la source a changé de structure | corriger l'étape nommée, pas la requête entière |
| « Le type de donnée est invalide » | un texte est arrivé dans une colonne de dates ou de nombres | traiter le cas à l'étape de conversion, avec un remplacement localisé |

Ces cinq messages ont un point commun : **ils nomment tous une étape**. Une requête dont les étapes
sont nommées — c'est la consigne du chapitre suivant — se répare en quelques minutes ; une requête
laissée en « Personnalisée1 » oblige à relire l'enchaînement depuis le début.

### 5.6 Ce que ce chapitre ne fait pas

Il ne branche rien : Power BI n'est pas installé dans l'atelier, et le chapitre l'écrit en tête plutôt
que de le laisser deviner. Ce qu'il fait à la place est plus utile qu'une capture d'écran : il
**mesure** ce que la décision de connexion met en jeu — le poids, la compression, le delta, la part de
chaque table — sur un socle que vous pouvez rouvrir. Quand vous serez devant l'écran, vous saurez
pourquoi vous cochez « import », et ce que vous perdrez en le cochant.

---

## 6. Exemple concret — trois sources, un seul rapport

**La situation.** Le rapport du fil rouge doit afficher **10** valeurs, dont le chiffre d'affaires net
(**15 595 154 955** FCFA), la marge (**29,12 %**), le panier moyen (**107 396** FCFA) et le taux de
rupture (**7,29 %**). Ces valeurs viennent de trois sources qui ne se comportent pas de la même façon.

| Source | Ce qu'elle fournit | Sa nature | Sa contrainte |
|---|---|---|---|
| Les fichiers d'export | les **12** tables du modèle, **293 120** lignes | texte figé, daté | à rejouer à chaque extraction |
| Le référentiel de coûts | **154** produits et leurs coûts | classeur tenu à la main | deux prix manquants, à traiter |
| La base de ventes | les mêmes ventes, côté serveur | interrogation à la demande | droits de lecture et passerelle |

**Ce que chaque source impose.** Les fichiers d'export se connectent en **import** : ils sont figés au
moment de l'extraction, et les relire chaque nuit suffit. Le classeur de coûts se connecte en
**import** aussi, mais avec un soin particulier : ses **2** prix manquants — les produits d'identifiants
`62` et `149` — sont **vides**, et un import qui convertit sans traiter le vide fabrique des erreurs
que le rapport affichera en clair. Quant à la base de ventes, elle pourrait se connecter en direct ;
le chapitre montre que c'est inutile ici : **2,11 %** des lignes changent par mois, et le rapport ne
se lit pas à la seconde.

**Le résultat mesuré.** Le modèle tient en **29,32** Mo de fichiers pour **4 489 143** cellules, et
les **10** valeurs attendues sont calculées sur le modèle en étoile : **15 595 154 955** FCFA,
**29,12 %**, **107 396** FCFA, **7,29 %**, **9,42** tours, **1,17 %** et **1,91 %**, **81,0 %** et
**78,2 %**, **1 202 550 590** FCFA. Les **8** valeurs comparables sont **identiques** à celles que M12
avait mesurées sur les tables opérationnelles. Deux chemins, un seul chiffre : c'est ce que le rapport
doit rendre, et c'est ce qui prouve que la connexion est correcte.

---

## 7. Démonstration pas à pas — brancher, alléger, actualiser

**Avertissement d'exécution.** Ces gestes n'ont pas été exécutés dans l'atelier (règle §1.5) : ils
sont écrits pour être rejoués devant votre écran. Les valeurs de contrôle, elles, sont mesurées.

**Étape 1 — Obtenir les données depuis un dossier.**

1. Dans le ruban **Accueil**, choisissez **Obtenir les données**, puis **Dossier**.
2. Indiquez le dossier qui contient les **12** fichiers d'export. L'outil propose deux actions :
   **Combiner** ou **Transformer les données**. Choisissez **Transformer** : vous voulez voir ce que
   contient un fichier avant d'empiler douze tables.
3. Vérifiez le premier fichier : encodage, séparateur, ligne d'en-tête, types. Puis, dans la requête
   du dossier, ajoutez une colonne qui porte le nom du fichier source : c'est elle qui permettra plus
   tard de retrouver l'origine d'une ligne douteuse.

**Étape 2 — Retirer les colonnes inutiles, et le vérifier.**

1. Ouvrez la requête du fait de ventes. Le rapport utilise **11** colonnes sur **17**.
2. Supprimez les **6** autres : identifiant de vente technique, taux de remise, montant de taxe, mode
   de paiement, canal, poids.
3. Contrôlez l'effet : le fichier passe de **26,06** à **16,28** Mo, soit **37,5 %** de moins. Si une
   page a besoin d'une des six colonnes plus tard, elle se rajoute en une étape — mais on ne garde pas
   une colonne « au cas où ».

**Étape 3 — Choisir le mode de connexion.**

1. Sélectionnez la requête, puis ouvrez ses **paramètres de source**.
2. Laissez le mode **import** pour les fichiers d'export et pour le classeur de coûts.
3. Si vous branchez la base de ventes, notez ce que le mode direct implique : une requête par visuel,
   une source rapide et indexée, et aucune lecture hors ligne. Comparez avec les **2,11 %** de lignes
   qui changent par mois, et décidez.
4. Écrivez la décision dans le dossier du rapport : mode retenu, raison, date.

**Étape 4 — Programmer l'actualisation.**

1. Publiez le rapport, puis ouvrez les paramètres du modèle sémantique dans le service : la section
   **Actualisation planifiée** porte la fréquence et les heures.
2. Réglez une actualisation nocturne : le socle change une fois par jour, et la formule simple permet
   **8** actualisations quotidiennes — largement assez.
3. Ajoutez une **notification d'échec** vers une adresse surveillée, et écrivez dans la page d'aide :
   fréquence, heure, et qui prévenir.
4. Faites le test d'échec : débranchez la source une fois, de votre plein gré, et regardez ce que le
   rapport affiche.

---

## 8. Erreurs fréquentes

| Erreur | Ce qui se passe | Le réflexe juste |
|---|---|---|
| importer tout, « au cas où » | le modèle charge des colonnes que personne ne lit | compter les colonnes utiles avant d'importer |
| connexion directe par principe | le rapport devient lent, et tombe quand la source tombe | choisir d'après la fraîcheur exigée |
| chemin écrit à la main | la première réorganisation du disque casse le rapport | nommer un paramètre de chemin |
| source unique par fichier | il faut modifier la requête à chaque nouvel export | passer par un dossier, avec une fonction |
| passerelle sur un poste de travail | l'actualisation s'arrête au premier congé | installer la passerelle sur une machine de service |
| actualisation sans alerte | des chiffres périmés sont présentés comme ceux du jour | brancher la notification d'échec |
| classeur rempli à la main | une cellule vidée devient une erreur affichée | traiter le vide dans la requête, avant le modèle |

---

## 9. Bonnes pratiques professionnelles

1. **Nommez chaque source dans le dossier du rapport** : nature, emplacement, propriétaire, fréquence
   de mise à jour. Une source sans propriétaire est une source qui s'arrêtera un jour sans prévenir.
2. **Un paramètre par chemin.** Le chemin du dossier d'export, le chemin du classeur de Coûts : deux
   paramètres, jamais des chemins écrits dans dix requêtes.
3. **Retirez les colonnes inutiles avant de publier.** Sur le fil rouge, **6** colonnes sur **17**,
   c'est **37,5 %** du poids de la table principale.
4. **Choisissez un mode par table, pas par projet.** Un rapport peut très bien importer l'historique
   et interroger en direct la seule table qui bouge en temps réel.
5. **Écrivez la politique d'actualisation dans la page d'aide :** fréquence, heure, fuseau, et la
   personne prévenue en cas d'échec.
6. **Testez la panne avant la mise en service.** Une source débranchée volontairement apprend plus
   qu'un mois d'utilisation normale.

---

## 10. Exercice guidé

**Énoncé.** Un service veut suivre ses livraisons. Il dispose d'un export mensuel de **9 000**
commandes, d'un fichier de suivi mis à jour **toutes les heures** par le transporteur, et d'une base
de données interne. Choisissez le mode de connexion de chacun, et justifiez par la fraîcheur exigée.

**Étape 1 — l'export mensuel.** **9 000** lignes qui changent une fois par mois : import, actualisation
mensuelle, aucune raison d'interroger la source à chaque clic.

**Étape 2 — le fichier du transporteur.** Mis à jour toutes les heures : c'est le cas d'usage de la
connexion directe — ou d'un import à fréquence horaire si la source est un simple fichier. Comparez
les deux : le mode direct exige une source interrogeable, pas un fichier posé sur un disque.

**Étape 3 — la base interne.** Elle porte **9 000** factures et **23 913** clients : l'import
convient, sauf si une règle de l'organisation interdit la copie — auquel cas la connexion directe
devient une contrainte et non un choix.

**Attendu.** Trois décisions, chacune justifiée par la fraîcheur attendue et par un ordre de grandeur,
et une phrase sur ce qui se passerait si l'on choisissait le même mode pour les trois.

---

## 11. Exercices autonomes

**Exercice 2.1.** Le fait de ventes pèse **26,06** Mo avec ses **17** colonnes et **16,28** Mo avec
les **11** colonnes utiles. Calculez la part des colonnes inutiles, et dites ce que cette part
représente en pourcentage du fichier d'import total de **29,32** Mo.

**Exercice 2.2.** Une source change **5 063** lignes par mois sur **240 000**. Expliquez pourquoi ce
seul nombre suffit à écarter l'argument « il faut du temps réel » sur ce projet, et dans quel cas il
ne suffirait pas.

**Exercice 2.3.** Un collègue a écrit le chemin de son fichier à la main dans **6** requêtes. Décrivez
ce qui se passera au premier déménagement du dossier, et écrivez la correction en **3** étapes.

**Exercice 2.4.** Le modèle passe de **26,06** Mo de fichier texte à **6,13** Mo au format colonne.
Expliquez pourquoi le facteur n'est pas le même pour toutes les colonnes, en prenant deux exemples du
fil rouge.

**Exercice 2.5.** Rédigez la politique d'actualisation du rapport du fil rouge en **5** lignes :
fréquence, heure, fuseau, mode, et qui est prévenu en cas d'échec. Justifiez la fréquence par la
mesure du delta.

---

## 12. Correction détaillée

**Exercice 2.1.** Les **6** colonnes inutiles pèsent **26,06 − 16,28 = 9,78** Mo, soit **37,5 %** de
la table de ventes. Rapportés au fichier d'import complet (**29,32** Mo), ces **9,78** Mo représentent
**33,4 %** du total : un tiers du poids du projet tient dans des colonnes que le rapport ne lit pas.

**Exercice 2.2.** **5 063** lignes sur **240 000**, c'est **2,11 %** du volume : autrement dit, plus de
**97 %** de ce qu'un rapport interrogerait à chaque clic n'a pas changé depuis un mois. Le temps réel
n'apporterait donc rien, et coûterait une requête par visuel. Il deviendrait nécessaire si l'écart se
creusait — un fichier de suivi horaire, par exemple — ou si la décision dépendait d'une information de
la journée : un stock, un encours, une rupture en cours.

**Exercice 2.3.** Au premier déménagement, les **6** requêtes échouent en même temps : l'outil ne sait
pas mettre à jour un chemin écrit à la main, et le rapport entier tombe pour un déplacement de dossier.
La correction en trois étapes : créer un **paramètre** de chemin ; remplacer dans les **6** requêtes
la valeur écrite par la référence au paramètre ; documenter la source dans la page d'aide, avec son
propriétaire.

**Exercice 2.4.** La compression dépend du nombre de valeurs distinctes : un **identifiant de ticket**
très varié se compresse mal, parce que presque chaque ligne porte une valeur différente ; un **drapeau
de retour** qui vaut vrai ou faux, ou un **numéro de magasin** parmi **6**, se compressent
extrêmement bien. C'est pourquoi la table la plus lourde d'un modèle est rarement celle qu'on croit :
celle qui porte beaucoup de colonnes d'identifiants coûte plus cher que celle qui porte les montants.

**Exercice 2.5.** « Actualisation quotidienne à **03:00**, fuseau du siège, mode import sur les **12**
tables ; l'export est relu intégralement (**240 000** lignes) parce que le delta mesuré est de
**5 063** lignes (**2,11 %**) et que la fenêtre nocturne suffit largement ; la personne prévenue en cas
d'échec est le contrôleur de gestion, et le rapport affiche sur sa page d'aide la date de la dernière
actualisation réussie. » Une politique d'actualisation qui cite le delta mesuré se défend ; une
politique qui dit « tous les jours » ne se défend pas.

---

## 13. Mini-projet de chapitre — la fiche de source du rapport

**Énoncé.** Produisez la **fiche de source** du rapport : pour chacune de ses tables, une ligne de
cinq colonnes. C'est le document que l'on donne au service informatique, et sans lequel chaque
incident devient une enquête.

| Colonne | Contenu attendu |
|---|---|
| Table | le nom de la table dans le modèle |
| Source | le système d'origine, et son emplacement |
| Mode | import, connexion directe, ou modèle partagé |
| Fréquence | à quelle heure et à quelle fréquence la donnée change |
| Propriétaire | qui fournit la donnée, qui prévient en cas d'échec |

**Barème indicatif** : les **12** tables décrites avec un mode justifié (**8** points) · fréquence et
propriétaire renseignés pour chacune (**6** points) · la politique d'actualisation en trois lignes,
avec la mesure du delta (**4** points) · sur **18** points.

> **Pourquoi ce mini-projet.** C'est le livrable qu'on oublie et qui coûte le plus cher : sans lui, la
> première panne d'actualisation se traite par tâtonnement, et personne ne sait à qui demander. Un
> analyste qui arrive avec cette fiche en réunion est un analyste qu'on rappelle.

---

## 14. Résumé du chapitre

| Notion | Mesure du module | Ce qu'elle enseigne |
|---|---|---|
| Sources du rapport | **12** tables, **293 120** lignes | un rapport vit de plusieurs sources, pas d'une |
| Poids total | **29,32** Mo, **4 489 143** cellules | la volumétrie se mesure, elle ne s'estime pas |
| Table dominante | **88,9 %** du poids pour le fait de ventes | une seule table décide du confort du modèle |
| Colonnes | **17** dans la table, **11** utiles, **6** inutiles | retirer coûte moins que garder |
| Gain mesuré | **9,78** Mo, **37,5 %** de la table | la propreté est une performance |
| Compression | **26,06** Mo vers **6,13** Mo, facteur **4,3** | pourquoi l'import tient dans un modèle d'**1** Go |
| Delta | **5 063** lignes, **2,11 %** du total | la fraîcheur exigée décide du mode |
| Limites de formule | **1** Go et **8** actualisations, **100** Go et **48** | les limites se lisent au modèle |
| Pannes typiques | **5** messages à reconnaître | une requête nommée se répare |

**Instrument.** `python3 tools/mesures_M14.py` recalcule le poids des **12** tables, la compression,
le delta du dernier mois, la part du fait principal et les valeurs de contrôle du rapport. Les gestes,
eux, ne s'exécutent pas dans l'atelier : ils s'écrivent, et ils s'exécutent devant votre écran.

**Le module en une ligne.** Le chapitre précédent a réglé la question d'argent ; celui-ci a fait
entrer la donnée — par un dossier, en mode import, avec des colonnes comptées, une actualisation
nocturne et une fiche de source — et il a montré que la bonne décision se lit en trois nombres plutôt
qu'en trois opinions.

---

## 15. À retenir

1. **Un mode de connexion se choisit par table, sur la fraîcheur exigée.** Sur le fil rouge, **5 063**
   lignes changent par mois (**2,11 %**) : l'import suffit, et il rapporte la lecture hors ligne.
2. **Le poids d'un modèle tient dans une seule table.** Le fait de ventes pèse **88,9 %** du fichier
   d'import ; ses **6** colonnes inutiles, **37,5 %** de sa propre table. Alléger, c'est mesurer.
3. **Une source a un propriétaire, une fréquence et une politique d'actualisation écrites.** Sans ces
   trois lignes, la première panne devient une enquête.

> **À retenir.** Une connexion réussie ne se voit pas, une connexion ratée se voit tout de suite : un
> rapport vide, ou pire, des chiffres d'avant-hier présentés comme ceux du jour. Les trois protections
> coûtent une heure et sauvent un trimestre : choisir le mode **par table**, nommer le **paramètre** de
> chemin au lieu de l'écrire, et brancher une **alerte** sur l'échec d'actualisation.

---

## 16. Évaluation formative

1. Citez les quatre modes de connexion et ce qui les distingue en une phrase chacun.
2. Que pèse le fait de ventes dans le fichier d'import, et pourquoi cette part compte-t-elle ?
3. Combien de colonnes le rapport utilise-t-il sur les **17** du fait, et que pèse le retrait des
   autres ?
4. Pourquoi un fichier rangé au format colonne est-il beaucoup plus léger qu'un fichier texte ?
5. Qu'est-ce qui décide du choix entre import et connexion directe ?
6. À quoi sert une passerelle, et où doit-elle être installée ?
7. Citez trois des cinq messages d'erreur de connexion et la cause de chacun.
8. Pourquoi un export mensuel placé dans un dossier vaut-il mieux que le même export placé dans un
   fichier unique ?
9. Que doit contenir la page d'aide d'un rapport, du point de vue des sources ?
10. Le rapport affiche **15 595 154 955** FCFA. Comment savez-vous que ce chiffre est le bon, et pas
    seulement le chiffre du jour ?

**Corrigé.** 1. Import (la donnée est copiée et rangée dans le modèle) ; connexion directe (chaque
visuel interroge la source) ; connexion à un modèle partagé (le rapport se branche sur un modèle
construit ailleurs) ; lecture de fichiers de plateforme (la copie vit dans l'infrastructure et se lit
sur place). 2. **88,9 %** : une seule table décide donc du confort du modèle et du temps
d'actualisation. 3. **11** sur **17** ; le retrait des **6** autres fait passer la table de **26,06** à
**16,28** Mo, soit **37,5 %** de moins. 4. Parce qu'il range les valeurs par colonne et les compresse :
sur le fil rouge, le facteur mesuré est de **4,3**. 5. La fraîcheur attendue, confrontée au coût
d'interrogation : ici **5 063** lignes changent par mois, sur **240 000**. 6. À relier le nuage à une
source du réseau interne ; elle s'installe sur une machine de service qui ne s'éteint pas. 7. « Fichier
introuvable » — la source a été déplacée ; « identifiants refusés » — le compte de connexion a changé ;
« passerelle indisponible » — le service local est arrêté. 8. Parce que le dossier absorbe l'arrivée du
fichier suivant sans intervention, alors qu'un fichier unique oblige à modifier la requête chaque
mois — et qu'on l'oublie. 9. La nature des sources, la fréquence d'actualisation, l'heure de la
dernière actualisation réussie et le nom de la personne prévenue en cas d'échec. 10. Parce qu'il est
**mesuré des deux côtés** : sur les tables opérationnelles comme sur le modèle en étoile, et les deux
chemins donnent le même chiffre — **8** valeurs sur **8** identiques.
