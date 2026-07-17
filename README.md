# κ-Fractal Stability (Working Hypothesis)

**Status:** experimental / exploratory — **not** an established physical law.  
May be revised, restricted in scope, or discarded when data disagree.

This repository records the **physics and mathematics** of a family of quantities
used to probe **fractal / information structure near dynamical separatrices**
(especially three-body and halo-orbit geometries). No personal or product material.

---

## Core idea

Near certain unstable manifolds (e.g. collinear Lagrange-point **halo** families and
**separatrix** neighborhoods), a **curvature-defect** proxy and an **information
entropy rate** appear **coupled**. That coupling is summarized by a scalar \(\kappa_C\);
a derived scale \(\kappa_{\mathrm{eff}} = e^{-\kappa_C}\) is compared to the constant
\(1 - 1/e \approx 0.6321\).

**Working claim (scoped):**  
In at least some **orbit families** with strong separatrix structure, close-approach
segments show positive \(\kappa_C\) with bootstrap support.  
**Not claimed:** a universal constant for all three-body or all chaotic systems.

---

## Definitions

### Coupling \(\kappa_C\)

At **close approach** to a reference manifold (separatrix / L-point neighborhood):

\[
\kappa_C
\;=\;
\mathrm{corr}\!\left(
  \mathcal{D}(t),\;
  \dot H_{\mathrm{kNN}}(t)
\right)
\]

where:

| Symbol | Meaning |
|--------|---------|
| \(\mathcal{D}(t)\) | Curvature-**defect** proxy along the trajectory (local geometric strain / defect window) |
| \(\dot H_{\mathrm{kNN}}(t)\) | k-nearest-neighbor **differential entropy rate** (information production proxy) |
| \(\mathrm{corr}\) | Pearson correlation over the close-approach sample |

**Typical pipeline parameters (replication battery v1):**

| Parameter | Value |
|-----------|------:|
| Close approach | nearest **15%** of separatrix distance |
| Defect window | 9 samples |
| Entropy \(k\) | 6 |
| Entropy window | 12 samples |

### Effective scale \(\kappa_{\mathrm{eff}}\)

\[
\kappa_{\mathrm{eff}} \;=\; \exp(-\kappa_C)
\]

**Reference band:** \(\kappa_{\mathrm{eff}}\) near

\[
1 - \frac{1}{e} \;=\; 1 - e^{-1} \;\approx\; 0.6321205588
\]

within relative tolerance \(\sim 15\%\) in systems that pass primary or alternate criteria.

### kNN differential entropy (Kozachenko–Leonenko form)

For a \(d\)-dimensional point cloud \(\{x_i\}_{i=1}^N\) and \(k\)-NN distances \(\rho_i\):

\[
\hat H
\;\approx\;
\frac{1}{N}\sum_{i=1}^{N}
\left[
  \log \rho_i
  + \log V_d
  + \log N
  - \log k
\right]
\]

with unit-ball volume \(V_d = \pi^{d/2}/\Gamma(d/2+1)\).  
**Entropy rate** uses sliding windows and absolute differencing:

\[
\dot H(t) \;\approx\; \big|\,\hat H_{W(t)} - \hat H_{W(t-1)}\,\big|
\]

Coarse (histogram) and refined (finer bins, shorter windows) entropy rates are used
as secondary diagnostics for separatrix resolution.

---

## Success and falsification (replication battery)

Predictions are **frozen before** evaluation (data outranks theory).

### Success (per system)

| Criterion | Rule |
|-----------|------|
| **Primary** | \(\kappa_C > 0.35\) and bootstrap CI lower bound \(> 0\) |
| **Alternate** | \(\kappa_{\mathrm{eff}}\) within **15%** of \(1-1/e\) |

### Cross-system requirement

At least **2 of 3** independent systems must pass primary **or** alternate.

### Falsification

- Fewer than 2 systems pass either criterion, **or**
- All systems yield \(\kappa_C\) means whose CIs include zero.

---

## Empirical status (cross-system battery v1)

| System | Description | Primary \(\kappa_C\) | Alternate \(\kappa_{\mathrm{eff}}\) | Pass? |
|--------|-------------|---------------------:|------------------------------------:|:-----:|
| JPL L1 halo (low-unstable) | Earth–Moon unstable L1 halo family | **yes** (\(\bar\kappa_C \approx 0.71\)) | no | **yes** |
| Horizons Sun–Earth–Moon | DE441-relative close approaches | no | **yes** (\(\kappa_{\mathrm{eff}}\approx 0.69\)) | **yes** |
| Kaggle TBP chaotic | Newtonian chaotic 3-body trajectories | no | no | **no** |

**Verdict:** `partially_supported_family_specific`  
**Physics positioning:** coupling holds in **at least one family** (notably L1-halo / separatrix-like geometries); **not** established as universal scaling.

