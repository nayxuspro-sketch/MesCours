# Analyse de la qualité technique et pédagogique du module « Thème 7 — Violence et addiction »
## Serious Game SDSR (sdsr.ticanalyse.org) — rapport destiné aux enseignants et formateurs accompagnant des élèves d'environ 15 ans au Burkina Faso

[[COVER]]
| Élément | Description |
|---|---|
| Ressource analysée | Page « Thème 7 – Serious Game » : https://sdsr.ticanalyse.org/theme-7/ |
| Titre porté par le module | « Thème 7 Violence et addiction » (intitulé de la plateforme : « Violences et addictions ») |
| Nature de la ressource | Serious game de sensibilisation — module e-learning HTML5, empaqueté en SCORM 1.2 |
| Plateforme | Serious Game SDSR (9 modules) — sdsr.ticanalyse.org, édité par TICANALYSE |
| Production éditoriale | BESbswy et _wb_incandescent |
| Technologie | Articulate Storyline 360 (HTML5), thème « unified », 1 scène / 12 diapositives |
| Version publiée | 29 octobre 2026 — Storyline 3.120.37241.0 |
| Public visé | Élèves d'environ 15 ans (collège), contexte burkinabè |
| Durée et volume | ≈ 10 minutes de module, puis un quiz d'évaluation (annonce de la plateforme : 10 min, 8 questions) |
| Corpus effectivement analysé | Code du module (data.js), 12 diapositives, 115 médias, 78 pistes de sous-titres lues intégralement, manifeste SCORM, page d'accueil, cadre de référence Enabel |
| Note de qualité technique | **4,9 / 10** — voir le chapitre 4 |
| Note de valeur et de qualité éducative | **5,3 / 10** — voir le chapitre 5 |
| Date du rapport | 6 novembre 2026 |
| Destinataires | Enseignants, formateurs, responsables de programme, commanditaire |
[[COVER_END]]

[[PAGEBREAK]]

## Sommaire

1. Synthèse et verdicts
2. Méthode, périmètre et limites de l'analyse
3. Fiche d’identité du module et parcours de l’apprenant
4. Analyse de la qualité technique
5. Analyse de la valeur et de la qualité éducative
6. Plan d’amélioration priorisé (13 actions)
7. Conclusion
8. Annexes (A à F)

## 1. Synthèse et verdicts

### 1.1 Verdict sur la qualité technique : 4,9 / 10 — « correct sur le fond, perfectible sur la forme »

Le module est **techniquement sain et industriellement propre**. Il est produit par un outil professionnel (Articulate Storyline 360), publié dans une version horodatée, livré avec un manifeste SCORM 1.2 valide, servi derrière un CDN Cloudflare avec compression Brotli, cache long (4 h) et en-têtes HSTS. Sur le plan de l’architecture et de la reproductibilité, il n’y a rien à redire : un autre formateur peut reprendre, corriger et republier le module sans intervention technique.

Deux réserves lourdes, toutefois, pèsent sur la note :

