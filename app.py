import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_mail import Mail, Message
from flask_cors import CORS
import logging

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app, resources={r"/api/*": {"origins": "*"}})
logging.basicConfig(level=logging.INFO)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')

mail = Mail(app)

# --- Routes ---

@app.route('/')
def home():
    return render_template('portfolio.html')

@app.route('/download-cv')
def download_cv():
    try:
        return send_from_directory(
            app.static_folder, 
            'Cv_final_best.pdf', 
            as_attachment=True
        )
    except FileNotFoundError:
        app.logger.error("CV file not found in the static folder.")
        return "Error: CV file not found on the server.", 404

# --- !! NEW DEBUGGING ROUTE !! ---
# This route will help us see the file structure on the Render server.
# After you solve the CV issue, you can remove this entire function.
@app.route('/debug-static')
def debug_static_files():
    """Lists the contents of the project's root and static directories."""
    try:
        # Get the root path of the project on the server
        root_path = os.path.abspath(os.path.dirname(__file__))
        root_contents = os.listdir(root_path)
        
        # Get the path to the static folder
        static_path = os.path.join(root_path, 'static')
        static_contents = "Static folder not found."
        
        if os.path.exists(static_path):
            static_contents = os.listdir(static_path)

        # Format the output to be readable in a browser
        response_html = f"""
        <h1>Server File Debugger</h1>
        <h2>Project Root Directory Contents:</h2>
        <p>Path: {root_path}</p>
        <pre>{root_contents}</pre>
        <hr>
        <h2>'static' Directory Contents:</h2>
        <p>Path: {static_path}</p>
        <pre>{static_contents}</pre>
        """
        return response_html
    except Exception as e:
        return f"An error occurred while debugging: {e}"


@app.route('/api/contact', methods=['POST'])
def contact():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request: No data received'}), 400

    name = data.get('name')
    email = data.get('email')
    message_body = data.get('message')
    
    mail_recipient = os.environ.get('MAIL_RECIPIENT')

    if not all([name, email, message_body]):
        app.logger.error("Email failed: Missing form data.")
        return jsonify({'error': 'Please fill out all fields.'}), 400

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
    app.run(host='0.0.0.0', port=5000, debug=True)

