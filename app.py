from flask import Flask, render_template, request, jsonify
import psycopg2
import os
import threading
import webbrowser
from flask_mail import Mail, Message

app = Flask(__name__)

# -------------------- DATABASE SETUP -------------------- #
DATABASE_URL = os.getenv("DATABASE_URL", "")

def init_db():
    """Create contacts table if it doesn't exist."""
    if not DATABASE_URL:
        print("⚠️ DATABASE_URL not found! Make sure it's set in Render environment variables.")
        return
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL
            )
        ''')
        conn.commit()
        cur.close()
        conn.close()
        print("✅ Database initialized successfully.")
    except Exception as e:
        print(f"❌ Database initialization error: {e}")

# -------------------- EMAIL (Flask-Mail) SETUP -------------------- #
# Set these values in Render → Environment Variables (do NOT hardcode)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  # Your Gmail address
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  # Your App Password (not normal Gmail password)
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

mail = Mail(app)

# -------------------- ROUTES -------------------- #
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    """Handle contact form submission: save + send email."""
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No data received"}), 400

    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    if not all([name, email, message]):
        return jsonify({"status": "error", "message": "Missing fields"}), 400

    # ---------- Save to Database ----------
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)",
            (name, email, message)
        )
        conn.commit()
        cur.close()
        conn.close()
        print(f"📩 New contact saved: {name} ({email})")
    except Exception as e:
        print(f"❌ Error saving contact: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

    # ---------- Send Email Notification ----------
    try:
        msg = Message(
            subject=f"New Contact Form Submission from {name}",
            recipients=[os.getenv('ADMIN_EMAIL', app.config['MAIL_USERNAME'])],  # Who receives the message
            body=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        )
        mail.send(msg)
        print("✅ Email notification sent successfully.")
    except Exception as e:
        print(f"❌ Email sending error: {e}")

    return jsonify({"status": "success", "message": "Contact saved and email sent!"})

@app.route('/view_contacts')
def view_contacts():
    """Optional route to view saved contacts."""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT * FROM contacts ORDER BY id DESC")
        contacts = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(contacts)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# -------------------- AUTO OPEN BROWSER (Local Only) -------------------- #
def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

# -------------------- MAIN ENTRY POINT -------------------- #
if __name__ == '__main__':
    init_db()
    threading.Timer(1, open_browser).start()
    app.run(debug=True)
