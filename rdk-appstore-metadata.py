from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

DB_FILE = 'maintainer_data.db'

# Initialize database table if not exists
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS maintainers
                 (code TEXT PRIMARY KEY,
                 name TEXT,
                 address TEXT,
                 homepage TEXT,
                 email TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS apps
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 maintainer_code TEXT,
                 header TEXT,
                 requirements TEXT)''')
    conn.commit()
    conn.close()

# Endpoint to add a new maintainer
@app.route('/maintainers', methods=['POST'])
def add_maintainer():
    req_data = request.get_json()
    code = req_data.get('code')
    name = req_data.get('name')
    address = req_data.get('address')
    homepage = req_data.get('homepage')
    email = req_data.get('email')

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO maintainers (code, name, address, homepage, email) VALUES (?, ?, ?, ?, ?)", (code, name, address, homepage, email))
        conn.commit()
        conn.close()
        return jsonify({"message": "Maintainer added successfully"}), 201
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "Maintainer with code '{}' already exists.".format(code)}), 400

# Endpoint to get maintainer details by code
@app.route('/maintainers/<string:code>', methods=['GET'])
def get_maintainer(code):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM maintainers WHERE code=?", (code,))
    maintainer = c.fetchone()
    conn.close()
    if maintainer:
        return jsonify({
            "code": maintainer[0],
            "name": maintainer[1],
            "address": maintainer[2],
            "homepage": maintainer[3],
            "email": maintainer[4]
        }), 200
    else:
        return jsonify({"error": "Maintainer with code '{}' not found.".format(code)}), 404

# Endpoint to get all maintainers
@app.route('/maintainers', methods=['GET'])
def get_all_maintainers():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM maintainers")
    maintainers = c.fetchall()
    conn.close()

    result = []
    for maintainer in maintainers:
        result.append({
            "code": maintainer[0],
            "name": maintainer[1],
            "address": maintainer[2],
            "homepage": maintainer[3],
            "email": maintainer[4]
        })

    return jsonify(result), 200

# Endpoint to add a new app for a maintainer
@app.route('/maintainers/<string:code>/apps', methods=['POST'])
def add_app(code):
    req_data = request.get_json()
    header = req_data.get('header')
    requirements = req_data.get('requirements')

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    try:
        # Ensure that code, header, and requirements are cast to strings
        c.execute("INSERT INTO apps (maintainer_code, header, requirements) VALUES (?, ?, ?)", (str(code), str(header), str(requirements)))
        conn.commit()
        conn.close()
        return jsonify({"message": "App added successfully"}), 201
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "Failed to add app"}), 400

# Endpoint to get all apps for a maintainer
@app.route('/maintainers/<string:code>/apps', methods=['GET'])
def get_all_apps(code):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT header, requirements FROM apps WHERE maintainer_code=?", (code,))
    apps = c.fetchall()
    conn.close()

    result = []
    for app in apps:
        result.append({
            "header": app[0],
            "requirements": app[1]
        })

    return jsonify(result), 200
@app.route('/maintainers/<string:code>/apps/<int:app_id>', methods=['GET'])
def get_app(code, app_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT header, requirements FROM apps WHERE maintainer_code=? AND id=?", (code, app_id))
    app = c.fetchone()
    conn.close()

    if app:
        return jsonify({
            "header": app[0],
            "requirements": app[1]
        }), 200
    else:
        return jsonify({"error": "App not found"}), 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

