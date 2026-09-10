# Documentation du projet Trends
## Tourisme international dans les principales destinations africaines

**Projet :** Trends - Gaea21  
**Thématique :** Tourisme international / tourisme durable  
**Statut du document :** Document vivant - à mettre à jour à chaque étape importante  
**Dernière mise à jour :** 8 septembre 2026

---

## 1. Présentation du document

### 1.1 Objectif de la documentation

Ce document constitue la documentation centrale du projet Trends consacré à l'analyse comparative du tourisme international dans plusieurs destinations africaines.

Son objectif est de conserver une trace structurée des travaux réalisés afin qu'une nouvelle personne puisse reprendre le projet sans devoir reconstruire l'historique des décisions, des traitements et des limites méthodologiques.

La documentation suit la chaîne de travail suivante :

**sources -> collecte -> audit -> harmonisation -> dataset maître -> analyse exploratoire -> choix des indicateurs -> dashboard -> interprétation -> transmission**

### 1.2 Public cible

Ce document s'adresse principalement :
- aux membres du département Statistiques de Gaea21 ;
- aux futurs contributeurs du projet Trends ;
- aux personnes chargées de maintenir ou d'enrichir le dataset ;
- aux personnes souhaitant comprendre ou reproduire les analyses et le dashboard.

### 1.3 Principe de mise à jour

Chaque étape importante doit être documentée avant le passage à l'étape suivante.

Statuts utilisés :
- **TERMINÉ** : étape réalisée et validée ;
- **EN COURS** : étape commencée mais non finalisée ;
- **À FAIRE** : travail identifié mais non commencé ;
- **LIMITE** : contrainte méthodologique ou technique connue ;
- **DÉCISION** : choix méthodologique à conserver.

---

## 2. Présentation du projet

### 2.1 Contexte

Trends est un projet du département Statistiques de Gaea21 visant à collecter, structurer, analyser et valoriser des données afin de produire des informations exploitables et des visualisations interactives.

Le sous-projet documenté ici porte sur le tourisme international en Afrique.

### 2.2 Problématique

Les données touristiques existent dans plusieurs bases et publications institutionnelles, mais elles ne sont pas directement comparables.

Les principales difficultés rencontrées sont :
- des sources différentes ;
- des périodes de couverture différentes ;
- des formats différents ;
- des unités différentes ;
- des niveaux de granularité différents ;
- des valeurs manquantes ;
- des périmètres de couverture variables selon les destinations.

La problématique de travail est donc :

> Comment transformer des données touristiques ouvertes et hétérogènes en informations fiables, comparables, traçables et exploitables pour l'analyse ?

### 2.3 Objectif principal

Construire une base analytique permettant d'étudier l'évolution du tourisme international dans sept destinations africaines selon trois dimensions principales :
1. les arrivées touristiques internationales ;
2. les recettes touristiques internationales ;
3. la provenance des visiteurs.

### 2.4 Destinations étudiées

Le périmètre comprend sept destinations :
- Afrique du Sud ;
- Égypte ;
- Kenya ;
- Maroc ;
- Maurice ;
- Tanzanie ;
- Tunisie.

### 2.5 Principe directeur

**DÉCISION - Aucune comparaison ne doit être réalisée sans contrôle préalable de la source, de la définition, de la période, de l'unité, de la granularité et du périmètre de couverture.**

---

## 3. Organisation technique du projet

### 3.1 Architecture cible du dépôt

```text
trends-tourisme-afrique/
|
|-- README.md
|-- requirements.txt
|-- .gitignore
|
|-- dashboard/
|   `-- app.py
|
|-- data/
|   |-- raw/
|   |-- processed/
|   `-- final/
|       |-- dataset_maitre_trends_tourisme_afrique.csv
|       `-- dataset_maitre_trends_tourisme_afrique.xlsx
|
|-- docs/
|   |-- project_documentation.md
|   |-- methodology.md
|   |-- data_sources.md
|   |-- data_dictionary.md
|   `-- handover_guide.md
|
|-- notebooks/
|   `-- 01_analyse_exploratoire.ipynb
|
|-- reports/
|   |-- figures/
|   `-- exports/
|
`-- src/
    |-- data_processing.py
    |-- indicators.py
    `-- visualizations.py
```

