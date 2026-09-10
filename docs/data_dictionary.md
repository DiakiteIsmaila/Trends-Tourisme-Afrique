# Dictionnaire de données — Dataset maître Trends
## Tourisme international dans les principales destinations africaines

**Projet :** Trends — Gaea21  
**Dataset :** `dataset_maitre_trends_tourisme_afrique`  
**Dernière mise à jour :** 8 septembre 2026  
**Dimensions du dataset :** 1 080 lignes × 17 colonnes  
**Destinations :** 7  
**Couches :** 3 (`arrivals`, `receipts`, `provenance`)

---

# 1. Objectif

Ce document décrit les 17 variables du dataset maître utilisé pour l'analyse exploratoire et le dashboard Streamlit.

Le dataset réunit trois familles de données :
- arrivées touristiques internationales ;
- recettes touristiques internationales ;
- provenance des visiteurs.

Le dictionnaire doit être consulté avec :
- `project_documentation.md` pour l'historique du projet ;
- `data_sources.md` pour la traçabilité des sources ;
- `methodology.md` pour les règles de comparaison.

> Règle générale : une colonne ne doit pas être interprétée indépendamment des variables qui précisent son unité, sa granularité, sa couverture et sa qualité.

---

# 2. Schéma général

| # | Variable | Type pandas observé | Rôle |
|---:|---|---|---|
| 1 | `dataset_layer` | object | Couche analytique |
| 2 | `destination` | object | Destination touristique étudiée |
| 3 | `iso3` | object | Code ISO-3 de la destination |
| 4 | `year` | int64 | Année de l'observation |
| 5 | `origin_name` | object | Marché / origine du visiteur |
| 6 | `origin_region` | object | Région associée à l'origine |
| 7 | `granularity` | object | Niveau de détail de l'observation |
| 8 | `metric` | object | Indicateur principal |
| 9 | `value` | float64 | Valeur numérique |
| 10 | `unit` | object | Unité de mesure |
| 11 | `metric_type` | object | Sous-type méthodologique de mesure |
| 12 | `coverage_scope` | object | Périmètre réel de couverture |
| 13 | `source_name` | object | Organisme / source |
| 14 | `source_reference` | object | Référence du dataset, rapport ou URL |
| 15 | `source_file` | object | Fichier utilisé dans la chaîne de traitement |
| 16 | `quality_flag` | object | Indicateur de qualité / comparabilité |
| 17 | `notes` | object | Note méthodologique ou précaution |

---

# 3. Description détaillée des variables

## 3.1 `dataset_layer`

**Type observé :** `object`  
**Obligatoire :** oui  
**Rôle :** identifie la grande couche de données à laquelle appartient l'observation.

### Valeurs présentes

```text
arrivals
receipts
provenance
```

### Signification

- `arrivals` : arrivées touristiques internationales au niveau destination ;
- `receipts` : recettes du tourisme international ;
- `provenance` : données relatives aux marchés ou régions d'origine.

### Règle

Toujours filtrer la couche pertinente avant une analyse. Les trois couches ne représentent pas la même unité d'observation.

---

## 3.2 `destination`

**Type observé :** `object`  
**Obligatoire :** oui  
**Rôle :** destination touristique à laquelle l'observation se rapporte.

### Valeurs présentes

```text
Afrique du Sud
Égypte
Kenya
Maroc
Maurice
Tanzanie
Tunisie
```

### Règle

Ces libellés constituent la nomenclature standard du projet. Une variante linguistique ou orthographique ne doit pas créer une nouvelle catégorie.

---

## 3.3 `iso3`

**Type observé :** `object`  
**Obligatoire :** oui  
**Rôle :** code pays ISO alpha-3 utilisé notamment pour les jointures et la cartographie.

### Valeurs présentes

| Destination | ISO-3 |
|---|---|
| Afrique du Sud | `ZAF` |
| Égypte | `EGY` |
| Kenya | `KEN` |
| Maroc | `MAR` |
| Maurice | `MUS` |
| Tanzanie | `TZA` |
| Tunisie | `TUN` |

### Usage

La carte Plotly doit privilégier cette colonne plutôt qu'une traduction dynamique du nom du pays.

