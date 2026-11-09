"""Common interface for text sources and the shared record format."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


class SourceError(Exception):
    pass


class MissingApiKeyError(SourceError):
    pass


class SubjectNotFoundError(SourceError):
    pass


class NoReviewsError(SourceError):
    pass


@dataclass(frozen=True)
class Review:
    text: str
    subject: str
    source: str
    author: str = ""
    rating: float | None = None
    url: str = ""


class BaseSource(ABC):
    @abstractmethod
    def fetch(self, query: str, limit: int) -> list[Review]:
        pass
