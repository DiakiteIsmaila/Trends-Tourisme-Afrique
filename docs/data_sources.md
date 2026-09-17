# Registre des sources de données — Projet Trends
## Tourisme international dans les principales destinations africaines

**Projet :** Trends — Gaea21  
**Document :** Registre de traçabilité des sources  
**Dernière mise à jour :** 15 septembre 2026\
**Statut :** Document vivant — les URL et dates d'accès non vérifiées restent explicitement signalées.

---

## 1. Objectif du registre

Ce document recense les sources utilisées pour construire le dataset maître du projet Trends consacré au tourisme international dans sept destinations africaines.

Il doit permettre à une nouvelle personne de répondre à cinq questions :

1. D'où vient chaque donnée ?
2. Quel organisme l'a produite ?
3. Quelle période et quelle unité sont couvertes ?
4. Quel fichier de travail a été construit à partir de cette source ?
5. Quelles limites doivent être respectées avant toute comparaison ?

La chaîne de traçabilité retenue est :

**source originale -> document/dataset collecté -> extraction -> harmonisation -> dataset maître -> analyse/dashboard**

> Règle : aucune URL, date d'accès ou référence documentaire précise ne doit être inventée. Lorsqu'une information n'a pas encore été retrouvée dans les archives du projet, elle est marquée `À VÉRIFIER`.

---

Les références institutionnelles ci-dessous sont consolidées à partir des références vérifiées fournies pour cette mise à jour et des métadonnées locales. Elles ne prouvent ni la date historique de collecte ni le rattachement de chaque valeur à une publication. Les archives historiques mentionnées ne sont pas actuellement présentes dans `data/raw/` ou `data/processed/`.

## 2. Synthèse des sources

| ID | Dimension | Destination | Organisme / source | Période utilisée | Unité / type | Niveau de couverture |
|---|---|---|---|---|---|---|
| SRC-ARVL | Arrivées | 7 destinations | Banque mondiale — World Development Indicators | série harmonisée du projet | personnes | série internationale harmonisée |
| SRC-RCPT | Recettes | 7 destinations | Banque mondiale — World Development Indicators | série harmonisée du projet | USD courants | série internationale harmonisée |
| SRC-MAR | Provenance | Maroc | MTAESS — portail officiel data.gov.ma | 2012–2020 | personnes | données par marché d'origine |
| SRC-TUN | Provenance | Tunisie | Office National du Tourisme Tunisien (ONTT) | 2017–2023 | personnes | arrivées aux frontières par nationalité |
| SRC-KEN | Provenance | Kenya | Tourism Research Institute (TRI) — rapports 2022, 2023 et 2024 identifiés | 2022–2024 | personnes | Top 30 marchés |
| SRC-TZA | Provenance | Tanzanie | NBS — International Visitors' Exit Survey Reports | 2022–2024 | parts | Top 15 marchés |
| SRC-MUS | Provenance | Maurice | Statistics Mauritius — International Travel and Tourism | 2022–2024 | personnes | panel de 7 marchés |
| SRC-ZAF | Provenance | Afrique du Sud | Stats SA — collections P0351 et P0350 ; tables du panel à consolider | 2022–2024 | personnes | panel de 18 marchés |
| SRC-EGY | Provenance | Égypte | CAPMAS identifié dans les archives documentaires ; rattachement exact aux valeurs à vérifier | 2010–2019 + agrégats 2019 | personnes / parts | couverture partielle |

---

## 3. Arrivées touristiques internationales

### SRC-ARVL — Banque mondiale

**Dimension :** Arrivées touristiques internationales  
**Destinations :** Afrique du Sud, Égypte, Kenya, Maroc, Maurice, Tanzanie, Tunisie  
**Organisme :** Banque mondiale  
**Base :** World Development Indicators (WDI)  
**Indicateur :** `ST.INT.ARVL`  
**Libellé :** International tourism, number of arrivals  
**Unité :** personnes / nombre d'arrivées  
**Fichier source de travail :** `WB_WDI_ST_INT_ARVL_WIDEF.csv`  
**Fichier harmonisé :** `audit_harmonisation_arrivees_7_pays_trends.xlsx`  
**Destination finale :** couche `arrivals` du dataset maître.

**Page officielle vérifiée :** https://data.worldbank.org/indicator/ST.INT.ARVL\
**Source statistique sous-jacente indiquée :** Yearbook of Tourism Statistics, Compendium of Tourism Statistics and data files, UN Tourism.

### Traitement appliqué

