from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import json
import shutil
import tarfile
from pathlib import Path


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def decode_parts(release_dir: Path, spec: dict) -> bytes:
    part_dir = release_dir / spec["parts"]
    paths = sorted(part_dir.glob("part-*.b64"))
    expected = int(spec["part_count"])
    if len(paths) != expected:
        raise RuntimeError(
            f"{spec['parts']}: expected {expected} parts, found {len(paths)}"
        )
    expected_names = [f"part-{index:03d}.b64" for index in range(expected)]
    actual_names = [path.name for path in paths]
    if actual_names != expected_names:
        raise RuntimeError(
            f"{spec['parts']}: non-contiguous parts: {actual_names}"
        )
    encoded = "".join(path.read_text(encoding="ascii").strip() for path in paths)
    payload = base64.b64decode(encoded, validate=True)
    actual = sha256(payload)
    if actual != spec["payload_sha256"]:
        raise RuntimeError(
            f"{spec['stored_filename']}: payload SHA-256 mismatch: {actual}"
        )
    return payload


def safe_extract_tar(archive_path: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    root = destination.resolve()
    with tarfile.open(archive_path, mode="r:gz") as archive:
        for member in archive.getmembers():
            target = (destination / member.name).resolve()
            if target != root and root not in target.parents:
                raise RuntimeError(f"Unsafe TAR path: {member.name}")
            if member.issym() or member.islnk() or member.isdev():
                raise RuntimeError(f"Unsafe TAR member: {member.name}")
        archive.extractall(destination, filter="data")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Materialize the reproducible Veritaxa v1.0 GitHub release."
    )
    parser.add_argument("--output-dir", default="build")
    parser.add_argument("--extract", action="store_true")
    parser.add_argument("--clean", action="store_true")
    args = parser.parse_args()

    release_dir = Path(__file__).resolve().parent
    manifest = json.loads((release_dir / "manifest.json").read_text(encoding="utf-8"))
    output = Path(args.output_dir)
    if args.clean and output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True, exist_ok=True)

    materialized: dict[str, Path] = {}
    for key, spec in manifest["artifacts"].items():
        payload = decode_parts(release_dir, spec)
        raw = gzip.decompress(payload) if spec["compression"] == "gzip" else payload
        actual = sha256(raw)
        if actual != spec["output_sha256"]:
            raise RuntimeError(
                f"{spec['output_filename']}: output SHA-256 mismatch: {actual}"
            )
        path = output / spec["output_filename"]
        path.write_bytes(raw)
        materialized[key] = path
        print(f"verified {path} ({actual})")

    if args.extract:
        source_root = output / "source"
        safe_extract_tar(materialized["source"], source_root)
        project = source_root / "veritaxa_workbench_v1_0"
        if not project.is_dir():
            raise RuntimeError("Expected source root veritaxa_workbench_v1_0 was not found.")
        shutil.copy2(materialized["workbook"], project / "veritaxa_workbench.xlsx")
        example_dir = project / "examples" / "v1_bundle"
        example_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(materialized["bundle"], example_dir / materialized["bundle"].name)
        shutil.copy2(
            materialized["bundle_manifest"],
            example_dir / materialized["bundle_manifest"].name,
        )
        shutil.copy2(materialized["demo_db"], example_dir / materialized["demo_db"].name)
        print(f"extracted {project}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
