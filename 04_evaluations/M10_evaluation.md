# Évaluation M10 — « Data visualization »

**Module M10 · 30 h · niveau N3 · 7 chapitres.**
**Total : 65 points** — quiz **15** (seuil 14/20 §B.6, soit 10,5/15), « prédisez la mesure »
**10**, exercices à rendre **20**, étude de cas **20** (seuil **12**). Durée conseillée : 1 h 30
pour le quiz et les prédictions, 2 h pour les exercices, 1 h 30 pour l'étude de cas.
**Matériel autorisé** : `01_socle_donnees/`, `03_exercices/dossier_M10/`,
`01_socle_donnees/data/reference/chiffres_cites.json` (clés `m10_*`, `m10p_*`, `m10e_*`) et le
script `tools/controle_refonte_M10.py`. **Toute réponse chiffrée doit être mesurable** : un chiffre
qui ne se retrouve pas dans le socle ne rapporte pas de point.

> **Ce que cette évaluation vérifie.** Que vous savez **relire** une figure : nommer son défaut,
> le **mesurer**, prévoir la conclusion fausse qu'un lecteur en tirerait, et produire la version
> qui rend cette conclusion impossible. Les questions ne demandent pas de dessiner : elles
> demandent de **dire de combien** — c'est la compétence du module.

---

## A · Questions de récupération (non notées)

Répondez de mémoire, en une ligne chacune. Elles ne rapportent rien : elles disent ce qu'il faut
relire.

1. Quel est l'**ordre perceptuel** des encodages, du plus précis au moins précis ?
2. Que signifie **« une couleur, un rôle »** ?
3. Quelle est la différence entre une **erreur** et une **décision** (C05) ?
4. Combien de parts un camembert peut-il porter avant de devenir illisible, selon le module ?
5. Quels sont les trois écrans d'une séquence (C06), dans l'ordre ?
6. Quels outils du module sont **exécutés**, et lequel est **cité** (C07) ?

## B · Quiz (15 questions · 15 points)

**Barème : 1 point par question, une seule bonne réponse.** Les cinq questions marquées
**« prédisez l'effet »** (Q3, Q6, Q9, Q12, Q15) demandent **la conclusion fausse qu'un lecteur
tirerait de la figure** — la réponse doit être la phrase du lecteur, pas le nom du défaut.

### Bloc 1 — La perception et le choix du graphique (C01—C02) (Q1 à Q3)

**Q1.** L'ordre perceptuel du module, du plus précis au moins précis, est :
a) position > longueur > angle > surface > couleur · b) couleur > surface > position > longueur ·
c) longueur > position > couleur > angle · d) tous les encodages se valent si la couleur est
choisie correctement.

**Q2.** Un demandeur veut **classer 8 catégories**. Le graphique adapté est :
a) un camembert à 8 parts · b) **des barres triées** · c) une carte de chaleur · d) un treemap.

**Q3 — prédisez l'effet.** Un rapport présente un camembert de **8** parts dont deux voisines sont
séparées de **0,05** point. La phrase que la direction prononcera est :
a) « les parts sont égales, il n'y a pas de hiérarchie » · b) **« voici le classement des
catégories : la seconde est devant la troisième »** — alors que 0,17° ne se distinguent pas ·
c) « il manque des données » · d) « le graphique est faux ».

### Bloc 2 — Couleurs, contraste, accessibilité (C03) (Q4 à Q6)

**Q4.** Le contraste minimal du module pour un élément de graphique (barre, ligne) contre le fond
blanc est :
a) **3,0** · b) 1,5 · c) 4,5 · d) cela dépend du nombre de séries.

**Q5.** Environ quelle proportion d'hommes présente une vision des couleurs atypique (le chiffre
du module, qui justifie la redondance couleur + forme + libellé) ?
a) 0,5 % · b) **8 %** · c) 25 % · d) 50 %.

**Q6 — prédisez l'effet.** Sur le fil rouge, la paire de couleurs VERT-ROUGE passe de **73,4** à
**35,7** de différence perçue en vision deutéranope (une différence confortable à
l'œil typique). Le lecteur deutéranope, lui, conclura :
a) **« les deux séries sont la même »** · b) « les deux séries sont opposées » ·
c) « il manque une légende » · d) rien : les couleurs ne changent pas la lecture.

