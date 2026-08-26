import pandas as pd

def load_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

def filter_by_source(df: pd.DataFrame, source: str) -> pd.DataFrame:
    return df[df["log_source"] == source].copy()