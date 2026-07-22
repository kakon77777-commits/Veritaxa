# Changelog

## 1.0.0 — Stable Governed Research Runtime

- Declared stable v1.0 compilation, lifecycle, MRASG, bundle, manifest and MCP schemas.
- Added `VeritaxaResearchRuntime` as the supported programmatic façade.
- Added deterministic Research Bundle 1.0 generation.
- Added complete file-level SHA-256 manifests and bundle validation.
- Added tamper detection and deterministic ZIP metadata.
- Added CLI and MCP capabilities for building and validating research bundles.
- Preserved v0.9 invalidation propagation, conflict reopening and review-gated recompilation.
- Added stable compatibility and governance contracts.
- Expanded the test suite to 41 passing tests.

## 0.9.0 — Research Lifecycle and Recompilation

- Added dependency edges from documents to spans, spans to claims, claims to claims, and claims to conclusions.
- Added immutable evidence invalidation records and impact propagation events.
- Added `evidence_invalidated` Claim Review state and governed recovery path.
- Added conflict cases with `OPEN_CONFLICT`, `QUALIFIED_CONSENSUS`, `RESOLVED_CONFLICT`, and `IRREDUCIBLE_DISAGREEMENT`.
- Reopen closed conflicts when dependent claims lose valid evidence.
- Added deterministic review-aware conclusions and `CONCLUSION_AFFECTED` state.
- Added versioned research recompilation that always returns changed research to `WAITING_REVIEW`.
- Added lifecycle CLI and MCP façade capabilities.
- Upgraded the argument graph to MRASG-0.9.
- Expanded the test suite to 37 passing tests.

## 0.8.0 — Governed Full-text and Claim Verification

- Added fail-closed full-text acquisition decisions.
- Added Claim Review state machine and immutable review events.
- Added governed Claim-to-Claim relations and MRASG-0.8.
- Added full-text planning and Claim Review CLI/MCP capabilities.
- Expanded the test suite to 32 passing tests.

## 0.7.0 — Evidence Span and MRASG-lite MVP

- Added deterministic document loading and stable Evidence Span segmentation.
- Added character offsets, line ranges, headings, document versions and SHA-256 span identities.
- Added conservative multilingual candidate-claim extraction.
- Kept all machine-extracted claims explicitly `unverified`.
- Added provisional supports/contradicts/qualifies relations.
- Added MRASG-lite graph compilation and Markdown/JSON review outputs.
- Added `literature-review` CLI command and `literature_review` MCP tool.
- Added fixture documents and three new regression tests.
- Expanded the test suite to 27 passing tests.

## 0.6.0 — Academic Search MVP

- Added `academic_discovery` task policy.
- Added Crossref REST and arXiv Atom academic adapters with injectable transports.
- Added deterministic offline fixture adapter for CI and air-gapped demonstrations.
- Added DOI/arXiv/title normalization and cross-source deduplication.
- Added metadata-level Evidence IR compilation and review boundary.
- Added `academic-search` CLI command.
- Added `academic_search` to the CHSA MCP profile.
- Added academic demo workbook and AI-native OS candidate compilation.
- Expanded test suite to 24 passing tests.

## 0.5.0 — CHSA Reference Runtime

- Repositioned Veritaxa as the first CHSA reference runtime.
- Separated EveTessera-specific ranking and publishing from the generic runtime.
- Added domain profiles, task policies, search methods, Evidence IR extensions, MCP façade, and batched XLSX updates.
