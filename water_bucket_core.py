"""
Water bucket puzzle — shared logic for reference script and FastAPI web app.

Three buckets (8 L, 5 L, 3 L). Actions: fill to capacity, empty, pour between buckets.
Win when any bucket holds exactly GOAL liters.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Literal

GOAL = 4
BUCKET_IDS: tuple[str, ...] = ("8", "5", "3")
BUCKET_CAPACITY: dict[str, int] = {"8": 8, "5": 5, "3": 3}

Action = Literal["fill", "empty", "pour"]
BucketId = Literal["8", "5", "3"]


def initial_state() -> dict[str, Any]:
    return {"water": {bid: 0 for bid in BUCKET_IDS}, "steps": 0}


def validate_bucket(bucket_id: str) -> None:
    if bucket_id not in BUCKET_CAPACITY:
        raise ValueError("Invalid bucket.")


def check_win(water: dict[str, int]) -> bool:
    return any(amount == GOAL for amount in water.values())


def apply_fill(water: dict[str, int], source: str) -> dict[str, int]:
    validate_bucket(source)
    next_water = dict(water)
    next_water[source] = BUCKET_CAPACITY[source]
    return next_water


def apply_empty(water: dict[str, int], source: str) -> dict[str, int]:
    validate_bucket(source)
    next_water = dict(water)
    next_water[source] = 0
    return next_water


def apply_pour(water: dict[str, int], source: str, dest: str) -> dict[str, int]:
    validate_bucket(source)
    validate_bucket(dest)
    if source == dest:
        raise ValueError("Choose a different bucket to pour into.")

    dst_size = BUCKET_CAPACITY[dest]
    empty_space = dst_size - water[dest]
    in_src = water[source]
    amount = min(empty_space, in_src)

    next_water = dict(water)
    next_water[source] -= amount
    next_water[dest] += amount
    return next_water


def apply_move(
    state: dict[str, Any],
    action: Action,
    source: str,
    dest: str | None = None,
) -> dict[str, Any]:
    """
    Return new state with incremented step count, or raise ValueError on bad input.
    """
    water = state.get("water")
    if not isinstance(water, dict):
        raise ValueError("Invalid game state.")

    steps = int(state.get("steps", 0))

    if action == "fill":
        new_water = apply_fill(water, source)
    elif action == "empty":
        new_water = apply_empty(water, source)
    elif action == "pour":
        if dest is None:
            raise ValueError("Pour requires a destination bucket.")
        new_water = apply_pour(water, source, dest)
    else:
        raise ValueError("Unknown action.")

    result = {"water": new_water, "steps": steps + 1}
    result["won"] = check_win(new_water)
    return result


def state_for_client(state: dict[str, Any]) -> dict[str, Any]:
    """JSON-friendly snapshot including win flag and goal."""
    water = state["water"]
    return {
        "water": deepcopy(water),
        "steps": state["steps"],
        "goal": GOAL,
        "capacities": deepcopy(BUCKET_CAPACITY),
        "won": check_win(water),
    }
