import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import logging

from datetime import datetime
from pymongo import MongoClient, errors
from scripts.parser import parse_roles
from app.models.user import User, UserPreferences
from scripts.parser import convert_to_timestamp

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def import_users():
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["crud_db"]
        users_collection = db["users"]
    except errors.ConnectionError as e:
        logging.error("Error connecting to MongoDB: %s", e)
        sys.exit(1)

    try:
        with open("data/udata.json", "r") as file:
            data = json.load(file)
    except Exception as e:
        logging.error("Error reading JSON file: %s", e)
        sys.exit(1)

    users_to_insert = []

    for user_data in data.get("users", []):
        required_fields = [
            "user",
            "password",
            "user_timezone",
            "created_at",
            "is_user_active",
        ]
        if not all(key in user_data for key in required_fields):
            logging.warning(
                "Incomplete data for user %s. Skipping.", user_data.get("user", "N/A")
            )
            continue

        created_ts = convert_to_timestamp(user_data["created_at"])
        if created_ts is None:
            logging.warning(
                "Invalid date for user %s. Skipping.", user_data.get("user", "N/A")
            )
            continue

        user_dict = {
            "user": user_data["user"],
            "password": user_data["password"],
            "is_user_admin": user_data["is_user_admin"],
            "is_user_manager": user_data["is_user_manager"],
            "is_user_tester": user_data["is_user_tester"],
            "user_timezone": user_data["user_timezone"],
            "is_user_active": user_data["is_user_active"],
            "created_at": user_data["created_at"],
        }

        users_to_insert.append(user_dict)

    if users_to_insert:
        try:
            result = users_collection.insert_many(users_to_insert)
            logging.info("Inserted %d users.", len(result.inserted_ids))
        except Exception as e:
            logging.error("Error inserting users: %s", e)
    else:
        logging.info("No users to insert.")


if __name__ == "__main__":
    import_users()
