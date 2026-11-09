# EDT – Text Data Exploration

| Project | Topic | Status |
|---------|-------|--------|
| 1 | Intelligent opinion monitoring (sentiment) | Implemented – [`project1_sentiment/`](project1_sentiment/) |
| 2 | Semantic search and NER | Requirements only in `docs/requirements/` |

## Documentation

- [Overview](docs/requirements/00-overview.md)
- [Project 1 requirements](docs/requirements/project-1-sentiment-monitoring.md)
- [Project 2 requirements](docs/requirements/project-2-semantic-search-ner.md)

## Git – what is ignored

See [.gitignore](.gitignore). **Do not commit**, among others:

- `.env` (TMDB key) – use `.env.example`
- `.venv/`, `__pycache__/`, `*.egg-info/`
- `data/raw/*.csv` (Kaggle IMDB), `models/*.joblib` (after training)
- `AGENTS.md`, `.cursor/` (AI-local files)

After clone: setup steps in [project1_sentiment/README.md](project1_sentiment/README.md) (**Quick start**).
