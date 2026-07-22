from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from materialize import main as materialize_main


def run(command: list[str], cwd: Path) -> None:
    print("+", " ".join(command))
    subprocess.run(command, cwd=cwd, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Reconstruct and verify the Veritaxa v1.0 release."
    )
    parser.add_argument("--keep", action="store_true")
    args = parser.parse_args()

    release_dir = Path(__file__).resolve().parent
    with tempfile.TemporaryDirectory(prefix="veritaxa-v1-release-") as temp:
        root = Path(temp)
        old_argv = sys.argv
        try:
            sys.argv = [
                str(release_dir / "materialize.py"),
                "--output-dir",
                str(root / "build"),
                "--extract",
                "--clean",
            ]
            materialize_main()
        finally:
            sys.argv = old_argv

        project = root / "build" / "source" / "veritaxa_workbench_v1_0"
        run(
            [sys.executable, "-m", "pip", "install", "-e", ".", "--no-build-isolation"],
            project,
        )
        run([sys.executable, "-m", "pytest", "-q"], project)

        bundle = root / "build" / "Veritaxa_v1.0_Demo_Research_Bundle.zip"
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "veritaxa.cli",
                "--db",
                str(root / "build" / "Veritaxa_v1.0_Demo.db"),
                "validate-bundle",
                "--path",
                str(bundle),
            ],
            cwd=project,
            check=True,
            text=True,
            capture_output=True,
        )
        print(result.stdout)
        if '"valid": true' not in result.stdout.lower():
            raise RuntimeError("Demo Research Bundle did not validate.")

        manifest = json.loads((release_dir / "manifest.json").read_text(encoding="utf-8"))
        if manifest["expected_tests"] != 41:
            raise RuntimeError("Release manifest expected_tests is not 41.")

        if args.keep:
            destination = Path.cwd() / "verified-v1.0"
            if destination.exists():
                import shutil
                shutil.rmtree(destination)
            import shutil
            shutil.copytree(root / "build", destination)
            print(f"kept {destination}")

    print("Veritaxa v1.0 release verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
