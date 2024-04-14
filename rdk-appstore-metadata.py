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
                 requirements TEXT,
                 bundleurl TEXT,
                 FOREIGN KEY (maintainer_code) REFERENCES maintainers(code) ON DELETE CASCADE)''')
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

# Endpoint to delete a maintainer
@app.route('/maintainers/<string:code>', methods=['DELETE'])
def delete_maintainer(code):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    try:
        # Check if the maintainer exists
        c.execute("SELECT * FROM maintainers WHERE code=?", (code,))
        maintainer = c.fetchone()
        if maintainer:
            # Delete the maintainer
            c.execute("DELETE FROM maintainers WHERE code=?", (code,))
            print("Maintainer deleted")
            # Check the associated apps before deletion
            c.execute("SELECT * FROM apps WHERE maintainer_code=?", (code,))
            associated_apps_before = c.fetchall()
            print("Associated apps before deletion:", associated_apps_before)
            # Delete associated apps
            c.execute("DELETE FROM apps WHERE maintainer_code=?", (code,))
            print("Associated apps deleted")
            conn.commit()
            conn.close()
            return jsonify({"message": "Maintainer deleted successfully"}), 200
        else:
            conn.close()
            return jsonify({"error": "Maintainer with code '{}' not found.".format(code)}), 404
    except Exception as e:
        conn.close()
        print("Error deleting maintainer:", e)
        return jsonify({"error": "Failed to delete maintainer", "details": str(e)}), 500

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
    bundleurl = req_data.get('bundleurl')  # New field
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    try:
        # Ensure that code, header, and requirements are cast to strings
        c.execute("INSERT INTO apps (maintainer_code, header, requirements, bundleurl) VALUES (?, ?, ?, ?)", (str(code), str(header), str(requirements), str(bundleurl)))
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
    c.execute("SELECT header, requirements,bundleurl FROM apps WHERE maintainer_code=?", (code,))
    apps = c.fetchall()
    conn.close()

    result = []
    for app in apps:
        result.append({
            "header": app[0],
            "requirements": app[1],
            "bundleurl": app[2]
        })

    return jsonify(result), 200
@app.route('/maintainers/<string:code>/apps/<int:app_id>', methods=['GET'])
def get_app(code, app_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT header, requirements, bundleurl FROM apps WHERE maintainer_code=? AND id=?", (code, app_id))
    app = c.fetchone()
    conn.close()

    if app:
        header = app[0]
        requirements = app[1]
        bundleurl = app[2]
        response_data = {
            "header": header,
            "requirements": requirements
        }
        if bundleurl is not None:
           response_data["bundleurl"] = bundleurl
        return jsonify(response_data), 200
    else:
        return jsonify({"error": "App not found"}), 404

# Endpoint to add a new variable (e.g., bundleurl) to the app with ID 1
@app.route('/maintainers/<string:code>/apps/<int:app_id>/variables', methods=['POST'])
def add_variable(code, app_id):
    req_data = request.get_json()
    variable_name = req_data.get('name')
    variable_value = req_data.get('value')
 
    # Update the app with the new variable
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    try:
        # Construct and execute SQL query to update the variable for the specified app
        c.execute("UPDATE apps SET {}=? WHERE maintainer_code=? AND id=?".format(variable_name), (variable_value, code, app_id))
        conn.commit()
        conn.close()
        return jsonify({"message": "Variable added/updated successfully"}), 200
    except Exception as e:
        conn.close()
        print("Error executing SQL query:", e)
        return jsonify({"error": "Failed to add/update variable", "details": str(e)}), 500
if __name__ == '__main__':
    init_db()
    app.run(debug=True)

