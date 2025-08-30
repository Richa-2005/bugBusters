import json
from flask import Flask, jsonify
from flask_cors import CORS
app = Flask(__name__)

CORS(app)

# This function safely loads JSON data from a file
def load_json_file(filename):
    """
    Loads and returns JSON data from a file, handling common errors.
    """
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return {"error": f"File '{filename}' not found."}
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{filename}'.")
        return {"error": f"Invalid JSON format in '{filename}'."}

@app.route("/jsonfile")
def get_json_data():
    """
    API endpoint that loads and combines data from multiple JSON files.
    """
    # Load data from all of your JSON files
    currentep_data = load_json_file('currentep.json')
    general_alert_data = load_json_file('generalalert.json')
    majoralert_data = load_json_file('majoralert_20250830_153041.json')
    wsummary_data = load_json_file('wsummary.json')

    # Combine the data into a single dictionary
    all_data = {
        "current_ep": currentep_data,
        "general_alert": general_alert_data,
        "majoralert": majoralert_data,
        "wsummary": wsummary_data
    }
    
    # Return the combined data as a JSON response
    return jsonify(all_data)

if __name__ == '__main__':
    # Make sure to run this file from the 'python' directory
    # so it can find the JSON files.
    app.run(debug=True)
