# Méthodologie du projet Trends
## Tourisme international dans les principales destinations africaines

**Projet :** Trends — Gaea21  
**Document :** Référentiel méthodologique  
**Dernière mise à jour :** 8 septembre 2026  
**Statut :** Document vivant — à mettre à jour lorsqu'une règle de traitement ou de comparaison évolue.

---

## 1. Objectif du document

Ce document formalise les règles méthodologiques utilisées pour construire, contrôler, harmoniser, analyser et visualiser les données du projet Trends consacré au tourisme international dans sept destinations africaines.

Il complète :
- `project_documentation.md`, qui retrace le déroulement général du projet ;
- `data_sources.md`, qui assure la traçabilité des sources ;
- `data_dictionary.md`, qui décrit les variables du dataset maître ;
- `handover_guide.md`, qui expliquera comment reprendre le projet.

L'objectif est qu'une nouvelle personne puisse comprendre non seulement **ce qui a été fait**, mais aussi **pourquoi les données ont été traitées de cette manière**.

---

# 2. Principe méthodologique central

Le projet repose sur le principe suivant :

> **Aucune comparaison ne doit être effectuée sans contrôle préalable de la source, de la définition, de la période, de l'unité, de la granularité et du périmètre de couverture.**

Deux valeurs portant le même nom peuvent ne pas mesurer exactement le même phénomène.

La priorité méthodologique est donc :

**fiabilité -> comparabilité -> analyse -> visualisation**

et non :

**visualisation -> interprétation -> vérification a posteriori**

---

# 3. Périmètre de l'étude

## 3.1 Destinations

Sept destinations africaines sont étudiées :

- Afrique du Sud ;
- Égypte ;
- Kenya ;
- Maroc ;
- Maurice ;
- Tanzanie ;
- Tunisie.

## 3.2 Dimensions principales

Trois dimensions sont intégrées au dataset maître :

1. **Arrivées touristiques internationales**
2. **Recettes touristiques internationales**
3. **Provenance des touristes**

## 3.3 Unité d'observation

L'unité d'observation dépend de la couche du dataset.

Pour `arrivals` et `receipts`, une observation correspond principalement à :

**destination × année × indicateur**

Pour `provenance`, elle peut correspondre à :

**destination × année × origine × indicateur × granularité**

Cette différence doit être conservée dans toute analyse.

---

# 4. Workflow méthodologique

Le workflow retenu est :

```text
1. Comprendre la thématique
        ↓
2. Identifier les indicateurs
        ↓
3. Rechercher les sources
        ↓
4. Collecter les données
        ↓
5. Auditer qualité et comparabilité
        ↓
6. Nettoyer et standardiser
        ↓
7. Harmoniser
        ↓
8. Construire le dataset maître
        ↓
9. Réaliser l'EDA
        ↓
10. Sélectionner les indicateurs analytiques
        ↓
11. Construire les visualisations / dashboard
        ↓
12. Interpréter et documenter
```

Chaque étape doit être suffisamment documentée pour être reproduite.

---

# 5. Sélection des sources

## 5.1 Priorité aux sources institutionnelles

Les sources institutionnelles ou statistiques officielles sont privilégiées.

Pour les séries d'arrivées et de recettes, une source internationale harmonisée est utilisée afin d'obtenir une base aussi comparable que possible entre destinations.

Pour la provenance, des sources nationales ont été nécessaires car aucune source unique utilisée dans le projet ne fournissait une couverture homogène et suffisamment détaillée pour les sept destinations.

## 5.2 Critères d'évaluation d'une source

Avant intégration, une source est évaluée selon :

- l'organisme producteur ;
- la définition de l'indicateur ;
- la période disponible ;
- l'unité ;
- la granularité ;
- la fréquence ;
- le périmètre géographique ;
- la couverture des marchés ;
- la présence de données manquantes ;
- la possibilité de retrouver et documenter la source.

## 5.3 Traçabilité

