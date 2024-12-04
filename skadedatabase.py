import sqlite3

# Opret forbindelse til databasen
conn = sqlite3.connect("damage_database.db")
cursor = conn.cursor()

# Opret tabellen med flere skadetyper
cursor.execute('''
CREATE TABLE IF NOT EXISTS damage(
    damage_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    car_id INTEGER, 
    date_reported DATETIME, 
    engine_damage TEXT CHECK(engine_damage IN ('none', 'minor', 'major')), 
    tire_damage TEXT CHECK(tire_damage IN ('none', 'puncture', 'worn out', 'bald')), 
    brake_damage TEXT CHECK(brake_damage IN ('none', 'squealing', 'broken')), 
    bodywork_damage TEXT CHECK(bodywork_damage IN ('none', 'dent', 'scratched')), 
    interior_damage TEXT CHECK(interior_damage IN ('none', 'scratched', 'torn', 'stained')), 
    electronic_damage TEXT CHECK(electronic_damage IN ('none', 'minor', 'major')), 
    glass_damage TEXT CHECK(glass_damage IN ('none', 'cracked', 'shattered')), 
    undercarriage_damage TEXT CHECK(undercarriage_damage IN ('none', 'scraped', 'dented')), 
    light_damage TEXT CHECK(light_damage IN ('none', 'broken', 'not working'))
)
''')

# Gem ændringer og luk forbindelsen
conn.commit()
conn.close()

# Indsæt testdata for at demonstrere skadesregistreringen
conn = sqlite3.connect("damage_database.db")
cursor = conn.cursor()

cursor.execute('''
INSERT INTO damage (car_id, date_reported, engine_damage, tire_damage, brake_damage, bodywork_damage, 
                    interior_damage, electronic_damage, glass_damage, undercarriage_damage, light_damage)
VALUES (123, '2024-12-03', 'minor', 'puncture', 'squealing', 'dent', 
        'none', 'minor', 'cracked', 'scraped', 'broken')
''')

cursor.execute('''
INSERT INTO damage (car_id, date_reported, engine_damage, tire_damage, brake_damage, bodywork_damage, 
                    interior_damage, electronic_damage, glass_damage, undercarriage_damage, light_damage)
VALUES (456, '2024-12-04', 'major', 'none', 'broken', 'scratched', 
        'stained', 'major', 'shattered', 'dented', 'not working')
''')

# Gem ændringer og luk forbindelsen
conn.commit()
conn.close()

