import sqlite3

# Opret forbindelse til databasen
conn = sqlite3.connect("damage_database.db")
cursor = conn.cursor()

# Opret tabellen
cursor.execute('''
CREATE TABLE IF NOT EXISTS damage(
    damage_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    car_id INTEGER, 
    description TEXT, 
    date_reported DATETIME, 
    severity TEXT CHECK(severity IN ('low', 'medium', 'high')), 
    cost_estimate REAL
)
''')

# Gem ændringer og luk forbindelsen
conn.commit()
conn.close()


conn = sqlite3.connect("damage_database.db")
cursor = conn.cursor()

cursor.execute('''
INSERT INTO damage (car_id, description, date_reported, severity, cost_estimate)
VALUES (123, 'Bule på bagkofanger', '2024-12-03', 'medium', 2500)
''')

conn.commit()
conn.close()
