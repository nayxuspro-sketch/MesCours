# Évaluation M09 — « Analyse exploratoire de données »

**Module M09 · durée totale 3 h 05 · cinq épreuves · seuils : quiz 11/15, exercices 11/15, étude de cas 12/20, projet 13/20**

| Épreuve | Durée | Barème | Noté | Ce qui est attendu |
|---|---|---|---|---|
| A · Questions de récupération | 10 min | non noté | non | vérifier qu'on a lu les six chapitres avant de se tromper cher |
| B · Quiz | 25 min | /15 | oui | quinze questions à réponse unique, cinq blocs, dont **5 « prédisez la sortie »** |
| C · Exercices « prédisez la sortie » | 30 min | /15 (auto-corrigé) | oui | quinze valeurs mesurées sur le socle, auto-validées par `tools/controle_exos_M09.py` |
| D · Exercices à rendre | 40 min | /20 | oui | cinq exercices courts (5 × /2) + « cette conclusion déborde » (/10) |
| E · Étude de cas — « les 5 questions du directeur » | 60 min | /20, seuil 12 | oui | **poser** les 5 questions les plus pertinentes, puis y répondre — la qualité de la question passe avant la réponse |

> Le score du module se lit ainsi : **B ≥ 11** et **C ≥ 11** et **E ≥ 12** valident le
> module ; le projet M09.P doit atteindre 13/20. L'épreuve E est **délibérément
> inversée** par rapport à M07/M08 : une **bonne question mal répondue** vaut plus
> qu'une mauvaise question bien répondue. Savoir exécuter un `groupby` ne dispense pas
> de savoir **quelle** question poser au fichier. Tout nombre de cette évaluation est
> mesuré sur le socle livré (`03_exercices/dossier_M09/`, quatre jeux, graine 45,
> empreinte dossier `b9a8d973119342ec…`) ; les corrections le citent avec leur clé
> `m09p_*` / `m09v_*` dans `chiffres_cites.json`.

---

## A · Questions de récupération (non notées)

À traiter sans document, en une ou deux phrases chacune. Elles ne sont pas comptées ;
elles servent à repérer ce qui n'est pas assimilé avant de perdre des points sur un
détail.

1. Citez les **10 étapes** du protocole EDA (C01) et dites pourquoi une étape peut être
   **vide** mais jamais **sautée**.
2. Pourquoi `head(5)` peut-il **mentir** (C01) ? Que regarde-t-on à la place pour
   décider si un fichier est propre ?
3. Quelles sont les **3 familles de défauts** de l'audit (C02), et pourquoi l'**audit
   vide** est-il suspect plutôt que réconfortant ?
4. Que sépare une **tendance** d'une **saisonnalité** (C03) ? Comment mesure-t-on qu'un
   cycle est **structurel** et non du bruit ?
5. Nommez les **3 témoins** de la preuve d'une anomalie (C04), et dites ce qu'on fait
   d'un **soupçon** qu'on ne peut pas prouver.
6. Pourquoi une corrélation ne suffit-elle **jamais** à conclure une cause (C05) ?
   Nommez les **3 fausses causes** du chapitre.
7. Quels sont les **4 chiffres** qui accompagnent un coefficient de corrélation publié
   (C05) ?
8. Quelles sont les **5 erreurs d'exploration** d'un graphique (C06), et le contrôle de
   chacune ? Que porte la **note d'EDA** (C06) ?

---

## B · Quiz (15 questions · 15 points)

**Barème : 1 point par question, une seule bonne réponse. Les réponses justifiées en une
ligne rapportent un demi-point de bonus, plafonné à 15.**

### Bloc 1 — Le protocole et l'audit (C01–C02) (Q1 à Q3)

**Q1.** Une étape du protocole qui ne trouve rien : a) se saute · b) **se déclare vide,
avec les contrôles faits pour l'affirmer** · c) se remplace par une autre · d) se
marque « à faire plus tard ».

**Q2.** Sur `consultation.csv`, la colonne `motif` compte 23 valeurs vides : c'est un
défaut de la famille : a) **manquants** · b) doublons · c) impossibles · d) aucun — un
motif peut être vide dans la réalité.

