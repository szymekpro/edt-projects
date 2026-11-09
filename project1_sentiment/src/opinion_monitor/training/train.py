"""Training entry point: `python -m opinion_monitor.training.train`.

Loads IMDB 50K, trains on the train split and saves the model to config.MODEL_PATH.
"""

from opinion_monitor import config
from opinion_monitor.model.sentiment_model import SentimentModel
from opinion_monitor.training.dataset import load_imdb, split_dataset


def main() -> None:
    df = load_imdb()
    X_train, _, y_train, _ = split_dataset(df)
    print(f"Training on {len(X_train)} reviews...")
    model = SentimentModel.train(X_train, y_train)
    path = model.save(config.MODEL_PATH)
    print(f"Model saved to {path}")


if __name__ == "__main__":
    main()
