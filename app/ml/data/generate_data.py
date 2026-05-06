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
        #Feature distributions (more realistic than uniform)

        years_experience = int(np.clip(np.random.normal(5, 3), 0, 20))
        company_size = int(np.clip(np.random.lognormal(mean=3, sigma=1), 1, 5000))
        role_score = np.random.randint(1, 10)
        activity_score = np.random.randint(1, 10)

        score = 0

        score += activity_score * 0.5
        score += years_experience * 0.2

        if company_size < 50:
            score += 2

        if role_score > 7:
            score += 2.5

        #Feature interaction
        if role_score > 7 and activity_score > 7:
            score += 2

        #Add noise
        score += np.random.normal(0, 1)

        #Convert to probability
        probability = 1 / (1 + np.exp(-score / 5))  # sigmoid scaling

        #Class imbalance control
        # Bias towards fewer positive responses
        probability *= 0.6

        responded = np.random.binomial(1, probability)

        data.append({
            "years_experience": years_experience,
            "company_size": company_size,
            "role_score": role_score,
            "activity_score": activity_score,
            "responded": responded
        })

    df = pd.DataFrame(data)

    positive_rate = df["responded"].mean()
    logger.info(f"Generated dataset with {n} rows | response_rate={positive_rate:.2f}")

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