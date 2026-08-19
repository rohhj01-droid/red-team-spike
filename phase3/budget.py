"""The only sanctioned way to advance WorldState during search. Same
pattern as phase2/budget.py, ported rather than imported -- Phase 2's
apply() takes a `data: GameData` parameter this single-domain engine
doesn't have.
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
