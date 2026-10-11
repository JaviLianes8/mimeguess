"""Lookups between file extensions and MIME types."""

from __future__ import annotations

from ._table import EXTENSION_TO_TYPE, TYPE_TO_EXTENSION


def _extension(path: str) -> str | None:
    """Return the final extension of a path, lowercase and without the dot."""
    name = path.replace("\\", "/").rsplit("/", 1)[-1]
    dot = name.rfind(".")
    if dot <= 0:  # no dot, or a leading-dot dotfile such as ".bashrc"
        return None
    return name[dot + 1 :].lower() or None


def guess_type(path: str) -> str | None:
    """Return the MIME type for a path from its extension, or None if unknown.

    The lookup uses only the final extension, so "photo.tar.gz" is read as a
    gzip file. It never touches the host registry, so the result is the same on
    every operating system.
    """
    ext = _extension(path)
    if ext is None:
        return None
    return EXTENSION_TO_TYPE.get(ext)


def guess_extension(mime: str) -> str | None:
    """Return the preferred extension (with a leading dot) for a MIME type.

    Any parameters such as "; charset=utf-8" are ignored. Returns None when the
    type is not in the table.
    """
    key = mime.split(";", 1)[0].strip().lower()
    ext = TYPE_TO_EXTENSION.get(key)
    return None if ext is None else "." + ext
