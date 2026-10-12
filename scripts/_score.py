"""Extension conflict scoring, ported from jshttp mime-types 3.0.2.

Source: https://cdn.jsdelivr.net/npm/mime-types@3.0.2/mimeScore.js and the
``_preferredType`` function in https://cdn.jsdelivr.net/npm/mime-types@3.0.2/index.js
(retrieved 2026-10-12). mime-types is MIT licensed; see LICENSES/mime-types.txt.

The constants and the arithmetic below follow that code exactly so that the
extension to type answers agree with mime-types for the same mime-db version.
"""

from __future__ import annotations

import re

FACET_SCORES = {"prs.": 100, "x-": 200, "x.": 300, "vnd.": 400}
FACET_DEFAULT = 900

SOURCE_SCORES = {"nginx": 10, "apache": 20, "iana": 40}
SOURCE_DEFAULT = 30

TYPE_SCORES = {"application": 1, "font": 2, "audio": 2, "video": 3}
TYPE_DEFAULT = 0

_FACET = re.compile(r"(\.|x-).*")


def mime_score(mime_type: str, source: str | None) -> float:
    """Return how "official" a type is; the higher score wins a conflict."""
    if mime_type == "application/octet-stream":
        return 0
    top, subtype = mime_type.split("/", 1)
    facet = _FACET.sub(r"\1", subtype, count=1)
    facet_score = FACET_SCORES.get(facet, FACET_DEFAULT)
    source_score = SOURCE_SCORES.get(source or "", SOURCE_DEFAULT)
    type_score = TYPE_SCORES.get(top, TYPE_DEFAULT)
    length_score = 1 - len(mime_type) / 100
    return facet_score + source_score + type_score + length_score


def preferred(current: str | None, candidate: str, sources: dict[str, str | None]) -> str:
    """Pick between the type already holding an extension and a new claimant.

    Mirrors ``score0 > score1 ? type0 : type1``: a tie goes to the later type.
    """
    if current is None:
        return candidate
    if mime_score(current, sources[current]) > mime_score(candidate, sources[candidate]):
        return current
    return candidate