**Q3.** Les 4 stocks négatifs du socle (jusqu'à -12) relèvent de la famille
« impossible » parce que : a) leur valeur est rare · b) **la borne métier dit qu'un
stock ne peut pas être négatif** · c) ils sont au-delà de l'intervalle interquartile ·
d) ils sont négatifs donc faux.

### Bloc 2 — Tendances et périodes comparables (C03) (Q4 à Q6)

**Q4. (prédisez la sortie)** Le socle du centre de santé s'arrête au 2026-12-28 ;
décembre 2026 compte 28 jours pour 31 en décembre 2025. La comparaison des **totaux**
mensuels : a) prouve une baisse de 8 % · b) **n'est pas comparable — comparer à mois
égal ou au flux par jour** · c) prouve une hausse · d) est valable, décembre est
toujours incomplet.

**Q5.** Pour juger qu'une saison est structurelle, on compare : a) la moyenne de l'été à
celle de l'hiver · b) **l'amplitude ENTRE positions à la variabilité DANS chaque
position** · c) le maximum au minimum · d) la médiane à la moyenne.

**Q6.** Sur le fil rouge, la moyenne glissante 3 mois du CA mensuel : a) suit la série
de près · b) **reste dans une bande étroite — le CA est plat** · c) montre une forte
croissance · d) n'existe pas, faute de 36 mois de recul.

### Bloc 3 — Anomalies et preuves (C04) (Q7 à Q9)

**Q7.** Un montant à 594 363 FCFA, répété 6 fois, se **garde** parce que : a) il est rare
· b) **c'est un plafond exact (10 × 49 946.47 × 1.19) — une rareté légitime** · c) il est
inférieur à la borne de Tukey · d) il est rond.

**Q8.** Une **rupture de stock** de 3 jours se traite : a) comme un défaut à corriger ·
b) comme un manquant à combler · c) **comme un signal métier à conserver et à dater** ·
d) comme un doublon.

**Q9.** Une anomalie qu'aucun des 3 témoins ne confirme : a) est exclue du fichier ·
b) est corrigée par la moyenne · c) **reste un soupçon : signalé, non traité** · d) est
publiée comme un fait.

### Bloc 4 — Relations, segments, groupes (C05) (Q10 à Q12)

**Q10. (prédisez la sortie)** La corrélation entre montant et taux de remise vaut
**0.001**, celle entre montant et remise **en FCFA** vaut **0.552**. La bonne lecture
est : a) les grosses ventes ont de grosses remises · b) **le 0.552 est un effet de
scale (montant en FCFA), le taux ne montre aucun lien** · c) les deux disent la même
chose · d) la remise cause le montant.

**Q11. (prédisez la sortie)** Sur le panier moyen par mode de paiement, l'écart entre le
minimum (156 150 FCFA) et le maximum (159 959 FCFA) vaut **2.4 %**, pour des groupes de
**2 552 à 20 175** ventes. On conclut : a) le mode 1 est le meilleur · b) **les modes ne
différencient pas le panier : l'écart est du bruit de taille** · c) il faut exclure les
petits groupes · d) l'écart est significatif.

**Q12.** Pour contrôler la variable tierce dans la relation absentéisme × résultats, on :
a) retire les élèves extrêmes · b) **recalcule la corrélation par bande de niveau
initial** · c) calcule une moyenne mobile · d) change de méthode de corrélation.

### Bloc 5 — Graphiques et note d'EDA (C06) (Q13 à Q15)

**Q13. (prédisez la sortie)** La courbe du CA est tracée sur un axe de **310 à 350 M**
FCFA. C'est : a) une faute, un axe part toujours de zéro · b) **licite si l'axe est
déclaré (données de niveau) — fautif s'il est silencieux** · c) une fraude · d) une
échelle logarithmique.

**Q14. (prédisez la sortie)** Le nuage montant × taux de remise porte `n = 50 008` dans
son titre et une transparence 0.25. Ces deux mentions servent à : a) décorer ·
b) **empêcher l'échantillon fantôme et la dissimulation de points** · c) accélérer le
rendu · d) remplacer la légende.

**Q15.** Une affirmation de la note d'EDA sans **limite** : a) est acceptable si le
chiffre est juste · b) **déborde de ce que les données disent : on la recule ou on la
retire** · c) se complète par « sous réserve » · d) est notée au bonus.

---