Chaque source doit être reliée autant que possible à :

```text
organisme
-> document / dataset
-> URL
-> date d'accès
-> fichier collecté
-> fichier harmonisé
-> dataset maître
```

Les informations exactes sont centralisées dans `data_sources.md`.

---

# 6. Diagnostic initial des données

Tout nouveau fichier doit être contrôlé avant transformation.

Les vérifications minimales sont :

- dimensions du fichier ;
- noms des colonnes ;
- types des variables ;
- valeurs manquantes ;
- doublons ;
- valeurs aberrantes ;
- années disponibles ;
- destinations présentes ;
- unités ;
- granularité ;
- cohérence des catégories.

Les variables numériques doivent être réellement numériques et les années doivent être exploitables comme années.

Les codes textuels tels que `-`, `..`, `n/a` ou équivalents doivent être interprétés selon la documentation de la source et transformés en valeur manquante lorsque cela correspond bien à une absence de donnée.

---

# 7. Standardisation

## 7.1 Noms des destinations

Les noms sont standardisés dans le dataset maître :

```text
Afrique du Sud
Égypte
Kenya
Maroc
Maurice
Tanzanie
Tunisie
```

Une nouvelle variante orthographique ne doit pas créer une nouvelle destination.

## 7.2 Années

`year` doit représenter une année entière.

Aucune observation annuelle ne doit être créée artificiellement uniquement pour obtenir une série continue.

## 7.3 Valeurs

`value` contient la valeur numérique de l'observation.

Sa signification dépend obligatoirement de `unit`, `metric_type`, `dataset_layer` et, pour la provenance, de `granularity`.

Une valeur seule ne doit donc jamais être interprétée sans son contexte.

## 7.4 Textes et catégories

Les espaces parasites, variantes de casse et caractères incohérents peuvent être normalisés lorsqu'ils ne modifient pas la signification de la donnée.

Les libellés originaux importants doivent rester traçables.

---

# 8. Gestion des unités

## 8.1 Principe

> **Deux valeurs exprimées dans des unités différentes ne sont pas directement comparables.**

Les unités ne doivent jamais être supprimées du raisonnement analytique.

## 8.2 Arrivées

Les arrivées sont traitées comme des volumes de personnes / arrivées selon la définition de l'indicateur source.

## 8.3 Recettes

Les recettes issues de la série principale sont exprimées en dollars US courants.

**Limite :** une hausse en dollars courants ne représente pas nécessairement une hausse équivalente en termes réels.

## 8.4 Provenance

La provenance peut contenir plusieurs unités.

Exemples principaux :

```text
persons
share
```

Une `share` n'est jamais convertie en volume de personnes sans disposer d'un dénominateur compatible, vérifié et méthodologiquement justifié.

## 8.5 Affichage des parts

Dans le dataset, une part peut être conservée sous forme décimale.

Exemple :

```text
0.243
```

peut être affiché dans le dashboard comme :

```text
24,3 %
```

Cette conversion est uniquement une transformation d'affichage.

La valeur brute du dataset ne doit pas être écrasée pour les exports.

---

# 9. Gestion des valeurs manquantes

## 9.1 Règle principale

> **Valeur manquante ≠ zéro**

Une absence d'information ne signifie pas que le phénomène mesuré vaut zéro.

## 9.2 Traitement

Lorsque l'information n'est pas disponible ou pas suffisamment fiable :

- la valeur reste manquante ;
- elle n'est pas remplacée par zéro ;
- elle n'est pas inventée ;
- elle n'est pas interpolée automatiquement ;
- la limite est documentée si elle affecte l'analyse.

## 9.3 Interpolation

Aucune interpolation n'est appliquée par défaut.

Une éventuelle interpolation future devrait être :
- justifiée ;
- documentée ;
- séparée des données observées ;
- identifiable par un indicateur de qualité.

## 9.4 Visualisation

Une année manquante dans une courbe ne doit pas être représentée comme une valeur nulle.

