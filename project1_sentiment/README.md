# Project 1 – Intelligent opinion monitoring

Tkinter GUI app: fetches movie reviews from TMDB and classifies sentiment (positive / negative).  
Requirements: [`../docs/requirements/project-1-sentiment-monitoring.md`](../docs/requirements/project-1-sentiment-monitoring.md).

## Quick start

**Requires:** Python 3.10+, internet, free [TMDB API key](https://www.themoviedb.org/settings/api) (v3 key).

1. Download Kaggle [IMDB Dataset of 50K Movie Reviews](https://www.kaggle.com/datasets/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews) and save the CSV as `data/raw/IMDB Dataset.csv`.
2. From this folder (`project1_sentiment`):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -e .
copy .env.example .env
```

3. Set `TMDB_API_KEY=...` in `.env`.
4. Train and run:

```powershell
python -m opinion_monitor.training.train
python -m opinion_monitor                    # GUI: movie title → Fetch and analyze
```

Optional:

```powershell
python -m opinion_monitor.training.evaluate       # IMDB held-out test metrics
python -m opinion_monitor.training.evaluate_web   # TMDB reviews, weak labels from user ratings
```

The trained model is saved to `models/sentiment_model.joblib` (gitignored). Run `train` before the GUI if the file is missing.

## Stack

| Piece | Choice |
|-------|--------|
| Training | Kaggle IMDB 50K → TF-IDF + Logistic Regression |
| Prediction | TMDB API (live reviews) |
| On-disk model | `models/sentiment_model.joblib` (from `training.train`) |
| GUI | Tkinter (stdlib) |

## Data consistency (assignment P1-D-03)

Training uses **English movie reviews** from Kaggle IMDB. Prediction uses **English user reviews** from TMDB for the same domain (movies). Reviews differ in length and tone (TMDB is often shorter); the same binary labels and `clean_text` preprocessing apply to both paths.

## `models/sentiment_model.joblib`

Serialized **fitted** scikit-learn pipeline (TF-IDF vocabulary + logistic regression weights). Created by `training.train`. GUI and `pipeline` load this file instead of retraining on every run.

- Delete it → run `python -m opinion_monitor.training.train` again.
- Change training data or hyperparameters → run `train` again.
- Not in git (local artifact); reviewers train from CSV + README.

## Layout

```
project1_sentiment/
├── data/raw/          # IMDB CSV (gitignored)
├── models/            # sentiment_model.joblib (gitignored)
└── src/opinion_monitor/
```
