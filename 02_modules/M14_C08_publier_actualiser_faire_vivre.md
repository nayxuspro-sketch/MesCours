# Module M14.C08 — Publier, actualiser, faire vivre

**Outils : DuckDB 1.5.5 (exécuté) ; pandas (non requis). Power BI Desktop et le Service sont *cités* —
l'outil n'est pas installé dans cet atelier (règle §1.5). La sécurité, les alertes et la taille du modèle
sont **mesurées** sur le socle à chaque exécution de `tools/mesures_M14.py`, section `publication`.**

![La grille de conception en 18 points, ses 4 familles et les 6 ajouts du module (production : `tools/figures_M14.py`)](../figures/M14_C08_grille_conception_enrichie.svg)

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous savez :

1. **distinguer l'espace de travail de l'application**, et dire qui voit quoi : le rapport du fil rouge
   a **6** magasins, **5** qui vendent, et un dépôt sans aucune ligne de vente ;
2. **poser la sécurité au niveau des lignes** et en connaître la limite : un rôle par magasin, des vues
   allant de **11,1 %** à **34,1 %** du chiffre d'affaires — et une table de stock de **6 776** lignes
   qui ne porte aucun magasin, donc que le filtre ne protège pas ;
3. **planifier l'actualisation** : **12** tables, **293 120** lignes, **29,32** Mo, soit **2,9 %** de la
   limite d'un modèle Pro — la question n'est pas la taille, c'est la fréquence ;
4. **régler un abonnement et une alerte utiles** : le taux de rupture mensuel va de **4,58 %** à
   **10,40 %** pour une moyenne de **7,29 %** ; un seuil à **10 %** se serait déclenché **2** fois en
   **44** mois ;
5. **passer les 7 tests de mise en production** et la **grille de conception en 18 points** enrichie de
   ses **6** sous-questions, avant de déclarer le rapport publié.

---

## 2. Pourquoi cette notion est importante

Un rapport qui vit dans un fichier personnel n'est pas un rapport : c'est un brouillon. Publier, c'est
lui donner une adresse, des lecteurs, un propriétaire — et des obligations.

**La première est la confidentialité.** Le rapport du fil rouge contient les ventes de **6** magasins. Un
directeur régional qui voit les **80 838** lignes d'un magasin voisin n'a pas commis de faute : le rapport
lui a donné. La sécurité au niveau des lignes n'est pas une option avancée, c'est la condition pour que
le rapport circule. Et elle a une limite mesurée : elle ne filtre que les tables qui portent un magasin —
la table de stock, avec ses **6 776** lignes produit × mois, n'en porte aucun.

**La deuxième est la fraîcheur.** Un rapport qui affiche les chiffres d'avant-hier sans le dire est pire
qu'un rapport absent : il fait décider sur des données mortes. L'actualisation planifiée existe pour
cela, et son réglage se déduit de la source — une **8** ou **48** fois par jour. Ici, la source bouge une
fois par nuit.

**La troisième est la vie du rapport.** Un rapport publié reçoit des retours ; le module porte d'ailleurs
un second projet construit sur **11** retours d'un comité. Publier sans prévoir la version 2, c'est
garantir que la version 2 se fera sans vous — dans un fichier Excel, à côté.

---

## 3. Explication simple — publier, c'est signer

Publier un rapport, c'est signer trois engagements :

- **un public** : qui le voit, et qui ne le voit pas — par permission et par filtre de sécurité ;
- **une fraîcheur** : quand la donnée se rafraîchit, et comment on s'en aperçoit si elle échoue ;
- **un propriétaire** : une personne nommée qui répond des chiffres, corrige les défauts et décide de
  la version suivante.

Le reste — l'espace de travail, l'application, les abonnements — n'est que l'outillage de ces trois
engagements. Et le test qui dit si la publication est réussie est simple : un collègue qui n'a jamais vu
le rapport peut-il **s'y fier sans appeler personne** ? Si la réponse est non, il reste du travail : une
définition à écrire, un filtre à poser, une actualisation à surveiller.

---

## 4. Vocabulaire essentiel

