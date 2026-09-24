# Évaluation M04 — « Qualité, préparation et documentation des données »

**Module M04 · durée totale 2 h 30 · quatre épreuves · seuils : quiz 11/15, exercices 14/20, étude de cas 12/20**

| Épreuve | Durée | Barème | Noté | Ce qui est attendu |
|---|---|---|---|---|
| A · Questions de récupération | 15 min | non noté | non | vérifier qu'on a lu les six chapitres avant de se tromper cher |
| B · Quiz | 25 min | /15 | oui | quinze questions à réponse unique, quatre blocs |
| C · Exercices pratiques | 50 min | /20 (auto-corrigé) | oui | quatre exercices menés jusqu'au chiffre sur le dossier du projet |
| D · Étude de cas | 60 min | /20, seuil 12 | oui | un dossier en quatre pages : « le stock indiqué est-il crédible ? » |

> Le score du module se lit ainsi : **B ≥ 11** et **D ≥ 12** valident le module ; le projet M04.P doit atteindre 13.
> Un candidat qui réussit B et échoue à D repasse uniquement D : savoir ce qu'est une quasi-identification ne
> dispense pas de dire si le comptage de 60 000 lignes est croyable.
> Tout nombre de cette évaluation est mesuré sur le socle livré ; les corrections le citent avec leur clé
> `m04_*`/`m04p_*` dans `chiffres_cites.json`.

---

## A · Questions de récupération (non notées)

À traiter sans document, en une ou deux phrases chacune. Elles ne sont pas comptées ; elles servent à repérer ce
qui n'est pas assimilé avant de perdre des points sur un détail.

1. Citez les cinq mécanismes d'absence du C02 et le traitement qui va avec chacun. Pourquoi `id_client = 0`
   (43 681 lignes, 2 813 668 030 FCFA) n'est-il aucun des cinq ?
2. Donnez les quatre niveaux où l'on peut chercher un doublon (C03) et, pour chacun, le résultat mesuré sur le
   fichier de ventes (0 / 0 / 3 440 / 8 453).
3. Citez les quatre familles de règles de contrôle (C04) avec un nombre mesuré chacune — et la famille qui a rendu
   24 180 alertes pour 0 erreur.
4. Quelles sont les deux voies indépendantes qui reconvertissent les 3 421 montants texte (C05), et quel nombre
   commun rendent-elles avant dédoublonnage ?
5. Quelles sont les quatre pièces que le C06 attend d'un dossier livré, et quel résidu **attendu** le contrôle
   final du fichier propre doit-il accepter (80 groupes) ?
6. Pourquoi les 973 remises à 12, 18, 25, 30 ne changent-elles aucun total, et pourquoi la division par 100 est-elle
   une réparation qui échoue son propre test ?
7. Quelle est la différence entre un identifiant direct et un quasi-identifiant, avec le chiffre du socle qui
   rend la distinction coûteuse (18 171 combinaisons uniques sur 20 809) ?

---

## B · Quiz (15 questions · 15 points)

**Barème : 1 point par question, une seule bonne réponse. Les réponses justifiées en une ligne rapportent un
demi-point de bonus, plafonné à 15.**

### Bloc 1 — Types et normalisation (Q1 à Q4)

**Q1.** La colonne `montant_ttc` contient 3 421 cellules du type `n nnn FCFA` parmi 239 939 nombres. Ce que
`=SOMME()` fait des 3 421 : a) les somme comme des nombres · b) les ignore, sans erreur · c) renvoie `#VALEUR!` ·
d) elles sont lues sans leur espace de milliers.

**Q2.** Normaliser `clients.nom` (élagage, minuscule, ponctuation retirée) fait passer 12 640 valeurs distinctes
à 12 342. Conclusion : a) 298 clients ont été supprimés · b) 298 écritures différentes d'un même nom se sont
rassemblées, sans que le nombre de clients change · c) 298 doublons exacts ont été fondus · d) la colonne est
corrompue.

**Q3.** Deux écritures d'un même téléphone : `+226 78 62 21 81 98` et `+2267862218198`. La colonne qui sert de clé
de jointure doit porter : a) le texte tel quel · b) les chiffres seuls · c) le nom du client · d) la ville.

