# Module M14.C01 — L'écosystème Power BI : quatre surfaces, quatre prix

**Outils : DuckDB 1.5.5 (exécuté) ; pandas (non requis ici). Power BI Desktop, Service, Fabric et
Mobile sont *cités* et jamais exécutés — l'outil n'est pas installé dans cet atelier (règle §1.5). Les
prix cités sont datés de septembre 2026 et convertis au taux pédagogique de **600** FCFA pour **1**
USD.**

![Les quatre surfaces de l'écosystème, ce que chacune coûte, l'échelle des licences et le seuil F64 (production : `tools/figures_M14.py`)](../figures/M14_C01_ecosysteme_et_licences.svg)

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous savez :

1. **distinguer les quatre surfaces** de l'écosystème — l'application de bureau, le service en ligne,
   la plateforme Fabric et l'application mobile — et dire à quoi chacune sert : on **construit** sur
   le poste, on **partage** dans le service, on **industrialise** sur la plateforme, on **consulte**
   sur le téléphone ;
2. **dire ce qui est gratuit et ce qui se paie** : la construction locale ne coûte rien, le partage
   coûte **8 400** FCFA par utilisateur et par mois en formule Pro, l'offre par utilisateur avancée
   coûte **14 400** FCFA, et une capacité Fabric à partir de **F64** fait **basculer les lecteurs
   dans le gratuit** ;
3. **chiffrer un pilote** avant de le demander : **4** personnes autour d'un rapport coûtent
   **33 600** FCFA par mois, soit **403 200** FCFA par an — une ligne de budget qu'on défend avec des
   chiffres, pas avec une conviction ;
4. **situer le module dans la chaîne** : M12 a **nommé** les sept étages de la chaîne BI, M13 a
   **construit** le quatrième — le modèle —, M14 branche le cinquième — la restitution — sur ce
   modèle, sans y toucher ;
5. **choisir une alternative quand il n'y a pas de licence**, et l'écrire : export PDF depuis le
   poste, tableur, outils ouverts, ou demande motivée d'une licence Pro pour un périmètre précis.

---

## 2. Pourquoi cette notion est importante

Un outil de restitution ne s'apprend pas comme un tableur. Un tableur coûte une fois et vit sur une
machine ; un outil de restitution vit sur un **compte**. C'est ce compte qui décide de ce que vous
pourrez partager, du nombre de personnes qui verront votre rapport, et de ce que l'organisation
paiera chaque mois.

La conséquence est simple et brutale : **le premier entretien professionnel sur Power BI ne porte pas
sur les visuels, il porte sur la licence.** Qui a le droit de publier ? Qui a le droit de lire ? Que
se passe-t-il quand le collègue d'à côté reçoit un message « vous n'avez pas accès à ce rapport » ?
Répondre « je ne sais pas » à ces trois questions fait échouer une candidature plus sûrement qu'un
graphique mal ordonné.

L'autre raison est économique, et elle est mesurable. Le dispositif raté du module précédent a coûté
**7 940 000** FCFA et n'a été ouvert que **4** fois le premier mois, avant d'être abandonné en **11**
semaines. Le pilote qui remplace ce genre de dispositif vise **3** lecteurs et **1** auteur : **4**
licences Pro, **403 200** FCFA par an. Le rapport n'a jamais été un problème d'argent : le problème
d'argent, c'est le rapport que personne n'ouvre.

Enfin, le chapitre règle une question que l'atelier rend visible : **ce module ne peut pas exécuter
Power BI**. Aucun chapitre de M14 ne lancera l'outil. Ce qui peut être mesuré le sera — les valeurs
que le rapport doit afficher, le poids des fichiers, les relations et les cardinalités — et le reste
sera écrit pas à pas, avec le libellé exact de chaque geste, pour que vous puissiez le refaire devant
votre écran.

---

## 3. Explication simple — le kiosque, l'imprimerie et le lecteur

Une organisation qui publie des chiffres ressemble à un journal, et un journal a quatre lieux.

Le **bureau du journaliste**, d'abord : c'est là qu'on écrit, qu'on rature, qu'on refait dix fois la
même page. Personne ne lit le brouillon, personne ne paie pour le brouillon, et c'est exactement le
rôle de l'application de bureau : elle est **gratuite**, elle vit sur votre machine, et elle suffit à
apprendre l'outil de bout en bout — jusqu'à la publication.

Le **kiosque**, ensuite : c'est l'endroit où des gens qui ne vous connaissent pas viennent chercher
votre journal, avec un droit d'entrée et un horaire. C'est le service en ligne : on y dépose un
rapport, on choisit qui le voit, on programme la livraison. Et comme au kiosque, l'entrée se paie —
par personne.

L'**imprimerie**, enfin : elle ne vend pas le journal, elle vend la **capacité** de l'imprimer, par
tonnes et par jour. C'est la plateforme Fabric : on y achète de la puissance, pas des personnes, et
au-delà d'un certain tonnage les lecteurs entrent gratuitement. C'est le seul endroit de l'écosystème
où le coût ne grimpe **pas** avec le nombre de lecteurs.

