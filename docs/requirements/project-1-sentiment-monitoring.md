# Project 1 – Intelligent opinion monitoring system

## 1. Goal

Build an application that:

1. **Fetches texts from the Internet** via API or web scraping.  
   Texts may be fetched **only for prediction** (training data may be static, e.g. Kaggle).
2. **Automatically analyzes sentiment** as **positive / negative**.
3. Provides a **simple graphical user interface (GUI)**.
4. Uses **any suitable data source**, e.g. product reviews, social comments, movie reviews.

## 2. Detailed requirements

### 2.1 Data

| ID | Requirement |
|----|-------------|
| P1-D-01 | **Prediction data must come from the Internet** (API or scraping). Mandatory. |
| P1-D-02 | Training data may be: (a) pre-collected (e.g. Kaggle), or (b) fetched from the Internet at runtime. |
| P1-D-03 | Training and prediction data **may differ in source** if they are **consistent in structure and character** (domain, language, style, label scale). |
| P1-D-04 | Data source is free choice (products, social media, movies, etc.). |

### 2.2 Sentiment model

| ID | Requirement |
|----|-------------|
| P1-M-01 | Binary sentiment: **positive / negative**. |
| P1-M-02 | Model **may be trained if required** by the chosen approach. |
| P1-M-03 | If trained: on pre-collected data (e.g. Kaggle) **or** data fetched online at training time. |
| P1-M-04 | Sentiment analysis is **automatic** (no manual labeling of fetched texts). |

### 2.3 Application and GUI

| ID | Requirement |
|----|-------------|
| P1-G-01 | **Simple GUI**. |
| P1-G-02 | GUI triggers fetching from the Internet and shows sentiment results. |

> The assignment does not specify exact GUI screens – items in section 3 below are optional extras.

## 3. Optional ideas (not mandatory)

- Query/source selection in the GUI (product, movie, keyword).
- List of texts with sentiment label and confidence.
- Summary: positive/negative share, chart.
- Export results (CSV).
- Model quality on a test set (accuracy, F1, confusion matrix).

## 4. Done criteria (from assignment)

- [x] Prediction texts fetched from the Internet (TMDB API).
- [x] Automatic positive/negative classification.
- [x] Working simple GUI (Tkinter).
- [x] Training vs prediction sources and IMDB↔TMDB consistency documented in `docs/requirements/` and README (no separate report required by assignment text unless instructor requires it).
- [x] Trained model: `train` + `evaluate` (IMDB test metrics).

## 5. Decisions made

Criterion: simplest, clearest, fastest to deliver.

| Topic | Decision | Rationale |
|-------|----------|-----------|
| Text language | **English** | Dataset and model choice. |
| Written report | **Not in P1 assignment** | README + requirements docs if explanation is needed. |
| Training data | **Kaggle: IMDB 50K Movie Reviews** | Labeled pos/neg, balanced, static (P1-D-02a). |
| Prediction data | **TMDB API** (reviews by title) | Legal API, free key; same domain (movie reviews, EN) for P1-D-03. |
| Model | **TF-IDF + Logistic Regression** (scikit-learn) | Fast CPU training, interpretable. |
| UI | **Tkinter GUI** | Meets P1-G-01, stdlib. Logic in `pipeline` only. |

Planned GUI: title field + “Fetch and analyze”, table (snippet | sentiment | confidence), summary bar, status line.  
Training/evaluation: `python -m opinion_monitor.training.train` and `python -m opinion_monitor.training.evaluate`.

## 6. Risks and notes

- **Tkinter + threads.** Network calls run off the UI thread so the window stays responsive.
- **Domain shift.** TMDB reviews are often shorter and more informal than IMDB 50K; document in README and demo (e.g. Morbius vs Inception).
- **No sentiment labels on TMDB.** Only optional author star ratings; live accuracy needs manual checks or weak labels (`evaluate_web`).
- **API key.** TMDB registration; store in `.env`, not in git.

## 7. Open decisions

- Max reviews per query and UX when a movie has none (current default: `MAX_REVIEWS=40`, errors via `NoReviewsError`).
- Neutral class: assignment is binary only; default is no neutral class.

## 8. Requirements traceability

### Flow

- **Training:** Kaggle IMDB 50K → `clean_text` inside TF-IDF → Logistic Regression → `models/sentiment_model.joblib`.
- **Prediction:** title in GUI → TMDB → same cleaning in saved pipeline → labels in table.
- GUI calls only `pipeline`; fetch runs in a background thread.

### Mapping

| Requirement | How we meet it | Code |
|-------------|----------------|------|
| Fetch from Internet (P1-D-01) | TMDB API for prediction only | `data_sources/api_source.py` |
| Static training allowed (P1-D-02) | Kaggle IMDB CSV | `training/dataset.py` |
| Different sources, consistent (P1-D-03) | EN movie reviews; rationale in docs | `docs/requirements/`, README |
| Free data source (P1-D-04) | Movie reviews (listed in assignment) | – |
| Auto binary sentiment (P1-M-01, P1-M-04) | No manual labeling in GUI | `model/sentiment_model.py` |
| Training (P1-M-02, P1-M-03) | Train on Kaggle; `evaluate` metrics | `training/train.py`, `training/evaluate.py` |
| Simple GUI (P1-G-01) | Tkinter | `gui/app.py` |
| Fetch + show results (P1-G-02) | “Fetch and analyze” → `pipeline` | `gui/app.py`, `pipeline.py` |

### Implementation status

- Code: train, GUI, TMDB, `evaluate`, `evaluate_web`.
- TMDB has no gold sentiment labels; `evaluate_web` uses reviewer ratings as weak labels only.
