# Veritaxa v1.0 Completion Report

## Stable runtime completed

- Stable `VeritaxaResearchRuntime` Python façade.
- Stable compilation, lifecycle, MRASG, bundle and manifest schemas.
- Deterministic Research Bundle 1.0.
- File-level SHA-256 manifest verification.
- Tamper detection.
- Stable CLI and CHSA MCP Profile 1.0 capabilities.
- v0.9 invalidation, conflict and recompilation semantics preserved.
- Stability contract and migration documentation.
- XLSX bundle and compatibility governance sheets.

## Stable schema identifiers

- `Veritaxa-Research-Compilation-1.0`
- `Veritaxa-Lifecycle-1.0`
- `MRASG-1.0`
- `Veritaxa-Research-Bundle-1.0`
- `Veritaxa-Manifest-1.0`

## Verification

```text
41 passed
```

Two bundles produced from unchanged research state have identical SHA-256 values. A deliberately modified `evidence.json` fails validation with a hash mismatch.
