import pandas as pd

# Exemple de données
data = {
    'transactionTime': ['2023-01-01 16:30:00', '2023-01-01 17:45:00', '2023-01-02 16:15:00', '2023-01-02 17:30:00'],
    'numberOutcomeTransaction': [10, 20, 15, 25],
    'numberIncomeTransaction': [5, 15, 10, 20],
    'totalIncome': [100, 200, 150, 250],
    'totalOutcome': [80, 180, 130, 230],
    'totalNumberTransaction': [15, 35, 25, 45]
}

# Créer un DataFrame
df = pd.DataFrame(data)

# Convertir la colonne transactionTime en datetime
df['transactionTime'] = pd.to_datetime(df['transactionTime'])

# Ajouter une colonne 'date' pour agréger par jour
df['date'] = df['transactionTime'].dt.date

# Agréger les données par jour
daily_outcome = df.groupby('date')['numberOutcomeTransaction'].sum().reset_index()

# Convertir les dates et les valeurs en listes
dates = daily_outcome['date'].astype(str).tolist()
outcomes = daily_outcome['numberOutcomeTransaction'].tolist()

# Afficher les résultats
print(dates)
print(outcomes)
