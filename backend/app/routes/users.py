from datetime import datetime
from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from scripts.parser import parse_user

users_bp = Blueprint("users", __name__)

MONGODB_URI = "mongodb://localhost:27017/"
DB_NAME = "crud_db"

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]
users_collection = db["users"]


@users_bp.route("/users", methods=["GET"])
def get_users():
    try:
        users = list(users_collection.find())
        parsed_users = []

        for user in users:
            user["_id"] = str(user["_id"])
            user_obj = parse_user(user)
            user_dict = user_obj.__dict__
            user_dict["preferences"] = user_obj.preferences.__dict__
            parsed_users.append(user_dict)

        return jsonify(parsed_users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@users_bp.route("/users", methods=["POST"])
def add_user():
    try:
        user_data = request.get_json()
        required_fields = ["user", "password", "is_user_active"]
        if not all(key in user_data for key in required_fields):
            return jsonify({"error": "Incomplete data for user."}), 400

        user_data["created_at"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

        result = users_collection.insert_one(user_data)
        user_obj = parse_user(user_data)
        user_dict = user_obj.__dict__
        user_dict["preferences"] = user_obj.preferences.__dict__
        user_dict["id"] = str(result.inserted_id)

        response = {"data": user_dict, "message": "User registered successfully."}
        return jsonify(response), 201

    except Exception as e:
        return (
            jsonify(
                {
                    "error": str(e),
                    "message": "An error occurred while trying to register the user.",
                }
            ),
            500,
        )


@users_bp.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    try:
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if user:
            user["_id"] = str(user["_id"])
            userParsed = parse_user(user)
            return jsonify(userParsed), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@users_bp.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    try:
        updated_data = request.get_json()

        existing_user = users_collection.find_one({"_id": ObjectId(user_id)})
        if not existing_user:
            return jsonify({"error": "User not found"}), 404

        result = users_collection.update_one(
            {"_id": ObjectId(user_id)}, {"$set": updated_data}
        )

        if result.matched_count:
            updated_user = users_collection.find_one({"_id": ObjectId(user_id)})
            updated_user["_id"] = str(updated_user["_id"])

            response = {
                "data": parse_user(updated_user),
                "message": "User updated successfully.",
            }
            return jsonify(response), 200
        else:
            return jsonify({"error": "User not found"}), 404

    except Exception as e:
        return (
            jsonify(
                {
                    "error": str(e),
                    "message": "An error occurred while trying to update the user.",
                }
            ),
            500,
        )


@users_bp.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return jsonify({"error": "User not found"}), 404

        username = user.get("user")

        result = users_collection.delete_one({"_id": ObjectId(user_id)})
        if result.deleted_count:
            return jsonify({"message": f"User ({username}) deleted successfully."}), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