---

## 3.4 `year`

**Type observé :** `int64`  
**Obligatoire :** oui  
**Rôle :** année de référence de l'observation.

### Couverture observée dans le dataset maître

Le dataset contient 30 années distinctes. La couverture exacte dépend de la couche et de la destination.

### Règles

- conserver un entier ;
- ne pas fabriquer les années absentes ;
- vérifier la disponibilité de `value` avant un calcul ;
- ne pas confondre absence d'année et valeur égale à zéro.

---

## 3.5 `origin_name`

**Type observé :** `object`  
**Obligatoire :** non pour toutes les couches  
**Rôle :** libellé du marché, pays, agrégat ou groupe d'origine.

Cette variable est principalement pertinente pour `dataset_layer == "provenance"`.

### Exemples observés

```text
Touristes Etrangers
France
Espagne
Royaume-Uni
Allemagne
Italie
Etats Unis
Belgique
Hollande
Maghreb
Chine
Scandinavie
```

Le dataset contient plus d'une centaine de libellés distincts.

### Attention

`origin_name` n'implique pas automatiquement une granularité `country`.

Toujours lire cette variable avec `granularity`.

---

## 3.6 `origin_region`

**Type observé :** `object`  
**Obligatoire :** non  
**Rôle :** région ou groupe géographique associé à l'origine.

### Exemples observés

```text
Total
Europe
Amériques
Afrique du Nord
Asie
Diaspora
Maghreb
Amérique du Nord
Moyen-Orient
Amérique du Sud
Océanie
Diaspora tunisienne
```

### Usage

Cette colonne permet :
- d'organiser les marchés ;
- d'identifier les agrégats ;
- de distinguer certaines populations spécifiques.

### Règle

Ne pas supposer que `origin_region` constitue une classification géographique internationale harmonisée. Elle peut refléter la nomenclature de la source.

---

## 3.7 `granularity`

**Type observé :** `object`  
**Obligatoire :** oui  
**Rôle :** précise le niveau de détail de l'observation.

### Valeurs présentes

```text
destination_total
aggregate_total
country
regional_aggregate
diaspora
institutional_category
```

### Définitions

#### `destination_total`

Observation globale au niveau de la destination.

Principalement utilisée pour les séries d'arrivées et de recettes.

#### `aggregate_total`

Total ou agrégat publié par une source de provenance.

Ne doit pas être traité comme un pays.

#### `country`

Marché d'origine au niveau pays.

C'est généralement la granularité utilisée pour les graphiques de classement des marchés.

#### `institutional_category`

Catégorie institutionnelle publiée par une source, distincte des pays, régions et totaux.
Dans le dataset : United Nations Organization, Kenya 2022. La définition statistique exacte reste à vérifier ; `exact_top30` et le rang source sont conservés.

#### `regional_aggregate`

Agrégat régional.

Exemple : Européens, Arabes, Américains.

#### `diaspora`

Population de ressortissants/résidents à l'étranger distinguée par la source.

Exemples méthodologiques : MRE ou TRE.

### Règle essentielle

```text
country != regional_aggregate != aggregate_total != diaspora
```

---

## 3.8 `metric`

**Type observé :** `object`  
**Obligatoire :** oui  
**Rôle :** identifie l'indicateur principal mesuré.

### Valeurs présentes

```text
tourist_arrivals
tourism_receipts
tourist_origin
```

### Correspondance

| `metric` | Signification |
|---|---|
| `tourist_arrivals` | Arrivées touristiques internationales |
| `tourism_receipts` | Recettes du tourisme international |
| `tourist_origin` | Provenance / origine des visiteurs |

### Différence avec `dataset_layer`

`dataset_layer` décrit l'organisation du dataset.

`metric` décrit ce qui est mesuré.

Les deux sont proches dans le dataset actuel, mais leurs rôles conceptuels restent différents.

---

## 3.9 `value`

**Type observé :** `float64`  
**Obligatoire :** non — certaines valeurs sont manquantes  
**Rôle :** valeur numérique de l'observation.

### Interprétation

`value` ne possède pas de signification autonome.

Il faut toujours consulter :

