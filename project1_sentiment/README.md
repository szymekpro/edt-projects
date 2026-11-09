# Projekt 1 – Inteligentny system monitorowania opinii

Aplikacja z GUI (Tkinter): pobiera recenzje filmów z TMDB, klasyfikuje sentyment (pozytywny / negatywny).
Wymagania: [`../docs/requirements/project-1-sentiment-monitoring.md`](../docs/requirements/project-1-sentiment-monitoring.md).

## Quick start (English)

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

3. Put your TMDB key in `.env` as `TMDB_API_KEY=...`.
4. Train and run:

```powershell
python -m opinion_monitor.training.train
python -m opinion_monitor                    # GUI: enter a movie title → Fetch and analyze
```

Optional: `python -m opinion_monitor.training.evaluate` (held-out IMDB test metrics).  
The trained model is written to `models/sentiment_model.joblib` (not in git). Without it, run `train` before the GUI.

## Stack

| Element | Wybór |
|---------|-------|
| Trening | Kaggle IMDB 50K → TF-IDF + Logistic Regression |
| Predykcja | TMDB API |
| Model na dysku | `models/sentiment_model.joblib` (wynik `training.train`, patrz niżej) |
| GUI | Tkinter |

## Uruchomienie (PowerShell)

```powershell
cd project1_sentiment
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -e .
copy .env.example .env          # TMDB_API_KEY
# data/raw/IMDB Dataset.csv     # z Kaggle
python -m opinion_monitor.training.train
python -m opinion_monitor.training.evaluate      # IMDB, test split
python -m opinion_monitor.training.evaluate_web  # TMDB, słaba etykieta z oceny użytkownika
python -m opinion_monitor                        # GUI
```

## Plik `models/sentiment_model.joblib`

To **zapisany, wytrenowany model** (cały pipeline scikit-learn: słownik TF-IDF + wagi regresji logistycznej).
Powstaje po `training.train` z danych IMDB. GUI i `pipeline` **ładują ten plik**, zamiast trenować od zera przy każdym uruchomieniu.

- Usuniesz go → trzeba ponownie `python -m opinion_monitor.training.train`.
- Zmienisz dane lub parametry treningu → znowu `train`.
- Jest w `.gitignore` (duży, zależy od Twojego komputera) – na oddanie oddajesz kod + instrukcję treningu, nie ten plik.

## Katalogi

```
project1_sentiment/
├── data/raw/          # IMDB CSV (poza gitem)
├── models/            # sentiment_model.joblib (poza gitem)
└── src/opinion_monitor/
```
