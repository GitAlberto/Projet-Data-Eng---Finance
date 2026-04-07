from sqlalchemy import create_engine
from scripts.extract_nett import extract_financial_data, clean_data
def load_data(df):
    """Charge le DataFrame dans la base PostgreSQL locale via Docker."""
    
    print("\n Connexion à la base de données PostgreSQL...")
    
    # L'URL de connexion : dialecte+driver://utilisateur:motdepasse@hote:port/base_de_donnees
    # On utilise bien le port 5432 qu'on a ouvert dans le docker-compose
    db_url = "postgresql+psycopg2://airflow:airflow@postgres:5432/airflow"
    
    # Création du moteur de connexion
    engine = create_engine(db_url)
    
    try:
        # to_sql crée la table et insère les données 
        # if_exists='replace' écrase la table si elle existe. 
        # En production, on utiliserait plutôt 'append' (ajouter).
        df.to_sql(name='cours_bourse', con=engine, if_exists='replace', index=False)
        print(" == SUCCÈS : Données chargées dans la table 'cours_bourse' ! ==")
        
    except Exception as e:
        print(f" X-X Erreur lors du chargement en base : {e} X-X")

# --- Dans le bloc if __name__ == "__main__", ajoute l'appel à la fonction : ---

if __name__ == "__main__":
    entreprises_cibles = ['CA.PA', 'CS.PA', 'ORA.PA']
    
    # 1. Extract
    raw_data = extract_financial_data(entreprises_cibles)
    
    # 2. Clean (Transform)
    clean_df = clean_data(raw_data, entreprises_cibles)
    
    print("\n == Données financières nettoyées ! Voici les dernières valeurs : ==")
    print(clean_df.tail())
    
    # 3. Load 
    load_data(clean_df)