| Terme | Ce qu'il désigne sur le fil rouge |
|---|---|
| **Espace de travail** | le conteneur qui rassemble le rapport, le modèle et les droits — l'atelier |
| **Application** | la version publiée pour les lecteurs : un paquet de pages, sans les outils de conception |
| **Permission** | le droit d'un compte sur l'espace de travail : administrer, modifier, ou seulement lire |
| **Rôle de sécurité** | le filtre de lignes appliqué à un lecteur : un par magasin, **6** en tout |
| **Sécurité au niveau des lignes** | le mécanisme qui ne montre à un lecteur que les lignes qui le concernent |
| **Actualisation planifiée** | le rendez-vous quotidien qui relit la source et recharge le modèle |
| **Passerelle** | le pont entre le service et la source restée sur le réseau interne |
| **Modèle réutilisable** | un modèle publié que plusieurs rapports partagent, plutôt que cinq copies |
| **Abonnement** | l'envoi automatique d'une page, à une heure fixe, à une liste de destinataires |
| **Alerte** | la notification déclenchée par un seuil sur une mesure : rupture au-delà de **10 %** |
| **Ligne de base** | la version publiée et figée, à laquelle les versions suivantes se comparent |
| **Cycle de vie** | les étapes d'un rapport : brouillon, publié, révisé, retiré |

> **Définition.** Un **espace de travail** est le conteneur de droits qui rassemble les rapports, les
> modèles et les personnes. Il se distingue de l'**application** : l'espace est l'atelier, l'application
> est la vitrine — les lecteurs entrent par la vitrine, et n'ont pas besoin de savoir comment l'atelier
> est rangé.

> **Définition.** La **sécurité au niveau des lignes** — *row-level security* — filtre les lignes qu'un
> lecteur peut voir, selon son compte. Elle s'applique au modèle, pas au visuel : c'est ce qui la rend
> robuste — et ce qui oblige à vérifier que **chaque table** porte la colonne qui la rend possible.

> **Définition.** L'**actualisation planifiée** est le rendez-vous qui relit la source et recharge le
> modèle. Sa fréquence se déduit de la vitesse à laquelle la source change, jamais de la puissance de la
> licence : actualiser toutes les heures une donnée qui bouge une fois par nuit coûte sans rien apporter.

---

## 5. Cours approfondi

### 5.1 L'espace de travail et l'application

Un rapport ne se partage pas comme un fichier. Trois étages, à ne pas confondre :

1. **l'espace de travail** porte le modèle, le rapport et les droits de ceux qui le construisent ;
2. **l'application** publie une sélection de pages pour les lecteurs, avec ses propres droits ;
3. **le partage direct** d'un rapport reste possible, mais il ne passe pas par la vitrine : il faut alors
   gérer les droits au cas par cas, et c'est ainsi qu'on finit par ne plus savoir qui voit quoi.

Le fil rouge tient dans un espace de travail nommé, avec un modèle de ventes, trois pages de fond, deux
pages de détail et une page d'aide. Les lecteurs reçoivent l'application ; les constructeurs gardent
l'accès à l'espace. Une règle simple pour un atelier : **les droits se donnent par groupe, jamais par
personne** — un nouvel arrivant dans un magasin hérite du groupe de son magasin, et personne n'oublie
de le retirer quand il part.

### 5.2 La sécurité au niveau des lignes, et sa limite

**6** magasins, **6** rôles : chaque directeur voit ses lignes de vente, ses tickets et sa part du
réseau. Le tableau est le cœur de la démonstration :

| Magasin | Lignes de vente | Tickets | Part du chiffre d'affaires |
|---|---|---|---|
| Ouaga 2000 | **80 838** | **49 474** | **34,1 %** |
| Gounghin | **51 794** | **32 123** | **22,0 %** |
| Bobo Kibidwé | **47 497** | **29 321** | **19,9 %** |
| Koudougou Centre | **30 863** | **18 742** | **13,0 %** |
| Kaya Marché | **26 199** | **15 552** | **11,1 %** |
| Dépôt central | **0** | **0** | aucune vente |

Deux constats, et une limite. Le premier constat : le filtre fonctionne — chaque directeur voit sa part,
et la somme des cinq parts redonne le chiffre du réseau. Le deuxième : le dépôt voit un rapport **vide**,
parce qu'il ne vend pas ; c'est son rôle, mais cela doit être écrit, sinon la première réunion passera à
chercher la panne. Et la limite, celle qui coûte cher : **la sécurité au niveau des lignes ne filtre que
les tables qui portent la colonne du filtre**. La table de stock, **6 776** lignes de produit × mois,
ne porte aucun `id_magasin` : la rotation affichée reste celle du réseau entier, pour tout le monde. La
conséquence est immédiate : soit on borne la question — la rotation est un indicateur de réseau —, soit
on descend la colonne magasin dans la table, et l'on refait le modèle.

