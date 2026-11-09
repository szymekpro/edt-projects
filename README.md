# EDT – Eksploracja danych tekstowych

| Projekt | Temat | Stan |
|---------|-------|------|
| 1 | Inteligentny system monitorowania opinii | Zaimplementowany – [`project1_sentiment/`](project1_sentiment/) |
| 2 | Wyszukiwanie semantyczne i NER | Tylko wymagania w `docs/requirements/` |

## Dokumentacja

- [Przegląd](docs/requirements/00-overview.md)
- [Wymagania – Projekt 1](docs/requirements/project-1-sentiment-monitoring.md)
- [Wymagania – Projekt 2](docs/requirements/project-2-semantic-search-ner.md)

## Repozytorium git – co jest ignorowane

Zob. [.gitignore](.gitignore). M.in. **nie commituj**:

- `.env` (klucz TMDB) – jest `.env.example`
- `.venv/`, `__pycache__/`, `*.egg-info/`
- `data/raw/*.csv` (IMDB z Kaggle), `models/*.joblib` (po treningu)
- `AGENTS.md`, `.cursor/` (pliki pod AI, poza oddaniem)

Po sklonowaniu: krótka instrukcja po angielsku w [project1_sentiment/README.md](project1_sentiment/README.md) (sekcja **Quick start**).
