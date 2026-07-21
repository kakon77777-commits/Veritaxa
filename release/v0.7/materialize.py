from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import io
import tarfile
from pathlib import Path

ARTIFACTS = {
    "source": {
        "parts": "source_parts",
        "filename": "veritaxa_v0_7_text_source.tar.gz",
        "sha256": "8f124f540fe28701fcec53fe505f8b055e13b6ad48af2e0f3784115adc95b03a",
    },
    "workbook": {
        "parts": "workbook_parts",
        "filename": "Veritaxa_Workbench_v0.7.xlsx.gz",
        "sha256": "cc6fd021898dfc0af2458215ffbec247458b6bbb34235e316694f0db353497d5",
    },
    "demo-db": {
        "parts": "db_parts",
        "filename": "Veritaxa_v0.7_Literature_Demo.db.gz",
        "sha256": "6638331360a8b9f75d9c564f73c7efe7ad5cf50ac9bead95f68b5b32a0e980e8",
    },
}


def decode_parts(release_dir: Path, spec: dict[str, str]) -> bytes:
    paths = sorted((release_dir / spec["parts"]).glob("part-*.b64"))
    if not paths:
        raise RuntimeError(f"No parts found in {spec['parts']}")
    encoded = "".join(path.read_text(encoding="ascii").strip() for path in paths)
    payload = base64.b64decode(encoded, validate=True)
    actual = hashlib.sha256(payload).hexdigest()
    if actual != spec["sha256"]:
        raise RuntimeError(f"SHA-256 mismatch for {spec['filename']}: {actual}")
    return payload


def safe_extract_tar(payload: bytes, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    root = destination.resolve()
    with tarfile.open(fileobj=io.BytesIO(payload), mode="r:gz") as archive:
        for member in archive.getmembers():
            target = (destination / member.name).resolve()
            if target != root and root not in target.parents:
                raise RuntimeError(f"Unsafe archive path: {member.name}")
        archive.extractall(destination, filter="data")


def main() -> int:
    parser = argparse.ArgumentParser(description="Materialize the reproducible Veritaxa v0.7 GitHub release.")
    parser.add_argument("--output-dir", default="build")
    parser.add_argument("--extract", action="store_true")
    args = parser.parse_args()

    release_dir = Path(__file__).resolve().parent
    output = Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)

    source = decode_parts(release_dir, ARTIFACTS["source"])
    source_path = output / ARTIFACTS["source"]["filename"]
    source_path.write_bytes(source)
    print(f"verified {source_path}")
    if args.extract:
        safe_extract_tar(source, output / "source")

    workbook_gz = decode_parts(release_dir, ARTIFACTS["workbook"])
    workbook = gzip.decompress(workbook_gz)
    workbook_path = output / "Veritaxa_Workbench_v0.7.xlsx"
    workbook_path.write_bytes(workbook)
    if args.extract:
        (output / "source" / "veritaxa_workbench.xlsx").write_bytes(workbook)
    print(f"materialized {workbook_path}")

    db_gz = decode_parts(release_dir, ARTIFACTS["demo-db"])
    database = gzip.decompress(db_gz)
    database_path = output / "Veritaxa_v0.7_Literature_Demo.db"
    database_path.write_bytes(database)
    print(f"materialized {database_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