**Q4.** `date_vente` est à 100 % en `AAAA-MM-JJ`, et 51 lignes portent une date postérieure au 31/08/2026, date du
relevé. L'action correcte : a) une formule de reformatage · b) un contrôle de domaine (date ≤ date du relevé) et une
décision documentée · c) la suppression des 51 lignes · d) aucune, le format est correct.

### Bloc 2 — Doublons et clés (Q5 à Q8)

**Q5.** La clé primaire rend 243 360 valeurs distinctes, mais 3 440 lignes sont en collision sur
(ticket, produit, quantité). Conclusion : a) la clé primaire est fausse · b) la clé métier voit ce que la clé
technique ne voit pas · c) le fichier est entièrement dupliqué · d) c'est une erreur de mesure.

**Q6.** 8 453 lignes partagent (ticket, produit) alors que la règle de garde n'en retire que 3 360. Explication :
a) un choix aléatoire · b) un même ticket peut légitimement porter plusieurs lignes sur un même produit (quantité,
heure ou client différents) · c) la clé compte mal · d) les 8 453 sont toutes des doublons.

**Q7.** La règle « même nom » sur les 23 912 clients fusionnerait 11 570 lignes. Réponse correcte : a) l'appliquer
puis vérifier a posteriori · b) la rejeter : elle retire 11 158 lignes de trop, des homonymes réels · c) la limiter
aux noms courts · d) l'appliquer aux noms avec espaces.

**Q8.** Les 412 quasi-doublons clients portent tous deux anomalies d'écriture (nom surchargé, téléphone sans
espaces), et 0 ligne conservée ne les porte. Ce qui s'en déduit : a) l'anomalie de format est la règle de
dédoublonnage · b) l'anomalie de format est un indice de rejeu, pas une règle : un doublon bien formaté ne serait
plus vu · c) le fichier est corrompu · d) il faut supprimer tous les espaces du fichier.

### Bloc 3 — Règles et valeurs aberrantes (Q9 à Q12)

**Q9.** `prix_unitaire_ht` : minimum 575, maximum 45 000 FCFA ; la règle des quartiles en signale 24 180 lignes.
Ces 24 180 lignes sont : a) des erreurs de saisie · b) la dispersion légitime du métier (du sac de ciment à la
palette d'ossature) · c) du bruit de mesure · d) des doublons.

**Q10.** La bande [0,95 ; 1,35] autour du prix catalogue rend 0 violation ; l'égalité au catalogue rend 232 981
« anomalies ». Leçon : a) le catalogue est faux · b) une règle qui signale 96 % d'un fichier sain est une règle
fausse, pas un fichier sale · c) il faut corriger les 232 981 prix · d) il faut utiliser le z-score.

**Q11.** 973 lignes ont `taux_remise` à 12, 18, 25 ou 30, mais un `montant_ht` correct et une TVA cohérente. La
division par 100 laisse 258 lignes au-dessus du plafond de 0,25. L'action défendable : a) diviser par 100 ·
b) reconstituer le taux depuis les montants (étendue 0,000 à 0,110, les 973 dans le domaine) et documenter ·
c) supprimer les 973 lignes · d) laisser tel quel sans note.

**Q12.** Le contrôle `qte_physique < seuil_alerte` déclenche sur exactement les mêmes 1 800 lignes que
`qte_physique < 0`, sur 60 000. Conclusion : a) le seuil est parfait · b) le seuil ne discrimine rien : le signal
réel est le signe ; les deux règles doivent être scindées (intégrité / risque) · c) les 1 800 lignes sont des
erreurs à supprimer · d) le seuil est trop bas.

### Bloc 4 — Documentation et protection (Q13 à Q15)

**Q13.** Le fichier propre garde 80 groupes en collision sur (ticket, produit, quantité), tous distincts par
l'heure, 0 indistincts. Le fichier est-il correctement dédoublonné ? a) non, à refaire · b) oui : le résidu est
attendu, écrit avant le contrôle, et les groupes sont des multi-lignes légitimes · c) c'est un bug du script ·
d) oui, tant que le résidu reste sous 100 groupes.

**Q14.** Une ligne de journal des transformations sans règle ni compteur avant → après est : a) une note, pas une
ligne de journal · b) une ligne valide, abrégée · c) une exigence d'audit · d) un risque juridique seulement.

