"""The only sanctioned way to advance WorldState during search. Ported
from phase3/budget.py (C1), import repointed to phase3/c2/engine.py --
C1 is sealed evidence, C2 doesn't import from it.
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