### 3.2 Technologies utilisées

- Python
- pandas
- Streamlit
- Altair
- Plotly
- Jupyter Notebook
- Git
- GitHub

### 3.3 Rôle des principaux dossiers

- `data/raw/` : données brutes lorsqu'elles peuvent être conservées dans le dépôt ;
- `data/processed/` : données intermédiaires nettoyées ou harmonisées ;
- `data/final/` : dataset maître destiné à l'analyse et au dashboard ;
- `notebooks/` : analyses exploratoires ;
- `dashboard/` : application Streamlit ;
- `src/` : fonctions Python réutilisables ;
- `docs/` : documentation méthodologique et technique ;
- `reports/` : figures et exports produits par les analyses.

---

## 4. Recherche et collecte des données

**Statut : TERMINÉ pour la collecte principale / EN COURS pour la consolidation documentaire.**

### 4.1 Stratégie de collecte

La collecte a privilégié les sources institutionnelles et officielles.

Deux familles de sources ont été utilisées :
- une source internationale harmonisée pour les séries d'arrivées et de recettes ;
- des sources nationales ou rapports statistiques pour la provenance détaillée des touristes.

La traçabilité détaillée sera centralisée dans `docs/data_sources.md`.

### 4.2 Arrivées touristiques internationales

**Source principale identifiée : Banque mondiale - World Development Indicators.**

Fichier de travail utilisé :
`WB_WDI_ST_INT_ARVL_WIDEF.csv`

Indicateur :
`ST.INT.ARVL` - arrivées touristiques internationales.

Le jeu harmonisé contient les observations correspondant aux sept destinations retenues.

### 4.3 Recettes touristiques internationales

**Source principale identifiée : Banque mondiale - World Development Indicators.**

Fichier de travail utilisé :
`WB_WDI_ST_INT_RCPT_CD_WIDEF.csv`

Indicateur :
`ST.INT.RCPT.CD` - recettes du tourisme international en dollars courants.

### 4.4 Provenance des touristes

La provenance n'a pas pu être obtenue dans une source internationale unique avec un niveau de détail homogène. Des sources nationales ont donc été utilisées.

Fichiers standardisés produits :
- `maroc_provenance_touristique_2012_2020_open_data.xlsx`
- `tunisie_provenance_touristique_2017_2023_ONTT.xlsx`
- `kenya_provenance_touristique_2022_2024_TRI.xlsx`
- `tanzania_tourism_provenance_2022_2024_NBS.xlsx`
- `maurice_provenance_touristique_2022_2024_statistics_mauritius.xlsx`
- `afrique_du_sud_provenance_touristique_2022_2024_stats_sa.xlsx`
- `egypte_provenance_touristique_donnees_verifiees.xlsx`

**LIMITE - Les sources, périodes, granularités et couvertures de provenance ne sont pas homogènes entre les sept destinations.**

Les organismes, documents exacts, URL, dates d'accès, unités et périmètres seront recensés dans `docs/data_sources.md`. Aucun lien ne doit être ajouté sans vérification de la source originale.

---

## 5. Audit de qualité et de comparabilité

**Statut : TERMINÉ.**

Un audit a été réalisé avant toute comparaison afin d'éviter de considérer comme équivalentes des observations qui ne mesurent pas exactement la même chose.

Fichier principal :
`audit_comparabilite_7_pays_trends.xlsx`

### 5.1 Critères contrôlés

Les contrôles portent notamment sur :
- la source ;
- la définition de l'indicateur ;
- la période disponible ;
- l'unité ;
- la granularité ;
- la couverture ;
- les valeurs manquantes ;
- le périmètre réellement comparable.

### 5.2 Comparabilité de la provenance

Résumé des niveaux de comparabilité actuellement retenus :