**Q15.** On retire nom, téléphone et e-mail des clients, on garde (ville, type, segment, date de création) :
18 171 combinaisons sur 20 809 désignent un client unique. Conclusion : a) le fichier est anonymisé · b) 87,3 %
des combinaisons restent ré-identifiables : effacer l'identifiant direct n'est pas anonymiser · c) seuls `2 638` combinaisons ne désignent personne d'unique · d) il suffit de retirer la ville.

### Corrigé du quiz

Q1 **b** — `SOMME` ignore le texte sans erreur : c'est ce qui rend le défaut silencieux (écart du total naïf :
2 111 789 FCFA). Q2 **b** — 12 640 − 12 342 = 298 écritures rassemblées ; le nombre de lignes est inchangé.
Q3 **b** — les chiffres seuls : c'est la colonne rare discriminante du C03. Q4 **b** — la norme est respectée, la
réalité non ; la décision se documente, elle ne se corrige pas par formule. Q5 **b** — l'unicité technique n'est
pas l'unicité métier. Q6 **b** — 8 453 lignes partagent (ticket, produit), mais la clé métier complète (avec la
quantité) distingue les multi-lignes légitimes. Q7 **b** — 11 570 − 412 = 11 158 lignes de trop. Q8 **b** — la
règle de format décrit un lot passé ; la règle de décision reste la clé. Q9 **b** — 24 180 alertes pour 0 erreur.
Q10 **b** — la règle se juge à ce qu'elle attrape, pas au volume d'alertes. Q11 **b** — la reconstitution tient sur
les 973 ; la division échoue sur 258. Q12 **b** — deux règles au lieu d'une, un destinataire par niveau. Q13 **b** —
le contrôle attend des résidus, pas des zéros universels. Q14 **a** — sans règle ni compteur, la ligne ne referme
rien. Q15 **b** — 87,3 % de combinaisons uniques ; la date de création fait le travail des trois autres colonnes.

---

## C · Exercices pratiques (50 min · /20)

Tout se fait sur `03_exercices/dossier_M04/` (le dossier du projet, 160 lignes ; ATTENDU.json à consulter
**après** vos calculs).

**E1 — La grille du dossier (5 points).** Passez la grille des 12 points sur `commandes_2026.csv`. Note attendue :
les quatre compteurs non nuls **avec dénominateurs** (17 montants texte sur 160 ; 5 remises hors domaine sur 160 ;
12 dates hors ISO sur 160 ; 8 lignes en doublon sur 160), plus la mention des 18 lignes au comptoir comme
convention et non comme donnée manquante. 1 pt par compteur justifié, 1 pt pour la séparation « total / analyse ».

**E2 — Le dédoublonnage du dossier (5 points).** Produisez 152 lignes et le total **8 209 940 FCFA**. Note attendue
: les 8 lignes retirées motivées (7 copies exactes + 1 resaisie reconnue à son champ unique, la date), le groupe
légitime (2 lignes, 8 colonnes différentes) survécut, et le chiffre de la règle naïve (151 lignes, 8 105 333 FCFA,
l'écart 104 607 FCFA identifié comme le montant de la ligne mangée). 2 pts pour le résultat, 2 pour la
motivation ligne à ligne, 1 pour l'opposition à la règle naïve.

**E3 — Conversion et import (5 points).** (a) Convertissez les 17 montants texte par le double retrait
(suffixe puis espaces) et montrez que les 2 retours à montant texte ne passent le contrôle de domaine
(retour ⇒ montant négatif) qu'après conversion : 1,5 pt. (b) Importez `tarif_fournisseur.csv` en déclarant
l'encodage Windows-1252, le séparateur point-virgule et les 3 lignes à sauter ; lisez les 10 prix à virgule
décimale par une formule qui énonce la virgule ; écrivez le coût du mauvais choix d'encodage (39 octets dont le
décodage Latin-1 fait des caractères de contrôle invisibles) : 3,5 pts.

**E4 — « Les trois chiffres faux » (5 points).** Le corrigé enseignant `rapport_defauts.json` du socle annonce
3 360 montants en texte, 2 640 dates en formats mixtes, 1 880 clients sans ville. Mesurez les trois valeurs
réellement livrées — 3 421, 0 et 1 911 — par un compteur unique chacune (3 pts), et écrivez la phrase qui dit
pourquoi un corrigé se génère **après** la fabrication du fichier, jamais avant (2 pts). Mention attendue : le
cas « 61 catégories hétéroclites annoncées, 44 ou 61 selon la définition » est une question de définition, pas une
troisième erreur — confondre les deux est le piège de l'exercice.

