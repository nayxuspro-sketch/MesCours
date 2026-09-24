# Module M03.C02 — Formats et saisie intelligente : monétaire FCFA, dates, validation, mise en forme conditionnelle

**Outil de ce chapitre : le tableur seul, sur le classeur de l'atelier.** Durée indicative : 4 h. Niveau : N2.

> **L'idée du chapitre.** Le chapitre C01 a montré qu'un montant peut être un texte et que rien ne le crie. Voici les
> trois gestes qui manquent : **dire ce qu'est une donnée** — la convertir, non l'habiller ; **empêcher la prochaine
> erreur d'entrer** — la validation des données ; **faire voir les défauts sans les chercher** — la mise en forme
> conditionnelle. Un classeur bien formaté n'est pas un classeur joli : c'est un classeur dont les erreurs se voient
> de loin.

> **Base de travail — deux chemins pour une seule donnée.** Le matériel est celui du chapitre précédent : le classeur
> `01_socle_donnees/data/projection/m03_classeur_atelier.xlsx`, le fichier reçu
> `01_socle_donnees/data/projection/ventes_magasin5_2025.csv`, la donnée nettoyée
> `01_socle_donnees/data/reference/ventes_magasin5_2025_ATTENDU.csv`, les objectifs
> `01_socle_donnees/data/brut/objectifs_de_ca.csv`. Chez vous : `donnees/projection/` et `donnees/reference/`. Les
> blocs écrivent le chemin de l'atelier ; remplacez le préfixe si vous travaillez dans votre dossier. Séparateur
> point-virgule, UTF-8, franc CFA (FCFA), virgule décimale. Chiffres cités :
> `01_socle_donnees/data/reference/chiffres_cites.md`, section M03. **Règle de ce chapitre : on travaille sur une
> copie de `ventes_brutes` nommée `ventes_en_forme`** — la feuille de preuve ne se met jamais en forme.

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous saurez :

1. **Lire** ce que le tableur a compris d'une saisie — nombre, texte, date, heure — et prévoir ce qu'il comprendra
   d'une colonne que vous n'avez pas encore ouverte.
2. **Écrire** les formats de gestion : monétaire franc CFA sans décimale, négatif en rouge, pourcentage à une
   décimale, date courte, et les formats personnalisés à sections.
3. **Convertir** une colonne de textes en nombres par trois voies, et le prouver au compteur, pas à l'œil.
4. **Poser** une validation qui refuse une quantité de 14 000 sans rejeter les lignes de retour — et dire ce
   qu'une validation ne protège pas.
5. **Régler** une mise en forme conditionnelle de contrôle, l'ancrer sur la bonne cellule et l'ordonner.

---

## 2. Pourquoi cette notion est importante

**Situation 1 — la mise en forme qui ne répare rien.** Sur le fichier reçu, 486 des 489 montants sont du texte. Un
stagiaire applique un format monétaire : la colonne prend le suffixe FCFA, le total passe de « rien » à « rien », et
l'on écrit dans la note que le chiffre n'est pas disponible. Le format a touché au rendu, pas à la nature. La
conversion, elle, change la nature — et sa preuve tient en un nombre : le compteur de valeurs numériques passe de 0
à 480.

**Situation 2 — la date qui se trie à l'envers.** La colonne `date` du fichier reçu mélange deux écritures : 424
lignes en ISO et 65 en notation française. Laissée en texte, la colonne se trie caractère par caractère : le
`01/01/2025` des lignes françaises se range avec les janvier, et `2025-09-02` se range avec les `2`. Triée comme
date, la même colonne rend un calendrier lisible sur 335 jours d'amplitude et 31 jours d'activité. Le tri n'a rien
réparé : c'est le typage, en amont, qui a tout décidé.

**Situation 3 — la remise saisie en points.** Un vendeur corrige une remise : au lieu de `0,11`, il tape `11`. Rien
ne bronche, la ligne perd un dixième de son prix — un montant *possible*, donc invisible. Trois heures plus tard, le
tableau croisé affiche une catégorie effondrée et l'on cherche une panne où il y a une saisie. Un format pourcentage
et une validation bornée à 0,25 ferment la porte.

> **Dans les faits.** Les audits de classeurs de gestion rapportent que la majorité des anomalies de chiffres vient
> de la saisie et du typage, non des formules. Un garde-fou se pose en vingt secondes ; le même défaut découvert en
> comité de direction coûte une décision annulée.

---

## 3. Explication simple

Quand vous tapez dans une cellule, le tableur **classe** avant d'afficher. Quatre bacs : les nombres, les dates (qui
sont des nombres), les heures (des fractions de jour), et le reste — le texte. Le classement dépend de votre
**réglage régional** (virgule ou point décimal), de la **forme** tapée (une espace dans `1 229 678` en fait un
texte), et du **format déjà présent** (une cellule au format Texte garde tout tel quel).

