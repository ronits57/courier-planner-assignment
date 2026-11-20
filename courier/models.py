"""Data design for the Mini-Courier Planner (Phase 1)."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Parcel:
    """A single parcel to be delivered.

    id        : unique parcel identifier, e.g. "P01"
    dest      : delivery point (a node name in the road graph)
    weight    : weight in kg (integer, used as knapsack weight)
    priority  : business value / priority score 1-10 (used as knapsack value)
    deadline  : delivery deadline in minutes after dispatch
    """
    id: str
    dest: str
    weight: int
    priority: int
    deadline: int
