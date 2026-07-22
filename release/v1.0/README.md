# Veritaxa v1.0 reproducible release

This directory reconstructs the complete Veritaxa v1.0 stable runtime and its governed release artifacts from contiguous Base64 parts.

## Artifacts

- complete runnable text source snapshot;
- v1.0 XLSX governance workbench;
- deterministic demo Research Bundle 1.0;
- bundle manifest;
- SQLite demo database.

## Reconstruct

```bash
python release/v1.0/materialize.py --output-dir build --extract --clean
cd build/source/veritaxa_workbench_v1_0
python -m pip install -e . --no-build-isolation
python -m pytest -q
```

Expected result: `41 passed`.

## One-command verification

```bash
python release/v1.0/verify_release.py
```

The materializer verifies contiguous part names, strict Base64, compressed payload hashes, decompressed output hashes, safe TAR paths, and the expected source root.