Sur une carte, une destination sans observation doit rester non renseignée.

---

# 10. Valeurs aberrantes

Une valeur inhabituelle n'est pas supprimée uniquement parce qu'elle est extrême.

Avant toute correction, il faut déterminer si elle correspond à :

- une erreur de saisie ;
- un changement d'unité ;
- une rupture méthodologique ;
- un événement réel ;
- une modification de couverture ;
- un problème d'extraction.

La crise de 2020 constitue par exemple une rupture réelle majeure dans les séries touristiques et ne doit pas être traitée comme une simple anomalie statistique.

---

# 11. Doublons

Un doublon doit être évalué selon la clé logique de l'observation.

Pour les séries simples :

```text
destination + year + dataset_layer + metric_type
```

Pour la provenance, la clé peut nécessiter :

```text
destination + year + origin_name + granularity + metric_type + unit
```

Deux lignes ayant la même destination et la même année ne sont donc pas nécessairement des doublons.

---

# 12. Granularité

## 12.1 Principe

> **Pays ≠ région ≠ agrégat ≠ panel**

La granularité doit être conservée explicitement.

## 12.2 Provenance pays

Une observation correspondant à un pays d'origine peut être utilisée dans une analyse des marchés pays lorsque son unité et son périmètre sont compatibles.

## 12.3 Agrégats régionaux

Exemples :

```text
Européens
Arabes
Américains
Autres
```

Ces catégories ne doivent pas être placées dans un classement de pays.

## 12.4 Totaux et sous-totaux

Un total ou sous-total ne doit pas être additionné à ses propres composantes.

Exemple conceptuel :

```text
France
Allemagne
Italie
TOTAL EUROPE
```

Le total Europe et ses pays ne doivent pas être additionnés dans le même calcul de total.

---

# 13. MRE, TRE et populations assimilées

Les catégories telles que :

- Marocains résidant à l'étranger (MRE) ;
- Tunisiens résidant à l'étranger (TRE) ;

doivent rester distinguées des touristes étrangers lorsque la source les distingue.

**Règle :** ne pas fusionner automatiquement diaspora / résidents à l'étranger avec les marchés touristiques étrangers.

Toute inclusion dans un indicateur doit être explicitement justifiée.

---

# 14. Audit de comparabilité

## 14.1 Objectif

L'audit vise à déterminer non seulement si une donnée existe, mais surtout **ce qu'il est raisonnable de comparer**.

## 14.2 Critères

Chaque série est évaluée selon :

1. source ;
2. définition ;
3. unité ;
4. période ;
5. granularité ;
6. couverture ;
7. qualité ;
8. exhaustivité ou caractère partiel.

## 14.3 Classification

Une classification opérationnelle a été utilisée :

### GREEN

Données suffisamment cohérentes pour les comparaisons prévues, sous réserve des limites normales de la source.

### ORANGE

Données exploitables mais avec couverture partielle, période courte, panel limité ou autre restriction nécessitant une interprétation prudente.

### RED

Données non directement comparables aux séries principales ou couverture trop limitée pour permettre une comparaison exhaustive.

**Important :** RED ne signifie pas « donnée inutile ». Cela signifie que son usage analytique doit être adapté à son périmètre.

---

# 15. Comparabilité par destination — provenance

## 15.1 Maroc — GREEN

- période retenue : 2012–2020 ;
- volumes exacts dans le jeu harmonisé ;
- analyse possible par marché d'origine dans le périmètre disponible.

## 15.2 Tunisie — GREEN

- période retenue : 2017–2023 ;
- arrivées détaillées par nationalité ;
- attention particulière aux agrégats et aux TRE.

## 15.3 Kenya — ORANGE

- période : 2022–2024 ;
- volumes exacts ;
- couverture limitée à un Top 30.

**Conséquence :** un classement correspond au Top 30 disponible et non à l'intégralité des marchés.

## 15.4 Tanzanie — RED

