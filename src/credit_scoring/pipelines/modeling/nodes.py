from autogluon.tabular import TabularPredictor
import pandas as pd
from pathlib import Path
import os


def train_model(data: pd.DataFrame) -> None:
    model_path = Path("models")
    model_path.mkdir(parents=True, exist_ok=True)

    TabularPredictor(label="Credit_Score", path=str(model_path)).fit(
        data,
        presets="medium_quality_faster_train",
        auto_stack=False
    )


def predict_model(test_data: pd.DataFrame, train_data: pd.DataFrame) -> pd.DataFrame:
    print(f"Dane wejściowe do predykcji: {test_data.shape}")
    model_path = Path("models")

    
    if not model_path.exists() or not any(model_path.iterdir()):
        print("Model nie istnieje – rozpoczynam trening...")
        train_model(train_data)

    
    model = TabularPredictor.load(str(model_path))
    predictions = model.predict(test_data)
    print(f"Liczba predykcji: {len(predictions)}")
    print(f"Przykładowe predykcje:\n{predictions.head(20)}")

    return pd.DataFrame(predictions, columns=["Credit_Score_Predicted"])