### Bloc 3 — Écrire un graphique (C04) (Q7 à Q9)

**Q7.** Un titre qui **affirme** est un titre qui :
a) nomme le fichier source · b) **porte une mesure** (un chiffre, un écart, une période) ·
c) décrit le graphique (« évolution du CA ») · d) tient en trois mots.

**Q8.** Sur le fil rouge, la longueur moyenne des titres passe de **38,4** à **113,2** caractères
entre la version « avant » et la version corrigée. Ce qui compte dans cette évolution, c'est :
a) la longueur elle-même · b) **le passage du libellé à l'affirmation** — la longueur n'est qu'une
conséquence · c) la lisibilité de la police · d) le nombre de mots.

**Q9 — prédisez l'effet.** Une courbe du CA est tracée sur un axe 300-350 M (**82,4 %** de hauteur
occupée) pour une variation réelle de **5,4 %**. La phrase fausse probable est :
a) **« l'activité est très volatile, elle décroche en fin de période »** · b) « le CA est stable » ·
c) « l'axe n'est pas à zéro » · d) « il manque les retours ».

### Bloc 4 — Les 10 erreurs (C05) (Q10 à Q12)

**Q10.** Sur un cumul à 100 %, ce qui est masqué est :
a) la composition · b) **le total de chaque période** · c) l'ordre des séries · d) rien : le cumul
à 100 % est une convention neutre.

**Q11.** Laquelle de ces erreurs **aucune déclaration ne rend acceptable** ?
a) un axe tronqué · b) une échelle logarithmique · c) **un effet 3D** · d) un camembert à 3 parts.

**Q12 — prédisez l'effet.** Un histogramme en échelle logarithmique **non annoncée** : la masse des
petits montants (**77,0 %** des ventes) occupe **93,5 %** de la largeur, la queue (**1 044**
ventes) **1,3 %**. La conclusion fausse du lecteur est :
a) **« les ventes sont homogènes, la queue est marginale »** · b) « les ventes sont très
concentrées » · c) « il y a un problème de données » · d) « le graphique est en log ».

### Bloc 5 — La séquence et les outils (C06—C07) (Q13 à Q15)

**Q13.** Les trois écrans d'une séquence sont, dans l'ordre :
a) décision, mécanisme, niveau · b) **niveau, mécanisme, décision** · c) mécanisme, niveau,
décision · d) niveau, décision, mécanisme.

**Q14.** Dans la maquette du chapitre, la séquence de **3** écrans couvre **5** objections sur 5,
quand le rapport en **1** écran de 12 chiffres en couvrait :
a) 1 · b) **2** · c) 4 · d) 5.

**Q15 — prédisez l'effet.** Le même graphique exporté en 96 dpi pour un rapport imprimé : les
étiquettes de 6 pt deviennent des taches. La phrase du lecteur, à la réunion de validation, est :
a) **« on ne lit rien, refaites l'export »** — la crédibilité de l'analyse est atteinte par un
fichier · b) « le graphique est faux » · c) « il manque la source » · d) « l'échelle est
logarithmique ».

## C · « Prédisez la mesure » (10 valeurs · 10 points · auto-corrigé)

**Consigne.** Pour chaque bloc de code exécuté sur le fil rouge (quincaillerie, hors retours pour
le CA), écrivez **ce que la console affiche**. Une valeur fausse = 0 ; une valeur juste arrondie
comme demandé = 1 point. Aucun calcul à la main : lancez le code après avoir écrit votre prédiction.

```python
import pandas as pd, numpy as np
v = pd.read_csv("03_exercices/dossier_M09/quincaillerie/vente.csv", parse_dates=["date_vente"])
p = pd.read_csv("03_exercices/dossier_M09/quincaillerie/produit.csv")
net = v[~v["est_retour"]]
ca = net.groupby(net["date_vente"].dt.to_period("M"))["montant_ttc"].sum()
ret = v.groupby(v["date_vente"])["est_retour"].sum()
ret = ret.groupby(ret.index.to_period("M")).sum().reindex(ca.index).fillna(0)
mg3 = ca.rolling(3).mean()
vp = net.merge(p[["id_produit", "id_categorie"]], on="id_produit", how="left")
cat = vp.groupby("id_categorie")["montant_ttc"].sum()
trim = net.groupby(net["date_vente"].dt.to_period("Q"))["montant_ttc"].sum()
parts = (net.assign(trim=net["date_vente"].dt.to_period("Q"))
         .pivot_table(index="trim", columns="id_mode", values="montant_ttc", aggfunc="sum"))
parts = parts.div(parts.sum(axis=1), axis=0) * 100
m = net["montant_ttc"]
```

