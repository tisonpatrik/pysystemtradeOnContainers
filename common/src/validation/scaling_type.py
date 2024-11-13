from enum import Enum


class ScalingType(str, Enum):
    none = "none"
    fixed = "fixed"
    estimated = "estimated"
