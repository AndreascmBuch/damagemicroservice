import sqlite3
from flask import Flask, request, jsonify, Response



def get_db_connection():
    return sqlite3.connect('damage_database.db')

app = Flask(__name__)

@app.route('/damage', methods=['GET'])
def list_of_car_damage():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM damage')
    damage = cursor.fetchall()
    conn.close()
    return jsonify(damage)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')