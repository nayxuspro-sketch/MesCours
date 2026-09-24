# Projet M04.P — « Le dossier de données de la quincaillerie de Koudougou »

**Module M04 · projet de fin de module · 6 h · barème /20, seuil de passage 13/20**

> **Le cadre réel.** Un gérant de quincaillerie vous a remis un dossier tel qu'il le tient dans son poste : un
> fichier de commandes de 160 lignes, un fichier de clients, un tarif fournisseur « généré par son logiciel », et
> une phrase : « je sais que c'est mal tenu, mais les totaux du mois doivent sortir lundi ». Ce dossier contient
> **sept défauts de natures différentes**, dont **deux qui cassent les totaux** — pas plus, pas moins. Vous rendez
> la boîte en état de rejeu : un diagnostic chiffré, un fichier réparé dont on sait d'où viennent les nombres, un
> journal, un README, un contrôle final qui sait ce qui *doit* rester, et un périmètre de protection pour les
> clients. C'est la synthèse des six chapitres : chaque livrable en mobilise un, et aucun n'est noté pour lui-même.

> **Note de cohérence.** Le dossier est généré de façon déterministe par `python3 tools/dossier_M04.py`
> (graine 41) : qui que vous soyez, vous touchez les mêmes 160 lignes. `03_exercices/dossier_M04/ATTENDU.json`
> contient les résultats attendus, **mesurés sur le dossier généré, jamais déduits** : vous n'y recourez qu'après
> avoir produit vos propres nombres, pour comparer, pas pour copier. Un candidat qui lit l'`ATTENDU` avant de
> calculer n'a plus rien à rendre. Les chiffres de ce corrigé sont ceux du dossier livré, vérifiables ligne à ligne.

---

## 1. Énoncé

### Le matériel

| Élément | Chemin | Ce que c'est |
|---|---|---|
| Commandes | `03_exercices/dossier_M04/commandes_2026.csv` | 160 lignes, 20 colonnes, encodage UTF-8 avec BOM, séparateur virgule |
| Clients | `03_exercices/dossier_M04/clients_2026.csv` | 132 lignes, 11 colonnes, UTF-8 avec BOM |
| Tarif fournisseur | `03_exercices/dossier_M04/tarif_fournisseur.csv` | 10 lignes utiles, séparateur point-virgule, encodage Windows-1252, en-tête décalé |
| Résultats attendus | `03_exercices/dossier_M04/ATTENDU.json` | à utiliser **après** le calcul, jamais comme source de copie |
| Outils | un tableur (Excel 2021+ ou LibreOffice Calc) ; Power Query si votre poste l'a | sinon : la voie accessible, et vous l'écrivez |

Le dossier contient sept défauts de natures différentes ; deux d'entre eux faussent le total de la somme directe,
les cinq autres faussent une analyse, une jointure ou un import — sans jamais changer un seul montant. Trouver les
sept, les séparer en deux natures, et prouver la séparation, c'est le premier tiers de la note.

### Les six livrables

**D1 — La grille du dossier** (3 points). La grille des 12 points (C01), passée sur `commandes_2026.csv` et
`clients_2026.csv` : pour chaque point non nul, le compteur **avec son dénominateur** (« 17 sur 160 », jamais
« 17 »). Vous identifiez les sept défauts, vous les classez en *casse un total* / *fausse une analyse, une jointure
ou un import*, et vous écrivez la phrase qui prouve la séparation : quels sont les deux défauts qui faussent la
somme directe, et pourquoi les cinq autres ne la faussent pas.

