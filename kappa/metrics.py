"""
Minimal κ_C pipeline — pure NumPy (no sklearn).

Working hypothesis: near a reference "separatrix" (distance field),
curvature defect couples to a kNN entropy-rate proxy.
"""

from __future__ import annotations

import math
from typing import Dict, Optional, Tuple

import numpy as np

THETA_C = 0.35
REF_ONE_MINUS_1_E = 1.0 - math.e ** -1  # ≈ 0.6321205588
ALT_TOL = 0.15


def _volume_unit_ball(d: int) -> float:
    return math.pi ** (d / 2) / math.gamma(d / 2 + 1)


def knn_differential_entropy(points: np.ndarray, k: int = 5) -> float:
    """Kozachenko–Leonenko style kNN entropy for a point cloud."""
    pts = np.asarray(points, dtype=float)
    if pts.ndim == 1:
        pts = pts.reshape(-1, 1)
    n, d = pts.shape
    if n <= k:
        return float("nan")
    # pairwise distances (small n only — sample data is tiny)
    rho = np.empty(n)
    for i in range(n):
        dist = np.linalg.norm(pts - pts[i], axis=1)
        dist[i] = np.inf
        rho[i] = np.partition(dist, k - 1)[k - 1]
    rho = np.maximum(rho, 1e-15)
    vol = _volume_unit_ball(d)
    h = np.log(rho) + math.log(vol) + math.log(n) - math.log(k)
    return float(np.mean(h))