> **Dans les faits.** Sur le socle, la logistique porte bien un magasin — **264** lignes, dont **44**
> pour le dépôt —, et les vendeurs en portent un aussi : **22** vendeurs dans **5** magasins, aucun au
> dépôt. La table de stock, elle, n'en porte aucun. Une sécurité ligne à ligne se vérifie donc **table
> par table**, avant publication.

### 5.3 Tester la sécurité, pas la déclarer

Un rôle déclaré n'est pas un rôle testé. Trois tests, à passer avant publication :

1. **se mettre dans la peau d'un magasin** : ouvrir le rapport avec un compte de test filtré, et vérifier
   les trois totaux — la page, ses visuels, le détail ;
2. **vérifier la somme** : la part des cinq magasins qui vendent doit redonner le chiffre du réseau —
   **34,1 %** à **11,1 %**, sans reste ;
3. **vérifier ce qui n'est pas filtré** : sortir la table de stock dans un visuel et confirmer que la
   rotation est bien celle du réseau, ou retirer le visuel de l'application.

Un quatrième test vaut pour tous les rôles : la page d'aide. Elle doit présenter les mêmes définitions
quel que soit le lecteur — un filtre de sécurité qui change le contenu de l'aide transforme la
documentation en malentendu.

### 5.4 L'actualisation planifiée et la passerelle

Le modèle du fil rouge tient en **12** tables, **293 120** lignes et **29,32** Mo — **2,9 %** de la limite
d'un modèle Pro. La taille n'est donc pas un sujet ; la fréquence en est un. Trois questions, dans
l'ordre :

1. **à quelle vitesse la source change-t-elle ?** Ici, une fois par nuit : **8** actualisations autorisées
   par jour en Pro suffisent largement, et **48** en PPU seraient du gaspillage ;
2. **quand actualiser ?** Avant l'ouverture, jamais pendant la réunion : un rapport qui se rafraîchit à
   9 h 05 affiche deux chiffres différents dans la même heure ;
3. **que se passe-t-il si l'actualisation échoue ?** Quelqu'un doit le savoir : une notification, un
   propriétaire nommé, et une règle écrite — « après deux échecs, la page d'aide affiche la date de la
   dernière actualisation réussie ».

La **passerelle** n'existe que si la source reste sur le réseau interne — un dossier partagé, une base
non exposée. Elle est alors un point de défaillance à surveiller comme les autres, et elle se documente :
machine, compte de service, qui la redémarre.

### 5.5 Les 7 tests avant mise en production

Sept contrôles, tous déjà outillés dans le module, et tous passés sur le rapport avant publication :

| # | Test | Ce qu'il vérifie |
|---|---|---|
| 1 | **Totaux aux trois niveaux** | page, visuel, détail : **15 595 154 955** FCFA partout |
| 2 | **Grain affiché** | le niveau de détail est écrit sous le visuel |
| 3 | **Vides expliqués** | les **7** cases vides de la matrice et le dépôt sans vente sont légendés |
| 4 | **Dates cohérentes** | une seule table de dates, une seule relation active, **44** mois |
| 5 | **Deux définitions déclarées** | panier **107 396** FCFA par ticket, **65 749** par ligne |
| 6 | **Ouverture mesurée** | moins de trois secondes, chronomètre en main |
| 7 | **Relecture par un pair** | la grille en **18** points, remplie par quelqu'un d'autre |

Ces sept tests ne sont pas une formalité : ce sont les sept questions qui seront posées en réunion par
des gens qui, eux, n'ont pas construit le rapport.

### 5.6 La grille de conception en 18 points, enrichie

La grille héritée de M10 tient en **18** points répartis **4 + 5 + 5 + 4** — une décision servie, la
justesse, la lisibilité, l'utilisation — et **18** questions fermées : une question se répond oui ou non,
avec une preuve sous les yeux. Le module l'a enrichie de **6** sous-questions, sans changer le total :

| Famille | Points | Ajouts du module |
|---|---|---|
| **1. La décision servie** | **4** | aucun |
| **2. La justesse** | **5** | cohérence des totaux · granularité · gestion des vides |
| **3. La lisibilité** | **5** | accessibilité · légende |
| **4. L'utilisation** | **4** | performance |

Trois des ajouts portent sur la justesse, parce que la grille d'origine ne demandait pas si les totaux
de la page, du visuel et du détail concordaient — et c'est l'erreur la plus fréquente d'un rapport
construit par accumulation. Les deux ajouts de lisibilité viennent du chapitre 6 — contraste, légende,
unité —, et celui de l'utilisation vient du chapitre 7 : moins de trois secondes à l'ouverture. La
planche de ce chapitre porte les **18** questions, avec les ajouts marqués.

