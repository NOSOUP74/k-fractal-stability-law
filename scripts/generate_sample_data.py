#!/usr/bin/env python3
"""Regenerate synthetic sample under data/sample/."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from kappa.synthetic import save_sample


def main() -> int:
    out = ROOT / "data" / "sample" / "synthetic_coupled_orbit"
    path = save_sample(out, seed=42)
    print(f"Wrote {path}")
    print(f"Wrote {path.with_suffix('.csv')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