- sélection des sept destinations ;
- passage au format analytique harmonisé ;
- normalisation des noms de destinations ;
- conversion de l'année ;
- conservation des valeurs manquantes ;
- conservation de la source et de l'unité dans le schéma final.

### Limites

Une valeur absente dans la série WDI n'est jamais transformée en zéro.

**URL historique de téléchargement, méthode et date d'extraction :** `À VÉRIFIER` ; une page officielle actuelle ne prouve pas les conditions de collecte historiques.

---

## 4. Recettes du tourisme international

### SRC-RCPT — Banque mondiale

**Dimension :** Recettes touristiques internationales  
**Destinations :** Afrique du Sud, Égypte, Kenya, Maroc, Maurice, Tanzanie, Tunisie  
**Organisme :** Banque mondiale  
**Base :** World Development Indicators (WDI)  
**Indicateur :** `ST.INT.RCPT.CD`  
**Libellé :** International tourism, receipts (current US$)  
**Unité :** dollars US courants  
**Fichier source de travail :** `WB_WDI_ST_INT_RCPT_CD_WIDEF.csv`  
**Fichier harmonisé :** `audit_harmonisation_recettes_7_pays_trends.xlsx`  
**Destination finale :** couche `receipts` du dataset maître.

**Page officielle vérifiée :** https://data.worldbank.org/indicator/ST.INT.RCPT.CD

### Traitement appliqué

- sélection des sept destinations ;
- harmonisation du format ;
- contrôle du type numérique ;
- conservation des années sans observation comme valeurs manquantes ;
- conservation de l'unité.

### Limites

Les recettes sont exprimées en USD courants, sans correction de l'inflation. Une comparaison temporelle de niveau ne constitue donc pas automatiquement une mesure en prix constants.

**URL historique de téléchargement, méthode et date d'extraction :** `À VÉRIFIER` ; une page officielle actuelle ne prouve pas les conditions de collecte historiques.

---

# 5. Provenance des touristes

## 5.1 Maroc — SRC-MAR

**Dimension :** Provenance  
**Destination :** Maroc  
**Période intégrée :** 2012–2020  
**Unité :** personnes  
**Granularité :** pays / marché d'origine  
**Niveau de comparabilité :** GREEN  
**Fichier standardisé :** `maroc_provenance_touristique_2012_2020_open_data.xlsx`

### Source

Les données ont été collectées depuis une source open data marocaine utilisée pendant la phase de collecte.

**Producteur vérifié :** MTAESS — Ministère du Tourisme, de l’Artisanat et de l’Économie Sociale et Solidaire.\
**Titre exact vérifié :** Evolution par nationalité des arrivées des touristes aux postes frontières 2012-2020.\
**Page officielle vérifiée :** https://data.gov.ma/data/fr/dataset/evolution-par-nationalite-des-arrivees-des-touristes-aux-postes-frontieres-2012-2020\
**Date d'accès :** `À VÉRIFIER.`

### Couverture

La série retenue contient des volumes d'arrivées par marché d'origine pour la période 2012–2020.

### Précaution

Le portail décrit l'évolution par nationalité des arrivées aux postes frontières pour 2012–2020. L'identification de cette page ne prouve pas l'URL utilisée historiquement ni la date d'accès : `À VÉRIFIER`. Les agrégats Maghreb/Scandinavie et les MRE restent distincts des marchés pays.

---

## 5.2 Tunisie — SRC-TUN

**Dimension :** Provenance  
**Destination :** Tunisie  
**Organisme :** Office National du Tourisme Tunisien (ONTT)  
**Documents :** publications annuelles *Le Tourisme Tunisien en Chiffres* / extraits correspondants  
**Période intégrée :** 2017–2023  
**Unité :** personnes  
**Granularité :** nationalité / marché d'origine  
**Niveau de comparabilité :** GREEN  
**Fichier standardisé :** `tunisie_provenance_touristique_2017_2023_ONTT.xlsx`

### Données utilisées

Les publications ONTT contiennent notamment les tableaux d'**arrivées aux frontières des non-résidents par nationalité**.

Les noms d'éditions/extraits documentés historiquement sont conservés ci-dessous ; ces fichiers ne sont pas présents dans les dossiers sources du dépôt audité :
- `tourisme en chiffres 2017.pdf`
- `Tourisme en chiffres 2018.pdf`
- `extrait tourisme en chiffres 2019 vf.pdf`
- `Extrait tourisme en chiffres 2020.pdf`
- `extrait ontt-2021.pdf`
- `EXTRAIT 2022.pdf`
- `EXTRAIT 2023.pdf`

