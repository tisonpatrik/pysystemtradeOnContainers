from enum import Enum

# Sample StatusEnum definition
class StatusEnum(str, Enum):
    active = "active"
    inactive = "inactive"
    deleted = "deleted"