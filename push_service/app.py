from flask import Flask, request, jsonify

app = Flask(__name__)

class PushNotificationSender:
    def send(self, recipient, message):
        try:
            print(f"Sending push notification to {recipient}: {message}")
            return True
        except Exception as e:
            print(f"Failed to send push notification: {e}")
            return False

@app.route("/send_push", methods=["POST"])
def send_push():
    data = request.json
    push_sender = PushNotificationSender()
    success = push_sender.send(data["recipient"], data["message"])

    if success:
        return jsonify({"status": "Push notification sent successfully!"}), 200
    return jsonify({"status": "Failed to send push notification"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
