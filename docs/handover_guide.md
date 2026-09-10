# Guide de reprise — Projet Trends
## Tourisme international dans les principales destinations africaines

**Projet :** Trends — Gaea21  
**Document :** Guide de reprise / handover  
**Dernière mise à jour :** 8 septembre 2026  
**Statut du projet :** En cours — dataset maître construit, documentation structurée, EDA à approfondir et dashboard à refondre/finaliser.

---

# 1. Objectif de ce guide

Ce document permet à une nouvelle personne de reprendre le projet sans devoir reconstituer tout l'historique du travail.

Il répond principalement aux questions suivantes :

- Quel est l'objectif du projet ?
- Où sont les fichiers importants ?
- Quel est l'état réel d'avancement ?
- Comment lancer l'environnement de travail ?
- Comment contrôler le dataset ?
- Quelles règles méthodologiques ne doivent pas être cassées ?
- Où reprendre concrètement le travail ?
- Dans quel ordre poursuivre les prochaines étapes ?
- Quels documents doivent être mis à jour après une modification ?

Ce guide ne remplace pas les autres documents de `docs/`. Il indique comment les utiliser ensemble.

---

# 2. Résumé du projet

Le projet étudie l'évolution et les tendances du tourisme international dans sept destinations africaines :

```text
Afrique du Sud
Égypte
Kenya
Maroc
Maurice
Tanzanie
Tunisie
```

Trois dimensions principales sont étudiées :

```text
arrivées touristiques internationales
recettes touristiques internationales
provenance des visiteurs
```

Le travail a été conçu selon une logique de Data Science :

```text
comprendre
→ collecter
→ auditer
→ harmoniser
→ analyser
→ visualiser
→ interpréter
→ documenter
```

Le principe directeur est de ne pas forcer une comparaison lorsque les sources, unités, périodes, granularités ou couvertures ne permettent pas de la défendre méthodologiquement.

---

# 3. État du projet au 8 septembre 2026

| Étape | Statut | Commentaire |
|---|---|---|
| Cadrage de la thématique | TERMINÉ | Périmètre et problématique définis |
| Sélection initiale des indicateurs | TERMINÉ | Arrivées, recettes, provenance |
| Collecte des données | TERMINÉ | Sources internationales et nationales |
| Audit de comparabilité | TERMINÉ | Limites identifiées |
| Harmonisation | TERMINÉ | Schéma commun construit |
| Dataset maître | TERMINÉ | 1 080 observations |
| Git / GitHub | EN PLACE | Dépôt structuré |
| Documentation de base | TERMINÉE | 5 documents dans `docs/` après ajout de ce guide |
| EDA initiale | ENGAGÉE | Doit être approfondie |
| Sélection finale des KPI dashboard | À FAIRE | Doit découler de l'EDA approfondie |
| Dashboard Streamlit V1 | FONCTIONNEL | Prototype existant, pas version finale |
| Refonte selon template Gaea21 | À FAIRE | Filtres principaux à placer dans `st.sidebar` |
| Validation finale | À FAIRE | Tests données + interface |
| Handover final | EN COURS | Ce guide en constitue la base |

> Ne pas présenter le dashboard actuel comme un livrable terminé. Il s'agit d'une V1 fonctionnelle / base de démonstration.

---

# 4. Arborescence cible du dépôt

```text
trends-tourisme-afrique/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── final/
│       ├── dataset_maitre_trends_tourisme_afrique.csv
│       └── dataset_maitre_trends_tourisme_afrique.xlsx
│
├── docs/
│   ├── project_documentation.md
│   ├── data_sources.md
│   ├── methodology.md
│   ├── data_dictionary.md
│   └── handover_guide.md
│
├── notebooks/
│   └── 01_analyse_exploratoire.ipynb
│
├── reports/
│   ├── figures/
│   └── exports/
│
└── src/
    ├── data_processing.py
    ├── indicators.py
    └── visualizations.py
```

---

# 5. Rôle des fichiers principaux

## `README.md`

Point d'entrée du dépôt.

Il doit présenter :
- le projet ;
- le périmètre ;
- l'installation ;
- le lancement ;
- la structure ;
- les principaux livrables.

