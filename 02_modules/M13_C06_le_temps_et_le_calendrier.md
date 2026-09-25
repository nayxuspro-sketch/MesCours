# Module M13.C06 — Le temps et le calendrier

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous savez :

1. **construire et brancher une dimension de temps** : le socle porte un calendrier de **1 339**
   lignes, du 2023-01-01 au 2026-08-31, et la jointure rend **240 000** lignes sur **240 000** —
   c'est la fermeture du trou déclaré au chapitre 4, où la dimension de temps n'était branchée sur
   aucun fait ;
2. **mesurer la complétude du calendrier dans les deux sens** : les jours du calendrier sans vente,
   et les dates des faits absentes du calendrier. Sur le socle, la première réponse vaut **0** et la
   seconde vaut **0** pour les ventes, mais **13** dates de livraison tombent hors du calendrier,
   pour **46** commandes et **32 772 075** FCFA ;
3. **lire le temps par attributs, pas par la date** : les jours fériés (**18**), le dimanche
   (**829 983 276** FCFA, soit **5,32 %** du chiffre d'affaires), le poids du quatrième trimestre
   (**29,7 %**) et celui de décembre dans ce trimestre (**33,6 %**) ne se calculent pas sur une
   colonne de date : ils se lisent dans la dimension ;
4. **comparer deux périodes honnêtement** : sur le même socle, le même chiffre d'affaires se lit
   **, 28,9 %**, ou **+ 15,4 %**, selon que l'année en cours est comparée entière ou sur les
   **8** premiers mois — **44,3** points d'écart pour une seule erreur de borne ;
5. **choisir la nature du temps dans une table de faits** : une date de vente, **3** dates dans un
   fait de commande ou d'encaissement, un mois dans **4** autres faits — et savoir ce que le modèle
   ne saura jamais dire, faute d'heure (**0** colonne d'heure sur **17**).

---

## 2. Pourquoi cette notion est importante

Le temps est la seule dimension qu'un modèle de données peut **remplir d'avance**. Les clients
arrivent au fil des ventes, les produits aussi ; les jours, eux, sont connus avant les faits, et même
avant l'ouverture du magasin. Un calendrier écrit une fois sert ensuite à tout le monde : il porte le
trimestre, le jour de la semaine, les fériés, l'exercice fiscal et les semaines commerciales, autant
d'attributs qu'aucune table de faits n'a envie de recalculer.

C'est aussi la dimension la plus souvent **déclarée et jamais branchée**. Le chapitre 4 a mesuré la
conformité des dimensions du socle et trouvé un résultat à zéro : la dimension de temps existe, elle
est propre, elle porte **1 339** lignes — et aucun fait ne la référence. Ce chapitre ferme ce trou,
et il explique pourquoi ce trou existe : un calendrier qui arrive dans un entrepôt avant les faits
reste inutile tant que personne ne l'a joint, et rien dans la base ne le signale.

La suite du raisonnement tient en trois pièges, tous mesurés dans ce chapitre. Le premier est une
**borne de temps** : comparer une année de **243** jours à une année complète produit un
effondrement de **, 28,9 %** qui n'existe pas. Le deuxième est une **date hors calendrier** : un
rapport qui joint en interne perd **46** commandes sans afficher la moindre erreur. Le troisième est
une **ambiguïté de vocabulaire** : le socle porte deux calendriers concurrents, la semaine
normalisée qui plafonne à **52** et la semaine commerciale qui monte à **53**. Trois pièges, aucune
faute de calcul, et des chiffres faux quand même.

---

## 3. Explication simple — le calendrier du mur et le cahier de caisse

Imaginez la salle de réunion d'un magasin. Sur le mur, un calendrier : une case par jour, avec la
date, le jour de la semaine, les jours fériés en rouge. Personne ne le remplit, il est imprimé
d'avance.

À côté, le cahier de caisse : une ligne par vente, avec la date du jour en marge. Il ne contient que
les jours où l'on a vendu quelque chose.

| | Calendrier du mur | Cahier de caisse |
|---|---|---|
| Qui le remplit | personne, il est imprimé | la caissière, à chaque vente |
| Combien de lignes | **1 339** jours | **240 000** ventes |
| Que dit-il de janvier | il existe, même si le magasin est fermé | rien, s'il n'y a pas de vente |
| Que porte-t-il en plus de la date | trimestre, semaine, férié, exercice | date, montant, produit, client |
| Sert à quoi | comparer, cumuler, compléter | raconter ce qui s'est passé |

Le geste de ce chapitre consiste à **poser le cahier à côté du calendrier du mur**. C'est tout :
on joint chaque vente à son jour. Et ce geste simple répond à des questions qu'aucune des deux
sources ne sait poser seule. Combien de dimanches compte l'année, et combien pèsent-ils ? Quel
chiffre d'affaires a été fait un jour férié ? Le mois de décembre pèse-t-il plus que les trois
autres mois du trimestre ? Le cahier de caisse ne le dira jamais ; le calendrier du mur le dit si on
le lui demande.

L'inverse est vrai aussi. Le calendrier du mur sait quel jour on n'a **pas** vendu : **1 339** cases
contre **1 339** jours travaillés sur le socle, donc aucune case vide. Sur un vrai magasin, cette
comparaison est le premier rapport qu'on ouvre, parce qu'une case vide au calendrier est soit une
fermeture légitime, soit une panne de caisse.

---

## 4. Vocabulaire essentiel

