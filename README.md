# Veritaxa Workbench v0.7

Veritaxa is a **CHSA (Composable Hybrid Search Architecture) reference runtime** with a spreadsheet governance plane, evidence ledger, source adapters, academic discovery, and a governed literature-review pipeline.

## v0.7 boundary

```text
Academic discovery
  → authorized full text / excerpt
  → stable Evidence Spans
  → unverified candidate Claims
  → supports / contradicts / qualifies
  → MRASG-lite graph
  → WAITING_REVIEW
```

Abstracts, citation counts, platform rankings, and model-generated sentences are not treated as proof. Machine-extracted claims remain `unverified` until governed review.

## Reproducible release

The repository stores the complete runnable text source, the v0.7 XLSX workbench, and the SQLite literature-review demo database as verified release parts. Materialize them with:

```bash
python release/v0.7/materialize.py --output-dir build --extract
cd build/source
python -m pip install -e .
python -m pytest -q
```

Expected result: `27 passed`.

The materializer verifies SHA-256 before extracting or decompressing each artifact and rejects unsafe archive paths.

## v0.7 capabilities

- stable Evidence Span offsets, line ranges, and SHA-256 fingerprints;
- deterministic candidate-claim extraction;
- `supports`, `contradicts`, and `qualifies` relations;
- MRASG-lite graph compilation;
- CLI and MCP `literature_review` entry points;
- spreadsheet review control sheet `23_文獻審核`;
- fixtures, Markdown/JSON demo outputs, SQLite Evidence IR, migration notes, and tests.

The included fixture demo produces 2 documents, 3 Evidence Spans, 7 candidate claims, 15 MRASG-lite nodes, and 14 edges. Its final state is `WAITING_REVIEW`.

## Architecture

```text
Search Method
× Domain Search Profile
× Task Search Policy
× Source Adapter
× Protocol Mode
```

```text
AI-native search / Cognitive Localization
└─ CHSA public architecture
   └─ Veritaxa reference runtime
      ├─ Spreadsheet Governance Plane
      ├─ Source Adapters
      ├─ Evidence Ledger / Evidence IR
      ├─ Academic Discovery
      ├─ Literature Review / MRASG-lite
      ├─ Optional MCP Gateway
      └─ EveTessera Application Profile
```

## License

MIT. Source-specific access rules, robots policies, copyrights, database terms, and publication permissions still apply to acquired material.
