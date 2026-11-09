"""Estimate model quality on real Internet data (TMDB) using the reviewer's own rating as a weak label.

    python -m opinion_monitor.training.evaluate_web                      # default list of movies
    python -m opinion_monitor.training.evaluate_web "Inception" "Morbius"

Weak label: rating >= 7 -> positive, rating <= 4 -> negative; reviews without a rating or
with a rating of 5-6 (ambiguous) are skipped. This is only an approximation of the true sentiment.
"""

import sys

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from opinion_monitor import pipeline
from opinion_monitor.data_sources.api_source import TMDBSource
from opinion_monitor.data_sources.base import SourceError
from opinion_monitor.model.sentiment_model import NEGATIVE, POSITIVE, SentimentModel

POSITIVE_MIN_RATING = 7.0
NEGATIVE_MAX_RATING = 4.0

DEFAULT_MOVIES = [
    "Inception", "The Dark Knight", "Interstellar", "Parasite", "Joker", "Avatar", "Oppenheimer",
    "Morbius", "Madame Web", "The Last Airbender 2010", "Batman & Robin", "Transformers: The Last Knight",
]


def weak_label(rating: float | None) -> str | None:
    if rating is None:
        return None
    if rating >= POSITIVE_MIN_RATING:
        return POSITIVE
    if rating <= NEGATIVE_MAX_RATING:
        return NEGATIVE
    return None


def main() -> None:
    movies = sys.argv[1:] or DEFAULT_MOVIES
    model = SentimentModel.load()
    source = TMDBSource()

    y_true: list[str] = []
    y_pred: list[str] = []
    mistakes: list[tuple[str, float, str, str]] = []
    total_reviews = 0

    for title in movies:
        try:
            result = pipeline.analyze(title, source=source, model=model)
        except SourceError as exc:
            print(f"[skip] {title}: {exc}")
            continue
        used = 0
        for item in result.items:
            total_reviews += 1
            truth = weak_label(item.review.rating)
            if truth is None:
                continue
            used += 1
            y_true.append(truth)
            y_pred.append(item.label)
            if truth != item.label:
                mistakes.append((result.subject, item.review.rating, item.label, item.display_text))
        print(f"[ok]   {result.subject}: {len(result.items)} reviews, {used} with usable rating")

    print(f"\nReviews fetched: {total_reviews}, used (rating >= {POSITIVE_MIN_RATING:g} or <= {NEGATIVE_MAX_RATING:g}): {len(y_true)}")
    if not y_true:
        print("Nothing to evaluate.")
        return

    print(f"Accuracy vs. rating-based label: {accuracy_score(y_true, y_pred):.4f}\n")
    print(classification_report(y_true, y_pred, labels=[NEGATIVE, POSITIVE], zero_division=0, digits=3))
    print("Confusion matrix (rows = rating-based label, cols = model; order: negative, positive):")
    print(confusion_matrix(y_true, y_pred, labels=[NEGATIVE, POSITIVE]))

    if mistakes:
        print(f"\nDisagreements ({len(mistakes)}) - check by hand, the rating can be misleading:")
        for subject, rating, predicted, text in mistakes:
            snippet = " ".join(text.split())[:160]
            print(f"- {subject} | rating {rating:g} | model: {predicted} | {snippet}")


if __name__ == "__main__":
    main()