## C · Exercices « prédisez la sortie » (15 valeurs · 15 points · auto-corrigé)

**Consigne.** Pour chaque bloc, écrivez la valeur que vous **prédisez** avant
d'exécuter, puis exécutez et comparez. Une valeur juste = 1 point ; une valeur fausse
**corrigée par l'exécution** = un demi-point (le but est le réflexe, pas le score).
L'auto-correction est donnée par `tools/controle_exos_M09.py` (quinze valeurs mesurées,
jamais déduites).

| # | Le bloc (à exécuter sur `dossier_M09/`) | Ce que vous prédisez |
|---|---|---|
| E01 | `len(pd.read_csv("quincaillerie/vente.csv"))` | le nombre de lignes de ventes |
| E02 | lignes après dédoublonnage sur les 12 colonnes métier | ventes distinctes |
| E03 | `sum(montant_ttc)` en centimes entiers, retours exclus, divisé une fois | le CA propre (FCFA) |
| E04 | `len(consultation.csv)` filtré sur 2025-07-01 → 2026-06-30 | les lignes du variant 12 mois |
| E05 | moyenne de consultations **par jour** sur ce variant | la fréquentation quotidienne |
| E06 | `max` des totaux mensuels de ce variant | le pic mensuel (consultations) |
| E07 | écart entre le pic et le creux mensuels du variant | l'amplitude mois |
| E08 | moyenne des mois d'été (juillet-septembre) du variant | la fréquentation d'été |
| E09 | écart-type des mois d'été du variant | la variabilité intra-été |
| E10 | consultations du lundi sur le variant | le jour le plus chargé |
| E11 | consultations du dimanche sur le variant | le jour le plus creux |
| E12 | `note.csv` filtré sur les notes hors bornes (0 à 20) | les notes impossibles |
| E13 | corrélation entre absences totales et moyenne des notes | le coefficient |
| E14 | `fichier_inconnu.csv` : doublons sur `tx_ref` | les transactions en double |
| E15 | succès normalisés du fichier projet, après dédoublonnage | le taux de succès (%) |

---

## D · Exercices à rendre (20 points)

**D1 (2 pts).** Écrire les **3 questions** que le fichier `fichier_inconnu.csv` **peut**
répondre, et **2** qu'il **ne peut pas** répondre — en justifiant chaque refus par la
variable manquante ou la période trop courte.

**D2 (2 pts).** Sur `consultation.csv`, écrire le contrôle qui prouve que la
moyenne/jour (**25.74**) et la médiane/jour (**29.0**) ne racontent pas la même chose —
et dire **laquelle** des deux on publie pour un pic de fréquentation, et pourquoi.

**D3 (2 pts).** Écrire la définition **exacte** (en une phrase) des deux défauts de
`stock_medicament.csv`, puis la commande qui les compte : **7 doublons** de 5-tuple et
**4 stocks négatifs**.

**D4 (2 pts).** Le fichier scolaire porte **6 notes hors bornes** (2 × 22.5, 25.0, et
trois négatives : -1.5, -0.5, -3.0) : écrire la décision **argumentée** (garder,
corriger ou exclure) **et** la ligne de rapport qui la justifie.

**D5 (2 pts).** Écrire la phrase qui publie le **taux de réussite** du jeu scolaire
(**58.7 %**) **avec ses 4 chiffres** : valeur, n, contrôle, limite.

**D6 (10 pts) — « cette conclusion déborde ».** On vous donne quatre conclusions
publiées. Pour chacune : dites **ce qui déborde** (1 pt), **la limite manquante**
(1 pt) et **la phrase réécrite** (0.5 pt) :

1. « Les remises **causent** la baisse du CA : la corrélation est de 0.552. »
2. « Le centre de santé est **saturé** : la fréquentation d'été est de 853
   consultations/mois. »
3. « Les élèves qui s'absentent ont 1.37 point de moins : **l'absentéisme fait
   baisser les notes**. »
4. « Le mode de paiement 3 est le **favori** des clients : son panier moyen est le plus
   élevé des cinq. »

---

## E · Étude de cas — « les 5 questions du directeur » (20 points · seuil 12)

