import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../shared'))

from flask import Flask, request, jsonify
import requests
from shared.database import Database

app = Flask(__name__)

class User:
    def __init__(self, user_id, name, email, device_id):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.device_id = device_id

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "device_id": self.device_id
        }

class UserManager:
    def __init__(self):
        self.db = Database()

    def get_user(self, user_id):
        # Pobiera użytkownika z bazy danych na podstawie ID
        query = "SELECT id AS user_id, name, email, device_id FROM users WHERE id = %s"
        user_data = self.db.execute_and_fetchone(query, (user_id,))
        if user_data:
            return User(**user_data)
        return None

    def get_all_users(self):
        # Pobiera wszystkich użytkowników z bazy danych
        query = "SELECT id AS user_id, name, email, device_id FROM users"
        users = self.db.fetch_all(query)
        return [User(**user).to_dict() for user in users]

user_manager = UserManager()

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = user_manager.get_user(user_id)
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({"error": "User not found"}), 404

@app.route("/users", methods=["GET"])
def get_all_users():
    return jsonify(user_manager.get_all_users()), 200

@app.route("/send_notification", methods=["POST"])
def send_notification():
    data = request.json

    # Walidacja danych wejściowych
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    required_fields = ["user_id", "type", "message"]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    # Pobieramy użytkownika
    user = user_manager.get_user(data["user_id"])
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Przygotowanie powiadomienia
    notification = {
        "user_id": user.user_id,
        "channel": data["type"],
        "recipient": user.email if data["type"] == "email" else user.device_id,
        "message": data["message"]
    }

    # Wysyłamy powiadomienie do Scheduler Service
    try:
        response = requests.post("http://scheduler_service:5000/add_notification", json=notification)
        response.raise_for_status()
    except requests.RequestException as e:
        return jsonify({"error": "Failed to communicate with Scheduler Service", "details": str(e)}), 500

    return jsonify({"message": "Notification sent to scheduler successfully"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