## `data/final/dataset_maitre_trends_tourisme_afrique.csv`

Dataset principal utilisé par le notebook et le dashboard.

Ne pas modifier manuellement des valeurs dans ce fichier sans pouvoir reproduire la modification depuis la chaîne de traitement.

## `notebooks/01_analyse_exploratoire.ipynb`

Notebook d'analyse exploratoire.

C'est le prochain livrable analytique à approfondir.

## `dashboard/app.py`

Application Streamlit.

La V1 permet déjà d'explorer :
- les tendances ;
- la provenance ;
- la carte.

Une refonte reste nécessaire pour mieux suivre le template Gaea21.

## `src/data_processing.py`

Fonctions liées au chargement et aux contrôles généraux des données.

## `src/indicators.py`

Emplacement prévu pour les calculs d'indicateurs réutilisables.

## `src/visualizations.py`

Emplacement prévu pour les fonctions de visualisation réutilisables.

---

# 6. Documentation à lire avant de modifier le projet

Ordre recommandé :

```text
1. README.md
2. docs/project_documentation.md
3. docs/data_sources.md
4. docs/methodology.md
5. docs/data_dictionary.md
6. docs/handover_guide.md
7. notebooks/01_analyse_exploratoire.ipynb
8. dashboard/app.py
```

### Pourquoi cet ordre ?

`project_documentation.md` explique l'historique.

`data_sources.md` explique d'où viennent les données.

`methodology.md` explique ce qu'il est permis ou non de comparer.

`data_dictionary.md` explique les 17 colonnes du dataset.

Le notebook montre l'analyse.

Le dashboard montre la valorisation interactive.

---

# 7. Préparer l'environnement

## 7.1 Prérequis

Environnement recommandé :

```text
Python 3.9+
VS Code
Git
```

Bibliothèques principales utilisées :

```text
pandas
streamlit
altair
plotly
```

D'autres dépendances peuvent être présentes dans `requirements.txt`.

## 7.2 Ouvrir le projet

Sous Windows / PowerShell :

```powershell
cd C:\Users\user\OneDrive\Documents\GitHub\trends-tourisme-afrique
```

Vérifier ensuite :

```powershell
git status
```

## 7.3 Installer les dépendances

Depuis la racine du dépôt :

```powershell
py -m pip install -r requirements.txt
```

Si la commande `py` n'est pas disponible :

```powershell
python -m pip install -r requirements.txt
```

## 7.4 Vérifier les bibliothèques principales

```powershell
py -c "import pandas, streamlit, altair, plotly; print('Environnement OK')"
```

---

# 8. Lancer le dashboard

Depuis la racine du dépôt :

```powershell
py -m streamlit run dashboard/app.py
```

Alternative :

```powershell
python -m streamlit run dashboard/app.py
```

Streamlit ouvre normalement l'application dans le navigateur.

Pour arrêter le serveur :

```text
Ctrl + C
```

---

# 9. Lancer le notebook

Dans VS Code :

1. ouvrir `notebooks/01_analyse_exploratoire.ipynb` ;
2. sélectionner l'environnement Python du projet ;
3. exécuter les cellules dans l'ordre ;
4. vérifier qu'aucune cellule ne dépend d'un état manuel non documenté.

Le notebook doit pouvoir être exécuté depuis le début sans intervention cachée.

---

# 10. Dataset maître

Le dataset principal est :

```text
data/final/dataset_maitre_trends_tourisme_afrique.csv
```

État connu :

```text
1 080 observations
7 destinations
3 couches
17 colonnes
```

Répartition connue :

```text
arrivals     182 observations
receipts     182 observations
provenance   716 observations
```

Les 17 variables sont documentées dans :

```text
docs/data_dictionary.md
```

---

# 11. Contrôles à effectuer après chargement

Avant toute nouvelle analyse :

```python
print(df.shape)
print(df.columns.tolist())
print(df.dtypes)
print(df.isna().sum())
print(df["destination"].value_counts())
print(df["dataset_layer"].value_counts())
```

Contrôler également :

```python
df.duplicated().sum()
df["unit"].value_counts(dropna=False)
df["granularity"].value_counts(dropna=False)
df["metric_type"].value_counts(dropna=False)
df["quality_flag"].value_counts(dropna=False)
```

