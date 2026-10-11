# mimeguess

Deterministic, OS-independent file extension and MIME type mapping from a vendored table, zero dependencies

## Install

```
pip install mimeguess
```

## Usage

```python
import mimeguess

mimeguess.guess_type("report.pdf")        # "application/pdf"
mimeguess.guess_type("PHOTO.JPG")         # "image/jpeg"
mimeguess.guess_type("backup.tar.gz")     # "application/gzip"
mimeguess.guess_type("Makefile")          # None

mimeguess.guess_extension("image/png")            # ".png"
mimeguess.guess_extension("text/html; charset=utf-8")  # ".html"
mimeguess.guess_extension("application/x-nope")   # None
```

Lookups are case insensitive, use only the final extension, and ignore any
parameters on a MIME type. An unknown input returns `None`.

## Why

The standard library `mimetypes` reads the host registry, so the same call can
return different answers on different machines and often returns `None` when the
system table is thin. Content sniffers such as `python-magic` need the native
`libmagic` library, and `filetype` or `puremagic` inspect bytes rather than map
names. `mimeguess` ships a fixed table inside the package: the result depends
only on the extension, never on the operating system, and there is nothing to
install beyond the wheel. Reach for it when you need a stable, portable name to
MIME mapping with zero dependencies.

## License

MIT. See [LICENSE](LICENSE).

## Links

- Website: https://lianes8studio.com
- GitHub: https://github.com/JaviLianes8
- LinkedIn: https://www.linkedin.com/in/jlianes/
