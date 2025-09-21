Deep Sengupta - Full-Stack Portfolio Website
This repository contains the complete source code for a personal portfolio website. The frontend is built with HTML, Tailwind CSS, and vanilla JavaScript. The backend is a REST API built with Python and Flask to handle contact form submissions by sending emails.

Project Structure
portfolio-project/
│
├── app.py              # The Flask backend application
├── templates/
│   └── portfolio.html  # The main HTML file for the frontend
├── static/
│   └── Cv_final_best.pdf # Place your CV file here
├── requirements.txt    # Python dependencies for the backend
└── README.md           # This file

How to Make It Your Own
1. Add Your CV
Place your CV file (e.g., Cv_final_best.pdf) inside the static folder. The "Download CV" button is already configured to link to this file.

2. Update Project and Certificate Links
In the portfolio.html file, find the projects and certificates arrays in the <script> section at the bottom. Replace the # placeholders with direct URLs to your GitHub repositories, live demos, or certificate verification pages.

Backend Email Setup (Crucial for Contact Form)
The backend is configured to send you an email whenever someone submits the contact form. To make this work, you need to provide your email credentials securely using environment variables.

1. Use a Gmail "App Password" (Recommended)
For security, do not use your main Gmail password. Instead, generate an "App Password".

Go to your Google Account settings: myaccount.google.com

Navigate to Security.

Ensure 2-Step Verification is turned ON. You cannot create App Passwords without it.

In the "Signing in to Google" section, click on App passwords.

Select "Mail" for the app and "Other (Custom name)" for the device. Name it something like "Portfolio Website".

Google will generate a 16-character password. Copy this password immediately. This is what you will use for EMAIL_PASS.

2. Set Environment Variables
Before running the server, you need to set the following environment variables.

On Windows (Command Prompt):

set EMAIL_USER=your-email@gmail.com
set EMAIL_PASS=your-16-character-app-password
set MAIL_RECIPIENT=your-email@gmail.com

On macOS/Linux:

export EMAIL_USER="your-email@gmail.com"
export EMAIL_PASS="your-16-character-app-password"
export MAIL_RECIPIENT="your-email@gmail.com"

Note: MAIL_RECIPIENT is the email address where you want to receive the contact form messages.

Local Development
1. Create Project Structure
Create the folders and files as shown in the "Project Structure" section above.

2. Set Up Virtual Environment
cd portfolio-project
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Set Environment Variables
Follow the steps in the "Backend Email Setup" section to set your email credentials.

5. Run the Backend Server
flask run

The server will start on http://127.0.0.1:5000. Open this URL in your browser to see your portfolio. The contact form is now fully functional and will send emails to you.