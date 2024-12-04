# Car Damage Microservice

Dette projekt er en Flask-baseret API til administration af en SQLite-database, der registrerer skader på biler. Projektet inkluderer kode til at oprette en database, oprette tabeller, indsætte eksempler og køre en webservice til at hente data om skader. Den er stadig under udvikling, så ændringer kan forekomme! 

Funktioner
Opret og administrér en SQLite-database: Tabellerne inkluderer data om bilskader.
RESTful API: Endpoint til at hente en liste over bilskader.
Docker containerization: Flask-applikationen og databasen kører i en Docker-container med support til persistens.


Krav
Software:
Python 3.10
Flask
Docker
SQLite
Biblioteker:
flask
sqlite3 


projektnavn/
│
├── app.py                # Flask-applikationen med API-logik
├── Dockerfile            # Docker-konfiguration
├── skadedatabase.py      # Script til at oprette og initialisere databasen
├── damage_database.db    # SQLite-databasefil
└── README.md             # 


Installation og brug
1. Klargøring af projektet
Sørg for, at du har Docker installeret på din maskine.
Klon dette projekt til din lokale maskine:
git clone <repo-url>
cd <projektnavn>

2. Byg Docker-image
Byg Docker-containeren med følgende kommando: 
docker build -t flask-app . 

3. Start containeren
Kør applikationen med følgende kommando. Denne opsætning inkluderer et volume til at gøre databasen persistent: 
docker run -p 5000:5000 -v $(pwd)/damage_database.db:/app/damage_database.db flask-app 

4. 
API'et er tilgængeligt på http://localhost:5000/damage. Brug et værktøj som Postman eller curl til at hente data: 

curl http://localhost:5000/damage



Endpoints
Metode	Endpoint	Beskrivelse
GET	/damage	Henter alle bilskader 

Databasen
Tabelstruktur: damage
Kolonnenavn	Datatype	Beskrivelse
damage_id	INTEGER	Primær nøgle, autogenereret
car_id	INTEGER	Bilens ID
description	TEXT	Beskrivelse af skaden
date_reported	DATETIME	Dato hvor skaden blev registreret
severity	TEXT (CHECK)	Skadens alvorlighed: low, medium, high
cost_estimate	REAL	Anslåede reparationsomkostninger


