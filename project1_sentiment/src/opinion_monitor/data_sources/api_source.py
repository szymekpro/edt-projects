"""TMDB API source: search a movie by title, then fetch its user reviews."""

import requests

from opinion_monitor import config
from opinion_monitor.data_sources.base import (
    BaseSource,
    MissingApiKeyError,
    NoReviewsError,
    Review,
    SourceError,
    SubjectNotFoundError,
)


class TMDBSource(BaseSource):
    def __init__(self, api_key: str | None = None, base_url: str = config.TMDB_BASE_URL):
        self._api_key = config.TMDB_API_KEY if api_key is None else api_key
        self._base_url = base_url

    def fetch(self, query: str, limit: int = config.MAX_REVIEWS) -> list[Review]:
        query = query.strip()
        if not query:
            raise SubjectNotFoundError("Enter a movie title.")
        if not self._api_key:
            raise MissingApiKeyError("TMDB_API_KEY is not set (see .env.example).")

        movie = self._search_movie(query)
        subject = self._subject_name(movie)

        reviews: list[Review] = []
        page, total_pages = 1, 1
        while page <= total_pages and len(reviews) < limit:
            data = self._get(f"/movie/{movie['id']}/reviews", page=page)
            total_pages = data.get("total_pages", 1)
            for item in data.get("results", []):
                text = (item.get("content") or "").strip()
                if not text:
                    continue
                rating = (item.get("author_details") or {}).get("rating")
                reviews.append(
                    Review(
                        text=text,
                        subject=subject,
                        source="TMDB",
                        author=item.get("author", ""),
                        rating=rating,
                        url=item.get("url", ""),
                    )
                )
            page += 1

        if not reviews:
            raise NoReviewsError(f"No reviews found for '{subject}'.")
        return reviews[:limit]

    def _search_movie(self, query: str) -> dict:
        results = self._get("/search/movie", query=query).get("results", [])
        if not results:
            raise SubjectNotFoundError(f"Movie not found: '{query}'.")
        return results[0]

    @staticmethod
    def _subject_name(movie: dict) -> str:
        title = movie.get("title") or movie.get("original_title") or "Unknown"
        year = (movie.get("release_date") or "")[:4]
        return f"{title} ({year})" if year else title

    def _get(self, path: str, **params) -> dict:
        try:
            response = requests.get(
                f"{self._base_url}{path}",
                params={"api_key": self._api_key, **params},
                timeout=config.REQUEST_TIMEOUT_S,
            )
        except requests.RequestException as exc:
            raise SourceError(f"Network error: {exc}") from exc
        if response.status_code == 401:
            raise MissingApiKeyError("TMDB rejected the API key (401).")
        if not response.ok:
            raise SourceError(f"TMDB error: HTTP {response.status_code}")
        return response.json()
