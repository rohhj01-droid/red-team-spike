"""The only sanctioned way to advance WorldState during search. Ported
from phase3/c3/budget.py, import repointed to phase3/c4/engine.py -- C1,
C2, and C3 are sealed evidence, C4 doesn't import from any of them.
"""
from __future__ import annotations

from dataclasses import dataclass

from engine import Action, WorldState, apply


class BudgetExhausted(Exception):
    pass


@dataclass
class Budget:
    limit: int
    used: int = 0

    def remaining(self) -> bool:
        return self.used < self.limit

    def step(self, world: WorldState, action: Action) -> WorldState:
        if self.used >= self.limit:
            raise BudgetExhausted()
        self.used += 1
        return apply(world, action)