Le **lecteur**, pour finir, et sa poche : l'application mobile ne sert à rien d'autre qu'à consulter,
mais elle décide souvent de la réussite du rapport, parce qu'un directeur commercial lit ses chiffres
sur un téléphone, entre deux rendez-vous, et jamais sur un écran de bureau.

Tenez cette image, elle règle la plupart des décisions du chapitre : **on écrit au bureau, on vend au
kiosque, on imprime à l'imprimerie, on lit dans sa poche.** Confondre les quatre, c'est demander à un
kiosque de composer un journal, ou acheter une imprimerie pour faire lire trois personnes.

---

## 4. Vocabulaire essentiel

| Terme | Ce qu'il désigne exactement | Où il vit |
|---|---|---|
| **Surface** | l'un des quatre visages de l'écosystème : bureau, service, plateforme, mobile | partout |
| **Application de bureau** (*Desktop*) | le programme installé sur le poste : il crée les rapports | votre machine |
| **Service** | le site en ligne : il héberge, partage et actualise | le nuage |
| **Fabric** | la plateforme qui porte le service, l'entrepôt et les flux de données | le nuage |
| **Mobile** | l'application de consultation | le téléphone |
| **Espace de travail** (*workspace*) | le dossier partagé qui contient rapports, modèles et flux | le service |
| **Application** (*app*) | le paquet publié pour les lecteurs : ils ne voient que ce paquet | le service |
| **Modèle sémantique** (*semantic model*) | l'ancien « jeu de données » : les tables, les relations, les mesures | le service |
| **Capacité** (*capacity*) | la puissance achetée au mois, indépendante du nombre de lecteurs | Fabric |
| **Locataire** (*tenant*) | l'organisation dans laquelle tous les comptes existent | l'administration |
| **Passerelle** (*gateway*) | le pont entre le nuage et une source restée sur le réseau interne | le serveur |
| **Actualisation** (*refresh*) | la recharge planifiée des données du modèle | le service |

> **Définition.** Une **surface** est un des quatre endroits où l'on touche à un rapport : on le
> **construit** sur le bureau, on le **partage** dans le service, on l'**industrialise** sur la
> plateforme, on le **consulte** sur le mobile. Un même rapport les traverse dans cet ordre, et
> chaque surface a sa propre question de licence.

> **Définition.** Un **espace de travail** est le dossier partagé du service : il contient les
> rapports, leurs modèles sémantiques et les flux qui les alimentent. C'est l'unité de travail des
> équipes, et c'est aussi **l'unité de permission** : on n'autorise pas quelqu'un sur un rapport, on
> l'autorise dans un espace.

> **Définition.** Une **application** est le paquet que les lecteurs voient. Elle peut rassembler
> plusieurs rapports d'un même espace et n'en montrer qu'une partie. La différence est importante :
> dans un espace de travail on voit tout, avec des droits de modification ; dans une application on
> voit ce qui a été publié et rien d'autre.

> **Définition.** La **capacité** est une puissance louée au mois pour un volume de calcul donné,
> indépendante du nombre de personnes. C'est pour cela qu'elle change l'économie : en dessous du
> seuil, chaque lecteur a besoin d'une licence ; à partir du seuil **F64**, les lecteurs consultent
> avec un compte gratuit, et l'organisation paie la machine plutôt que les yeux.

> **Définition.** Le **locataire** (*tenant*) est l'espace administratif de l'organisation : c'est
> lui qui détient les licences, applique les règles et décide, par exemple, que seuls certains
> groupes peuvent publier à l'extérieur. Un rapport qui doit sortir de l'organisation passe par une
> décision du locataire, jamais par un réglage de rapport.

> **Attention.** « Gratuit » ne veut pas dire « sans compte ». L'application de bureau s'installe et
> crée des rapports sans licence payante, mais publier dans un espace de travail partagé, ou lire un
> rapport publié par quelqu'un d'autre dans un espace qui n'est pas adossé à une capacité, demande une
> licence. La confusion coûte un après-midi, puis une réunion.

> **Attention.** Les prix et les seuils bougent. Ceux de ce chapitre portent leur date : **septembre
> 2026**. La bonne habitude professionnelle n'est pas de les retenir par cœur, c'est de les
> **revérifier à la source** avant d'écrire une note de budget — et de dater cette note.

> **Dans les faits.** Le seuil qui décide de tout se lit en une ligne : **F64** — soit **64** unités
> de capacité, l'équivalent de l'ancienne offre P1. En dessous, chaque lecteur a besoin d'une
> licence ; à partir de là, les lecteurs consultent gratuitement. Une organisation de **3** lecteurs
> n'a donc pas de raison de l'acheter ; une organisation de **300** lecteurs n'a pas de raison de
> faire autrement.

---

## 5. Cours approfondi

### 5.1 Les quatre surfaces, et ce qu'on y fait

| Surface | Ce qu'on y fait | Ce qu'on n'y fait pas | Licence |
|---|---|---|---|
| **Bureau** | créer les rapports, écrire les mesures, modéliser, tester | partager, planifier, notifier | gratuite |
| **Service** | publier, organiser les espaces, gérer les droits, planifier l'actualisation, commenter | créer depuis zéro (les retouches restent limitées) | **8 400** FCFA par utilisateur et par mois (Pro) |
| **Fabric** | héberger les données, chaîner les traitements, servir à grande échelle | remplacer le poste de travail de l'analyste | à partir du seuil **F64**, prix au mois |
| **Mobile** | consulter, filtrer, commenter, recevoir une alerte | créer ou modifier un rapport | inclus dans la licence de lecture |