```text
unit
metric
metric_type
granularity
coverage_scope
quality_flag
```

### Exemples conceptuels

```text
value = 5 000 000 + unit = persons
```

n'a pas la même signification que :

```text
value = 0.243 + unit = share
```

### Règles

- `NaN` reste une donnée manquante ;
- ne jamais remplacer automatiquement `NaN` par `0` ;
- ne pas comparer directement des valeurs ayant des unités différentes.

---

## 3.10 `unit`

**Type observé :** `object`  
**Obligatoire :** oui lorsque `value` est interprétée  
**Rôle :** unité de la valeur.

### Valeurs présentes

```text
persons
current_USD
share
```

### Définitions

#### `persons`

Nombre de personnes / arrivées selon le contexte de l'indicateur.

#### `current_USD`

Valeur monétaire exprimée en dollars US courants.

#### `share`

Part stockée sous forme décimale.

Exemple :

```text
0.15 = 15 %
```

### Règle d'affichage

Pour `share`, le dashboard peut utiliser :

```python
display_value = value * 100
```

uniquement pour l'affichage.

La valeur brute doit rester inchangée dans le dataset et dans les exports analytiques.

---

## 3.11 `metric_type`

**Type observé :** `object`  
**Obligatoire :** oui  
**Rôle :** précise la nature méthodologique de la mesure à l'intérieur d'un indicateur.

### Valeurs présentes

```text
destination_total
tourist_arrivals
diaspora_arrivals
source_market_share
regional_tourist_share
regional_tourist_nights_share
```

### Définitions

#### `destination_total`

Mesure globale de la destination pour les couches principales.

#### `tourist_arrivals`

Volume d'arrivées de touristes pour une origine donnée.

#### `diaspora_arrivals`

Arrivées associées à une catégorie de diaspora explicitement distinguée par la source.

#### `source_market_share`

Part d'un marché d'origine.

#### `regional_tourist_share`

Part des touristes correspondant à un agrégat régional.

#### `regional_tourist_nights_share`

Part des nuitées touristiques correspondant à un agrégat régional.

### Règle essentielle

`regional_tourist_share` et `regional_tourist_nights_share` ne sont pas interchangeables.

---

## 3.12 `coverage_scope`

**Type observé :** `object`  
**Obligatoire :** méthodologiquement importante  
**Rôle :** décrit ce que la source couvre réellement.

### Exemples présents

```text
Common WDI destination-level series
Série officielle incluant agrégats publiés
Nationalités/pays publiés par Open Data Maroc
MRE séparés des touristes étrangers
Nationalités publiées par ONTT
Nationalités publiées + TRE séparés
Top 30 marchés sources publiés
Top 15 marchés — parts issues de l'Exit Survey
7 principaux marchés publiés dans les annual highlights
Panel harmonisé: 10 marchés SADC + 8 marchés overseas
Un seul marché pays vérifié: États-Unis
Répartition régionale 2019 uniquement
```

### Importance

Cette variable empêche de présenter une couverture partielle comme exhaustive.

### Exemple

```text
coverage_scope = "Top 30 marchés sources publiés"
```

signifie que le classement porte sur ce Top 30, et non sur tous les marchés possibles.

---

## 3.13 `source_name`

**Type observé :** `object`  
**Obligatoire :** oui  
**Rôle :** nom de la source ou de l'organisme associé à l'observation.

### Valeurs observées

```text
World Bank WDI
Open Data Maroc / Ministère chargé du Tourisme
ONTT
TRI / Directorate of Immigration Services
Tanzania NBS / International Visitors' Exit Survey
Statistics Mauritius
Statistics South Africa
User-provided source file
CAPMAS Statistical Yearbook - Tourism
```

### Usage

Permet :
- la traçabilité ;
- le contrôle méthodologique ;
- l'identification rapide des différences de source.

### Attention

Le registre détaillé et les références exactes doivent rester centralisés dans `data_sources.md`.

---

## 3.14 `source_reference`

**Type observé :** `object`  
**Obligatoire :** oui lorsque disponible  
**Rôle :** référence technique ou documentaire de la source.

### Types de contenu observés

