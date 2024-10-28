from flask import Flask, jsonify, request
import sqlite3
import json
import re

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
                 testurl TEXT,
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

# Endpoint to delete an app under a maintainer
@app.route('/maintainers/<string:code>/apps/<int:app_id>', methods=['DELETE'])
def delete_app(code, app_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    try:
        # Check if the maintainer exists
        c.execute("SELECT * FROM maintainers WHERE code=?", (code,))
        maintainer = c.fetchone()
        if not maintainer:
            conn.close()
            return jsonify({"error": f"Maintainer with code '{code}' not found."}), 404

        # Check if the app exists for this maintainer
        c.execute("SELECT * FROM apps WHERE maintainer_code=? AND id=?", (code, app_id))
        app = c.fetchone()
        if not app:
            conn.close()
            return jsonify({"error": f"App with id '{app_id}' not found for maintainer '{code}'."}), 404

        # Delete the app
        c.execute("DELETE FROM apps WHERE maintainer_code=? AND id=?", (code, app_id))
        conn.commit()
        conn.close()
        return jsonify({"message": f"App with id '{app_id}' deleted successfully from maintainer '{code}'."}), 200
    except Exception as e:
        conn.close()
        print("Error deleting app:", e)
        return jsonify({"error": "Failed to delete app", "details": str(e)}), 500

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
    testurl = req_data.get('testurl')  # New field
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    try:
        # Ensure that code, header, and requirements are cast to strings
        c.execute("INSERT INTO apps (maintainer_code, header, requirements, testurl) VALUES (?, ?, ?, ?)", (str(code), str(header), str(requirements), str(testurl)))
        conn.commit()
        conn.close()
        return jsonify({"message": "App added successfully"}), 201
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "Failed to add app"}), 400

# Endpoint to get all apps for a maintainer
@app.route('/maintainers/<string:code>/apps', methods=['GET'])
#def get_all_apps(code):
#    conn = sqlite3.connect(DB_FILE)
#    c = conn.cursor()
#    c.execute("SELECT header, requirements,testurl FROM apps WHERE maintainer_code=?", (code,))
#    apps = c.fetchall()
#    conn.close()

#    result = []
#    for app in apps:
#        result.append({
#            "header": app[0],
#            "requirements": app[1],
#            "testurl": app[2]
#        })

#    return jsonify(result), 200

def get_all_apps(code):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT header, requirements, testurl FROM apps WHERE maintainer_code=?", (code,))
    apps = c.fetchall()
    conn.close()

    result = {
        "applications": [],
        "meta": {
            "resultSet": {
                "count": len(apps),
                "offset": 0,
                "limit": 10,  # Adjust based on your pagination requirements
                "total": len(apps)
            }
        }
    }

    for app in apps:
        try:
            # Safely parse 'header' and 'requirements' with ast.literal_eval
            header = ast.literal_eval(app[0])
            requirements = ast.literal_eval(app[1])

            application_data = {
                "id": header.get("id"),
                "version": header.get("version"),
                "icon": header.get("icon"),
                "name": header.get("name"),
                "description": header.get("description"),
                "url": header.get("url"),
                "type": "application/vnd.rdk-app.dac.native",
                "category": header.get("category"),
                "localisations": [
                    {
                        "languageCode": loc.get("languageCode"),
                        "name": loc.get("name"),
                        "description": loc.get("description")
                    } for loc in header.get("localization", [])
                ]
            }

            result["applications"].append(application_data)

        except (ValueError, SyntaxError) as e:
            # Log the error and continue with the next app
            print(f"Error parsing JSON for app: {app[0]} or {app[1]}. Error: {e}")

    return jsonify(result), 200

@app.route('/maintainers/<string:code>/apps/<int:app_id>', methods=['GET'])
def get_app(code, app_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT header, requirements, testurl FROM apps WHERE maintainer_code=? AND id=?", (code, app_id))
    app = c.fetchone()
    conn.close()

    if app:
        header = app[0]
        requirements = app[1]
        testurl = app[2]
        response_data = {
            "header": header,
            "requirements": requirements
        }
        if testurl is not None:
           response_data["testurl"] = testurl
        return jsonify(response_data), 200
    else:
        return jsonify({"error": "App not found"}), 404



import re

import ast
import json

@app.route('/maintainers/<string:code>/apps/<string:app_id>', methods=['GET'])
def get_app_by_id(code, app_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # Fetch all apps from the database
    c.execute("SELECT * FROM apps")
    all_apps = c.fetchall()

    conn.close()

    # Initialize variables to store the found application details
    application_data = None

    # Iterate through fetched apps to find the matching app_id
    for app_data in all_apps:
        id_, maintainer_code, header_str, requirements_str, testurl = app_data
        
        # Convert header and requirements from string to dictionary
        header_dict = ast.literal_eval(header_str)
        requirements_dict = ast.literal_eval(requirements_str) if requirements_str else {}

        if header_dict.get("id") == app_id:
            # Build the response structure without hardcoding
            application_data = {
                "header": header_dict,  # Pulls all header fields directly
                "requirements": {
                    "dependencies": requirements_dict.get("dependencies"),
                    "platform": requirements_dict.get("platform", {}),
                    "hardware": requirements_dict.get("hardware", {}),
                    "features": requirements_dict.get("features")
                },
                "maintainer": {
                    "code": maintainer_code,
                    "name": requirements_dict.get("maintainerName"),
                    "address": requirements_dict.get("maintainerAddress"),
                    "homepage": requirements_dict.get("maintainerHomepage"),
                    "email": requirements_dict.get("maintainerEmail")
                },
                "versions": [{"version": header_dict.get("version")}]
            }

            # Add test URL if it exists and is not 'None'
            if testurl and testurl != 'None':
                application_data["testurl"] = testurl

            break  # Exit loop once the matching app_id is found

    if application_data:
        return jsonify(application_data), 200
    else:
        return jsonify({"error": "App not found"}), 404


@app.route('/maintainers/<string:code>/apps/<int:app_id>/variables', methods=['POST'])
def add_variable(code, app_id):
    req_data = request.get_json()
    variable_name = req_data.get('name')
    variable_value = req_data.get('value')
 
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    try:
        if variable_name == 'url':
            # Fetch the current header
            c.execute("SELECT header FROM apps WHERE maintainer_code=? AND id=?", (code, app_id))
            header_str = c.fetchone()[0]
            
            # Parse the header
            header_dict = ast.literal_eval(header_str)
            
            # Update the URL
            header_dict['url'] = variable_value
            
            # Convert back to string
            new_header_str = str(header_dict)
            
            # Update the header in the database
            c.execute("UPDATE apps SET header=? WHERE maintainer_code=? AND id=?", (new_header_str, code, app_id))
        else:
            # For other variables, update as before
            c.execute(f"UPDATE apps SET {variable_name}=? WHERE maintainer_code=? AND id=?", (variable_value, code, app_id))
        
        conn.commit()
        conn.close()
        return jsonify({"message": f"{variable_name} updated successfully"}), 200
    except Exception as e:
        conn.close()
        print(f"Error updating {variable_name}:", e)
        return jsonify({"error": f"Failed to update {variable_name}", "details": str(e)}), 500

if __name__ == '__main__':
    init_db()
    #default bound to 127.0.0.1
    #app.run(debug=True)
    #curl -X GET http://10.0.0.70:5000/maintainers/rdk4
    #app.run(host='127.0.0.1', port=5000,debug=True)
    app.run(debug=True, host='192.168.64.47', port=8089)
