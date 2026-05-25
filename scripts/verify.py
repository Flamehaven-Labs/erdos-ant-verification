"""Thin shim that delegates to ``erdos_ant.verify.main``.

The verification logic itself lives in ``src/erdos_ant/verify.py`` so it
is reachable as the console script ``erdos-ant-verify`` and via
``python -m erdos_ant.verify``. This script remains as a convenience for
users who prefer ``python scripts/verify.py`` from a clean checkout.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Allow running from a clean checkout (before pip install -e .).
_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from erdos_ant.verify import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