Cette colonne peut contenir :
- un identifiant de série ;
- un nom de fichier ;
- un titre de rapport ;
- une URL institutionnelle ou documentaire.

### Exemples

```text
WB_WDI_ST_INT_ARVL
WB_WDI_ST_INT_RCPT_CD
evolution-par-nationalite-des-arrivees-des-touristes-aux-postes-frontieres.xlsx
Rapports annuels ONTT 2017–2023
```

Elle contient également des références documentaires/URL pour certaines sources nationales.

### Règle

Ne pas modifier une référence uniquement pour la rendre plus lisible sans conserver la référence originale quelque part.

---

## 3.15 `source_file`

**Type observé :** `object`  
**Obligatoire :** oui lorsque la chaîne de traitement possède un fichier intermédiaire identifié  
**Rôle :** fichier du projet à partir duquel l'observation a été intégrée ou harmonisée.

### Exemples observés

```text
audit_harmonisation_arrivees_7_pays_trends.xlsx
audit_harmonisation_recettes_7_pays_trends.xlsx
evolution-par-nationalite-des-arrivees-des-touristes-aux-postes-frontieres.xlsx
tunisie_provenance_touristique_2017_2023_ONTT.xlsx
kenya_provenance_touristique_2022_2024_TRI.xlsx
tanzania_tourism_provenance_2022_2024_NBS.xlsx
maurice_provenance_touristique_2022_2024_statistics_mauritius.xlsx
afrique_du_sud_provenance_touristique_2022_2024_stats_sa.xlsx
Number of Tourists and Tourist Nights between Egypt and the United States of America.xls
egypte_provenance_touristique_donnees_verifiees.xlsx
```

### Différence avec `source_reference`

- `source_reference` pointe vers la référence documentaire ou la source originale ;
- `source_file` pointe vers le fichier utilisé dans la chaîne de traitement du projet.

---

## 3.16 `quality_flag`

**Type observé :** `object`  
**Obligatoire :** fortement recommandé  
**Rôle :** qualifie la disponibilité, la précision ou le périmètre de l'observation.

### Valeurs présentes

```text
available
missing_in_source
missing_unverified
exact_aggregate
exact_country
exact_diaspora
exact_top30
survey_share_top15
exact_main7
exact_panel18
exact_single_country
regional_share_only
```

### Définitions

#### `available`

Observation disponible dans une série principale.

#### `missing_in_source`

Valeur absente dans la source.

**Ne signifie jamais zéro.**

#### `missing_unverified`

Valeur absente du dataset harmonisé ; cause de l'absence non vérifiée dans la source originale.
Concerne 60 lignes tunisiennes de provenance en 2017–2018. `value` reste manquant.
Ne signifie ni zéro ni absence confirmée dans la source : ne pas remplacer par `missing_in_source` sans vérification.

#### `exact_aggregate`

Valeur exacte correspondant à un agrégat publié.

#### `exact_country`

Valeur exacte au niveau pays dans la source utilisée.

#### `exact_diaspora`

Valeur exacte pour une catégorie diaspora.

#### `exact_top30`

Valeur exacte dans un Top 30 publié.

La donnée peut être exacte sans que la couverture soit exhaustive.

#### `survey_share_top15`

Part provenant d'une enquête et appartenant au Top 15 retenu.

Principalement utilisée pour le cas tanzanien.

#### `exact_main7`

Valeur exacte dans le panel de sept principaux marchés retenus.

#### `exact_panel18`

Valeur exacte dans le panel harmonisé de 18 marchés.

#### `exact_single_country`

Valeur exacte mais pour un seul marché pays vérifié.

Cas important pour l'Égypte.

#### `regional_share_only`

Observation disponible uniquement sous forme de part régionale.

### Règle

`exact` qualifie la valeur dans son périmètre ; cela ne signifie pas nécessairement que la couverture de la source est exhaustive.

---

## 3.17 `notes`

**Type observé :** `object`  
**Obligatoire :** non techniquement, mais importante pour les cas particuliers  
**Rôle :** conserve les précautions, décisions ou informations nécessaires à l'interprétation.

### Exemples de contenu observé