Un changement inattendu doit être investigué avant de continuer.

---

# 12. Règles méthodologiques à ne jamais casser

## 12.1 Valeur manquante

```text
NaN ≠ 0
```

Ne jamais remplacer automatiquement les valeurs absentes par zéro.

## 12.2 Pas de fabrication

Ne pas :
- inventer une valeur ;
- interpoler silencieusement ;
- reconstruire un volume à partir d'une part sans base méthodologique vérifiée.

## 12.3 Unités

```text
persons ≠ share ≠ current_USD
```

Ne jamais combiner directement des unités différentes.

## 12.4 Granularités

```text
country ≠ regional_aggregate ≠ aggregate_total ≠ diaspora
```

Un agrégat régional ne doit pas être classé comme un pays.

## 12.5 Totaux

Ne pas additionner un agrégat avec ses propres composantes.

## 12.6 MRE / TRE

Les populations de diaspora distinguées dans les sources restent séparées des touristes étrangers lorsque la source les distingue.

## 12.7 Top N / panels

Un Top 30, Top 15 ou panel partiel reste partiel après harmonisation.

L'harmonisation de la structure ne rend pas la couverture exhaustive.

---

# 13. Cas particuliers à connaître

## Maroc

Comparabilité de provenance classée GREEN dans l'audit actuel.

Période principale :

```text
2012–2020
```

## Tunisie

Comparabilité classée GREEN.

Période principale :

```text
2017–2023
```

Attention :
- agrégats publiés ;
- TRE ;
- nationalités.

## Kenya

Comparabilité classée ORANGE.

```text
2022–2024
Top 30
```

Ne pas présenter le Top 30 comme une couverture exhaustive.

## Tanzanie

Comparabilité classée RED.

```text
2022–2024
Top 15
unité = share
```

Ne jamais traiter ces parts comme des volumes exacts de personnes.

## Maurice

Comparabilité classée ORANGE.

```text
2022–2024
panel de 7 marchés
```

## Afrique du Sud

Comparabilité classée ORANGE.

```text
2022–2024
panel de 18 marchés
```

## Égypte

Comparabilité classée RED.

La couverture pays vérifiée intégrée est limitée aux États-Unis pour 2010–2019, complétée par des agrégats régionaux pour 2019.

Ne pas :
- présenter les États-Unis comme premier marché ;
- construire un classement exhaustif ;
- mélanger pays et régions ;
- mélanger part des touristes et part des nuitées.

---

# 14. Où reprendre le projet aujourd'hui ?

## PRIORITÉ 1 — Auditer le notebook EDA actuel

Ouvrir :

```text
notebooks/01_analyse_exploratoire.ipynb
```

Faire l'inventaire de :
- ce qui existe déjà ;
- ce qui est correct ;
- ce qui doit être approfondi ;
- ce qui doit être supprimé ou déplacé ;
- ce qui manque.

Ne pas repartir de zéro si les cellules existantes sont correctes.

## PRIORITÉ 2 — Approfondir l'EDA

Structure cible :

```text
01 — Introduction et objectifs de l'EDA

02 — Chargement et validation du dataset maître

03 — Structure et qualité des données
     3.1 Dimensions du dataset
     3.2 Types de variables
     3.3 Valeurs manquantes
     3.4 Doublons
     3.5 Couverture par dimension
     3.6 Couverture temporelle par destination

04 — Analyse des arrivées touristiques
     4.1 Évolution globale
     4.2 Comparaison des 7 destinations
     4.3 Tendances avant 2020
     4.4 Rupture de 2020
     4.5 Reprise post-Covid
     4.6 Niveaux récents

05 — Analyse des recettes touristiques
     5.1 Évolution globale
     5.2 Comparaison entre destinations
     5.3 Rupture de 2020
     5.4 Reprise post-Covid
     5.5 Niveaux récents

06 — Analyse croisée arrivées × recettes
     6.1 Relation arrivées/recettes
     6.2 Recette par arrivée lorsque calculable
     6.3 Différences entre destinations
     6.4 Précautions d'interprétation

07 — Dynamique et croissance
     7.1 Variations annuelles
     7.2 Croissance pré-Covid
     7.3 Chute 2020
     7.4 Vitesse de reprise
     7.5 Retour ou non au niveau pré-Covid

08 — Analyse des provenances
     8.1 Couverture disponible
     8.2 Maroc
     8.3 Tunisie
     8.4 Kenya
     8.5 Tanzanie
     8.6 Maurice
     8.7 Afrique du Sud
     8.8 Égypte
     8.9 Comparaisons réellement possibles

09 — Synthèse comparative des 7 destinations

10 — Limites méthodologiques de l'EDA

11 — Enseignements principaux

12 — Indicateurs retenus pour le dashboard
```

