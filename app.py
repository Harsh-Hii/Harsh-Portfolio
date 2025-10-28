from flask import Flask, render_template, request, jsonify
import json
import os
import threading
import webbrowser

app = Flask(__name__)

# Path for saving JSON file
DATA_FILE = "contact_data.json"

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission
@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    data = request.get_json()  # Get JSON data from fetch request
    if not data:
        return jsonify({"status": "error", "message": "No data received"}), 400
    
    # Check if file exists
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                contacts = json.load(f)
            except json.JSONDecodeError:
                contacts = []
    else:
        contacts = []
    
    contacts.append(data)
    
    # Save updated data
    with open(DATA_FILE, "w") as f:
        json.dump(contacts, f, indent=4)
    
    return jsonify({"status": "success", "message": "Contact saved!"})
    

# Function to open browser automatically
def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == '__main__':
    threading.Timer(1, open_browser).start()
    app.run(debug=True)