- **Maroc - GREEN** : arrivées exactes par provenance, 2012-2020.
- **Tunisie - GREEN** : données exactes par provenance, 2017-2023.
- **Kenya - ORANGE** : données exactes 2022-2024, couverture Top 30.
- **Tanzanie - RED** : volumes détaillés indisponibles dans le jeu retenu ; utilisation de parts pour un Top 15, 2022-2024.
- **Maurice - ORANGE** : données exactes 2022-2024, couverture limitée à sept marchés.
- **Afrique du Sud - ORANGE** : données exactes 2022-2024, panel limité.
- **Égypte - RED** : données pays vérifiées limitées aux États-Unis sur 2010-2019, complétées par des agrégats régionaux pour 2019.

**DÉCISION - Les catégories GREEN / ORANGE / RED servent à empêcher les comparaisons qui dépassent le périmètre réellement supporté par les sources.**

---

## 6. Nettoyage et harmonisation

**Statut : TERMINÉ.**

### 6.1 Objectif

Transformer les différentes sources en jeux de données cohérents et exploitables sans fabriquer d'information absente.

### 6.2 Règles principales

**DÉCISION - Une donnée manquante n'est jamais transformée en zéro.**

**DÉCISION - Aucune interpolation ou fabrication de valeur n'est effectuée sans justification explicite.**

**DÉCISION - Les volumes, parts, pays et agrégats régionaux restent distingués.**

**DÉCISION - Les informations de source, couverture, granularité et qualité sont conservées lorsque nécessaire pour l'interprétation.**

### 6.3 Fichiers harmonisés

Arrivées :
`audit_harmonisation_arrivees_7_pays_trends.xlsx`

Recettes :
`audit_harmonisation_recettes_7_pays_trends.xlsx`

Provenance :
`harmonisation_provenance_7_pays_trends.xlsx`

---

## 7. Construction du dataset maître

**Statut : TERMINÉ.**

Fichiers finaux :
- `dataset_maitre_trends_tourisme_afrique.csv`
- `dataset_maitre_trends_tourisme_afrique.xlsx`

### 7.1 Structure générale

Le dataset maître rassemble trois couches :
- `arrivals`
- `receipts`
- `provenance`

Il contient **1 080 observations** réparties comme suit :
- 182 observations d'arrivées ;
- 182 observations de recettes ;
- 716 observations de provenance.

Les sept destinations sont présentes.

### 7.2 Principe

Le dataset maître n'a pas pour objectif de masquer l'hétérogénéité des sources. Il fournit un schéma commun tout en conservant les informations nécessaires pour déterminer quelles comparaisons sont valides.

---

## 8. Analyse exploratoire

**Statut : EN COURS - approfondissement demandé après revue avec le coordinateur.**

Notebook :
`notebooks/01_analyse_exploratoire.ipynb`

### 8.1 Travail déjà engagé

Les premiers contrôles ont porté sur :
- dimensions du dataset ;
- structure des variables ;
- destinations ;
- couches de données ;
- valeurs manquantes ;
- couverture générale.

### 8.2 Structure cible de l'EDA approfondie

L'analyse sera développée selon les axes suivants :

1. qualité et couverture du dataset ;
2. évolution des arrivées touristiques ;
3. évolution des recettes ;
4. analyse croisée arrivées / recettes ;
5. rupture de 2020 ;
6. reprise post-Covid ;
7. croissance et trajectoires des destinations ;
8. provenance des visiteurs ;
9. comparabilité des marchés d'origine ;
10. synthèse des enseignements ;
11. sélection des indicateurs destinés au dashboard.

### 8.3 Format documentaire du notebook

Chaque analyse importante suivra la structure :

**Markdown -> Code -> Interprétation**

Le notebook doit permettre de comprendre :
- la question posée ;
- la méthode ou le calcul utilisé ;
- le résultat ;
- son interprétation ;
- les limites éventuelles.

---

## 9. Dashboard Streamlit

**Statut : EN COURS - prototype fonctionnel à refondre sur la forme.**