> **Définition.** Une **dimension de temps** (ou **calendrier**) est une table dont la ligne
> représente un jour, et dont les colonnes sont les lectures de ce jour : année, trimestre, mois,
> semaine, jour de la semaine, jour férié, exercice. Elle ne décrit aucun client, aucun produit :
> elle décrit le temps lui-même, et se remplit par génération, jamais par les faits.

> **Définition.** La **clé de date** est l'identifiant qui relie un fait à son jour. Elle prend deux
> formes : un entier lisible, qui colle l'année, le mois et le jour dans cet ordre, ou la date native
> du moteur.
> Le socle utilise la date native et écrit la comparaison `d.date = f.date_vente` ; les deux formes
> se valent, à condition de choisir une fois pour tout le modèle.

> **Définition.** La **semaine normalisée** (dite ISO) est la semaine qui commence le lundi et dont
> la première contient au moins quatre jours de janvier. Elle a deux propriétés qui étonnent : elle
> peut valoir **52** pour le 1er janvier d'une année, et une année peut compter **53** semaines.

> **Définition.** Un **exercice fiscal décalé** est une période comptable qui ne coïncide pas avec
> l'année civile. Le socle en porte un : l'exercice 2022 court du 2023-01-01 au 2023-06-30, et
> **725** jours du calendrier appartiennent à une année fiscale différente de leur année civile.

> **Définition.** Une **dimension à rôles** est une même dimension référencée plusieurs fois par un
> fait, chaque référence jouant un rôle différent. Un fait de commande porte trois dates : commandée,
> promise, livrée. Les trois pointent vers le même calendrier, et le rôle se lit dans le nom de
> l'alias, jamais dans la table.

> **Définition.** Une **période partielle** est une période encore en cours : au 2026-08-31, l'année
> 2026 compte **243** jours sur **365**. Comparer une période partielle à une période complète
> n'a aucun sens ; une comparaison n'est recevable que si les deux bornes de fin sont identiques.

---

## 5. Cours approfondi

### 5.1 Pourquoi une dimension plutôt qu'une colonne de date

Une table de faits porte déjà la date : elle n'a besoin de rien d'autre pour être juste. Ce qu'elle
ne sait pas faire, c'est répondre aux questions qui portent sur le **contexte** de cette date.

Prenons le fait de ventes du socle : **17** colonnes, dont une date. Pour obtenir le chiffre
d'affaires du premier trimestre, il faut écrire un test sur le mois ; pour les fériés, il faut une
liste de dates tenue à la main ; pour la semaine commerciale, une formule ; pour l'exercice fiscal,
une seconde formule. Chaque question devient du code, et chaque code peut se tromper différemment.

La dimension de temps remplace ces formules par une jointure. Le socle en porte **15** colonnes :
la date, l'année, le trimestre, le mois et son libellé, la semaine normalisée, le jour de la semaine
et son libellé, le dimanche, le férié et son libellé, l'année-mois, la semaine commerciale, l'année
fiscale et la période fiscale. Une seule jointure ouvre les quinze.

Le gain n'est pas la vitesse. Le gain est que **la définition vit à un seul endroit**. Si le
calendrier décide que la semaine commence le lundi, tous les rapports la suivent ; s'il faut passer
à la semaine du dimanche au samedi, une seule table change.

D'où la règle, et elle est absolue : **une seule table de dates par modèle**. Pas une par fait, pas
une par service, pas une par usage. Le socle l'applique : sa table de ventes, ses **3** dates de
commande et ses **3** dates d'encaissement pointent toutes vers la même dimension de **1 339**
lignes, et c'est ce qui rend le chiffre d'affaires, le délai de livraison et le délai
d'encaissement comparables sur le même axe de temps. Deux calendriers dans un même modèle, ce sont
deux façons de découper l'année, donc deux rapports qui ne se recoupent pas.

### 5.2 Ce que le calendrier du socle contient

| Mesure | Valeur | Lecture |
|---|---|---|
| Lignes du calendrier | **1 339** | 3 ans et 8 mois de jours |
| Première date | 2023-01-01 | un dimanche, jour férié |
| Dernière date | 2026-08-31 | l'année en cours est ouverte |
| Découpage annuel | 2023 : **365** jours — 2024 : **366** jours — 2025 : **365** jours — 2026 : **243** jours | une année bissextile dans la période |
| Jours fériés | **18** jours, **5** libellés distincts | tous travaillés par le magasin |
| Dimanches | **192** | une seule valeur du jour de la semaine |
| Semaine normalisée, maximum | **52** | aucune année de la période ne compte 53 semaines |
| Semaine commerciale, maximum | **53** | **8** jours portent cette valeur |

Les **5** libellés de fériés du socle sont ceux du pays où opère Sahel Distribution : Nouvel An,
Fête du Travail, Anniversaire de la Révolution, Fête nationale et Noël. Tous portent une date fixe,
et la répétition se lit dans le calendrier : le 01-01, le 05-01 et le 08-05 reviennent **4** fois
chacun sur la période, le 12-11 et le 12-25 seulement **3** fois, parce que le calendrier s'arrête
le 2026-08-31 et que leurs deux dates tombent après la borne. Le compte des jours fériés se vérifie
ainsi de tête : 4 + 4 + 4 + 3 + 3 = **18**. Ce petit calcul dit quelque chose d'important sur les
compteurs : **18** n'est pas le nombre de jours fériés du pays, c'est le nombre de jours fériés
compris entre la première et la dernière date du calendrier. Un compteur dépend toujours de sa
borne, et la borne ici se lit dans la dimension, pas dans le fait.