Trois remarques de terrain, qui évitent trois déceptions.

**Premièrement, tout le travail de construction est gratuit.** Le module entier — les **12**
relations, les **10** mesures, les **3** pages — se fait sans licence payante, sur le poste. C'est une
bonne nouvelle pédagogique : vous pouvez apprendre l'outil complet sans qu'on vous ouvre un compte.

**Deuxièmement, le service n'est pas un lecteur de fichiers.** Le rapport que vous voyez sur votre
poste n'est pas ce que vos lecteurs verront : dans le service, le modèle sémantique et le rapport
sont **deux objets distincts**, reliés. C'est cette séparation qui permet à dix rapports de partager
un même modèle, et c'est elle qui rend la question de l'actualisation importante : on n'actualise pas
un rapport, on actualise un modèle.

**Troisièmement, la retouche dans le service existe mais reste l'exception.** L'outil sait modifier
un rapport sans revenir au poste, mais un rapport professionnel se construit au poste, se relit, puis
se publie. Un rapport né dans le service est un rapport qui ne passera probablement jamais la grille
de conception du chapitre C08.

### 5.2 Ce qui est gratuit, ce qui se paie, et pourquoi le seuil change tout

Reprenons l'échelle, avec les quatre marches et le seul point de rupture.

| Formule | Prix | Ce qu'elle donne | Quand elle suffit |
|---|---|---|---|
| Bureau seul | **0** FCFA | création et analyse locales, export vers un fichier | apprendre, prototyper, livrer un PDF |
| Pro | **8 400** FCFA par utilisateur et par mois | publier, partager, planifier, lire | le cas courant d'une PME |
| Premium Per User | **14 400** FCFA par utilisateur et par mois | tout Pro, avec des modèles plus grands, plus d'actualisations par jour et les rapports paginés | un analyste qui manipule de gros volumes |
| Capacité Fabric | prix au mois, à partir du seuil **F64** | les **lecteurs** consultent sans licence payante | beaucoup de lecteurs, peu d'auteurs |

Le raisonnement tient en deux phrases. **En dessous du seuil**, le coût suit le nombre de personnes :
**100** lecteurs en Pro coûtent **840 000** FCFA par mois, et **300** en coûtent **2 520 000**. **À
partir du seuil**, le coût suit la machine : on paie la capacité, et le nombre de lecteurs devient une
question de droits, plus de budget. C'est pour cette raison qu'une organisation bascule rarement pour
une raison technique : elle bascule quand le nombre de lecteurs rend la facture par personne absurde.

> **À retenir.** En dessous du seuil **F64**, la facture suit les personnes : **100** lecteurs en
> formule simple coûtent **840 000** FCFA par mois, **300** en coûtent **2 520 000**, et **40** en
> coûtent **336 000**. À partir du seuil, elle suit la machine, et le nombre de lecteurs cesse d'être
> une ligne de budget pour devenir une ligne de droits.

Trois précisions qui font la différence entre une note de budget juste et une note approximative.

- **L'auteur paie toujours sa licence**, capacité ou pas. La capacité fait lire gratuitement, elle ne
  fait pas **créer** gratuitement.
- **L'offre avancée par utilisateur ne se partage pas** avec des lecteurs en formule simple : un
  rapport publié dans un espace de ce niveau se lit avec le même niveau, sauf s'il est adossé à une
  capacité. Autrement dit, on n'achète pas « une licence avancée pour le patron » sans vérifier qui
  doit lire.
- **Les anciennes offres de capacité ne se vendent plus** : les contrats existants arrivent à échéance
  et migrent vers les offres actuelles. Un dossier de budget qui cite encore l'ancienne grille est un
  dossier que le service informatique corrigera à votre place.

### 5.3 Le compte, le locataire et les quatre rôles d'un espace

Avant toute licence, il y a un compte, et ce compte a une nature.

| Type de compte | Ce qu'il permet | Ce qu'il ne permet pas |
|---|---|---|
| Compte professionnel ou scolaire | tout : publier dans un espace, partager, lire | rien de ce qui suit |
| Compte personnel | créer et analyser localement, garder ses rapports à soi | publier dans un espace partagé, recevoir une application |

C'est la première cause d'échec d'un stagiaire : il construit un rapport avec son adresse personnelle,
il l'envoie, et le rapport ne peut pas être publié là où l'entreprise l'attend. Le contrôle est
immédiat : **quel compte utilisez-vous, et à quel locataire appartient-il ?**

Dans un espace de travail, quatre rôles se distribuent, et il faut savoir lequel on demande :

| Rôle | Ce qu'il peut faire | À qui on le donne |
|---|---|---|
| **Administrateur** | tout, y compris ajouter et retirer des membres | le responsable de l'espace |
| **Membre** | publier, modifier, partager, gérer les droits | l'équipe qui produit |
| **Contributeur** | publier et modifier le contenu | l'analyste |
| **Lecteur** | lire ce qui est dans l'espace | celui qui doit voir le détail |

