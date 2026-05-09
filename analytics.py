import pandas as pd


def build_summary(df: pd.DataFrame):
    if df.empty:
        return pd.DataFrame()

    summary = df["department"].value_counts().reset_index()
    summary.columns = ["Department", "Count"]
    return summary