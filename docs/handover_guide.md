# Guide de reprise — Projet Trends

**État au 15 septembre 2026 :** EDA et dashboard finalisés ; phase de clôture/transmission.

## 1. Point d'entrée

L'application officielle est **`dashboard/app.py`**. L'EDA finalisée est `notebooks/01_analyse_exploratoire.ipynb` (sections 01–12). Les KPI sont déjà sélectionnés et implémentés : il n'est pas nécessaire de reconstruire le dashboard ou d'approfondir l'EDA initiale pour reprendre le projet.

## 2. Prérequis et installation

Environnement de référence : Python 3.13.7 sous Windows. Les versions directes sont fixées dans `requirements.txt`, sans verrouillage complet des dépendances transitives. L'installation neuve reste à valider séparément.

Depuis la racine du dépôt :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip check
```

Sous Linux/macOS : `source .venv/bin/activate` ; utiliser `python3` pour créer l'environnement si nécessaire. Voir aussi [README](../README.md#installation).

## 3. Données et documents

| Élément | Emplacement |
|---|---|
| Maître utilisé par le code | `data/final/dataset_maitre_trends_tourisme_afrique.csv` |
| Version Excel | `data/final/dataset_maitre_trends_tourisme_afrique.xlsx` |
| EDA | `notebooks/01_analyse_exploratoire.ipynb` |
| Chargement et indicateurs | `src/data_processing.py`, `src/indicators.py` |
| Corrections au maître existant | `src/metadata_corrections.py` |
| Journal des corrections réalisées | `reports/exports/metadata_corrections_log.csv` |
| Schéma et catégories | [data_dictionary.md](data_dictionary.md) |
| Sources et réserves historiques | [data_sources.md](data_sources.md) |
| Règles analytiques | [methodology.md](methodology.md) |
| État et livrables | [project_documentation.md](project_documentation.md) |

Le maître contient 1 080 lignes et 17 colonnes. Les visualisations actuelles sont définies dans l'application et le notebook.

## 4. Lancer l'EDA et le dashboard

Environnement activé, depuis la racine :

```shell
python -m notebook notebooks/01_analyse_exploratoire.ipynb
```

Choisir le noyau Python de l'environnement, puis redémarrer le noyau et exécuter toutes les cellules pour une validation complète. Le notebook recherche le maître depuis la racine ou le dossier `notebooks/`.

Commande officielle :

```shell
python -m streamlit run dashboard/app.py
```

L'application charge le CSV à partir de son emplacement dans le dépôt. Aucune génération préalable de données ni réapplication des corrections n'est nécessaire pour consulter les livrables.

## 5. Utiliser le dashboard

- **Tendances :** Destinations / Indicateur / Période dans la sidebar. Évolution et Variation annuelle suivent ces filtres. Le Ratio combine arrivées et recettes : seul le choix des destinations et de la période s'applique. Comparaison utilise 2019 pour les niveaux et 1998–2019 pour la médiane/volatilité ; son choix de dimension est dans la sous-vue centrale.
- **Provenance :** destination, année et catégorie dans la sidebar ; couverture, qualité, absences et unités explicites. Le panneau régional égyptien est fixé à 2019 et distingué de l'année du marché pays.
- **Carte :** indicateur national et année dans la sidebar, 2019 par défaut ; mêmes année et unité pour toutes les destinations.
- **Exports :** CSV correspondant aux périmètres des vues ; parts conservées sous leur unité, absences laissées vides. L'Égypte dispose d'un export distinct pour les parts régionales 2019.

## 6. Règles à préserver

- Missing ≠ 0 : aucune interpolation, fabrication ou reconstruction.
- Variation annuelle uniquement entre deux années strictement consécutives pour la même destination et le même indicateur, base strictement positive.
- Recettes en USD courants, sans correction d'inflation.
- Ratio `receipts / arrivals` sur même destination et année, deux valeurs présentes, arrivées strictement positives. Ni dépense/revenu individuels, ni rentabilité, ni qualité touristique.
- Niveaux, médiane annuelle et volatilité distincts ; aucun score composite ni causalité déduite des corrélations.
- Les séries nationales s'arrêtent au plus tard en 2020 selon disponibilité : aucune conclusion fiable sur la reprise nationale post-Covid avec ce dataset.
- Provenance : pays, régions, diasporas, institutions, volumes et parts séparés ; Top-N/panels explicités.
- Tanzanie : parts uniquement, sans conversion en volumes ni renormalisation.
- Égypte : couverture insuffisante pour un classement complet ; références exactes USA et parts régionales encore à vérifier.
- Tunisie : 60 absences 2017–2018 restent `missing_unverified` ; Scandinaves reste un agrégat régional.
- ONU au Kenya : catégorie institutionnelle ; Réunion : marché distinct de France. Les réserves de source restent applicables.

## 7. Reproductibilité et archives

**REPRODUCTIBLE depuis le maître :** exploitation du CSV/XLSX, corrections documentées applicables au maître, EDA, indicateurs et dashboard.

**NON AUTONOME avec le dépôt actuel :** reconstruction intégrale du maître depuis toutes les publications originales. `data/raw/` et `data/processed/` ne contiennent pas les fichiers historiques listés dans le registre. Leur localisation reste à consolider. Cette limite de traçabilité n'empêche pas l'exploitation analytique du maître.

Une page institutionnelle identifiée ne prouve ni une date historique d'accès ni l'attribution valeur par valeur. Ne pas transformer les mentions « À VÉRIFIER » en certitudes sans preuve.

## 8. Ajouter ou corriger des données

1. Identifier la publication, l'organisme, la table, l'unité, les définitions et le périmètre. Conserver les pièces et dates réellement connues.
2. Documenter la source et les transformations dans le registre ; garder les références incertaines explicitement ouvertes.
3. Vérifier les clés logiques, doublons, absences, catégories et compatibilité des périodes avant intégration. Ne jamais additionner agrégats et composantes.
4. Modifier le schéma seulement avec mise à jour du dictionnaire ; conserver la traçabilité des corrections et la concordance CSV/XLSX.
5. Réexécuter l'EDA dans un noyau neuf ; contrôler les chiffres et textes réutilisés.
6. Tester filtres, trous temporels, ratios, catégories, absences, carte et exports du dashboard. Mettre à jour les documents affectés.
7. Réexaminer les années communes et les références fixes 2019 / 1998–2019 si la couverture change ; aucune nouvelle analyse de reprise sans données nationales appropriées.

La commande `python -B src/metadata_corrections.py` concerne seulement les corrections déjà approuvées au maître existant ; ne pas l'assimiler à une procédure générale de collecte ou d'intégration.

## 9. Contrôles et clôture

Déjà réalisés dans l'environnement installé : exécution complète EDA, tests applicatifs des vues/filtres et des sept destinations, contrôles des exports, unités, absences, ratios, syntaxe et concordance CSV/XLSX.

Avant transmission définitive :

- valider une installation neuve et consigner l'environnement ;
- localiser les archives et poursuivre les rattachements documentaires restant ouverts ;
- confirmer au destinataire ces limites et les points d'entrée officiels ;
- effectuer la revue Git selon le processus du projet.

Aucune quantification de reprise nationale post-Covid n'est exigée avec les données actuelles. Les futures évolutions analytiques sont séparées de cette clôture.

## Historique

- 8 septembre 2026 : guide initial.
- 15 septembre 2026 : guide réorienté vers la reprise des livrables finalisés ; étapes analytiques déjà terminées retirées des travaux à effectuer.
