from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import io
import json
import tarfile
from pathlib import Path

RELEASE_DIR = Path(__file__).resolve().parent
ARTIFACTS = json.loads((RELEASE_DIR / "manifest.json").read_text(encoding="utf-8"))


def decode_parts(spec: dict[str, object]) -> bytes:
    paths = sorted((RELEASE_DIR / str(spec["parts"])).glob("part-*.b64"))
    if len(paths) != int(spec["part_count"]):
        raise RuntimeError(f"Part count mismatch for {spec['filename']}: {len(paths)}")
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
    parser = argparse.ArgumentParser(description="Materialize the reproducible Veritaxa v0.8 release.")
    parser.add_argument("--output-dir", default="build-v0.8")
    parser.add_argument("--extract", action="store_true")
    args = parser.parse_args()
    output = Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)

    source = decode_parts(ARTIFACTS["source"])
    source_path = output / str(ARTIFACTS["source"]["filename"])
    source_path.write_bytes(source)
    print(f"verified {source_path}")
    if args.extract:
        safe_extract_tar(source, output / "source")

    workbook = gzip.decompress(decode_parts(ARTIFACTS["workbook"]))
    workbook_path = output / "Veritaxa_Workbench_v0.8.xlsx"
    workbook_path.write_bytes(workbook)
    if args.extract:
        (output / "source" / "veritaxa_workbench.xlsx").write_bytes(workbook)
    print(f"materialized {workbook_path}")

    database = gzip.decompress(decode_parts(ARTIFACTS["demo-db"]))
    database_path = output / "Veritaxa_v0.8_Literature_Demo.db"
    database_path.write_bytes(database)
    print(f"materialized {database_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
