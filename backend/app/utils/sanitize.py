"""Input sanitization utilities."""

from __future__ import annotations

import re


# Matches HTML/script tags (opening and closing, with attributes)
_TAG_RE = re.compile(r"</?[a-zA-Z][^>]*>", re.DOTALL)


def sanitize_input(value: str) -> str:
    """Strip HTML/script tags and trim whitespace from *value*.

    This provides basic sanitization for user-supplied text fields.
    """
    cleaned = _TAG_RE.sub("", value)
    return cleaned.strip()