**Situation.** Le directeur du centre de santé vous remet **un an de consultations,
12 mois glissants** (2025-07-01 → 2026-06-30) — un **variant** que vous n'avez pas
traité dans les chapitres, extrait de `sante/consultation.csv` par un simple filtre de
dates. Il ne vous donne **aucune question** : c'est vous qui les posez.

**Consigne (délibérément inversée).**

1. **Écrivez d'abord les 5 questions** les plus pertinentes **pour lui** (12 pts —
   2.4 pts par question). Chaque question est notée sur : sa **pertinence métier**
   (elle intéresse la direction), sa **formulation falsifiable** (on peut y répondre
   par un chiffre, et une réponse fausse est imaginable), et le fait qu'elle soit
   **répondable par CE fichier** (variables et période disponibles).
2. **Répondez ensuite à vos 5 questions** (8 pts) : un chiffre par question, **avec sa
   source** (la sortie exécutée) — et pour **deux** d'entre elles, la **limite**.
3. **Le contrôle final** : une question que le fichier **ne peut pas** répondre, écrite
   avec la raison (elle rapporte 1 point si les 5 questions en cours n'ont pas déjà
   épuisé le barème).

---

## Correction détaillée

### A · Réponses de récupération

1. Les 10 étapes : inspecter, comprendre les variables, détecter les problèmes,
   premières statistiques, tendances, anomalies, relations, hypothèses, visualisations,
   conclusions provisoires. Une étape **vide** est déclarée avec ses contrôles ; une
   étape **sautée** est un défaut du rapport (C01 §5.2).
2. `head(5)` montre les premières lignes : les défauts (doublons, négatifs, dates
   futures) peuvent être **ailleurs** ; on regarde `shape`, `dtypes`, `isna().sum()` et
   les bornes métier.
3. Doublons, manquants, impossibles. L'audit vide est **suspect** parce qu'un audit
   réel produit des contrôles : on vérifie le contrôle du contrôle (C02 §5.2).
4. La tendance est le **lit** (moyenne glissante), la saisonnalité est la variation
   **régulière et prévisible** ; un cycle est structurel quand l'amplitude **entre**
   positions domine la variabilité **dans** chaque position (C03 §5.2).
5. Position (iqr, Tukey), récurrence (hier + entrées - sorties), métier (bornes). Un
   soupçon se **signale** (« au-delà de la borne, non exploré ») et ne se traite pas
   (C04 §5.2).
6. Parce qu'une association n'est pas une cause ; les trois fausses causes sont la
   **variable tierce**, la **régression vers la moyenne** et le **sens inversé**
   (C05 §5.2).
7. Valeur, n, contrôle, limite — les quatre ensemble (C05 §5.1).
8. Axe non zéro silencieux, graphique sans question, couleur sans légende, échelle log
   non annoncée, nuage sans n. La note d'EDA porte, par affirmation, sa **source** et sa
   **limite** (C06 §5.2 et §5.5).

### B · Corrigé du quiz (1 pt par question)

| # | Rép. | La justification attendue |
|---|---|---|
| Q1 | b | une étape se **déclare** vide avec ses contrôles ; le silence est le défaut que le correcteur cherche |
| Q2 | a | 23 motifs vides sur 18 818 consultations = famille « manquants » (`m09p_s_motifs_manquants`) |
| Q3 | b | le négatif n'est pas « rare », il est **impossible** : la borne métier (stock >= 0) le dit seule |
| Q4 | b | décembre 2026 est partiel (28 jours) : comparer à mois égal ou au flux par jour |
| Q5 | b | amplitude entre positions (198) contre variabilité intra-position (48) : la saison est structurelle |
| Q6 | b | la moyenne glissante 3 mois reste dans une bande étroite : plat, +1.6 % à mois égal |
| Q7 | b | 10 × 49 946.47 × 1.19 = 594 363 : c'est le **plafond**, une rareté légitime (`m09p_q_montant_max`) |
| Q8 | c | une rupture est un **fait métier** (offre coupée) : on la garde et on la date, on ne la corrige pas |
| Q9 | c | sans les 3 témoins, c'est un **soupçon** : signalé, non traité (C04 §5.3) |
| Q10 | b | le 0.552 vient du **scale** (montant en FCFA) ; en taux, la corrélation est 0.001 |
| Q11 | b | 2.4 % d'écart pour des groupes de rapport 8 : bruit de taille, les n sont dans le graphique |
| Q12 | b | on recalcule **par bande** de niveau initial (confond) : −0.145 / −0.085 / +0.163 |
| Q13 | b | sur des **niveaux**, l'axe non zéro est licite **s'il est déclaré** ; silencieux, il dramatise |
| Q14 | b | sans le n, 50 008 points ou 200 se ressemblent ; la transparence qui masque doit être dite |
| Q15 | b | une limite vide = une affirmation qui **déborde** : on la recule ou on la retire |