Le **format** vient après, comme une étiquette : décimales, séparateurs, symbole, couleur des négatifs. Il ne décide
jamais de ce que verront `SOMME()`, un tri ou un tableau croisé. Deux conséquences : on choisit le format **avant**
de saisir, et l'on vérifie la nature d'une colonne importée **avant** de l'habiller.

Trois dispositifs, trois métiers : la **validation des données** interdit une saisie impossible ; la **mise en forme
conditionnelle** signale ce qui est déjà là ; la **colonne utilitaire** du chapitre précédent tranche ligne par
ligne.

---

## 4. Vocabulaire essentiel

| Français — English | Définition simple | Piège à éviter |
|---|---|---|
| **Format de nombre — number format** | Modèle d'affichage : décimales, séparateurs, symbole, négatifs. | Le confondre avec un type : il ne convertit rien. |
| **Format personnalisé — custom format** | Modèle écrit à la main, `# ##0 "FCFA";[Rouge]-# ##0 "FCFA"`. | Ne pas le documenter : six mois plus tard, nul ne sait d'où vient le suffixe. |
| **Nombre de série de date — date serial** | Une date est un compteur de jours, l'heure sa partie décimale. | Croire qu'une date affichée est une date stockée. |
| **Validation des données — data validation** | Règle qu'une plage applique à ce qu'on y saisit. | Croire qu'elle filtre le collage et l'import : elle ne garde que la frappe. |
| **Liste déroulante — drop-down list** | Validation de type Liste, adossée à une plage ou une table. | Pointer la plage de références sans la figer : la liste décroche. |
| **Mise en forme conditionnelle — conditional formatting** | Format appliqué quand une condition est vraie. | Ancrer la formule ailleurs que sur la première cellule de la plage. |
| **Coercition — coercion / type casting** | Tentative de forcer un contenu dans un type demandé. | Convertir en perdant : l'illisible devenu 0 compte comme une donnée. |
| **Arrondi d'affichage — display rounding** | Écart entre la valeur stockée et ce qui est montré. | Reporter les valeurs affichées dans une note : le total ne tombe plus. |

> **Définition.** Un **format à sections** s'écrit `positif;négatif;zéro;texte`. Notre colonne de montants pourrait
> porter `# ##0 "FCFA";[Rouge]-# ##0 "FCFA";"-"` : un montant de 1 229 678 FCFA en noir, un retour de 150 804 FCFA
> en rouge, et un tiret à la place des zéros, pour qu'une ligne vide ne se lise pas comme une valeur nulle.

---

## 5. Cours approfondi

