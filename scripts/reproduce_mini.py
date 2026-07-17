#!/usr/bin/env python3
"""
One-command κ_C mini reproduction (synthetic sample).

  python scripts/reproduce_mini.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from kappa.metrics import REF_ONE_MINUS_1_E, THETA_C, compute_pipeline
from kappa.synthetic import load_sample, save_sample


def main() -> int:
    sample = ROOT / "data" / "sample" / "synthetic_coupled_orbit.npz"
    if not sample.is_file():
        print("Sample missing — generating synthetic_coupled_orbit (seed=42)...")
        save_sample(sample.with_suffix(""), seed=42)

    positions, dist = load_sample(sample)
    result = compute_pipeline(
        positions,
        dist,
        percentile=15.0,
        k=5,
        entropy_window=24,
        defect_window=9,
        n_boot=400,
        seed=0,
    )

    print("=" * 72)
    print("κ-Fractal Stability — mini reproduction (SYNTHETIC data)")
    print("Working hypothesis only — not a settled physical law.")
    print("=" * 72)
    print(f"n_points          : {len(positions)}")
    print(f"n_close (mask)    : {result['n_mask']}")
    print(f"n_pairs (boot)    : {int(result['n_close'])}")
    print(f"kappa_C (point)   : {result['kappa_C_point']:.4f}")
    print(f"kappa_C (boot μ)  : {result['kappa_C_boot_mean']:.4f}")
    print(
        f"kappa_C 95% CI    : [{result['kappa_C_ci_lo']:.4f}, {result['kappa_C_ci_hi']:.4f}]"
    )
    print(f"kappa_eff         : {result['kappa_eff']:.4f}")
    print(f"theta_C           : {THETA_C}")
    print(f"ref 1-1/e         : {REF_ONE_MINUS_1_E:.6f}")
    print(f"primary_pass      : {result['primary_pass']}")
    print(f"alternate_pass    : {result['alternate_pass']}")
    print("-" * 72)
    print("Expected (seed=42, defaults): kappa_C boot mean roughly > 0.3, often primary_pass.")
    print("If numbers drift slightly across OS/BLAS, compare band not exact float.")
    print("=" * 72)

    out = ROOT / "data" / "sample" / "last_repro_result.json"
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Wrote {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
