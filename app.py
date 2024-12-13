import os 
import sqlite3
from flask import Flask, jsonify, request
from dotenv import load_dotenv

DB_PATH = os.getenv('DB_PATH', 'damage_database.db')

def get_db_connection():
    conn = sqlite3.connect('DB_PATH')
    conn.row_factory = sqlite3.Row  
    return conn



app = Flask(__name__)

@app.route('/damage', methods=['POST'])
def register_damage():
    data = request.json
    car_id = data.get("car_id")
    date_reported = data.get("date_reported")  # Kan være None
    
    # Skadetyper
    engine_damage = data.get("engine_damage", "none")
    tire_damage = data.get("tire_damage", "none")
    brake_damage = data.get("brake_damage", "none")
    bodywork_damage = data.get("bodywork_damage", "none")
    interior_damage = data.get("interior_damage", "none")
    electronic_damage = data.get("electronic_damage", "none")
    glass_damage = data.get("glass_damage", "none")
    undercarriage_damage = data.get("undercarriage_damage", "none")
    light_damage = data.get("light_damage", "none")

    # Tjek for nødvendige felter
    if not car_id:
        return jsonify({"error": "car_id is required"}), 400

    # Forbind til databasen og indsæt skaden
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
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM damage')
    damage_records = cursor.fetchall()
    conn.close()

   
    damage_list = [dict(row) for row in damage_records]

    return jsonify(damage_list)

@app.route('/damage/<int:car_id>', methods=['GET'])
def get_damage_by_car_id(car_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Udfør SQL-forespørgsel
        cursor.execute('SELECT * FROM damage WHERE car_id = ?', (car_id,))
        records = cursor.fetchall()
        conn.close()

        # Konverter til en liste af dicts
        damage_list = [dict(row) for row in records]

        # Returnér data
        if damage_list:
            return jsonify(damage_list), 200
        else:
            return jsonify({"error": "No damage data found for this car"}), 404

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500


@app.route('/damage/change/<int:damage_id>', methods=['PUT'])
def update_damage_report(damage_id):
    # Forbind til databasen
    conn = get_db_connection()
    cursor = conn.cursor()

    # Hent data fra HTTP-request body
    updated_data = request.get_json()

    # Lav en liste af gyldige felter, der kan opdateres
    updatable_fields = [
        "date_reported", "engine_damage", "tire_damage", "brake_damage",
        "bodywork_damage", "interior_damage", "electronic_damage", 
        "glass_damage", "undercarriage_damage", "light_damage"
    ]

    # Generer SQL og værdier dynamisk baseret på de medsendte felter
    set_clause = ", ".join([f"{field} = ?" for field in updated_data.keys() if field in updatable_fields])
    values = [updated_data[field] for field in updated_data.keys() if field in updatable_fields]

    # Tjek, om der er noget at opdatere
    if not set_clause:
        return jsonify({"message": "No valid fields to update"}), 400

    # Tilføj `damage_id` til værdierne for WHERE-betingelsen
    values.append(damage_id)

    # Udfør SQL-opdateringen
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
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # SQL query to delete the damage record with the given damage_id
        cursor.execute('DELETE FROM damage WHERE damage_id = ?', (damage_id,))
        conn.commit()
        
        if cursor.rowcount == 0:
            return jsonify({"message": f"No damage report found with id {damage_id}"}), 404
        return jsonify({"message": f"Damage report {damage_id} deleted successfully"}), 200

    except sqlite3.Error as e:
        return jsonify({"message": f"Database error: {str(e)}"}), 500
    finally:
        conn.close()


@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "service": "Damage Service",
        "version": "1.0.0",
        "description": "A RESTful API for managing car damages"
    })

if __name__ == '__main__':
    app.run()
