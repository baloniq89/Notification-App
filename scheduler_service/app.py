import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../shared'))

from flask import Flask, request, jsonify
from shared.database import Database
import requests

app = Flask(__name__)

class NotificationManager:
    def __init__(self):
        self.db = Database()

    def add_notification(self, user_id, channel, recipient, message):
        query = """
            INSERT INTO notifications (user_id, channel, recipient, message, sent)
            VALUES (%s, %s, %s, %s, FALSE)
            RETURNING id, user_id, channel, recipient, message, sent
        """
        return self.db.execute_and_fetchone(query, (user_id, channel, recipient, message))

    def fetch_pending_notifications(self):
        query = "SELECT * FROM notifications WHERE sent = FALSE"
        return self.db.fetch_all(query)

    def mark_as_sent(self, notification_id):
        query = "UPDATE notifications SET sent = TRUE WHERE id = %s"
        self.db.execute(query, (notification_id,))

class NotificationSender:
    def __init__(self):
        self.email_service_url = "http://email_service:5000/send_email"
        self.push_service_url = "http://push_service:5000/send_push"

    def send(self, notification):
        channel = notification["channel"]
        data = {
            "recipient": notification["recipient"],
            "message": notification["message"]
        }

        if channel == "email":
            response = requests.post(self.email_service_url, json=data)
        elif channel == "push":
            response = requests.post(self.push_service_url, json=data)
        else:
            raise ValueError(f"Unknown channel: {channel}")

        if response.status_code == 200:
            print(f"Notification sent successfully: {notification}")
            return True
        else:
            print(f"Failed to send notification: {notification}")
            return False

notification_manager = NotificationManager()

@app.route("/add_notification", methods=["POST"])
def add_notification():
    data = request.json
    notification = notification_manager.add_notification(
        user_id=data["user_id"],
        channel=data["channel"],
        recipient=data["recipient"],
        message=data["message"]
    )
    return jsonify(notification), 200

@app.route("/schedule_notifications", methods=["GET"])
def schedule_notifications():
    notifications = notification_manager.fetch_pending_notifications()
    sender = NotificationSender()

    for notification in notifications:
        try:
            if sender.send(notification):
                notification_manager.mark_as_sent(notification["id"])
        except Exception as e:
            print(f"Error processing notification {notification['id']}: {e}")

    return jsonify({"status": "Notifications processed"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