| # | Prédiction à écrire | La valeur attendue |
|---|---|---|
| 1 | `round((mg3.max()-mg3.min())/mg3.min()*100, 1)` | ? |
| 2 | `round(100*(ca.max()-ca.min())/1e6/350, 1)` | ? |
| 3 | `round(100*(ca.max()-ca.min())/1e6/50, 1)` | ? |
| 4 | `round(float(ca.corr(ret)), 2)` | ? |
| 5 | `round(float(np.diff(np.sort(cat/cat.sum()*100)).min())*3.6, 2)` | ? |
| 6 | `round(100*(trim.max()-trim.min())/trim.min(), 1)` | ? |
| 7 | `round(float((parts.max(axis=0)-parts.min(axis=0)).max()), 1)` | ? |
| 8 | `round(100*(m < 250000).mean(), 1)` puis `round(np.log10(250000)/np.log10(m.max())*100, 1)` | ? et ? |
| 9 | `int((v["montant_ttc"] > 500000).sum())` | ? |
| 10 | inversions d'un tri alphabétique contre le tri par valeur, sur les 8 catégories | ? sur 28 paires |

## D · Exercices à rendre (20 points)

**Trois exercices argumentés.** La consigne du module s'applique : **la justification pèse plus que
le choix**. Chaque réponse suit le même gabarit : (1) la question servie, (2) le graphique choisi et
son encodage, (3) la mesure qui appuie le choix, (4) le piège écarté.

**E1 — « choisir le graphique, justifier par la question » (7 points).** Cinq commandes réelles,
cinq questions. Pour chacune : le graphique, l'encodage dominant (ordre perceptuel, C01), la
mesure du socle qui l'illustre, et le piège.

1. « Où en est le CA, mois par mois, sur deux ans ? »
2. « Quelles catégories pèsent le plus, et de combien ? »
3. « Les gros paniers pèsent-ils lourd dans le CA ? »
4. « Le mix de paiement a-t-il bougé d'un trimestre à l'autre ? »
5. « Où sont les tensions dans la distribution des montants ? »

**E2 — « la palette de notre maison » (6 points).** À partir des mesures de C03 (contrastes WCAG
contre le blanc : bleu 8,66 · rouge 6,74 · vert 5,91 · orange 3,78 · gris 3,05 · jaune 1,43), écrivez
la charte d'une page : la palette (3 à 5 couleurs), le seuil de contraste (**4,5** pour du texte,
**3,0** pour un élément de graphique), la redondance obligatoire (couleur **+** forme **+**
libellé), et la règle de rôle (« une couleur, un rôle »). Rendez la charte **plus** le test : pour
chaque couleur, sa valeur de contraste et l'usage autorisé.

**E3 — « la relecture de 60 secondes » (7 points).** Prenez le rapport de la quincaillerie
(`rapport_avant/rapport_avant.md`) et passez les 6 questions du §5.7 de C05 sur chacune des 5
affirmations. Rendez un tableau : affirmation du rapport · question de la check-list qui l'attrape ·
mesure qui la contredit · verdict (confirmée / à corriger / fausse).

## E · Étude de cas — « ce graphique a déclenché une décision fausse » (20 points · seuil 12)

**Le contexte.** Avril 2026, comité de direction d'une enseigne de quincaillerie (**5** magasins,
**24** mois, **50 008** ventes). À l'ordre du jour : la réorganisation de l'équipe commerciale. Le
service présente **une** courbe : « Évolution du chiffre d'affaires ». La courbe est tracée sur un
axe **300-350 M FCFA**. Elle monte, plonge, remonte. Le service conclut : **« l'activité est très
volatile ; il faut une équipe de renfort et un pilotage hebdomadaire »**. Le comité vote la
réorganisation. **Trois mois plus tard**, le surcoût est de l'ordre de plusieurs dizaines de
millions de FCFA et l'activité n'a pas bougé : le CA net est resté dans une bande étroite.

