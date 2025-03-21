from flask import Blueprint, request, jsonify
from flask_mail import Mail, Message


# Create a Flask-Mail instance (to be configured later)
mail = Mail()

# Create a blueprint for email routes
email_bp = Blueprint('email_bp', __name__)

def configure_mail(app):
# Gmail SMTP Configuration
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False  # Using TLS instead
    app.config['MAIL_USERNAME'] = 'p2682455@gmail.com'  # Your Gmail address
    app.config['MAIL_PASSWORD'] = 'bmfs wzio ttnl cxnt'  # 16-character App Password from Google
    app.config['MAIL_DEFAULT_SENDER'] = 'p2682455@gmail.com'  # Sender's email
    mail.init_app(app)



@email_bp.route('/send-email', methods=['POST'])
def send_email():
    """Endpoint to send emails."""
    try:
        data = request.get_json()
        required_fields = ['subject', 'message', 'from_email']

        # Validate input data
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"message": f"Missing {field} field."}), 400

        # Hardcoded email to receive messages
        to_email = 'p2682455@gmail.com'  # Replace with your actual email address

        # Create and send the email
        msg = Message(
            subject=data['subject'],
            recipients=[to_email],  # Your hardcoded email
            body=data['message'],
            reply_to=data['from_email']  # User's email for replies
        )

        mail.send(msg)
        return jsonify({"message": "Email sent successfully!"}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Failed to send email."}), 500