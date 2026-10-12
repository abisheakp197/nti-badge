"""Score drift detection re-exported from nti_badge."""
from nti_badge.drift import (
    compute_drift,
    is_significant_regression,
)

__all__ = [
    "compute_drift",
    "is_significant_regression",
]
