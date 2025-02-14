import time
from app.models.user import User, UserPreferences
from datetime import datetime


def parse_roles(user_data):
    roles = []
    if user_data.get("is_user_admin"):
        roles.append("admin")
    if user_data.get("is_user_manager"):
        roles.append("manager")
    if user_data.get("is_user_tester"):
        roles.append("tester")
    return roles


def convert_to_timestamp(date_str):
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        return time.mktime(dt.timetuple())
    except ValueError as e:
        print("Error converting date '%s': %s", date_str, e)
        return None


def parse_user(user_data: dict) -> User:

    return User(
        id=user_data.get("_id"),
        username=user_data.get("user"),
        password=user_data.get("password"),
        roles=parse_roles(user_data),
        preferences=UserPreferences(timezone=user_data.get("user_timezone", "UTC")),
        created_ts=user_data.get("created_at"),
        active=user_data.get("is_user_active", True),
    )