La règle professionnelle est de donner le rôle le plus faible qui suffit. Un directeur n'a pas besoin
d'être membre pour lire trois pages : il a besoin de l'**application** publiée et du rôle de lecteur,
sinon le premier clic malheureux lui montrera les rapports en cours d'écriture.

### 5.4 Fabric, et ce que la plateforme change (ou ne change pas)

Fabric n'est pas un cinquième outil de restitution : c'est le socle dans lequel le service est
désormais rangé. Le module M12 en a nommé les étages ; voici ce que cela change **pour un auteur de
rapports**, en trois lignes.

- **La donnée peut vivre à côté du rapport.** Une table hébergée dans la plateforme se lit sans
  passerelle et sans copie locale, ce qui simplifie l'actualisation.
- **Les gros volumes deviennent ordinaires.** Un rapport qui interrogeait une base distante peut lire
  une copie locale au format colonne, avec des temps de réponse très courts.
- **Le vocabulaire change, pas le métier.** On parle de lac de données, d'entrepôt et de flux ; le
  travail reste : modéliser proprement, mesurer juste, publier lisiblement.

Ce que Fabric **ne change pas** : un modèle mal construit reste mal construit, une relation ambiguë
reste ambiguë, et un rapport illisible reste illisible. L'argent dépensé en capacité ne corrige aucune
des trois choses que M13 a enseignées.

### 5.5 Quand il n'y a pas de licence

C'est le cas le plus fréquent dans une petite structure, et il a quatre réponses, à essayer dans cet
ordre.

1. **Travailler au poste et livrer un fichier.** Le rapport se construit sans licence, s'exporte en
   PDF et se diffuse. On perd l'actualisation et l'interaction, on garde la justesse.
2. **Utiliser ce qui est déjà payé.** Une organisation qui possède déjà une suite bureautique
   professionnelle possède parfois la formule Pro sans le savoir : c'est la première question à poser
   au service informatique, avant toute demande d'achat.
3. **Changer d'outil pour un usage précis.** Un outil ouvert hébergé en interne peut suffire pour
   consulter ; M16 compare ces outils et leurs coûts réels. La bonne question n'est pas « quel outil
   est le meilleur », c'est « quel outil ce besoin-là justifie-t-il ».
4. **Demander un pilote chiffré.** Un pilote n'est pas une envie : c'est un périmètre, un nombre de
   personnes, un coût mensuel, une durée, et deux indicateurs de succès — combien d'ouvertures, et
   quelle décision a changé. Le mini-projet de ce chapitre fait écrire cette note.

> **Conseil professionnel.** Écrivez votre note de licence en trois paragraphes : ce que le rapport
> sert à décider, qui le lira et combien ils sont, ce que cela coûte par mois et par an. Une demande
> de licence qui commence par « Power BI est un excellent outil » est refusée ; une demande qui
> commence par « trois personnes doivent lire ce chiffre chaque lundi, cela coûte **33 600** FCFA par
> mois » est arbitrée.

### 5.6 Où ce chapitre s'arrête

Le chapitre suivant fait entrer la donnée : connecteurs, modes de connexion, actualisation. Avant de
le lire, retenez ce qui vient d'être établi : **l'apprentissage ne coûte rien, le partage se paie, et
le seuil qui fait basculer une organisation se compte en lecteurs.** Tout le reste du module se
construit sur cette base, sans jamais y revenir.

---

## 6. Exemple concret — trois scénarios, une décision

**La situation.** Une entreprise de distribution de **40** personnes veut publier le rapport du fil
rouge — **3** pages, **14** visuels, **10** mesures. Trois populations sont concernées : **1** auteur
(le contrôle de gestion), **3** lecteurs réguliers (direction commerciale, direction générale,
responsable des achats) et, à terme, **20** lecteurs occasionnels (les chefs de rayon).

**Scénario A — rien, ou presque.** Le rapport vit sur le poste de l'auteur et sort en PDF chaque
lundi.

| Poste | Coût |
|---|---|
| Licence | **0** FCFA |
| Temps de l'auteur, chaque semaine | la manipulation manuelle et l'envoi |
| Ce qu'on perd | l'actualisation, l'interaction, les segments, l'accès mobile |

**Scénario B — quatre licences Pro.** Le rapport est publié, l'actualisation est planifiée, les
**4** personnes entrent dans le service, les **20** autres attendent.

| Poste | Coût |
|---|---|
| Licence, **4** personnes | **33 600** FCFA par mois, soit **403 200** FCFA par an |
| Ce qu'on gagne | rapport toujours à jour, interaction, mobile, commentaires |
| Ce qu'on perd | les **20** lecteurs occasionnels ne sont pas couverts : s'ils doivent lire, chacun coûte **8 400** FCFA de plus par mois |

**Scénario C — la capacité.** On adosse l'espace à une capacité Fabric à partir du seuil **F64** : les
lecteurs consultent sans licence payante.

| Poste | Coût |
|---|---|
| Licence auteur | **1** licence Pro, **8 400** FCFA par mois |
| Capacité | un montant mensuel fixe, indépendant du nombre de lecteurs |
| Ce qu'on gagne | les **20** lecteurs occasionnels lisent sans licence |
| Ce qu'on perd | la souplesse : on paie la machine même le mois où personne ne regarde |

