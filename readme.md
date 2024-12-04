# **Car Damage Microservice**

Dette projekt er en Flask-baseret API til administration af en SQLite-database, der registrerer skader på biler. Projektet inkluderer kode til at oprette en database, oprette tabeller, indsætte eksempler og køre en webservice til at hente data om skader.

## **Funktioner**
- **Opret og administrér en SQLite-database:** Tabellerne inkluderer data om bilskader.
- **RESTful API:** Endpoint til at hente en liste over bilskader.
- **Docker containerization:** Flask-applikationen og databasen kører i en Docker-container med support til persistens.

---

## **Krav**
- **Software:**
  - Python 3.10
  - Flask
  - Docker
  - SQLite
- **Biblioteker:**
  - `flask`
  - `sqlite3`

---

## **Installation og brug**

### **1. Klargøring af projektet**
1. Sørg for, at du har Docker installeret på din maskine.
2. Klon dette projekt til din lokale maskine:
   ```bash
   git clone <repo-url>
   cd <projektnavn>
2. Byg Docker-image
Byg Docker-containeren med følgende kommando:
docker build -t flask-app .
3. Start containeren
Kør applikationen med følgende kommando. Denne opsætning inkluderer et volume til at gøre databasen persistent:
docker run -p 5000:5000 -v $(pwd)/damage_database.db:/app/damage_database.db flask-app
4. Brug API'et
API'et er tilgængeligt på http://localhost:5000/damage. Brug et værktøj som Postman eller curl til at hente data:

bash
Kopier kode
curl http://localhost:5000/damage
Endpoints
Metode	Endpoint	Beskrivelse
GET	/damage	Henter alle bilskader
Databasen
| Kolonnenavn     | Datatype      | Beskrivelse                                    |
|:-----------------|:-------------:|-----------------------------------------------:|
| `damage_id`      | INTEGER       | Primær nøgle, autogenereret                   |
| `car_id`         | INTEGER       | Bilens ID                                     |
| `description`    | TEXT          | Beskrivelse af skaden                         |
| `date_reported`  | DATETIME      | Dato hvor skaden blev registreret             |
| `severity`       | TEXT (CHECK)  | Skadens alvorlighed: `low`, `medium`, `high`  |
| `cost_estimate`  | REAL          | Anslåede reparationsomkostninger              |



Før første kørsel, skal du initialisere databasen med scriptet skadedatabase.py:
python skadedatabase.py
Dette opretter tabellen og indsætter en testpost.

Bekræft at API'et fungerer ved at sende en GET-anmodning til /damage.

Vedligeholdelse
Databasen
For at ændre eller opdatere databasen, kan du enten:

Køre kommandoer via SQLite CLI.
Bruge Python og sqlite3-modulet til at opdatere data.
Docker
For at stoppe containeren:
bash
Kopier kode
docker stop <container_id>
For at starte containeren igen:
bash
Kopier kode
docker start <container_id>
Fejlfinding
Problem: Data bliver ikke gemt efter containerstop.
Løsning: Sørg for, at du bruger et korrekt mappet volume ved at inkludere -v $(pwd)/damage_database.db:/app/damage_database.db i docker run.

Problem: Endpoint returnerer en tom liste.
Løsning: Tjek, om databasen indeholder data ved at køre sqlite3 damage_database.db og verificere tabellen.