---

# 15. Format attendu dans le notebook

Chaque bloc analytique doit suivre :

```text
Markdown — question / objectif
        ↓
Code
        ↓
Résultat / graphique
        ↓
Markdown — interprétation
```

Éviter un notebook composé uniquement de cellules de code.

Chaque graphique doit répondre à une question.

Chaque interprétation doit rester limitée à ce que les données démontrent réellement.

---

# 16. Après l'EDA : sélectionner les indicateurs

La sélection initiale des trois dimensions est déjà faite.

La **sélection finale des KPI et visualisations du dashboard** doit être réalisée après l'EDA approfondie.

Exemples d'indicateurs à évaluer :

```text
niveau récent des arrivées
niveau récent des recettes
variation annuelle
chute 2020
taux de reprise
écart au niveau pré-Covid
recette par arrivée
principaux marchés disponibles
parts de marchés lorsque disponibles
```

Un KPI ne doit être retenu que s'il :
- apporte une information utile ;
- est calculable de manière fiable ;
- est compréhensible ;
- respecte la comparabilité ;
- peut être expliqué méthodologiquement.

---

# 17. Refonte du dashboard

Le dashboard actuel est une V1 fonctionnelle.

La refonte devra conserver les éléments utiles tout en s'alignant davantage sur le modèle Gaea21.

## Exigence principale

Les filtres principaux doivent être placés dans :

```python
st.sidebar
```

afin de libérer la zone principale.

## Architecture à conserver / adapter

Le modèle Gaea21 utilise :
- une configuration globale ;
- une palette corporate ;
- du CSS ;
- `@st.cache_data` ;
- des onglets ;
- des filtres dans la sidebar ;
- `st.session_state` lorsque nécessaire ;
- Altair pour les graphiques ;
- Plotly pour la carte ;
- des exports CSV.

## Dashboard Trends cible

Les trois espaces fonctionnels actuels peuvent rester une bonne base :

```text
Tendances
Provenance
Carte
```

Le contenu exact doit toutefois découler de l'EDA approfondie.

---

# 18. Contrôles avant modification du dashboard

Avant de modifier `dashboard/app.py` :

```text
[ ] Le dataset maître fonctionne
[ ] Le notebook a été exécuté
[ ] L'indicateur est validé dans l'EDA
[ ] L'unité est connue
[ ] La granularité est connue
[ ] La couverture est connue
[ ] Le quality_flag est compris
[ ] Le comportement des valeurs manquantes est défini
[ ] Le cas Égypte/Tanzanie est traité si concerné
```

Après modification :

```text
[ ] Le dashboard démarre sans erreur
[ ] Les filtres fonctionnent
[ ] Les valeurs correspondent au dataset
[ ] Les valeurs manquantes ne deviennent pas zéro
[ ] Les parts sont affichées correctement
[ ] Les exports conservent les valeurs brutes
[ ] La carte utilise les bons codes pays
[ ] Les avertissements méthodologiques restent visibles
```

---

# 19. Tests minimums du dashboard

Lancer :

```powershell
py -m streamlit run dashboard/app.py
```

Puis tester manuellement :

```text
Tendances → arrivées
Tendances → recettes
plusieurs plages d'années
une seule destination
les sept destinations
Provenance → Maroc
Provenance → Tunisie
Provenance → Kenya
Provenance → Tanzanie
Provenance → Maurice
Provenance → Afrique du Sud
Provenance → Égypte
Carte → arrivées
Carte → recettes
années avec données manquantes
exports CSV
```