- **Le poids est rédhibitoire pour le contexte visé.** Le paquet exporté pèse **162,8 Mo**, dont **107,8 Mo de GIF animés** (66 %) et 45,5 Mo de vidéos MP4. À cela s’ajoute un player qui n’est pas « adaptatif » : il n’y a ni mode « réseau faible », ni téléchargement hors ligne, ni version allégée. Dans un pays où la connexion est souvent mobile, limitée et facturée au volume, un élève qui ouvre le module dans un cybercafé ou avec un forfait data voit le contenu se charger par morceaux.
- **L’accessibilité est techniquement disponible mais désactivée.** Le moteur sait faire des sous-titres, du texte accessible, des descriptions alternatives et une navigation clavier : ces fonctions existent dans les données du module, mais le paramètre `displayCaptions` est à `false`, `accessibleText` est à `false`, et aucun sous-titre n’est proposé par défaut à l’apprenant. Le contraste de certains libellés (#7A7A7A sur #212121, soit ≈ 3,2:1) est en outre en dessous du seuil de 4,5:1 attendu.

S’ajoutent des points moins critiques mais réels : l’absence d’activation du SCORM par le site (aucune remontée de résultat ni de suivi), une interopérabilité xAPI explicitement désactivée, une chaîne de production mono-éditeur (Storyline), aucune politique de confidentialité repérable, et une édition française qui conserve plusieurs coquilles sur des messages pédagogiques clés.

> **Ce que l’enseignant doit retenir :** le module fonctionne, il s’ouvre, il se projette, il ne plante pas. Il est seulement trop lourd, et ses qualités d’accessibilité ne sont pas activées.

### 1.2 Verdict sur la valeur et la qualité éducative : 5,3 / 10 — « un bon module d’introduction, pas encore un module de curriculum »

Le module est **narrativement supérieur à la moyenne** de ce que l’on trouve en santé de la reproduction au Burkina Faso. Ce n’est pas un diaporama passif : c’est un scénario à quatre séquences dans lequel l’apprenant **agit, choisit et subit les conséquences de ses choix**. La structure est en réalité un **arbre de décisions** : cinq points de décision (D1 à D5), chacun suivi d’une conséquence explicitement énoncée à l’apprenant. Le module admet même la rechute et fait construire à l’apprenant un argumentaire contre la stigmatisation. Sur le plan de l’engagement et de la scénarisation, c’est le point fort du produit.

Mais trois écarts profonds séparent ce module de ce que le dispositif SDSR promet :

- **Un écart de couverture.** Le référentiel thématique du projet (document Enabel, décembre 2025) consacre au Thème 7 quatorze pages couvrant : définitions, caractéristiques communes des addictions, causes et facteurs de vulnérabilité, conséquences, types de drogues (licites et illicites, alcool, tabac, solvants, cannabis, tramadol), précautions, et **violences physiques, psychologiques et morales**. Le module ne traite qu’un seul versant : la pression des pairs autour d’une « drogue » générique. Le mot « violence » — au cœur de l’intitulé du thème — **n’apparaît dans aucune des 78 pistes de sous-titres** du module.
- **Un décalage entre compétence développée et compétence évaluée.** Les séquences font travailler l’application et l’analyse (Bloom 3-4) ; le quiz, lui, ne mesure que la compréhension et la mémorisation (Bloom 1-2). Cinq items vrai/faux, seuil de réussite à 80 %, **18,75 % de réussite possible par hasard pur**. Le module évalue donc ce que l’apprenant a retenu du discours, pas ce qu’il est censé savoir faire.
- **Un déficit d’accompagnement.** Aucune fiche d’animation, aucun scénario de débriefing, aucune consigne pour l’enseignant, aucun relais clairement identifié (centre de santé, école, association), aucune exploitation des résultats. Un serious game sans dispositif d’accompagnement est un film interactif : divertissant, mais peu formatif en tant que dispositif pédagogique.

### 1.3 Les cinq constats qui structurent le rapport

1. **Le module est « trop » bien construit pour ce qu’il dit, et « trop peu » construit pour ce qu’il devrait dire.** L’arbre de décisions est remarquable ; la couverture thématique est étroite ; l’évaluation est faible. L’effort de production a été consenti sur l’interactivité, pas sur le contenu ni sur l’instrumentation pédagogique.
2. **Le poids du contenu est inversement proportionnel à sa valeur.** 162,8 Mo pour sept minutes de récit : une large part du paquet est constituée de GIF animés à usage décoratif. On peut diviser le poids par quatre sans perdre une seconde de sens pédagogique.
3. **Les fonctions d’accessibilité existent mais sont éteintes.** Le module a été produit par un outil qui sait faire mieux ; c’est les paramètres de configuration qui n’ont pas été activés. La correction est quasi gratuite.
4. **Le module est cohérent avec lui-même, pas avec son annonce.** La plateforme annonce « 8 questions » pour un quiz de 5 items ; l’intitulé du thème promet la violence, le module ne parle que de drogues. C’est un problème de contrat de communication, pas de contenu.
5. **Le module est utilisable seul, mais excellent accompagné.** En l’état, il fonctionne comme une amorce de discussion ; il ne fonctionne pas comme une séance complète de prévention. Il manque le débriefing, qui est le moment où, chez les 15 ans, la prévention se joue.

### 1.4 À retenir en deux minutes

> **Ce qui est bon :** un scénario rythmé, une langue orale directe et proche, un arbre de décisions qui donne de l’agentivité à l’apprenant, une option-piège très bien construite (« je continue à les fréquenter, mais je ne prendrai plus rien »), un double message (refuser la pression / soutenir l’entourage), et une intention de stigmatisation de la toxicomanie explicitement combattue.
>
> **Ce qui manque :** le versant « violence » du thème, les produits réellement accessibles aux jeunes burkinabè (alcool, tabac, solvants, tramadol), les données et les repères de santé publique, un personnage féminin, les relais concrets vers l’aide, un item d’évaluation de niveau supérieur, et tout le dispositif d’accompagnement enseignant.
>
> **Ce qu’il faut corriger en priorité :** alléger le paquet, activer les sous-titres et le texte accessible, fixer les métadonnées annoncées, enrichir le quiz d’un item d’application, et produire une fiche d’animation d’une page.

[[PAGEBREAK]]

## 2. Méthode, périmètre et limites de l’analyse

### 2.1 Protocole

L’analyse ne repose sur aucune impression d’écran ni sur la seule lecture de la page de présentation : le module a été **désossé** et lu à la source. Chaque affirmation de ce rapport renvoie soit à un fichier du paquet exporté, soit à un document de référence externe.

| Source consultée | Ce qui en a été tiré | Usage dans le rapport |
|---|---|---|
| Page `sdsr.ticanalyse.org/theme-7/` | Intitulé du module, lecteur intégré, encadré « Ressources », messages du lecteur | Cadrage, §3 |
| Page d’accueil `sdsr.ticanalyse.org/` | Les 9 modules de la plateforme, niveaux, durées et nombres de questions annoncés | §3, §4.11 |
| `…/articulate_uploads/Theme-7/html5/data/js/data.js` | Modèle de contenu complet : liste des 12 diapositives, configuration du quiz, inventaire des 115 médias (tailles, durées), textes français, réglages du lecteur | §4.1 à §4.11, annexes C et F |
| Scripts de diapositives (`5guRVR1aCO4`, `5xrM8Lmi1NO`, `5XKtytmYCOn`, `66A4bh6oQxh`…) | Structure des écrans, boutons, groupes de réponses, couches de feedback, écran de résultats | §4, §5.6, §5.7 |
| 78 pistes de sous-titres (16 transcriptions de vidéo + 62 sous-titres audio) | **Narration intégrale, libellés de l’arbre de décisions et conséquences, énoncés et feedbacks du quiz** | §4.9, §5.2 à §5.7, annexes A et B |
| `…/Theme-7/imsmanifest.xml` et `index_lms.html` | Déclaration SCORM 1.2, point de lancement, version du lecteur Storyline, message hors-ligne | §4.2, §4.6, §4.7 |
| Document « Contenus thématiques sur la SDSR adaptés aux jeunes et adolescent·e·s à digitaliser » (Enabel, décembre 2025) | Référentiel de contenu des 9 thèmes, dont les 5 rubriques du Thème 7 (définitions, caractéristiques, causes, conséquences, types de drogues, précautions, violences) | §5.2, §5.3, annexe D |
| Documentation publique de la plateforme (TICANALYSE, « Digitalisation de contenus ») | Positionnement de l’offre et méthode de conception des serious games | §2.2, §6 |

### 2.2 Limites de l’analyse

- **Six fichiers de sous-titres annoncés dans l’inventaire n’étaient pas présents dans le paquet** au moment de l’analyse : les branches correspondantes ont donc été reconstituées à partir des transcriptions vidéo et des sous-titres restants. Les libellés et conséquences de ces branches sont déduits, non copiés.
- **Les scores et les règles de barème n’ont pas pu être observés en conditions réelles d’apprentissage** : l’analyse repose sur le code du module, pas sur une classe. Les gains de temps de chargement réels ne sont donc pas mesurés, et le plan d’amélioration est formulé en termes de modifications de code et de scénario.
- **La plateforme dans son ensemble n’a été qu’inventoriée** : les 8 autres modules ont été repérés (titres, durées, nombre de questions) sans être analysés, ce rapport portant sur le seul Thème 7.
- **Les données de santé publique (prévalence, chiffres de l’épidémie) n’ont pas été ajoutées** à la critique : le document Enabel n’en fournit pas davantage et le module n’en cite aucune. Le signalement est fait comme un manque, pas comme une erreur.

### 2.3 Grille de notation utilisée

Les notes sont attribuées sur 10 et **pondérées** selon la criticité de chaque critère dans le contexte d’usage visé (usage scolaire de masse, réseau contraint, matériel disparate).

| Note | Signification retenue dans ce rapport |
|---|---|
| 9 – 10 | Excellent, conforme aux meilleures pratiques, aucun correctif nécessaire |
| 7 – 8 | Bon, utilisable en l’état, corrections mineures |
| 5 – 6 | Acceptable mais perfectible ; reserves à traiter avant un usage à grande échelle |
| 3 – 4 | Insuffisant ; bloque une partie de l’usage visé |
| 1 – 2 | Défaillant |

Les deux grilles pondérées figurent en fin de chapitre technique (4.12) et de chapitre pédagogique (5.12), avec le poids de chaque critère, pour que le lecteur puisse refaire le calcul et discuter des pondérations.

[[PAGEBREAK]]

## 3. Fiche d’identité du module et parcours de l’apprenant

### 3.1 Fiche d’identité

| Rubrique | Constat vérifié |
|---|---|
| Intitulé du module | « Thème 7 Violence et addiction » |
| Intitulé de la plateforme | « Violences et addictions » (7ᵉ des 9 modules de la plateforme SDSR) |
| Type | Serious game narratif — 4 séquences scénarisées + quiz d’évaluation à 5 items |
| Durée annoncée | 10 minutes (plateforme) |
| Niveau annoncé | « Apprenant » |
| Quiz annoncé | 8 questions (plateforme) — **réel : 5 items** |
| Moteur | Articulate Storyline 360, lecteur 3.120.37241.0, thème « unified », 1 scène, 12 diapositives |
| Format de diffusion | Web (iframe `story.html`) + paquet SCORM 1.2 (`imsmanifest.xml`, lancement `index_lms.html`) |
| Langue | Français (localisation du lecteur incluse) |
| Personnage principal | Moussa, adolescent ; secondary characters : Moussard (grand frère), le groupe de pairs, un adulte référent |
| Contenu sensible traité | Consommation de drogues, pression des pairs, dépendance,_entraide et soutien, rechute |
| Contenu sensible **non** traité | Alcool, tabac, solvants, tramadol, cannabis ; violences physiques, psychologiques et morales |
| Médias | 115 fichiers, 162,8 Mo : 16 MP4, 62 MP3, GIF et PNG ; ≈ 7 min 11 s de médias |
| Accessibilité | Moteur compatible (sous-titres WEBVTT, texte accessible, tabulation, descriptions) mais **fonctions désactivées** |
| Interopérabilité | SCORM 1.2 produit mais non activé par le site ; xAPI désactivé ; aucune remontée de résultat |
| Hébergement | WordPress + CDN Cloudflare (Brotli, ETag, HSTS, cache 4 h) |
| Date de publication | 29 octobre 2026 (version du lecteur et date de publication du paquet) |
| Production | TICANALYSE (développement) ; BESbswy et _wb_incandescent (contenu) ; projet SDSR / Enabel (commanditaire) |

### 3.2 Le parcours de l’apprenant, minute par minute

1. **Ouverture (≈ 0:00).** L’apprenant arrive sur la page « Thème 7 Violence et addiction », un lecteur de diapositives est déjà intégré, avec ses commandes (lecture, sous-titres, vitesse, zoom, texte accessible, raccourcis clavier). Le module démarre sur la première séquence.
2. **Séquence 1 — La situation (≈ 0:00 → 2:30).** Moussa, 15 ans, dans son entourage. Un groupe de pairs lui propose de « prendre quelque chose ». L’apprenant est placé en **position de décision**, pas de spectateur.
3. **Point de décision D1 (≈ 2:30).** Accepter ou refuser. Chaque branche déclenche une conséquence explicitement énoncée : accepter et rester avec le groupe, ou refuser et s’éloigner.
4. **Séquence 2 — L’aggravation (≈ 2:30 → 5:00).** Les signes de l’évolution : changement de comportement, isolement, tensions. Le module montre la **progression** de la dépendance et l’amorce du remords.
5. **Point de décision D2 (≈ 5:00).** Un adulte propose son aide. Accepter (« Oui, j’ai un problème, je voudrais en parler avec vous ») ou refuser (« Non, tout va bien », « Je peux arrêter tout seul »). Le refus est traité sans procès, mais sa conséquence est dite.
6. **Point de décision D3 (≈ 6:00).** L’option-piège : « Je vais continuer à les fréquenter, mais je ne prendrai plus rien » face à une rupture assumée du lien. C’est le moment le plus formateur du module.
7. **Séquence 3 — L’inversion des rôles (≈ 6:00 → 7:30).** Moussa change de place : il devient celui qui constate l’addiction de son grand frère Moussard. Le module déplace la question de «comment sortir » vers « comment aider ».
8. **Point de décision D4 (≈ 7:30).** *Que va conseiller Moussa ?* Stigmatiser (« Laisse-le se débrouiller, c’est son problème ») ou soutenir (« Parle lui sans le juger et encourage le à demander de l’aide »).
9. **Point de décision D5 (≈ 8:00).** La proposition de reconsommation : « D’accord, juste pour une dernière fois. » Le module **admet la rechute** et en montre le coût.
10. **Quiz (≈ 8:30 → 10:00).** Cinq items vrai/faux, notés 10 points chacun, seuil de réussite à 80 % (soit 4/5). Chaque item reçoit un feedback explicatif, juste ou incorrect.
11. **Écran de résultats (≈ 10:00).** Score obtenu, score à atteindre, incitation à recommencer. **Les résultats ne sont pas transmis à l’enseignant** : rien n’est enregistré côté serveur.

### 3.3 Cartographie des 12 diapositives

| # | Diapositive (identifiant Storyline) | Contenu | Verdict pédagogique |
|---|---|---|---|
| 1 | `5guRVR1aCO4` | Séquence 1 — mise en situation, pression des pairs | Point d’entrée narratif solide |
| 2 | `6mLPNYCHPmB` | Séquence 2 — progression et signes de la dépendance | Bonne dramatisation, mais vocabulaire non outillé |
| 3 | `60r9wkCxoTh` | Séquence 3 — inversion des rôles, le cas du grand frère | Moment le plus fort du module |
| 4 | `6PTK0u594oo` | Séquence 4 — conseil, soutien, rechute | Clôture moralisée mais honnête |
| 5 | `5xrM8Lmi1NO` | Introduction au quiz (invite « Vrai ou faux ») | Clair, mais formulation fautive relevée |
| 6 | `5XKtytmYCOn` | Question 1 | Item de niveau 1 (mémorisation) |
| 7 | `5W5ep06D6Pi` | Question 2 | Item de niveau 1-2 |
| 8 | `6Lho6koseKD` | Question 3 | Item de niveau 2, le plus utile |
| 9 | `5nIVFRqt1G7` | Question 4 | Item de niveau 2, porte le message anti-stigmatisation |
| 10 | `63oS9JOhBCU` | Question 5 | Item de niveau 2, le plus directement appliqué |
| 11 | `66A4bh6oQxh` | Écran de résultats (« VOTRE SCORE », seuil) | Fonctionnel, sans capitalisation pédagogique |
| 12 | `5c4t2a8OMjH` | Reboot / retour au début | Boucle de réessai |
| + | 2 invites (prompts) | Transitions et consignes | Utilisées pour le rythme |

[[PAGEBREAK]]
## 4. Analyse de la qualité technique

### 4.1 Architecture, hébergement et sécurité du transport

Le module est servi depuis le site WordPress de la plateforme, dans le dossier `wp-content/uploads/articulate_uploads/Theme-7/`. La page `theme-7` (identifiant WordPress 2540, dernière modification le 29 octobre 2026) n’héberge pas le contenu elle-même : elle insère une **iframe** qui charge le point d’entrée `story.html` du paquet Storyline. Ce même dossier héberge également le **paquet SCORM complet** (`imsmanifest.xml`, `index_lms.html`, `html5/…`), c’est-à-dire que le contenu existe en double version : web et SCORM.

Le transport est assuré par **Cloudflare** devant un **nginx/1.24.0 (Ubuntu)**. Les en-têtes observés montrent une configuration sérieuse : compression **Brotli**, **ETag**, **HSTS**, `Cache-Control` avec un `max-age=14400` (4 heures) et un message de reconnexion hors ligne explicitement traduit en français dans le lecteur.

| Point contrôlé | Constat | Appréciation |
|---|---|---|
| Point d’entrée web | `story.html` en iframe, chargement autonome | Correct |
| Paquet SCORM | `imsmanifest.xml` valide (SCORM 1.2), lancement `index_lms.html` | Correct, mais inutilisé par le site (§4.6) |
| Chiffrement et en-têtes | HTTPS, HSTS, ETag, Brotli | Bon |
| Cache | 4 heures sur les ressources statiques | Correct pour une consultation répétée |
| Gestion hors ligne | Message de reconnexion présent et traduit | Correct |
| Versionnage des contenus | Contenu publié dans `uploads/`, sous une URL stable | **Réserve** : la mise à jour écrase le contenu sous la même adresse, sans numéro de version ni empreinte de contrôle |
| Accès direct au paquet | Le paquet est téléchargeable sans authentification | Choix cohérent pour un contenu ouvert ; en revanche, le module ne peut pas servir de preuve de formation |
| Politique de confidentialité | Aucune page de politique de confidentialité repérée sur le site | **Réserve** : à traiter si le module est décliné en version nominative ou utilisé dans un dispositif de validation |

**Appréciation.** L’architecture est propre, standard et sans surprise. Le principal risque n’est pas technique mais **contractuel** : le module est publié sous une URL non versionnée, et le site n’expose aucune politique de protection des données, deux points à verrouiller avant toute exploitation à l’échelle d’un district.

### 4.2 Moteur et chaîne de production

Le module est produit avec **Articulate Storyline 360** (version du lecteur 3.120.37241.0, thème graphique « unified », une scène, douze diapositives, localisation française incluse). L’ensemble du contenu est décrit dans un fichier unique `html5/data/js/data.js` : liste des diapositives, identifiants Storyline, configuration du quiz, bibliothèque de 115 médias avec tailles et durées, table des chaînes de caractères françaises et variables du lecteur.

Ce que cela permet :

- **Une reproductibilité totale.** Un formateur ou un développeur peut auditer, corriger et republier le module sans intervenir sur le serveur : les textes sont dans le paquet, les médias sont dans la bibliothèque, les règles du quiz sont paramétrées.
- **Une chaîne de production standard pour l’équipe.** Storyline est un outil de production que les équipes de formation utilisent ; la maintenance ne demande pas de compétence web.
- **Une version datée et identifiée.** Le paquet indique une date de publication (29 octobre 2026) et un numéro de version du lecteur.

Ce que cela limite :

- **Le récit n’existe pas comme données structurées.** Les libellés de l’arbre de décisions n’existent que dans les transcriptions et les sous-titres ; il n’y a pas d’export structuré du graphe de décisions. Conséquence directe : ni l'analyste ni le commanditaire ne peuvent auditer automatiquement la cohérence des branches — ce que nous avons dû faire à la main, piste de sous-titre par piste de sous-titre.
- **Une dépendance mono-éditeur.** Aucun format ouvert ne permet de reprendre le contenu (par exemple en SCORM ou en CM5, ou avec un export structuré des branches).
- **Un paramétrage par défaut « en.programmation ».** Les réglages du lecteur sont ceux du produit, non ceux du projet : sous-titres désactivés, texte accessible désactivé, zoom automatique désactivé, xAPI désactivé. C’est la cause racine de plusieurs réserves des sections 4.4, 4.5 et 4.6.

### 4.3 Poids total, budget de bande passante : le point faible majeur

L’inventaire des 115 médias du paquet exporté donne le tableau suivant.

| Type de média | Nombre | Poids total | Part du paquet | Durée cumulée |
|---|---:|---:|---:|---:|
| GIF animés | — (majorité des 37 médias restants) | ≈ 107,8 Mo | **66 %** | — |
| Vidéos MP4 | 16 | 45,5 Mo | 28 % | ≈ 3 min 30 s |
| Pistes audio MP3 | 62 | ≈ 0,8 Mo | 0,5 % | ≈ 3 min 40 s |
| Images PNG | — | ≈ 1,7 Mo | 1 % | — |
| Scripts, styles, polices | — | ≈ 7 Mo | 4 % | — |
| **Total** | **115 médias** | **≈ 162,8 Mo** | **100 %** | **≈ 7 min 11 s** |

Le rapport entre le poids et la durée parle de lui-même : **environ 23 Mo par minute de jeu**. Le contenu narratif, lui, est remarquablement léger : les 62 pistes audio de narration pèsent ensemble moins de 1 Mo.

Ce sont donc les **GIF animés décoratifs** qui coûtent le prix. Dans une classe burkinabè — connexion partagée, Mobile Money pour les données, ordinateur portable ancien — ce poids produit trois effets :

1. **Une attente à l’ouverture.** Les premiers écrans arrivent, puis la page « patine ». L’apprenant, qui est adolescent et sur téléphone, ferme.
2. **Un coût pour l’apprenant.** Selon les forfaits, 160 Mo de téléchargement sont significatifs pour une famille. Le risque social est réel : la friction financière d’un module gratuit est une barrière d’accès.
3. **Une projection collective fragile.** En classe, l’enseignant projette ; si la connexion est coupée en cours de séance, la séquence en cours est perdue.

La parade est simple et peu coûteuse : convertir les GIF en **vidéos MP4 (ou WebM) de courte durée**, ou en **images fixes** quand l’animation n’apporte rien ; contrôler la résolution (les GIF exportés sont souvent en 1920 × 1080) ; active le chargement différé ; et **proposer le paquet SCORM en téléchargement** pour un usage hors ligne. L’objectif raisonnable est de passer sous **25 Mo**, sans aucune perte de sens pédagogique.

### 4.4 Performance, fluidité et adaptation mobile

Le moteur Storyline est **léger et entièrement client** : une fois le paquet chargé, la navigation, les décisions et le quiz s’exécutent dans le navigateur, sans appel serveur. C’est un point fort réel : la fluidité interactive ne dépend pas du réseau une fois le module ouvert.

Les réserves portent sur le chargement et sur l’affichage :

- **`zoomToFit` est à `false`.** Le module ne s’adapte pas automatiquement à la taille de la fenêtre ; sur téléphone, les diapositives sont vues à l’échelle d’un écran d’ordinateur, et la page doit proposer « Utiliser le zoom du navigateur ». Pour un public d’adolescents qui consultera massivement sur mobile, c’est un défaut d’usage.
- **Aucune adaptation au débit.** Il n’existe ni version allégée, ni « mode faible connexion », ni chargement progressif des médias : le paquet est monolithique.
- **Aucun budget de performance documenté** ni mesure de référence : le temps d’ouverture réel sur un réseau 3G ou 4G lent n’est pas documenté par le projet (ce qui est cohérent avec l’absence de suivi de la qualité de service).
- **Les GIF sont coûteux à décoder** sur les appareils d’entrée de gamme : plusieurs GIF animés peuvent tourner simultanément, avec un effet de saccade et une consommation de batterie élevée.

**Appréciation.** Le module est rapide *une fois chargé*, et c’est tout. La question n’est pas la fluidité mais le **temps d’entrée**. C’est le premier correctif technique à engager.

### 4.5 Accessibilité (RGAA / WCAG)

Le moteur sait faire ; le paramétrage du projet ne l’a pas demandé. C’est le constat le plus facile à corriger et l’un des plus rentables.

| Critère | Constat vérifié | État | Référence |
|---|---|---|---|
| Sous-titres de l’audio et de la vidéo | 78 pistes de sous-titres existent (16 transcriptions + 62 sous-titres) mais `displayCaptions = false` : l’apprenant ne les obtient pas | **Non conforme** | WCAG 1.2.2 (A), RGAA 8.8 |
| Texte accessible (alternative au lecteur) | `accessibleText = false`, alors que le bouton « Fonction Texte accessible » figure dans l’interface | **Non conforme** | WCAG 1.1.1 / 4.1.2, RGAA 8.1 |
| Descriptions alternatives des images | Attributs `altText` présents sur les images | Conforme | WCAG 1.1.1 |
| Navigation au clavier | `tabIndex` et `accType` renseignés, raccourcis clavier documentés dans le lecteur | Conforme | WCAG 2.1.1, RGAA 8.7 |
| Contraste des textes | Libellés en #7A7A7A sur fond #212121, soit ≈ 3,2:1, sous le seuil de 4,5:1 | **Insuffisant** | WCAG 1.4.3 (AA) |
| Langue de la page | Localisation française du lecteur, attribut de langue présent | Conforme | WCAG 3.1.1 |
| Zoom et redimensionnement | Zoom navigateur disponible, mais pas d’ajustement automatique au viewport | Partiel | WCAG 1.4.4 / 1.4.10 |
| Animation et photosensibilité | Aucune commande de pause des animations, aucun traitement du réglage système « réduire les animations » | **Non traité** | WCAG 2.3.3 |
| Description audio des séquences | Absente : les informations clés des séquences sont portées par la narration | **Non conforme** | WCAG 1.2.5 (AA) |
| Absence de chronomètre | Le module et le quiz ne sont pas chronométrés | Conforme (avantage) | WCAG 2.2.1 |

**Appréciation.** Un élève sourd ou malentendant, ou un élève dont le poste est en library, se voit privé de l’essentiel du message : ce module repose sur la narration et l’animation. Réparer cet axe ne coûte presque rien (deux réglages), et il change la nature du produit : il ne s’adresse plus seulement aux élèves qui ont des écouteurs dans un bureau.

### 4.6 Interopérabilité avec un LMS et traçabilité des apprentissages

Le module est **techniquement prêt pour un LMS et pratiquement non connecté**. Le manifeste SCORM 1.2 est présent et valide (lancement `index_lms.html`), mais la page du site embarque `story.html`, c’est-à-dire la version **web**, hors session LMS.

| Fonctionnalité | État dans le module | Conséquence pour l’enseignant |
|---|---|---|
| Session LMS (SCORM 1.2) | Non ouverte par le site | Aucune donnée d’apprentissage envoyée au LMS |
| Remontée du score (`cmi.core.score`) | Sans objet sans session | L’enseignant ne sait pas qui a réussi |
| Suivi de progression (`cmi.core.lesson_status`) | Sans objet sans session | Pas de reprise de session entre élèves ou entre postes |
| xAPI | `lrsEnabled = false` | Aucune trace d’activité exploitable en analyse fine |
| Réinitialisation du quiz | `resettype = all`, `submitunanswered = all` | Comportement cohérent pour un quiz de maîtrise |
| Verrouillage des réponses | Choix verrouillés après la première tentative | Empêche la correction « au fil de l’eau » ; cohérent avec un seuil de réussite |
| Reprise après échec | Écran de résultats avec relance (« Reboot ») | Boucle de réessai possible, mais sans trace ni différenciation |

Conséquence générale : **le module ne sait rien de ses utilisateurs**. C’est acceptable pour une consultation individuelle, et temporairement inacceptable pour un dispositif de formation piloté : on ne peut ni regrouper les résultats, ni identifier les acquis, ni adapter le suivi, ni restituer une attestation.

**Appréciation.** L’activation du SCORM (ou, à défaut, d’un petit appel de remontée de score) est l’un des deux ou trois chantiers les plus rentables du projet : le travail technique est déjà fait par l’éditeur.

[[PAGEBREAK]]
### 4.7 Robustesse, reprise, gestion d’erreur et fonctionnement hors ligne

Le lecteur est **robuste sur le plan du réseau** : il détecte la perte de connexion, affiche un message de reconnexion et réessaie. Ce message existe dans une version française dans le paquet lui-même ; la coquille du site affiche encore une formule anglaise (« You are offline. Trying to reconnect… »), trace d’une localisation incomplète des éléments de l’interface.

Sur le plan pédagogique, la logique de reprise est cohérente avec l’objectif de maîtrise : les réponses sont **verrouillées après la première tentative**, les questions sans réponse sont soumises (`submitunanswered: all`), le quiz peut être réinitialisé intégralement (`resettype: all`), et un écran de résultats invite à recommencer.

Trois faiblesses subsistent :

- **Aucune reprise de session.** Le module ne mémorise pas la progression dans un stockage durable ni dans un LMS : un élève qui ferme l’onglet ou change de poste repart de zéro. Sur un réseau scolaire instable, c’est la règle, pas l’exception.
- **Aucun point de contrôle intermédiaire.** Les séquences ne sont pas sauvegardées une à une ; il n’y a pas de « reprise à la dernière scène ».
- **Une impasse de navigation.** Le module se termine sur une diapositive de relance (« Reboot ») : l’apprenant qui a terminé tourne en boucle tant qu’il ne ferme pas l’onglet, et n’est jamais invité à consulter la section « Ressources » de la page, pourtant prévue par la plateforme. Un module qui ne sait pas se terminer est un module qui prolonge l’écran sans véritable issue.

### 4.8 Confidentialité, données personnelles et sécurité

Le module **ne collecte rien** : pas de compte, pas de nom, pas de cookie de suivi, `xapi.lrsEnabled = false`, aucune remontée vers un LRS. C’est une **protection des données par défaut** et un point fort réel, particulièrement pour un dispositif scolaire de masse : aucun élève n'est exposé à une collecte.

Les réserves sont organisationnelles :

- **Aucune politique de confidentialité repérée** sur le site, alors que le dispositif héberge des contenus de santé de la reproduction et d’éducation sexuelle et qu’il s’adresse à des mineurs.
- **Aucun chemin de traitement nominatif** : si le commanditaire souhaite un suivi individuel (attestation, remédiation), il n’existe aujourd’hui ni fonction technique ni cadre déclaratif. C’est aussi un frein à l’appropriation par les enseignants, qui ne peuvent pas savoir qui a fait le module.
- **Un flux externe** : la plateforme intègre une vidéo de présentation hébergée hors du site (Microsoft Stream). Elle expose l’adresse IP et les cookies des visiteurs à un tiers, sans nécessité pédagogique pour le module lui-même. Dans un établissement équipé d’un filtrage réseau strict, c’est un obstacle technique supplémentaire.

**Appréciation.** Ne rien collecter est une excellente décision par défaut. Elle doit maintenant être **formalisée** (page de confidentialité, mention « aucune donnée personnelle collectée », contrat de sous-traitance si des données nominatives sont ajoutées plus tard).

### 4.9 Qualité de la langue et de l’édition

La langue du module est **orale, directe, courte** : c’est un choix réussi pour l’âge, et l’une des raisons de l'efficacité du module. Le vocabulaire employé reste accessible, les phrases sont courtes, le rythme est rapide.

Mais l’édition n’a pas été relue. Les défauts relevés (dans les sous-titres comme dans les textes de branchement) sont concentrés sur des **messages porteurs**, ce qui augmente leur impact :

| Formulation relevée | Localisation | Problème | Correction proposée |
|---|---|---|---|
| « repasser le cuis » | Narration, séquence 2 | Mot inexistant, manifestement une troncature ou une faute de frappe | Reprendre la phrase d’origine et la réécrire |
| « bouton de marque » | Interface ou narration | Erreur lexicale ; contexte probable : le bouton de démarrage | « bouton de démarrage » |
| « de ne pas rester **seule** » | Feedback de la question 2 | Accord en genre : le sujet est Moussa, masculin | « de ne pas rester **seul** » |
| « Parle lui sans le juger et encourage **le** à demander de l’aide » | Branche D4 | Ponctuation et trait d’union ; tournure maladroite | « Parle-lui sans le juger et encourage-le à demander de l’aide » |
| « **ses** leçons » | Item 1 du quiz | Le contenu porte sur les leçons de l’apprenant : « ses » doit être « **tes** » ou « tes » | « tes leçons » |
| « **Vrai ou faux.** » | Écran d’introduction du quiz | Ponctuation déclarative là où il faut une question | « Vrai ou faux ? » |
| « **Que va conseiller Moussa.** » | Libellé de la branche D4 | Même problème de ponctuation | « Que va conseiller Moussa ? » |
| Personnage « **Moussard** » | Grand frère de Moussa | Prénom plausible mais très proche de « Moussa » ; confusion probable chez les plus jeunes | Conserver, mais distinguer explicitement les deux personnages à l’oral |

Deux observations complémentaires :

- **Registre de langue.** Le module tutoie l’apprenant dans certains retours et vouvoie l’adulte dans d’autres. Dans une classe, l’élève s’adresse à l’enseignant avec « vous » ; le module devrait être cohérent et **expliciter le tutoiement** au début (« dans la fiction, on se tutoie »).
- **Absence de glossaire et de niveau de langue.** Aucun lexique, aucune indication de niveau (A1/A2/B1) : c’est un manque pour les élèves non francophones ou en difficulté de lecture.

### 4.10 Qualité audiovisuelle

Le module est **entièrement doublé en français** : 62 pistes audio de narration, 16 vidéos, environ 7 minutes 11 s de médias. C’est un atout rare et décisif dans le contexte burkinabè, où les niveaux de lecture sont très inégaux et où la lecture silencieuse n’est pas toujours possible (salle bruyante, matériel partagé, téléphone personnel). Un élève qui ne lit pas correctement peut suivre le module.

| Critère | Constat | Appréciation |
|---|---|---|
| Couverture sonore | Narration intégrale, dialogues incarnés | **Excellent** |
| Registre | Langue courante, phrases courtes, ton non moralisateur | **Bon** |
| Cohérence des voix | Plusieurs voix pour les personnages, stables sur l’ensemble | Bon |
| Style visuel | Personnages dessinés/animés, pas de photographie | **Bon** : évite l’image de l’enfant africain victime et les clichés de la pauvreté |
| Encodage des GIF | GIF animés haute définition pour des usages décoratifs | **À corriger** (poids, §4.3) |
| Sonorité de la vidéo | MP4 de qualité correcte, codecs standards | Bon |
| Description audio | Absente | À corriger (§4.5) |
| Sous-titres | Présents mais non proposés par défaut | À corriger (§4.5) |

### 4.11 Métadonnées et cohérence entre l’annonce et le contenu

C’est le point de contact le plus visible par l’utilisateur final, et il est en défaut.

| Élément annoncé | Élément réel | Écart |
|---|---|---|
| « Quizz **8 questions** » (fiche de la plateforme) | Quiz de **5 items** (notés 10 points chacun) | **Écart de 3 items** : l’utilisateur peut croire le module incomplet |
| « Thème 7 **Violences et addictions** » | Le module ne traite que l’addiction, la « drogue » générique | **Écart majeur de contenu** : aucun mot « violence » dans les 78 pistes de sous-titres |
| « Durée 10 min » | ≈ 7 min 11 s de médias + quiz | Cohérent |
| « Niveau **Apprenant** » | Un seul niveau pour les 9 modules, sans différenciation | À revoir : un module de prévention gagnerait à proposer deux niveaux (initiation / approfondissement) |
| Section « Ressources » sur la page | Le module n’y renvoie jamais | **Manque de monetisation** : la ressource de sortie n’est pas exploitée |
| Version / date de mise à jour | Présente dans le paquet, invisible pour l’apprenant | Manque : afficher « mis à jour le … » sur la page |
| Description détaillée de la page | Renvoie au module, sans préciser son périmètre réel | Manque : annoncer « module d’introduction sur la pression des pairs » |

**Appréciation.** Un module peut être excellent et néanmoins mal décrit. Ici, la fiche de la plateforme promet plus que le module ne tient, et cette dissonance décourage l’enseignant qui lit avant de projeter. La correction est rédactionnelle, pas technique, mais elle est indispensable.

### 4.12 Grille de notation technique pondérée

| Critère | Note / 10 | Poids | Commentaire |
|---|---:|---:|---|
| Architecture, hébergement, sécurité du transport | 8 | 8 % | Standard SCORM, Cloudflare, HSTS, Brotli, ETag, message hors-ligne traduit |
| Moteur et chaîne de production | 8 | 7 % | Storyline 360, version datée, paquet intégralement auditable |
| Poids et budget de bande passante | 3 | 20 % | 162,8 Mo, 66 % en GIF ; bloquant en usage scolaire et mobile |
| Performance, fluidité, adaptation mobile | 4 | 8 % | Moteur léger, mais pas de mode « réseau faible » ni d’ajustement au viewport |
| Accessibilité (RGAA / WCAG) | 4 | 18 % | Base technique solide, fonctions désactivées, contraste insuffisant |
| Interopérabilité LMS et traçabilité | 4 | 10 % | SCORM produit mais non utilisé ; xAPI désactivé ; aucun reporting |
| Robustesse, reprise, gestion d’erreur | 7 | 7 % | Reprise, réessai, réinitialisation ; pas de sauvegarde de progression |
| Qualité de la langue et de l’édition | 5 | 6 % | Oral juste et adapté, mais coquilles sur des messages clés |
| Qualité audiovisuelle | 6 | 8 % | Doublage intégral et personnages dessinés ; encodage trop lourd |
| Métadonnées et cohérence annonce/contenu | 5 | 8 % | « 8 questions » et « violence » non conformes au module |
| **MOYENNE PONDÉRÉE** | **4,9** | 100 % | **Correct sur le fond, perfectible sur la forme ; deux réserves lourdes (poids, accessibilité)** |

*Les pondérations reflètent le contexte d’usage visé : usage scolaire de masse, sur réseau contraint, en projection ou sur mobile. Sur un usage individuel sur ordinateur de bureau bien connecté, la moyenne remonterait d’environ un point. Corriger le poids, l’accessibilité et la remontée SCORM ferait passer la note de 4,9 à environ 6,5 sans toucher au contenu.*

[[PAGEBREAK]]
## 5. Analyse de la valeur et de la qualité éducative

### 5.1 Intention, public cible et cohérence d’ensemble

L’intention du module est explicite : **sensibiliser par l’expérience**, en plaçant l’apprenant dans la situation plutôt qu’en lui délivrant un cours. Cette intention est lisible dans le code même du module (des branches, des conséquences, un quiz final) et elle est **cohérente avec le dispositif SDSR**, dont le document de référence présente les contenus thématiques « adaptés aux jeunes et adolescent·e·s à digitaliser ».

Le public visé est cohérent avec le format : **≈ 10 minutes**, un niveau unique « Apprenant », un contenu entièrement oral. Dans une séance de 45 à 55 minutes, le module occupe un cinquième du temps — une proportion qui laisse la place au débat, qui est précisément le moment où la prévention agit.

| Dimension | Appréciation | Commentaire |
|---|---|---|
| Clarté de l’intention | **Bonne** | Prévenir par l’expérience ; le module ne s’annonce jamais comme un cours |
| Adéquation à l’âge (15 ans) | **Bonne** | Durée, langue, longueur des dialogues,des sujets proches de leur quotidien |
| Cohérence interne | **Très bonne** | Un seul fil narratif, un seul personnage principal, aucune dispersion |
| Cohérence avec le dispositif | **Partielle** | Le module ne couvre qu’une partie du Thème 7 annoncé (§5.3) |
| Cadrage pour l’enseignant | **Absent** | Aucun prérequis, aucun objectif opérationnel, aucune consigne d’animation |
| Différenciation | **Absente** | Un seul niveau pour neuf modules ; pas de version « approfondissement » |

**Appréciation.** Le module est **bien pensé pour son âge** et **mal calibré pour son dispositif**. Il manque ce qui fait la différence entre un serious game et une séance de prévention : les objectifs affichés, le contrat pédagogique (ce que l’élève va faire et ce qu’il va apprendre), et la place de l’enseignant.

### 5.2 Exactitude scientifique et justesse des messages

Tout ce que le module affirme est **juste**. Le contenu a été relu avec attention sur le plan scientifique, et c’est un point fort à souligner, car beaucoup de supports de prévention en santé de la reproduction contiennent des approximations.

| Message du module | Verdict scientifique | Commentaire |
|---|---|---|
| « Les drogues peuvent aider à mieux mémoriser ses leçons et à devenir plus intelligent » → **Faux** | Exact | Idée reçue très répandue chez les jeunes ; l’item la démonte explicitement |
| Demander de l’aide à une personne de confiance est la première étape pour sortir d’une addiction | Exact | Formulation conforme aux bonnes pratiques |
| Rester dans un groupe qui incite à consommer complique l’arrêt | Exact | Mechanisme de renforcement social bien identifié |
| Une personne confrontée à une addiction doit être jugée et rejetée → **Faux** | Exact | Message anti-stigmatisation, central en prévention |
| Refuser clairement et s’éloigner résiste à la pression | Exact | Recommandation de référence |
| Reprendre la consommation peut remettre en difficulté le chemin parcouru | Exact | Le module admet la rechute sans dramatiser |

En revanche, **le module ne dit rien** de ce qui fait l’information utile :

- **Aucune donnée chiffrée** : ni prévalence d’usage, ni nombre de jeunes concernés, ni tendance. Un module de prévention qui ne donne aucun repère chiffré laisse le teenager sans matière pour situer le phénomène.
- **Aucun mécanisme** : ni comment agissent les substances, ni dépendance physique et psychologique, ni syndrome de sevrage.
- **Aucune conséquence physique** : pas de risque de surdosage, pas de dangers spécifiques, pas de mention des produits réellement accessibles localement.
- **Aucun produit nommé** : ni alcool, ni tabac, ni solvants, ni tramadol, ni cannabis — les substances que le document de référence présente (illustrations « L’alcool », « La cigarette », « L’inhalant et solvant », « Le cannabis », « Tramadol vendu dans la rue »).
- **Aucune source, aucun renvoi** : ni source sanitaire, ni « pour en savoir plus ».

**Appréciation.** Le module est irréprochable sur ce qu’il affirme et muet sur l’essentiel. Pour un public de 15 ans, un module qui ne nomme aucune substance identifiable et ne donne aucun chiffre a une conséquence perverse : l’apprenant sort en ayant compris le mécanisme de la pression, mais sans aucun savoir sur ce qui l|attendance.

### 5.3 Couverture du référentiel thématique : l’écart central

Le document de référence du dispositif consacre au **Thème 7 « Violences et addictions »** quatorze pages structurées en cinq rubriques (et sept sous-rubriques). La confrontation est explicite :

| Rubrique du référentiel (Enabel, décembre 2025) | Traitement dans le module | Couverture estimée |
|---|---|---:|
| **I. Définition des concepts** (addiction, dépendance, usage) | Aucune définition n’est donnée ; le module montre la situation, il ne nomme pas les concepts | **0 %** |
| **I bis. Caractéristiques communes des addictions** (critères de dépendance, tolérance, sevrage) | Les signes sont *montrés* dans le récit (changement de comportement, isolement) mais ne sont jamais nommés ni outillés | **20 %** |
| **II. Causes et facteurs de vulnérabilité** (alcool, drogue, tabac) | La pression des pairs est traitée ; aucun autre facteur (précarité, famille, déscolarisation, perte de repères) n’est évoqué | **25 %** |
| **III. Conséquences de la consommation** (alcool et tabac / drogue) | Conséquences relationnelles et sociales uniquement ; aucune conséquence physique, psychologique ou économique | **25 %** |
| **IV. Les différents types de drogues** (licites : alcool, tabac ; illicites : solvants, cannabis, tramadol) | Aucun produit nommé, la « drogue » reste générique | **0 %** |
| **V. Précautions à prendre** | Les cinq décisions du module *sont* des précautions appliquées ; mais aucune précaution n’est formulée comme consigne explicite | **60 %** |
| **VI. Violences physiques** | Aucun traitement | **0 %** |
| **VI bis. Violences psychologiques et morales** | Aucun traitement, malgré l mails de stigmatisation traité dans le module | **0 %** |
| **Couverture globale** | | **≈ 15 %** |

Le constat est vérifié piste par piste : sur les **78 fichiers de sous-titres** du paquet (16 transcriptions de vidéo et 62 sous-titres audio), **aucune occurrence** des mots « alcool », « tabac », « cigarette », « cannabis », « tramadol » ou « violence » ; le seul terme employé est le mot générique « drogue ».

**Appréciation.** C’est l’écart le plus lourd du rapport, et il ne s’agit pas d’une question de quantité mais de **nature**. Le module ne peut pas prétendre couvrir le Thème 7 : il traite un **chapitre** de ce thème (la pression des pairs autour d’une substance non identifiée). Deux solutions s’offrent au commanditaire : soit renommer et repositionner le module (« La pression des pairs »), soit l’enrichir pour couvrir le thème annoncé. La seconde est préférable, mais elle est un projet, pas une correction.

### 5.4 Scénarisation, engagement et qualité des personnages

La scénarisation est **le point fort du produit**, et de loin.

- **Un personnage unique et identifiable.** Moussa, 15 ans, ni victimisation ni caricature ; l’apprenant s’identifie à lui parce qu’il tient sa place dans le récit plutôt que d’y assister.
- **Une durée d’écran maîtrisée.** Les dialogues sont courts, les plans courts, l’interaction arrive vite : la rétention est réelle.
- **Des situations socialement plausibles.** La proposition au groupe, la honte, le remords, la tentation du « je ne prends plus rien mais je reste » : ce sont des situations que les élèves de 15 ans reconnaissent.
- **Un procédé rare et efficace : l’inversion des rôles.** Dans la séquence 3, Moussa n’est plus le consommateur mais celui qui constate la dépendance de son grand frère. Le module fait ainsi passer l’apprenant du « comprendre » au « faire conseil », et lui fait découvrir l’enjeu de la stigmatisation de l’intérieur.

Trois réserves :

- **Aucun personnage féminin.** Pour un module de prévention d’un dispositif consacré à la santé de la reproduction et à la santé sexuelle, l’absence totale de fillette ou d’adolescente est une lacune de représentation, d’autant que la stigmatisation de la « toxicomanie » est particulièrement genrée et que les filles de 15 ans sont les premières visées par les sollicitations.
- **Un adulte qui n’est pas un personnage.** L’adulte qui propose son aide n’a ni nom, ni visage, ni statut (parent ? enseignant ? soignant ? agent de santé ?). Or c’est exactement le personnage que l’élève de 15 ans doit pouvoir appeler : le message « parle à quelqu’un de confiance » reste suspendu tant que ce « quelquien » n’existe pas dans la fiction.
- **Aucun repère de lieu, de classe, de pays.** Le module pourrait se passer n’importe où. L’ancrage local n’est pas un détail esthétique : il détermine l’identification.

### 5.5 Les points de décision : un véritable arbre de conséquences

C’est la découverte la plus importante de l’analyse narrative, et elle valorise fortement le module. Les séquences ne sont pas de simples diaporamas : ce sont **cinq points de décision** successifs, chacun suivi d’une **conséquence explicitement énoncée** à l’apprenant.

| # | Question posée à l’apprenant | Options | Conséquence énoncée par le module |
|---|---|---|---|
| **D1** | *Que va faire Moussa ?* (après la proposition du groupe) | **Accepter** « Bon, juste une fois. » · **Refuser** « Non merci, je ne veux pas essayer. » | *Accepter* → « Ils restent avec eux et acceptent finalement. » · *Refuser* → « Il s’éloigne et refuse de céder à la pression. » / « Refuser une drogue permet d’éviter de commencer une consommation qui peut devenir difficile à arrêter. » |
| **D2** | L’adulte propose son aide | **Accepter** « Oui, j’ai un problème, je voudrais en parler avec vous. » · **Refuser** « Non, tout va bien, je vais régler ça tout seul. » / « Je peux arrêter tout seul, je n’ai pas besoin d’aide. » | *Accepter* → « Accepter un accompagnement permet à Moussa de ne pas rester seul face à son problème et de commencer une démarche pour sortir de la consommation. » · *Refuser* → « Cacher le problème ne permet pas de le résoudre. » / « Vouloir s’en sortir est important, mais refuser l’aide peut rendre la démarche plus difficile. » |
| **D3** | Le groupe revient à la charge | **Modérer** « Je vais continuer à les fréquenter, mais je ne prendrai plus rien. » · **Rompre** « Non merci, je ne veux plus consommer. » / « Je vais accepter l’aide et suivre les conseils qu’on me donne. » | *Modérer* → « Éviter les mauvaises fréquentations peut aider Moussa à ne pas retomber dans la consommation. » / « Reprendre la consommation peut remettre en difficulté le chemin parcouru. » · *Rompre* → « Face à une proposition, il est important de savoir dire non et de s’éloigner. » |
| **D4** | *Que va conseiller Moussa ?* (à propos de son grand frère Moussard) | **Stigmatiser** « Laisse-le se débrouiller, c’est son problème. » · **Soutenir** « Parle-lui sans le juger et encourage-le à demander de l’aide. » | *Stigmatiser* → « Ignorer le problème peut laisser la personne seule face à ces difficultés ; il est possible de l’encourager à chercher de l’aide. » · *Soutenir* → « Écouter, conseiller et orienter vers une personne de confiance peut aider une personne confrontée à une addiction. » |
| **D5** | Proposition de reconsommation | « D’accord, juste pour une dernière fois. » | La rechute est montrée comme une **issue possible** : le module admet que l’on peut fléchir, et en montre le coût. |

Deux qualités remarquables en découlent et doivent être soulignées :

- **La décision D3 est la plus fine du module.** L’option « je continue à les fréquenter, mais je ne prendrai plus rien » est un **piège pédagogique classique**, et il est très bien construit : c’est la solution rassurante que choisissent beaucoup d’adolescents (on garde le groupe, on lâche la substance), et le module en montre le coût (« reprendre la consommation peut remettre en difficulté le chemin parcouru ») sans jamais la caricaturer. De même, D4 offre un choix social entre stigmatisation et soutien, à un âge où la « fidélité » au groupe est déterminante.
- **Le module admet l’erreur et la rechute** (D5, « juste pour une dernière fois »). Il ne construit pas un héros exemplaire : il construit un adolescent qui peut fléchir. C’est une exigence de réalisme en prévention, et cela détermine la qualité de l’identification.

**Appréciation.** La structure est exemplaire pour l’âge : sur le plan narratif et pédagogique, le module fait mieux que la plupart des supports de prévention courts produits en Afrique de l’Ouest. Elle justifie à elle seule une note élevée sur la scénarisation.

### 5.6 Interactivité et qualité des feedbacks

L’interactivité réelle du module est **concentrée et dense** : cinq décisions de scénario et cinq items de quiz, chacun suivi d’un retour écrit et argumenté. La qualité des feedbacks est **au-dessus de la moyenne** : ce ne sont pas des messages de notation automatique (« Faux. »), mais des explications qui sont argumentées.

| Élément | Constat | Appréciation |
|---|---|---|
| Retour sur décision de scénario | Conséquence énoncée, mais **aucun feedback évaluatif** : le module ne dit pas si le choix était bon | **Faiblesse majeure** : l’apprenant peut suivre le « mauvais » chemin sans le savoir |
| Retour sur item de quiz | Un texte spécifique par item, juste et incorrect, qui explique le raisonnement | **Très bon** |
| Retour sur l’échec au seuil | Écran de résultats avec le score obtenu et le seuil, puis relance | Correct, mais sans différenciation |
| Nombre de points d’interaction | 10 sur ≈ 7 minutes de médias | Correct ; le module n’est pas un « lecteur de diaporama » |
| Adaptation au profil | Aucune : tous les apprenants suivent le même parcours, les mêmes items | Manque |
| Répétition espacée | Aucune | Manque |

Le point le plus important de cette section est la **première ligne du tableau**. Dans un serious game, la conséquence d’une décision doit à la fois **informer** et **évaluer** : « si tu fais cela, il arrivera ceci » ne suffit pas si l’apprenant ne sait pas si « cela » est une bonne ou une mauvaise chose. Ici, la conséquence est toujours narrée au positif ou au négatif, mais jamais évaluée explicitement, et **aucun score n’est associé aux décisions de scénario** : le seul score vient du quiz final. Un apprenant peut donc faire les cinq choix les plus discutables, obtenir 5/5 au quiz, et sortir avec le sentiment d’avoir réussi.

**Appréciation.** C’est le correctif pédagogique le plus rentable du module : **une simple ligne de score et un libellé de validation par branche** (« choix prudent » / « choix risqué ») suffiraient à transformer l’expérience.

### 5.7 Qualité de l’évaluation : items, feedbacks et psychométrie

Le quiz comporte **5 items** vrai/faux, notés **10 points** chacun, avec un seuil de réussite de **80 %** (soit 4 items sur 5). Les énoncés et les feedbacks sont reproduits en annexe A.

| # | Énoncé (extrait) | Réponse | Ce que l’item mesure réellement | Niveau (Bloom) |
|---|---|---|---|---|
| Q1 | « Les drogues peuvent aider à mieux mémoriser ses leçons et à devenir plus intelligent. » | Faux | Restitution d’un message / une idée reçue | 1-2 |
| Q2 | « Demander de l’aide à une personne de confiance… première étape pour sortir d’une addiction. » | Vrai | Restitution d’un message | 1-2 |
| Q3 | « Continuer à fréquenter des camaraderie qui incitent à consommer ne présente aucun risque… » | Faux | Jugement, mais sans application | 2 |
| Q4 | « Une personne confrontée à une addiction doit être jugée et rejetée… » | Faux | Valeur : anti-stigmatisation | 2 |
| Q5 | « Face à une proposition de drogue, refuser et s’éloigner… » | Vrai | Restitution d’un message | 1-2 |

**Analyse psychométrique.**

- **La réussite au hasard est de 18,75 %.** Avec un seuil à 80 % (4/5) et un format binaire, un apprenant qui répond au hasard atteint le seuil avec une probabilité de 6/32 ≈ 18,75 %. Le seuil ne peut donc pas être atteint « par accident » à chaque fois, mais un dixième environ des élèves non informés passera l’épreuve — et l’enseignant n’en saura rien.
- **La note majoritaire est une restitution.** Trois items sur cinq (Q1, Q2, Q5) se contentent de vérifier que l’apprenant a compris un message du module. Or **la compétence visée par le module — résister à la pression — est une compétence d’application** : elle ne peut pas être vérifiée par une question de compréhension. C’est le décalage le plus discutable de l’ensemble du dispositif.
- **Un item est en tension avec le scénario.** Q3 affirme que « continuer à fréquenter des camarades qui incitent à consommer ne présente aucun risque » est faux. Or la branche D3 enseigne précisément une **nuance** : l’option « je reste avec eux mais je ne prends plus rien » est un piège dont le coût est énoncé. Un apprenant qui a compris D3 peut hésiter sur un item qui, lui, simplifie. Le quiz et le scénario ne parlent pas tout à fait la même langue.
- **Aucun item n’évalue les branches.** Sur les cinq points de décision, aucun n’est repris en question : ce que le module a montré n’est jamais mesuré.
- **Aucun item de niveau supérieur.** Ni application à une situation nouvelle, ni comparaison, ni priorisation, ni mise en œuvre d’une stratégie de résistance en contexte.
- **Le format est trop étroit.** Un vrai/faux à cinq items ne permet ni distracteurs, ni analyse d’erreurs fines, ni progressivité de difficulté.

**Recommandations minimales (voir §6, actions 7 à 9).** Passer à 8 à 10 items mêlant vrai/faux et QCM ; ajouter **deux items d’application** du type « Un camarade te propose… que fais-tu ? » et « Ton cousin consomme… que lui dis-tu ? » ; **un item reprenant explicitement une conséquence de branche** (D2 ou D4) ; abaisser le seuil à 70 % ; et surtout, **associer un score et une validation aux décisions de scénario**.

[[PAGEBREAK]]
### 5.8 Alignement sur les compétences visées et taxonomie de Bloom

Le module ne déclare pas ses objectifs, mais ils sont reconstructibles à partir du référentiel et du scénario : **résister à la pression des pairs**, **demander de l’aide**, **ne pas stigmatiser**, **soutenir un proche**. Ce sont des compétences psychosociales, précisément celles que le dispositif SDSR cherche à développer chez les jeunes et adolescents.

L’analyse montre un **décalage net entre ce qui est développé et ce qui est évalué**.

| Compétence visée | Niveau atteint dans les séquences | Niveau réellement évalué par le quiz | Écart |
|---|---|---|---|
| Résister à la pression | **Application / analyse** (Bloom 3-4) : l’apprenant décide, arbitre, subit la conséquence (D1, D3, D5) | **Compréhension** (Bloom 2) : Q5 vérifie qu’il a compris le message « refuser et s’éloigner » | **Majeur** |
| Demander de l’aide | **Application** (D2 : accepter ou refuser l’accompagnement) | **Mémorisation** (Bloom 1) : Q2 | Majeur |
| Ne pas stigmatiser | **Analyse** (D4 : stigmatiser ou soutenir) | **Compréhension** (Bloom 2) : Q4 | Modéré |
| Connaître les consequences de la consommation | **Compréhension** (les conséquences sont montrées et nommées) | **Mémorisation** (Bloom 1) : Q1 | Faible |
| Identifier les produits et les risques | **Non développé** (aucun produit nommé) | **Non évalué** | Total |

Autrement dit : **le module fait travailler l’application et l’analyse ; le quiz mesure la compréhension et la mémorisation.** Un élève peut avoir parfaitement intégré la logique des cinq décisions et échouer parce qu’il ne se souvient plus de la formulation exacte d’un message ; symétriquement, un élève qui a mémorisé les cinq messages peut réussir le quiz sans avoir jamais été capable de dire non dans la cour.

Deux remarques complémentaires :

- **Les compétences ne sont jamais nommées pour l’apprenant.** Le module ne dit pas « tu vas apprendre à dire non » ni « tu vas apprendre à aider ». Expliciter l’objectif (une phrase, en ouverture) augmente la motivation et rend l’évaluation lisible.
- **La taxonomie de Bloom n’est pas outillée.** L’absence d’items de niveau 3-4 ne vient pas d’un choix explicite mais d’un paramétrage par défaut : le quiz est « 5 questions à choix binaires », format imposé par l’outil plus que par la pédagogie.

### 5.9 Adéquation au contexte burkinabè pour des élèves de 15 ans

C’est le second angle mort du module, après la couverture thématique.

| Dimension | Constat | Appréciation |
|---|---|---|
| Langue et registre | Oral, direct, phrases courtes, tutoiement | **Très adapté** |
| Noms des personnages | « Moussa », « Moussard » : plausibles et ancrés | **Adapté** |
| Durée | ≈ 10 min, compatible avec une séance | **Adapté** |
| Absence de repère local | Aucun lieu, aucune classe, aucun pays identifiable | À corriger |
| Produits et substances | Aucun produit nommé, alors que le document de référence présente l’alcool, le tabac, les solvants, le cannabis et le tramadol | **Manque majeur** |
| Personnages | Aucune fille, aucun enseignant, aucun parent, aucun soignant identifié | **Manque notable** |
| Réalité économique | Aucune mention du coût de la consommation, du racket, de l’accès aux produits | Manque |
| Contexte scolaire | Aucun lien avec les programmes, les évaluations, l’année scolaire | Manque |
| Équité d’accès | 162,8 Mo : les élèves les mieux connectés sont les mieux servis | **Problème d’équité** |

Le point d’équité mérite d’être souligné parce qu’il relie les deux analyses : **le poids du module est un problème pédagogique**. En classe, ce sont les élèves dont le forfait de données est limité qui ne pourront pas terminer le module ; ce sont donc les plus exposés au risque qui sont les moins bien servis par l’outil.

Sur le fond, la situation burkinabè appelle un module qui nomme ce que les élèves de 15 ans rencontrent réellement : le **tramadol** et les **solvants** (colle, « l collisions »), l’**alcool** artisanal, le **tabac**, la **pression du groupe** et les **violences** entre pairs. Le module ne traite que la pression autour d’une « drogue » abstraite. Il reste dans le générique, là où la réalité est concrète.

**Appréciation.** Le module est **bien écrit pour des jeunes Burkinabè de 15 ans**, mais il n’est pas **écrit par et pour eux** : il transpose un scénario de prévention internationale dans un décor non nommé. Deux ajustements — un personnage féminin, une scène située (une cour de collège, un quartier) — rapprocheraient le module de son public à un coût très faible.

### 5.10 Utilisabilité pédagogique en classe

Un serious game destiné au collège n’est pas un produit fini : c’est un **support de séance**. Or le module arrive nu.

| Besoin de l’enseignant | État | Conséquence |
|---|---|---|
| Fiche d’animation (objectifs, déroulement, minutage) | **Absente** | L’enseignant improvise, donc l’exploitation varie d’une classe à l’autre |
| Questions de débriefing | **Absentes** | Le moment le plus utile (la discussion) n’est pas outillé, alors que le module contient une matière exceptionnelle pour l’alimenter |
| Consignes de gestion de groupe (individuel, collectif ou en binôme) | **Absentes** | Par défaut, chacun sur son écran, sans bénéfice pédagogique de l’interaction |
| Critères d’évaluation / grille | **Absents** | Le score du quiz n’est pas exploité |
| Remontée des résultats | **Aucune** | Impossible de suivre la progression d’une classe |
| Différenciation | **Aucune** | Le même parcours pour tous, y compris pour les élèves en difficulté de lecture |
| Activités de prolongement | **Aucune** | Pas de débat, pas de saynète, pas de recherche, pas de séance de suivi |
| Gestion de la panne réseau | **Non prévue** | Le paquet SCORM existe mais n’est pas proposé en téléchargement |
| Lien avec les autres modules | **Aucun** | Le module est un îlot : il ne renvoie ni au Thème 6 (violences sexuelles), ni au Thème 9 (pratiques traditionnelles néfastes) |

**Appréciation.** C’est le manque le plus coûteux en temps enseignant, et le plus facile à corriger : **une fiche d’animation d’une page** (trois objectifs, un minutage, trois questions de débriefing, une consigne de relance) transformerait un « serious game » en **séquence pédagogique**. Ce document est d’ailleurs l’objet du présent rapport.

### 5.11 Qualité de l’oral, du ton et de la langue

Le ton est le point fort de ce registre. Le module **ne moralise pas** : il ne dit jamais « il faut savoir dire non », il montre ce qui arrive. Il ne diabolise pas non plus l’adolescent : Moussa est un peer comme les autres, et l’adulte qui l’aide n’est pas présenté comme un autorité intrusive. C’est le ton juste pour 15 ans, et c’est ce qui permet au message anti-stigmatisation de passer.

Les réserves sont d’ordre linguistique et éditorial (le détail des coquilles est donné au §4.9) :

- **Registre incohérent** : le module tutoie dans certains retours et vouvoie dans d’autres. Il faut choisir et l’annoncer.
- **Mots clés non définis à l’écran** : « addiction », « dépendance », « sujet », « pression » ne sont pas expliqués ; pour un élève qui lit lentement, c’est un obstacle. Un micro-glossaire de cinq mots, affiché au moment opportun, suffirait.
- **Coquilles sur des messages porteurs** : l’accord « seule » pour un garçon, l’impératif mal ponctué, le pronom « ses » au lieu de « tes ». Sur un module de prévention, une coquille n’est pas qu’un défaut d’image : elle dévalue le message.
- **Aucune différenciation de vocabulaire** : le module parle à tout le monde avec les mêmes mots ; rien n’est proposé pour les élèves en difficulté.

### 5.12 Grille de notation pédagogique pondérée

| Critère | Note / 10 | Poids | Commentaire |
|---|---:|---:|---|
| Pertinence de l’intention et du ciblage | 7 | 8 % | Prévention pertinente, public et durée cohérents |
| Qualité scientifique et justesse des contenus | 6 | 8 % | Messages justes, mais aucune donnée, aucune source, aucun repère de santé publique |
| Couverture du thème de référence | 3 | 20 % | ≈ 15 % du contenu de référence ; 0 % du versant « violence », 0 % des produits nommés |
| Qualité de la scénarisation et de l’engagement | 8 | 15 % | Cinq points de décision, arbre de conséquences, rôle inversé, option-piège, rechute assumée |
| Interactivité et qualité des feedbacks | 7 | 9 % | Feedbacks explicatifs et argumentés ; mais aucune validation des décisions de scénario |
| Qualité de l’évaluation (items, feedback, psychométrie) | 4 | 15 % | 5 items vrai/faux, seuil à 80 %, 18,75 % de réussite au hasard, aucun item d’application |
| Alignement sur les compétences SDSR / psychosociales | 5 | 8 % | Compétences ciblées pertinentes, mais compétence clé (appliquer) non évaluée |
| Adéquation au contexte burkinabè (15 ans) | 5 | 8 % | Langue et durée adaptées ; pas de personnage féminin, pas de produits locaux, pas de cadre scolaire |
| Utilisabilité pédagogique en classe | 4 | 6 % | Aucun dispositif d’accompagnement, aucune fiche d’animation, aucun suivi |
| Qualité de l’oral, du ton et de la langue | 6 | 3 % | Oral et direct, sans moralisation ; coquilles et incohérences de registre |
| **MOYENNE PONDÉRÉE** | **5,3** | 100 % | **Module d’introduction de réelle qualité narrative ; à enrichir pour tenir la promesse du thème et pour servir l’évaluation d’un compétences** |

*Les pondérations pondèrent les deux écarts les plus lourds : la couverture du thème de référence (20 %) et la solidité de l’évaluation (15 %). Le module obtient 7,5 sur 8 aux critères de scénarisation, d’interactivité et de ton : sa faiblesse n’est pas la qualité de l’écriture, mais l’étroitesse du périmètre et l’absence d’instrumentation. En conservant la scénarisation et en traitant les six actions prioritaires du chapitre 6, la note pourrait approcher 7/10.*

### 5.13 Ce que le module ne fait pas — synthèse des manques

1. Il ne traite **aucune violence**, alors que c’est le premier mot de l’intitulé du thème.
2. Il ne nomme **aucun produit** : ni alcool, ni tabac, ni solvants, ni tramadol, ni cannabis.
3. Il ne donne **aucune donnée chiffrée** ni aucune source sur les produits et les risques.
4. Il ne **définit pas** les mots clés qu’il emploie (addiction, dépendance, pression).
5. Il ne **montre aucun adulte nommé** ni aucun relais concret vers l’aide.
6. Il ne **montre aucune fille** et aucune autre réalité que la sienne.
7. Il ne **propose aucun dispositif d’accompagnement** pour l’enseignant.
8. Il n’**évalue pas** les décisions que l’apprenant prend dans le scénario.
9. Il ne **trace rien** : ni progression, ni résultat, ni attestation.

[[PAGEBREAK]]
## 6. Plan d’amélioration priorisé (13 actions)

### 6.1 Vue d’ensemble

| N° | Action | Objectif | Mise en œuvre concrète | Priorité | Charge |
|---|---|---|---|---|---|
| 1 | **Alléger le paquet** | Passer de 162,8 Mo à moins de 25 Mo | Convertir les GIF animés en MP4/WebM ou en images fixes ; réduire la résolution ; charger les médias à la demande ; proposer le paquet SCORM en téléchargement pour un usage hors ligne | **1** | Faible |
| 2 | **Activer l’accessibilité** | Rendre le module utilisable par tous | Activer `displayCaptions` et `accessibleText` ; corriger les contrastes (≥ 4,5:1) ; proposer un gel des animations ; ajouter une description audio des séquences | **1** | Faible |
| 3 | **Aligner la description sur le contenu** | Supprimer la dissonance annonce/contenu | Corriger « 8 questions » → « 5 questions » ; reformuler la description de la page ; afficher la date de mise à jour ; annoncer explicitement le périmètre du module | **1** | Faible |
| 4 | **Relire la langue** | Éliminer les coquilles sur les messages porteurs | Corriger « repasser le cuis », « bouton de marque », « seule/seul », « encourage le », « ses/tes leçons », « Vrai ou faux. », « Que va conseiller Moussa. » ; uniformiser le registre (tutoiement ou vouvoiement) | **1** | Faible |
| 5 | **Réparer la fin du parcours** | Éviter l’impasse narrative | Ajouter un écran de fin qui renvoie explicitement à la section « Ressources » de la page et à l’enseignant, au lieu de la boucle « Reboot » | 2 | Faible |
| 6 | **Valoriser les décisions de scénario** | Faire de l’arbre de décision un vrai évaluateur | Associer à chaque branche D1–D5 un libellé (« choix prudent » / « choix risqué ») et un point ; afficher un bilan des décisions à l’écran de résultats | **1** | Moyenne |
| 7 | **Enrichir et recaler le quiz** | Mesurer la compétence visée | Passer à 8–10 items ; ajouter 2 items d’application (« un camarade te propose… que fais-tu ? ») et 1 item sur les conséquences de branche ; abaisser le seuil à 70 % ; vérifier qu’aucun item ne peut être réussi par déduction | **1** | Moyenne |
| 8 | **Créer la fiche d’animation enseignant** | Transformer le module en séquence pédagogique | Une page : objectifs, minutage, 3 questions de débriefing, 1 consigne de relance si un élève est en difficulté, grille d’observation, prolongements | **1** | Faible |
| 9 | **Activer la remontée des résultats** | Rendre le dispositif pilotable | Activer le SCORM 1.2 (lancer `index_lms.html`) ou mettre en place un envoi de résultat ; à défaut, prévoir un export/impression du score | 2 | Moyenne |
| 10 | **Nommer les produits réels** | Ancrer la prévention dans la réalité locale | Ajouter une séquence sur l’alcool, le tabac, les solvants et le tramadol, avec les risques spécifiques et les messages de refus adaptés à chaque produit | **1** (contenu) | Élevée |
| 11 | **Ajouter le versant « violence »** | Tenir l’intitulé du thème | Une séquence sur les violences physiques, psychologiques et morales, avec les formes, les witnessing et le rôle témoin ; à traiter dans le cadre du Thème 6 (violences sexuelles) pour éviter les doublons | **1** (contenu) | Élevée |
| 12 | **Diversifier les personnages et les relais** | Élargir l’identification et le « à qui parler » | Introduire un personnage féminin ; nommer l’adulte référent (enseignant, parent, agent de santé) et indiquer un relais concret ; distinguer nettement Moussa et Moussard | 2 | Moyenne |
| 13 | **Formaliser la protection des données et l’accès hors ligne** | Sécuriser le cadre | Publier une page de confidentialité précisant qu’aucune donnée personnelle n’est collectée ; proposer le téléchargement du paquet SCORM pour les classes sans réseau | 2 | Faible |

### 6.2 Séquencement recommandé

| Horizon | Actions | Effet attendu |
|---|---|---|
| **0 – 3 mois** (correctifs légers, sans refonte) | 1, 2, 3, 4, 7, 8 | Note technique de 4,9 à ≈ 6,2 ; note éducative de 5,3 à ≈ 6,0 ; le module devient utilisable en classe dès la rentrée |
| **3 – 9 mois** (améliorations structurelles) | 5, 6, 9, 12, 13 | L’arbre de décision devient évaluatif ; les résultats sont exploitables ; le module s’utilise en pilote encadré |
| **9 – 18 mois** (contenu) | 10, 11, puis version « approfondissement » | Le module tient la promesse du thème ; la plateforme gagne un niveau de différenciation |

### 6.3 Les six actions prioritaires, en une phrase chacune

1. **Convertir les GIF en vidéos** : c’est le geste le plus rentable du projet, il fait gagner 130 Mo sans toucher au scénario.
2. **Activer les sous-titres et le texte accessible** : deux réglages, et le module cesse d’exclure une partie des élèves.
3. **Corriger la fiche de la plateforme** : « 5 questions », description honnête, date de mise à jour.
4. **Écrire la fiche d’animation** : une page qui transforme un jeu en séance de prévention.
5. **Ajouter deux questions d’application et un item de branche** : pour que le quiz mesure enfin ce que le module fait travailler.
6. **Nommer les produits et ajouter un personnage féminin** : pour que le module parle la langue du Burkina Faso.

## 7. Conclusion

Le module **Thème 7 — Violence et addiction** est un **bon produit narratif dans un mauvais produit pédagogique**, et c’est précisément ce que la présente analyse permet d’affirmer.

Ce qui est acquis et solide : une architecture technique professionnelle, une chaîne de production reproductible, un doublage intégral, un ton juste, et surtout un **arbre de décisions à cinq branches avec conséquences explicites** — rare dans le paysage de la prévention en santé de la reproduction. Un module qui fait vivre des moments de choix, qui montre l’option-piège du « je ne prends plus rien mais je reste avec eux », qui fait basculer l’apprenant du rôle de consommateur à celui de conseiller, et qui admet la rechute : sur le plan de l’engagement, il est au-dessus de la moyenne.

Ce qui manque et qui pèse : le **périmètre** (15 % du thème de référence, aucun produit nommé, aucune violence, aucune donnée), l’**instrumentation** (aucun dispositif enseignant, aucun résultat remonté, aucune trace, quiz cantonné à la mémorisation avec un seuil atteignable par hasard une fois sur cinq) et l’**accessibilité** (des fonctions disponibles mais éteintes, sur un module de 162,8 Mo qui réserve le meilleur accès aux élèves les mieux connectés).

Les deux notes de ce rapport — **4,9/10 pour la qualité technique, 5,3/10 pour la valeur et la qualité éducative** — ne sont pas des verdicts de rejet. Elles désignent un produit **utilisable dès aujourd’hui en classe, à condition d’être accompagné**, et **perfectible à coût modéré**. Les treize actions du chapitre 6 sont ordonnées en conséquence : sept d’entre elles ne demandent pas de développement lourd et ne demandent ni développement lourd, ni réécriture du contenu. En les exécutant, le module peut passer de « bon support d’amorce » à « séquence de prévention évaluable », sans perdre une seconde de sa force narrative.

**Au mot de la fin pour l’enseignant.** Utilisez le module en ouverture de séance, projetez-le, puis retirez l’écran : la valeur du dispositif est dans les dix minutes de discussion qui suivent. Le module ne dit jamais à l’élève ce qu’il doit faire ; il lui montre, à lui de décider — et c’est précisément cette décision qu’il faut aller chercher dans la classe, avec trois questions bien choisies.

**Méthode et portée.** Ce rapport repose sur la lecture intégrale du code du module (contenu, 12 diapositives, 115 médias, 78 pistes de sous-titres), sur l’examen du paquet SCORM et de la configuration du lecteur, et sur la confrontation au document de référence « Contenus thématiques sur la SDSR » (Enabel, décembre 2025). Six fichiers de sous-titres annoncés n’étaient pas disponibles dans le paquet au moment de l’analyse ; les branches correspondantes ont été reconstituées à partir des transcriptions. Les notes sont pondérées selon le contexte d’usage visé et peuvent être recalculées par le lecteur à partir des grilles des sections 4.12 et 5.12.

[[PAGEBREAK]]

## 8. Annexes

### Annexe A — Verbatim du quiz (5 items, seuils et feedbacks)

| # | Énoncé | Récorrect | Feedback « juste » (extrait) | Feedback « faux » (extrait) |
|---|---|---|---|---|
| Q1 | « Les drogues peuvent aider à mieux mémoriser ses leçons et à devenir plus intelligent. » | **Faux** | « Les promesses d’amélioration de la mémoire ou de l’intelligence servent à inciter à consommer. » | Le même message, qui démonte l’idée reçue |
| Q2 | « Demander de l’aide à une personne de confiance… première étape pour sortir d’une addiction. » | **Vrai** | « Demander de l’aide permet de ne pas rester **seule** face à son problème. » | Message d encouragement à demander de l’aide (la formulation contient une coquille d’accord à corriger) |
| Q3 | « Continuer à fréquenter des camarades qui incitent à consommer ne présente aucun risque… » | **Faux** | « Rester dans un environnement où l’on est poussé à consommer peut compliquer l’arrêt de la consommation. » | Message sur la vigilance vis-à-vis de l’entourage |
| Q4 | « Une personne confrontée à une addiction doit être jugée et rejetée… » | **Faux** | « Il vaut mieux écouter la personne sans la juger et l’encourager à rechercher de l’aide. » | Message anti-stigmatisation |
| Q5 | « Face à une proposition de drogue, refuser et s’éloigner… » | **Vrai** | « Refuser clairement et s’éloigner d’une situation à risque permet de résister à la pression. » | Message sur la gestion de la pression |

Paramètres relevés : **5 items**, **10 points** chacun, **seuil de réussite 80 %** (soit 4/5), réponses verrouillées après la première tentative, soumission des questions sans réponse (`submitunanswered: all`), réinitialisation complète possible (`resettype: all`), remontée xAPI désactivée. Écran de résultats : mention « VOTRE SCORE » et « Score à atteindre : … ».

### Annexe B — Arbre de décisions : récapitulatif opérationnel

| Branche | Situation | Choix 1 (souvent risqué) | Choix 2 (soutenu par le module) | Conséquence enseignée |
|---|---|---|---|---|
| D1 | Proposition du groupe | « Bon, juste une fois. » | « Non merci, je ne veux pas essayer. » | Accepter → rester avec eux ; refuser → s’éloigner, éviter de commencer |
| D2 | Proposition d’aide | « Non, tout va bien » / « Je peux arrêter tout seul » | « Oui, j’ai un problème, je voudrais en parler avec vous » | Refuser l’aide → démarche plus difficile ; accepter → ne pas rester seul |
| D3 | Retour de la pression | « Je continue à les fréquenter, mais je ne prendrai plus rien » | « Non merci, je ne veux plus consommer » / rupture assumée | L’option modérée peut mener à la reprise ; la rupture protège le chemin parcouru |
| D4 | Grand frère Moussard | « Laisse-le se débrouiller, c’est son problème » | « Parle-lui sans le juger et encourage-le à demander de l’aide » | Ignorer laisse seul ; écouter et orienter aide |
| D5 | Reconsommation | « D’accord, juste pour une dernière fois » | (implicitement : refus) | La rechute est possible et remet en difficulté le chemin parcouru |

### Annexe C — Inventaire des médias et budget de poids

| Catégorie | Nombre | Poids | Part | Usage |
|---|---:|---:|---:|---|
| GIF animés | 37 fichiers restants (majorité) | ≈ 107,8 Mo | 66 % | Animations décoratives et transitions de scène |
| Vidéos MP4 | 16 | 45,5 Mo | 28 % | Séquences animées (≈ 3 min 30 s) |
| Pistes audio MP3 | 62 | ≈ 0,8 Mo | 0,5 % | Narration, dialogues, feedbacks (≈ 3 min 40 s) |
| Images PNG | — | ≈ 1,7 Mo | 1 % | Illustrations, boutons, éléments d’interface |
| Scripts, styles, polices | — | ≈ 7 Mo | 4 % | Lecteur Storyline |
| **Total** | **115 médias** | **≈ 162,8 Mo** | **100 %** | **≈ 7 min 11 s de contenus** |

Ratio à retenir : **≈ 23 Mo par minute de jeu**. La narration, qui porte l’essentiel du message, ne représente que 0,5 % du poids.

### Annexe D — Grille de correspondance avec le référentiel thématique (Enabel, décembre 2025)

| Rubrique du Thème 7 | Attendu d’après le référentiel | Présent dans le module ? | Manque principal |
|---|---|---|---|
| I. Définition des concepts | Définition de l’addiction, de la dépendance, de l’usage | Non | Aucune définition à l’écran |
| I bis. Caractéristiques communes des addictions | Critères, tolérance, sevrage, contrôle de l’usage | Partiel | Les signes sont montrés, jamais nommés |
| II. Causes et facteurs de vulnérabilité | Alcool, drogue, tabac : contexte, famille, précarité, déscolarisation | Partiel | Seule la pression des pairs est traitée |
| III. Conséquences | Conséquences de l’alcool et du tabac ; conséquences de la drogue | Partiel | Conséquences relationnelles seulement |
| IV. Types de drogues | Licites (alcool, tabac) et illicites (solvants, cannabis, tramadol) | Non | Aucun produit nommé ; or la « drogue » reste générique |
| V. Précautions à prendre | Précautions concrètes face à la consommation et à la pression | Partiel | Les précautions sont pratiquées, pas formulées |
| VI. Violences physiques | Formes et conséquences | Non | Aucun traitement |
| VI bis. Violences psychologiques et morales | Formes, witnessing, tabou | Non | Aucun traitement, malgré la question de la stigmatisation traitée |
| Couverture globale estimée | ≈ 14 pages de contenu de référence | **≈ 15 %** | — |

### Annexe E — Protocole de contrôle technique (reproductible)

| Objet contrôlé | Moyen | Résultat observé |
|---|---|---|
| Hébergement et transport | Analyse des en-têtes de réponse (CDN, cache, compression) | Cloudflare, Brotli, ETag, HSTS, `max-age=14400` |
| Structure du contenu | Lecture du modèle de contenu `data.js` | 12 diapositives, 2 invites, 115 médias, 1 scène, thème « unified » |
| Paramètres du quiz | Lecture de la configuration de quiz | 5 items, 10 points, seuil 80 %, `resettype: all`, `submitunanswered: all`, verrouillage après tentative |
| Interopérabilité | Lecture du manifeste et de la page de lancement | SCORM 1.2 valide ; site en `story.html` ; `xapi.lrsEnabled = false` |
| Accessibilité | Lecture des réglages `displayCaptions`, `accessibleText`, `zoomToFit`, `altText`, `tabIndex`, `accType` | Fonctions présentes, désactivées ; contrastes 3,2:1 sur les libellés |
| Poids et durée | Somme des tailles et des durées de l’inventaire médias | 162,8 Mo ; ≈ 7 min 11 s ; 115 médias |
| Contenu narratif et branches | Lecture des 78 pistes de sous-titres (16 transcriptions + 62 sous-titres) | 5 points de décision et leurs conséquences ; verbatims des feedbacks |
| Couverture thématique | Confrontation au document de référence Enabel | ≈ 15 % de couverture ; 0 occurrence d’« alcool », « tabac », « cigarette », « cannabis », « tramadol », « violence » |
| Métadonnées annoncées | Lecture de la page d’accueil et de la fiche du module | « 8 questions » annoncées pour 5 items réelles ; intitulé « Violences et addictions » non entièrement traité |

### Annexe F — Glossaire et références

| Terme | Définition employée dans ce rapport |
|---|---|
| SCORM 1.2 | Standard d’emballage de contenu e-learning (version 1.2) permettant à un LMS de suivre un module et de recevoir son score |
| xAPI | Standard de traçabilité des activités d’apprentissage, plus fin que SCORM (statuts, durée, tentatives) |
| LRS | « Learning Record Store » : serveur où sont stockées les traces xAPI |
| CMI | Variables du modèle de données SCORM (score, statut de leçon, temps, tentatives) |
| RGAA | Référentiel français d’accessibilité des sites et applications web |
| WCAG | Normes internationales d’accessibilité du contenu web (niveaux A, AA, AAA) |
| Bloom (taxonomie) | Classification des niveaux cognitifs : mémorisation, compréhension, application, analyse, synthèse, évaluation |
| GIF / MP4 / WebM | Formats d’image animée et de vidéo ; le GIF est très lourd et non adapté à l’animation longue |
| HSTS / ETag / Brotli | En-têtes de sécurité et de performance : forçage du HTTPS, validation de cache, compression |
| Serious game | Jeu à visée pédagogique ou de formation ; la plateforme Serious Game SDSR héberge les 9 modules du projet |
| Serious Game SDSR | La plateforme de serious games développée dans le cadre du projet SDSR (santé de la reproduction et santé sexuelle) |
| Prévention par les pairs | Prévention conduite par ou avec des jeunes du même public, à partir de leur expérience |

**Sources consultées pour ce rapport**

- Plateforme Serious Game SDSR — `https://sdsr.ticanalyse.org/` (9 modules, niveaux, durées, nombres de questions annoncés).
- Fiche du Thème 7 — `https://sdsr.ticanalyse.org/theme-7/` (intitulé, lecteur intégré, section « Ressources »).
- Paquet du module — `https://sdsr.ticanalyse.org/wp-content/uploads/articulate_uploads/Theme-7/` : `imsmanifest.xml`, `index_lms.html`, `story.html`, `html5/data/js/data.js`, scripts de diapositives, 78 pistes de sous-titres, inventaire de 115 médias.
- Référentiel thématique — « Contenus thématiques sur la SDSR adaptés aux jeunes et adolescent·e·s à digitaliser », Enabel, décembre 2025 (fichier `Document-Contenu-Thematique-SDSR.pdf`), notamment le Thème 7 (14 pages) et son glossaire.
- Présentation de l’offre « Digitalisation de contenus », TICANALYSE.