![Un même montant selon qu'il est texte, nombre, ou nombre mis en forme — et la règle de validation qui arrête 14 000](../figures/M03_C02_formats_saisie.svg)

### 5.1 Ce que le tableur a compris, et pourquoi

Un même chiffre, neuf saisies, trois sorts :

| Vous tapez | Le tableur lit | Pourquoi |
|---|---|---|
| `1229678` | nombre | chiffres seuls |
| `1 229 678` | **texte** | l'espace casse la lecture numérique |
| `1229.678` | texte | le point n'est pas le séparateur décimal du réglage français |
| `1 229,678` | nombre | espace de milliers admise, virgule lue |
| `0.03` | **texte** | c'est le cas des 489 remises du fichier reçu |
| `0,03` | nombre | bon séparateur |
| `2025-01-01` | date | l'ISO est reconnu presque partout |
| `01/01/2025` | date | notation française reconnue |
| `1er janv. 2025` | texte | aucune règle de lecture |

Cette table explique les trois défauts mesurés du fichier reçu : 486 montants en texte (les espaces de milliers), 489
remises en texte (le point), et 65 dates écrites à la française contre 424 en ISO. Elle explique aussi pourquoi un
même fichier donne trois chiffres : 0 FCFA en sommant la feuille de preuve, 2 444 FCFA si l'import automatique a
converti trois cellules, 36 073 185 FCFA sur la donnée nettoyée.

> **À retenir.** Le tableur ne corrige pas une saisie, il la **classe**. Ce que vous avez voulu dire ne compte pas :
> la seule chose qui compte est ce qui a été lu.

### 5.2 Les quatre formats de la gestion

- **Montants** : `# ##0 "FCFA"` — le format du classeur d'atelier. Aucune décimale : le franc CFA se compte, et
  153 596,42 FCFA dans un tableau se lit plus mal que 153 596.
- **Négatifs** : `# ##0 "FCFA";[Rouge]-# ##0 "FCFA"`. Nos 8 lignes de retour pèsent −283 933 FCFA : elles sautent
  aux yeux sans une seule règle de mise en forme.
- **Taux** : `0,0 %`. La plus forte remise de la donnée nettoyée est 11 % ; une cellule qui affiche `1 100,0 %`
  crie qu'on a saisi `11`.
- **Dates** : `JJ/MM/AAAA` pour le contrôle, `mmm. aaaa` pour un graphique. Le format court `JJ/MM` perd l'année et
  rend tout rapprochement annuel impossible.

Trois habitudes : appliquer le format sur la **colonne entière**, le **documenter** dans `Aidez-moi` (une ligne par
colonne : format et pourquoi), et ne jamais coder une information par la seule couleur de police — la couleur se
perd à l'export, la règle non.

### 5.3 Les dates : un compteur de jours, pas une image

> **Définition.** Une date stockée comme date est un **nombre de série** : un compteur de jours, dont l'heure est la
> partie décimale. Le contrôle est cruel de simplicité : passez `B2` de la feuille `ventes` en *Nombre général*, vous
> verrez un entier ; la différence entre la première et la dernière ligne de l'extrait, 335, est exactement le nombre
> de jours du 01/01/2025 au 02/12/2025.

Trois conséquences de travail. **Une colonne à moitié date, à moitié texte, est pire qu'une colonne entièrement
texte** : tri et filtres ne s'appliquent plus au tout — chez nous, les 424 lignes ISO et les 65 lignes françaises se
rangent chacune de leur côté. **Une date lue au clavier dépend du poste** : le même fichier, sur un réglage régional
différent, donne des dates en texte ; c'est la première cause de « ça marchait chez moi », et la parade est l'import
assisté à types forcés, ou `DATE()` avec ses trois arguments entiers. Enfin, **une date figée n'est pas une date qui
bouge** : `Ctrl` + `;` insère la date du jour comme valeur, `=AUJOURDHUI()` la recalcule — la première atteste, la
seconde alerte ; une fiche de prise en main veut la première, un tableau de bord la seconde.

### 5.4 Convertir vraiment : trois voies, une preuve

1. **Collage spécial, opération Ajouter 0.** Une cellule contenant `0`, copiée, *Collage spécial → Ajouter* sur la
   colonne. Les textes chiffrés deviennent nombres ; les valeurs réellement illisibles renvoient une erreur. Rapide,
   destructeur.
2. **Colonne utilitaire.** `=CNUM(SUBSTITUE(SUBSTITUE(M2;" ";"");" ".""))` lit le texte après avoir retiré les
   espaces et les points. C'est la voie du classeur : la valeur d'origine reste visible à côté, et l'échec
   s'affiche (`#VALEUR!`) au lieu de se noyer dans un 0.
3. **Conversion à l'import**, en forçant le type de chaque colonne dans l'assistant — la seule qui répare aussi les
   dates, parce qu'elle décide avant que le tableur n'ait classé. Pour un nettoyage rejouable, le module M05 le
   confiera à Power Query ; ici, on fait les trois à la main pour savoir ce que chacune perd.

> **Définition.** On parle de **coercition** quand le tableur force un contenu dans un type demandé :
> `=CNUM("56 658")` échoue, `=CNUM("56658")` réussit, `=CNUM("")` renvoie `#VALEUR!`. Un nettoyage qui ne dit pas
> combien de cellules il a fait échouer n'est pas un nettoyage : c'est une perte.

**La preuve est le compteur, pas l'œil.** *Nombre de valeurs numériques* doit passer de 0 à 480 et la somme redevenir
36 073 185 FCFA. Une conversion qui rend 489 nombres sur la feuille de preuve doit mener à 36 339 317 FCFA — les
266 132 FCFA d'écart étant les 9 doublons : la soustraction des doublons est une seconde opération, pas un
sous-produit de la première.

### 5.5 Validation des données : interdire la prochaine erreur

*Données → Validation des données* attache une règle à une plage. Trois types servent en gestion.

- **Liste** : les 7 catégories, les 6 magasins, l'oui/non d'un retour. Une liste adossée à une plage doit la figer
  (`$A$2:$A$8`) ou, mieux, pointer une table nommée.
- **Nombre entier compris entre** : `quantite` de `1` à `500` refuse la ligne à 14 000 du fichier reçu — et refuse
  aussi les retours, dont la quantité descend jusqu'à −13. La règle juste est **personnalisée** :
  `=ET(I2>=-500;I2<=500)`, qui borne des deux côtés et admet le retour.
- **Nombre décimal compris entre** pour `remise` : `0` à `0,25`. Le fichier nettoyé plafonne à 11 %, le fichier de
  la direction prévoit des remises contractuelles jusqu'à 25 %. Le message d'erreur dira : « la remise s'exprime en
  pourcentage : 11 % se saisit 0,11 ».

> **Attention.** Trois limites, qu'aucune aide en ligne ne résume aussi net : la validation **ne s'applique ni au
> collage ni à l'import** — un `Ctrl` + `V` par-dessus la cellule écrase la règle ; une règle posée sur la colonne
> entière laisse la ligne 490 du prochain import sans garde-fou, il faut la *copier* sur la plage de données ; et un
> message qui ne dit pas la valeur attendue pousse l'utilisateur à cocher « Tout ignorer » dès le premier refus.

### 5.6 Mise en forme conditionnelle : le détecteur qui ne dort pas

1. **Texte dans une colonne qui devrait être numérique.** Plage `M2:M490`, règle *Utilisez une formule*,
   `=NON(ESTNUM(M2))` : sur la feuille de preuve, 489 cellules allumées ; 486 après un import automatique qui en a
   converti trois. C'est un contrôle, pas un nettoyage.
2. **Montant hors de l'échelle.** `=M2>1000000` : 4 lignes de l'extrait dépassent le million, dont celle de
   1 229 678 FCFA. Une ligne à six chiffres mérite une phrase dans la note.
3. **Retours.** `=M2<0` : 8 lignes, −283 933 FCFA. Le format `[Rouge]` les montre déjà ; la règle les rend
   impossibles à manquer.
4. **Barre de données** sur `montant_ttc` : la distribution apparaît sans calculer, et l'on voit la colonne écrasée
   par sa queue.
5. **Valeurs en double** sur `n_ticket` : les 9 doublons sautent aux yeux avant tout tri.

> **Définition.** L'**ancrage** d'une règle de mise en forme conditionnelle est la cellule où l'on se trouvait quand
> on l'a écrite : la formule est ensuite reportée *relativement* sur chaque cellule de la plage. `=NON(ESTNUM(M2))`
> créée avec `M5` active juge la ligne 2 sur la ligne 5 — et produit un décompte faux de trois unités, avec des
> couleurs plausibles.

Dans **Gérer les règles**, trois réglages distinguent l'outil du sapin : cochez *Arrêter si vrai* pour que la
première règle gagne ; bornez la portée sur « ce qui est présent dans le fichier de travail », pas la feuille
entière ; et gardez **trois règles maximum par feuille**, chacune reliée à une ligne de la fiche de prise en main.

### 5.7 Les gestes de saisie qui font gagner une heure

`Tab` et `Maj` + `Tab` pour parcourir une ligne sans quitter la saisie. `Ctrl` + `Entrée` pour écrire la même valeur
dans toute la sélection — 489 cellules d'un coup, par exemple le taux de 18 % ou un libellé de source. `Alt` +
`Entrée` pour un retour à la ligne dans une cellule, à réserver aux en-têtes et jamais aux données. `Ctrl` + `;` pour
une date figée. La **poignée de recopie incrémentée**, qui sur `Janvier` produit les 12 mois et sur `lun.` les
lundis — c'est elle qui construira la grille mensuelle en C07. Enfin `Suppr` contre `Ctrl` + `-` : le premier efface
la valeur, la seconde supprime la **ligne**, ce qui n'a rien d'équivalent quand une table nourrit des formules.

> **Boîte à outils.** `Ctrl` + `1` (Format de cellule), `Ctrl` + `Maj` + `1` (nombre avec séparateurs),
> `Ctrl` + `Maj` + `2` (heure), `Ctrl` + `Maj` + `3` (date), `Ctrl` + `Maj` + `$` (monétaire),
> `Ctrl` + `Maj` + `%` (pourcentage), `Ctrl` + `Maj` + `~` (retour au format Général — le « montre-moi ce que tu
> stocks » de ce chapitre), et *Accueil → Mise en forme conditionnelle → Nouvelle règle*. Dans LibreOffice Calc, les
> formats et `Ctrl` + `1` sont identiques ; la validation s'appelle *Données → Validité* et la mise en forme
> *Format → Conditionnelle → Liste*.

---

## 6. Exemple concret : trois lignes saisies, quatre pièges refermés

Sur la copie `ventes_en_forme`, on saisit ce qu'un magasin enverrait par courriel, et l'on regarde ce que font les
garde-fous.

| Saisie | Sans garde-fou | Avec format, validation et détection |
|---|---|---|
| Quantité `14 000` | acceptée ; la ligne devient un bruit de plusieurs millions | refusée : « Quantité entre −500 et 500 » |
| Quantité `-13` (un retour) | acceptée, personne ne la voit | acceptée par la règle personnalisée, et en rouge par `[Rouge]` |
| Remise `11` | acceptée ; la ligne perd un dixième de son prix | refusée ; en `0,0 %`, la saisie `0,11` affiche `11,0 %` |
| Montant `56 658` en texte | entre dans la colonne, jamais sommé | allumé par `=NON(ESTNUM(M2))` : la ligne est à reprendre |

Le quatrième cas est le plus fréquent du métier : on ne réimporte pas le fichier, on **corrige une ligne à la main**.
La détection est ce qui empêche la correction d'ouvrir un second défaut.

## 7. Démonstration pas à pas : la colonne de contrôle de saisie

Quatre étapes sur la copie `ventes_en_forme` (colonnes du fichier reçu : `I` quantité, `K` remise, `M` montant TTC).

**1. Préparer.** Copie de `ventes_brutes`, largeurs ajustées, ligne supérieure figée, format
`# ##0 "FCFA";[Rouge]-# ##0 "FCFA"` sur `L2:M490`. La barre d'état sur `M` dit toujours *valeurs numériques : 0* : le
format n'a rien changé, et c'est la leçon.

**2. Convertir.** Colonne utilitaire `O` : `=CNUM(SUBSTITUE(SUBSTITUE(M2;" ";"");" ".""))`. Sans les deux
`SUBSTITUE`, seules les trois cellules écrites sans espace passent (797, 821 et 826 FCFA, soit 2 444 FCFA) ; avec,
les 489 passent. Copiez `O`, *Collage spécial → Valeurs* sur `M`, supprimez `O` : la somme est 36 339 317 FCFA.

**3. Retirer les doublons.** *Données → Supprimer les doublons* (le geste proprement dit est en C03) : 9 lignes
partent, 480 restent, la somme tombe à 36 073 185 FCFA et le compteur à 480. Les trois nombres se suivent : c'est
cette chaîne qui rend la conversion défendable.

**4. Statut de saisie.** En `N`, titre « statut », et sur chaque ligne :
`=SI(NON(ESTNUM(M2)),"montant non numérique",SI(OU(I2>500;I2<-500),"quantité hors bornes",SI(OU(K2<0;K2>0,25),"remise hors bornes","conforme")))`.
Sur la donnée nettoyée : 480 « conforme » — la quantité maximale y est 68 et aucune ligne ne dépasse 100, la remise
maximale 11 %. Sur la feuille de preuve avant conversion, le même texte écrit 489 fois « montant non numérique ».

**Contrôles qualité du chapitre.**

| # | Contrôle | Seuil | Résultat attendu | Si échec |
|---|---|---|---|---|
| 1 | Somme de `montant_ttc` après conversion, avant dédoublonnage | ±1 FCFA | 36 339 317 FCFA | conversion partielle ou `SUBSTITUE` oubliée |
| 2 | Somme après suppression des doublons | ±1 FCFA | 36 073 185 FCFA | 9 lignes de moins, ou de trop |
| 3 | *Nombre de valeurs numériques* sur `M` | identité | 480 | format pris pour une conversion |
| 4 | Décompte de la colonne `statut` | deux nombres | 7 quantités hors bornes · 8 retours | règle mal bornée : retours rejetés ou non détectés |
| 5 | Remise maximale | 0,1 point | 11,0 % | colonne restée en point décimal |

## 8. Erreurs fréquentes

1. **Confondre embellissement et réparation.** Un format monétaire sur une colonne texte produit une colonne texte
   jolie : le total ne bouge pas.
2. **Convertir sans garder la valeur d'origine.** Écraser `56 658` rend impossible la preuve que 486 lignes ont été
   touchées. On convertit dans une colonne utilitaire, puis on remplace — pas l'inverse.
3. **Croire la donnée protégée par une validation.** Elle ne filtre ni collage, ni import, ni formule. Sur un
   fichier qui entre tous les jours, la protection utile est la détection relue après chaque import.
4. **Écrire une règle avec la mauvaise cellule active.** Le décalage d'ancrage produit des couleurs justes pour de
   mauvaises raisons — le pire résultat possible, parce qu'il est vraisemblable.
5. **Reporter les valeurs affichées.** Deux lignes affichent 12 % et 12 %, leurs valeurs sont 0,115 et 0,121 : le
   chiffre cité dans une note vient de la barre de formule, avec sa décimale.
6. **Sauver en `.csv` pour alléger.** Formats, validations et mises en forme conditionnelles ne survivent pas à
   l'export ; seule la donnée reste. Le `.csv` est un canal d'échange, jamais un classeur de travail.

> **Attention.** Le piège le plus coûteux de ce chapitre est un arrondi : le total de la colonne recalculée diffère
> du total enregistré de **4 FCFA**, et ce n'est pas une faute. Six lignes de l'extrait ont un produit qui tombe
> exactement à un demi-franc, et sur quatre d'entre elles la règle d'arrondi choisie change le résultat. Dites la
> vôtre, dans `Aidez-moi` : « arrondi à l'unité, au demi-franc supérieur » — sinon un relecteur croisera deux
> tableaux à 4 FCFA près et perdra une heure à chercher une erreur inexistante.

## 9. Bonnes pratiques professionnelles

1. **Un format par famille de colonne, écrit une fois** et nommé dans `Aidez-moi` : montants, taux, dates,
   quantités. Les dérives unitaires viennent des formats posés cellule à cellule.
2. **La devise dans le format, jamais dans la cellule** — un `FCFA` tapé dans une cellule de montant en fait un
   texte, exactement le défaut que nous venons de réparer.
3. **Tout négatif visible** : format `[Rouge]` ou règle sur `<0`. Masquer les 8 retours gonflerait le chiffre de
   l'extrait de 0,8 %.
4. **Validation + commentaire + ligne de fiche.** La règle vit dans la cellule, sa justification dans le
   commentaire, son existence dans la fiche. Une validation non documentée est supprimée à la première gêne, et la
   gêne arrive toujours.
5. **La colonne de statut avant la couleur.** Le texte « montant non numérique » se filtre, se compte, s'imprime en
   noir et blanc ; le jaune, non.

> **Conseil professionnel.** Avant d'envoyer un classeur, testez-le en noir et blanc : *Fichier → Imprimer →
> Aperçu*, niveaux de gris. Si les lignes que vous vouliez signaler disparaissent, votre signal reposait sur une
> couleur et non sur une règle — écrivez le mot dans la colonne de statut, et gardez la couleur par-dessus.

## 10. Exercice guidé — formats, conversion, garde-fous (30 min, /10)

**Commande.** Sur une copie de `ventes_brutes` nommée `ventes_en_forme`, menez les six étapes et notez, à chacune,
ce qu'affiche la barre d'état sur `montant_ttc`.

| Étape | Geste | Nombre attendu |
|---|---|---|
| 1 | Format monétaire sur `L2:M490` | valeurs numériques 0 · somme 0 |
| 2 | Colonne utilitaire, `CNUM` seul, sans `SUBSTITUE` | 3 · 2 444 FCFA |
| 3 | Même colonne avec les deux `SUBSTITUE` | 489 · 36 339 317 FCFA |
| 4 | Collage spécial → Valeurs sur `M`, suppression de l'utilitaire | 489 · 36 339 317 FCFA |
| 5 | *Supprimer les doublons* | 480 · 36 073 185 FCFA · moyenne 75 152 FCFA |
| 6 | Validation `=ET(I2>=-500;I2<=500)` et règle `=NON(ESTNUM(M2))` | refus sur 14 000, acceptation de −13, 0 cellule allumée |

**Démarrage.** Les étapes 1 à 3 sont le point de bascule : le format ne change pas le compteur, la conversion le
change, et `SUBSTITUE` change la conversion. Notez les trois paires de nombres avant d'aller plus loin. À l'étape 3,
la somme attendue est 36 339 317 FCFA, soit 266 132 FCFA de trop : ce sont les doublons, et l'étape 5 doit les faire
disparaître — une conversion et un dédoublonnage sont deux opérations, pas une. À l'étape 6, tapez les deux valeurs
tests : 14 000 doit être refusé, −13 accepté ; si −13 est refusé, votre règle borne à 1 et vous venez d'interdire
les retours.

**Barème (10 points).** Six étapes menées, deux nombres notés à chaque étape (4) · les deux sommes exactes avant et
après dédoublonnage (2) · validation bornée des deux côtés avec message rédigé (2) · règle de détection ancrée sur
la première cellule de la plage, *Arrêter si vrai* coché (2).

## 11. Exercices autonomes

**Exercice 2.1 (★) — Les neuf saisies.** Dans une feuille neuve, recopiez les neuf contenus du tableau §5.1, un par
ligne. Notez l'alignement, ce que rend la barre de formule, et le compteur de valeurs numériques. Concluez par la
phrase : « le tableur lit … ».

**Exercice 2.2 (★) — Ce que la cellule stocke.** Sur `ventes`, passez `montant_ttc` en *Nombre général*, notez
`M2` et `M356`, repassez en monétaire, puis comparez la somme des valeurs affichées et la somme réelle de la
colonne. Écrivez la phrase qui évitera à un lecteur de chercher les centimes perdues.

**Exercice 2.3 (★★) — Trois voies pour une date.** Sur une copie, convertissez la colonne `date` du fichier reçu
par les trois voies : format seul, import avec type forcé, colonne utilitaire reconstruisant `DATE()` avec `STXT` et
`NBCAR` sur les 65 lignes à la française. Contrôlez chaque voie par trois nombres : cellules reconnues, bornes de
période, résultat du tri du dernier mois.

**Exercice 2.4 (★★) — La validation qui n'a rien vu.** Posez « entier de 1 à 500 » sur `quantite` d'une copie, puis
collez par-dessus la plage venue de `ventes` (qui contient les 8 retours). Comptez ce qui est passé quand même, et ce
que la validation est devenue. Écrivez la règle qui aurait vu, et les deux lignes de fiche qui la justifient.

**Exercice 2.5 (★★) — Le rouge qui ment.** Appliquez `=NON(ESTNUM(M5))` à la plage `M2:M490` sur une colonne
partiellement convertie, puis la règle correctement ancrée. Comparez les deux décomptes, expliquez l'écart par la
mécanique d'ancrage, et terminez par l'ordre des règles dans *Gérer les règles*.

## 12. Correction détaillée

**Exercice 2.1.** Restent du texte : `1 229 678`, `1229.678`, `0.03`, `1er janv. 2025` — à gauche, ignorés par le
compteur. Deviennent des nombres : `1229678`, `1 229,678`, `0,03` — à droite, comptés. Deviennent des dates (donc
des nombres) : `2025-01-01` et `01/01/2025`. Phrase attendue : « le tableur lit ce que son réglage régional
autorise, et rien d'autre ».

**Exercice 2.2.** En *Nombre général*, `M2` rend 56658 et `M356` rend 1229678 ; en monétaire, les mêmes entiers
précédés de l'espace de milliers et suivis de FCFA. La somme est 36 073 185 FCFA dans les deux cas : le format n'a
rien ajouté ni retiré. Phrase attendue : « montants en francs CFA, stockés en nombres entiers, aucune décimale — les
totaux sont calculés sur les valeurs stockées, pas sur les valeurs affichées ».

**Exercice 2.3.** Format seul : 0 reconnaissance — on ne convertit pas un rendu. Import typé en Date : 424 lignes
ISO passent, les 65 lignes à la française restent en texte, et les bornes 01/01/2025 et 02/12/2025 ne se retrouvent
que sur la partie convertie. Reconstruction par `DATE()` : les 489 passent, avec contrôle croisé — 335 jours
d'amplitude, 31 jours distincts, et un tri du dernier mois qui rend le 02/12/2025 en tête. Seule la troisième voie
est défendable : les deux autres dépendent du poste qui ouvre le fichier.

**Exercice 2.4.** Le collage n'exécute pas la règle : les 8 lignes de retour, quantité jusqu'à −13, passent sans
message, et le collage emporte avec lui la validation de la plage collée (elle est remplacée par celle de la source,
c'est-à-dire souvent rien). La règle qui aurait vu : `=ET(I2>=-500;I2<=500)` en *Personnalisée*, doublée de
`=I2<0` en mise en forme conditionnelle — 8 lignes signalées — et d'un contrôle de décompte rejoué après chaque
import. Fiche : « plage `I2:I490`, règle personnalisée bornée à ±500, motif : 8 retours sur 480 lignes, posée le
… ».

**Exercice 2.5.** Ancrée sur `M5`, la règle juge `M2` avec le contenu de `M5`, `M3` avec `M6`, et ainsi de suite :
le décompte diffère du vrai de trois lignes, dans un sens qui dépend du hasard des conversions, et les trois
dernières lignes sont jugées sur du vide. L'ancre correcte est `M2` ; dans *Gérer les règles*, la détection passe en
tête avec *Arrêter si vrai*, et la portée se limite à `M2:M490`.

## 13. Mini-projet M03.P1 — suite : le volet formats et garde-fous (40 min)

**Commande.** Reprenez la fiche de prise en main du chapitre C01 et complétez-la par le volet formats, en une page,
pour que le classeur se suffise à lui-même sans explication orale.

**Livrables numérotés.** (1) le tableau des formats du classeur — colonne, format exact, motif ; (2) la preuve
chiffrée de la conversion en trois temps : avant (0 · 0 FCFA), après conversion (489 · 36 339 317 FCFA), après
dédoublonnage (480 · 36 073 185 FCFA) ; (3) les règles de validation, leur message, et la ligne de fiche qui les
justifie ; (4) les trois règles de mise en forme conditionnelle — formule, portée, ordre — et le décompte de
cellules allumées avant conversion (489) et après (0).

**Barème (20 points, seuil 13).** Tableau des formats complet et exact (5) · preuve de conversion en trois temps,
dans l'ordre (4) · validation bornée des deux côtés avec message utile (4) · règles de détection : ancrage, portée,
ordre, décomptes (4) · style : une page, aucun format posé cellule à cellule (3).

## 14. Résumé du chapitre

Le tableur classe avant d'afficher : ce qu'il a lu décide de tout, et le réglage régional décide de ce qu'il lit. Les
formats — monétaire, négatif en rouge, pourcentage à une décimale, date courte — sont des couches de rendu ; ils
rendent lisible, jamais juste. Convertir est un autre acte : collage spécial avec opération, colonne utilitaire avec
`CNUM(SUBSTITUE(…))`, ou types forcés à l'import ; la preuve tient dans un compteur qui passe de 0 à 480 et une
somme qui revient à 36 073 185 FCFA, après une conversion **et** un retrait des 9 doublons, deux opérations
distinctes.

Le classeur se protège en trois couches : la validation refuse la saisie impossible, la mise en forme conditionnelle
signale ce qui est déjà là, la colonne de statut écrit le mot qu'une couleur ne peut pas dire. Les dates sont le cas
d'école : un compteur de jours, deux écritures dans le fichier reçu (424 et 65), 335 jours d'amplitude, 31 jours
d'activité, et une conversion explicite qui affranchit du poste de celui qui ouvrira le fichier.

## 15. À retenir

> **À retenir.** Un format ne convertit pas. La preuve d'une conversion n'est pas la colonne qui brille en FCFA,
> c'est *Nombre de valeurs numériques* qui passe de 0 à 480.

> **À retenir.** La validation garde la frappe, pas le collage ni l'import. Sur un fichier qui entre tous les jours,
> la protection utile est une règle de détection relue après chaque import, et un mot écrit dans une colonne de
> statut.

> **À retenir.** Une règle de mise en forme conditionnelle s'ancre sur la première cellule de sa plage : une
> référence décalée de trois lignes produit un décompte faux de trois unités et des couleurs plausibles.

1. La devise est dans le format, jamais dans la cellule ; les négatifs sont en rouge ; les taux à une décimale, pour
   que `1 100,0 %` crie de lui-même.
2. Une date est un nombre de jours : le test du *Nombre général* est le seul qui dise ce que la cellule stocke.
3. Convertir dans une colonne utilitaire, remplacer, garder la trace : on ne corrige pas la preuve.
4. Trois règles de détection maximum, *Arrêter si vrai*, chacune adossée à une ligne de la fiche.
5. Les 4 FCFA d'écart entre montants enregistrés et recalculés ne sont pas une faute : c'est l'arrondi de six lignes
   à un demi-franc. Dites votre règle, on ne la cherchera pas.

## 16. Évaluation formative (auto-correction, 8 min)

1. Un montant affiché `36 073 185 FCFA` peut-il être du texte ? Comment le savoir en trois secondes ?
2. Citez les trois voies de conversion et, pour chacune, ce qu'elle fait des valeurs illisibles.
3. La colonne `remise` est écrite `0.03` dans le fichier reçu. Que lit un tableur français, que lit un tableur
   anglais, et quelle borne attendez-vous après conversion sur la donnée nettoyée ?
4. Vous posez « entier de 1 à 500 » sur `quantite` : quelles lignes de la donnée nettoyée cette règle aurait-elle
   fait disparaître, et pour quel montant ?
5. Une règle `=NON(ESTNUM(M2))` est créée avec `M5` comme cellule active sur `M2:M490`. Que voit-on, et pourquoi
   est-ce pire que l'absence de règle ?

**Question ouverte.** Un collègue écrit : « j'ai mis un format, puis une validation, donc le classeur est propre ».
Répondez en nommant ce que son dispositif ne voit pas, et la couche qui le voit.

---

**Corrigé de l'évaluation formative.**

1. Oui : le format n'agit que sur le rendu. Trois secondes, deux gestes — l'alignement (gauche : texte) et
   *Nombre de valeurs numériques* sur la colonne (0 : tout est texte, même orné de FCFA).
2. Collage spécial avec opération : rapide, transforme l'illisible en erreur ou en valeur fausse, sans trace
   conservée ; colonne utilitaire avec `CNUM` : garde la valeur d'origine et rend les échecs lisibles en `#VALEUR!` ;
   types forcés à l'import : la seule voie qui répare aussi les dates, parce qu'elle décide avant le classement.
3. En français, du texte — le point n'est pas le séparateur décimal ; en anglais, le nombre 0,03. Après conversion,
   la borne attendue est 0,11, soit 11,0 % au format pourcentage : au-delà, on est hors politique commerciale.
4. Les 8 lignes de retour, quantité jusqu'à −13, pour −283 933 FCFA. Les exclure affiche 36 357 118 FCFA — le total
   des seules lignes positives — au lieu de 36 073 185 FCFA : un chiffre surévalué de 0,8 %, impossible à défendre
   une fois les retours retrouvés.
5. La règle juge la ligne 2 sur la ligne 5, la ligne 3 sur la ligne 6 : le décompte est faux de trois unités, dans
   un sens imprévisible, et les couleurs restent plausibles. C'est pire qu'une absence de règle, parce qu'une absence
   ne fait pas semblant d'être juste.
   *Question ouverte* — Réponse attendue : « le format ne voit rien, la validation ne voit que la frappe : ni le
   collage par-dessus la plage, ni les 486 textes entrés par l'import. Ce que le dispositif ne voit pas, la détection
   par formule le voit — `ESTNUM`, une colonne de statut, et un contrôle de compteur rejoué après chaque import ».

---

**Suite du module.** Le chapitre C03 quitte l'habillage pour la structure : la table structurée, qui fait grandir la
donnée avec son format et sa validation ; le tri honnête, avec extension de la sélection ; les filtres ; et la
suppression des doublons — les 9 lignes retirées à la main tout à l'heure, proprement cette fois.