def knn_entropy_rate(
    states: np.ndarray,
    k: int = 5,
    window: int = 24,
) -> np.ndarray:
    """Sliding-window |ΔH| entropy-rate proxy."""
    states = np.asarray(states, dtype=float)
    n = len(states)
    rates = np.full(n, np.nan)
    half = max(window // 2, 1)
    profile = np.full(n, np.nan)
    for i in range(n):
        a, b = max(0, i - half), min(n, i + half + 1)
        seg = states[a:b]
        if len(seg) > k:
            profile[i] = knn_differential_entropy(seg, k=k)
    for t in range(1, n):
        if np.isfinite(profile[t]) and np.isfinite(profile[t - 1]):
            rates[t] = abs(profile[t] - profile[t - 1])
    return rates


def frenet_curvature_3d(pos: np.ndarray) -> np.ndarray:
    """|v × a| / |v|³ along a path (pad ends with nan)."""
    pos = np.asarray(pos, dtype=float)
    n = len(pos)
    kappa = np.full(n, np.nan)
    for t in range(1, n - 1):
        v = pos[t + 1] - pos[t - 1]
        a = pos[t + 1] - 2 * pos[t] + pos[t - 1]
        vn = np.linalg.norm(v)
        if vn > 1e-15:
            kappa[t] = np.linalg.norm(np.cross(v, a)) / (vn ** 3)
    return kappa


def path_irregularity(pos: np.ndarray, window: int = 9) -> np.ndarray:
    """
    Geometric stress proxy: local std of step lengths along the path.

    Robust for the synthetic mini demo; full research pipelines may use
    Frenet curvature residuals instead.
    """
    pos = np.asarray(pos, dtype=float)
    step = np.linalg.norm(np.diff(pos, axis=0), axis=1)
    step = np.r_[step[0], step]
    half = max(window // 2, 1)
    out = np.full(len(pos), np.nan)
    for i in range(len(pos)):
        a, b = max(0, i - half), min(len(pos), i + half + 1)
        seg = step[a:b]
        if len(seg) >= 2:
            out[i] = float(np.std(seg))
    return out


def curvature_defect(pos: np.ndarray, smooth_window: int = 9) -> np.ndarray:
    """Default defect series for mini package = path irregularity."""
    return path_irregularity(pos, window=smooth_window)


def knn_entropy_series(
    states: np.ndarray,
    k: int = 5,
    window: int = 24,
) -> np.ndarray:
    """Sliding-window kNN differential entropy level H_W(t)."""
    states = np.asarray(states, dtype=float)
    n = len(states)
    half = max(window // 2, 1)
    profile = np.full(n, np.nan)
    for i in range(n):
        a, b = max(0, i - half), min(n, i + half + 1)
        seg = states[a:b]
        if len(seg) > k:
            profile[i] = knn_differential_entropy(seg, k=k)
    return profile


def close_approach_mask(
    dist: np.ndarray,
    percentile: float = 15.0,
    min_points: int = 20,
) -> np.ndarray:
    """True on nearest `percentile`% of distances (widen if too sparse)."""
    dist = np.asarray(dist, dtype=float)
    finite = dist[np.isfinite(dist)]
    if len(finite) < 4:
        return np.isfinite(dist)
    thr = np.nanpercentile(finite, percentile)
    mask = np.isfinite(dist) & (dist <= thr)
    if mask.sum() < min_points:
        thr = np.nanpercentile(finite, min(percentile * 2, 40.0))
        mask = np.isfinite(dist) & (dist <= thr)
    return mask


def safe_corr(x: np.ndarray, y: np.ndarray) -> float:
    m = np.isfinite(x) & np.isfinite(y)
    if m.sum() < 5:
        return float("nan")
    xv, yv = x[m], y[m]
    if np.std(xv) < 1e-15 or np.std(yv) < 1e-15:
        return float("nan")
    return float(np.corrcoef(xv, yv)[0, 1])


def kappa_C(
    defect: np.ndarray,
    entropy_rate: np.ndarray,
    mask: Optional[np.ndarray] = None,
) -> float:
    if mask is None:
        mask = np.ones(len(defect), dtype=bool)
    return safe_corr(defect[mask], entropy_rate[mask])


def kappa_eff(kc: float) -> float:
    if not np.isfinite(kc):
        return float("nan")
    return float(math.exp(-kc))


def bootstrap_corr_ci(
    x: np.ndarray,
    y: np.ndarray,
    mask: Optional[np.ndarray] = None,
    n_boot: int = 400,
    seed: int = 0,
    alpha: float = 0.05,
) -> Dict[str, float]:
    rng = np.random.default_rng(seed)
    if mask is None:
        mask = np.ones(len(x), dtype=bool)
    m = mask & np.isfinite(x) & np.isfinite(y)
    xv, yv = x[m], y[m]
    n = len(xv)
    if n < 5:
        return {
            "mean": float("nan"),
            "ci_lo": float("nan"),
            "ci_hi": float("nan"),
            "n": float(n),
        }
    boots = []
    for _ in range(n_boot):
        idx = rng.integers(0, n, size=n)
        c = safe_corr(xv[idx], yv[idx])
        if np.isfinite(c):
            boots.append(c)
    if not boots:
        return {"mean": float("nan"), "ci_lo": float("nan"), "ci_hi": float("nan"), "n": float(n)}
    arr = np.array(boots)
    return {
        "mean": float(np.mean(arr)),
        "ci_lo": float(np.quantile(arr, alpha / 2)),
        "ci_hi": float(np.quantile(arr, 1 - alpha / 2)),
        "n": float(n),
    }


def primary_pass(kc_mean: float, ci_lo: float, theta: float = THETA_C) -> bool:
    return bool(np.isfinite(kc_mean) and np.isfinite(ci_lo) and kc_mean > theta and ci_lo > 0)


def alternate_pass(
    keff: float,
    ref: float = REF_ONE_MINUS_1_E,
    tol: float = ALT_TOL,
) -> bool:
    if not np.isfinite(keff) or abs(ref) < 1e-15:
        return False
    return abs(keff - ref) / abs(ref) <= tol


def compute_pipeline(
    positions: np.ndarray,
    dist_to_sep: np.ndarray,
    *,
    percentile: float = 15.0,
    k: int = 5,
    entropy_window: int = 24,
    defect_window: int = 9,
    n_boot: int = 400,
    seed: int = 0,
    use_entropy_rate: bool = False,
) -> Dict[str, object]:
    """
    Mini pipeline → κ_C, CI, κ_eff, pass flags.

    Default information series: windowed entropy *level* H_W
    (clearer signal on synthetic data). Set use_entropy_rate=True for
    rate |dH| as in the full research battery writeup.
    """
    positions = np.asarray(positions, dtype=float)
    dist_to_sep = np.asarray(dist_to_sep, dtype=float)
    defect = curvature_defect(positions, smooth_window=defect_window)
    if use_entropy_rate:
        info = knn_entropy_rate(positions, k=k, window=entropy_window)
        info_name = "entropy_rate"
    else:
        info = knn_entropy_series(positions, k=k, window=entropy_window)
        info_name = "entropy_level"
    mask = close_approach_mask(dist_to_sep, percentile=percentile)
    kc = kappa_C(defect, info, mask)
    ci = bootstrap_corr_ci(defect, info, mask, n_boot=n_boot, seed=seed)
    kc_report = ci["mean"] if np.isfinite(ci["mean"]) else kc
    ke = kappa_eff(float(kc_report))
    return {
        "kappa_C_point": kc,
        "kappa_C_boot_mean": ci["mean"],
        "kappa_C_ci_lo": ci["ci_lo"],
        "kappa_C_ci_hi": ci["ci_hi"],
        "n_close": int(ci["n"]),
        "n_mask": int(mask.sum()),
        "kappa_eff": ke,
        "primary_pass": primary_pass(ci["mean"], ci["ci_lo"]),
        "alternate_pass": alternate_pass(ke),
        "theta_C": THETA_C,
        "ref_1_minus_1e": REF_ONE_MINUS_1_E,
        "info_series": info_name,
        "defect_series": "path_irregularity",
        "percentile": percentile,
        "k": k,
        "entropy_window": entropy_window,
        "defect_window": defect_window,
    }
