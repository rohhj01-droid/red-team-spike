"""Frozen at the end of Commit D. See CALIBRATION.md for how each value
was chosen. Do not edit after D.5 -- that is the entire point of this
file existing separately from run_calibration.py.
"""

BUDGET = 100_000
MAX_DEPTH = 36

BEAM_WIDTH = 25          # shared by Beam-Naive and Beam-Diverse
NOVELTY_WEIGHT = 1
NOVELTY_K = 4

MCTS_C = 2 ** 0.5  # sqrt(2) -- not swept; see CALIBRATION.md for why sweeping it is mathematically inert

SEEDS = list(range(10))  # Random and MCTS, per CONTRACT.md
