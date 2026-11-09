"""Central configuration: paths, model settings, API settings (secrets come from env / .env)."""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BASE_DIR / ".env")

DATA_RAW_DIR = BASE_DIR / "data" / "raw"
MODELS_DIR = BASE_DIR / "models"

DATASET_PATH = Path(os.getenv("DATASET_PATH", DATA_RAW_DIR / "IMDB Dataset.csv"))
MODEL_PATH = Path(os.getenv("MODEL_PATH", MODELS_DIR / "sentiment_model.joblib"))

TEST_SIZE = 0.2
RANDOM_STATE = 42

TMDB_API_KEY = os.getenv("TMDB_API_KEY", "")
TMDB_BASE_URL = "https://api.themoviedb.org/3"
REQUEST_TIMEOUT_S = 10

MAX_REVIEWS = 40