```text
No interpolation; missing stays blank.
Valeur WDI conservée telle que publiée; aucune interpolation.
Ne pas ventiler les agrégats Maghreb/Scandinavie; MRE reste diaspora.
Absence d'une nationalité publiée ≠ zéro; TRE non fusionnés avec touristes étrangers.
```

Pour certains panels, les notes indiquent également le rang officiel et rappellent que la table n'est pas exhaustive.

### Usage

Cette colonne est particulièrement utile lors :
- des contrôles qualité ;
- de la reprise du projet ;
- de l'interprétation d'un cas atypique.

Elle ne doit pas être supprimée du dataset maître uniquement parce qu'elle n'est pas utilisée dans un graphique.

---

# 4. Relations entre les variables

## 4.1 Arrivées

Structure analytique principale :

```text
dataset_layer = arrivals
metric = tourist_arrivals
granularity = destination_total
unit = persons
```

Variables centrales :

```text
destination
iso3
year
value
source_name
quality_flag
```

`origin_name` et `origin_region` ne sont pas nécessaires pour cette couche.

---

## 4.2 Recettes

Structure analytique principale :

```text
dataset_layer = receipts
metric = tourism_receipts
granularity = destination_total
unit = current_USD
```

Variables centrales :

```text
destination
iso3
year
value
source_name
quality_flag
```

---

## 4.3 Provenance

Structure plus détaillée :

```text
dataset_layer = provenance
metric = tourist_origin
```

L'interprétation dépend ensuite de :

```text
origin_name
origin_region
granularity
value
unit
metric_type
coverage_scope
quality_flag
```

Ces variables doivent être utilisées ensemble.

---

# 5. Valeurs manquantes

Une valeur manquante peut être :
- structurelle, parce qu'une colonne n'est pas pertinente pour une couche ;
- documentaire, parce que la source ne fournit pas l'information ;
- analytique, parce que la valeur n'est pas disponible pour une année donnée.

### Exemple structurel

`origin_name` est naturellement vide pour de nombreuses observations `arrivals` et `receipts`.

Cela n'est pas une erreur.

### Exemple documentaire

```text
quality_flag = missing_in_source
value = NaN
```

signifie que la valeur n'est pas disponible dans la source.

### Règle

```text
NaN != 0
```

---

# 6. Clés logiques recommandées

Le dataset ne doit pas être dédoublonné uniquement sur `destination + year`.

## 6.1 Arrivées / recettes

Une clé logique de contrôle peut utiliser :

```text
dataset_layer
destination
year
metric
metric_type
```

## 6.2 Provenance

Une clé plus détaillée est nécessaire :

```text
dataset_layer
destination
year
origin_name
granularity
metric_type
unit
```

Selon les sources, `origin_region` peut également être utilisé comme contrôle complémentaire.

---

# 7. Variables à utiliser dans le dashboard

## Tendances

Minimum :

```text
dataset_layer
destination
year
value
unit
```

## Provenance

Minimum :

```text
destination
year
origin_name
origin_region
granularity
value
unit
metric_type
coverage_scope
quality_flag
```

## Carte

Minimum :

```text
destination
iso3
year
dataset_layer
value
unit
```

---

# 8. Variables à ne pas ignorer dans l'EDA

Même lorsqu'elles ne sont pas affichées directement, les variables suivantes doivent être utilisées pour contrôler les analyses :

```text
granularity
metric_type
coverage_scope
source_name
source_reference
quality_flag
notes
```

Elles constituent une partie de la logique méthodologique du dataset.

---

# 9. Contrôles automatiques recommandés

Lors du chargement du dataset, vérifier au minimum :

```python
assert set(df["dataset_layer"].dropna().unique()) == {
    "arrivals",
    "receipts",
    "provenance",
}

assert df["destination"].nunique() == 7

assert df["iso3"].nunique() == 7
```

Vérifier également :

```python
df.shape
df.dtypes
df.isna().sum()
df.duplicated().sum()
df["unit"].value_counts(dropna=False)
df["granularity"].value_counts(dropna=False)
df["metric_type"].value_counts(dropna=False)
df["quality_flag"].value_counts(dropna=False)
```

Ces contrôles ne remplacent pas l'audit méthodologique.

