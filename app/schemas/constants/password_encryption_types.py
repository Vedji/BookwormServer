from enum import Enum


class PasswordEncryptionTypes(str, Enum):
    NONE = "none"
    SHA256 = "sha256"
    BCRYPT = "bcrypt"
