import pandas as pd
import numpy as np

def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    # Napraw separator, jeśli plik ma jedną kolumnę
    if len(data.columns) == 1 and "," in data.columns[0]:
        data = data.iloc[1:].copy()
        data.columns = data.columns[0].split(",")
        data = data.reset_index(drop=True)

    # Kolumny wymagane do treningu lub predykcji
    keep_cols = [
        'Age',
        'Annual_Income',
        'Monthly_Inhand_Salary',
        'Num_of_Loan',
        'Num_of_Delayed_Payment',
        'Outstanding_Debt',
        'Amount_invested_monthly',
        'Monthly_Balance'
    ]

    # Dodajemy Credit_Score tylko jeśli istnieje (trening)
    if 'Credit_Score' in data.columns:
        keep_cols.append('Credit_Score')

    data = data[[col for col in keep_cols if col in data.columns]]

    # Usuwanie znaku podkreślenia i konwersja
    for col in data.columns:
        data[col] = data[col].astype(str).str.replace('_', '', regex=False)
        if col != 'Credit_Score':
            data[col] = pd.to_numeric(data[col], errors='coerce')

    # Filtrowanie wieku
    if 'Age' in data.columns:
        data.loc[(data['Age'] < 18) | (data['Age'] > 100), 'Age'] = np.nan

    # Uzupełnianie braków średnimi
    for col in data.columns:
        if col != 'Credit_Score':
            data[col] = data[col].fillna(data[col].astype(float).mean())

    # Zamiana Credit_Score tylko jeśli istnieje
    if 'Credit_Score' in data.columns:
        score_map = {"Poor": 0, "Standard": 1, "Good": 2}
        data['Credit_Score'] = data['Credit_Score'].map(score_map)
        data = data.dropna(subset=['Credit_Score'])

    return data

def print_columns(data: pd.DataFrame) -> None:
    print("Kolumny po czyszczeniu:\n", list(data.columns))

def clean_test(data: pd.DataFrame) -> pd.DataFrame:
    return clean_data(data)