from flask import Flask, render_template, jsonify, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('DROP TABLE IF EXISTS jobs') # Reset for new column
    conn.execute('''CREATE TABLE jobs 
                 (id INTEGER PRIMARY KEY, title TEXT, company TEXT, 
                  location TEXT, stipend TEXT, min_cgpa REAL)''')
    
    sample_jobs = [
        ('Java Intern', 'Google', 'Bangalore', '₹35,000', 8.5),
        ('SDE Intern', 'Amazon', 'Hyderabad', '₹40,000', 8.0),
        ('Web Developer', 'TCS', 'Remote', '₹25,000', 6.5),
        ('Data Analyst', 'Microsoft', 'Mumbai', '₹45,000', 9.0)
    ]
    conn.executemany('INSERT INTO jobs (title, company, location, stipend, min_cgpa) VALUES (?,?,?,?,?)', sample_jobs)
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/jobs')
def api_jobs():
    conn = get_db_connection()
    jobs = conn.execute('SELECT * FROM jobs').fetchall()
    conn.close()
    return jsonify([dict(row) for row in jobs])

@app.route('/api/save-student', methods=['POST'])
def save_student():
    data = request.json
    record = f"STUDENT: {data['name']} | CGPA: {data['cgpa']}\nInternships: {data['internships']}\n{'-'*30}\n"
    with open('student_records.txt', 'a') as f:
        f.write(record)
    return jsonify({"message": "Profile synced and saved!"})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)