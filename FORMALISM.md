# Formalism: κ coupling near separatrices

Mathematics-only companion to the README. Working hypothesis.

---

## 1. Phase space and trajectory

Let \(\mathcal{M}\) be a smooth manifold of dimension \(d\) (configuration or
phase space). A trajectory is a map

\[
x : I \subset \mathbb{R} \to \mathcal{M}, \qquad t \mapsto x(t).
\]

In practice \(x(t) \in \mathbb{R}^d\) in adapted coordinates (e.g. relative
Earth–Moon frame for CR3BP / ephemeris reductions).

---

## 2. Separatrix distance

Let \(S \subset \mathcal{M}\) be a reference **unstable manifold** or Lagrange
point neighborhood. Define

\[
d_S(t) \;=\; \mathrm{dist}\big(x(t),\, S\big).
\]

Close-approach set at level \(p\in(0,100)\):

\[
A_p
=
\big\{
  t\in I :
  d_S(t) \le Q_p(d_S)
\big\},
\]

where \(Q_p\) is the \(p\)-th empirical percentile of \(\{d_S(t)\}\).  
Default battery: \(p = 15\); widen if \(\lvert A_p\rvert\) is below a minimum sample size.

---

## 3. Curvature defect proxy \(\mathcal{D}(t)\)

Let \(K(t)\) be a local geometric diagnostic (curvature of a reconstructed
curve, discrete Frenet-type estimate, or manifold defect residual). A
**defect** series is a high-pass / residual form, e.g. windowed deviation

\[
\mathcal{D}(t)
=
K(t) - \mathrm{smooth}_{W_{\mathcal{D}}}\big(K\big)(t)
\quad\text{or}\quad
\mathcal{D}(t) = \big\lVert R(t)\big\rVert
\]

for residual \(R\) against a local manifold fit.  
Implementation uses a finite **defect window** \(W_{\mathcal{D}}\) (battery: 9).

Exact coordinate formula is system-dependent; the **hypothesis** only requires
that \(\mathcal{D}\) track **local geometric stress** near \(S\).

---

## 4. Differential entropy and rates

### 4.1 Kozachenko–Leonenko kNN estimator

For samples \(X = \{x_i\}_{i=1}^{N}\subset\mathbb{R}^d\), let \(\rho_{i,k}\) be
the Euclidean distance from \(x_i\) to its \(k\)-th nearest neighbor (excluding
self). With unit-ball volume

\[
V_d = \frac{\pi^{d/2}}{\Gamma(d/2+1)},
\]

\[
\hat H(X)
=
\frac{1}{N}\sum_{i=1}^{N}
\big(
  \log\rho_{i,k}
  + \log V_d
  + \log N
  - \log k
\big).
\]

### 4.2 Sliding-window profile

For window length \(W_H\) centered at \(t\),

\[
\hat H_W(t) = \hat H\big(x|_{[t-W_H/2,\, t+W_H/2]}\big).
\]

### 4.3 Entropy rate proxy

\[
\dot H(t)
=
\big\lvert
  \hat H_W(t) - \hat H_W(t-\Delta t)
\big\rvert.
\]

Battery defaults: \(k=6\), \(W_H=12\).

### 4.4 Coarse histogram rate (diagnostic)

Partition a local box into \(n_b\) bins, form occupation entropy \(H_{\mathrm{bin}}(t)\),
then \(\lvert\Delta H_{\mathrm{bin}}\rvert\). Refined bins / shorter windows improve
separatrix resolution but increase variance.

---

## 5. Coupling statistic \(\kappa_C\)

Restrict time to \(A_p\). Let \(\mathcal{D}|_{A_p}\) and \(\dot H|_{A_p}\) be the
restricted series (aligned, finite samples only). Define

\[
\kappa_C
=
\frac{
  \mathrm{Cov}\big(\mathcal{D},\,\dot H\big)
}{
  \sigma(\mathcal{D})\,\sigma(\dot H)
}
\in [-1,1]
\]

when both standard deviations are positive; else undefined.

### Bootstrap

Resample pairs on \(A_p\) with replacement; report mean \(\bar\kappa_C\) and
percentile CI. Primary success requires CI lower bound \(> 0\).

