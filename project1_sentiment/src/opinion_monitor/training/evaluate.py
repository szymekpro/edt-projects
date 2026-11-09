"""Model evaluation on the held-out test split: `python -m opinion_monitor.training.evaluate`."""

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from opinion_monitor.model.sentiment_model import POSITIVE, SentimentModel
from opinion_monitor.training.dataset import load_imdb, split_dataset


def main() -> None:
    df = load_imdb()
    _, X_test, _, y_test = split_dataset(df)
    model = SentimentModel.load()
    y_pred = [1 if p.label == POSITIVE else 0 for p in model.predict(X_test)]

    print(f"Test reviews: {len(y_test)}")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}\n")
    print(classification_report(y_test, y_pred, target_names=["negative", "positive"], digits=4))
    print("Confusion matrix (rows = true, cols = predicted; order: negative, positive):")
    print(confusion_matrix(y_test, y_pred))


if __name__ == "__main__":
    main()
