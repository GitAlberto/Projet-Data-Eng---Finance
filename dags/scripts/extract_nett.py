import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def extract_financial_data(tickers):
    """Extrait les données boursières de la veille pour une liste d'entreprises."""
    # Calcule la date d'hier pour s'assurer d'avoir des données complètes (hors week-end)
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d') # On prend 365 jours pour être sûr d'avoir des données (hors week-end)
    
    print(f"Téléchargement des données pour : {tickers}...")
    
    # yfinance télécharge directement les données au format Pandas DataFrame
    df = yf.download(tickers, start=start_date, end=end_date, group_by='ticker')
    
    return df

def clean_data(raw_df, tickers):
    """Transforme les données boursières brutes en format base de données (lignes)."""
    clean_rows = [] # Liste pour stocker les DataFrames nettoyés de chaque entreprise
    
    # On boucle sur chaque entreprise pour restructurer la donnée proprement
    for ticker in tickers:
        # On extrait les données spécifiques à l'entreprise
        ticker_df = raw_df[ticker].copy()
        ticker_df = ticker_df.dropna() # On enlève les jours fériés / week-ends (valeurs nulles)
        
        # On réinitialise l'index pour que la Date devienne une colonne valide
        ticker_df = ticker_df.reset_index()
        
        # On ajoute le nom de l'entreprise comme colonne pour pouvoir filtrer dans Power BI
        ticker_df['Entreprise'] = ticker
        
        clean_rows.append(ticker_df) # On stocke le DataFrame nettoyé de l'entreprise dans la liste
    
    # On fusionne le tout en un seul grand tableau
    final_df = pd.concat(clean_rows, ignore_index=True) 
    
    # Nettoyage final : renommage des colonnes (SQL friendly) et sélection de ce qui est utile
    final_df.rename(columns={
        'Date': 'date_cloture',
        'Close': 'prix_cloture_eur',
        'Volume': 'volume_echanges',
        'Open': 'prix_ouverture_eur',
        'High': 'prix_plus_haut_eur',
        'Low': 'prix_plus_bas_eur'
    }, inplace=True ) # Inplace = True : Pour que les changements soient appliqués directement sur le DataFrame
    
    # On ne garde que les colonnes qui vont intéresser le métier
    final_df = final_df[['date_cloture', 'Entreprise', 'prix_cloture_eur', 'volume_echanges', 'prix_ouverture_eur', 'prix_plus_haut_eur', 'prix_plus_bas_eur']]
    
    # Arrondir les prix à 2 décimales pour la propreté
    final_df['prix_cloture_eur'] = final_df['prix_cloture_eur'].round(2)
    final_df['prix_ouverture_eur'] = final_df['prix_ouverture_eur'].round(2)
    final_df['prix_plus_haut_eur'] = final_df['prix_plus_haut_eur'].round(2)
    final_df['prix_plus_bas_eur'] = final_df['prix_plus_bas_eur'].round(2)

    # On renomme le CAC40 en CAC40_eur
    final_df['Entreprise'] = final_df['Entreprise'].replace('^FCHI', 'CAC40_eur')
    
    return final_df

if __name__ == "__main__":
    # Nos cibles métiers : Carrefour (CA.PA), AXA (CS.PA), Orange (ORA.PA), BNP (BNP.PA), TotalEnergies (TTE.PA)
    # Le ".PA" signifie qu'on regarde sur le marché de Paris (Euronext)
    entreprises_cibles = ['CA.PA', 'CS.PA', 'ORA.PA', 'BNP.PA','TTE.PA','^FCHI']
    
    # Étape 1 : Extraction des données financières de la veille dans un format brut (avec toutes les colonnes que yfinance fournit)
    raw_data = extract_financial_data(entreprises_cibles)
    # Nettoyage et transformation des données pour les rendre exploitables par Power BI selon les regles de ma fonction clean_data
    clean_df = clean_data(raw_data, entreprises_cibles)
    
    # Affichage des résultats pour vérification
    print("\n Données financières nettoyées ! Voici les dernières valeurs :")
    print(clean_df.tail()) # Affiche les dernières lignes
    
    print("\n Structure prête pour PostgreSQL :")
    print(clean_df.info())
    print("\n Aperçu des données :")
    print(clean_df.head())