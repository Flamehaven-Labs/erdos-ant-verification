"""erdos_ant: independent verification artifact for the OpenAI/Sawin disproof
of the Erdos planar unit-distance conjecture.

This package provides a TOE-free, reproducible Python implementation of the
finite, checkable parts of:

  - "Planar Point Sets with Many Unit Distances", OpenAI, 2026
    https://cdn.openai.com/pdf/74c24085-19b0-4534-9c90-465b8e29ad73/unit-distance-proof.pdf
  - "Remarks on the Disproof of the Unit Distance Conjecture",
    Alon, Bloom, Gowers, Litt, Sawin, Shankar, Tsimerman, Wang, Wood, 2026
    https://cdn.openai.com/pdf/74c24085-19b0-4534-9c90-465b8e29ad73/unit-distance-remarks.pdf

It does NOT contain a new proof, a new construction, or any peer-reviewed
mathematical result. See README.md for the exact scope and limits.
"""

from __future__ import annotations

__version__ = "0.1.0"
