from dataclasses import dataclass


@dataclass
class UserPreferences:
    timezone: str


@dataclass
class User:
    id: str
    username: str
    password: str
    roles: list
    preferences: UserPreferences
    created_ts: float
    active: bool = True
