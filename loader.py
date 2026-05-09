import pandas as pd
import requests
from pathlib import Path
from src.config import DATA_DIR
from src.utils import logger

CONTACT_FILE = DATA_DIR / "contacts.csv"
REMINDER_FILE = DATA_DIR / "reminders.csv"


class DataLoader:
    def __init__(self):
        self.contacts = pd.DataFrame()
        self.reminders = pd.DataFrame()

    def load_csv_contacts(self):
        try:
            if CONTACT_FILE.exists():
                self.contacts = pd.read_csv(CONTACT_FILE)
                logger.info("Contacts loaded from CSV")
            return self.contacts
        except Exception as e:
            logger.error(f"CSV contacts load failed: {e}")
            return pd.DataFrame()

    def load_csv_reminders(self):
        try:
            if REMINDER_FILE.exists():
                self.reminders = pd.read_csv(REMINDER_FILE)
                logger.info("Reminders loaded from CSV")
            return self.reminders
        except Exception as e:
            logger.error(f"CSV reminders load failed: {e}")
            return pd.DataFrame()

    def load_api_contacts(self):
        try:
            url = "https://jsonplaceholder.typicode.com/users"
            response = requests.get(url, timeout=10)
            data = response.json()

            df = pd.DataFrame(data)
            df = df.rename(columns={
                "name": "full_name",
                "email": "email"
            })

            df["department"] = "Operations"
            df["status"] = "Active"

            logger.info("Contacts loaded from API")
            return df[["full_name", "email", "department", "status"]]

        except Exception as e:
            logger.error(f"API load failed: {e}")
            return pd.DataFrame()

    def clean(self, df):
        if df.empty:
            return df

        df = df.drop_duplicates()
        df = df.dropna()
        return df.reset_index(drop=True)

    def merge_sources(self):
        api_df = self.load_api_contacts()
        csv_df = self.load_csv_contacts()

        frames = []

        if not api_df.empty:
            frames.append(api_df)

        if not csv_df.empty:
            frames.append(csv_df)

        if frames:
            merged = pd.concat(frames, ignore_index=True)
            merged = self.clean(merged)
            logger.info("Data merged successfully")
            return merged

        return pd.DataFrame()