**Votre travail.** Reconstituer la chaîne complète : **défaut → lecture fausse → décision**, puis
produire la version qui aurait empêché la décision.

1. **Le défaut, mesuré (5 pts).** Nommez-le (C05) et donnez **trois** mesures : la hauteur occupée
   de l'axe (**82,4 %** en version tronquée contre **11,8 %** à zéro), l'amplitude apparente
   (**× 7,0**) et la variation réelle (**5,4 %** sur la moyenne glissante, contre **13,4 %** sur la
   série brute). Conclusion en une phrase : l'écart entre les deux lectures vient de **la
   fenêtre**, pas de la donnée.
2. **La lecture fausse, écrite (4 pts).** Rédigez les **trois** phrases que la courbe donne à lire
   à un lecteur pressé : « la volatilité augmente », « il y a un décrochage », « la croissance est
   portée par le second semestre ». Pour chacune, la **mesure qui la contredit** (les mois, la
   moyenne glissante, le rapport entre les deux années).
3. **La décision, chiffrée (4 pts).** Écrivez la décision telle qu'elle a été prise, puis
   chiffrez ce qu'elle coûte au regard de ce qu'elle visait : quelle variation réelle aurait
   justifié un dispositif de renfort (proposez un seuil et justifiez-le) ?
4. **La version qui l'aurait empêchée (4 pts).** Proposez la figure corrigée : axe à zéro, titre
   qui **affirme** (avec le chiffre), annotation du chiffre clé, et **la déclaration** écrite dans
   la figure. Expliquez en trois lignes pourquoi la décision n'aurait pas été votée.
5. **La généralisation (3 pts).** Le contrôle automatique du module (`tools/controle_refonte_M10.py`)
   aurait-il attrapé cette figure ? Répondez précisément : **quelle couche** (L1 à L4) vérifie quoi,
   et **quelle couche** ne suffit pas ici — un axe tronqué n'est pas un changement de **valeur**.
   Proposez le contrôle supplémentaire qui l'attrape (« comparer la fenêtre de l'axe à l'étendue
   des données »).

**Critères de réussite.** Sont exigés : les trois mesures du défaut (1), les trois phrases fausses
avec leur contre-mesure (2), une décision écrite **et** chiffrée (3), une figure corrigée avec sa
déclaration (4), et une réponse exacte sur les couches du contrôle (5). Le seuil est de **12/20**.

---

## Correction détaillée

### A · Réponses de récupération

1. **Position** > longueur > angle > surface > couleur — Cleveland et McGill 1984, répliqué en 2010
   sur des milliers de participants.
2. Une couleur **un seul rôle** dans une figure et dans la charte : si l'orange signifie « remise »
   ici et « retours » là, le lecteur ne peut plus construire de contrat de lecture (C03).
3. Une **erreur** est un écart entre ce que la figure laisse croire et ce que les données disent ;
   une **décision** est cet écart **déclaré** (axe non nul annoncé, échelle log annoncée). Une
   erreur déclarée devient légitime ; la 3D et la couleur à tout faire sont les deux seules
   qu'aucune déclaration ne sauve (C05).
4. Jusqu'à **3** parts ; au-delà, l'écart minimal entre deux voisines tombe à **0,05** point, soit
   **0,17°**.
5. **Niveau** (« où en est-on ? »), **mécanisme** (« pourquoi ? »), **décision** (« que fait-on,
   pour combien, et comment le saura-t-on ? »).
6. **Exécutés** : matplotlib/seaborn (et Excel, écrit **puis relu**). **Cité** : Power BI
   (**9** clics décrits, aucun fichier produit) — règle §1.5.

### B · Corrigé du quiz (1 pt par question)

