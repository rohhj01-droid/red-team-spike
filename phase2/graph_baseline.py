"""Static Conversion-Cycle Baseline.

Deterministic, no search budget in the sense the other algorithms use one.
Models every SINGLE-INPUT transformation (buy, sell, craft, dismantle) as
a directed edge with weight -log(rate), and finds a positive-value cycle
via Bellman-Ford negative-cycle detection -- the standard currency-
arbitrage trick (a cycle whose rate PRODUCT > 1 becomes, after -log, a
cycle whose weight SUM < 0).

Scope is deliberately narrow (CONTRACT.md): a case is either fully
`is_supported` (every recipe has exactly one input item AND every
dismantle rule has exactly one output item type) or it is reported
entirely N/A -- never partially solved. Multi-input recipes are a
hypergraph problem this baseline does not attempt.
"""
from __future__ import annotations

import math
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple

from engine import Action, GameData
from oracle import is_exploit_found

GOLD = "__GOLD__"


@dataclass
class GraphResult:
    supported: bool
    found: bool
    path: Optional[List[Action]]
    wall_seconds: float
    nodes_inspected: int
    edges_inspected: int


def is_supported(data: GameData) -> bool:
    for inputs in data.recipes.values():
        if len(inputs) != 1:
            return False
    for outputs in data.dismantle.values():
        if len(outputs) != 1:
            return False
    return True


def _build_edges(data: GameData) -> List[Tuple[str, str, float, Action]]:
    edges: List[Tuple[str, str, float, Action]] = []
    for item, price in data.shop_buy.items():
        rate = 1.0 / price  # `price` gold buys 1 unit
        edges.append((GOLD, item, -math.log(rate), Action("buy", item)))
    for item, price in data.shop_sell.items():
        rate = float(price)  # 1 unit sells for `price` gold
        edges.append((item, GOLD, -math.log(rate), Action("sell", item)))
    for output, inputs in data.recipes.items():
        (item, qty), = inputs.items()
        rate = 1.0 / qty  # `qty` units of item make 1 unit of output
        edges.append((item, output, -math.log(rate), Action("craft", output)))
    for target, outputs in data.dismantle.items():
        (item, qty), = outputs.items()
        rate = float(qty)  # 1 unit of target makes `qty` units of item
        edges.append((target, item, -math.log(rate), Action("dismantle", target)))
    return edges


def find_positive_cycle(data: GameData) -> GraphResult:
    t0 = time.perf_counter()
    if not is_supported(data):
        return GraphResult(supported=False, found=False, path=None, wall_seconds=time.perf_counter() - t0, nodes_inspected=0, edges_inspected=0)

    edges = _build_edges(data)
    nodes: Set[str] = {GOLD}
    for u, v, _, _ in edges:
        nodes.add(u)
        nodes.add(v)

    dist: Dict[str, float] = {n: 0.0 for n in nodes}  # implicit zero-weight virtual source
    pred: Dict[str, Optional[Tuple[str, Action]]] = {n: None for n in nodes}

    x: Optional[str] = None
    for _ in range(len(nodes)):
        x = None
        for u, v, w, a in edges:
            if dist[u] + w < dist[v] - 1e-12:
                dist[v] = dist[u] + w
                pred[v] = (u, a)
                x = v

    wall = time.perf_counter() - t0
    if x is None:
        return GraphResult(supported=True, found=False, path=None, wall_seconds=wall, nodes_inspected=len(nodes), edges_inspected=len(edges))

    # x is guaranteed on (or reachable-into) a negative cycle; walk back
    # len(nodes) times to land strictly inside it.
    y = x
    for _ in range(len(nodes)):
        prev, _ = pred[y]
        y = prev

    # Collect (from_node, action) walking backward, then reverse to forward order.
    segment: List[Tuple[str, Action]] = []
    cur = y
    while True:
        prev, action = pred[cur]
        segment.append((prev, action))
        cur = prev
        if cur == y:
            break
    segment.reverse()

    # Rotate so the sequence starts right after leaving GOLD (the only
    # sensible starting point -- you always begin with money, not items).
    from_nodes = [n for n, _ in segment]
    if GOLD in from_nodes:
        i = from_nodes.index(GOLD)
        segment = segment[i:] + segment[:i]
    cycle_actions = [a for _, a in segment]

    # The graph model treats conversion rates as continuous; it says
    # nothing about whether a single unit's worth of each step is legal
    # to execute back to back (a craft recipe needing 2+ of its single
    # input, e.g., isn't satisfiable by one prior buy). Validate against
    # the real oracle rather than claim a path that would fail if run.
    if is_exploit_found(data, cycle_actions):
        return GraphResult(supported=True, found=True, path=cycle_actions, wall_seconds=wall, nodes_inspected=len(nodes), edges_inspected=len(edges))
    return GraphResult(
        supported=True, found=True, path=None,
        wall_seconds=wall, nodes_inspected=len(nodes), edges_inspected=len(edges),
    )  # a profitable rate cycle exists, but this baseline doesn't attempt
       # batch-quantity scaling to turn it into a literal legal sequence