---

# 10. Règles d'évolution du schéma

Toute nouvelle colonne doit être ajoutée à ce dictionnaire.

Toute modification d'une valeur catégorielle importante doit entraîner une vérification de :
- `methodology.md` ;
- le notebook EDA ;
- `dashboard/app.py` ;
- les scripts de `src/`.

Une catégorie ne doit pas être renommée silencieusement si elle est déjà utilisée par le code.

---

# 11. Résumé des catégories critiques

## `dataset_layer`

```text
arrivals
receipts
provenance
```

## `granularity`

```text
destination_total
aggregate_total
country
regional_aggregate
diaspora
institutional_category
```

## `metric`

```text
tourist_arrivals
tourism_receipts
tourist_origin
```

## `unit`

```text
persons
current_USD
share
```

## `metric_type`

```text
destination_total
tourist_arrivals
diaspora_arrivals
source_market_share
regional_tourist_share
regional_tourist_nights_share
```

## `quality_flag`

```text
available
missing_in_source
missing_unverified
exact_aggregate
exact_country
exact_diaspora
exact_top30
survey_share_top15
exact_main7
exact_panel18
exact_single_country
regional_share_only
```

---

# 12. Lecture correcte d'une observation

Une observation de provenance ne doit pas être lue comme :

```text
Égypte — 2019 — 0.643
```

mais comme une combinaison de variables :

```text
destination
year
origin_name / origin_region
granularity
metric
value
unit
metric_type
coverage_scope
quality_flag
source
```

C'est cette combinaison qui donne son sens réel à la valeur.

---

# 13. Références documentaires internes

Pour comprendre les variables :

```text
docs/project_documentation.md
docs/data_sources.md
docs/methodology.md
docs/data_dictionary.md
```

Pour observer leur utilisation :

```text
notebooks/01_analyse_exploratoire.ipynb
dashboard/app.py
src/data_processing.py
src/indicators.py
src/visualizations.py
```

---

# 14. Historique

| Date | Modification |
|---|---|
| 2026-09-08 | Création du dictionnaire à partir du dataset maître réel |
| 2026-09-08 | Documentation des 17 colonnes |
| 2026-09-08 | Documentation des catégories `granularity`, `metric_type`, `unit` et `quality_flag` |
| 2026-09-08 | Ajout des règles d'utilisation dans l'EDA et le dashboard |

---

## Règle finale

> Le dataset maître est harmonisé au niveau de sa structure, mais toutes ses observations ne sont pas interchangeables.

Les variables de contexte (`unit`, `granularity`, `metric_type`, `coverage_scope`, `quality_flag`, `source_name` et `notes`) doivent rester associées à `value` pour garantir une interprétation correcte.

## Corrections approuvées des métadonnées — 8 septembre 2026

- Tunisie / Scandinaves : 7 lignes, 2017–2023, `regional_aggregate` et `exact_aggregate`. Composition exacte à vérifier ; aucune ventilation en pays ni fusion automatique avec d'autres groupes scandinaves.
- Kenya / United Nations Organization : 1 ligne, 2022, `institutional_category` ; `exact_top30` et rang 22 conservés.
- Tunisie / valeurs absentes : 60 lignes, 30 origines sur 2017 et 2018, `missing_unverified`.

`country` ne signifie pas automatiquement que toute catégorie publiée par une source est géographiquement un pays ; les catégories institutionnelles et agrégées doivent être explicitement distinguées.

`Reunion Island` reste `country` dans l'état actuel du modèle : marché source distinct dans la publication enregistrée, sans fusion automatique avec `France`. Cette conservation n'affirme pas un statut de pays souverain.

Égypte–États-Unis : `source_name = User-provided source file` est conservé pour les dix observations 2010–2019. L'attribution CAPMAS existe dans l'historique documentaire, mais la liaison avec ces observations n'est pas vérifiable avec les pièces actuellement présentes dans le dépôt.

Procédure : `python -B src/metadata_corrections.py`. Journal par cellule modifiée : `reports/exports/metadata_corrections_log.csv`. Aucune valeur, ligne, origine source ou attribution de source n'est modifiée.
