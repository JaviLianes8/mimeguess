"""Hand-written adjustments applied on top of the mime-db snapshot.

Everything in this file is written by hand, not copied from an external source.
It is deliberately small and only ever adds; it never deletes a type or an
extension that mime-db lists.

EXTRA_EXTENSIONS attaches extensions to a type. It exists so that extensions the
0.1.0 table answered and mime-db does not list keep working. When an added
extension is already claimed by another type, the normal mime-types scoring in
``_score.py`` decides, exactly as for mime-db's own conflicts. Today that moves
exactly three extensions to the registered type: "flac" to audio/flac (from
audio/x-flac) and "yaml" and "yml" to application/yaml (from text/yaml). The
test suite pins that list. A type that mime-db does not know is created with
the source "supplement".

PREFERRED_EXTENSION moves an extension that mime-db already lists for a type to
the front of that type's list, so the preferred (reverse lookup) extension is
the everyday one, for example "mp3" rather than "mpga" for audio/mpeg.
"""

from __future__ import annotations

EXTRA_EXTENSIONS: dict[str, tuple[str, ...]] = {
    # mime-db 1.54.0 lists these registered types without any extension.
    "application/vnd.sqlite3": ("sqlite", "sqlite3", "db"),
    "application/yaml": ("yaml", "yml"),
    "application/zstd": ("zst",),
    "audio/flac": ("flac",),
    # Not in mime-db; the name the Python standard library uses.
    "text/x-python": ("py",),
    # mime-db already maps "ini" and "conf" to text/plain; "cfg" joins them.
    "text/plain": ("cfg",),
}

PREFERRED_EXTENSION: dict[str, str] = {
    "audio/aac": "aac",
    "audio/mpeg": "mp3",
    "audio/ogg": "ogg",
    "video/quicktime": "mov",
}
