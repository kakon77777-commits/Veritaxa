# Pull request verification notes

This branch upgrades Veritaxa from the v0.x governed literature-review runtime to the v1.0 stable research lifecycle runtime.

Verification gate:

```bash
python release/v1.0/verify_release.py
```

Expected result: `41 passed`.

The release materializer validates Base64 part count, payload SHA-256, output SHA-256, output size, and safe archive extraction before running the test suite.