---

## 6. Effective scale \(\kappa_{\mathrm{eff}}\)

\[
\kappa_{\mathrm{eff}} = e^{-\kappa_C}.
\]

Properties:

- \(\kappa_C = 0 \Rightarrow \kappa_{\mathrm{eff}} = 1\) (no coupling → full scale).  
- \(\kappa_C \to +\infty \Rightarrow \kappa_{\mathrm{eff}} \to 0\).  
- \(\kappa_C = 1 \Rightarrow \kappa_{\mathrm{eff}} = e^{-1}\).  
- Target band around \(1-e^{-1}\):

\[
\big\lvert
  \kappa_{\mathrm{eff}} - (1-e^{-1})
\big\rvert
\le
0.15\,(1-e^{-1})
\quad\text{(illustrative 15% relative rule used in battery)}
\]

or equivalently relative error \(\le 0.15\) as implemented.

---

## 7. Decision rules (replication)

Let systems be \(s=1,\ldots,S\) (battery \(S=3\)).

\[
\mathrm{Pass}_s^{\mathrm{pri}}
=
\big[
  \bar\kappa_C^{(s)} > \theta_C
  \;\wedge\;
  \mathrm{CI}_{\mathrm{lo}}^{(s)} > 0
\big],
\quad
\theta_C = 0.35.
\]

\[
\mathrm{Pass}_s^{\mathrm{alt}}
=
\big[
  \mathrm{relerr}\big(\kappa_{\mathrm{eff}}^{(s)},\, 1-e^{-1}\big) \le 0.15
\big].
\]

\[
\mathrm{Pass}_s = \mathrm{Pass}_s^{\mathrm{pri}} \lor \mathrm{Pass}_s^{\mathrm{alt}}.
\]

Global battery:

\[
\sum_{s=1}^{S} \mathbf{1}[\mathrm{Pass}_s] \;\ge\; 2.
\]

**Family-specific support** if the inequality holds but at least one system fails
(especially fully chaotic samples without the same manifold structure).

---

## 8. Auxiliary: FTLE peak gating

Finite-time Lyapunov exponent \(\Lambda(t)\). Peak mask:

\[
\Lambda(t) \ge Q_{q}(\Lambda), \quad q\approx 85.
\]

Optional diagnostic: average \(\hat H_W(t)\) only for \(t\) in the peak mask.
Used for visualization of stretching–entropy alignment; **not** the primary
definition of \(\kappa_C\).

---

## 9. Exploratory constant matching

Given a fitted scalar \(c\) from power-law or saturation fits, relative distance
to a reference set \(\mathcal{R}=\{e, e^{-1}, \ln 2, \pi/e, \ldots\}\):

\[
\mathrm{relerr}(c,r) = \frac{\lvert c-r\rvert}{\max(\lvert r\rvert,\varepsilon)}.
\]

Nearest reference is a **discovery hint**, not a theorem.

Power-law fit on positive pairs \((x_i,y_i)\):

\[
\log y \approx \log a + b\log x,
\qquad
R^2 = 1 - \frac{\sum(y-\hat y)^2}{\sum(y-\bar y)^2}.
\]

---

## 10. What is *not* asserted

- \(\kappa_C\) is **not** proven invariant under all diffeomorphisms.  
- \(1-1/e\) is **not** derived as a universal fixed point of gravity.  
- Failure on chaotic TBP samples does **not** alone falsify family-specific L1 results;
  it **does** block universal claims.

---

## 11. Notation cheatsheet

| Symbol | Name |
|--------|------|
| \(S\) | Separatrix / L-point reference set |
| \(d_S\) | Distance to \(S\) |
| \(A_p\) | Close-approach time set |
| \(\mathcal{D}\) | Curvature defect proxy |
| \(\hat H\) | kNN differential entropy |
| \(\dot H\) | Entropy rate proxy |
| \(\kappa_C\) | Defect–entropy coupling |
| \(\kappa_{\mathrm{eff}}\) | \(e^{-\kappa_C}\) |
| \(\Lambda\) | FTLE |
| \(\theta_C\) | Primary threshold \(0.35\) |
