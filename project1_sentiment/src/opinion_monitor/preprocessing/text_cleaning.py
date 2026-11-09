"""Cleaning and normalization of raw text.

`clean_text` is used as the TfidfVectorizer preprocessor, so training and prediction
are guaranteed to apply identical cleaning. `clean_for_display` is only for the UI.
"""

import html
import re

_HTML_TAG = re.compile(r"<[^>]+>")
_URL = re.compile(r"https?://\S+|www\.\S+")
_MARKDOWN = re.compile(r"[*_#>`~]+")
_WHITESPACE = re.compile(r"\s+")

_BLOCK_BREAK = re.compile(r"<br\s*/?>|</(?:p|h[1-6]|li|div|article|section)>", re.IGNORECASE)
_MD_EMPHASIS = re.compile(r"\*+|_{2,}|`+|~{2,}")
_MD_LINE_PREFIX = re.compile(r"^\s*(?:#{1,6}|>)+\s*", re.MULTILINE)
_SPACES = re.compile(r"[ \t\u00a0]+")
_BLANK_LINES = re.compile(r"\n{3,}")


def clean_text(text: str) -> str:
    """Lowercase text and strip HTML tags, URLs, markdown symbols and extra whitespace."""
    if not isinstance(text, str):
        return ""
    text = html.unescape(text)
    text = _HTML_TAG.sub(" ", text)
    text = _URL.sub(" ", text)
    text = _MARKDOWN.sub(" ", text)
    text = _WHITESPACE.sub(" ", text)
    return text.strip().lower()


def clean_for_display(text: str) -> str:
    """Readable version of a review for the UI: no HTML/markdown noise, paragraphs kept, case kept."""
    if not isinstance(text, str):
        return ""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = _BLOCK_BREAK.sub("\n", text)
    text = _HTML_TAG.sub("", text)
    text = html.unescape(text)
    text = _URL.sub("[link]", text)
    text = _MD_LINE_PREFIX.sub("", text)
    text = _MD_EMPHASIS.sub("", text)
    lines = (_SPACES.sub(" ", line).strip() for line in text.split("\n"))
    text = "\n".join(lines)
    return _BLANK_LINES.sub("\n\n", text).strip()