- période : 2022–2024 ;
- Top 15 ;
- données retenues sous forme de parts.

**Interdiction méthodologique :** traiter ces parts comme des volumes exacts comparables aux séries `persons`.

## 15.5 Maurice — ORANGE

- période : 2022–2024 ;
- volumes exacts ;
- panel de sept marchés dans le jeu harmonisé.

**Conséquence :** ne pas présenter ce panel comme un classement exhaustif.

## 15.6 Afrique du Sud — ORANGE

- période : 2022–2024 ;
- volumes exacts ;
- panel de 18 marchés dans le jeu harmonisé.

**Conséquence :** limiter les conclusions au panel réellement présent.

## 15.7 Égypte — RED

Le cas égyptien est traité séparément.

Données pays retenues :
- États-Unis ;
- 2010–2019 ;
- volumes enregistrés comme exacts dans le jeu harmonisé ; liaison à la source originale non vérifiable avec les pièces présentes dans le dépôt.

Données régionales :
- année 2019 ;
- parts régionales.

Deux métriques régionales sont distinguées :
- `regional_tourist_share` ;
- `regional_tourist_nights_share`.

**Interdictions méthodologiques :**
- présenter les États-Unis comme premier marché d'origine sur la seule base de cette série ;
- construire un classement exhaustif des pays d'origine ;
- mélanger les parts de touristes et les parts de nuitées ;
- comparer directement un agrégat régional à un pays comme s'ils avaient la même granularité.

---

# 16. Couverture partielle et Top N

## 16.1 Principe

Un Top N ou un panel partiel ne devient pas exhaustif après harmonisation.

L'harmonisation standardise la structure, pas le niveau de couverture de la source.

## 16.2 Présentation

Les visualisations et textes doivent utiliser des formulations telles que :

```text
Principaux marchés disponibles dans la source
Top 30 disponible
Panel de 18 marchés
Marchés couverts par le jeu de données
```

et éviter :

```text
Tous les marchés
Classement exhaustif
Répartition complète
```

lorsque la source ne le permet pas.

---

# 17. Quality flags et couverture

Lorsque le dataset fournit des variables telles que `quality_flag` ou `coverage_scope`, elles doivent être conservées et utilisées dans l'interprétation.

Elles servent à répondre à des questions telles que :

- la donnée est-elle exacte ou agrégée ?
- la couverture est-elle exhaustive ou partielle ?
- s'agit-il d'un seul marché vérifié ?
- la valeur représente-t-elle un volume ou une part ?

Un `quality_flag` ne doit pas être ignoré uniquement pour simplifier une visualisation.

---

# 18. Construction du dataset maître

## 18.1 Objectif

Le dataset maître fournit un schéma commun aux trois dimensions tout en conservant les informations nécessaires à leur interprétation.

## 18.2 Principe

> **Harmoniser la structure sans effacer les différences méthodologiques.**

Les données ne sont donc pas rendues artificiellement « identiques ».

Les différences de :
- source ;
- unité ;
- granularité ;
- couverture ;
- qualité ;

doivent rester identifiables.

## 18.3 Couches

```text
arrivals
receipts
provenance
```

Une analyse doit commencer par sélectionner la couche appropriée.

---

# 19. Méthodologie de l'analyse exploratoire

## 19.1 Format du notebook

Le notebook suit la structure :

```text
Markdown
   ↓
Code
   ↓
Résultat
   ↓
Interprétation Markdown
```

Le code seul n'est pas considéré comme une analyse complète.

## 19.2 Contrôles préalables

Avant les analyses de tendance :

- contrôler les années ;
- contrôler les valeurs disponibles ;
- contrôler l'unité ;
- identifier les ruptures ;
- vérifier les destinations réellement comparables.

## 19.3 Statistiques descriptives

Selon la pertinence, les analyses pourront inclure :

