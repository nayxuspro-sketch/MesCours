# M14 — Les 11 retours du comité d'utilisateurs

**Le principe du projet P2.** Ces onze retours arrivent ensemble, dans le désordre, comme dans la vraie vie : certains sont contradictoires, un demande une donnée que l'entreprise ne produit pas, un autre veut tout voir sur un seul écran. Votre travail n'est pas de satisfaire tout le monde : c'est de **trier, prioriser, faire et refuser** en écrivant pourquoi.
| # | Le retour, tel qu'il est dit | Ce qu'il cache | La bonne réponse à trouver |
|---|---|---|---|
| 1 | « Le chiffre de la page Direction n'est pas celui de la page Commercial. » | Les deux pages ne lisent pas le même fait, ou l'une d'elles compte les retours. | chercher la cause dans le MODÈLE : une relation, un filtre ou deux définitions |
| 2 | « Je ne devrais voir que mon magasin, pas ceux des autres. » | Le besoin est légitime et il se traite au bon endroit. | rôle de sécurité au niveau des lignes sur la dimension des magasins |
| 3 | « Ajoutez le chiffre d'affaires par heure de la journée. » | La donnée n'existe pas : le fait de ventes porte une date, pas une heure. | refus argumenté : une donnée absente ne s'invente pas, elle se collecte |
| 4 | « Mon équipe travaille en anglais. » | Les libellés d'un rapport se traduisent. | traductions des textes du rapport, pas des noms de colonnes |
| 5 | « Les montants en dollars, personne ne les lit ici. » | La devise doit être portée par le visuel. | format de devise en FCFA, et l'unité écrite dans le titre |
| 6 | « Mettez les douze indicateurs de la carte sur la première page. » | Douze visuels sur un écran, c'est douze messages que personne ne lit. | refus partiel chiffré : cinq visuels sur la page, le reste en page de détail |
| 7 | « Envoyez-le en PDF chaque lundi matin. » | Un abonnement automatisé existe, à condition d'un espace de travail payant. | abonnement au rapport, ou refus assumé et écrit |
| 8 | « Je veux le détail d'une vente en cliquant sur un magasin. » | L'exploration par clic descend d'un niveau en gardant le filtre. | page de détail et exploration par clic |
| 9 | « Le total des retours est négatif, c'est une erreur. » | Les retours du socle portent une quantité négative : la convention existe, elle doit être écrite. | définir et afficher la convention de signe |
| 10 | « Il met quarante secondes à s'ouvrir. » | Un rapport lent n'est pas utilisé, même juste. | mesurer, trouver la cause (trop de visuels, colonne calculée, relation bidirectionnelle), corriger |
| 11 | « Je veux la couverture de stock en semaines, pas le taux de rupture. » | Une mesure nouvelle, une table du modèle qui n'est pas encore reliée. | hors périmètre de M14 : c'est le travail de P2, et il exige une relation de plus |

**Ce que le barème attend de vous** : **3** refus au moins, chacun argumenté ; les retours contradictoires (le n° **6** contre la grille, le n° **1** contre le n° **9**) traités par une décision, pas par un compromis ; et une phrase finale qui dit ce que vous refusez de faire dans ce trimestre.
