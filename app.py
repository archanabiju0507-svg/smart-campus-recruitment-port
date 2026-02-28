import os
from flask import Flask, render_template, jsonify, request
import sqlite3
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration for file uploads
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Limit file size to 2MB
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    # Updated students table to include 'photo'
    conn.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            sgpa REAL,
            cgpa REAL,
            academic_performance TEXT,
            skills TEXT,
            external_events TEXT,
            internships TEXT,
            photo TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/submit_profile', methods=['POST'])
def submit_profile():
    # When uploading files, we use request.form instead of request.json
    try:
        name = request.form.get('name')
        sgpa = request.form.get('sgpa')
        cgpa = request.form.get('cgpa')
        performance = request.form.get('academic_performance')
        skills = request.form.get('skills')
        events = request.form.get('external_events')
        internships = request.form.get('internships')

        # Handle Photo Upload
        photo_name = None
        if 'photo' in request.files:
            file = request.files['photo']
            if file.filename != '':
                photo_name = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_name))

        conn = get_db_connection()
        conn.execute('''
            INSERT INTO students (name, sgpa, cgpa, academic_performance, skills, external_events, internships, photo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, sgpa, cgpa, performance, skills, events, internships, photo_name))
        conn.commit()
        conn.close()
        
        return jsonify({"status": "success", "message": "Profile and Photo saved successfully!"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    init_db()
    app.run(debug=True)