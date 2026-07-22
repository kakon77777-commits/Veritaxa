# Veritaxa Workbench v1.0

Veritaxa v1.0 is the first stable **CHSA (Composable Hybrid Search Architecture) reference runtime** for governed academic discovery, evidence compilation, Claim Review, argument graphs, research lifecycle maintenance, and portable audit bundles.

## Stable research loop

```text
Search / authorized source input
  → normalized Evidence IR
  → stable Evidence Span
  → candidate Claim
  → governed Claim Review
  → MRASG-1.0
  → evidence invalidation and dependency propagation
  → conflict reopening / human closure
  → conclusion recompilation
  → WAITING_REVIEW
  → deterministic Research Bundle 1.0
```

The system preserves four boundaries:

```text
Extraction ≠ Evidence
Evidence ≠ Verified Claim
Approved Claim ≠ Universal Truth
Recompilation ≠ Automatic Republication
```

## Reproducible v1.0 release

The repository stores the complete runnable text source, the v1.0 XLSX governance workbench, a deterministic Research Bundle, its manifest, and a SQLite demo database as verified Base64 release parts.

```bash
python release/v1.0/materialize.py --output-dir build --extract --clean
cd build/source/veritaxa_workbench_v1_0
python -m pip install -e . --no-build-isolation
python -m pytest -q
```

Expected result: `41 passed`.

One-command verification:

```bash
python release/v1.0/verify_release.py
```

The materializer verifies contiguous part names, strict Base64, compressed payload SHA-256, decompressed artifact SHA-256, safe archive paths, and the expected source root. The verifier also runs the complete test suite and validates the demo Research Bundle.

## Stable v1.0 interfaces

### Python

```python
from veritaxa import VeritaxaResearchRuntime

runtime = VeritaxaResearchRuntime("data/research.db")
result = runtime.literature_review(
    "Research question",
    ["authorized_documents.json"],
    output_dir="exports/literature",
)

runtime.invalidate_evidence(
    result["run_id"],
    "span_...",
    "superseded",
    actor="source_monitor",
    rationale="A newer version replaced the cited span.",
)

runtime.recompile(result["run_id"], output_dir="exports/lifecycle")
bundle = runtime.build_bundle(result["run_id"], output_dir="exports/bundles")
assert runtime.validate_bundle(bundle["bundle_path"])["valid"]
```

### CLI

```bash
veritaxa --db data/research.db literature-review \
  --query "Research question" \
  --input authorized_documents.json \
  --output-dir exports/literature

veritaxa --db data/research.db evidence-invalidate \
  --run-id <run_id> \
  --source-ref <span_or_claim_id> \
  --change-type retracted \
  --actor source_monitor \
  --rationale "The source was formally retracted."

veritaxa --db data/research.db research-recompile \
  --run-id <run_id> \
  --output-dir exports/lifecycle

veritaxa --db data/research.db research-bundle \
  --run-id <run_id> \
  --output-dir exports/bundles

veritaxa --db data/research.db validate-bundle \
  --path exports/bundles/Veritaxa_<run_id>_Research_Bundle_v1.0.zip
```

## Stable schemas

- `Veritaxa-Research-Compilation-1.0`
- `Veritaxa-Lifecycle-1.0`
- `MRASG-1.0`
- `Veritaxa-Research-Bundle-1.0`
- `Veritaxa-Manifest-1.0`
- CHSA MCP Profile `1.0`

Minor v1.x releases may add optional fields, tools, tables, and resources. They must not silently change the meaning of existing v1.0 fields or permit machine-generated truth upgrades.

## Architecture

```text
AI-native search / Cognitive Localization
└─ CHSA public architecture
   └─ Veritaxa v1.0 stable runtime
      ├─ Spreadsheet Governance Plane
      ├─ Source Adapters
      ├─ Evidence Ledger / Evidence IR
      ├─ Academic Discovery
      ├─ Literature Review
      ├─ Claim Review
      ├─ MRASG-1.0
      ├─ Research Lifecycle Engine
      ├─ Deterministic Research Bundle
      ├─ Optional MCP Gateway
      └─ EveTessera Application Profile
```

## License

MIT. Source-specific access rules, robots policies, copyrights, database terms, and publication permissions still apply.
