"""Deterministic, OS-independent extension and MIME type mapping from a vendored table.

The table is generated from a committed snapshot of jshttp mime-db (MIT), which
merges the IANA registry, Apache httpd and nginx data. Results never depend on
the host operating system. See :func:`data_source` for provenance.
"""

from __future__ import annotations

from ._guess import (
    content_type_for,
    default_charset,
    extensions_for,
    guess,
    guess_extension,
    guess_type,
    is_compressible,
    is_textual,
    known_extensions,
    known_types,
    media_type_info,
    type_for_extension,
)
from ._load import data_source, default_table
from ._mediatype import essence, structured_suffix
from ._models import Guess, InvalidMediaType, MediaTypeInfo, Source, SourceInfo
from ._sniff import sniff
from ._table import MimeTable

__version__ = "0.2.1"

__all__ = [
    "Guess",
    "InvalidMediaType",
    "MediaTypeInfo",
    "MimeTable",
    "Source",
    "SourceInfo",
    "content_type_for",
    "data_source",
    "default_charset",
    "default_table",
    "essence",
    "extensions_for",
    "guess",
    "guess_extension",
    "guess_type",
    "is_compressible",
    "is_textual",
    "known_extensions",
    "known_types",
    "media_type_info",
    "sniff",
    "structured_suffix",
    "type_for_extension",
]