### Scope guidance

| Keep | Retire / avoid |
|------|----------------|
| Family-specific halo / separatrix tests | Universal “ribbon” claims without per-family tests |
| Frozen predictions before data | Using Hurst as primary proxy |
| CI + multi-system replication | Treating \(\kappa\) as settled fundamental constant |

---

## Geometric / dynamical context

### Close-approach manifold

Let \(d_{\mathrm{sep}}(t)\) be distance to a reference separatrix or L-point.

\[
\mathcal{M}_{\mathrm{close}}
=
\big\{\, t :\; d_{\mathrm{sep}}(t) \le Q_{p}\!\big(d_{\mathrm{sep}}\big) \,\big\}
\]

with percentile \(p \approx 15\%\) (widened if too few points). Coupling is estimated
**on** \(\mathcal{M}_{\mathrm{close}}\), not on the full trajectory.

### Why separatrices?

Near unstable manifolds, stretching (e.g. FTLE peaks) and local phase-space volume
changes co-occur. \(\kappa_C\) is a **phenomenological** summary of defect \(\leftrightarrow\)
entropy-rate alignment in that neighborhood—not a derived first principle (yet).

### FTLE-aligned diagnostics (secondary)

Peaks of finite-time Lyapunov exponent (FTLE) can gate kNN entropy windows:

\[
t \in \mathrm{FTLE}_{\mathrm{peak}}
\quad\Rightarrow\quad
\text{estimate local }\hat H\text{ in a window about }t
\]

Used for resolution / visualization, not as the sole success metric of the battery.

---

## Relation to \(e\) and fractal-scale language

- The alternate target \(1-1/e\) arises as \(\exp(-\kappa_C)\) when \(\kappa_C \approx 1\),
  and more generally as a **dimensionless** band for \(\kappa_{\mathrm{eff}}\).
- “Fractal fold” language refers to **self-similar information geometry** near
  folds / separatrices, **not** a claim that spacetime dimension equals \(e\).
- Power-law and exponential-saturation fits appear in exploratory **derivation**
  notebooks (fit \(y \approx a x^{b}\), compare to \(e\), \(1/e\), \(\ln 2\), …);
  those are **discovery diagnostics**, not confirmed constants.

---

## Minimal algorithm (outline)

1. Integrate or load trajectory \(x(t) \in \mathbb{R}^d\).  
2. Compute \(d_{\mathrm{sep}}(t)\) and select close-approach mask.  
3. Compute defect series \(\mathcal{D}(t)\) (windowed curvature / geometric defect).  
4. Compute \(\dot H_{\mathrm{kNN}}(t)\) (windowed kNN entropy rate).  
5. Restrict both series to the mask; estimate \(\kappa_C = \mathrm{corr}(\mathcal{D},\dot H)\).  
6. Form \(\kappa_{\mathrm{eff}} = e^{-\kappa_C}\); bootstrap CI on \(\kappa_C\).  
7. Apply primary / alternate criteria; require multi-system replication for scope claims.

---

## Mathematical objects (summary table)

| Object | Formula / role |
|--------|----------------|
| Shannon entropy (bins) | \(H = -\sum p_i \log p_i\) |
| Coarse entropy rate | \(\lvert H_{t}-H_{t-\Delta}\rvert\) on coarse bins |
| kNN \(\hat H\) | Kozachenko–Leonenko estimator |
| \(\kappa_C\) | \(\mathrm{corr}(\mathcal{D}, \dot H_{\mathrm{kNN}})\) on close approach |
| \(\kappa_{\mathrm{eff}}\) | \(e^{-\kappa_C}\) |
| Reference scale | \(1-e^{-1}\) |
| Success | \(\kappa_C>0.35\) with CI\(_\mathrm{lo}>0\), or \(\kappa_{\mathrm{eff}}\) within 15% of \(1-e^{-1}\) |

---

## Hypotheses still open

1. Is \(\kappa_C\) a **family** invariant under smooth coordinate change?  
2. Can \(\mathcal{D}\) be replaced by a coordinate-free geometric invariant?  
3. Does any **first-principles** argument fix \(1-1/e\), or is it only an empirical attractor?  
4. Where is the **boundary** between L1-halo-like success and fully chaotic TBP failure?

---

## Citation / use

Use as **hypothesis + methods + numbers**, not as textbook law.  
When embedding in larger systems, keep confidence **capped** and label **hypothesis mode**
until independent replications expand the supported family set.

---

## Changelog

| Date | Note |
|------|------|
| 2025–2026 | Initial public stub |
| 2026-07 | Physics/math refresh: definitions, battery criteria, multi-system results, scope limits |

---

## License

See `LICENSE` (MIT unless stated otherwise).
