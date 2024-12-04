import sqlite3
from flask import Flask, jsonify

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
