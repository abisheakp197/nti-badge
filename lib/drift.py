"""Score drift detection.


Compares the new cert's score to the previous cert for the same repo.
Triggers alerts on regressions.
"""




def compute_drift(previous: dict, current: dict) -> dict:
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




def is_significant_regression(drift: dict, threshold: int = 10) -> bool:
    return drift["direction"] == "regressed" and abs(drift["delta"]) >= threshold