- moyenne ;
- médiane ;
- minimum ;
- maximum ;
- écart-type ;
- taux de variation ;
- taux de croissance annuel moyen ;
- niveaux avant/après rupture.

Ces statistiques ne doivent être calculées que sur des séries suffisamment comparables.

---

# 20. Analyse temporelle

## 20.1 Évolution

Les séries temporelles doivent conserver les années réellement observées.

## 20.2 Rupture de 2020

L'année 2020 doit être analysée comme une rupture structurelle liée au contexte du tourisme mondial, et non comme un simple point aberrant à supprimer.

## 20.3 Reprise post-Covid

La reprise peut être évaluée notamment par comparaison avec un niveau pré-Covid approprié.

Toute définition de « retour au niveau pré-Covid » doit indiquer clairement l'année de référence.

## 20.4 Taux de variation

Formule générale :

```text
taux_variation = ((valeur_t - valeur_t-1) / valeur_t-1) × 100
```

Le calcul n'est pas effectué lorsque la valeur de référence est manquante ou incompatible.

---

# 21. Analyse croisée arrivées × recettes

Les arrivées et recettes peuvent être étudiées conjointement lorsqu'elles concernent la même destination et une période compatible.

Un indicateur dérivé tel que :

```text
recettes / arrivées
```

peut être calculé uniquement si :
- les deux valeurs existent ;
- les périodes correspondent ;
- les unités sont connues ;
- l'interprétation est explicitée.

Cet indicateur est un ratio analytique. Il ne doit pas être automatiquement présenté comme une dépense individuelle exacte de chaque touriste.

---

# 22. Méthodologie des comparaisons

Une comparaison doit :

1. nommer clairement les destinations ou groupes comparés ;
2. utiliser le même indicateur ;
3. vérifier l'unité ;
4. vérifier la période ;
5. signaler les différences de couverture ;
6. quantifier les écarts lorsque pertinent ;
7. contextualiser les résultats ;
8. éviter les conclusions causales non démontrées.

Une corrélation visuelle ou statistique n'est pas une preuve de causalité.

---

# 23. Méthodologie du dashboard

## 23.1 Principe

Le dashboard ne doit pas permettre à l'interface de faire disparaître les limites méthodologiques.

## 23.2 Filtres

Les filtres doivent permettre de sélectionner les dimensions pertinentes sans créer de combinaison incohérente.

La version cible suit le template Gaea21 avec les filtres principaux dans `st.sidebar`.

## 23.3 Tendances

Les courbes :
- utilisent uniquement les observations disponibles ;
- ne remplacent pas les trous par zéro ;
- affichent l'unité appropriée ;
- doivent être interprétées selon la période sélectionnée.

## 23.4 Provenance

La visualisation dépend du type de donnée disponible.

### Données `persons`

Affichage possible sous forme de volumes.

### Données `share`

Conversion en pourcentage uniquement pour l'affichage.

### Égypte

Le dashboard doit distinguer :
- série pays États-Unis ;
- agrégats régionaux ;
- part des touristes ;
- part des nuitées.

## 23.5 Carte

Une carte compare uniquement les destinations possédant une observation valide pour l'indicateur et l'année sélectionnés.

Une destination sans valeur ne doit pas être colorée comme si sa valeur était zéro.

---

# 24. Exports

Les exports CSV doivent préserver autant que possible les valeurs analytiques originales.

Exemple :
- une part `0.243` peut être affichée `24,3 %` ;
- l'export peut conserver `0.243` afin d'éviter de modifier la valeur source.

Les transformations purement visuelles doivent être séparées des transformations de données.

---

# 25. Reproductibilité

Toute nouvelle transformation importante doit pouvoir être expliquée.

Lors d'une modification :

```text
1. identifier le besoin
2. modifier le traitement
3. contrôler le résultat
4. documenter la décision
5. mettre à jour le notebook / code concerné
6. mettre à jour les documents concernés
7. créer un commit Git explicite
```

La documentation fait partie du livrable et non d'une étape optionnelle de fin de projet.

