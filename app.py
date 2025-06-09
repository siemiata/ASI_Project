import streamlit as st
import pandas as pd
import subprocess
from pathlib import Path
from autogluon.tabular import TabularPredictor
from azure.storage.blob import BlobServiceClient
import os
import uuid

st.title("🧠 Credit Scoring – Formularz oceny kredytowej")

model_path = Path("models")

if not model_path.exists() or not any(model_path.iterdir()):
    st.warning("⚠️ Model nie istnieje – uruchamiam `kedro run`...")

    try:
        subprocess.run(["kedro", "run"], check=True)
        st.success("✅ Model wytrenowany przez pipeline Kedro!")
    except subprocess.CalledProcessError as e:
        st.error(f"❌ Błąd podczas trenowania przez Kedro:\n{e}")
        st.stop()

model = TabularPredictor.load(str(model_path))

score_labels = {0: "Poor", 1: "Standard", 2: "Good"}

st.markdown("Wprowadź dane klienta:")

age = st.number_input("Wiek", min_value=18, max_value=100, value=30)
annual_income = st.number_input("Roczny dochód (PLN)", min_value=0.0, value=50000.0)
monthly_salary = st.number_input("Miesięczna wypłata (PLN)", min_value=0.0, value=4000.0)
num_loans = st.number_input("Liczba pożyczek", min_value=0, value=1)
num_delayed = st.number_input("Liczba opóźnień w spłacie", min_value=0, value=0)
outstanding_debt = st.number_input("Pozostały dług (PLN)", min_value=0.0, value=1000.0)
amount_invested = st.number_input("Kwota inwestowana miesięcznie (PLN)", min_value=0.0, value=500.0)
monthly_balance = st.number_input("Miesięczne saldo (PLN)", min_value=0.0, value=2000.0)

def save_prediction_to_blob(input_df: pd.DataFrame, prediction_label: str):
    try:
        connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")

        if not connect_str or not container_name:
            st.warning("⚠️ Brak konfiguracji Azure Storage – dane nie zostały zapisane.")
            return

        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        container_client = blob_service_client.get_container_client(container_name)

        input_df["Prediction"] = prediction_label
        blob_name = f"predictions/prediction_{uuid.uuid4().hex}.csv"
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(input_df.to_csv(index=False), overwrite=True)

        st.info(f"🗃️ Zapisano dane do Azure Blob Storage jako `{blob_name}`.")
    except Exception as e:
        st.error(f"❌ Błąd przy zapisie do Azure Blob: {e}")

if st.button("🔮 Przewiduj Credit Score"):
    input_df = pd.DataFrame([{
        "Age": age,
        "Annual_Income": annual_income,
        "Monthly_Inhand_Salary": monthly_salary,
        "Num_of_Loan": num_loans,
        "Num_of_Delayed_Payment": num_delayed,
        "Outstanding_Debt": outstanding_debt,
        "Amount_invested_monthly": amount_invested,
        "Monthly_Balance": monthly_balance
    }])

    prediction = model.predict(input_df)
    predicted_class = prediction.values[0]
    label = score_labels.get(predicted_class, "Nieznane")

    st.success(f"📊 Wynik modelu: {predicted_class} → {label}")

    save_prediction_to_blob(input_df, label)
