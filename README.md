# 📊 End-to-End Data Pipeline : Analyse Boursière 


Ce dépôt contient le code source et la documentation d'un pipeline de données complet (Proof of Concept) permettant l'extraction, le stockage, l'orchestration et la visualisation de données boursières de plusieurs grandes entreprises françaises (TotalEnergies, Orange, AXA, BNP Paribas, Crédit Agricole) comparées à l'indice de référence CAC 40.

🛠️ Stack Technique
* Extraction : Python (pandas, yfinance, SQLAlchemy)

* Orchestration : Apache Airflow

* Base de données : PostgreSQL (conteneurisé via Docker)

Data Visualization : Power BI (DAX)

📂 Structure du Projet
L'arborescence du dépôt est organisée pour faciliter le déploiement de l'environnement Airflow et la lecture du code :

Plaintext
├── dags/
│   ├── scripts/
│   │   ├── extract_nett.py           # Extraction (API Yahoo Finance) et nettoyage (Pandas)
│   │   └── chargement.py             # Connexion et insertion dans PostgreSQL (SQLAlchemy)
│   └── bourse_pipeline_dag.py        # DAG Airflow (orchestration et dépendances des tâches)
├── images/                           # Captures d'écran pour la documentation
├── Data Dictionary.md                # Dictionnaire détaillant les champs de la base de données
├── ReportingING-Finance.pbix         # Tableau de bord Power BI (Data Viz & DAX)
├── docker-compose.yml                # Déploiement des conteneurs Postgres et Airflow
├── requirements.txt                  # Dépendances Python (yfinance, pandas, sqlalchemy...)
└── README.md

⚙️ Choix d'Architecture et Logique Métier

* Infrastructure (Docker + PostgreSQL) : Déploiement reproductible. PostgreSQL est très bien adapté au stockage de séries temporelles financières (Date, Ouverture, Clôture, Volumes) et s'intègre nativement avec Power BI.

* Orchestration (Airflow) : Choisi pour la fiabilité des exécutions quotidiennes (post-clôture) et la gestion des échecs d'appels API (stratégie de retries) via le script extract_nett.py.

* Modélisation BI (Power BI & DAX) :

Performance Base 0 : Création d'une mesure DAX pour normaliser les prix. Cela permet d'afficher des variations en pourcentage (%) sur une échelle commune, rendant la comparaison entre une action à 15€ et un indice à 8000 points pertinente.

Exclusion des biais : Le CAC 40 est un indicateur, pas une entreprise. Il est exclu des calculs d'agrégation (volumes globaux, moyennes de prix) par filtrage DAX pour conserver la justesse métier.

Table de dates dynamique : Calendrier généré en DAX se basant sur le MIN et MAX de la table des faits pour garantir des axes temporels stricts.

🚀 Lancement Rapide
Cloner le dépôt et lancer l'infrastructure :

Bash
docker-compose up -d
Accéder à l'interface Airflow (http://localhost:8080) pour activer le DAG.

Ouvrir ReportingING-Finance.pbix et actualiser les sources de données PostgreSQL locales.

NB : Vous devez avoir installé Docker desktop, PostgreSQL, Airflow via le fichier docker-compose.yml et Power BI Desktop pour pouvoir exécuter ce projet sans oublier l'installation des requirements.