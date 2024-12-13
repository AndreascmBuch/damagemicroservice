import os
import sqlite3
from flask import Flask, jsonify, request, g
from dotenv import load_dotenv

# Tjek om DB_path virker 

def get_db_connection():
    """Function to get the database connection."""
    conn = sqlite3.connect(DB_PATH)  # Use the correct DB_PATH
    conn.row_factory = sqlite3.Row  
    return conn

# Initialize the Flask app
app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Get DB_PATH from environment variable or use default
DB_PATH = os.getenv('DB_PATH', 'damage_database.db')

# Close the database connection after the request is finished
@app.teardown_appcontext
def close_db(error):
    """Closes the database connection after each request."""
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/', methods=['GET'])
def home():
    """Basic home route to check if the service is running."""
    return jsonify({
        "service": "Damage Service",
        "version": "1.0.0",
        "description": "A RESTful API for managing car damages"
    })

@app.route('/damage', methods=['POST'])
def register_damage():
    """Route to register a new damage report."""
    data = request.json
    car_id = data.get("car_id")
    date_reported = data.get("date_reported")  # Can be None
    
    # Damage types (defaults to "none" if not provided)
    engine_damage = data.get("engine_damage", "none")
    tire_damage = data.get("tire_damage", "none")
    brake_damage = data.get("brake_damage", "none")
    bodywork_damage = data.get("bodywork_damage", "none")
    interior_damage = data.get("interior_damage", "none")
    electronic_damage = data.get("electronic_damage", "none")
    glass_damage = data.get("glass_damage", "none")
    undercarriage_damage = data.get("undercarriage_damage", "none")
    light_damage = data.get("light_damage", "none")

    # Check for required fields
    if not car_id:
        return jsonify({"error": "car_id is required"}), 400

    # Connect to the database and insert the damage record
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO damage (car_id, date_reported, engine_damage, tire_damage, brake_damage, 
                                bodywork_damage, interior_damage, electronic_damage, glass_damage, 
                                undercarriage_damage, light_damage)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (car_id, date_reported, engine_damage, tire_damage, brake_damage, 
              bodywork_damage, interior_damage, electronic_damage, glass_damage, 
              undercarriage_damage, light_damage))
        conn.commit()
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500
    finally:
        conn.close()

    return jsonify({"message": "Damage registered successfully"}), 201

@app.route('/damage', methods=['GET'])
def list_of_car_damage():
    """Route to fetch all damage records."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM damage')
    damage_records = cursor.fetchall()
    conn.close()

    damage_list = [dict(row) for row in damage_records]

    return jsonify(damage_list)

@app.route('/damage/<int:car_id>', methods=['GET'])
def get_damage_by_car_id(car_id):
    """Route to get damage records for a specific car."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Execute SQL query
        cursor.execute('SELECT * FROM damage WHERE car_id = ?', (car_id,))
        records = cursor.fetchall()
        conn.close()

        # Convert to a list of dicts
        damage_list = [dict(row) for row in records]

        # Return data
        if damage_list:
            return jsonify(damage_list), 200
        else:
            return jsonify({"error": "No damage data found for this car"}), 404

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/damage/change/<int:damage_id>', methods=['PUT'])
def update_damage_report(damage_id):
    """Route to update a damage report."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get the data from the request body
    updated_data = request.get_json()

    # List of valid fields that can be updated
    updatable_fields = [
        "date_reported", "engine_damage", "tire_damage", "brake_damage",
        "bodywork_damage", "interior_damage", "electronic_damage", 
        "glass_damage", "undercarriage_damage", "light_damage"
    ]

    # Dynamically create the SQL query based on provided fields
    set_clause = ", ".join([f"{field} = ?" for field in updated_data.keys() if field in updatable_fields])
    values = [updated_data[field] for field in updated_data.keys() if field in updatable_fields]

    # Ensure there are valid fields to update
    if not set_clause:
        return jsonify({"message": "No valid fields to update"}), 400

    # Add the damage_id for the WHERE condition
    values.append(damage_id)

    try:
        cursor.execute(f"UPDATE damage SET {set_clause} WHERE damage_id = ?", values)
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": f"No report found with id {damage_id}"}), 404
    except sqlite3.Error as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500
    finally:
        conn.close()

    return jsonify({"message": f"Damage report {damage_id} updated successfully"}), 200

@app.route('/damage/change/<int:damage_id>', methods=['DELETE'])
def delete_damage(damage_id):
    """Route to delete a damage report."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Execute SQL query to delete the damage record
        cursor.execute('DELETE FROM damage WHERE damage_id = ?', (damage_id,))
        conn.commit()
        
        if cursor.rowcount == 0:
            return jsonify({"message": f"No damage report found with id {damage_id}"}), 404
        return jsonify({"message": f"Damage report {damage_id} deleted successfully"}), 200

    except sqlite3.Error as e:
        return jsonify({"message": f"Database error: {str(e)}"}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