---

# 20. Workflow Git recommandé

Avant une session :

```powershell
git status
git pull
```

Après une étape cohérente :

```powershell
git status
git add .
git commit -m "description claire de la modification"
git push
```

Exemples de commits :

```text
docs: add project handover guide
eda: deepen arrivals analysis
eda: add post-covid recovery indicators
dashboard: move filters to sidebar
dashboard: add validated recovery KPI
docs: update methodology after EDA
```

Éviter un seul commit regroupant de nombreuses modifications sans rapport entre elles.

---

# 21. Cycle de travail recommandé

Pour la suite du projet :

```text
TRAVAIL
   ↓
CONTRÔLE
   ↓
INTERPRÉTATION
   ↓
DOCUMENTATION
   ↓
GIT
   ↓
ÉTAPE SUIVANTE
```

La documentation doit être mise à jour pendant le projet, pas uniquement à la fin.

---

# 22. Chaîne de traçabilité à conserver

Pour toute donnée :

```text
SOURCE
   ↓
COLLECTE
   ↓
FICHIER BRUT
   ↓
AUDIT
   ↓
HARMONISATION
   ↓
DATASET MAÎTRE
   ↓
EDA
   ↓
INDICATEUR
   ↓
DASHBOARD
   ↓
INTERPRÉTATION
```

Une nouvelle transformation doit pouvoir être replacée dans cette chaîne.

---

# 23. Quand mettre à jour quel document ?

## Nouvelle source

Mettre à jour :

```text
docs/data_sources.md
```

et si nécessaire :

```text
docs/methodology.md
docs/data_dictionary.md
```

## Nouvelle règle méthodologique

Mettre à jour :

```text
docs/methodology.md
```

## Nouvelle colonne ou nouvelle catégorie

Mettre à jour :

```text
docs/data_dictionary.md
```

## Nouvelle étape importante ou décision de projet

Mettre à jour :

```text
docs/project_documentation.md
```

## Modification importante de la procédure de reprise

Mettre à jour :

```text
docs/handover_guide.md
```

---

# 24. Que faire si une donnée semble incorrecte ?

Ne pas la corriger directement dans le dataset final.

Procédure :

```text
1. Identifier l'observation
2. Lire source_name
3. Lire source_reference
4. Lire source_file
5. Lire quality_flag
6. Lire notes
7. Consulter docs/data_sources.md
8. Revenir au fichier source / harmonisé
9. Vérifier la donnée
10. Corriger la chaîne de traitement
11. Régénérer le résultat
12. Documenter la correction
13. Commit Git
```

---

# 25. Que faire si une nouvelle source contredit une ancienne ?

Ne pas remplacer immédiatement l'ancienne donnée.

Comparer :
- définition ;
- période ;
- unité ;
- fréquence ;
- couverture ;
- organisme ;
- méthodologie.

Déterminer ensuite si la nouvelle source :
- corrige l'ancienne ;
- mesure autre chose ;
- constitue une révision ;
- complète une période ;
- n'est pas comparable.

Documenter la décision.

---

# 26. Fichiers de collecte/harmonisation importants

Les fichiers historiques associés au projet comprennent notamment :

```text
WB_WDI_ST_INT_ARVL_WIDEF.csv
WB_WDI_ST_INT_RCPT_CD_WIDEF.csv

audit_comparabilite_7_pays_trends.xlsx
audit_harmonisation_arrivees_7_pays_trends.xlsx
audit_harmonisation_recettes_7_pays_trends.xlsx
harmonisation_provenance_7_pays_trends.xlsx

maroc_provenance_touristique_2012_2020_open_data.xlsx
tunisie_provenance_touristique_2017_2023_ONTT.xlsx
kenya_provenance_touristique_2022_2024_TRI.xlsx
tanzania_tourism_provenance_2022_2024_NBS.xlsx
maurice_provenance_touristique_2022_2024_statistics_mauritius.xlsx
afrique_du_sud_provenance_touristique_2022_2024_stats_sa.xlsx
egypte_provenance_touristique_donnees_verifiees.xlsx
```

Le registre détaillé est :

```text
docs/data_sources.md
```