---

# 26. Ce qu'il ne faut pas faire

Les pratiques suivantes sont interdites sans justification méthodologique explicite :

- remplacer les valeurs manquantes par zéro ;
- inventer des observations ;
- interpoler silencieusement ;
- additionner un agrégat et ses composantes ;
- mélanger personnes et parts ;
- mélanger touristes et nuitées ;
- présenter un Top N comme exhaustif ;
- présenter un panel comme l'ensemble du marché ;
- classer des pays et régions dans la même catégorie ;
- ignorer les `quality_flag` pour faciliter un graphique ;
- comparer des périodes incompatibles sans avertissement ;
- tirer une conclusion causale d'une simple corrélation ;
- modifier une valeur brute uniquement pour améliorer une visualisation.

---

# 27. Checklist avant une nouvelle analyse

Avant de produire un KPI, graphique ou conclusion :

```text
[ ] Quelle est la source ?
[ ] Quel est l'indicateur ?
[ ] Quelle est sa définition ?
[ ] Quelle est l'unité ?
[ ] Quelle est la période ?
[ ] Quelle est la granularité ?
[ ] Quelle est la couverture ?
[ ] Y a-t-il des valeurs manquantes ?
[ ] Y a-t-il un quality_flag ?
[ ] Les observations comparées sont-elles réellement compatibles ?
[ ] La visualisation risque-t-elle de masquer une limite ?
[ ] La conclusion reste-t-elle dans le périmètre supporté par les données ?
```

---

# 28. Checklist avant ajout d'une nouvelle source

```text
[ ] Organisme identifié
[ ] Titre exact identifié
[ ] URL conservée
[ ] Date d'accès conservée
[ ] Fichier brut archivé si possible
[ ] Définition de l'indicateur vérifiée
[ ] Unité vérifiée
[ ] Période vérifiée
[ ] Granularité vérifiée
[ ] Couverture vérifiée
[ ] Valeurs manquantes contrôlées
[ ] Doublons contrôlés
[ ] Transformations documentées
[ ] Source ajoutée à data_sources.md
[ ] Variables nouvelles ajoutées à data_dictionary.md
```

---

# 29. Règles pour la reprise du projet

Une personne reprenant le projet doit consulter dans cet ordre :

```text
README.md
        ↓
docs/project_documentation.md
        ↓
docs/data_sources.md
        ↓
docs/methodology.md
        ↓
docs/data_dictionary.md
        ↓
notebooks/01_analyse_exploratoire.ipynb
        ↓
dashboard/app.py
```

Avant de modifier une règle existante, elle doit vérifier si celle-ci répond à une limite connue de comparabilité.

---

# 30. Historique des décisions méthodologiques

| Date | Décision | Motif |
|---|---|---|
| 2026 | Conservation des valeurs manquantes | Absence de donnée ≠ zéro |
| 2026 | Pas d'interpolation automatique | Éviter la fabrication d'information |
| 2026 | Séparation volumes / parts | Unités non équivalentes |
| 2026 | Séparation pays / agrégats | Granularités non équivalentes |
| 2026 | MRE / TRE conservés séparément | Population spécifique dans les sources |
| 2026 | Classification GREEN / ORANGE / RED | Formaliser le niveau de comparabilité |
| 2026 | Panels partiels explicitement signalés | Éviter les classements faussement exhaustifs |
| 2026 | Traitement spécifique de l'Égypte | Couverture pays insuffisante pour un classement complet |
| 2026 | Traitement spécifique de la Tanzanie | Parts disponibles plutôt que volumes comparables |
| 2026 | Documentation avant visualisation finale | Garantir la transmission et la reproductibilité |
| 2026-09-08 | Approfondissement de l'EDA avant refonte finale du dashboard | Faire dériver les indicateurs visuels de l'analyse |
| 2026-09-08 | Filtres du dashboard à déplacer dans `st.sidebar` | Alignement avec le template Gaea21 |

