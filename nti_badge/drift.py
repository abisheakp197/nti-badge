"""Score drift detection.

Compares the new cert's score to the previous cert for the same repo.
Triggers alerts on regressions.
"""

from typing import Any


def compute_drift(previous: dict[str, Any] | None, current: dict[str, Any]) -> dict[str, Any]:
    prev_score = previous.get("score", 0) if previous else None
    curr_score = current.get("score", 0)
    if prev_score is None:
        return {"direction": "first_scan", "delta": 0, "previous": None, "current": curr_score}
    delta = curr_score - prev_score
    if delta > 0:
        direction = "improved"
    elif delta < 0:
        direction = "regressed"
    else:
        direction = "stable"
    return {
        "direction": direction,
        "delta": delta,
        "previous": prev_score,
        "current": curr_score,
    }


def is_significant_regression(drift: dict[str, Any], threshold: int = 10) -> bool:
    direction = drift.get("direction")
    delta = drift.get("delta", 0)
    return direction == "regressed" and abs(int(delta)) >= threshold