---

# 27. Points restant à vérifier dans la documentation des sources

Certains organismes sont identifiés, mais certaines références exactes/URL doivent encore être consolidées à partir des archives de collecte.

Ne jamais compléter ces champs par supposition.

Utiliser :

```text
À VÉRIFIER
```

tant que la référence originale n'est pas retrouvée.

---

# 28. Definition of Done — EDA

L'EDA pourra être considérée comme suffisamment avancée lorsque :

```text
[ ] structure et qualité analysées
[ ] couverture temporelle explicitée
[ ] arrivées analysées
[ ] recettes analysées
[ ] rupture 2020 analysée
[ ] reprise post-Covid quantifiée
[ ] arrivées × recettes étudiées
[ ] provenance étudiée destination par destination
[ ] limites de comparabilité rappelées
[ ] principaux enseignements rédigés
[ ] KPI dashboard sélectionnés
[ ] notebook exécutable du début à la fin
```

---

# 29. Definition of Done — Dashboard

Le dashboard pourra être considéré comme finalisable lorsque :

```text
[ ] KPI issus de l'EDA
[ ] filtres principaux dans st.sidebar
[ ] thème Gaea21 cohérent
[ ] navigation claire
[ ] graphiques lisibles
[ ] unités visibles
[ ] valeurs manquantes correctement gérées
[ ] cas particuliers correctement signalés
[ ] exports testés
[ ] carte testée
[ ] application testée sur les 7 destinations
[ ] documentation mise à jour
```

---

# 30. Definition of Done — Documentation

La documentation sera considérée comme complète lorsque :

```text
[ ] README à jour
[ ] project_documentation.md à jour
[ ] data_sources.md sans références critiques non vérifiées
[ ] methodology.md à jour
[ ] data_dictionary.md synchronisé avec le dataset
[ ] handover_guide.md synchronisé avec l'état final
[ ] commandes de lancement testées
[ ] prochaine étape identifiable sans explication orale
```

---

# 31. Priorités immédiates

À la date de ce guide, l'ordre recommandé est :

```text
1. Inspecter le notebook EDA actuel
2. Conserver les analyses correctes
3. Approfondir l'EDA
4. Rédiger les interprétations
5. Sélectionner les KPI finaux
6. Refondre le dashboard
7. Déplacer les filtres principaux dans st.sidebar
8. Tester les 7 destinations
9. Mettre à jour la documentation
10. Préparer la livraison finale
```

---

# 32. Résumé pour une reprise en 5 minutes

Si vous venez d'arriver sur le projet :

```text
1. Lisez README.md.
2. Lisez les 5 fichiers dans docs/.
3. Ne modifiez pas le dataset avant d'avoir lu methodology.md.
4. Ouvrez 01_analyse_exploratoire.ipynb.
5. Reprenez à l'EDA approfondie.
6. Ne refondez le dashboard qu'après sélection des KPI.
7. Placez les filtres principaux dans st.sidebar.
8. Ne transformez jamais une valeur manquante en zéro.
9. Respectez les unités, granularités et coverage_scope.
10. Documentez puis committez chaque étape importante.
```

---

# 33. Historique du guide

| Date | Modification |
|---|---|
| 2026-09-08 | Création du guide de reprise |
| 2026-09-08 | Formalisation de l'état d'avancement |
| 2026-09-08 | Ajout des procédures de lancement |
| 2026-09-08 | Ajout des règles de contrôle et de reprise |
| 2026-09-08 | Ajout du plan EDA cible |
| 2026-09-08 | Ajout des exigences de refonte du dashboard Gaea21 |
| 2026-09-08 | Ajout des Definition of Done |

---

## Conclusion

Le projet dispose désormais d'une base de données harmonisée, d'une première application Streamlit et d'une documentation structurée.

La prochaine personne ne doit pas recommencer la collecte ni reconstruire le projet depuis zéro.

**Le point de reprise opérationnel est l'analyse exploratoire approfondie.**

Cette analyse doit ensuite conduire à la sélection finale des indicateurs et à la refonte du dashboard, tout en conservant la priorité donnée à la comparabilité, à la traçabilité et à l'absence de fabrication des données.