**Q1** a — la hiérarchie du module, fondée sur les erreurs de jugement mesurées.
**Q2** b — des barres triées : la longueur bat l'angle pour un classement de **8** catégories.
**Q3** b — la phrase fausse attendue est un classement, alors que **0,17°** ne se distinguent pas ;
le camembert reste lisible jusqu'à **3** parts.
**Q4** a — **3,0** pour un élément de graphique, **4,5** pour du texte ; le jaune du socle (1,43)
échoue aux deux et ne s'utilise qu'en remplissage secondaire.
**Q5** b — environ **8 %** des hommes ; d'où la redondance couleur + forme + libellé.
**Q6** a — « les deux séries sont la même » : **35,7** de différence perçue reste au-dessus du seuil
de **10**, mais la paire n'est plus fiable seule — la redondance est obligatoire.
**Q7** b — le titre qui affirme **porte une mesure** : sur le fil rouge, **0** sur 5 titres « avant »
portaient une mesure, **5** sur 5 après.
**Q8** b — c'est l'affirmation qui compte ; **113,2** caractères mesurent une conséquence, pas une
qualité.
**Q9** a — la volatilité est fabriquée par la **fenêtre** : **5,4 %** réels contre une amplitude
apparente **× 7,0**.
**Q10** b — le **total** de chaque période : les huit trimestres vont de **960 721 755** à
**1 012 518 068** FCFA (**5,4 %**) quand la part d'un mode ne bouge que de **1,9** point.
**Q11** c — l'**effet 3D** : la profondeur ne porte aucune donnée et déforme les comparaisons. Un
axe tronqué se déclare, une échelle log s'annonce, un camembert à **3** parts est lisible.
**Q12** a — « les ventes sont homogènes, la queue est marginale » : le log donne **93,5 %** de la
largeur à la masse et réduit la queue (**1 044** ventes, **7,1 %** du CA) à **1,3 %**.
**Q13** b — niveau, mécanisme, décision.
**Q14** b — **2** sur 5 : le cadre unique de **12** chiffres couvrait le niveau et le levier, rien
d'autre.
**Q15** a — « on ne lit rien, refaites l'export » : le format ne change pas la donnée, mais
**604 × 340** px ne suffisent pas à l'impression quand **1 889 × 1 062** px sont attendus.

### C · Corrigé des dix prédictions

| # | Valeur | Ce que la valeur sert à démontrer |
|---|---|---|
| 1 | **5,4** | la variation réelle du fil rouge (moyenne glissante) |
| 2 | **11,8** | la hauteur occupée sur un axe à zéro, en % |
| 3 | **82,4** | la hauteur occupée sur l'axe tronqué 300-350 M |
| 4 | **+0,35** | la corrélation affichée par le double axe |
| 5 | **0,17** | l'écart minimal entre deux parts, en degrés |
| 6 | **5,4** | la variation des totaux trimestriels, masquée par le cumul |
| 7 | **1,9** | l'amplitude d'une part de mode, en points — ce que le cumul, lui, montrait |
| 8 | **77,0** puis **93,5** | la masse sous 250 000 FCFA, en % des ventes et en % de largeur en log |
| 9 | **1 044** | les ventes de plus de 500 000 FCFA (**2,1 %** des ventes, **7,1 %** du CA) |
| 10 | **21** sur **28** | les paires classées à l'envers par un tri alphabétique (**75 %**) |

### D · Corrigé des exercices à rendre

**E1 — les cinq questions.**

1. **Évolution du CA** → courbe + moyenne glissante, axe à zéro annoncé ; mesure : **5,4 %** de
   variation réelle, **307,6** à **348,8** M FCFA ; piège écarté : l'axe tronqué, qui porterait la
   hauteur occupée à **82,4 %**.
2. **Classement des catégories** → barres triées, valeurs absolues ; mesure : de **697** à
   **1 231** M FCFA (**8** catégories) ; piège écarté : le camembert (angle), illisible au-delà de
   **3** parts.
3. **Poids des gros paniers** → barres ou histogramme avec zoom séparé sur la queue ; mesure :
   **1 044** ventes de plus de 500 000 FCFA = **2,1 %** des ventes et **7,1 %** du CA ;
   piège écarté : l'échelle logarithmique non annoncée, qui écrase la queue à **1,3 %** de largeur.
4. **Mix de paiement** → barres empilées en **valeurs absolues** (ou lignes par mode) ; mesure :
   totaux trimestriels de **960 721 755** à **1 012 518 068** FCFA (**5,4 %**) ; piège écarté : le
   cumul à 100 %, qui masque ces totaux.
