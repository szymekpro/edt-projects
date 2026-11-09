"""Loading the Kaggle "IMDB Dataset of 50K Movie Reviews" and creating the train/test split."""

from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

from opinion_monitor import config

LABEL_TO_INT = {"negative": 0, "positive": 1}


def load_imdb(path: Path = config.DATASET_PATH) -> pd.DataFrame:
    """Return a DataFrame with columns `review` (str) and `label` (0 = negative, 1 = positive)."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {path}. Download 'IMDB Dataset of 50K Movie Reviews' "
            "from Kaggle and place the CSV there (or set DATASET_PATH)."
        )
    df = pd.read_csv(path)
    missing = {"review", "sentiment"} - set(df.columns)
    if missing:
        raise ValueError(f"Dataset is missing columns: {sorted(missing)}")
    df = df.dropna(subset=["review", "sentiment"]).copy()
    df["label"] = df["sentiment"].str.lower().map(LABEL_TO_INT)
    df = df.dropna(subset=["label"])
    df["label"] = df["label"].astype(int)
    return df[["review", "label"]].reset_index(drop=True)


def split_dataset(df: pd.DataFrame):
    """Deterministic stratified split -> X_train, X_test, y_train, y_test."""
    return train_test_split(
        df["review"],
        df["label"],
        test_size=config.TEST_SIZE,
        random_state=config.RANDOM_STATE,
        stratify=df["label"],
    )
