# Proof Origin

## Source documents

The mathematical content this artifact verifies originates entirely from
two PDFs released in May 2026:

1. **OpenAI (2026)**, *Planar Point Sets with Many Unit Distances*
   - URL: <https://cdn.openai.com/pdf/74c24085-19b0-4534-9c90-465b8e29ad73/unit-distance-proof.pdf>
   - 18 pages.
   - Contains the AI-generated proof of Theorem 1.1: there exists an
     absolute constant `delta > 0` and infinitely many positive integers
     `n` such that `nu(n) >= n^(1 + delta)`.

2. **Alon, Bloom, Gowers, Litt, Sawin, Shankar, Tsimerman, Wang, Wood
   (2026)**, *Remarks on the Disproof of the Unit Distance Conjecture*
   - URL: <https://cdn.openai.com/pdf/74c24085-19b0-4534-9c90-465b8e29ad73/unit-distance-remarks.pdf>
   - 19 pages.
   - Contains a "human-digested, somewhat simplified, and somewhat
     generalized version" of the AI proof, including Sawin's simplified
     construction using a pro-2 tower over a multi-quadratic field and the
     explicit numerical exponent excess in equation (2.2).

## What was proved (by them, not by this repository)

Both PDFs prove **Theorem 1.1**:

> There exists an absolute constant `delta > 0` and infinitely many
> positive integers `n` such that `nu(n) >= n^(1 + delta)`.

This **disproves** the Erdős unit-distance conjecture (1946), which held
that `nu(n) <= n^(1 + C / log log n)` for some absolute constant `C`.

## What was NOT proved (and is also not in this repository)

- The literal numerical values `delta ~ 0.014` and `delta ~ 0.0318`
  reported in secondary coverage (Gil Kalai's blog, news outlets) do
  **not appear verbatim** in either PDF. We verified this by direct text
  extraction with `pypdf`.
- The remarks PDF eq (2.2) gives the only numerical lower bound that
  appears verbatim: `delta >= 6.24 * 10^(-38)` for the explicit choice
  `T = {3, 5, 7, 11, 13, 17}`, `S = {101, infinity}`,
  `k = ceil(18 r^3 / pi)`, `r = 2 * 3 * 5 * 7 * 11 * 13 * 17 = 510510`.

## Construction overview

The unit-distance graph is built in three layers:

1. **A CM field of growing degree.** Take an infinite tower of totally
   real fields `L_0 subset L_1 subset L_2 subset ...` of bounded root
   discriminant, then set `K_j = L_j(i)` to make each layer CM.
2. **Norm-one elements (Lemma 2.2).** For sufficiently many rational
   primes `q_b` that split completely in every `K_j`, build many ideals of
   the form `A_eps = prod_j P_j^{eps_j} (P_j')^{k - eps_j}` and use a
   class-group pigeonhole to extract an exponentially growing set of
   elements `u_eps in K_j^*` with `u_eps * conj(u_eps) = 1`.
3. **Planar projection (Lemma 2.1).** Embed `O_{K_j}` into `C^{f_j}` via
   the Minkowski map, intersect with a polydisc window, and project to
   one complex coordinate. The norm-one elements become unit translations
   in the plane, giving the required `n^(1 + delta)` lower bound.

## Existence vs. constructivity

The infinite tower in step 1 is supplied by:

- **Golod-Shafarevich theorem (1964, 1965)** -- a finite pro-`p` group
  with `d` generators and `r` relations satisfying `r <= d^2 / 4` is
  infinite.
- **Shafarevich's relation-rank estimate** for unramified pro-`p` Galois
  groups of totally real fields.
- **Hajir-Maire-Ramakrishna** technique for cutting out splitting
  conditions while preserving Golod-Shafarevich admissibility
  (Proposition 2.3 of the remarks PDF).

These results prove **existence** of the tower; they do not produce an
explicit closed-form description of `L_j` for `j >= 2`. This is a
fundamental property of the proof: no finite computation can exhibit the
entire infinite tower. See `docs/ARCHITECTURE.md` for what this means
for the scope of this artifact.
