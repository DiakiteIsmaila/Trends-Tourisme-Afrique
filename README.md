# Trends — Tourisme international en Afrique

Projet d'analyse de Gaea21 consacré aux **arrivées touristiques**, aux **recettes touristiques** et à la **provenance des visiteurs** dans sept destinations : Afrique du Sud, Égypte, Kenya, Maroc, Maurice, Tanzanie et Tunisie.

## État et livrables

L'EDA est finalisée : les sections **01 à 12** de [l'analyse exploratoire](notebooks/01_analyse_exploratoire.ipynb) couvrent la qualité des données, les analyses nationales et de provenance, les limites, les insights et les indicateurs recommandés.

L'application officielle est **[dashboard/app.py](dashboard/app.py)**. Le dashboard finalisé comprend :

- **Tendances** : filtres Destinations / Indicateur / Période dans la sidebar ; sous-onglets Évolution, Variation annuelle, Ratio recettes / arrivées et Comparaison.
- **Provenance** : filtres propres à chaque destination, couverture, groupes comparables et cas particuliers.
- **Carte** : niveaux nationaux sur une même année, 2019 par défaut, absences explicites.

Les vues proposent des exports CSV. Le projet est en phase de clôture/transmission ; la validation d'une installation neuve et la consolidation des archives restent distinctes de la finalisation analytique.

## Organisation du dépôt

| Emplacement | Rôle |
|---|---|
| `data/final/` | Dataset maître `dataset_maitre_trends_tourisme_afrique.csv` et version XLSX |
| `data/raw/`, `data/processed/` | Emplacements prévus ; sources historiques et intermédiaires absents du dépôt actuel |
| `notebooks/` | EDA finalisée |
| `dashboard/app.py` | Application Streamlit officielle |
| `src/` | Chargement, indicateurs et corrections de métadonnées |
| `reports/exports/metadata_corrections_log.csv` | Journal des corrections réalisées |
| `reports/figures/` | Emplacement de figures ; aucun export de figure livré actuellement |
| `docs/` | Documentation projet, méthodologie, sources, dictionnaire et guide de reprise |

## Documentation

Commencer par le [guide de reprise](docs/handover_guide.md). La [documentation projet](docs/project_documentation.md) décrit les livrables ; le [dictionnaire](docs/data_dictionary.md) décrit le schéma du maître.

## Limites principales

Les séries nationales s'arrêtent au plus tard en 2020 : **aucune analyse fiable de reprise nationale post-Covid** n'est possible. Les recettes sont nominales ; le ratio agrégé n'est pas une dépense individuelle. Les provenances ont des périmètres hétérogènes et partiels ; missing ≠ 0.

L'exploitation du maître, l'EDA et le dashboard sont reproductibles depuis les fichiers finaux. La reconstruction intégrale depuis les publications originales est **NON AUTONOME** avec le seul dépôt actuel. Voir la [méthodologie](docs/methodology.md) et le [registre des sources](docs/data_sources.md).

## Installation

Environnement de référence relevé : Python 3.13.7 sous Windows. Depuis la racine du dépôt :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip check
```

Sous Linux/macOS, activer l'environnement avec `source .venv/bin/activate` (utiliser `python3` pour le créer si nécessaire).

Lancement officiel du dashboard :

```shell
python -m streamlit run dashboard/app.py
```

Pour le notebook :

```shell
python -m notebook notebooks/01_analyse_exploratoire.ipynb
```

Sélectionner le noyau Python de cet environnement. Les versions des dépendances directes sont fixées à celles de l'environnement fonctionnel ; les dépendances transitives restent résolues par pip. Ce fichier n'est donc pas un verrouillage intégral de l'environnement. L'installation dans un environnement neuf reste à valider séparément.
