# Documentation du projet Trends

**Projet :** Trends — Gaea21
**État au 15 septembre 2026 :** analyses et dashboard finalisés ; clôture/transmission.

## 1. Objectif et périmètre

Étudier les arrivées, recettes et provenances touristiques dans sept destinations : Afrique du Sud, Égypte, Kenya, Maroc, Maurice, Tanzanie et Tunisie. Le dataset harmonise la structure sans rendre toutes les observations interchangeables.

## 2. Livrables et statuts

| Livrable | Statut | Emplacement |
|---|---|---|
| Dataset maître CSV/XLSX | TERMINÉ, avec limites documentées | `data/final/dataset_maitre_trends_tourisme_afrique.csv` et `.xlsx` |
| EDA, sections 01–12 | TERMINÉ | `notebooks/01_analyse_exploratoire.ipynb` |
| Sélection des indicateurs | TERMINÉ | Section 12 de l'EDA |
| Dashboard et organisation Gaea21 | TERMINÉ | `dashboard/app.py` |
| Dictionnaire des données | PRÉSENT et synchronisé avec le schéma | `docs/data_dictionary.md` |
| Corrections de métadonnées | RÉALISÉES ET JOURNALISÉES | `reports/exports/metadata_corrections_log.csv` |
| Documentation de fonctionnement | SYNCHRONISÉE avec l'état actuel | README et documents de `docs/` |
| Installation en environnement neuf | À VALIDER SÉPARÉMENT | `requirements.txt`, procédure README |
| Reconstruction depuis les publications originales | NON AUTONOME avec le dépôt actuel | Archives historiques à localiser |

## 3. Données et traçabilité

Le maître contient 1 080 lignes et 17 colonnes, avec trois couches : `arrivals`, `receipts`, `provenance`. Les CSV et XLSX ont été contrôlés concordants. Les noms des fichiers historiques sont conservés dans le registre, mais les fichiers sources/intermédiaires ne sont pas présents dans `data/raw/` ou `data/processed/`.

L'exploitation du maître, les corrections applicables à ce maître, l'EDA, les indicateurs et le dashboard sont reproductibles depuis les fichiers finaux. La collecte/extraction/harmonisation complète depuis les publications ne peut pas être reproduite de façon autonome avec le seul dépôt. Cette réserve n'invalide pas le maître.

Les pages institutionnelles et collections identifiées, ainsi que les références historiques restant à vérifier, sont centralisées dans [data_sources.md](data_sources.md). Ne pas inventer de date d'accès ni de rattachement valeur–publication.

## 4. EDA finalisée

Les sections 01–12 couvrent : introduction ; chargement/validation ; structure/qualité ; arrivées ; recettes ; analyse croisée ; dynamiques/croissance ; provenance ; synthèse comparative ; limites ; insights ; indicateurs dashboard.

Les comparaisons de niveaux utilisent 2019, année commune. Les variations annuelles ne franchissent pas les trous temporels. La dynamique médiane et la volatilité pré-2020 restent distinctes. Les recettes sont en USD courants ; le ratio agrégé n'est ni dépense individuelle, ni rentabilité, ni qualité. Aucune reprise nationale post-Covid n'est calculée.

## 5. Dashboard finalisé

**Application officielle : `dashboard/app.py`.** Les anciennes versions ont été retirées du dépôt de travail ; leur historique reste accessible dans Git.

- Identité visuelle Gaea21, chargement mis en cache, filtres dans `st.sidebar`.
- **Tendances :** sidebar Destinations / Indicateur / Période ; sous-onglets Évolution, Variation annuelle, Ratio recettes / arrivées, Comparaison. Le choix de dimension analytique est dans Comparaison. Niveaux en 2019 ; statistiques sur 1998–2019, sans application trompeuse du filtre de période.
- **Provenance :** destination, année et catégorie ; couverture et absences visibles, groupes homogènes, panels partiels signalés. Parts tanzaniennes sans conversion ; marché pays égyptien distinct du panneau régional 2019 et des deux métriques de parts.
- **Carte :** arrivées ou recettes, année commune 2019 par défaut, unité et destinations absentes explicites.
- Tableaux et exports CSV conservent les unités, périodes et métadonnées adaptées à chaque vue. Aucun score composite.

## 6. Corrections et réserves conservées

Les corrections approuvées du 8 septembre 2026 sont journalisées :

- Tunisie / Scandinaves : sept lignes reclassées en agrégat régional ; composition exacte à vérifier.
- Kenya / United Nations Organization : catégorie institutionnelle, non pays ; rang et valeur conservés.
- Tunisie : 60 valeurs absentes en 2017–2018 qualifiées `missing_unverified` ; cause non vérifiée, jamais zéro.

Réunion / Reunion Island reste un marché distinct de France ; aucune nouvelle correction n'est induite par cette conservation. Pour les dix observations Égypte–États-Unis, `User-provided source file` reste inchangé : l'identification de CAPMAS dans l'historique documentaire ne démontre pas l'attribution de chaque valeur.

Le script `src/metadata_corrections.py` applique les corrections au maître existant, sans reconstruire les données originales. Il n'est pas une étape nécessaire pour simplement consulter les livrables déjà corrigés.

## 7. Installation, exécution et contrôles

Suivre l'[installation du README](../README.md#installation), avec l'environnement Python 3.13.7 de référence et les dépendances directes fixées dans `requirements.txt`.

Depuis la racine, environnement activé :

```shell
python -m pip install -r requirements.txt
python -m pip check
python -m notebook notebooks/01_analyse_exploratoire.ipynb
python -m streamlit run dashboard/app.py
```

Les contrôles réalisés comprennent : EDA complète en noyau neuf, tests applicatifs des vues et filtres, cas de provenance, exports, absences, ratios/jointures, syntaxe et `git diff --check`. Ils ne constituent pas une validation d'installation neuve ni une preuve d'attribution aux publications originales.

## 8. Transmission et évolutions

Les prochaines actions portent sur la validation en environnement neuf, la localisation des archives et les références encore ouvertes, puis la revue de transmission. L'approfondissement initial de l'EDA, la construction du dashboard et la sélection des KPI sont terminés.

Toute nouvelle donnée exige une vérification de source, unité, période, granularité et couverture ; mise à jour du registre et du dictionnaire si nécessaire ; contrôles de non-régression ; réexécution de l'EDA et vérification des exports. Voir [handover_guide.md](handover_guide.md).

## 9. Documents associés

- [Méthodologie](methodology.md)
- [Registre des sources](data_sources.md)
- [Dictionnaire](data_dictionary.md)
- [Guide de reprise](handover_guide.md)

## Historique

- 8 septembre 2026 : documentation initiale et corrections de métadonnées approuvées.
- 15 septembre 2026 : synchronisation avec l'EDA 01–12 et le dashboard finalisés, sans modification des données ni du code.
