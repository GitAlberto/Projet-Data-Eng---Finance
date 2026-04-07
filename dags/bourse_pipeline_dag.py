from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# On importe les fonctions du script !
from scripts.extract_nett import extract_financial_data, clean_data
from scripts.chargement import load_data

# 1. Les paramètres par défaut (en cas d'erreur, qui prévenir, etc.)
default_args = {
    'owner': 'data_engineer', # Qui est responsable de ce DAG (pour les notifications)
    'depends_on_past': False,  # Ce DAG peut-il s'exécuter si la précédente exécution a échoué ? Non, on veut que chaque jour soit indépendant
    'start_date': datetime(2026, 4, 1), # À partir de quand le robot commence à compter
    'retries': 1, # Si ça plante, il réessaie 1 fois
    'retry_delay': timedelta(minutes=5), # Il attend 5 minutes avant de réessayer
}

# 2. La fonction "Wrapper" (qui emballe ton code pour Airflow)
def executer_pipeline_complet():
    entreprises_cibles = ['CA.PA', 'CS.PA', 'ORA.PA'] # Mes entreprises cibles (Carrefour, AXA, Orange sur Euronext Paris)
    
    print(" !! Démarrage de l'extraction...")
    raw_data = extract_financial_data(entreprises_cibles)
    
    print(" Démarrage du nettoyage...")
    clean_df = clean_data(raw_data, entreprises_cibles)
    
    print(" ==  Chargement dans PostgreSQL... ==")
    load_data(clean_df)
    
    print(" == Pipeline terminé avec succès ! ==")

# 3. La définition du DAG
with DAG(
    dag_id='pipeline_bourse_journalier', # Nom unique du DAG
    default_args=default_args, # Paramètres par défaut
    description='Extrait et stocke les cours de la bourse tous les matins', # Description pour les autres data engineers
    schedule_interval='13 52 * * 1-5', # Expression Cron : À 08h00, du Lundi (1) au Vendredi (5)
    catchup=False, # Ne pas rattraper les exécutions manquées (si le DAG était arrêté pendant un moment, il ne va pas essayer de faire tout le backlog)
    tags=['finance'] # Tags pour organiser les DAGs dans l'interface d'Airflow
) as dag:

    # 4. Création de la tâche physique
    tache_etl = PythonOperator(
        task_id='processus_elt_complet', # Nom de la tâche (doit être unique dans le DAG)
        python_callable=executer_pipeline_complet # La fonction à exécuter quand cette tâche est lancée
    )

    # Ordre d'exécution (ici on a qu'une seule grande tâche, donc on la met juste là)
    tache_etl