### C · Corrigé des quinze valeurs

Les valeurs attendues sont **mesurées** (elles ne sont pas déduites des chapitres) ;
`tools/controle_exos_M09.py` les recalcule depuis le dossier livré et affiche, pour
chacune, la valeur obtenue et le verdict. Les ordres de grandeur de référence : les
ventes du fil rouge sont ~50 000 lignes (8 doublons → ~50 000 distinctes), le variant
santé fait **9 450 lignes sur 365 jours** (moyenne 25.89/jour) avec un **pic mensuel de
882** consultations (2025-07) et un **creux de 678** (2026-02), une moyenne d'été de
**857.3** contre **770.7** en hiver pour un écart-type intra-été de **24.03**, le lundi
à **1 899** consultations contre **201** le dimanche ; le fichier projet porte **14**
doublons de `tx_ref` et un taux de succès de **81.15 %** après normalisation. Chaque
valeur est vérifiée par le contrôleur, clé `m09v_*` ou `m09p_*` à l'appui.

### D · Corrigé des exercices à rendre

**D1.** Répondables (exemples) : volume et nombre de transactions par mois ; taux de
succès par canal ; répartition in/out. Non répondables : la **cause des échecs** (aucune
colonne de motif), la **localisation** (pas de zone ni de point de vente) — deux refus
justifiés par une variable absente, pas par une opinion.

**D2.** `cons.groupby("date_consultation").size()` puis `mean()` (25.74) contre
`median()` (29.0) : la moyenne est **tirée vers le bas** par les jours creux (dimanches
à 201 consultations sur un an), la médiane décrit **un jour ordinaire**. Pour un pic de
fréquentation, on publie la **médiane** des jours comme référence d'activité et le
**maximum** comme dimensionnement (`m09p_s_moyenne_jour`, `m09p_s_mediane_jour`).

**D3.** Doublon de stock : « même médicament, même date, même mouvement, mêmes
entrées/sorties et même stock de fin — la ligne est répétée » →
`stk.duplicated().sum()` = **7** ; stock négatif : « stock de fin inférieur à zéro, ce
qu'aucun inventaire réel ne produit » → `(stk["stock_fin"] < 0).sum()` = **4**
(`m09p_s_doublons_stock`, `m09p_s_stocks_negatifs`).

**D4.** Décision : **exclure les six notes du calcul** (elles ne sont pas « très bonnes »
ou « très faibles », elles sont **impossibles** : une note sur 20 ne vaut ni 22.5 ni
-1.5), **sans** corriger par la moyenne (on inventerait une valeur) et **en le
déclarant** : « 6 notes hors bornes (0 à 20) exclues du calcul des moyennes ; elles
sont signalées à la source pour correction » (`m09p_sc_notes_hors_bornes`).

**D5.** « Le taux de réussite est de **58.7 %** (n = 400 élèves distincts, notes
recalculées après exclusion des 6 notes hors bornes et rattachement des doublons
d'élèves), à lire comme une **photographie d'une session** : aucun contrôle sur la
difficulté des épreuves ni sur les élèves sortis en cours d'année »
(`m09p_sc_taux_reussite`).

**D6 — « cette conclusion déborde » :**

1. *Déborde* : la causalité (« causent ») et l'usage du coefficient en FCFA. *Limite
   manquante* : le scale (0.001 en taux) et l'absence de lien démontré. *Réécriture* :
   « la remise **en FCFA** est corrélée au montant (0.552) mais le **taux** de remise ne
   l'est pas (0.001) : aucune relation entre politique de remise et taille du panier. »
2. *Déborde* : « saturé » est une **conclusion d'organisation** (personnel, lits,
   médicaments) que la fréquentation seule ne prouve pas. *Limite manquante* : la
   saturation dépend de la capacité, variable absente du fichier. *Réécriture* : « la
   fréquentation est **saisonnière** (été 853 contre 655 en hiver) ; la saturation ne
   peut pas être conclue : le fichier ne porte pas la capacité du centre. »
