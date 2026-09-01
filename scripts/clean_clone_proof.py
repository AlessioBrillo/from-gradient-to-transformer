#!/usr/bin/env python3
"""
Clean-Clone Reproducibility Proof (ADR-0024 Row 4)

Fresh clone → `uv sync` → `make reproduce-quick` → `make verify-claims`
Full transcript with timestamps.
"""

import argparse
import subprocess
import sys
import tempfile
import time
from pathlib import Path


def run_cmd(cmd: list[str], cwd: Path, log_file) -> tuple[int, str, str]:
    """Run command and log output."""
    print(f"  $ {' '.join(cmd)}", file=log_file)
    log_file.flush()
    start = time.time()
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=3600)
    elapsed = time.time() - start
    print(f"  [exit {result.returncode}, {elapsed:.1f}s]", file=log_file)
    if result.stdout:
        print(result.stdout, file=log_file)
    if result.stderr:
        print(result.stderr, file=log_file)
    log_file.flush()
    return result.returncode, result.stdout, result.stderr


def main():
    parser = argparse.ArgumentParser(description="Clean-Clone Reproducibility Proof")
    parser.add_argument("--repo-url", default="https://github.com/AlessioBrillo/from-gradient-to-transformer.git",
                        help="Repository URL to clone")
    parser.add_argument("--branch", default="dev", help="Branch to clone")
    parser.add_argument("--output", type=Path, default=Path("06_production_ai/proofs/reproducible-from-clean-clone.md"),
                        help="Output transcript file")
    args = parser.parse_args()

    output_path = args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as log_file:
        print(f"# Clean-Clone Reproducibility Proof Transcript", file=log_file)
        print(f"**Date**: {time.strftime('%Y-%m-%d %H:%M:%S')}", file=log_file)
        print(f"**Repo**: {args.repo_url} (branch: {args.branch})", file=log_file)
        print(f"**Host**: {__import__('platform').node()}", file=log_file)
        print(f"**Python**: {sys.version}", file=log_file)
        print("", file=log_file)

        with tempfile.TemporaryDirectory() as tmpdir:
            clone_dir = Path(tmpdir) / "test-clone"
            print(f"## Working directory: {tmpdir}", file=log_file)
            print("", file=log_file)

            # 1. Fresh clone
            print("## Step 1: Fresh Clone", file=log_file)
            print("```bash", file=log_file)
            rc, out, err = run_cmd(
                ["git", "clone", "--branch", args.branch, "--depth", "1", args.repo_url, str(clone_dir)],
                Path(tmpdir), log_file
            )
            print("```", file=log_file)
            if rc != 0:
                print("[FAILED]: Clone failed", file=log_file)
                return 1
            print("[OK] Clone successful", file=log_file)
            print("", file=log_file)

            # 2. uv sync
            print("## Step 2: uv sync", file=log_file)
            print("```bash", file=log_file)
            rc, out, err = run_cmd(["uv", "sync"], clone_dir, log_file)
            print("```", file=log_file)
            if rc != 0:
                print("[FAILED]: uv sync failed", file=log_file)
                return 1
            print("[OK] uv sync successful", file=log_file)
            print("", file=log_file)

            # 3. make reproduce-quick
            print("## Step 3: make reproduce-quick", file=log_file)
            print("```bash", file=log_file)
            rc, out, err = run_cmd(["make", "reproduce-quick"], clone_dir, log_file)
            print("```", file=log_file)
            if rc != 0:
                print("[FAILED]: make reproduce-quick failed", file=log_file)
                return 1
            print("[OK] make reproduce-quick successful", file=log_file)
            print("", file=log_file)

            # 4. make verify-claims
            print("## Step 4: make verify-claims", file=log_file)
            print("```bash", file=log_file)
            rc, out, err = run_cmd(["make", "verify-claims"], clone_dir, log_file)
            print("```", file=log_file)
            if rc != 0:
                print("[FAILED]: make verify-claims failed", file=log_file)
                return 1
            print("[OK] make verify-claims successful", file=log_file)
            print("", file=log_file)

            print("## Summary", file=log_file)
            print("[OK] ALL STEPS PASSED -- Clean-clone reproducibility proven", file=log_file)
            print(f"**Completed**: {time.strftime('%Y-%m-%d %H:%M:%S')}", file=log_file)

    print(f"Transcript written to {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())