**La décision, et sa règle.** Avec **4** personnes, le scénario B est le bon : la capacité coûte plus
cher que les licences qu'elle remplace. Avec **40** lecteurs réguliers, l'arbitrage s'inverse : **40**
licences Pro coûtent **336 000** FCFA par mois, contre une capacité au prix fixe qui fait lire tout le
monde. Le point de bascule ne se calcule pas de mémoire : il se calcule une fois, pour son
organisation, et il se revérifie chaque année, parce que les prix changent et l'effectif aussi.

**Ce que le socle apporte à cet exemple.** Les trois scénarios portent sur le même rapport, dont les
valeurs sont mesurées et publiées : **15 595 154 955** FCFA de chiffre d'affaires, **29,12 %** de
marge, **107 396** FCFA de panier moyen, **7,29 %** de rupture, **2 428** couples produit-magasin-mois
en rupture, **9 000** factures dont **1 202 550 590** FCFA d'encours. Un rapport qui décide de ces
chiffres-là justifie **403 200** FCFA par an ; un rapport qui n'en décide aucun ne les justifie pas,
quelle que soit la formule.

---

## 7. Démonstration pas à pas — installer, vérifier sa licence, publier

**Avertissement d'exécution.** Aucun geste de cette démonstration n'a été exécuté dans l'atelier :
Power BI n'y est pas installé (règle §1.5). Ce qui suit est le libellé exact des gestes, dans l'ordre,
tel qu'il doit être rejoué devant votre écran. Les valeurs de contrôle, elles, sont mesurées sur le
socle : ce sont celles du fichier des attendus, et elles ne dépendent pas de l'outil.

**Étape 1 — Installer l'application de bureau.**

1. Ouvrez la boutique d'applications de votre système ou la page de téléchargement officielle de
   l'éditeur, et installez **Power BI Desktop**.
2. Au premier lancement, l'écran d'accueil propose de se connecter ou de continuer sans compte. Vous
   pouvez continuer sans compte : c'est le mode création locale, gratuit.
3. Vérifiez la version installée : c'est la première information à donner quand vous signalerez un
   problème. Deux versions coexistent habituellement — une mise à jour chaque mois, et une version
   indépendante du magasin. Notez celle que vous utilisez ; les nouveautés n'arrivent pas au même
   moment dans les deux.

**Étape 2 — Vérifier la licence, avant de promettre quoi que ce soit.**

1. Connectez-vous avec votre compte **professionnel ou scolaire**, pas avec une adresse personnelle.
2. Ouvrez le menu de votre profil, en haut à droite : il affiche le compte connecté et le locataire
   auquel il appartient.
3. Dans le service, la page de gestion des licences de votre organisation indique ce qui vous est
   attribué. Trois cas possibles, et trois conclusions : **gratuit** — vous construisez et vous ne
   partagez pas ; **Pro** — vous publiez dans les espaces de travail ; **avancé** — vous publiez et
   vous ouvrez les fonctions de gros volume.

**Étape 3 — Publier un rapport de test, et vérifier qui le voit.**

1. Dans l'application de bureau, le ruban **Accueil** porte le bouton **Publier**. C'est le geste qui
   fait passer un rapport du poste au service.
2. L'outil demande l'espace de travail de destination. Choisissez un espace différent de celui de
   production, et nommez le rapport d'après la règle du module : sujet, périmètre, date.
3. Une fois publié, partagez-le avec un collègue qui n'a **pas** de licence et demandez-lui d'ouvrir
   le lien. Trois réponses possibles : il lit — son compte est couvert ; il ne voit rien — il lui
   manque une licence ; il voit le rapport mais pas les données — il a la licence et pas le droit.
   Ces trois symptômes se ressemblent et n'ont rien à voir : **c'est exactement pour cela que ce
   chapitre existe avant les autres.**

**Étape 4 — Lire les valeurs de contrôle.**

Le rapport du fil rouge doit afficher, une fois branché sur le modèle du module précédent, les
valeurs du fichier des attendus. Les huit premières :

| Indicateur | Valeur attendue |
|---|---|
| Chiffre d'affaires net | **15 595 154 955** FCFA |
| Taux de marge | **29,12** % |
| Panier moyen par ticket | **107 396** FCFA |
| Taux de rupture | **7,29** % |
| Rotation des stocks | **9,42** tours |
| Taux de retour, lignes ou tickets | **1,17** % ou **1,91** % |
| Taux de service, deux dénominateurs | **81,0** % ou **78,2** % |
| Encours client | **1 202 550 590** FCFA |

**Pourquoi ces huit-là.** Parce qu'elles sont **mesurées des deux côtés** : sur les tables
opérationnelles comme sur le modèle en étoile, et les deux chemins donnent le même chiffre —
**8** valeurs sur **8** identiques. C'est ce que le tableau de bord doit rendre, et c'est aussi la
preuve que le modèle est juste avant même d'ouvrir l'outil.

---

## 8. Erreurs fréquentes