---

## D · Étude de cas (60 min · /20, seuil 12) — « Le stock indiqué est-il crédible ? »

**Contexte.** Le magasinier a remis `stocks_quotidiens.csv` : 60 000 lignes, 7 colonnes (`date`, `id_produit`,
`id_magasin`, `qte_theorique`, `qte_physique`, `seuil_alerte`, `valeur_stock_ht`). La direction demande : peut-on
se fier au stock indiqué ? Vous rendez un dossier de quatre pages.

**Le fichier, mesuré.** 154 produits × 6 dépôts = 924 séries, sur 1 339 jours distincts (du 01/01/2023 au
31/08/2026). 0 cellule vide. `qte_theorique` : 0 à 1 795, **aucun négatif**. `qte_physique` : **1 800 négatifs**
(3,0 % des lignes), présents sur les 154 produits sans exception. `seuil_alerte` : 0 à 448. Le contrôle
`qte_physique < seuil_alerte` déclenche sur exactement les mêmes 1 800 lignes que `qte_physique < 0`.
Écart théorique − physique : moyenne 2,77, maximum 532, **118 lignes au-dessus de 100**, 2 au-dessus de 500.

**Le livrable, en quatre parties :**

1. **Ce que le fichier est** (description et grain) : 3 points.
2. **Le verdict de crédibilité, en deux temps** : comme *comptage* (1 800 négatifs impossibles sur 154 produits :
   le comptage n'est pas fiable) et comme *signal* (les 1 800 alertes sont exactement les 1 800 négatifs : le
   seuil n'ajoute rien, le signal utile est le signe) : 4 points.
3. **Le calibrage de l'écart** : avec les valeurs mesurées et leurs dénominateurs, délimitez la file de travail —
   1 800 négatifs à recompter + 118 écarts au-dessus de 100 à instruire — et dites pourquoi 532 de maximum sur
   une moyenne de 2,77 change la nature du problème (queue, pas bruit) : 4 points.
4. **Trois règles qui rendraient le prochain fichier crédible**, chacune avec son niveau (bloquant / corriger /
   surveiller / ignorer tracé) et son destinataire : (a) intégrité — quantité physique négative ⇒ recomptage
   programmé (niveau 2, magasinier) ; (b) risque — seuil recalibré pour un taux d'alerte traitable (les 118 plus
   grands écarts d'abord, niveau 3, responsable de dépôt) ; (c) journal de comptage — date, produit, dépôt,
   théorique, physique, écart, compteur (le journal que ce fichier n'a pas) : 4 points.

**Grille de qualité (complément des 4 parties, 5 points).** Ce que le fichier ne peut pas dire : 3 points —
`qte_theorique` est supposé juste, or le logiciel de gestion n'est pas dans le dossier : la cohérence externe
(ventes ↔ mouvements de stock) est impossible à vérifier ici, et le dossier le dit. Reproductibilité : 2 points —
chaque chiffre du dossier est reproducible par une formule ou un compteur nommé.

**Ce qui est piégé dans l'étude.** (1) Répondre « oui, c'est fiable » ou « non, c'est faux » d'un bloc : le
verdict doit être en deux temps. (2) Proposer de supprimer les 1 800 lignes négatives : ce sont le signal, pas le
bruit. (3) Citer un écart sans son dénominateur. (4) Oublier que le seuil actuel est **redondant** avec le signe —
la règle qui compte deux fois le même événement n'est pas une règle, c'est du doublon de contrôle (le mot du C03,
réemployé au contrôle).

---

## Lecture des résultats

- **B ≥ 11 et D ≥ 12** : module validé (le projet M04.P doit, de son côté, atteindre 13/20).
- **B < 11** : le socle des définitions n'est pas acquis ; repasser B et la récupération A, le module reste ouvert.
- **D < 12 avec B ≥ 11** : le candidat sait ce qu'est un quasi-identifiant mais ne sait pas dire si un comptage de
  60 000 lignes est croyable ; repasser D uniquement.
- Le projet M04.P se note séparément (13/20 de seuil) et pèse sur la validation finale du module.
