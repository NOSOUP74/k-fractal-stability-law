"""
Synthetic trajectory with positive defect ↔ entropy-rate coupling near a separatrix.

Not real celestial data — redistributable demo for the repro package.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple

import numpy as np


def generate_coupled_orbit(
    n: int = 500,
    seed: int = 42,
) -> Dict[str, np.ndarray]:
    """
    Helix that repeatedly approaches the z-axis (separatrix proxy).

    Near the axis we inject:
      - high-frequency geometric wiggle → Frenet curvature spikes
      - larger local scatter → higher windowed kNN entropy / rate

    Shared latent amplitude ⇒ positive corr(defect, entropy_rate) on close approach.
    """
    rng = np.random.default_rng(seed)
    t = np.linspace(0.0, 16 * np.pi, n)

    # Base radial distance with two deep close approaches
    r = 1.4 + 0.55 * np.cos(0.4 * t)
    r = r * (1.0 - 0.72 * np.exp(-0.5 * ((t - 18.0) / 2.2) ** 2))
    r = r * (1.0 - 0.68 * np.exp(-0.5 * ((t - 38.0) / 2.5) ** 2))
    r = np.clip(r, 0.06, None)

    theta = t
    z = 0.12 * t

    # Shared stress: large when close to axis
    stress = 1.0 / (r + 0.08)
    stress = (stress - np.mean(stress)) / (np.std(stress) + 1e-12)
    stress = np.clip(stress, -2.5, 4.0)

    # Unit cylindrical frame
    er = np.column_stack([np.cos(theta), np.sin(theta), np.zeros(n)])
    et = np.column_stack([-np.sin(theta), np.cos(theta), np.zeros(n)])
    ez = np.tile(np.array([0.0, 0.0, 1.0]), (n, 1))

    # High-freq wiggle amplitude tracks stress → curvature defect near close approach
    amp = 0.01 + 0.09 * np.maximum(stress, 0.0)
    wiggle = (
        (amp * np.sin(14 * t))[:, None] * er
        + (0.7 * amp * np.cos(11 * t))[:, None] * et
        + (0.4 * amp * np.sin(9 * t))[:, None] * ez
    )

    pos = np.column_stack([r * np.cos(theta), r * np.sin(theta), z]) + wiggle

    # Local dispersion tracks same stress → entropy production near close approach
    noise_amp = 0.004 + 0.055 * np.maximum(stress, 0.0)
    pos = pos + rng.normal(size=pos.shape) * noise_amp[:, None]

    dist = np.sqrt(pos[:, 0] ** 2 + pos[:, 1] ** 2)
    return {
        "positions": pos,
        "dist_to_sep": dist,
        "stress": stress,
        "t": t,
    }


def save_sample(path: Path, seed: int = 42) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = generate_coupled_orbit(n=500, seed=seed)
    npz = path.with_suffix(".npz")
    np.savez_compressed(
        npz,
        positions=data["positions"],
        dist_to_sep=data["dist_to_sep"],
        stress=data["stress"],
        t=data["t"],
        seed=np.array([seed]),
        note=np.array(["synthetic_coupled_orbit_v2"]),
    )
    csv_path = path.with_suffix(".csv")
    arr = np.column_stack([data["t"], data["positions"], data["dist_to_sep"]])
    np.savetxt(
        csv_path,
        arr,
        delimiter=",",
        header="t,x,y,z,dist_to_sep",
        comments="",
    )
    return npz


def load_sample(path: Path) -> Tuple[np.ndarray, np.ndarray]:
    path = Path(path)
    if path.suffix == ".npz" or path.with_suffix(".npz").is_file():
        p = path if path.suffix == ".npz" else path.with_suffix(".npz")
        z = np.load(p)
        return z["positions"], z["dist_to_sep"]
    p = path if path.suffix == ".csv" else path.with_suffix(".csv")
    arr = np.loadtxt(p, delimiter=",", skiprows=1)
    return arr[:, 1:4], arr[:, 4]