5. **Distribution des montants** → histogramme linéaire **annoncé** et zoom sur la queue ; mesure :
   médiane **119 482** FCFA, maximum **594 363** (rapport **5**), **77,0 %** des ventes sous
   250 000 FCFA ; piège écarté : le log surprise.

**E2 — la charte.** Attendu : **3** à **5** couleurs, chacune avec son contraste (bleu **8,66**,
rouge **6,74**, vert **5,91**, orange **3,78**, gris **3,05**), le seuil rappelé (**4,5** texte /
**3,0** graphique), la redondance écrite (couleur **+** forme **+** libellé), et la règle de rôle.
Le contraste du jaune (**1,43**) doit être signalé comme rédhibitoire pour un élément porteur
d'information.

**E3 — la relecture.** Attendu, pour les 5 affirmations du rapport :

| Affirmation du rapport | Question qui l'attrape | Mesure qui la contredit | Verdict |
|---|---|---|---|
| « croissance continue » | l'échelle | **5,4 %** de variation réelle, **+1,4 %** sur un an | à corriger (l'axe tronqué fait le récit) |
| « les retours suivent le CA » | les liens | corrélation **+0,35** sur **24** mois, retours de **4** à **16** par mois | fausse (le double axe crée le lien) |
| « catégories déséquilibrées, une pèse un quart » | la densité et l'ordre | **8** parts, écart minimal **0,17°** ; de **697** à **1 231** M FCFA | à corriger (barres triées, valeurs écrites) |
| « le mix est stable » | les liens | totaux variant de **5,4 %**, part d'un mode bougeant de **1,9** point | à corriger (le cumul masque les totaux) |
| « les gros montants sont rares » | la question de l'échelle | **1 044** ventes > 500 000 FCFA = **7,1 %** du CA | confirmée, mais illisible en log |

### E · Corrigé de l'étude de cas — les cinq attendus

1. **Le défaut mesuré.** Axe tronqué (n° 1) : la fenêtre 300-350 M occupe **82,4 %** de sa hauteur
   pour une étendue qui n'en occupe que **11,8 %** sur un axe à zéro ; amplitude apparente
   **× 7,0** ; variation réelle **5,4 %** (moyenne glissante) contre **13,4 %** sur la série brute.
   Phrase clé : l'écart vient de **la fenêtre**, la donnée n'a pas bougé.
2. **Les trois phrases fausses.** (a) « la volatilité augmente » → contredite par la moyenne
   glissante, qui reste entre **320** et **337** M FCFA ; (b) « il y a un décrochage » → le point
   bas isolé est un mois creux de la série brute, pas une tendance ; (c) « la croissance est portée
   par le second semestre » → sur **24** mois, l'écart entre les deux années n'est que de **+1,4 %**.
3. **La décision chiffrée.** Dispositif de renfort voté pour répondre à une volatilité **apparente**
   **× 7,0** : le coût de plusieurs dizaines de millions de FCFA est à comparer à ce qui l'aurait
   justifié — un seuil raisonnable, par exemple une variation de la moyenne glissante supérieure à
   **10 %** sur deux trimestres, n'est jamais atteint (**5,4 %** au maximum).
4. **La version qui l'aurait empêchée.** Axe à zéro, titre qui affirme (« Le CA est plat sur
   **24** mois : moyenne glissante entre **320** et **337** M FCFA »), annotation de la moyenne
   glissante, et déclaration écrite (« axe à zéro, non tronqué »). La courbe devenant franchement
   plate, la demande de renfort n'aurait pas tenu une question.
5. **Les couches du contrôle.** **L2** (totaux identiques) **ne suffit pas** : un axe tronqué ne
   change aucune valeur. **L4** (audit du code) l'attrape **si** le contrôle lit les `set_ylim` —
   c'est justement pourquoi le contrôle audite le **code** et non l'image. Il faut donc un contrôle
   supplémentaire : **comparer la fenêtre de l'axe à l'étendue des données** et exiger une
   **déclaration** dans le titre quand la fenêtre est tronquée. C'est la leçon du module : ce qui
   ne se mesure pas ne se corrige pas.
