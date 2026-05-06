import logging
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict
from app.ml.data.generate_data import generate_leads_dataset
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

logger = logging.getLogger(__name__)


class LeadScoringModel:

    def __init__(self, model_version: str = "v1"):
        self.model = None
        self.model_version = model_version
        self.model_path = Path(f"models/lead_model_{model_version}.pkl")

        self.feature_order = [
            "years_experience",
            "company_size",
            "role_score",
            "activity_score"
        ]

    def train(self, n_samples: int = 1000):
        logger.info("Starting model training")

        #Generate dataset
        df = generate_leads_dataset(n=n_samples)

        X = df[self.feature_order]
        y = df["responded"]

        #Train/test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        #Pipeline
        pipeline = Pipeline([
            ("scaler", StandardScaler()),
            ("model", LogisticRegression(max_iter=1000))
        ])

        pipeline.fit(X_train, y_train)

        #Evaluation
        y_pred = pipeline.predict(X_test)
        report = classification_report(y_test, y_pred)

        logger.info("Model evaluation:\n" + report)

        #Save model
        self.model = pipeline
        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(pipeline, self.model_path)

        logger.info(f"Model saved to {self.model_path}")

    def load(self):
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model not found: {self.model_path}")

        self.model = joblib.load(self.model_path)
        logger.info(f"Loaded model from {self.model_path}")

    def predict_probab(self, features: Dict) -> float:
        if self.model is None:
            raise ValueError("Model not loaded. Call load() or train() first.")

        try:
            input_data = [features[f] for f in self.feature_order]
        except KeyError as e:
            raise ValueError(f"Missing feature: {e}")

        input_df = pd.DataFrame([features], columns=self.feature_order)

        prob = self.model.predict_proba(input_df)[0][1]

        return float(prob)

if __name__ == "__main__":
    model = LeadScoringModel()

    model.train(n_samples=1001)

    model.load()

    prob = model.predict_probab({
        "years_experience": 5,
        "company_size": 50,
        "role_score": 8,
        "activity_score": 9
    })

    print("Predicted probability:", prob)    