"""Classic ML sentiment model: TF-IDF + Logistic Regression (scikit-learn), persisted with joblib."""

from dataclasses import dataclass
from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from opinion_monitor import config
from opinion_monitor.preprocessing.text_cleaning import clean_text

POSITIVE = "positive"
NEGATIVE = "negative"


class ModelNotFoundError(FileNotFoundError):
    """Raised when the trained model file does not exist."""


@dataclass(frozen=True)
class Prediction:
    label: str  # "positive" | "negative"
    confidence: float  # probability of the predicted label, 0.5-1.0


def build_pipeline() -> Pipeline:
    return Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    preprocessor=clean_text,
                    ngram_range=(1, 2),
                    min_df=2,
                    max_df=0.95,
                    sublinear_tf=True,
                ),
            ),
            ("clf", LogisticRegression(max_iter=1000, C=4.0)),
        ]
    )


class SentimentModel:
    """Wrapper around a fitted sklearn pipeline."""

    def __init__(self, pipeline: Pipeline):
        self._pipeline = pipeline

    @classmethod
    def train(cls, texts, labels) -> "SentimentModel":
        pipeline = build_pipeline()
        pipeline.fit(texts, labels)
        return cls(pipeline)

    @classmethod
    def load(cls, path: Path = config.MODEL_PATH) -> "SentimentModel":
        path = Path(path)
        if not path.exists():
            raise ModelNotFoundError(
                f"Model not found: {path}. Train it first: python -m opinion_monitor.training.train"
            )
        return cls(joblib.load(path))

    def save(self, path: Path = config.MODEL_PATH) -> Path:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self._pipeline, path)
        return path

    def predict(self, texts) -> list[Prediction]:
        texts = list(texts)
        if not texts:
            return []
        proba_positive = self._pipeline.predict_proba(texts)[:, 1]
        return [
            Prediction(POSITIVE, float(p)) if p >= 0.5 else Prediction(NEGATIVE, float(1 - p))
            for p in proba_positive
        ]
