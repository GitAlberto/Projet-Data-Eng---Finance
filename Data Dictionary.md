## Annexe : Dictionnaire des Données (Data Dictionary)
Ce document décrit les colonnes retenues à la fin du processus d'extraction et de nettoyage (pipeline ELT), qui seront chargées dans la base de données PostgreSQL pour alimenter les tableaux de bord métiers.

date_cloture (Type : Date)

Description : La date exacte à laquelle la séance boursière s'est terminée.

Pourquoi je la garde (Valeur Métier) : C'est la clé de voûte de toute analyse temporelle (Time-Series). Elle permettra dans Power BI de créer l'axe des abscisses (X) pour observer les tendances, calculer des moyennes, ou comparer les performances d'un mois sur l'autre (MoM - Month over Month).

Entreprise (Type : Texte / Chaîne de caractères)

Description : Le symbole boursier (Ticker) identifiant l'entreprise sur le marché financier (ex: CA.PA pour Carrefour, CS.PA pour AXA).

Pourquoi je la garde (Valeur Métier) : C'est notre axe d'analyse principal (Dimension). Sans cette colonne, toutes les données seraient mélangées. Elle permet de filtrer les visuels dans Power BI, de comparer les entreprises entre elles (Benchmark concurrentiel) et servira de clé de jointure si l'on souhaite croiser cette table avec un référentiel d'entreprises (secteur d'activité, pays, etc.).

prix_cloture_eur (Type : Numérique / Float)

Description : La valeur de l'action de l'entreprise à la fermeture du marché, exprimée en Euros et arrondie à deux décimales.

Pourquoi on la garde (Valeur Métier) : C'est le KPI financier (Indicateur de Performance) numéro un. Il reflète la valorisation de l'entreprise par le marché à un instant T. Il permet aux analystes de calculer la rentabilité, la volatilité (le risque) et la santé financière globale des concurrents.

volume_echanges (Type : Numérique / Entier)

Description : Le nombre total d'actions de cette entreprise qui ont été achetées et vendues au cours de cette journée.

Pourquoi on la garde (Valeur Métier) : Le volume donne du "poids" au prix. Une chute du prix de l'action avec un volume d'échanges très faible n'est pas très inquiétante. En revanche, une chute du prix accompagnée d'un volume d'échanges massif indique un mouvement de panique (les investisseurs fuient). C'est un indicateur de liquidité crucial pour les analystes financiers.