| Erreur | Ce qui se passe | Le réflexe juste |
|---|---|---|
| construire avec une adresse personnelle | la publication dans l'espace de travail est refusée | vérifier la nature du compte **avant** de commencer |
| croire que le bureau est une version d'essai | on repousse le travail en attendant « la vraie version » | le bureau est gratuit sans limite de durée |
| publier dans son espace personnel | personne ne peut recevoir l'application | publier dans un espace de travail partagé |
| croire que les lecteurs sont toujours gratuits | la moitié de l'équipe ne peut pas ouvrir le rapport | compter les lecteurs **avant** de choisir la formule |
| acheter l'offre avancée « pour le patron » | elle ne se partage pas avec des lecteurs en formule simple | vérifier qui doit lire, pas qui doit briller |
| citer des prix de mémoire | la note de budget est fausse à la première révision | dater les prix, les revérifier à la source |
| croire que Fabric est obligatoire | on reporte le projet d'un an | la plateforme est un choix, pas un prérequis |

La sixième ligne mérite un mot de plus, parce que c'est celle qui vieillit le plus vite. Un chiffre
écrit de mémoire dans un document professionnel est un chiffre faux à retardement : les prix de ce
chapitre sont datés de **septembre 2026**, et la première chose qu'un lecteur attentif doit pouvoir
faire, c'est vérifier qu'ils sont encore vrais. Le manuel applique cette règle à lui-même : chaque
nombre cité dans ces pages vient d'un relevé recalculé, et les prix d'un produit commercial portent
leur date.

---

## 9. Bonnes pratiques professionnelles

1. **Nommez le compte et le locataire dans le dossier du rapport.** Deux lignes, écrites une fois, qui
   évitent une réunion : avec quel compte le rapport a-t-il été publié, et dans quel locataire.
2. **Comptez les lecteurs avant de choisir la formule.** Écrivez la liste : qui lit, à quelle
   fréquence, et pour décider quoi. Une licence sans lecteur identifié est une licence perdue.
3. **Gardez une licence d'auteur par personne qui publie.** Un espace de travail sans auteur est un
   espace qui s'arrête à la première absence.
4. **Testez le partage avec un lecteur sans droits.** Le seul test qui compte est celui d'un collègue
   à qui vous n'avez rien expliqué : s'il doit vous appeler, la page d'aide du rapport manque.
5. **Datez toute note de budget**, avec la source du prix. Les tarifs d'un service en ligne changent ;
   une note sans date ne peut pas être révisée, seulement contestée.
6. **Écrivez la sortie de secours.** Que se passe-t-il si la licence n'est pas renouvelée, ou si
   l'actualisation échoue ? Un rapport dont personne ne sait ce qui arrive en cas de panne est un
   rapport fragile, même s'il est beau.

---

## 10. Exercice guidé

**Énoncé.** Une association dispose de **1** analyste et de **6** lecteurs réguliers, plus **12**
bénévoles qui consultent une fois par mois. Elle construit son rapport sur le poste, sans licence.
Écrivez la note de licence : ce qu'elle paye aujourd'hui, ce qu'elle paierait avec des licences Pro,
ce que changerait une capacité, et votre recommandation.

**Étape 1 — le coût actuel.** **0** FCFA de licence, et l'analyste exporte une capture ou un PDF à
chaque mise à jour. Comptez ce que cela coûte en temps : ce n'est pas nul, mais ce n'est pas de
l'argent.

**Étape 2 — le coût en licences Pro.** Les **7** personnes qui lisent régulièrement ou construisent :
**7** fois **8 400** FCFA, soit **58 800** FCFA par mois, ou **705 600** FCFA par an. Les **12**
bénévoles restent dehors : ils n'ont pas de licence, et **705 600** FCFA pour **7** personnes est
difficile à défendre devant un trésorier d'association.

**Étape 3 — la capacité.** Elle couvre tous les lecteurs sans licence, mais son prix au mois ne
dépend pas du nombre de personnes : elle vise les organisations à beaucoup de lecteurs. Pour **19**
personnes, l'argument ne tient pas encore.

**Étape 4 — la recommandation.** Une licence pour l'analyste, et un rapport publié **dans un espace
public en lecture** si l'organisation en dispose, ou une livraison PDF mensuelle pour les bénévoles :
la note doit chiffrer les deux et trancher.

**Attendu.** Une note de **10** lignes, trois chiffres (coût actuel, coût Pro, coût capacité), une
recommandation, et la phrase qui dit ce que l'association perd en échange.

---

## 11. Exercices autonomes

**Exercice 1.1.** Pour chacune des situations suivantes, dites quelle surface est concernée —
bureau, service, plateforme ou mobile — et si un compte payant est nécessaire : (a) écrire une mesure
sur son poste ; (b) programmer une actualisation chaque nuit ; (c) lire un rapport dans le train ;
(d) héberger la copie locale d'une table de ventes ; (e) recevoir un commentaire sur un visuel.

**Exercice 1.2.** Une équipe compte **1** auteur et **5** lecteurs. Calculez le coût mensuel et annuel
de deux options — cinq licences Pro, ou une capacité — et dites à partir de combien de lecteurs
l'arbitrage change de camp. Écrivez vos hypothèses, faute de quoi le chiffre ne vaut rien.

**Exercice 1.3.** Un collègue vous écrit : « J'ai publié mon rapport hier, et le directeur me dit
qu'il ne peut pas l'ouvrir. » Écrivez les **4** questions que vous posez avant de proposer quoi que ce
soit, dans l'ordre où vous les posez.