> **À retenir.** Une grille de conception n'est pas une checklist de confort : chaque question fermée
> remplace une discussion de réunion. Les **6** ajouts du module portent sur des erreurs vues trois fois
> dans les chapitres précédents — totaux, grain, vides, contraste, légende, lenteur.

La grille se passe **deux fois** : par l'auteur avant publication, puis par un pair. Un rapport relu par
la personne qui l'a construit ne passe pas le test de la relecture — elle lit ce qu'elle a voulu écrire,
pas ce qui est affiché.

### 5.7 Les modèles réutilisables et la certification

Le rapport du fil rouge consomme un modèle de ventes qui servira aussi aux modules suivants : un
**modèle réutilisable** — un modèle publié, partagé par plusieurs rapports — évite les copies divergentes.
Trois bénéfices, un risque :

- **un seul endroit** où la définition du chiffre d'affaires net existe, donc un seul endroit à corriger ;
- **une seule actualisation** pour cinq rapports, donc une seule facture de fraîcheur ;
- **une seule sécurité** à tester — la même pour tous les rapports qui consomment le modèle ;
- le risque : **le modèle partagé devient un point de défaillance unique**, et le modifier engage tous ses
  consommateurs. Un modèle partagé se modifie donc par version, avec une note de changement.

> **Attention.** Un modèle partagé est un **point de défaillance unique** : une mesure modifiée pour un
> rapport change les chiffres des autres, sans qu'aucun lecteur n'ait rien demandé. Une modification de
> modèle partagé se fait par version, avec une note de changement et une date.

La **certification** va un cran plus loin : elle signale aux lecteurs que le modèle a été relu et
approuvé. Un modèle certifié ne se modifie pas pour un besoin d'équipe : il se modifie pour un besoin
documenté, testé et annoncé.

### 5.8 Abonnements et alertes

Un rapport consulté une fois par mois ne sert à rien ; un rapport qui vient à vous sert tous les jours.
L'**abonnement** envoie une page à heure fixe — le lundi à 7 h, le tableau de bord du réseau —, et
l'**alerte** se déclenche sur un seuil :

- le taux de rupture mensuel du socle va de **4,58 %** à **10,40 %**, pour une moyenne de **7,29 %** sur
  **44** mois ;
- un seuil à **10 %** se serait déclenché **2** fois — assez rare pour être lu, assez fréquent pour ne
  pas être ignoré ;
- un seuil à **8 %** n'aurait **rien** signalé : une alerte qui ne se déclenche jamais finit par être
  supprimée, puis oubliée.

> **Définition.** Une **alerte** est une règle posée sur une mesure : au-delà d'un seuil, un message part
> vers quelqu'un qui peut agir. Un seuil se choisit sur l'historique de la mesure, jamais sur une
> intuition — sans quoi l'alerte se déclenche trop, ou jamais, et dans les deux cas elle est ignorée.

Trois règles pour une alerte utile : un seuil choisi **sur l'historique**, un destinataire qui **peut
agir**, et une revue annuelle des alertes — la moitié des alertes d'un rapport vieillissent mal.

> **Attention.** Un abonnement par courriel transporte une **copie** des chiffres, avec la date de
> l'envoi mais sans le contexte du rapport. Un destinataire qui imprime la page pour la commenter
> travaille sur une version figée : la page d'aide doit rappeler la date de la dernière actualisation et
> le fait que l'abonnement est une photographie, pas le rapport.

### 5.9 Faire vivre le rapport : la boucle de retour

Publier est le début d'un cycle : usage, retours, version 2. Le module en porte la preuve dans son second
projet — **11** retours d'un comité qui deviennent autant de décisions de conception. Trois questions
structurent cette boucle :

1. **qui l'utilise vraiment ?** Une page consultée par personne est une page à retirer ;
2. **quels retours reviennent ?** Un mot-clé oublié, un chiffre contesté deux fois, une définition
   absente — ce sont des corrections, pas des opinions ;
3. **que garde-t-on ?** Une version publiée sert de **ligne de base** : la version 2 se compare à elle, et
   les chiffres ne changent pas sans être expliqués.

### 5.10 Trois clics, et quelqu'un s'en sert

Un rapport publié se mesure : le nombre de lecteurs, les abonnements actifs, et le fait que quelqu'un
trouve le chiffre **sans appeler**. Trois contrôles simples, à faire un mois après la publication :

1. **usage réel** : combien de personnes ont ouvert le rapport, et combien d'abonnements sont actifs ;
2. **autonomie** : personne n'a demandé par message où se trouve un chiffre — la page d'aide a répondu ;
3. **confiance** : les chiffres du rapport sont ceux des décisions prises, y compris quand ils
   contredisent une impression.

