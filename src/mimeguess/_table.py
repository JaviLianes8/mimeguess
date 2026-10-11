"""Vendored extension to MIME type table, shipped with the package."""

from __future__ import annotations

# Each row is a MIME type and its extensions, the first being the preferred one
# for reverse lookups. Extensions are stored without a leading dot, lowercase.
_TYPES: tuple[tuple[str, tuple[str, ...]], ...] = (
    # Text
    ("text/plain", ("txt", "text", "log", "ini", "conf", "cfg")),
    ("text/markdown", ("md", "markdown")),
    ("text/csv", ("csv",)),
    ("text/tab-separated-values", ("tsv",)),
    ("text/calendar", ("ics",)),
    ("text/vcard", ("vcf",)),
    ("text/x-python", ("py",)),
    ("text/x-c", ("c", "h")),
    # Web
    ("text/html", ("html", "htm")),
    ("text/css", ("css",)),
    ("text/javascript", ("js", "mjs", "cjs")),
    ("application/json", ("json",)),
    ("application/xml", ("xml",)),
    ("application/xhtml+xml", ("xhtml",)),
    ("application/manifest+json", ("webmanifest",)),
    ("application/rss+xml", ("rss",)),
    ("application/atom+xml", ("atom",)),
    ("application/yaml", ("yaml", "yml")),
    ("application/toml", ("toml",)),
    ("application/wasm", ("wasm",)),
    # Images
    ("image/jpeg", ("jpg", "jpeg", "jpe")),
    ("image/png", ("png",)),
    ("image/gif", ("gif",)),
    ("image/webp", ("webp",)),
    ("image/avif", ("avif",)),
    ("image/svg+xml", ("svg",)),
    ("image/bmp", ("bmp",)),
    ("image/tiff", ("tiff", "tif")),
    ("image/x-icon", ("ico",)),
    ("image/heic", ("heic",)),
    ("image/heif", ("heif",)),
    ("image/vnd.adobe.photoshop", ("psd",)),
    # Audio
    ("audio/mpeg", ("mp3",)),
    ("audio/ogg", ("ogg", "oga")),
    ("audio/wav", ("wav",)),
    ("audio/flac", ("flac",)),
    ("audio/aac", ("aac",)),
    ("audio/mp4", ("m4a",)),
    ("audio/opus", ("opus",)),
    ("audio/webm", ("weba",)),
    ("audio/midi", ("mid", "midi")),
    # Video
    ("video/mp4", ("mp4", "m4v")),
    ("video/webm", ("webm",)),
    ("video/ogg", ("ogv",)),
    ("video/quicktime", ("mov",)),
    ("video/x-msvideo", ("avi",)),
    ("video/x-matroska", ("mkv",)),
    ("video/mpeg", ("mpeg", "mpg")),
    ("video/3gpp", ("3gp",)),
    # Archives
    ("application/zip", ("zip",)),
    ("application/gzip", ("gz",)),
    ("application/x-tar", ("tar",)),
    ("application/x-bzip2", ("bz2",)),
    ("application/x-xz", ("xz",)),
    ("application/zstd", ("zst",)),
    ("application/x-7z-compressed", ("7z",)),
    ("application/vnd.rar", ("rar",)),
    ("application/java-archive", ("jar",)),
    # Documents and office
    ("application/pdf", ("pdf",)),
    ("application/msword", ("doc",)),
    (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ("docx",),
    ),
    ("application/vnd.ms-excel", ("xls",)),
    (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ("xlsx",),
    ),
    ("application/vnd.ms-powerpoint", ("ppt",)),
    (
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        ("pptx",),
    ),
    ("application/vnd.oasis.opendocument.text", ("odt",)),
    ("application/vnd.oasis.opendocument.spreadsheet", ("ods",)),
    ("application/vnd.oasis.opendocument.presentation", ("odp",)),
    ("application/rtf", ("rtf",)),
    ("application/epub+zip", ("epub",)),
    # Fonts
    ("font/woff", ("woff",)),
    ("font/woff2", ("woff2",)),
    ("font/ttf", ("ttf",)),
    ("font/otf", ("otf",)),
    ("application/vnd.ms-fontobject", ("eot",)),
    # Data, code and other binaries
    ("application/octet-stream", ("bin",)),
    ("application/x-sh", ("sh",)),
    ("application/sql", ("sql",)),
    ("application/x-sqlite3", ("sqlite", "db")),
    ("application/vnd.android.package-archive", ("apk",)),
    ("application/x-msdownload", ("exe", "dll")),
    ("application/x-apple-diskimage", ("dmg",)),
    ("application/x-iso9660-image", ("iso",)),
)

EXTENSION_TO_TYPE: dict[str, str] = {ext: mime for mime, exts in _TYPES for ext in exts}

TYPE_TO_EXTENSION: dict[str, str] = {mime: exts[0] for mime, exts in _TYPES}
