import sqlite3
from flask import Flask, jsonify, request

def get_db_connection():
    conn = sqlite3.connect('damage_database.db')
    conn.row_factory = sqlite3.Row  
    return conn

app = Flask(__name__)

@app.route('/damage', methods=['GET'])
def list_of_car_damage():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM damage')
    damage_records = cursor.fetchall()
    conn.close()

   
    damage_list = [dict(row) for row in damage_records]

    return jsonify(damage_list)

@app.route('/damage/<int:damage_id>', methods=['PUT'])
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

 

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
