# La grille visuelle en 18 points — l'artefact du module M10

**Ce que c'est.** La grille d'évaluation d'un graphique ou d'un tableau de bord, en **18** points
répartis en **4** familles. Elle sert à **auto-évaluer** un livrable, puis à le faire **relire par un
pair**. Elle est née au module M10 (Data visualization), où elle note le projet « La refonte », et
elle est **réutilisée** telle quelle dans les modules **M14** (Power BI), **M17** (automatisation) et
**M21** (mission finale) : c'est un artefact du manuel, pas un barème jetable.

**Pourquoi 18 points, et non 20.** L'architecture (§E.7) annonçait « 20 points, 4 points par
famille » — une incohérence arithmétique (4 × 4 = **16**). Le module M10 et le module M14 disent
**18** points en **4** familles ; la répartition retenue est **4 / 5 / 5 / 4**, et l'errata est porté
au fichier d'architecture dans le push de clôture de M10. Une grille de 20 points n'aurait pas changé
le seuil : elle aurait seulement changé le barème du dernier point.

---

## 1. La grille

**Comment la lire.** Chaque ligne est un **critère mesurable** : la colonne « le test » dit ce qu'on
regarde, pas ce qu'on ressent. Un critère se coche ou ne se coche pas ; une case à moitié cochée est
un critère à reformuler, pas à arrondir. Les quatre familles sont notées séparément — c'est ce qui
permet de dire « juste mais illisible » ou « lisible mais faux », deux diagnostics que la note globale
écrase.

### Famille 1 — Décision servie (4 points)

| # | Critère | Le test |
|---|---|---|
| **1** | **Une décision est nommée** | la figure ou le tableau de bord répond à une décision écrite en clair (« faut-il renforcer la relance sur la queue ? »), pas à un thème (« le CA ») |
| **2** | **Une question par figure** | chaque figure sert une question : si le titre énonce deux choses, le critère n'est pas coché |
| **3** | **Le chiffre principal est identifiable en 5 secondes** | un lecteur qui découvre la figure doit pouvoir énoncer le chiffre clé sans aide ; s'il hésite entre deux, c'est non |
| **4** | **La décision demandée est écrite** | la figure ou la note porte une demande : qui agit, sur quoi, pour combien ; une figure sans appel à la décision ne sert aucune décision |

### Famille 2 — Justesse (5 points)

| # | Critère | Le test |
|---|---|---|
| **5** | **Les totaux sont cohérents aux niveaux affichés** | le total de la figure = somme des parties, **à 0,00** près (le contrôle automatique du module compare les trois sommes : catégories, trimestres, total net) |
| **6** | **L'axe est honnête** | axe à zéro, ou troncature **déclarée** dans le titre ; aucun axe tronqué pour des **barres** |
| **7** | **Les liens sont déclarés** | double axe, échelle logarithmique, cumul à 100 % : chacun est annoncé, ou retiré ; la coïncidence visuelle n'est jamais présentée comme un lien |
| **8** | **L'unité, la source et la période sont écrites** | unité (FCFA, %, nombre), source (jeu, filtres), période (du … au …), et date d'extraction pour un indicateur suivi |
| **9** | **Aucun chiffre n'est modifié par la mise en forme** | pas de lissage, d'arrondi de série, de « nettoyage » ni de regroupement qui change un total ; le module refuse une refonte qui change un chiffre |

### Famille 3 — Lisibilité (5 points)

| # | Critère | Le test |
|---|---|---|
| **10** | **La hiérarchie est visible** | le chiffre principal domine la figure ; le regard ne se perd pas entre quatre tailles de texte et six couleurs |
| **11** | **Le titre affirme** | le titre porte une **mesure** (un chiffre, un écart, une période) ; « Évolution du chiffre d'affaires » ne coche pas |
| **12** | **L'annotation porte le chiffre clé** | le constat principal est annoté **dans** la figure, pas relégué au commentaire oral |
| **13** | **Les catégories sont ordonnées** | tri par valeur, par temps ou par métier — jamais l'ordre alphabétique par défaut (**21** paires sur **28** sont alors à l'envers sur **8** catégories) |
| **14** | **Contraste et accessibilité** | contraste ≥ **3,0** contre le fond pour un élément porteur d'information (≥ **4,5** pour du texte) ; redondance couleur **+** forme **+** libellé, une couleur par rôle |

