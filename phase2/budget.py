"""The only sanctioned way to advance state during Phase 2 search.

CONTRACT.md's cost unit rule: 1 transition evaluation = 1 `apply()` call,
counted identically whether it happens during tree expansion or rollout.
Every algorithm (Random, Beam-Naive, Beam-Diverse, MCTS) must call
`Budget.step()` to get a successor state -- never `engine.apply()`
directly -- so counting can't drift between algorithms by accident (the
exact risk flagged for MCTS: rollout steps undercounted relative to tree
expansion would hand it an uncosted advantage). `step()` also raises once
the budget is spent, so a caller can't silently keep going past the limit.
"""
from __future__ import annotations

from dataclasses import dataclass

from engine import Action, GameData, GameState, apply


class BudgetExhausted(Exception):
    pass


@dataclass
class Budget:
    limit: int
    used: int = 0

    def remaining(self) -> bool:
        return self.used < self.limit

    def step(self, data: GameData, state: GameState, action: Action) -> GameState:
        if self.used >= self.limit:
            raise BudgetExhausted()
        self.used += 1
        return apply(data, state, action)