Fichier :
`dashboard/app.py`

### 9.1 Objectif

Fournir une interface interactive permettant d'explorer les résultats sans avoir à manipuler directement le dataset ou le notebook.

### 9.2 Structure fonctionnelle actuelle

Trois onglets :
- Tendances ;
- Provenance ;
- Carte.

### 9.3 Template Gaea21

Le dashboard utilise déjà plusieurs principes du modèle Gaea21 :
- Streamlit ;
- thème corporate ;
- Altair ;
- Plotly ;
- cache des données ;
- onglets ;
- exports CSV.

### 9.4 Correction demandée après revue coordinateur

**À FAIRE - Replacer les filtres dans la barre latérale gauche (`st.sidebar`) afin de respecter davantage la structure du template Gaea21.**

Les filtres devront être adaptés au contexte de chaque analyse tout en laissant la zone centrale prioritairement consacrée aux résultats et visualisations.

### 9.5 Autres améliorations prévues

- approfondir les indicateurs à partir des résultats de l'EDA ;
- harmoniser le thème Altair avec l'identité corporate ;
- vérifier tous les contrastes et libellés ;
- maintenir les précautions méthodologiques dans l'interface ;
- tester chaque onglet et chaque filtre avant finalisation.

---

## 10. Règles méthodologiques à conserver

Ces règles sont essentielles pour toute personne reprenant le projet.

1. **Donnée manquante != zéro.**
2. **Ne pas interpoler ou inventer des valeurs sans justification.**
3. **Ne pas comparer des unités différentes comme si elles étaient équivalentes.**
4. **Ne pas traiter une part comme un volume exact.**
5. **Ne pas traiter un agrégat régional comme un pays.**
6. **Toujours contrôler source, période, unité, granularité et couverture avant comparaison.**
7. **Conserver les limites de couverture dans les analyses et visualisations.**
8. **Ne pas transformer un panel partiel en classement exhaustif.**
9. **Documenter toute nouvelle transformation importante.**

---

## 11. Reproductibilité

**Statut : EN COURS de documentation.**

### 11.1 Installation

Depuis la racine du dépôt :

```powershell
py -m pip install -r requirements.txt
```

### 11.2 Lancement du dashboard

```powershell
py -m streamlit run dashboard/app.py
```

### 11.3 Analyse exploratoire

Ouvrir :
`notebooks/01_analyse_exploratoire.ipynb`

Le notebook doit utiliser le dataset maître présent dans `data/final/`.

### 11.4 Versionnement

Après validation d'une étape :
1. enregistrer les fichiers ;
2. mettre à jour la documentation ;
3. contrôler les changements Git ;
4. créer un commit explicite ;
5. pousser la version validée vers le dépôt distant.

---

## 12. Limites connues

### 12.1 Provenance

La provenance est la dimension la moins homogène du dataset. Les pays ne disposent pas tous des mêmes périodes, marchés ou unités.

### 12.2 Égypte

Les données pays vérifiées disponibles dans le jeu de provenance sont limitées. Elles ne permettent pas d'établir un classement exhaustif des marchés d'origine.

### 12.3 Tanzanie

Les données retenues reposent sur des parts pour la provenance et ne doivent pas être interprétées comme des volumes exacts.

### 12.4 Panels partiels

Certaines destinations disposent uniquement d'un Top N ou d'un panel de marchés. Ces données restent utiles pour une analyse interne à leur périmètre mais ne doivent pas être présentées comme une couverture exhaustive.

---

## 13. État d'avancement

| Étape | Statut |
|---|---|
| Cadrage du projet | TERMINÉ |
| Revue documentaire | TERMINÉ |
| Mindmap | TERMINÉ |
| Sélection des indicateurs | TERMINÉ |
| Collecte des données | TERMINÉ |
| Audit de comparabilité | TERMINÉ |
| Harmonisation | TERMINÉ |
| Dataset maître | TERMINÉ |
| Organisation Git / GitHub | TERMINÉ |
| Analyse exploratoire | EN COURS |
| Documentation complète | EN COURS |
| Dashboard Streamlit | EN COURS |
| Refonte conforme au template Gaea21 | À FAIRE |
| Tests finaux | À FAIRE |
| Handover final | À FAIRE |