Un rapport qui échoue à ces trois contrôles n'est pas mauvais : il est **inachevé**, et la prochaine
version commence par là.

### 5.11 Ce qui se retire, et comment

Faire vivre un rapport, c'est aussi savoir l'arrêter. Un rapport se retire quand sa décision n'existe
plus, quand une source disparaît, ou quand il a été remplacé — et il se retire proprement : annonce aux
lecteurs, redirection vers la version qui remplace, archivage du modèle, désactivation des abonnements et
des alertes. Un rapport qu'on laisse en ligne « au cas où » continue d'envoyer des chiffres qu'aucun
propriétaire ne défend plus.

> **Conseil professionnel.** Avant la première publication, écrivez la **fiche de vie** du rapport :
> public, propriétaire, source, fréquence d'actualisation, rôles de sécurité, abonnements et alertes,
> date de la première revue. Une page. Elle se relit chaque trimestre, et c'est ce document qui permet de
> savoir, deux ans plus tard, pourquoi un chiffre est calculé comme il l'est.

---

## 6. Exemple concret — la mise en production du rapport, jour par jour

| Quand | Ce qui se fait | Le contrôle |
|---|---|---|
| **J-5** | grille en **18** points passée par l'auteur | les **6** ajouts sont satisfaits |
| **J-3** | relecture par un pair, sur le rapport publié en test | les **7** tests, dont les totaux aux trois niveaux |
| **J-2** | rôles de sécurité créés et testés, magasin par magasin | **11,1 %** à **34,1 %**, dépôt vide et expliqué |
| **J-1** | actualisation planifiée et passerelle réglées | la nuit suivante, l'actualisation passe |
| **J** | publication de l'application aux **6** groupes | chacun ouvre et voit sa part |
| **J+7** | abonnements et alertes activés | seuil de rupture à **10 %**, **2** déclenchements en **44** mois |
| **J+30** | revue d'usage et ligne de base | les trois contrôles d'autonomie, et la version 2 cadrée |

Ce calendrier n'a rien de cérémoniel : il empêche la seule erreur qui coûte vraiment — publier un rapport
le jour où on le montre, et découvrir en réunion que la moitié des lecteurs voient les chiffres de
l'autre moitié.

---

## 7. Démonstration pas à pas — publier le rapport

L'outil n'est pas installé dans cet atelier : ces gestes se rejouent devant votre écran.

1. **Créez l'espace de travail** et nommez-le ; vérifiez que le modèle et le rapport y sont bien tous les
   deux.
2. **Créez les 6 rôles** de sécurité — un par magasin — et testez chacun avec un compte de test.
   Contrôle : **80 838** lignes pour Ouaga 2000, **26 199** pour Kaya Marché, **0** pour le dépôt.
3. **Vérifiez la somme** des parts visibles par les cinq magasins qui vendent : elle doit redonner le
   chiffre d'affaires du réseau, **15 595 154 955** FCFA.
4. **Sortez la table de stock** dans un visuel de test et constatez qu'elle n'est pas filtrée : elle ne
   porte pas de magasin. Décidez, et écrivez la décision.
5. **Réglez l'actualisation planifiée** : une fois par nuit, avant ouverture, avec un propriétaire nommé.
6. **Vérifiez la passerelle** si la source est interne, et notez le compte de service dans le dossier.
7. **Publiez l'application** en choisissant les pages visibles — les trois pages de fond, les deux pages
   de détail et la page d'aide.
8. **Donnez les droits par groupe**, jamais par personne : un groupe par magasin, plus un groupe pour la
   direction.
9. **Passez les 7 tests** de mise en production, dans l'ordre, et cochez-les un par un.
10. **Passez la grille en 18 points**, puis faites-la passer par un pair. Contrôle : les **6** ajouts du
    module sont satisfaits ou justifiés.
11. **Créez un abonnement** — la page Direction, le lundi à 7 h — et une **alerte** sur le taux de rupture
    au seuil de **10 %**.
12. **Écrivez la fiche de vie** du rapport et fixez la date de la première revue, un mois plus tard.

---

## 8. Erreurs fréquentes

1. **Confondre l'espace de travail et l'application.** Les lecteurs n'ont pas à naviguer dans l'atelier :
   ils reçoivent la vitrine.
2. **Déclarer les rôles sans les tester.** Un rôle non testé est un rôle qui montre les ventes du voisin :
   **6** rôles, **6** comptes de test.
