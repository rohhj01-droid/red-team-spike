"""Paths shared by the Run 2 tools, and the one sys.path insertion that makes the
exploratory study's tools importable (they are imported, never copied or edited:
preregistration design Section 6)."""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RUN2 = os.path.abspath(os.path.join(HERE, ".."))
REPO = os.path.abspath(os.path.join(RUN2, "..", ".."))
EXPLORATORY_TOOLS = os.path.join(REPO, "phase3_5", "exploratory", "tools")
TARGET = os.path.join(RUN2, "target")


def use_exploratory_tools() -> None:
    """Put the exploratory tools first on sys.path so `import common, inventory, universe, snapshot` resolve."""
    if EXPLORATORY_TOOLS not in sys.path:
        sys.path.insert(0, EXPLORATORY_TOOLS)
