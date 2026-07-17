# Mini reproduction

**Hypothesis only.** Synthetic demo — not celestial ephemeris.

## One command

```bash
# from repo root
python -m pip install -r requirements.txt
python scripts/reproduce_mini.py
```

If `data/sample/synthetic_coupled_orbit.npz` is missing, the script generates it (seed=42).

Regenerate sample explicitly:

```bash
python scripts/generate_sample_data.py
```

## What it prints

| Field | Meaning |
|-------|---------|
| `kappa_C (boot μ)` | Bootstrap mean of defect ↔ entropy-rate correlation on close approach |
| `kappa_C 95% CI` | Percentile CI |
| `kappa_eff` | \(\exp(-\kappa_C)\) |
| `primary_pass` | mean \(> 0.35\) and CI lower \(> 0\) |
| `alternate_pass` | \(\kappa_{\mathrm{eff}}\) within 15% of \(1-1/e\) |

## Expected band (seed=42, defaults)

On a normal NumPy install you should see roughly:

- `kappa_C` boot mean **~0.65–0.80** (example run: **0.71**, CI ~[0.61, 0.80])
- `primary_pass: True`
- `alternate_pass` may be False (κ_eff not forced near \(1-1/e\) on synthetic)

Do **not** expect bit-identical floats across OS/BLAS; use the band.

Mini package uses **path irregularity** × **entropy level** on close approach.
Full research writeups also discuss Frenet residual × entropy **rate**; toggle with
`use_entropy_rate=True` in `compute_pipeline` if you experiment.

## Data origin

`data/sample/synthetic_coupled_orbit.*` is **synthetic**: a spiral that approaches the
z-axis (separatrix proxy) with curvature stress correlated to local dispersion so the
pipeline has a known positive coupling. It is **not** JPL / Horizons data.

Real multi-system results remain documented in `README.md` (family-specific battery).

## No private paths

This package does not read JoeysAI or absolute user directories.
