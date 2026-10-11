"""Deterministic, OS-independent extension and MIME type mapping from a vendored table."""

from __future__ import annotations

from ._guess import guess_extension, guess_type

__version__ = "0.1.0"

__all__ = ["guess_extension", "guess_type"]
