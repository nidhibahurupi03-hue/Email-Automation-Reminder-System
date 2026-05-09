import pandas as pd
from src.config import OUTPUT_DIR
from src.utils import logger, ensure_folder

ensure_folder(OUTPUT_DIR)


def run_dry(df):
    results = []

    for _, row in df.iterrows():
        logger.info(f"Simulated mail sent to {row['email']}")

        results.append({
            "name": row["full_name"],
            "email": row["email"],
            "status": "Sent"
        })

    report = pd.DataFrame(results)
    report.to_csv(OUTPUT_DIR / "sent_report.csv", index=False)

    return report