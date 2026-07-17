# κ-Fractal Stability — Work Queue

Ordered list. Work **top → bottom**. Mark status as we go.

**Scope:** physics / math / reproducibility only.  
**Stance:** working hypothesis, family-specific — not universal law.

---

## Status legend

| Tag | Meaning |
|-----|---------|
| `TODO` | Not started |
| `ACTIVE` | Current focus |
| `DONE` | Finished |
| `BLOCKED` | Waiting on data/decision |
| `SKIP` | Explicitly deferred |

---

## Queue

| # | Item | Status | Notes |
|---|------|--------|-------|
| **1** | **Repro mini-package** — public-runnable κ_C path + tiny sample (or synthetic) data | `ACTIVE` | Highest leverage; no private paths |
| **2** | **Sensitivity table (L1 only)** — vary \(p\), \(k\), windows; report \(\bar\kappa_C\), CI, \(n\) | `TODO` | After #1 can run |
| **3** | **Pre-register next tests** — freeze criteria for (a) one new family, (b) one null | `TODO` | Before looking at results |
| **4** | **Run pre-registered battery** — record pass/fail only against frozen rules | `TODO` | Data outranks theory |
| **5** | **Coordinate-free defect trial** — 1–2 alternate \(\mathcal{D}\) on L1 only | `TODO` | Check effect isn’t pure coordinates |
| **6** | **Repo hygiene** — merge or label `fold-math-e-lock` / `e-lock-fractal-` as legacy | `TODO` | Avoid three half-stories |
| **7** | **Public surface freeze** — badge/claim line + open falsifiers; optional short note | `TODO` | No spam; no universal claims |
| **8** | **JoeysAI quarantine check** — κ stays hypothesis-capped; no dig/promote from κ as truth | `TODO` | Integration discipline |

---

## Active item detail — #1 Repro mini-package

**Goal:** Anyone can clone this repo and compute a κ_C-style coupling on a **small, redistributable** trajectory set without JoeysAI private paths.

**Deliverables:**

1. `src/` or `kappa/` module: defect proxy, kNN entropy rate, close-approach mask, \(\kappa_C\), \(\kappa_{\mathrm{eff}}\)
2. `data/sample/` — tiny public or synthetic series (documented origin / synthetic seed)
3. `scripts/reproduce_mini.py` — prints \(\kappa_C\), CI (bootstrap), \(\kappa_{\mathrm{eff}}\), pass/fail vs \(\theta_C=0.35\)
4. `REPRO.md` — one-command run + expected numeric band (approx OK)
5. `requirements.txt` — numpy (+ optional sklearn for kNN)

**Done when:**

- [ ] Clone + `pip install -r requirements.txt` + run script succeeds on a clean machine
- [ ] No absolute personal filesystem paths in code
- [ ] README links to REPRO.md
- [ ] Hypothesis disclaimer remains

**Out of scope for #1:** full 3-system battery, Horizons downloads, Kaggle bulk.

---

## Parking lot (not in main queue)

- Bio-AI / QG narrative expansions  
- PhaseLoom thresholds driven by κ  
- Peer outreach for marketing  
- Constant-hunting as lead claim  

---

## Log

| Date | Event |
|------|--------|
| 2026-07-17 | Queue created; #1 ACTIVE |

---

*When an item finishes: set `DONE`, add a one-line log entry, promote next `TODO` → `ACTIVE`.*