---

## Règle finale

> **Une visualisation techniquement correcte n'est pas nécessairement méthodologiquement correcte.**

Toute analyse ou visualisation Trends doit rester fidèle au périmètre réellement supporté par les données.

## Procédure reproductible de correction des métadonnées — 8 septembre 2026

Exécuter depuis la racine :

```powershell
python -B src/metadata_corrections.py
```

Le script résout les chemins depuis son emplacement, lit le CSV maître et prépare toutes les sorties avant sauvegarde. Il vérifie 1 080 lignes avant/après, un hash inchangé des chaînes numériques `value` (valeurs absentes incluses), et l'identité de toutes les cellules hors métadonnées explicitement autorisées. Les identités, années, origines, valeurs, sources et couvertures sont conservées. Aucun ajout ni suppression de ligne.

| Cible | Lignes | Modification |
|---|---:|---|
| Tunisie / Scandinaves, 2017–2023 | 7 | `country` → `regional_aggregate` ; `exact_country` → `exact_aggregate` |
| Kenya / United Nations Organization, 2022 | 1 | `country` → `institutional_category` ; `exact_top30` conservé |
| Provenance Tunisie / `value` absent, 2017–2018 | 60 | `exact_country` → `missing_unverified` |

Les notes existantes sont conservées et complétées une seule fois. Le journal `reports/exports/metadata_corrections_log.csv` enregistre chaque cellule effectivement modifiée avec ancien/nouveau contenu et justification. Une réexécution ne duplique ni notes ni journal et ne réécrit pas les fichiers inchangés. Toute cible ou ancien état inattendu bloque la sauvegarde.

### Définitions et réserves

- `institutional_category` : catégorie institutionnelle publiée, distincte d'un pays, d'un agrégat régional et d'un total. Pour ONU/Kenya, définition statistique exacte à vérifier ; rang source conservé.
- `missing_unverified` : valeur absente du dataset harmonisé, cause non vérifiée dans la source originale. Ne signifie jamais zéro. `missing_in_source` reste réservé à une absence confirmée dans la source ; il n'est pas attribué aux 60 lignes tunisiennes.
- `Scandinaves` : groupe régional dont la composition exacte reste à vérifier ; aucune ventilation en pays ni fusion automatique avec d'autres agrégats scandinaves. Le drapeau `exact_aggregate` reclasse la nature de la mesure sans certifier à nouveau les chiffres.

`country` ne signifie pas automatiquement que toute catégorie publiée par une source est géographiquement un pays ; les catégories institutionnelles et agrégées doivent être explicitement distinguées.

`Reunion Island` reste `country` comme marché source distinct dans l'état actuel du modèle. Ne pas fusionner automatiquement ce marché avec `France`. Aucun changement de granularité ni correspondance multilingue n'est appliqué.

Égypte–États-Unis : l'attribution CAPMAS existe dans l'historique documentaire, mais sa liaison aux dix observations 2010–2019 n'est pas vérifiable avec les pièces actuellement présentes dans le dépôt. `User-provided source file`, les références et les valeurs restent inchangés.

### Synchronisation Excel et sécurité d'écriture

Le CSV est la source utilisée par les scripts. Le XLSX est synchronisé par remplacement ciblé des cellules textuelles dans son archive XML : `Dataset_maitre`, drapeaux de `Audit_maitre`, règles de `Dictionnaire` et précisions de `Methodologie`. Les cellules numériques, styles, tables, autres feuilles et structure restent conservés. Une incompatibilité bloque l'ensemble avant sauvegarde.

Les sorties sont préparées en mémoire puis dans des fichiers temporaires, avec remplacement atomique par fichier et restauration en cas d'erreur d'écriture interceptée. Ce mécanisme n'est pas une transaction multi-fichiers résistante à une coupure système.

Cette phase ne modifie ni l'EDA, ni le dashboard, ni les indicateurs analytiques.
