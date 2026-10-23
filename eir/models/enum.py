from enum import Enum, StrEnum


class SessionStatus(str, Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ABANDONED = "abandoned"

class UserRole(StrEnum):
    PATIENT = "patient"
    DOCTOR = "doctor"