**Exercice 1.4.** Le rapport du fil rouge pèse **29,32** Mo une fois ses **12** tables exportées, dont
**240 000** lignes de ventes. Expliquez, en cinq lignes, pourquoi cette taille rend la question du
mode de connexion **peu urgente** sur ce projet, et dans quel cas elle deviendrait urgente.

**Exercice 1.5.** Reprenez la liste des **sept** erreurs fréquentes du chapitre et, pour chacune,
écrivez le symptôme que vous verriez dans une équipe — c'est-à-dire ce qui vous ferait dire
« l'erreur de la ligne 4 est en train de se produire chez nous ».

---

## 12. Correction détaillée

**Exercice 1.1.** (a) le bureau, gratuit : un poste suffit pour écrire une mesure ; (b) le service,
payant, puisqu'il faut publier un modèle et planifier sa recharge ; (c) le mobile, avec une licence de
lecture — ou la licence de quelqu'un qui la couvre ; (d) la plateforme, avec un hébergement qui ne
dépend pas du nombre de lecteurs ; (e) le service, avec une licence de lecture et les droits sur
l'espace.

**Exercice 1.2.** Cinq licences Pro : **5** fois **8 400** FCFA = **42 000** FCFA par mois, soit
**504 000** FCFA par an. Une capacité : un montant mensuel fixe indépendant du nombre de lecteurs,
mais nettement supérieur à **42 000** FCFA. L'arbitrage bascule quand la facture par personne dépasse
le prix de la capacité : cela dépend du tarif obtenu, donc de la région et du contrat — et c'est
pourquoi l'exercice exige vos hypothèses écrites. Sans elles, il n'y a pas de réponse défendable.

**Exercice 1.3.** (1) Avec quel compte le rapport a-t-il été publié, et de quel type est ce compte ?
(2) Dans quel espace de travail a-t-il été publié : un espace partagé ou un espace personnel ?
(3) Le rapport a-t-il été partagé directement, ou publié comme **application** ? (4) Le directeur a-t-il
une licence de lecture — et laquelle ? Ces quatre questions séparent les trois symptômes du chapitre :
compte sans licence, rapport sans droits, partage mal fait. Poser une question de plus — « quel message
exact s'affiche ? » — vous fera gagner encore un aller-retour.

**Exercice 1.4.** **29,32** Mo pour **12** tables et **293 120** lignes, c'est-à-dire **4 489 143**
cellules : un volume qui se charge en mémoire sur n'importe quel poste, et qui se recycle chaque nuit.
Le mode d'import convient donc, et la question de la connexion directe ne devient urgente que dans
trois cas : quand la donnée dépasse les limites de la formule retenue, quand l'entreprise a besoin
d'une donnée **à la seconde** — ce qui n'arrive pas sur un rapport journalier — ou quand une règle
interdit de copier la donnée ailleurs, ce qui est une contrainte juridique et non technique.

**Exercice 1.5.** Compte personnel : la publication échoue avec un message de type de compte.
Bureau pris pour un essai : personne ne travaille, tout le monde attend une version « complète ».
Espace personnel : le lien partagé renvoie un accès refusé à tout le monde. Lecteurs payants : la
moitié de l'équipe ne peut pas ouvrir le rapport, et le service informatique reçoit des demandes de
licence en urgence. Offre avancée à une personne : les lecteurs en formule simple ne voient rien de
ce qui a été publié dans cet espace. Prix de mémoire : la note de budget est contredite en réunion.
Fabric pris pour un prérequis : le projet attend une plateforme dont il n'avait pas besoin.

---

## 13. Mini-projet de chapitre — la note de licence d'une page

**Énoncé.** Vous devez obtenir de votre direction une décision sur la licence du rapport du fil
rouge, en **une** page. Le mini-projet se fait en trois temps.

1. **Le périmètre.** Nommez les lecteurs et leur rôle : qui construit, qui lit chaque semaine, qui lit
   une fois par mois. Pour chacun, dites **quelle décision** ce rapport aide à prendre. Un lecteur
   sans décision associée ne compte pas.
2. **Les trois formules.** Chiffrez, en FCFA par mois et par an : le poste seul, les licences Pro pour
   les lecteurs nommés, et la capacité. Donnez la source de chaque prix et sa date.
3. **La recommandation.** Une phrase, un chiffre, une condition de révision — par exemple « à revoir
   au-delà de **20** lecteurs, ou au prochain changement de tarif ».

**Barème indicatif** : périmètre nommé avec les décisions associées (**6** points) · trois formules
chiffrées avec source et date (**6** points) · recommandation argumentée et conditionnée (**6** points)
· sur **18** points.

> **Pourquoi ce mini-projet.** C'est le seul livrable du module qu'un directeur lira **avant** de voir
> le rapport. La compétence qui s'achète est rare : la plupart des candidats savent construire un
> visuel, très peu savent expliquer pourquoi trois personnes doivent payer pour le regarder.

---

## 14. Résumé du chapitre

