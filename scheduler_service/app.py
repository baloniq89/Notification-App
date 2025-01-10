import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../shared'))

from flask import Flask, jsonify
from shared.database import Database
import requests

app = Flask(__name__)

class NotificationManager:
    def __init__(self):
        self.db = Database()

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

@app.route("/schedule_notifications", methods=["GET"])
def schedule_notifications():
    manager = NotificationManager()
    sender = NotificationSender()
    notifications = manager.fetch_pending_notifications()

    for notification in notifications:
        try:
            if sender.send(notification):
                manager.mark_as_sent(notification["id"])
        except Exception as e:
            print(f"Error processing notification {notification}: {e}")

    return jsonify({"status": "Notifications processed", "notifications": notifications}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