3. *Déborde* : le sens (« fait baisser ») et la tierce variable. *Limite manquante* : le
   contrôle par bande montre que le lien se **réduit** (−0.145 / −0.085 / +0.163) et le
   sens n'est pas départagé. *Réécriture* : « l'absentéisme et les résultats sont
   **associés** (−0.232) ; une part du lien vient du niveau initial, le sens reste
   indéterminé — association, pas causalité. »
4. *Déborde* : « favori » est un **choix des clients** que 2.4 % d'écart ne démontrent
   pas. *Limite manquante* : l'écart pour des groupes de 2 552 à 20 175 ventes (bruit de
   taille) et la part des **retours** dans le mode. *Réécriture* : « les cinq modes ont
   des paniers moyens **statistiquement indiscernables** (156 150 à 159 959 FCFA pour
   2.4 % d'écart) : aucun mode n'est « favori » en valeur de panier. »

### E · Corrigé de l'étude de cas — les 5 questions attendues

**Les 5 questions les plus pertinentes** (2.4 pts chacune ; le jury accepte toute
question de même niveau, la liste suivante est la référence) :

1. **« Y a-t-il une saison, et de quelle ampleur ? »** — moyennes d'été (857.3
   consultations/mois) contre hiver (770.7), pour un écart-type interne d'été de 24.03 :
   la saison est **structurelle** (l'écart entre positions domine la variabilité
   interne). *Réponse chiffrée :* 857.3 contre 770.7 (`m09v_ete`, `m09v_hiver`) ;
   *limite :* 12 mois seulement, deux étés partiels, la cause (pluies, épidémie) est
   hors fichier.
2. **« Quel est le mois de pointe, et de combien dépasse-t-il le creux ? »** — pic
   2025-07 à 882 consultations, creux 2026-02 à 678, soit **204** consultations d'écart
   (`m09v_pic_mois`, `m09v_creux_mois`, `m09v_chute_max`). C'est la question du
   **dimensionnement** : le stock et les effectifs se calent sur le pic, pas sur la
   moyenne.
3. **« Quels jours de la semaine portent la charge ? »** — lundi **1 899**
   consultations contre dimanche **201** sur 365 jours (`m09v_lundi`,
   `m09v_dimanche`) : le planning du personnel se déduit de cette question, pas de la
   moyenne (25.89/jour).
4. **« La fréquentation quotidienne est-elle homogène ou faite de journées extrêmes ? »**
   — la moyenne/jour (25.89) et la médiane/jour (29.0) ne disent pas la même chose :
   publier les deux, plus le maximum, sous peine de sous-dimensionner les pointes.
   *Limite :* le fichier ne porte pas les **fermetures** du centre (elles
   apparaîtraient comme des jours creux).
5. **« La rupture de stock de juillet tombe-t-elle au pic de fréquentation ? »** — oui
   pour M01 (3 jours, 2025-07-14 → 16), non pour M02 (5 jours en mars) : la seule
   rupture **qui compte** opérationnellement est celle qui coïncide avec le pic
   (`m09p_s_rupture_m01`, `m09p_s_rupture_la_plus_longue`).

**La question que le fichier ne peut PAS répondre** : « **pourquoi** les patients
viennent-ils plus l'été ? » — le fichier porte la fréquentation, le motif (`paludisme`
en tête : 2 417 lignes) et l'âge, mais **aucune** variable environnementale (pluies,
températures, épidémie) ni de population de référence : la cause est **hors fichier**
(1 pt si le barème des 5 questions n'est pas épuisé).

> **Comment l'épreuve E est notée, en une phrase.** Une **bonne question mal répondue**
> vaut plus qu'une mauvaise question bien répondue : une question de dimensionnement
> (pic, charge hebdomadaire, rupture au pic) qui reçoit un chiffre approximatif mais
> **sourcé** rapporte plus qu'une question décorative parfaitement calculée — c'est
> l'inverse de M07/M08, délibérément, parce que la compétence du module est de **savoir
> ce qu'on demande** aux données avant de savoir le calculer.
