import os
import sqlite3
from flask import Flask, jsonify, request, g
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get DB_PATH from environment variable or use default
DB_PATH = os.getenv('DB_PATH', 'damage_database.db')

# Initialize the Flask app
app = Flask(__name__)

# Function to get the database connection
def get_db_connection():
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH) 
        g.db.row_factory = sqlite3.Row
    return g.db

# Close the database connection after the request is finished
@app.teardown_appcontext
def close_db(error):
    if 'db' in g:
        g.db.close()

# Ensure the database and table exist
with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS damage(
        damage_id INTEGER PRIMARY KEY AUTOINCREMENT, 
        car_id INTEGER NOT NULL, 
        date_reported DATETIME DEFAULT CURRENT_TIMESTAMP, 
        engine_damage TEXT CHECK(engine_damage IN ('none', 'minor', 'major')) DEFAULT 'none', 
        tire_damage TEXT CHECK(tire_damage IN ('none', 'puncture', 'worn out', 'bald')) DEFAULT 'none', 
        brake_damage TEXT CHECK(brake_damage IN ('none', 'squealing', 'broken')) DEFAULT 'none', 
        bodywork_damage TEXT CHECK(bodywork_damage IN ('none', 'dent', 'scratched')) DEFAULT 'none', 
        interior_damage TEXT CHECK(interior_damage IN ('none', 'scratched', 'torn', 'stained')) DEFAULT 'none', 
        electronic_damage TEXT CHECK(electronic_damage IN ('none', 'minor', 'major')) DEFAULT 'none', 
        glass_damage TEXT CHECK(glass_damage IN ('none', 'cracked', 'shattered')) DEFAULT 'none', 
        undercarriage_damage TEXT CHECK(undercarriage_damage IN ('none', 'scraped', 'dented')) DEFAULT 'none', 
        light_damage TEXT CHECK(light_damage IN ('none', 'broken', 'not working')) DEFAULT 'none'
    )
    ''')
    conn.commit()

# Home route
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "service": "Damage Service",
        "version": "1.0.0",
        "description": "A RESTful API for managing car damages"
    })

# Route to register a new damage report
@app.route('/damage/add', methods=['POST'])
def register_damage():
    data = request.json
    car_id = data.get("car_id")
    date_reported = data.get("date_reported")  # Optional

    # Damage types (defaults to "none" if not provided)
    damage_fields = [
        "engine_damage", "tire_damage", "brake_damage", "bodywork_damage",
        "interior_damage", "electronic_damage", "glass_damage",
        "undercarriage_damage", "light_damage"
    ]
    damage_values = {field: data.get(field, "none") for field in damage_fields}

    if not car_id:
        return jsonify({"error": "car_id is required"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO damage (car_id, date_reported, engine_damage, tire_damage, brake_damage, 
                                bodywork_damage, interior_damage, electronic_damage, glass_damage, 
                                undercarriage_damage, light_damage)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (car_id, date_reported, *damage_values.values()))
        conn.commit()
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500

    return jsonify({"message": "Damage registered successfully"}), 201

# Route to fetch all damage records
@app.route('/damage', methods=['GET'])
def list_of_car_damage():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM damage')
    damage_records = cursor.fetchall()

    damage_list = [dict(row) for row in damage_records]

    return jsonify(damage_list)

# Route to get damage records for a specific car
@app.route('/damage/<int:car_id>', methods=['GET'])
def get_damage_by_car_id(car_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM damage WHERE car_id = ?', (car_id,))
    records = cursor.fetchall()

    damage_list = [dict(row) for row in records]

    if damage_list:
        return jsonify(damage_list), 200
    else:
        return jsonify({"error": "No damage data found for this car"}), 404

# Route to update a damage report
@app.route('/damage/change/<int:damage_id>', methods=['PUT'])
def update_damage_report(damage_id):
    updated_data = request.get_json()

    updatable_fields = [
        "date_reported", "engine_damage", "tire_damage", "brake_damage",
        "bodywork_damage", "interior_damage", "electronic_damage", 
        "glass_damage", "undercarriage_damage", "light_damage"
    ]

    set_clause = ", ".join([f"{field} = ?" for field in updated_data.keys() if field in updatable_fields])
    values = [updated_data[field] for field in updated_data.keys() if field in updatable_fields]

    if not set_clause:
        return jsonify({"message": "No valid fields to update"}), 400

    values.append(damage_id)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"UPDATE damage SET {set_clause} WHERE damage_id = ?", values)
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": f"No report found with id {damage_id}"}), 404
    except sqlite3.Error as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

    return jsonify({"message": f"Damage report {damage_id} updated successfully"}), 200

# Route to delete a damage report
@app.route('/damage/change/<int:damage_id>', methods=['DELETE'])
def delete_damage(damage_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM damage WHERE damage_id = ?', (damage_id,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": f"No damage report found with id {damage_id}"}), 404
        return jsonify({"message": f"Damage report {damage_id} deleted successfully"}), 200

    except sqlite3.Error as e:
        return jsonify({"message": f"Database error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