**D2 — Le fichier réparé et son total** (4 points). `commandes_2026_propres.csv` : 152 lignes, total TTC
**8 209 940 FCFA** — à obtenir par votre méthode, pas à viser. Les 8 lignes retirées s'écrivent dans la feuille de
travail avec leur motif : 7 copies exactes (retirées sur la règle du contenu) et 1 **resaisie** — une ligne jumelle
qui ne diffère de son original que d'un champ (la date) et porte le plus grand `id_vente` ; le piège de l'énoncé,
c'est que le fichier compte **9 groupes en collision** : le neuvième est un ticket multi-lignes **légitime**
(deux lignes qui diffèrent sur l'heure, le client, le prix et le mode de paiement) et ses 2 lignes doivent
survivre. Une règle qui ne garde qu'une ligne par groupe (le plus petit `id_vente`, sans regard) tombe à 151 lignes
et 8 105 333 FCFA : vous écrivez ce que ce total a mangé.

**D3 — Le journal des transformations** (3 points). Cinq lignes au format du C06 (date, fichier, opération,
règle, compteur avant → après), couvrant au minimum : la conversion des 17 montants texte (dont 2 négatifs qui sont
des retours), le retrait des 8 doublons, la reconstruction des 12 dates hors norme, et le retrait des 2
quasi-doublons clients. Chaque ligne se referme : avant − après = retirés ou modifiés.

**D4 — Le README du dossier et le dictionnaire des trois fichiers** (3 points). Six sections, 56 lignes de cible
(C06) : scénario, tables avec leur grain, règles de gestion (retour = montant négatif ; `id_client = 0` = comptoir,
**pas** une donnée à remplir — 18 lignes dans le dossier), défauts constatés, ce qui manque volontairement. Le
dictionnaire déclare pour chaque fichier : encodage (les deux CSV du dossier portent un BOM ; le tarif est en
Windows-1252 — un import en Latin-1 y insère des caractères de contrôle invisibles), séparateur (`;` pour le tarif),
position de l'en-tête (ligne 4 pour le tarif, 3 lignes de bruit avant), et le type de chaque clé. Les 10 prix du
tarif sont à virgule décimale : le README dit comment les lire sur une machine à point.

**D5 — Le contrôle final avec ses résidus attendus** (3 points). La grille de 12 points sur le fichier réparé, avec
les résidus attendus **écrits avant** de lancer le contrôle (C06) : 0 montant non numérique, 0 remise hors [0 ; 1]
— à condition d'avoir traité les 5 remises en points, sinon 5 résidus —, 0 date hors norme ISO, 0 groupe de doublon,
1 groupe multi-lignes légitime à 2 lignes. La convergence est écrite avec l'écart : votre total 8 209 940 FCFA
contre l'`ATTENDU.json`, écart 0 — l'écart est le chiffre, pas le total.

**D6 — Le périmètre de protection de `clients_2026.csv` et sa version pseudonymisée** (4 points). Vous délimitez
les données personnelles (nom, téléphone : 132 lignes ; e-mail : les lignes renseignées ; ville, date de création),
vous mesurez ce que l'effacement des identifiants directs ne protège pas, et vous produisez
`clients_2026_anonymes.csv` : `id_client` figée et remplacée par un pseudonyme stable, nom/téléphone/e-mail
remplacés, **part de ré-identification résiduelle mesurée et écrite**. Le dossier compte 12 noms portés par deux
téléphones ou plus (homonymes) : vous écrivez pourquoi « dédoublonner sur le nom » y retirerait des clients réels,
et pourquoi la règle qui retire exactement les 2 quasi-doublons (132 → 130) est la clé nom normalisé + chiffres du
téléphone — pas le nom seul.

---

## 2. Ce qui est noté, ce qui est piégé

| Piège du dossier | Où il se cache | Ce qu'il enseigne |
|---|---|---|
| 17 montants en texte (« n nnn FCFA »), dont 2 négatifs | `commandes_2026.csv`, colonne N | la somme directe rate 17 lignes ; les 2 négatifs sont des retours que le contrôle de domaine ne voit qu'après conversion |
| 8 lignes en doublon (7 copies + 1 resaisie) | `commandes_2026.csv` | la resaisie n'est pas une copie exacte : la règle « contenu identique » ne la voit pas, la règle « un seul champ différent » la voit |
| 1 ticket multi-lignes légitime (2 lignes, 8 colonnes différentes) | `commandes_2026.csv` | « une ligne par groupe » mange une vente réelle (8 105 333 au lieu de 8 209 940) |
| 5 remises en points de pourcentage (12/18/25/30/18) | `commandes_2026.csv`, colonne K | la division par 100 est un test à faire, pas une réparation à appliquer |
| 12 dates en deux écritures (JJ/MM/AAAA et AAAA-MM-JJ) | `commandes_2026.csv`, colonne C | le tri chronologique et le pivot mensuel sont faux tant que les deux écritures cohabitent |
| 2 quasi-doublons clients (nom surchargé + téléphone sans espaces) + 12 homonymes | `clients_2026.csv` | la règle « même nom » retire bien plus que les 2 doublons ; la clé juste est nom normalisé + chiffres |
| 3 lignes de bruit, cp1252, `;`, décimales à virgule | `tarif_fournisseur.csv` | l'import par défaut lit 1 colonne, un en-tête faux, et des prix en texte |

---

## 3. Barème et seuil

- D1 : 3 points — grille complète avec dénominateurs (1) · les sept défauts en deux natures (1) · la phrase de
  séparation des totaux (1).
- D2 : 4 points — 152 lignes et 8 209 940 FCFA obtenus (1,5) · les 8 lignes retirées motivées ligne à ligne (1) ·
  le groupe légitime survit et l'erreur de la règle naïve est chiffrée (1,5).
- D3 : 3 points — cinq lignes au format complet (1) · chaque ligne se referme par son écart (1) · la conversion des
  montants se referme par un contrôle de convergence (1).
- D4 : 3 points — six sections lisibles sans ouvrir les fichiers (1) · encodages, séparateurs et en-têtes déclarés
  (1) · la convention `id_client = 0` écrite comme convention et non comme donnée manquante (1).
- D5 : 3 points — résidus attendus écrits avant le contrôle (1) · grille du réparé avec le groupe légitime nommé (1)
  · convergence écrite avec l'écart contre l'`ATTENDU` (1).
- D6 : 4 points — périmètre délimité et chiffré (1) · pseudonymisation stable qui ne casse aucune jointure (1) ·
  part de ré-identification résiduelle **mesurée et écrite** (1) · la règle des 2 quasi-doublons opposée à la règle
  du nom seul, avec les 12 homonymes en argument (1).

**Seuil de validation : 13/20.** Un livrable dont un compteur manque son dénominateur perd 0,5 point par compteur,
sans plafond : la précision du dénominateur est la matière du module, pas une coquille.

---

## 4. Correction des points d'attention

- **D1, séparation des totaux.** La somme directe sur la colonne N ne rate que les lignes non numériques : 17. Les
  doublons la faussent en double comptant 8 lignes. Les 5 remises, les 12 dates, les 2 quasi-doublons et l'encodage
  du tarif ne changent aucun montant : ils faussent une analyse (remises), un calendrier (dates), une jointure
  (clients) et un import (tarif). La phrase attendue : « Deux défauts cassent le total — 17 montants en texte non
  sommés et 8 lignes comptées deux fois ; les cinq autres laissent la somme intacte et cassent chacune une autre
  lecture du fichier. »
- **D2, le groupe légitime.** Le groupe formé du ticket `T01-230101-000140`, produit 74, quantité 3 : deux lignes
  qui diffèrent sur l'heure, le vendeur, le client, le prix, les trois montants et le mode de paiement. C'est une
  double vente réelle du même ticket, pas un doublon. La règle naïve « une ligne par groupe, plus petit `id_vente` »
  la réduit à 1 ligne : 151 lignes, 8 105 333 FCFA — l'écart 104 607 FCFA est le montant de la ligne mangée.
- **D2, la resaisie.** Le groupe du ticket `T01-230103-000122`, produit 103, quantité 3 : deux lignes identiques
  sauf la date. Ce n'est pas une copie exacte (le contrôle de contenu la laisse passer) ; c'est une ressaisie avec
  une erreur de date, reconnaissable à son `id_vente` plus grand. La règle de garde la retire sans toucher au
  groupe légitime, qui diffère sur 8 colonnes.
- **D5, les résidus attendus.** « 0 non numérique, 0 hors domaine, 0 hors norme, 0 groupe de doublon, **1 groupe
  multi-lignes légitime à 2 lignes** » — le résidu est écrit avant le contrôle ; un contrôle qui ne s'attendrait
  qu'à des zéros rejetterait le bon fichier.
- **D6, la part résiduelle.** Elle se mesure sur les colonnes conservées (ville, type, segment, date de création,
  conditions de paiement, plafond) : sur ce dossier, elle se compte en combinaisons désignant un client unique.
  L'e-mail, quand il est renseigné, encode souvent l'identifiant : le pseudonyme stable doit exister **avant**
  l'effacement, sinon la jointure avec `commandes_2026.csv` se rompt.
- **Le tarif.** Lu en Windows-1252 avec 3 lignes sautées : 10 lignes, 6 colonnes, 10 prix à virgule décimale. Lu en
  UTF-8, il casse à l'octet ; lu en Latin-1 sans saut, il donne une colonne et un en-tête faux. Le README déclare
  les trois réglages ; la formule de lecture des prix est celle qui énonce la virgule, pas celle qui l'hérite de la
  locale.
