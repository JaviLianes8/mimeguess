"""The MimeTable: an immutable extension and MIME type lookup table."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from types import MappingProxyType
from typing import NamedTuple

from ._mediatype import lenient_essence, real_charset, structured_suffix, textual
from ._models import Guess, MediaTypeInfo, Source
from ._paths import candidates, normalize_extension, segments, split_encoding


class Entry(NamedTuple):
    """Internal row: one MIME type and what the table knows about it."""

    source: Source
    charset: str | None
    compressible: bool | None
    extensions: tuple[str, ...]  # lowercase, no leading dot, preferred first


class MimeTable:
    """An immutable mapping between file extensions and MIME types.

    The package-level functions use :func:`default_table`. Build a variant with
    :meth:`with_types` to add or override mappings without touching any global
    state. Lookups are case-insensitive and never consult the operating system.
    """

    __slots__ = ("_extensions", "_max_dots", "_types")

    def __init__(self, types: Mapping[str, Entry], extensions: Mapping[str, str]) -> None:
        self._types = MappingProxyType(dict(types))
        self._extensions = MappingProxyType(dict(extensions))
        self._max_dots = max((ext.count(".") for ext in self._extensions), default=0)

    def with_types(self, mapping: Mapping[str, Iterable[str]]) -> MimeTable:
        """Return a new table where the given extensions map to the given types.

        ``mapping`` maps a MIME type to its extensions, preferred first; leading
        dots are optional and compound extensions such as ``"d.ts"`` are allowed::

            table = default_table().with_types({"text/x-typescript": ["ts", "d.ts"]})

        Each listed extension now resolves to its new type. The new extensions
        are placed at the front of the type's list (so the first becomes its
        preferred extension), followed by any extensions it already had. Other
        types keep their own lists unchanged.

        Raises:
            ValueError: on a malformed MIME type or extension, or a type with no
                extensions.
        """
        types = dict(self._types)
        extensions = dict(self._extensions)
        for mime, exts in mapping.items():
            key = lenient_essence(mime)
            if key is None or key != mime.strip().lower():
                raise ValueError(f"not a bare type/subtype media type: {mime!r}")
            if isinstance(exts, str):
                raise ValueError(f"extensions for {mime!r} must be a list, not a string")
            new = list(dict.fromkeys(normalize_extension(ext) for ext in exts))
            if not new:
                raise ValueError(f"no extensions given for {mime!r}")
            old = types.get(key, Entry("custom", None, None, ()))
            merged = (*new, *(ext for ext in old.extensions if ext not in new))
            types[key] = old._replace(extensions=merged)
            for ext in new:
                extensions[ext] = key
        return MimeTable(types, extensions)

    def type_for_extension(self, ext: str) -> str | None:
        """Return the MIME type for an extension such as ``"pdf"`` or ``".tar.gz"``.

        The whole value is one extension; it is not split. Returns ``None`` when
        the extension is unknown or malformed.
        """
        try:
            key = normalize_extension(ext)
        except ValueError:
            return None
        return self._extensions.get(key)

    def _lookup(self, parts: list[str]) -> tuple[str, str] | tuple[None, None]:
        for ext in candidates(parts, self._max_dots):
            mime = self._extensions.get(ext)
            if mime is not None:
                return mime, ext
        return None, None

    def guess_type(self, path: str) -> str | None:
        """Return the MIME type of a path from its extension, or ``None``.

        The longest dotted suffix the table knows wins, so with the default
        table ``backup.tar.gz`` is ``application/gzip``. Use :meth:`guess` to
        separate the content coding instead.
        """
        return self._lookup(segments(path))[0]

    def guess(self, path: str) -> Guess:
        """Return the type, content coding and matched extension of a path.

        A trailing compression extension becomes the encoding, following the
        standard library rules: ``a.tar.gz`` is ``application/x-tar`` with
        encoding ``gzip``, ``a.tgz`` is the same, and a lone ``a.gz`` has encoding
        ``gzip`` and no type.
        """
        parts, encoding = split_encoding(segments(path))
        mime, ext = self._lookup(parts)
        return Guess(type=mime, encoding=encoding, extension=ext)

    def extensions_for(self, mime: str) -> tuple[str, ...]:
        """Return every extension of a type with a leading dot, preferred first.

        Parameters and case are ignored. Returns an empty tuple when the type is
        unknown, malformed, or has no extensions.
        """
        entry = self._entry(mime)
        return () if entry is None else tuple("." + ext for ext in entry.extensions)

    def guess_extension(self, mime: str) -> str | None:
        """Return the preferred extension of a type with a leading dot, or ``None``."""
        exts = self.extensions_for(mime)
        return exts[0] if exts else None

    def media_type_info(self, mime: str) -> MediaTypeInfo | None:
        """Return everything known about a type, or ``None`` when it is unknown."""
        key = lenient_essence(mime)
        entry = None if key is None else self._types.get(key)
        if key is None or entry is None:
            return None
        return MediaTypeInfo(
            type=key,
            source=entry.source,
            extensions=tuple("." + ext for ext in entry.extensions),
            charset=real_charset(entry.charset),
            compressible=entry.compressible,
            suffix=structured_suffix(key),
        )

    def default_charset(self, mime: str) -> str | None:
        """Return the default charset for a type, lowercase, or ``None``.

        The charset the source data declares wins (``application/json`` gives
        ``"utf-8"``); otherwise any ``text/*`` type gets ``"utf-8"``, the same
        policy as jshttp mime-types. Other types give ``None``.
        """
        key = lenient_essence(mime)
        if key is None:
            return None
        entry = self._types.get(key)
        declared = None if entry is None else real_charset(entry.charset)
        if declared is not None:
            return declared
        return "utf-8" if key.startswith("text/") else None

    def is_textual(self, mime: str) -> bool:
        """Return whether a type carries text: ``text/*``, a type with a declared
        charset, or a ``+json``, ``+xml``, ``+yaml`` or ``+json-seq`` suffix."""
        key = lenient_essence(mime)
        if key is None:
            return False
        entry = self._types.get(key)
        return textual(key, None if entry is None else real_charset(entry.charset))

    def is_compressible(self, mime: str) -> bool | None:
        """Return whether a type usually compresses well, ``None`` when unknown."""
        entry = self._entry(mime)
        return None if entry is None else entry.compressible

    def content_type_for(self, path: str) -> str | None:
        """Return a Content-Type value for a path, with a charset when one applies.

        ``index.html`` gives ``"text/html; charset=utf-8"`` and ``photo.png``
        gives ``"image/png"``. Returns ``None`` when the type is unknown.
        """
        mime = self.guess_type(path)
        if mime is None:
            return None
        charset = self.default_charset(mime)
        return mime if charset is None else f"{mime}; charset={charset}"

    def known_types(self) -> tuple[str, ...]:
        """Return every MIME type in the table, sorted."""
        return tuple(sorted(self._types))

    def known_extensions(self) -> tuple[str, ...]:
        """Return every extension the table resolves, with a leading dot, sorted."""
        return tuple(sorted("." + ext for ext in self._extensions))

    def _entry(self, mime: str) -> Entry | None:
        key = lenient_essence(mime)
        return None if key is None else self._types.get(key)