3. **Oublier les tables qui ne portent pas la colonne du filtre.** La table de stock, **6 776** lignes
   sans magasin, reste visible en entier — et personne ne l'apprend avant la question gênante.
4. **Actualiser trop souvent.** **8** fois par jour pour une source qui bouge une nuit sur deux, c'est
   payer pour rien — et multiplier les échecs silencieux.
5. **Régler une alerte sans historique.** Un seuil à **8 %** sur une rupture qui vit entre **4,58 %** et
   **10,40 %** ne se déclenche jamais : l'alerte est morte à la naissance.
6. **Publier sans propriétaire.** Sans nom sur la porte, les corrections n'arrivent pas, et la version 2
   se fait ailleurs.

---

## 9. Bonnes pratiques professionnelles

1. **Donner les droits par groupe** : un groupe par magasin, un pour la direction, et rien d'autre.
2. **Tester la sécurité par compte**, pas par déclaration : les trois tests du chapitre, avant publication.
3. **Vérifier table par table** que les tables sensibles portent la colonne du filtre.
4. **Régler la fréquence sur la source**, jamais sur la licence : **8** ou **48** actualisations par jour
   ne se choisissent pas au hasard.
5. **Nommer un propriétaire** et écrire la fiche de vie du rapport.
6. **Choisir les seuils d'alerte sur l'historique** — de **4,58 %** à **10,40 %** ici — et revoir les
   alertes une fois par an.
7. **Passer les 7 tests et la grille en 18 points** avant de dire « publié ».
8. **Faire relire par un pair** qui n'a pas construit le rapport : c'est le seul test qui vaut pour tout
   le reste.

> **Boîte à outils.** La liste de publication tient en **7** lignes : espace de travail créé · application
> publiée · **6** rôles testés · actualisation planifiée et surveillée · **7** tests passés · grille en
> **18** points relue par un pair · fiche de vie écrite. Sept lignes, et le rapport est en production.

---

## 10. Exercice guidé

**Énoncé.** Le rapport est publié. Un directeur de magasin signale que sa page de rotation des stocks
affiche le même chiffre que celle de ses collègues. Le modèle est le bon, les rôles sont bons, et
pourtant le filtre ne protège pas cette page. Trouvez la cause, décidez, et écrivez-le.

**Étape 1 — vérifier le rôle.** Le compte de test du magasin de Kaya affiche bien **26 199** lignes de
vente et **15 552** tickets : la sécurité fonctionne sur les ventes.

**Étape 2 — inspecter la table en cause.** La table de stock porte le produit et le mois — **6 776**
lignes — mais **aucun** magasin. Le filtre de sécurité n'a donc rien à filtrer : la rotation affichée est
celle du réseau, pour tout le monde.

**Étape 3 — choisir.** Deux voies : garder la rotation comme indicateur de réseau, la retirer des pages
des magasins et l'expliquer ; ou descendre l'`id_magasin` dans la table de stock, et refaire le modèle
pour ce besoin.

**Étape 4 — écrire.** La décision retenue va dans la fiche de vie, avec sa raison, et le visuel porte la
mention correspondante. Sans cette ligne, la question reviendra tous les six mois.

**Attendu.** La table fautive identifiée, l'absence de colonne magasin constatée, l'arbitrage écrit, et
le visuel mis à jour ou retiré.

---

## 11. Exercices autonomes

**Exercice 8.1.** Citez les **6** rôles de sécurité du rapport, le nombre de lignes que chacun voit, et
expliquez en une phrase pourquoi le dépôt voit un rapport vide.

**Exercice 8.2.** Une table du modèle porte le stock par produit et par mois, sans magasin. Rédigez la
note de deux lignes qui explique ce que cela implique pour la sécurité, et la décision à prendre.

**Exercice 8.3.** Le taux de rupture mensuel vit entre **4,58 %** et **10,40 %**. Proposez un seuil
d'alerte, dites combien de fois il se serait déclenché en **44** mois, et justifiez le choix.

**Exercice 8.4.** Vous devez publier le rapport pour **6** groupes de lecteurs. Décrivez ce que vous
publiez — espace, application, droits — et les trois tests que vous passez avant.

**Exercice 8.5.** Un collègue propose de régler l'actualisation toutes les heures « pour être sûr ». Que
répondez-vous, avec trois arguments chiffrés sur ce modèle ?

---

## 12. Correction détaillée