### Couverture

Les données permettent de travailler avec des marchés d'origine détaillés et des agrégats présents dans les publications.

### Précautions

- distinguer les nationalités individuelles des agrégats (`TOTAL EUROPEENS`, `TOTAL MAGHREBINS`, etc.) ;
- ne pas compter simultanément un agrégat et ses composantes dans un total analytique ;
- distinguer touristes étrangers et Tunisiens résidant à l'étranger lorsque nécessaire ;
- conserver les 60 valeurs manquantes en 2017–2018 (`missing_unverified`) : leur cause est `À VÉRIFIER`, missing ≠ 0 ;
- traiter « Scandinaves » comme agrégat régional, non comme pays ; sa composition exacte reste `À VÉRIFIER`.

**URL(s) exacte(s) des éditions utilisées :** `À VÉRIFIER avant ajout.`  
**Date(s) d'accès :** `À VÉRIFIER.`

---

## 5.3 Kenya — SRC-KEN

**Dimension :** Provenance  
**Destination :** Kenya  
**Organisme identifié dans le travail de collecte :** Tourism Research Institute (TRI)  
**Période intégrée :** 2022–2024  
**Unité :** personnes  
**Granularité :** pays / marché d'origine  
**Couverture :** Top 30  
**Niveau de comparabilité :** ORANGE  
**Fichier standardisé :** `kenya_provenance_touristique_2022_2024_TRI.xlsx`

### Précaution

Le jeu intégré correspond à un **Top 30**. Il ne doit donc pas être interprété comme une liste exhaustive de tous les marchés émetteurs du Kenya.

**Rapports officiels identifiés :**
- Annual Tourism Sector Performance Report 2022 : https://tri.go.ke/wp-content/uploads/2023/12/TOURISM-SECTOR-PERFORMANCE-REPORT_2022.pdf ; tableau « Performance by Source Markets - Top 30 Source Countries 2022 ».
- Tourism Sector Performance Report 2023 : URL exacte `À VÉRIFIER`.
- Annual Tourism Sector Performance Report 2024 : https://tri.go.ke/wp-content/uploads/2025/02/TRI-Tourism-Sector-Performance-Report-2024.pdf ; Directorate of Immigration Services indiquée comme source du tableau correspondant.

« United Nations Organization » est une catégorie institutionnelle, pas un pays. Sa définition exacte reste `À VÉRIFIER`. L'identification des rapports ne constitue pas une validation valeur par valeur du panel harmonisé.\
**Date d'accès :** `À VÉRIFIER.`

---

## 5.4 Tanzanie — SRC-TZA

**Dimension :** Provenance  
**Destination :** Tanzanie  
**Organisme identifié :** National Bureau of Statistics (NBS), Tanzanie  
**Période intégrée :** 2022–2024  
**Unité :** parts (`share`)  
**Granularité :** pays / marché d'origine  
**Couverture :** Top 15  
**Niveau de comparabilité :** RED  
**Fichier standardisé :** `tanzania_tourism_provenance_2022_2024_NBS.xlsx`

### Particularité méthodologique

Les données retenues pour cette dimension correspondent à des **parts** et non à des volumes exacts comparables aux séries `persons` des autres destinations.

### Précautions

- ne jamais présenter les parts comme des nombres d'arrivées ;
- ne pas comparer directement leur valeur avec les volumes des autres pays ;
- conserver l'unité `share` ;
- signaler la couverture partielle Top 15 ;
- aucune reconstruction en nombre d'arrivées et aucune renormalisation à 100 %.

**Collection officielle identifiée :** International Visitors' Exit Survey Reports.\
**Éditions, tables et URL exactes rattachées aux valeurs 2022–2024 :** `À VÉRIFIER`.\
**URL exacte :** `À VÉRIFIER.`  
**Date d'accès :** `À VÉRIFIER.`

---

## 5.5 Maurice — SRC-MUS

**Dimension :** Provenance  
**Destination :** Maurice  
**Organisme identifié :** Statistics Mauritius  
**Période intégrée :** 2022–2024  
**Unité :** personnes  
**Granularité :** pays / marché d'origine  
**Couverture :** panel de 7 marchés retenus  
**Niveau de comparabilité :** ORANGE  
**Fichier standardisé :** `maurice_provenance_touristique_2022_2024_statistics_mauritius.xlsx`

### Précaution

