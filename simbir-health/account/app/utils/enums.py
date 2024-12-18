from enum import Enum


class Role(str, Enum):
    INACTIVE = 'inactive'
    USER = 'user'
    DOCTOR = 'doctor'
    ADMIN = 'admin'
    MANAGER = 'manager'