| Notion | Mesure du module | Ce qu'elle enseigne |
|---|---|---|
| Surfaces | **4** — bureau, service, plateforme, mobile | chaque surface a sa question de licence |
| Construction locale | **0** FCFA | on apprend tout l'outil sans licence |
| Formule simple | **8 400** FCFA par utilisateur et par mois | le partage se paie par personne |
| Formule avancée | **14 400** FCFA par utilisateur et par mois | ne se partage pas avec des lecteurs simples |
| Seuil de bascule | **F64**, soit **64** unités de capacité | au-delà, les lecteurs deviennent gratuits |
| Pilote type | **4** personnes, **33 600** FCFA par mois, **403 200** FCFA par an | une demande de budget se chiffre |
| Leçon du module précédent | **7 940 000** FCFA pour **4** ouvertures | le rapport que personne n'ouvre est le vrai coût |
| Valeurs de contrôle | **8** valeurs, **8** identiques des deux côtés | le rapport doit rendre les chiffres du socle |

**Instrument.** Les valeurs de ce chapitre sont reproductibles : `python3 tools/mesures_M14.py`
recalcule les **10** valeurs du rapport sur le modèle en étoile, les compare à la mesure
opérationnelle de M12, pèse les **12** tables d'import et publie la grille de conception. Les prix, eux,
ne se mesurent pas : ils se **datent**, et la date est dans le texte.

**Le module en une ligne.** M14 branche la restitution sur le modèle : huit chapitres qui prennent les
**12** tables de M13 et les **10** indicateurs de M12 et en font un rapport publié, actualisé,
protégé et relu. Ce premier chapitre a réglé la question d'argent et posé les quatre surfaces ;
le suivant fait entrer la donnée.

---

## 15. À retenir

1. **Quatre surfaces, un seul ordre :** on construit sur le poste, on partage dans le service, on
   industrialise sur la plateforme, on consulte sur le mobile. L'application de bureau est gratuite ;
   c'est le **partage** qui se paie, par personne.
2. **Le seuil F64 est le seul point de rupture de l'échelle.** En dessous, le coût suit le nombre de
   lecteurs ; au-delà, il suit la machine. Une organisation ne bascule pas pour une raison technique,
   mais parce que la facture par personne est devenue absurde.
3. **Une demande de licence se chiffre :** **4** personnes coûtent **403 200** FCFA par an. Le
   contre-argument n'est jamais « c'est trop cher », c'est « qui va décider quoi avec ce rapport ».

> **À retenir.** Le meilleur rapport du monde ne vaut rien s'il ne peut pas être ouvert, et la
> question « qui peut l'ouvrir ? » se tranche **avant** la première requête, pas après le premier
> refus. Retenez les trois nombres qui suffisent à tenir une conversation professionnelle :
> **0** FCFA pour construire, **8 400** FCFA par lecteur et par mois pour partager, **64** unités de
> capacité à partir desquelles les lecteurs deviennent gratuits.

---

## 16. Évaluation formative

1. Citez les quatre surfaces de l'écosystème et ce qu'on fait dans chacune.
2. Le poste de travail est-il une version d'essai limitée dans le temps ?
3. Combien coûte, par mois et par an, un pilote de **4** personnes en formule simple ?
4. Qu'est-ce qui, dans l'échelle des licences, change l'économie et à partir de quel seuil ?
5. Pourquoi une offre avancée achetée pour une seule personne est-elle souvent une erreur ?
6. Quelle est la différence entre un espace de travail et une application, du point de vue du lecteur ?
7. Le rapport du fil rouge pèse **29,32** Mo. Faut-il s'en inquiéter ?
8. Un collègue n'arrive pas à ouvrir un rapport publié : citez les trois causes possibles et la
   question qui distingue chacune.
9. Pourquoi la note de licence se limite-t-elle à **une** page ?
10. Que fait une organisation qui n'a pas de licence ? Donnez les quatre réponses, dans l'ordre.

**Corrigé.** 1. Bureau (construire), service (partager et actualiser), plateforme (héberger et
industrialiser), mobile (consulter). 2. Non : il est gratuit sans limite de durée, et la construction
complète d'un rapport s'y fait sans licence. 3. **33 600** FCFA par mois, **403 200** FCFA par an.
4. La lecture : à partir du seuil **F64**, les lecteurs consultent sans licence payante, et le coût
suit la machine au lieu du nombre de personnes. 5. Parce que cette offre ne se partage pas avec des
lecteurs en formule simple : le rapport publié dans cet espace reste invisible pour eux. 6. Dans
l'espace de travail on voit tout le contenu et l'on peut modifier ; dans l'application on ne voit que
ce qui a été publié, et l'on ne modifie rien. 7. Non : **12** tables, **293 120** lignes et **4 489
143** cellules se chargent sans difficulté, et la recharge nocturne suffit à un rapport journalier.
8. Il n'a pas de licence de lecture ; il n'a pas les droits sur l'espace ou l'application ; le rapport
n'a pas été publié dans un espace partagé. La question qui tranche : quel compte utilise-t-il, et
quel message exact voit-il ? 9. Parce qu'elle est lue par un décideur, et qu'une décision se prend sur
un périmètre, trois chiffres et une recommandation. 10. Travailler au poste et livrer un fichier ;
utiliser une formule déjà payée par l'organisation ; changer d'outil pour un usage précis ; demander
un pilote chiffré avec une durée et deux indicateurs de succès.
