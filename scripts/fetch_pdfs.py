"""Download the OpenAI unit-distance PDFs and extract text for offline audit.

The PDFs are NOT included in this repository (copyright). This script
fetches them from the OpenAI CDN and produces plain-text extractions next
to them under `docs/pdf_extracts/` (also gitignored). Use the extractions
as a local audit trail when reviewing the numerical reproduction in
`scripts/verify.py`.

Requires: pypdf (in the [dev] extra).
"""

from __future__ import annotations

import sys
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = REPO_ROOT / "docs" / "pdf_extracts"

PDFS = {
    "unit_distance_proof.pdf": (
        "https://cdn.openai.com/pdf/74c24085-19b0-4534-9c90-465b8e29ad73/"
        "unit-distance-proof.pdf"
    ),
    "unit_distance_remarks.pdf": (
        "https://cdn.openai.com/pdf/74c24085-19b0-4534-9c90-465b8e29ad73/"
        "unit-distance-remarks.pdf"
    ),
}


def fetch(url: str, dest: Path) -> None:
    print(f"Fetching {url}")
    with urllib.request.urlopen(url, timeout=30) as resp:
        dest.write_bytes(resp.read())
    print(f"  -> {dest} ({dest.stat().st_size} bytes)")


def extract_text(pdf_path: Path) -> Path:
    try:
        import pypdf
    except ImportError:
        sys.exit(
            "pypdf is not installed. Install dev extras: "
            "pip install -e '.[dev]'"
        )
    reader = pypdf.PdfReader(str(pdf_path))
    text_path = pdf_path.with_suffix(".txt")
    text_path.write_text(
        "\n\n=== PAGE BREAK ===\n\n".join(p.extract_text() for p in reader.pages),
        encoding="utf-8",
    )
    print(f"  extracted: {text_path} ({len(reader.pages)} pages)")
    return text_path


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for filename, url in PDFS.items():
        dest = OUT_DIR / filename
        fetch(url, dest)
        extract_text(dest)
    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