---

## 14. Prochaines étapes

Ordre de travail recommandé :

1. compléter `docs/data_sources.md` avec les sources exactes et vérifiées ;
2. consolider `docs/methodology.md` ;
3. créer `docs/data_dictionary.md` ;
4. approfondir `01_analyse_exploratoire.ipynb` ;
5. sélectionner les indicateurs finaux issus de l'EDA ;
6. refondre le dashboard avec les filtres dans `st.sidebar` ;
7. effectuer les tests fonctionnels et méthodologiques ;
8. compléter `docs/handover_guide.md` ;
9. mettre à jour le README ;
10. réaliser une revue finale du dépôt.

---

## 15. Historique des modifications

| Date | Modification | Statut |
|---|---|---|
| 2026-09-08 | Création de la structure documentaire centrale du projet | TERMINÉ |
| 2026-09-08 | Ajout du principe de traçabilité des sources | TERMINÉ |
| 2026-09-08 | Ajout de la demande de refonte des filtres selon le template Gaea21 | TERMINÉ |
| 2026-09-08 | Planification de l'approfondissement de l'EDA | EN COURS |

---

## 16. Documents associés

La documentation finale sera répartie entre :

- `README.md` - porte d'entrée du dépôt ;
- `docs/project_documentation.md` - historique et déroulement complet ;
- `docs/data_sources.md` - registre des sources et de leur traçabilité ;
- `docs/methodology.md` - décisions et règles méthodologiques ;
- `docs/data_dictionary.md` - définition des variables du dataset maître ;
- `docs/handover_guide.md` - instructions pour la reprise du projet.

**Règle de maintenance : toute modification importante des données, de la méthodologie, de l'EDA ou du dashboard doit entraîner une vérification de la documentation associée.**

## Phase de correction des métadonnées — 8 septembre 2026

**Statut : corrections approuvées mises en œuvre par une procédure reproductible.**

Script : `src/metadata_corrections.py` ; commande : `python -B src/metadata_corrections.py`.
Journal : `reports/exports/metadata_corrections_log.csv`.

Périmètre : 7 lignes Tunisie/Scandinaves reclassées `regional_aggregate` / `exact_aggregate`, 1 ligne Kenya/ONU reclassée `institutional_category` (drapeau `exact_top30` conservé), 60 valeurs tunisiennes absentes étiquetées `missing_unverified`. Les notes sont complétées sans effacer les précédentes. Les nouvelles modalités sont définies dans `data_dictionary.md` et `methodology.md`.

`institutional_category` distingue une catégorie institutionnelle d'un pays, d'une région ou d'un total. `missing_unverified` signifie que la cause de l'absence n'a pas été vérifiée dans la source originale : ni zéro, ni `missing_in_source`.

`country` ne signifie pas automatiquement que toute catégorie publiée par une source est géographiquement un pays ; les catégories institutionnelles et agrégées doivent être explicitement distinguées.

Réunion reste un marché source distinct (`Reunion Island`, `country`), sans fusion avec France. Pour les dix observations Égypte–États-Unis, l'attribution CAPMAS mentionnée dans l'historique documentaire n'est pas reliée de façon vérifiable aux pièces présentes dans le dépôt ; `User-provided source file` reste inchangé.

Les 1 080 lignes, toutes les valeurs numériques, les libellés sources, les destinations, les années et les références sont préservés. Le CSV et les cellules textuelles concernées du XLSX sont synchronisés sans reconstruction du classeur. Le script est idempotent et journalise uniquement les métadonnées effectivement modifiées.

L'EDA, les dashboards, les KPI et les correspondances multilingues ne sont pas modifiés pendant cette phase. Les fichiers sources intermédiaires et publications originales restent à retrouver avant de lever les réserves documentaires.
