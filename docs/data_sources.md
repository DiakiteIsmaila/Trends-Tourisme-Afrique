# Registre des sources de données — Projet Trends
## Tourisme international dans les principales destinations africaines

**Projet :** Trends — Gaea21  
**Document :** Registre de traçabilité des sources  
**Dernière mise à jour :** 8 septembre 2026  
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

## 2. Synthèse des sources

| ID | Dimension | Destination | Organisme / source | Période utilisée | Unité / type | Niveau de couverture |
|---|---|---|---|---|---|---|
| SRC-ARVL | Arrivées | 7 destinations | Banque mondiale — World Development Indicators | série harmonisée du projet | personnes | série internationale harmonisée |
| SRC-RCPT | Recettes | 7 destinations | Banque mondiale — World Development Indicators | série harmonisée du projet | USD courants | série internationale harmonisée |
| SRC-MAR | Provenance | Maroc | Source open data marocaine — référence exacte à confirmer dans l'archive de collecte | 2012–2020 | personnes | données par marché d'origine |
| SRC-TUN | Provenance | Tunisie | Office National du Tourisme Tunisien (ONTT) | 2017–2023 | personnes | arrivées aux frontières par nationalité |
| SRC-KEN | Provenance | Kenya | Tourism Research Institute (TRI) — référence documentaire exacte à confirmer | 2022–2024 | personnes | Top 30 marchés |
| SRC-TZA | Provenance | Tanzanie | National Bureau of Statistics (NBS) — référence documentaire exacte à confirmer | 2022–2024 | parts | Top 15 marchés |
| SRC-MUS | Provenance | Maurice | Statistics Mauritius — référence documentaire exacte à confirmer | 2022–2024 | personnes | panel de 7 marchés |
| SRC-ZAF | Provenance | Afrique du Sud | Statistics South Africa (Stats SA) — référence documentaire exacte à confirmer | 2022–2024 | personnes | panel de 18 marchés |
| SRC-EGY | Provenance | Égypte | CAPMAS / publications statistiques égyptiennes utilisées lors de la collecte | 2010–2019 + agrégats 2019 | personnes / parts | couverture partielle |

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

### Traitement appliqué

- sélection des sept destinations ;
- passage au format analytique harmonisé ;
- normalisation des noms de destinations ;
- conversion de l'année ;
- conservation des valeurs manquantes ;
- conservation de la source et de l'unité dans le schéma final.

### Limites

Une valeur absente dans la série WDI n'est jamais transformée en zéro.

**URL exacte utilisée lors du téléchargement :** `À VÉRIFIER dans l'archive de collecte avant ajout au registre.`

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

### Traitement appliqué

- sélection des sept destinations ;
- harmonisation du format ;
- contrôle du type numérique ;
- conservation des années sans observation comme valeurs manquantes ;
- conservation de l'unité.

### Limites

Les recettes sont exprimées en dollars courants. Une comparaison temporelle de niveau ne constitue donc pas automatiquement une mesure en prix constants.

**URL exacte utilisée lors du téléchargement :** `À VÉRIFIER dans l'archive de collecte avant ajout au registre.`

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

**Organisme exact :** `À VÉRIFIER dans le fichier/source original.`  
**Nom exact du jeu de données :** `À VÉRIFIER.`  
**URL exacte :** `À VÉRIFIER.`  
**Date d'accès :** `À VÉRIFIER.`

### Couverture

La série retenue contient des volumes d'arrivées par marché d'origine pour la période 2012–2020.

### Précaution

La source doit être ré-identifiée précisément avant toute publication externe du registre. Le fichier standardisé ne suffit pas, à lui seul, à prouver l'URL originale.

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

Les archives du projet comprennent plusieurs éditions/extraits annuels, notamment :
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
- distinguer touristes étrangers et Tunisiens résidant à l'étranger lorsque nécessaire.

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

**Titre exact du rapport :** `À VÉRIFIER dans l'archive de collecte.`  
**URL exacte :** `À VÉRIFIER.`  
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
- signaler la couverture Top 15.

**Titre exact de la publication :** `À VÉRIFIER.`  
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

**Publication/table exacte :** `À VÉRIFIER dans l'archive de collecte.`  
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

**Titre exact de la publication/table :** `À VÉRIFIER dans l'archive de collecte.`  
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

Les archives du projet contiennent plusieurs publications CAPMAS sur les statistiques touristiques. Elles confirment l'utilisation de catégories régionales et la publication de statistiques d'arrivées et de nuitées.

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

**À FAIRE — Source Maroc**
- retrouver l'organisme exact ;
- retrouver le nom exact du jeu open data ;
- retrouver l'URL et la date d'accès.

**À FAIRE — Kenya**
- retrouver le titre exact du ou des rapports TRI ;
- enregistrer l'URL officielle et la date d'accès.

**À FAIRE — Tanzanie**
- retrouver le titre exact de la publication NBS ;
- enregistrer l'URL et la date d'accès.

**À FAIRE — Maurice**
- retrouver la table/publication exacte de Statistics Mauritius ;
- enregistrer l'URL et la date d'accès.

**À FAIRE — Afrique du Sud**
- retrouver le rapport/table Stats SA exact ;
- enregistrer l'URL et la date d'accès.

**À FAIRE — Égypte**
- relier chaque groupe de données du fichier standardisé au document CAPMAS exact ;
- identifier précisément la source des parts régionales 2019.

**À FAIRE — Banque mondiale**
- conserver l'URL exacte ou la méthode d'extraction utilisée pour les deux fichiers WDI ;
- renseigner la date d'extraction si elle peut être retrouvée.

---

# 9. Historique du registre

| Date | Modification |
|---|---|
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
