from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_mail import Mail, Message
import logging
import os

# Initialize the Flask application
app = Flask(__name__, static_folder='static', template_folder='templates')

# --- Email Configuration ---
# IMPORTANT: Use environment variables to keep your credentials secure.
# Do not hardcode your email and password in the code.
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

# Initialize Flask-Mail
mail = Mail(app)

# Enable Cross-Origin Resource Sharing (CORS)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    """Serves the main portfolio HTML file."""
    return render_template('portfolio.html')

@app.route('/api/contact', methods=['POST'])
def handle_contact_form():
    """
    API endpoint to handle contact form submissions.
    It receives form data, sends an email, and returns a JSON response.
    """
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "Invalid request"}), 400

    name = data.get('name')
    email = data.get('email')
    message_body = data.get('message')

    if not all([name, email, message_body]):
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    # Create the email message
    subject = f"New Contact Form Message from {name}"
    sender = app.config['MAIL_USERNAME']
    # The recipient should be your personal email address, where you want to receive notifications.
    # It's good practice to also load this from an environment variable.
    recipient = os.environ.get('MAIL_RECIPIENT', app.config['MAIL_USERNAME'])

    msg = Message(subject, sender=sender, recipients=[recipient])
    msg.body = f"""
    You have received a new message from your portfolio contact form.

    Name: {name}
    Email: {email}

    Message:
    {message_body}
    """

    try:
        # Send the email
        mail.send(msg)
        app.logger.info(f"Email sent successfully from {email}")
        return jsonify({"status": "success", "message": "Message sent successfully! Thank you for reaching out."}), 200
    except Exception as e:
        app.logger.error(f"Failed to send email: {e}")
        return jsonify({"status": "error", "message": "Sorry, there was an error sending your message. Please try again later."}), 500

if __name__ == '__main__':
    app.run(debug=True)