Le 29 février 2024 mérite un mot : ce jour n'existe qu'une année sur quatre, le calendrier le porte
une fois, et le fait de ventes y réalise **195** lignes pour **13 044 279** FCFA. Un modèle qui
connaît les années bissextiles n'a rien à faire pour ce jour ; un modèle qui compte les jours en
divisant par **365** se trompe une année sur quatre.

La dernière ligne du tableau vaut un avertissement. Une année civile fait **365** ou **366** jours,
mais une année **commerciale** faite de semaines de sept jours fait 364 ou 371 jours : les deux
calendriers ne se superposent jamais exactement, et le socle en porte la trace en portant les deux.

### 5.3 Le branchement : fermer le trou déclaré au chapitre 4

Le chapitre 4 avait mesuré la conformité des dimensions du socle et rendu un zéro pour la dimension
de temps : aucun fait ne la référençait. La fermeture est une jointure, et elle se contrôle dans les
deux sens.

| Contrôle | Résultat |
|---|---|
| Lignes du fait jointes au calendrier | **240 000** sur **240 000** |
| Dates de vente absentes du calendrier | **0** |
| Jours du calendrier sans aucune vente | **0** |
| Rapport des volumes | **1** ligne de calendrier pour **179,2** lignes de faits |

Le rapport des volumes explique une propriété du calendrier qu'il faut connaître avant de le
prolonger : c'est la seule table du modèle dont le volume ne suit pas l'activité. Doubler les ventes
ne change rien au calendrier ; traverser une année de plus lui ajoute **365** lignes, et une année
bissextile **366**. C'est une table qu'on remplit par décennie, pas par chargement.

Le fait que la seconde et la troisième ligne valent toutes deux zéro mérite qu'on s'y arrête. Cela
signifie que le magasin du socle n'a **jamais** fermé : un calendrier complet et des faits complets
sont deux affirmations différentes, et leur égalité est un résultat, pas une hypothèse de départ.

> **Dans les faits.** Le socle est un cas limite, et il faut le dire avant d'en tirer une règle. Ses
> **1 339** jours portent tous au moins une vente, y compris les **18** jours fériés et les **192**
> dimanches. Un commerce réel ferme : jours de fête religieuse, inventaire annuel, travaux, panne de
> caisse. Sur un tel modèle, le contrôle « jours du calendrier sans vente » ne rendrait pas **0**
> mais une dizaine de journées par an, et chacune d'elles demanderait une explication avant d'être
> acceptée. C'est précisément parce que le socle répond **0** que le contrôle des dates hors
> calendrier, lui, devient la question intéressante : quand tout est complet d'un côté, le manque se
> cache de l'autre, et il se cachait dans les livraisons de septembre et d'octobre 2026.

> **Attention.** Une date d'un fait peut **sortir du calendrier**, et une jointure interne la
> supprime alors en silence. Le calendrier s'arrête au 2026-08-31 ; les dates de livraison du fait
> de commandes vont jusqu'au 2026-10-14. Sur le socle, **13** dates de livraison tombent hors du
> calendrier, pour **46** commandes et **32 772 075** FCFA — sur les **6 491 975 325** FCFA de
> commandes livrées, soit **0,5 %**. La jointure interne rend **8 635** lignes au lieu de **8 681**,
> et le montant manquant n'apparaît nulle part : aucun message, aucune ligne en erreur, un rapport
> simplement incomplet. La correction tient en **122** lignes ajoutées au calendrier, jusqu'au
> 2026-12-31, et elle ramène les **8 681** commandes, leur montant, sans toucher aux ventes
> (**240 000** lignes). Un calendrier se prolonge **avant** que les faits n'y arrivent.

### 5.4 Les attributs qu'aucun fait ne sait dire

Le socle offre une occasion rare : un magasin qui travaille tous les jours, y compris les jours
fériés. Le tableau suivant ne se calcule pas sur le fait de ventes ; il se calcule en joignant le
calendrier.

| Lecture | Valeur | Part du chiffre d'affaires |
|---|---|---|
| Lundi | **2 663 495 054** FCFA | **17,1 %** |
| Dimanche | **829 983 276** FCFA | **5,32 %** |
| Week-end (samedi et dimanche) | — | **21,0 %** |
| Jours fériés (**18** jours, tous travaillés) | **234 388 370** FCFA | **1,5 %** |
| Quatrième trimestre 2025 | — | **29,7 %** |
| Décembre, dans ce quatrième trimestre | — | **33,6 %** |

Le dimanche est le jour le plus faible de la semaine : **3,21** fois moins de chiffre d'affaires
que le lundi, et **4 322 830** FCFA en moyenne par dimanche contre **11 646 867** FCFA en moyenne
par jour. Les deux journées les plus faibles du socle sont d'ailleurs deux dimanches, dont le
2023-06-18 avec **1 313 588** FCFA. La journée la plus forte, le 2026-03-17, est un mardi, à
**26 933 751** FCFA — soit **20,5** fois la plus faible, et **31** journées dépassent les
20 millions de FCFA.

Aucune de ces phrases ne demande une jointure supplémentaire : tous ces attributs sont dans la
dimension, écrits une fois, et lus autant de fois qu'on veut. C'est le rendement réel d'une
dimension de temps.

### 5.5 Les deux calendriers du socle

La semaine normalisée et la semaine commerciale ne s'accordent pas, et le socle le montre.