Le panel intégré ne représente pas nécessairement l'ensemble des marchés d'origine. Les analyses doivent être présentées comme une analyse du périmètre disponible et non comme un classement exhaustif.

**Collection identifiée :** International Travel and Tourism ; ventilation par Country of Residence. Réunion / Reunion Island reste un marché distinct de France, conformément à la source et au dataset harmonisé.\
**Éditions et tables exactes rattachées au panel :** `À VÉRIFIER`.\
**URL exacte :** `À VÉRIFIER.`  
**Date d'accès :** `À VÉRIFIER.`

---

## 5.6 Afrique du Sud — SRC-ZAF

**Dimension :** Provenance  
**Destination :** Afrique du Sud  
**Organisme identifié :** Statistics South Africa (Stats SA)  
**Période intégrée :** 2022–2024  
**Unité :** personnes  
**Granularité :** pays / marché d'origine  
**Couverture :** panel de 18 marchés  
**Niveau de comparabilité :** ORANGE  
**Fichier standardisé :** `afrique_du_sud_provenance_touristique_2022_2024_stats_sa.xlsx`

### Précaution

Le jeu intégré est un panel et non une couverture exhaustive de tous les marchés émetteurs. Les classements doivent rester limités au panel réellement présent.

**Collections officielles identifiées :** P0351 — Tourism and Migration ; P0350 — International Tourism pour les publications correspondantes plus récentes. Ventilation notamment par région et country of residence.\
**Rattachement du panel annuel de 18 marchés aux tables/publications exactes :** `À VÉRIFIER`. L'institution et les collections sont identifiées, pas chaque correspondance annuelle.\
**URL exacte :** `À VÉRIFIER.`  
**Date d'accès :** `À VÉRIFIER.`

---

## 5.7 Égypte — SRC-EGY

**Dimension :** Provenance  
**Destination :** Égypte  
**Organisme vérifié dans les archives :** Central Agency for Public Mobilization and Statistics (CAPMAS)  
**Fichier standardisé :** `egypte_provenance_touristique_donnees_verifiees.xlsx`  
**Niveau de comparabilité :** RED

### Données pays intégrées

Un seul marché pays a été conservé comme série vérifiée dans le dataset harmonisé :

**États-Unis — 2010–2019 — unité : personnes**

Cette série ne doit pas être interprétée comme un classement des principaux marchés émetteurs de l'Égypte.

### Données régionales intégrées

Des répartitions régionales pour 2019 sont également présentes dans le dataset sous forme de parts.

Deux indicateurs sont distingués :
- part des touristes (`regional_tourist_share`) ;
- part des nuitées (`regional_tourist_nights_share`).

Ces deux indicateurs ne doivent pas être mélangés.

### Sources archivées

CAPMAS est identifié dans l'historique des archives documentaires du projet. Ces archives ne sont pas présentes dans les dossiers sources du dépôt audité ; cette identification institutionnelle ne démontre pas le rattachement de chaque valeur à une publication CAPMAS précise.

Les dix observations États-Unis 2010–2019 conservent `source_name = "User-provided source file"`. Les parts régionales portent une attribution CAPMAS dans le maître, mais leur référence exacte reste à vérifier. Aucune attribution du dataset n'est modifiée par cette consolidation documentaire.

### Précautions

- ne pas comparer directement la série États-Unis avec les agrégats régionaux ;
- ne pas interpréter les États-Unis comme « premier marché » ;
- ne pas mélanger part des touristes et part des nuitées ;
- ne pas présenter la couverture comme exhaustive.

**Référence exacte ayant servi à chaque valeur 2010–2019 :** `À VÉRIFIER / consolider à partir des archives de collecte.`  
**Référence exacte des parts régionales 2019 :** `À VÉRIFIER.`  
**URL institutionnelle identifiée dans les documents CAPMAS :** `www.capmas.gov.eg`  
**URL précise des publications :** `À VÉRIFIER avant ajout.`

---

# 6. Fichiers issus de la collecte

Les noms historiques des sections 6.1 et 6.2 sont documentés dans le registre, mais les fichiers correspondants ne sont actuellement présents ni dans `data/raw/` ni dans `data/processed/`. Les fichiers maîtres de la section 6.3 sont présents dans `data/final/`.

**REPRODUCTIBLE depuis le dataset maître :** exploitation du dataset final, corrections de métadonnées applicables au maître, EDA, indicateurs et dashboard.

