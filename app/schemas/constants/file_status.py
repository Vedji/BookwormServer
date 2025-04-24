from enum import Enum


class FileStatus(str, Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    DELETED = "deleted"
    LOCAL = "local"
