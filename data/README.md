# Source snapshots

The files in this folder are gzip copies of upstream data, byte for byte as
fetched on 2026-10-12. Decompress them to get the original bytes; the SHA-256
values below are of the decompressed (original) content.

## mime-db-1.54.0.json.gz

- What: `db.json` from jshttp mime-db 1.54.0 (published 2025-03-18). It merges
  the IANA Media Types registry, Apache httpd `mime.types` and nginx
  `mime.types`, recording for each type which of them it came from.
- URL: https://raw.githubusercontent.com/jshttp/mime-db/v1.54.0/db.json
- SHA-256: `96b8a5746867c832ab56743c05e46e73c9facb04879677df0b356f20496cb6cd`
  (identical to `db.json` inside https://registry.npmjs.org/mime-db/-/mime-db-1.54.0.tgz)
- License: MIT, Copyright (c) 2014 Jonathan Ong, (c) 2015-2022 Douglas
  Christopher Wilson. Full text in `LICENSES/mime-db.txt`.
- Used by: `scripts/generate_table.py`, which builds `src/mimeguess/_data.json.gz`
  and `src/mimeguess/_meta.py` from it.

## apache-httpd-mime.types-r1930012.gz

- What: `docs/conf/mime.types` from the Apache httpd trunk, SVN revision
  1930012 (Last-Modified: Wed, 26 Nov 2025 11:30:42 GMT).
- URL: https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types
- SHA-256: `f0aca42aa6ae1ea0c856e363d45a6abd67b3afe1bd59e64f256c5610fc84505b`
- License: the file states it "has been placed in the public domain for
  unlimited redistribution"; Apache httpd as a whole is Apache License 2.0.
- Used by: `tests/test_crosscheck.py` only, as an independent check. It is not
  part of the generated table or the wheel.

## Updating

1. Fetch the new release from the URLs above (change the version or revision).
2. Store it gzipped here under a new versioned name and update the paths and
   constants at the top of `scripts/generate_table.py`.
3. Run `python scripts/generate_table.py`, then the test suite. Review the diff
   of `tests/golden/` and the pinned counts in the tests; regenerate the golden
   conflict file from the matching mime-types release as described in
   `tests/golden/PROVENANCE.txt`.
