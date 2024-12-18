# Car Damage Microservice

## Introduktion
Denne mikroservice tilbyder en RESTful API til at administrere skaderapporter for biler, herunder oprettelse, opdatering og sletning af skaderegistreringer knyttet til biler i en flåde. Den anvender Flask og SQLite til datalagring og Flask-JWT-Extended til autentificering.

## Krav
- Python 3.10 eller nyere
- Flask
- SQLite3
- flask-jwt-extended
- python-dotenv
- gunicorn

## Opsætning

### 1. Klon repositoryet
```bash
git clone <repository_url>
cd <repository_directory>
```

### 2. Installer afhængigheder
Sørg for, at du har pip installeret, og kør derefter:
```bash
pip install -r requirements.txt
```

### 3. Opret en .env-fil
Opret en `.env`-fil i roden af dit projekt med følgende variabler:
```env
DB_PATH=damage_database.db
FLASK_ENV=development
KEY=din_hemmelige_nøgle
```

### 4. Opsætning af database
Databasen oprettes automatisk, når applikationen startes, sammen med en tabel til lagring af skaderapporter.

### 5. Kør applikationen
Du kan køre applikationen med følgende kommando:
```bash
flask run
```
Eller for produktion, brug Gunicorn:
```bash
gunicorn --bind 0.0.0.0:80 app:app
```

## API Endpoints

### `/`
**GET**: Returnerer grundlæggende information om mikroservicen.

Eksempel på svar:
```json
{
  "service": "Damage Service",
  "version": "1.0.0",
  "description": "En RESTful API til at administrere skader på biler"
}
```

### `/debug`
**GET**: Returnerer JWT-hemmelig nøgle og database-sti til fejlsøgning.

Eksempel på svar:
```json
{
  "JWT_SECRET_KEY": "din_hemmelige_nøgle",
  "Database_Path": "damage_database.db"
}
```

### `/damage/add`
**POST**: Registrerer en ny skaderapport for en bil. Kræver en gyldig JWT-token i Authorization-headeren.

**Request body:**
```json
{
  "car_id": 123,
  "date_reported": "2024-12-16T15:00:00",
  "engine_damage": "minor",
  "tire_damage": "puncture",
  "brake_damage": "broken",
  "bodywork_damage": "dent",
  "interior_damage": "scratched",
  "electronic_damage": "minor",
  "glass_damage": "cracked",
  "undercarriage_damage": "scraped",
  "light_damage": "broken"
}
```

**Eksempel på svar:**
```json
{
  "message": "Skade registreret med succes"
}
```

### `/damage`
**GET**: Henter en liste over alle skaderapporter.

**Eksempel på svar:**
```json
[
  {
    "damage_id": 1,
    "car_id": 123,
    "date_reported": "2024-12-16T15:00:00",
    "engine_damage": "minor",
    "tire_damage": "puncture",
    "brake_damage": "broken",
    "bodywork_damage": "dent",
    "interior_damage": "scratched",
    "electronic_damage": "minor",
    "glass_damage": "cracked",
    "undercarriage_damage": "scraped",
    "light_damage": "broken"
  }
]
```

### `/damage/<car_id>`
**GET**: Henter alle skaderapporter for en specifik bil ved hjælp af car_id.

**Eksempel på svar:**
```json
[
  {
    "damage_id": 1,
    "car_id": 123,
    "date_reported": "2024-12-16T15:00:00",
    "engine_damage": "minor",
    "tire_damage": "puncture",
    "brake_damage": "broken",
    "bodywork_damage": "dent",
    "interior_damage": "scratched",
    "electronic_damage": "minor",
    "glass_damage": "cracked",
    "undercarriage_damage": "scraped",
    "light_damage": "broken"
  }
]
```

### `/damage/change/<damage_id>`
**PUT**: Opdaterer en eksisterende skaderapport. Kræver en gyldig JWT-token i Authorization-headeren.

**Request body:**
```json
{
  "engine_damage": "major",
  "tire_damage": "worn out"
}
```

**Eksempel på svar:**
```json
{
  "message": "Skaderapport 1 opdateret med succes"
}
```

**DELETE**: Sletter en skaderapport ved damage_id. Kræver en gyldig JWT-token i Authorization-headeren.

**Eksempel på svar:**
```json
{
  "message": "Skaderapport 1 slettet med succes"
}
```

## Docker Opsætning

### Dockerfile
En Dockerfile er inkluderet for at bygge og køre applikationen i en container.
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:app"]
```

## Autentificering
Denne mikroservice anvender JWT til autentificering. For at interagere med endpoints skal du først indhente en JWT-token.

### Få en JWT-token
For at få en token skal du implementere en login-route, der returnerer en JWT-token ved succesfuld brugerautentificering (dette trin er ikke implementeret i den medfølgende kode).

Når du er autentificeret, inkluder tokenen i Authorization-headeren i følgende format:
```http
Authorization: Bearer <din_token_her>
```

## Licens
Dette projekt er licenseret under MIT-licensen - se LICENSE-filen for detaljer.