**NON AUTONOME avec le seul dépôt actuel :** reconstruction intégrale du maître depuis toutes les publications originales. Il s'agit d'une limite de traçabilité/reconstruction, pas d'une invalidation du dataset final.

## 6.1 Fichiers sources / intermédiaires principaux

```text
WB_WDI_ST_INT_ARVL_WIDEF.csv
WB_WDI_ST_INT_RCPT_CD_WIDEF.csv

maroc_provenance_touristique_2012_2020_open_data.xlsx
tunisie_provenance_touristique_2017_2023_ONTT.xlsx
kenya_provenance_touristique_2022_2024_TRI.xlsx
tanzania_tourism_provenance_2022_2024_NBS.xlsx
maurice_provenance_touristique_2022_2024_statistics_mauritius.xlsx
afrique_du_sud_provenance_touristique_2022_2024_stats_sa.xlsx
egypte_provenance_touristique_donnees_verifiees.xlsx
```

## 6.2 Fichiers d'audit et d'harmonisation

```text
audit_comparabilite_7_pays_trends.xlsx
audit_harmonisation_arrivees_7_pays_trends.xlsx
audit_harmonisation_recettes_7_pays_trends.xlsx
harmonisation_provenance_7_pays_trends.xlsx
```

## 6.3 Dataset maître

```text
dataset_maitre_trends_tourisme_afrique.csv
dataset_maitre_trends_tourisme_afrique.xlsx
```

---

# 7. Règles de traçabilité

Toute nouvelle source ajoutée au projet doit renseigner au minimum :

- organisme producteur ;
- titre exact du dataset, tableau ou rapport ;
- URL exacte ;
- date d'accès ou d'extraction ;
- destination concernée ;
- indicateur ;
- définition ;
- période ;
- unité ;
- granularité ;
- couverture ;
- fichier brut conservé ;
- fichier harmonisé produit ;
- transformations effectuées ;
- limites connues.

Lorsqu'une information n'est pas connue, utiliser `À VÉRIFIER` plutôt que de la déduire ou de l'inventer.

---

# 8. Points restant à consolider

Les institutions, collections et pages indiquées comme vérifiées ci-dessus ne restent pas des tâches ouvertes. Restent :

- **Banque mondiale :** URL/méthode historique et dates d'extraction des deux séries — `À VÉRIFIER`.
- **Maroc :** date d'accès et URL effectivement utilisée historiquement — `À VÉRIFIER` ; producteur, titre et page officielle consolidés.
- **Tunisie :** URL des éditions et dates d'accès, cause des 60 absences, composition de Scandinaves — `À VÉRIFIER`.
- **Kenya :** URL 2023, dates d'accès, correspondance précise des valeurs harmonisées avec les tables et définition de la catégorie ONU — `À VÉRIFIER`.
- **Tanzanie :** éditions/tables/URL exactes et dates d'accès — `À VÉRIFIER` ; collection Exit Survey et nature Top 15 en parts consolidées.
- **Maurice :** tables annuelles exactes, URL et dates d'accès — `À VÉRIFIER` ; collection et ventilation par résidence identifiées.
- **Afrique du Sud :** rattachement précis du panel annuel de 18 marchés aux publications/tables, URL et dates d'accès — `À VÉRIFIER`.
- **Égypte :** référence exacte de la série USA 2010–2019 et des parts régionales 2019, correspondances valeur → publication et dates historiques — `À VÉRIFIER`. Ne pas présumer que toutes les valeurs proviennent d'une publication CAPMAS déterminée.
- **Archives :** localisation et récupération des fichiers sources/intermédiaires historiques — `À VÉRIFIER` ; documenter ensuite la chaîne de reconstruction.

---

# 9. Historique du registre

| Date | Modification |
|---|---|
| 2026-09-15 | Consolidation des références institutionnelles fournies ; réserves historiques, granularités et disponibilité des archives explicitées, sans modification des données |
| 2026-09-08 | Création du registre central des sources |
| 2026-09-08 | Identification des sources principales arrivées / recettes |
| 2026-09-08 | Documentation des sept périmètres de provenance |
| 2026-09-08 | Ajout explicite des références restant à vérifier |

---

## Règle de maintenance

`data_sources.md` doit être mis à jour dès qu'une source est ajoutée, remplacée, corrigée ou qu'une référence originale est retrouvée.

Ce registre complète :
- `project_documentation.md` pour l'historique global ;
- `methodology.md` pour les règles méthodologiques ;
- `data_dictionary.md` pour le schéma du dataset ;
- `handover_guide.md` pour la reprise opérationnelle du projet.
