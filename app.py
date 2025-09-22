import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_mail import Mail, Message
from flask_cors import CORS  # Import CORS
import logging

# This structure assumes your 'portfolio.html' is in a 'templates' folder
# and your CV is in a 'static' folder.
app = Flask(__name__, template_folder='templates', static_folder='static')

# ** THE FIX for "failed to fetch" **
# This allows your frontend (even on localhost) to make requests to your backend.
CORS(app, resources={r"/api/*": {"origins": "*"}})

logging.basicConfig(level=logging.INFO)

# --- Configuration ---
# Use environment variables for sensitive data
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')

mail = Mail(app)

# --- Routes ---

@app.route('/')
def home():
    """Serves the main portfolio page from the 'templates' folder."""
    return render_template('portfolio.html')

@app.route('/download-cv')
def download_cv():
    """
    Handles the request to download the CV.
    Looks for the file in the 'static' folder.
    """
    try:
        # This tells Flask to find 'Cv_final_best.pdf' inside the 'static' folder
        return send_from_directory(
            app.static_folder, 
            'Cv_final_best.pdf', 
            as_attachment=True
        )
    except FileNotFoundError:
        app.logger.error("CV file not found in the static folder.")
        return "Error: CV file not found on the server.", 404

@app.route('/api/contact', methods=['POST'])
def contact():
    """Handles the contact form submission via AJAX."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request: No data received'}), 400

    name = data.get('name')
    email = data.get('email')
    message_body = data.get('message')
    
    mail_recipient = os.environ.get('MAIL_RECIPIENT')

    if not all([name, email, message_body]):
        app.logger.error("Email failed: Missing form data (name, email, or message).")
        return jsonify({'error': 'Please fill out all fields.'}), 400

    # Final check for email credentials loaded from environment
    if not app.config['MAIL_USERNAME'] or not app.config['MAIL_PASSWORD'] or not mail_recipient:
        app.logger.error("CRITICAL: Server email environment variables are not set.")
        return jsonify({'error': 'Server configuration error.'}), 500

    msg = Message(
        subject=f"New Portfolio Message from {name}",
        sender=('Portfolio Website', app.config['MAIL_USERNAME']),
        recipients=[mail_recipient]
    )
    msg.body = f"You have a new message from:\n\nName: {name}\nEmail: {email}\n\nMessage:\n{message_body}"

    try:
        mail.send(msg)
        app.logger.info(f"Email sent successfully from {email}")
        return jsonify({'message': 'Message sent successfully!'}), 200
    except Exception as e:
        app.logger.error(f"Failed to send email: {e}")
        return jsonify({'error': 'An error occurred while sending the email.'}), 500

if __name__ == '__main__':
    # Use 0.0.0.0 to make it accessible on your network
    app.run(host='0.0.0.0', port=5000, debug=True)

