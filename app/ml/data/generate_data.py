import pandas as pd
import numpy as np
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def generate_leads_dataset(
    n: int = 1000,
    seed: int = 42,
    save_path: str | None = None
) -> pd.DataFrame:

    np.random.seed(seed)

    data = []

    for _ in range(n):

        #FEATURE DISTRIBUTIONS

        years_experience = int(np.clip(np.random.normal(5, 3), 0, 20))

        company_size = int(
            np.clip(np.random.lognormal(mean=3, sigma=1), 1, 5000)
        )

        role_score = np.random.randint(1, 11)   # 1–10 (slightly stronger scale)
        activity_score = np.random.randint(1, 11)

        #BASE SCORING FUNCTION

        score = 0.0

        # Strongest signal → activity
        score += activity_score * 0.8

        # Experience matters but less than activity
        score += years_experience * 0.3

        # Company size influence (SMBs respond more)
        if company_size < 100:
            score += 2.5
        elif company_size < 500:
            score += 1.0

        # Role strength
        if role_score >= 8:
            score += 3.0
        elif role_score >= 6:
            score += 1.5

        #FEATURE INTERACTIONS

        # High intent synergy
        if role_score >= 8 and activity_score >= 8:
            score += 3.5

        if activity_score >= 7 and years_experience >= 7:
            score += 2.0

        #NOISE

        score += np.random.normal(0, 0.8)

        #CONVERT TO PROBABILITY

        probability = 1 / (1 + np.exp(-score / 4.5))

        #Slight class imbalance 
        probability *= 0.65

        #Clamp probability
        probability = np.clip(probability, 0.01, 0.95)

        #LABEL GENERATION

        responded = np.random.binomial(1, probability)

        data.append({
            "years_experience": years_experience,
            "company_size": company_size,
            "role_score": role_score,
            "activity_score": activity_score,
            "responded": responded
        })

    df = pd.DataFrame(data)

    #DATASET HEALTH CHECK

    positive_rate = df["responded"].mean()
    logger.info(
        f"Generated dataset | rows={n} | response_rate={positive_rate:.2f}"
    )

    #SAVE DATASET

    if save_path:
        path = Path(save_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(path, index=False)
        logger.info(f"Dataset saved to {path.resolve()}")

    return df

if __name__ == "__main__":
    df = generate_leads_dataset(
        n=1001,
        save_path="app/ml/data/leads_dataset.csv"
    )

    print(df.head())