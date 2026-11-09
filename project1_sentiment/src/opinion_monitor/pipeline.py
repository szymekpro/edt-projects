"""End-to-end flow used by the GUI: fetch reviews -> predict sentiment -> return result."""

from dataclasses import dataclass
from functools import cached_property

from opinion_monitor import config
from opinion_monitor.data_sources.api_source import TMDBSource
from opinion_monitor.data_sources.base import BaseSource, Review
from opinion_monitor.model.sentiment_model import POSITIVE, SentimentModel
from opinion_monitor.preprocessing.text_cleaning import clean_for_display


@dataclass(frozen=True)
class AnalyzedReview:
    review: Review
    label: str
    confidence: float

    @cached_property
    def display_text(self) -> str:
        """Review text cleaned for showing in the UI (no HTML/markdown noise)."""
        return clean_for_display(self.review.text)


@dataclass(frozen=True)
class AnalysisResult:
    query: str
    subject: str
    items: list[AnalyzedReview]

    @property
    def positive_count(self) -> int:
        return sum(1 for i in self.items if i.label == POSITIVE)

    @property
    def negative_count(self) -> int:
        return len(self.items) - self.positive_count

    @property
    def positive_share(self) -> float:
        return self.positive_count / len(self.items) if self.items else 0.0


def analyze(
    query: str,
    limit: int = config.MAX_REVIEWS,
    source: BaseSource | None = None,
    model: SentimentModel | None = None,
) -> AnalysisResult:
    """Fetch reviews for `query` from the Internet and classify each one."""
    model = model or SentimentModel.load()
    source = source or TMDBSource()

    reviews = source.fetch(query, limit)
    predictions = model.predict(r.text for r in reviews)
    items = [AnalyzedReview(r, p.label, p.confidence) for r, p in zip(reviews, predictions)]
    return AnalysisResult(query=query, subject=reviews[0].subject, items=items)
