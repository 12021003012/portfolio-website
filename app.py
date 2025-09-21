import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_mail import Mail, Message
import logging

app = Flask(__name__, template_folder='templates', static_folder='static')
logging.basicConfig(level=logging.INFO)

# Configuration for Flask-Mail
# Using port 465 for SSL, which is standard for smtplib
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')

mail = Mail(app)

@app.route('/')
def home():
    """Serves the main portfolio page."""
    return render_template('portfolio.html')

@app.route('/download-cv')
def download_cv():
    """Handles the request to download the CV."""
    try:
        # Serves the file from the 'static' folder
        return send_from_directory(app.static_folder, 'Cv_final_best.pdf', as_attachment=True)
    except FileNotFoundError:
        return "Error: CV file not found on the server.", 404

@app.route('/api/contact', methods=['POST'])
def contact():
    """Handles the contact form submission."""
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    message_body = data.get('message')
    
    mail_recipient = os.environ.get('MAIL_RECIPIENT')

    if not all([name, email, message_body, mail_recipient]):
        return jsonify({'error': 'Missing form data or server configuration'}), 400

    msg = Message(
        subject=f"New Contact Form Message from {name}",
        sender=app.config['MAIL_USERNAME'],
        recipients=[mail_recipient]
    )
    msg.body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message_body}"

    try:
        mail.send(msg)
        app.logger.info(f"Email sent successfully from {email}")
        return jsonify({'message': 'Message sent successfully!'}), 200
    except Exception as e:
        app.logger.error(f"Failed to send email: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

