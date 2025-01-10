from flask import Flask, request, jsonify

app = Flask(__name__)

class EmailSender:
    def send(self, recipient, message):
        try:
            print(f"Sending email to {recipient}: {message}")
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False

@app.route("/send_email", methods=["POST"])
def send_email():
    data = request.json
    email_sender = EmailSender()
    success = email_sender.send(data["recipient"], data["message"])

    if success:
        return jsonify({"status": "Email sent successfully!"}), 200
    return jsonify({"status": "Failed to send email"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)