# Reproducing remarks PDF equation (2.2)

This document explains, with extra detail beyond `docs/ARCHITECTURE.md`,
how the numerical reproduction of equation (2.2) of the
*Remarks on the Disproof of the Unit Distance Conjecture* PDF is computed
in this repository.

## The published claim

The remarks PDF section 2.1 takes the specific choice

```
T = {3, 5, 7, 11, 13, 17}
S = {101, infinity}
L_T = Q(sqrt 5, sqrt 13, sqrt 17, sqrt 21, sqrt 33)   (totally real, degree 32)
K_j = L_j(i)                                          (CM by adjoining i)
r = 2 * 3 * 5 * 7 * 11 * 13 * 17 = 510510
```

and states, immediately after Lemma 2.1,

> "Explicitly, the exponent in (2.1) can be taken to be
>
>     1 + log(u pi / (36 v)) / log(36 / delta^2) ~ 1 + 6.24 * 10^{-38}
>
> where v = r/2, delta >= 101^{-2 ceil(18 r^3 / pi)}, and
> u = ceil(18 r^3 / pi) * r^{-2}, with r = 2 * 3 * 5 * 7 * 11 * 13 * 17."

This is the **only verbatim numerical lower bound** that appears in
either formal PDF. The widely reported values `~ 0.014` and `~ 0.0318`
do **not** appear in either PDF.

## What this repository computes

The function `evaluate_sawin_exponent_bound()` in
`src/erdos_ant/sawin_multiquadratic.py` evaluates exactly the formula
above using mpmath at 200-bit precision and returns a
`SawinDeltaEvaluation` dataclass with the field `exponent_excess`.

Running on commit-pinned environment:

```python
from erdos_ant.sawin_multiquadratic import evaluate_sawin_exponent_bound
e = evaluate_sawin_exponent_bound()
print(f"K = {e.k + 1}")
print(f"exponent excess = {e.exponent_excess:.4e}")
```

produces

```
K = 7.62e17  (= ceil(18 * 510510^3 / pi))
exponent excess = 6.2391e-38
```

Relative error against the published value `6.24e-38`:
`|6.2391e-38 - 6.24e-38| / 6.24e-38 ~= 0.000144`, i.e. about 0.01%.

The remaining difference is consistent with the published value being
quoted to two significant figures.

## Why mpmath is needed

After simplification,

```
exponent_excess = log(K * pi / (18 * r^3)) / (log(36) + 4 * K * log(101))
```

with `r = 510510`. We have

```
K = ceil(18 * r^3 / pi)
```

so the ratio `K * pi / (18 * r^3)` is in the half-open interval
`(1, 1 + pi / (18 * r^3)]`. Numerically

```
pi / (18 * r^3) ~= 1.31 * 10^(-18)
```

so the numerator of the formula is `log(1 + x)` for `x` on the order of
`10^(-18)`. Standard IEEE 754 `float64` (52-bit mantissa, machine
epsilon `~ 2.2 * 10^(-16)`) cannot represent `1 + 1e-18` distinctly from
`1`, so the naive evaluation produces `log(1) = 0` and the entire
exponent excess collapses to 0.

To avoid this, we evaluate the ratio and its logarithm using
`mpmath.mp.prec = 200` (about 60 decimal digits of precision). This is
sufficient to recover the correct `~ 10^(-38)` value with several
digits of trustworthy accuracy.

## Reproducing the result yourself

```bash
# Clone, install
git clone https://github.com/Flamehaven-Labs/openai-erdos-eq22-reproduction
cd openai-erdos-eq22-reproduction
pip install -e ".[dev]"

# Single-line verification
python -c "from erdos_ant.sawin_multiquadratic import evaluate_sawin_exponent_bound; e = evaluate_sawin_exponent_bound(); print(f'{e.exponent_excess:.4e}')"
# 6.2391e-38

# Full test suite (pins this value plus the rest of the construction)
pytest -q

# End-to-end verification, default frozen-report mode
python scripts/verify.py

# Refresh tracked JSON + Markdown evidence
python scripts/verify.py --write-evidence
```

The default verifier mode prints the verdict without touching tracked
evidence files. Release maintainers use `--write-evidence` when they
intend to refresh `reports/verification_result.json` and
`reports/verification_report.md`.

## Pinned test for regression protection

The reproduction is pinned by
`tests/test_sawin_multiquadratic.py::test_sawin_exponent_bound_matches_remarks_eq_2_2`,
which asserts that

```
abs(exponent_excess - 6.24e-38) / 6.24e-38 < 1e-3
```

The current tolerance is `1e-3`, matching the deviation-log policy that
values below `1e-3` relative error are consistent with the
two-significant-figure source value. The observed error is about
`1.4e-4`, leaving margin for source rounding while still catching
meaningful drift.