### Famille 4 — Utilisation (4 points)

| # | Critère | Le test |
|---|---|---|
| **15** | **Le format est adapté au support** | définition et format d'export alignés sur l'usage (écran, impression, retouche) ; **300** dpi pour l'impression, vectoriel pour un graphique de traits |
| **16** | **Le fichier est réutilisable** | la source est transmise avec la figure (script ou classeur) ; un pair peut refaire le graphique sans appeler l'auteur |
| **17** | **Les segments et filtres utiles existent** | un tableau de bord se filtre sur ce qui sert la décision, et **pas** sur tout : chaque filtre est justifié par la question (famille 1) |
| **18** | **Le livrable est documenté** | une note d'une page : ce que la figure montre, ce qu'elle ne montre pas, ce qu'il faut vérifier avant de s'en servir |

---

## 2. Comment l'utiliser (le protocole en deux notes)

1. **L'auteur s'auto-évalue** : il coche les **18** critères, écrit une phrase par critère non coché,
   et obtient une note sur **18** — puisqu'un critère se coche ou ne se coche pas, et que la
   répartition est **4 / 5 / 5 / 4**.
2. **Un pair relit** la même figure sans connaître la note de l'auteur, et remplit la même grille.
3. **L'écart se commente.** Un écart d'un point se règle en une phrase ; un écart de **3** points et
   plus signale presque toujours un critère mal compris par l'un des deux — c'est le commentaire qui
   fait progresser, pas la moyenne des deux notes.
4. **Le seuil.** **12** points sur **18** valident un livrable publiable en interne ; en dessous de
   **12**, on reprend en priorité la famille la plus basse (c'est presque toujours la famille 1 : la
   décision servie).

**Le contrôle automatique du projet** (`tools/controle_refonte_M10.py`) vérifie ce qui est
vérifiable par machine — **L2** les totaux identiques et conformes au socle, **L3** le format et la
largeur des figures, **L4** l'écriture auditée **dans le code** (titres qui affirment, axes, échelle,
annotations). La grille, elle, juge ce qui ne se calcule pas : la décision servie, la hiérarchie, la
documentation. Les deux se complètent : un contrôle automatique vert avec une note de grille de
**9** sur **18** donne un livrable exact et inutilisable.

## 3. Ce que la grille attrape, mesuré sur le fil rouge

| Famille | Le défaut le plus fréquent | La mesure qui le contrôle |
|---|---|---|
| Décision servie | la figure répond à un thème, pas à une décision | la séquence de trois écrans couvre **5** objections sur **5** quand un cadre unique en couvrait **2** |
| Justesse | l'axe tronqué présenté comme un zoom | **82,4 %** de hauteur occupée pour une variation réelle de **5,4 %** (amplitude apparente **× 7,0**) |
| Lisibilité | le titre d'étiquetage | **0** titre sur **5** portait une mesure avant correction, **5** sur **5** après |
| Utilisation | un PNG 96 dpi envoyé à l'imprimeur | **604 × 340** px contre les **1 889 × 1 062** px attendus à **300** dpi |

> **À retenir.** Une grille qui coche tout ne vaut rien : si les **18** critères sont satisfaits du
> premier coup, c'est la grille qui n'a pas été lue attentivement. Sur le fil rouge, le rapport
> d'origine — chiffres justes, mise en page soignée — obtient **7** points sur **18** et échoue dans
> **3** familles sur **4**. C'est l'écart entre « pas faux » et « honnête » que cette grille mesure.