**Exercice 8.1.** Six rôles, un par magasin : Ouaga 2000 — **80 838** lignes, **49 474** tickets ·
Gounghin — **51 794** et **32 123** · Bobo Kibidwé — **47 497** et **29 321** · Koudougou Centre —
**30 863** et **18 742** · Kaya Marché — **26 199** et **15 552** · Dépôt central — **0** ligne et
**0** ticket. Le dépôt ne vend pas : il porte du stock et de la logistique, pas de ventes, donc son
rapport de ventes est vide — ce qui doit être écrit dans la fiche de vie pour ne pas être pris pour une
panne.

**Exercice 8.2.** Note possible : « la table de stock (**6 776** lignes, produit × mois) ne porte pas
d'`id_magasin` : la sécurité au niveau des lignes ne peut donc pas la filtrer, et la rotation reste
celle du réseau pour tous les lecteurs. Décision : garder la rotation comme indicateur de réseau, la
retirer des pages de magasin, ou descendre `id_magasin` dans la table lors de la prochaine révision du
modèle. » La note dit le fait, la conséquence et la décision — sans quoi la question revient.

**Exercice 8.3.** Un seuil de **10 %** est défendable : il se serait déclenché **2** fois en **44** mois,
sur les deux mois les plus tendus, et une alerte rare est une alerte lue. Un seuil de **8 %** n'aurait
rien signalé — la moyenne mensuelle est de **7,29 %** et le plancher de **4,58 %** —, donc l'alerte
n'aurait produit que du bruit inexistant : pire, elle aurait donné l'impression d'une surveillance.
Le seuil se choisit sur l'historique, et se revoit une fois par an.

**Exercice 8.4.** Ce qu'on publie : **un** espace de travail qui porte le modèle et le rapport, **une**
application qui expose les trois pages de fond, les deux pages de détail et la page d'aide, et **6**
groupes de lecteurs — un par magasin — auxquels s'ajoute un groupe de direction. Les trois tests : le
**compte de test** de chaque magasin affiche sa part et la bonne somme (**34,1 %** à **11,1 %**) ; les
**totaux aux trois niveaux** donnent **15 595 154 955** FCFA ; l'**ouverture** de la page Direction reste
sous trois secondes.

**Exercice 8.5.** Réponse : la source bouge une fois par nuit, donc **8** actualisations par jour
suffisent — la fréquence horaire produirait 24 lectures pour une donnée identique. Le modèle ne pèse que
**29,32** Mo, soit **2,9 %** de la limite d'un modèle Pro : la contrainte n'est pas la taille, c'est le
nombre d'échecs possibles — et chaque échec silencieux est un rapport faux. Enfin, une actualisation
pendant les heures d'ouverture fait cohabiter deux fraîcheurs dans la même journée, ce qui est exactement
ce que le rapport cherche à éviter.

---

## 13. Mini-projet de chapitre — le dossier de mise en production

**Énoncé.** Produisez le **dossier de mise en production** du rapport : la fiche de vie, les **6** rôles
de sécurité avec leurs tests, le réglage de l'actualisation, la liste des **7** tests passés, la grille en
**18** points remplie, et le plan de la version 2 construit sur les retours du comité.

**Barème indicatif** : la fiche de vie complète — public, propriétaire, source, fréquence, rôles
(**4** points) · les **6** rôles testés, avec les lignes vues par chacun (**4** points) · les **7** tests
passés et datés, dont la mesure d'ouverture (**4** points) · la grille en **18** points remplie et relue
par un pair (**4** points) · le plan de la version 2 appuyé sur les retours, avec la ligne de base
(**2** points) · sur **18** points.

> **Pourquoi ce mini-projet.** Parce que la publication est ce qui transforme un travail en service : à
> partir de là, quelqu'un décide avec vos chiffres. Le dossier de mise en production est la pièce qui
> permet à un successeur de prendre le rapport en main sans vous appeler — la définition même d'un
> livrable professionnel.

---

## 14. Résumé du chapitre

