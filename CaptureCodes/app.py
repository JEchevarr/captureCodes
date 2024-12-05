
from flask import Flask, request, render_template, jsonify
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect("geology.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS observations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location_type TEXT,
            location_detail TEXT,
            capture_code TEXT,
            observation_date TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_observation', methods=['POST'])
def add_observation():
    data = request.json
    conn = sqlite3.connect("geology.db")
    c = conn.cursor()
    c.execute('''
        INSERT INTO observations (location_type, location_detail, capture_code, observation_date)
        VALUES (?, ?, ?, ?)
    ''', (data['location_type'], data['location_detail'], data['capture_code'], data['observation_date']))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/query_observations', methods=['GET'])
def query_observations():
    filter_criteria = request.args.get('filter', '')
    conn = sqlite3.connect("geology.db")
    c = conn.cursor()
    query = f"SELECT * FROM observations WHERE capture_code LIKE ?"
    c.execute(query, (f"%{filter_criteria}%",))
    results = c.fetchall()
    conn.close()
    return jsonify(results)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
