from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def connect_db():
    conn = sqlite3.connect("notes.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    """)
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save_note():
    data = request.json
    note = data['content']

    conn = connect_db()
    conn.execute("INSERT INTO notes (content) VALUES (?)", (note,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Note saved successfully!"})

@app.route('/notes')
def get_notes():
    conn = connect_db()
    notes = conn.execute("SELECT * FROM notes ORDER BY id DESC").fetchall()
    conn.close()

    return jsonify([
        {"id": n[0], "content": n[1]} for n in notes
    ])

if __name__ == '__main__':
    connect_db().close()
    app.run(debug=True)