| Notion | Mesure du module | Ce qu'elle enseigne |
|---|---|---|
| Espace et application | **6** groupes de lecteurs | l'atelier pour construire, la vitrine pour lire |
| Sécurité ligne à ligne | **80 838** à **26 199** lignes vues, **0** au dépôt | un rôle se teste par compte, pas par déclaration |
| Limite de la sécurité | **6 776** lignes de stock sans magasin | une table non filtrable doit être connue et décidée |
| Actualisation | **12** tables, **293 120** lignes, **29,32** Mo (**2,9 %** d'un modèle Pro) | la fréquence se règle sur la source |
| Alertes | **4,58 %** à **10,40 %**, moyenne **7,29 %** | un seuil à **10 %** se déclenche **2** fois en **44** mois |
| Les 7 tests | totaux, grain, vides, dates, définitions, ouverture, relecture | ce sont les questions posées en réunion |
| La grille | **18** points, **4 + 5 + 5 + 4**, **6** ajouts | une question fermée, une preuve, un pair |

**Instrument.** `python3 tools/mesures_M14.py` recalcule les lignes visibles par chaque rôle, le total
des parts, la taille du modèle face à la limite de licence, la série mensuelle de rupture et le seuil
d'alerte, et le compte des tests de mise en production.

**Le module en une ligne.** Les sept chapitres précédents ont construit un rapport ; celui-ci l'a mis en
service — avec des droits testés, une fraîcheur surveillée, des alertes choisies sur l'historique et une
grille relue par un pair. Un rapport publié sans ces quatre pièces n'est pas un livrable : c'est une
démonstration.

---

## 15. À retenir

1. **Les droits se donnent par groupe et se testent par compte.** **6** rôles, six vérifications : de
   **80 838** lignes vues à **26 199**, et un dépôt qui voit un rapport vide — expliqué, pas caché.
2. **La sécurité a une limite écrite : les tables qui ne portent pas la colonne du filtre.** La table de
   stock, **6 776** lignes, n'est pas filtrable — on l'accepte, on la retire, ou on refait le modèle.
3. **Fréquence, alerte et livraison se règlent sur l'historique.** **8** actualisations par jour,
   un seuil de rupture à **10 %** qui se serait déclenché **2** fois en **44** mois, et **7** tests avant
   de dire « publié ».

> **À retenir.** Publier n'est pas envoyer : c'est nommer un propriétaire, régler une fraîcheur,
> vérifier des droits et accepter d'être relu. Un rapport publié avec ces quatre éléments vit des années ;
> sans eux, il meurt à la première contradiction chiffrée.

---

## 16. Évaluation formative

1. Quelle est la différence entre un espace de travail et une application ?
2. Combien de rôles de sécurité porte le rapport, et que voit le dépôt central ?
3. Quelle table du modèle ne peut pas être filtrée par magasin, et quelle en est la conséquence ?
4. Citez les trois tests de sécurité à passer avant publication.
5. Quelle fréquence d'actualisation retenez-vous pour ce rapport, et pourquoi ?
6. Que se passe-t-il si une actualisation planifiée échoue, et qui doit le savoir ?
7. Citez les 7 tests de mise en production, dans l'ordre.
8. Combien de points et de familles compte la grille de conception, et quels sont ses 6 ajouts ?
9. Quel seuil d'alerte proposez-vous pour le taux de rupture, et combien de fois se serait-il déclenché ?
10. Que contient la fiche de vie d'un rapport, et à quoi sert-elle ?

**Corrigé.** 1. L'**espace de travail** est le conteneur de construction — modèle, rapport, droits des
constructeurs ; l'**application** est la version publiée pour les lecteurs, avec ses propres droits.
2. **6** rôles, un par magasin ; le dépôt central voit **0** ligne de vente, **0** ticket, et son rapport
de ventes est vide — ce qui s'écrit. 3. La table de **stock** — **6 776** lignes de produit × mois —
ne porte aucun `id_magasin` : la rotation reste celle du réseau pour tous les lecteurs, et la décision
s'écrit. 4. Le compte de test par magasin, la somme des parts (**34,1 %** à **11,1 %**), et la
vérification de ce qui n'est **pas** filtré. 5. Une fois par nuit, avant ouverture : la source change une
fois par jour, le modèle pèse **29,32** Mo, et **8** actualisations par jour sont autorisées en Pro — donc
largement assez. 6. Une notification part vers un propriétaire nommé, et la règle écrite prévoit
d'afficher la date de la dernière actualisation réussie sur la page d'aide. 7. Totaux aux trois niveaux ·
grain affiché · vides expliqués · dates cohérentes · deux définitions déclarées · ouverture sous trois
secondes · relecture par un pair. 8. **18** points en **4** familles — **4 + 5 + 5 + 4** — avec **6**
ajouts : cohérence des totaux, granularité, gestion des vides, accessibilité, légende, performance.
9. Un seuil de **10 %** : le taux mensuel vit entre **4,58 %** et **10,40 %** pour une moyenne de
**7,29 %**, et le seuil se serait déclenché **2** fois en **44** mois — une alerte rare est une alerte
lue. 10. La fiche de vie porte le public, le propriétaire, la source, la fréquence d'actualisation, les
rôles de sécurité, les abonnements et alertes, et la date de la première revue : elle permet de savoir
deux ans plus tard pourquoi un chiffre est calculé comme il l'est.