| | Semaine normalisée | Semaine commerciale |
|---|---|---|
| Commence le | lundi | lundi (fixé par l'entreprise) |
| Première semaine de l'année | celle qui contient au moins quatre jours de janvier | la première semaine complète de l'exercice |
| Maximum sur la période | **52** | **53** |
| 1er janvier 2023 | semaine **52** | semaine **1** |
| Jours portant la valeur 53 | aucun | **8** |

La première ligne du tableau est la source d'erreur la plus fréquente des rapports hebdomadaires :
le 1er janvier 2023 appartient à la semaine **52**, celle de décembre 2022, parce que la semaine
normalisée n'appartient pas à l'année où elle commence. Un rapport qui groupe les ventes par année
et par semaine normalisée range donc ce jour dans une semaine qui n'existe pas dans l'année des
ventes, et deux rapports annuels successifs se recouvrent ou laissent un trou.

> **À retenir.** Le temps ne se lit pas dans une colonne de date, il se lit dans des **attributs**
> préparés une fois pour toutes. Et quand deux calendriers coexistent, comme ici la semaine
> normalisée et la semaine commerciale, ce n'est pas une incohérence à corriger : c'est un choix à
> écrire, parce qu'un rapport hebdomadaire qui ne dit pas quel calendrier il suit n'est pas
> vérifiable.

### 5.6 L'exercice fiscal, et un nom qui promet plus que la mesure

L'exercice fiscal du socle ne suit pas l'année civile : l'exercice 2022 court du 2023-01-01 au
2023-06-30, ce qui place **725** jours du calendrier dans une année fiscale différente de leur année
civile. Deux chiffres d'affaires annuels coexistent donc pour la même activité : celui de l'année
civile et celui de l'exercice, et un rapport qui n'annonce pas lequel il utilise ne peut pas être
comparé à un autre.

Le calendrier porte deux colonnes pour cela : `annee_fiscale` et `periode_fiscale`. La première
tient sa promesse. La seconde, non : elle ne prend que **2** valeurs sur les **1 339** lignes du
calendrier, alors que son nom laisse attendre un découpage en douze périodes. C'est un défaut de
nom, pas un défaut de calcul, et il coûte cher : un auteur de rapport qui écrit « par période
fiscale » en attendant douze lignes en reçoit deux, et croit à une erreur de jointure.

La leçon dépasse ce cas. Un attribut dont le **libellé promet plus que la mesure** se détecte par un
contrôle simple : compter les valeurs distinctes de chaque colonne du calendrier avant de s'en
servir. Un contrôle de dix lignes de SQL évite des heures de doute.

### 5.7 Le mois partiel : deux vérités contradictoires sur la même table

Le calendrier s'arrête au 2026-08-31. L'année 2026 compte donc **243** jours sur **365**, et c'est
la lecture la plus utile du chapitre, parce qu'elle ne demande aucun outil nouveau.

| Comparaison | Chiffre d'affaires | Écart |
|---|---|---|
| 2026 entier contre 2025 entier | **3 360 553 372** FCFA contre **4 724 700 286** FCFA | **, 28,9 %** |
| Janvier à août 2026 contre janvier à août 2025 | **3 360 553 372** FCFA contre **2 913 055 394** FCFA | **+ 15,4 %** |

Les deux lignes portent sur la même table, la même jointure et le même filtre de retours. La
première annonce un effondrement, la seconde une croissance, et il y a **44,3** points d'écart entre
les deux. La règle est donc simple : une comparaison entre deux périodes n'est recevable que si
**la borne de fin est la même** des deux côtés.

> **Attention.** Un cumul n'échappe pas au piège du mois partiel, il le déplace. Le cumul des douze
> derniers mois vaut **5 172 198 264** FCFA au 2026-08-31, contre **4 452 117 890** FCFA pour les
> douze mois précédents, soit **+ 16,2 %**. Ce chiffre est comparable parce que les deux fenêtres
> font exactement douze mois, quelle que soit l'année civile dans laquelle elles tombent : le cumul
> glissant est la seule lecture annuelle qui reste juste quand l'année n'est pas finie.

> **Conseil professionnel.** Remplissez le calendrier **par horizon**, jamais par chargement : deux
> ans d'avance coûtent moins de huit cents lignes et suppriment toute la classe d'erreurs décrite
> ici. Puis posez trois contrôles fixes, exécutés à chaque chargement. Le premier compte les jours du
> calendrier sans aucun fait rattaché, et les compare aux fermetures connues de l'entreprise. Le
> deuxième compte les dates des faits absentes du calendrier, et **échoue** au lieu de continuer :
> c'est ce contrôle qui aurait signalé les **13** dates de livraison hors calendrier du socle. Le
> troisième vérifie que la première et la dernière date du calendrier encadrent bien celles des
> faits, avec une marge d'au moins un exercice. Ces trois contrôles tiennent en une requête chacun
> et remplacent une confiance qui, elle, ne se mesure pas.

### 5.8 Le temps dans les six autres faits

Le socle porte **7** tables de faits et **3** manières d'y écrire le temps.

| Nature du temps | Faits | Colonnes | Pourquoi |
|---|---|---|---|
| Une date native | fait de ventes | `date_vente` | la vente a lieu à un instant unique |
| Trois dates | commandes, encaissements | commandée, promise, livrée / facturée, échue, encaissée | le processus a trois étapes observables |
| Un mois | logistique, ruptures, stock mensuel, objectifs | `mois` (ou `annee` et `mois`) | la mesure est mensuelle par nature |

Les deux premiers cas se lisent avec la même dimension, jointe une fois ou trois fois. Le troisième
cache une ambiguïté qu'il faut voir : le mot `mois` recouvre **deux natures**. Dans trois faits,
c'est un texte de la forme `2023-01`, qui porte l'année et le mois. Dans le fait des objectifs,
c'est l'entier **12** au maximum, sans l'année — l'année vit dans une colonne voisine. Un rapport qui
joint ces faits au calendrier doit donc écrire deux fois la même intention, une fois pour chaque
nature du mot. Rien ne le signale : la colonne porte le même nom.

Le fait de commandes montre ce que trois dates permettent : le délai moyen entre commande et
livraison vaut **6,66** jours, **1 646** commandes sur **8 681** livrées dépassent la date promise,
soit **19,0 %**, et le retard moyen de ces commandes vaut **10,29** jours. Ces trois mesures ne sont
pas additives : le délai moyen d'un trimestre n'est pas la somme des délais moyens des trois mois.
Une moyenne de délais se recalcule toujours au grain supérieur, et c'est le lien direct avec le
chapitre 3 sur l'additivité.

Reste ce que le modèle ne saura jamais dire. Le fait de ventes porte **17** colonnes, et **0** d'entre
elles contient une heure. L'heure de pointe, la répartition par créneau, l'affluence du samedi après
midi : hors de portée. Ce n'est pas une erreur de modélisation, c'est un choix de grain qu'il faut
nommer, parce qu'aucune analyse ne peut le contourner après coup.

---

## 6. Exemple concret — les 46 commandes que la jointure interne effaçait

Voici le cas, dans l'ordre où il se produit en atelier.

Une analyste veut publier le chiffre d'affaires livré par semaine. Elle écrit une jointure ordinaire
entre le fait de commandes et le calendrier, filtre les commandes livrées, groupe par semaine, et
obtient un tableau propre. Personne ne proteste : les semaines se suivent, les totaux se cumulent,
la somme des semaines égale le total général — puisqu'il a été calculé dans la même requête.

Le contrôle arrive le lendemain, quand le service logistique annonce **6 491 975 325** FCFA de
commandes livrées pour la période et que le rapport en affiche **6 459 203 250** FCFA. L'écart vaut
**32 772 075** FCFA, et rien dans le rapport ne permet de le localiser.

Voici les trois nombres qui racontent tout.

| Ligne du rapport | Valeur |
|---|---|
| Commandes livrées dans le fait | **8 681** |
| Commandes rendues par la jointure au calendrier | **8 635** |
| Dates de livraison hors calendrier (**13** dates, du 2026-09-01 au 2026-10-14) | **46** commandes |

Le calendrier s'arrête au 2026-08-31. Les commandes passées en août 2026 sont livrées en septembre
et parfois en octobre, et la jointure ne trouve pas ces jours : elle les élimine. Une jointure
interne ne perd pas des lignes, elle perd des lignes **silencieusement** — c'est la différence entre
un modèle incomplet et un modèle faux.

La correction ne touche ni le fait, ni la requête : elle touche le calendrier, prolongé de **122**
jours jusqu'au 2026-12-31. Le calendrier passe de **1 339** à **1 461** lignes, les **8 681**
commandes reviennent, le montant aussi, et les ventes ne bougent pas. Le coût de la correction tient
en **122** lignes d'une table qu'aucune activité n'alimente, pour récupérer **32 772 075** FCFA de
commandes qui existaient depuis le début.

---

## 7. Démonstration pas à pas — cinq gestes

Les cinq gestes se font dans l'ordre, et chacun produit un contrôle qui reste au modèle.

**Geste 1 — vérifier la complétude du calendrier avant de s'en servir.**

```sql
SELECT COUNT(*) AS jours,
       MIN(date) AS premier,
       MAX(date) AS dernier
FROM dim_date;
```

**1 339** jours, du 2023-01-01 au 2026-08-31. Un calendrier se contrôle avant sa jointure, pas
après : le même contrôle appliqué aux faits ne dirait rien de ses trous.

**Geste 2 — joindre le fait au calendrier, et compter les deux côtés.**

```sql
SELECT COUNT(*) AS jointes
FROM fait_ventes f
JOIN dim_date d ON d.date = f.date_vente;
```

**240 000** lignes pour **240 000** lignes du fait : aucune perte. C'est le contrôle de recette du
branchement, et il se pose une fois pour toutes.

**Geste 3 — chercher ce que la jointure a laissé de côté.**

```sql
SELECT COUNT(*) AS dates_hors_calendrier
FROM (SELECT DISTINCT date_livraison FROM fait_commandes
      WHERE date_livraison IS NOT NULL) v
LEFT JOIN dim_date d ON d.date = v.date_livraison
WHERE d.date IS NULL;
```

**13** dates de livraison sortent du calendrier. Le geste est un **left join suivi d'un test de
nul**, jamais une jointure interne : la jointure interne aurait rendu **8 635** lignes sans rien
signaler, le left join rend les **8 681** lignes et désigne les fautives.

**Geste 4 — prolonger le calendrier au lieu de corriger la requête.**

```sql
SELECT COUNT(*) AS jours_prolonges
FROM (SELECT date FROM dim_date
      UNION ALL
      SELECT (DATE '2026-08-31' + INTERVAL (i) DAY)::DATE
      FROM generate_series(1, 122) AS t(i)) c;
```

Dans le script de chargement, les **14** autres colonnes se calculent de la même façon, à partir de
la date engendrée : `EXTRACT(year FROM …)`, `STRFTIME(…, '%Y-%m')` pour l'année-mois, et ainsi de
suite. Le geste 4 ne touche ni la structure du calendrier ni son grain : il ajoute des jours.

**1 461** lignes. Après prolongation, la jointure sur la date de livraison rend **8 681** lignes,
retrouve les **6 491 975 325** FCFA, et il ne reste **0** date orpheline ni côté livraison ni côté
date promise. Le geste 4 rend le geste 5 possible.

**Geste 5 — borner la comparaison avant de publier.**

```sql
SELECT d.annee, SUM(f.montant_ttc) AS ca
FROM fait_ventes f
JOIN dim_date d ON d.date = f.date_vente
WHERE f.est_retour = 0 AND d.mois <= 8
GROUP BY 1 ORDER BY 1;
```

Les années 2023 à 2026 rendent respectivement **2 127 742 355**, **2 527 257 254**,
**2 913 055 394** et **3 360 553 372** FCFA. La comparaison des deux dernières donne **+ 15,4 %**,
et c'est la seule lecture annuelle recevable au 2026-08-31. Comparer les années entières aurait
donné **, 28,9 %**.

---

## 8. Erreurs fréquentes

Ce sont les six pièges de dates que le modèle du projet doit avoir fermés, dans l'ordre où ils se
rencontrent en atelier.

1. **Comparer une période partielle à une période complète.** Le cas le plus fréquent, et le plus
   coûteux : **44,3** points d'écart entre les deux lectures du même chiffre d'affaires.
2. **Joindre un fait au calendrier en interne.** Les dates hors calendrier disparaissent sans
   message : **46** commandes et **32 772 075** FCFA sur le socle.
3. **Remplir le calendrier avec les dates des faits.** Un calendrier construit sur les ventes ne
   contient que les jours vendus, donc il ne peut pas montrer les fermetures — exactement ce qu'on
   lui demande. Le socle a la chance d'avoir **0** jour sans vente ; un vrai magasin en a.
4. **Confondre semaine normalisée et semaine commerciale.** L'une plafonne à **52** et l'autre à
   **53** sur la même période ; un rapport qui ne dit pas laquelle il suit n'est pas vérifiable.
5. **Joindre trois fois la même dimension sans alias dans la même requête.** Les trois dates d'une
   commande pointent vers la même table : sans alias, la requête est illisible ou refusée.
6. **Confondre l'année civile et l'exercice fiscal.** **725** jours du socle appartiennent à une
   autre année fiscale que leur année civile, et `periode_fiscale` promet douze périodes pour en
   rendre **2** : ni la borne du rapport, ni le libellé d'une colonne, ne disent ce que l'auteur
   croyait avoir demandé.

---

## 9. Bonnes pratiques professionnelles

1. **Remplir le calendrier par horizon**, avec au moins un exercice d'avance, et le prolonger par un
   script rejouable : **122** lignes ont suffi à récupérer **32 772 075** FCFA.
2. **Poser trois contrôles à chaque chargement** : jours sans fait, dates de fait hors calendrier,
   encadrement des bornes. Les deux premiers se comptent, le troisième se compare.
3. **Nommer le calendrier dans chaque rapport.** Une semaine sans mention de son calendrier, un
   trimestre sans mention de son exercice, sont des chiffres non vérifiables.
4. **Comparer à bornes égales**, et écrire la borne dans le titre du rapport : « janvier à août »,
   jamais « 2026 contre 2025 » quand l'année n'est pas finie.
5. **Recalculer au grain supérieur toute mesure non additive.** Les délais moyens du socle
   (**6,66** jours de commande à livraison, **10,29** jours de retard moyen) ne s'additionnent pas.
6. **Déclarer ce que le grain ne porte pas.** **0** colonne d'heure sur **17** : l'analyse par
   créneau horaire est impossible, et le dire évite qu'on la demande.

---

## 10. Exercice guidé

**Énoncé.** Le service commercial veut un rapport du chiffre d'affaires par jour de la semaine et
par trimestre pour l'exercice 2025, avec la part des jours fériés. Construisez-le et rendez les
quatre nombres demandés.

**Étape 1.** Joindre le fait de ventes au calendrier et filtrer l'année.

```sql
SELECT d.libelle_jour, d.trimestre, SUM(f.montant_ttc) AS ca
FROM fait_ventes f JOIN dim_date d ON d.date = f.date_vente
WHERE f.est_retour = 0 AND d.annee = 2025
GROUP BY 1, 2 ORDER BY 2, 1;
```

**Étape 2.** Le jour le plus fort de la semaine rend **2 663 495 054** FCFA, le plus faible
**829 983 276** FCFA : le rapport vaut **3,21** pour un.

**Étape 3.** Le trimestre le plus lourd rend **1 405 274 549** FCFA, soit **29,7 %** de l'année.

**Étape 4.** Les jours fériés de l'année pèsent **234 388 370** FCFA sur l'ensemble de la période du
socle, soit **1,5 %**.

**Attendu.** Quatre nombres : **2 663 495 054** · **829 983 276** · **29,7 %** · **1,5 %**. Le
rapport doit nommer son calendrier, son exercice et sa borne de fin.

---

## 11. Exercices autonomes

**Exercice 6.1.** Le calendrier du socle porte **1 339** lignes. Combien en faudrait-il pour couvrir
dix ans à partir du 2023-01-01, années bissextiles comprises ? Quel volume de faits cela
représenterait-il, au rapport mesuré de **179,2** lignes de faits pour une ligne de calendrier ?

**Exercice 6.2.** Un rapport annonce une baisse de **, 28,9 %** du chiffre d'affaires 2026. Écrivez
la requête qui produit ce chiffre, puis celle qui produit la lecture comparable. Donnez les deux
valeurs et l'écart en points.

**Exercice 6.3.** Écrivez la requête qui compte les dates de livraison absentes du calendrier, puis
mesurez le montant perdu par une jointure interne. Proposez une correction qui ne modifie ni le fait
ni la requête.

**Exercice 6.4.** Le fait de commandes porte trois dates. Écrivez la requête qui donne le délai moyen
de livraison et la part des commandes en retard sur la date promise. Expliquez pourquoi ces deux
mesures ne s'additionnent pas d'un mois sur l'autre.

**Exercice 6.5.** Le 1er janvier 2023 appartient à la semaine normalisée **52**. Écrivez la requête
qui le prouve, puis expliquez en trois phrases pourquoi un rapport annuel par semaine normalisée
peut recouvrir deux années ou en laisser une de côté.

---

## 12. Correction détaillée

**Exercice 6.1.** Dix années civiles, du 2023-01-01 au 2032-12-31, comptent **3 653** jours :
sept années de **365** jours et trois années bissextiles de **366** (2024, 2028 et 2032), soit
**2 555** plus **1 098**. Au rapport mesuré de **179,2** lignes de faits pour une ligne de
calendrier, ces **3 653** lignes de calendrier porteraient environ **654 618** lignes de faits, et
c'est beaucoup pour dix ans. La conclusion utile n'est pas le nombre, c'est le rapport : le
calendrier grandit de **365** ou **366** lignes par an, quand les faits grandissent de dizaines de
milliers.

**Exercice 6.2.** La première requête groupe par année sur le fait entier et compare deux années
dont l'une est partielle : **3 360 553 372** FCFA contre **4 724 700 286** FCFA, soit **, 28,9 %**.
La seconde ajoute `AND d.mois <= 8` et borne les deux années aux huit premiers mois :
**3 360 553 372** FCFA contre **2 913 055 394** FCFA, soit **+ 15,4 %**. L'écart entre les deux
lectures vaut **44,3** points, et il tient à une clause de trois mots.

**Exercice 6.3.** Le comptage se fait par `LEFT JOIN` et test de valeur nulle sur le calendrier :
**13** dates de livraison hors calendrier, **46** commandes, **32 772 075** FCFA. La jointure interne
rend **8 635** lignes au lieu de **8 681**. La correction consiste à prolonger le calendrier de
**122** jours, jusqu'au 2026-12-31 : il passe à **1 461** lignes, et les commandes livrées
reviennent toutes, avec leur montant de **6 491 975 325** FCFA.

**Exercice 6.4.** Le délai moyen vaut **6,66** jours, la part des commandes livrées après la date
promise vaut **19,0 %** — soit **1 646** commandes sur **8 681** — et le retard moyen de ces
commandes vaut **10,29** jours. Ces trois nombres sont des moyennes : le délai moyen d'un trimestre
n'est pas la moyenne des délais moyens des mois qui le composent, parce que les trois mois n'ont pas
le même nombre de commandes. Une moyenne se recalcule toujours à partir des lignes, jamais à partir
d'autres moyennes.

**Exercice 6.5.** La preuve tient en une requête : `SELECT date, semaine_iso FROM dim_date WHERE
date = DATE '2023-01-01'` rend **52**. Un rapport annuel groupé par semaine normalisée range ce jour
dans la semaine **52**, celle de décembre 2022 : l'année 2023 compte donc **52** semaines et le
rapport de 2022 en compte **52** également, avec un jour à cheval. La même année, la semaine
commerciale du socle monte jusqu'à **53**, sur **8** jours : deux rapports annuels bâtis sur deux
calendriers différents ne se recoupent pas.

---

## 13. Mini-projet de chapitre

**Objet.** Doter le modèle de Sahel Distribution d'un calendrier qui ne produit plus de pertes.

**Livrables.**

1. Un script rejouable qui génère le calendrier du 2023-01-01 au 2027-12-31, avec les **15**
   colonnes du socle, les jours fériés à une liste déclarée en clair, et un identifiant de ligne.
2. Trois contrôles de complétude, chacun en une requête : jours du calendrier sans fait, dates de
   fait absentes du calendrier, encadrement des bornes par un exercice de marge.
3. Un rapport trimestriel du chiffre d'affaires livré, avec mention du calendrier utilisé et des
   bornes de comparaison.
4. Une note de trois paragraphes sur ce que le modèle ne saura jamais dire faute d'heure, et sur ce
   qu'il faudrait changer pour le dire.

**Barème indicatif.** Génération et colonnes : **3** points. Contrôles : **4** points. Rapport
borné : **2** points. Note sur le grain : **1** point. Total : **10** points.

**Critère de réussite.** Le contrôle des dates de fait absentes du calendrier rend **0**, et le
rapport affiche un chiffre d'affaires livré égal à la somme des lignes du fait, sans écart.

---

## 14. Résumé du chapitre

| Notion | Mesure du socle | Ce qu'elle enseigne |
|---|---|---|
| Dimension de temps | **1 339** lignes, du 2023-01-01 au 2026-08-31 | une table qui se remplit par génération, pas par chargement |
| Branchement | **240 000** lignes sur **240 000** | le trou déclaré au chapitre 4 se ferme par une jointure |
| Complétude | **0** jour sans vente, **0** date de vente hors calendrier | deux contrôles différents, deux réponses distinctes |
| Date hors calendrier | **13** dates, **46** commandes, **32 772 075** FCFA | une jointure interne perd en silence |
| Correction | **122** lignes ajoutées, **8 681** commandes retrouvées | prolonger le calendrier, pas la requête |
| Attributs | dimanche **5,32 %**, fériés **1,5 %**, quatrième trimestre **29,7 %** | ce qu'aucun fait ne sait dire |
| Deux calendriers | semaine normalisée **52**, semaine commerciale **53** | une ambiguïté à écrire, pas à corriger |
| Exercice fiscal | **725** jours décalés, **2** valeurs de période | un libellé n'est pas une spécification |
| Période partielle | **, 28,9 %** contre **+ 15,4 %** | **44,3** points pour une borne mal choisie |
| Cumul glissant | **5 172 198 264** FCFA, **+ 16,2 %** | la seule lecture annuelle juste en année ouverte |
| Grain du temps | **3** dates, **4** mois, **0** heure sur **17** colonnes | ce que le modèle ne dira jamais |

**Instrument.** Toutes les valeurs de ce chapitre sont reproductibles : `python3 tools/modele_M13.py`
exécute la section **15** de l'instrument, qui contrôle le branchement du calendrier dans les deux
sens, prolonge le calendrier en mémoire, compare les deux lectures d'une année ouverte et rend les
quatre textes de synthèse.

---

## 15. À retenir

Trois phrases portent ce chapitre.

1. **Une dimension de temps se remplit d'avance et se joint sans perte.** Le socle en porte **1 339**
   lignes et la jointure rend **240 000** lignes sur **240 000** : le travail est fait une fois, lu
   autant de fois qu'on veut.
2. **Une borne de fin, une jointure interne et un libellé ambigu suffisent à rendre un rapport
   faux.** Le même chiffre d'affaires s'écrit **, 28,9 %** ou **+ 15,4 %** selon la borne, **46**
   commandes disparaissent dans une jointure interne, et `periode_fiscale` promet douze périodes
   pour en rendre **2**.
3. **Le contrôle se fait dans les deux sens.** Les jours du calendrier sans fait disent les
   fermetures et les pannes ; les dates des faits hors calendrier disent les horizons trop courts.
   Le socle répond **0** à la première question et **13** à la seconde, ce qui est exactement
   l'inverse de ce que le bon sens suggérait.

> **À retenir.** Le temps est la seule dimension que le modèle connaît avant les faits, et c'est
> pour cela qu'elle pardonne moins que les autres. Un client manquant se rattrape par une ligne
> inconnue ; un jour manquant ne se rattrape pas, parce qu'il n'existe nulle part dans les faits.
> Prolonger un calendrier coûte **122** lignes ; ne pas le prolonger coûte **32 772 075** FCFA
> qu'aucun message d'erreur ne signalera.

---

## 16. Évaluation formative

1. Pourquoi une dimension de temps existe-t-elle alors que la table de faits porte déjà une date ?
2. Combien de lignes porte le calendrier du socle, et sur quelle période ?
3. Quels sont les deux contrôles de complétude d'un calendrier, et que répond le socle à chacun ?
4. Qu'est-ce qu'une date hors calendrier, et pourquoi une jointure interne est-elle dangereuse ?
5. Combien de lignes faut-il ajouter au calendrier du socle pour le prolonger jusqu'à la fin de
   2026, et qu'est-ce que cela récupère ?
6. Le dimanche pèse **5,32 %** du chiffre d'affaires et les jours fériés **1,5 %** : pourquoi ces
   deux nombres ne se calculent-ils pas sans le calendrier ?
7. Quelles sont les deux semaines du socle, et de combien diffèrent leurs maximums ?
8. Que fait un rapport annuel groupé par semaine normalisée du 1er janvier d'une année ?
9. Le chiffre d'affaires 2026 vaut **3 360 553 372** FCFA contre **4 724 700 286** FCFA en 2025 :
   cette comparaison est-elle recevable, et que faut-il écrire à la place ?
10. Que vaut, au 2026-08-31, le cumul des douze derniers mois, et pourquoi cette lecture échappe-t-
    elle au piège du mois partiel ?

**Corrigé.** 1. Parce que la date seule ne porte pas le contexte : trimestre, jour de la semaine,
férié, exercice, semaine. 2. **1 339** lignes, du 2023-01-01 au 2026-08-31. 3. Les jours sans fait,
qui valent **0**, et les dates de fait hors calendrier, qui valent **0** pour les ventes mais **13**
pour les livraisons de commandes. 4. Une date d'un fait absente de la dimension : la jointure interne
la supprime sans erreur — **46** commandes et **32 772 075** FCFA sur le socle. 5. **122** lignes,
jusqu'au 2026-12-31, ce qui ramène les **8 681** commandes livrées et leurs **6 491 975 325** FCFA.
6. Parce que ni le jour de la semaine ni le statut de férié ne figurent dans le fait : ils se lisent
dans la dimension, jointure faite. 7. La semaine normalisée, maximum **52**, et la semaine
commerciale, maximum **53** sur **8** jours. 8. Il range ce jour dans la semaine **52**, celle de
décembre de l'année précédente, et décale de fait la première semaine du rapport. 9. Non : l'année
2026 est ouverte et compte **243** jours sur **365**. Il faut borner les deux années aux huit
premiers mois, ce qui donne **+ 15,4 %** au lieu de **, 28,9 %**. 10. Il vaut **5 172 198 264**
FCFA, contre **4 452 117 890** FCFA pour la fenêtre précédente, soit **+ 16,2 %** : les deux fenêtres
comptent douze mois pleins, donc la comparaison est juste quelle que soit la position de l'année
civile.
