# Veritaxa v0.8 reproducible release

```bash
python release/v0.8/materialize.py --output-dir build-v0.8 --extract
cd build-v0.8/source
python -m pip install -e .
python -m pytest -q
```

Expected: `32 passed`.

The materializer verifies SHA-256, validates part counts, rejects invalid base64, and performs path-safe tar extraction.
