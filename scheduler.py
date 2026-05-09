import pandas as pd
from pathlib import Path
from src.config import OUTPUT_DIR
from src.utils import logger, ensure_folder

ensure_folder(OUTPUT_DIR)

SCHEDULE_FILE = OUTPUT_DIR / "scheduled_reminders.csv"


def save_schedule(reminder_type, reminder_date, message):
    data = pd.DataFrame([{
        "type": reminder_type,
        "date": str(reminder_date),
        "message": message
    }])

    data.to_csv(SCHEDULE_FILE, index=False)

    logger.info("Reminder scheduled")
    return True