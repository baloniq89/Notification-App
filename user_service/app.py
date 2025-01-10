from flask import Flask, request, jsonify
from shared.database import Database

app = Flask(__name__)

class UserManager:
    def __init__(self):
        self.db = Database()

    def add_user(self, name, email, device_id):
        query = """
            INSERT INTO users (name, email, device_id)
            VALUES (%s, %s, %s)
            RETURNING id, name, email, device_id
        """
        return self.db.execute_and_fetchone(query, (name, email, device_id))

    def get_user(self, user_id):
        query = "SELECT id, name, email, device_id FROM users WHERE id = %s"
        return self.db.execute_and_fetchone(query, (user_id,))

    def get_all_users(self):
        query = "SELECT id, name, email, device_id FROM users"
        return self.db.execute_and_fetchall(query)

user_manager = UserManager()

@app.route("/users", methods=["POST"])
def add_user():
    data = request.json
    user = user_manager.add_user(data["name"], data["email"], data["device_id"])
    return jsonify({"message": "User added", "user": user}), 201

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = user_manager.get_user(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404

@app.route("/users", methods=["GET"])
def get_all_users():
    users = user_manager.get_all_users()
    return jsonify(users), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
