# Le tableau de bord que personne n'ouvrait — le dossier du projet M12

**12 pages de pièces. C'est le matériel du projet M12.P : un dispositif réel, livré, payé, et
abandonné en onze semaines. Rien n'est inventé sur les chiffres ; tout est mesurable dans le socle
du module — et vous devrez le mesurer.**

---

## Pièce 1 — La commande initiale (mars 2026)

> « La direction veut un **tableau de bord unique** pour suivre l'activité des cinq magasins.
> Il doit contenir **tout** : le chiffre d'affaires, la marge, les stocks, les ruptures, les
> livraisons, les impayés, la logistique, et les comparaisons avec l'an dernier. Les directeurs
> l'ouvriront tous les matins. »

Le prestataire retenu répond en trois pages, avec une maquette de **41 indicateurs** répartis en
**7** onglets.

## Pièce 2 — Le devis, accepté sans discussion

| Poste | Montant | Détail |
|---|---|---|
| Conception et développement | 4 850 000 FCFA | 22 jours |
| Reprise et nettoyage des sources | 1 640 000 FCFA | 8 jours |
| Formation d'une heure | 250 000 FCFA | 1 session, 12 participants |
| Maintenance annuelle | 1 200 000 FCFA | forfait |
| **Total** | **7 940 000 FCFA** | livraison annoncée en 6 semaines |

## Pièce 3 — Les 41 indicateurs livrés (extrait : les 7 onglets)

1. **Activité** — CA du jour, CA du mois, CA cumulé, CA N-1, écart, nombre de tickets, panier
   moyen, marge brute, taux de marge.
2. **Stock** — valeur du stock, nombre de références, ruptures, rotation, couverture, produits
   dormants, top 10 des acheteurs.
3. **Ruptures** — ruptures du jour, jours de rupture cumulés, CA perdu estimé, top 10 des produits
   en rupture.
4. **Livraisons** — commandes du jour, taux de service, retards, délai moyen, commandes annulées,
   top 10 clients en retard.
5. **Encaissements** — encaissements du jour, taux de recouvrement, encours, encours échu, DSO,
   balance âgée, top 10 des impayés.
6. **Logistique** — colis expédiés, poids, coût unitaire, coût au kilo, coût par magasin, coût par
   véhicule.
7. **Écarts** — comparaisons N-1 sur 9 indicateurs, cibles, seuils, feux tricolores.

## Pièce 4 — Le démarrage (avril 2026)

Le tableau de bord est publié. **14** personnes reçoivent l'adresse. Le lendemain, **4** l'ouvrent.
La première semaine, la moyenne quotidienne d'ouvertures est de **6** ; la deuxième, de **3**.

Au bout de trois semaines, deux questions arrivent :

- « Le CA affiché n'est pas celui de la compta : il manque les retours. » — Réponse du prestataire :
  « ce sont deux définitions ; l'une est la vente, l'autre est la vente nette. »
- « La marge est fausse sur les matériaux. » — Réponse : « nous utilisons le coût d'achat standard
  du référentiel, pas le dernier prix payé. »

Personne ne tranche. **Chacun garde son chiffre.**

## Pièce 5 — Les trois sources de la discorde

| Indicateur | Version « compta » | Version « tableau de bord » | L'écart |
|---|---|---|---|
| CA du mois | ventes nettes de retours | ventes brutes | le tableau de bord ignore **2 809** lignes de retour |
| Marge brute | coût du dernier achat | coût standard du référentiel | deux coûts pour un produit |
| Panier moyen | CA net / nombre de tickets | CA brut / nombre de lignes | deux dénominateurs |

## Pièce 6 — Le coût de l'abandon, onze semaines plus tard

Le contrat de maintenance est résilié. Les fichiers sources continuent d'être mis à jour pour
**rien**. Les **41** indicateurs restent affichés, avec des chiffres que plus personne ne défend :
la direction a repris ses trois tableaux Excel, dont deux contiennent encore la formule de
l'an dernier.

**Ce que l'abandon a laissé :**

- **7 940 000** FCFA dépensés, dont la maintenance (1 200 000) ;
- **30** jours de travail, dont 8 sur les sources ;
- une équipe de deux personnes refroidie pour trois ans ;
- et un chiffre d'affaires que personne n'a su lire : la vraie question de la direction — « où
  perdons-nous de la marge ? » — n'a jamais reçu de réponse.

## Pièce 7 — Ce que le prestataire n'a jamais demandé

- Qui décide avec ce chiffre, et **quand** ?
- Que fera-t-on **différemment** si le chiffre est mauvais ?
- Quelle est **déjà** la réponse des gens à cette question, et où la lisent-ils aujourd'hui ?
- Qui est **responsable** de la définition de chaque indicateur ?
- Combien de temps par jour le lecteur accepte-t-il d'y consacrer ?
- Que se passe-t-il le 8 du mois, quand la donnée arrive en retard ?

## Pièce 8 — Les trois questions posées en réunion

1. « Combien avons-nous vendu ? » → une réponse, mais laquelle des deux définitions ?
2. « Où perdons-nous de la marge ? » → **personne** ne peut répondre : la marge n'existe que par
   produit, et l'onglet « Écarts » la compare à une cible que personne n'a fixée.
3. « Que fait-on si la rupture dépasse le seuil ? » → **la question n'a pas de réponse**, parce que
   le seuil n'a jamais été associé à une action.

## Pièce 9 — Le courriel de clôture du projet

> « Bonjour, après onze semaines, le tableau de bord ne répond pas aux attentes. Nous le laissons
> disponible mais nous ne reconduirons pas la maintenance. Merci de votre travail. »

## Pièce 10 — Le mandat de reprise (aujourd'hui)

Vous êtes mandaté pour **diagnostiquer** ce dispositif et proposer une **reprise**. Le mandat est
explicite : « pas plus de **10** indicateurs, chacun avec sa définition écrite, son responsable, sa
fréquence, son seuil et son contre-indicateur. Et une réponse à la seule question qui compte : que
fait-on quand il passe au rouge ? »

---

**Vos pièces de travail** : `socle_m12.sql` (les cinq tables opérationnelles), `ATTENDU.json` (les
mesures de référence), et les **6** chapitres du module. Toutes les valeurs du dossier ci-dessus se
recalculent sur le socle — commencez par là : un diagnostic qui ne mesure rien est un avis.
