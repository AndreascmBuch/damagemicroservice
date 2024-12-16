# Car Damage Microservice

This microservice provides a RESTful API for managing car damage reports, including creating, updating, and deleting damage records associated with cars in a fleet. It leverages Flask and SQLite for storing the data and Flask-JWT-Extended for authentication.

## Requirements

- Python 3.10 or higher
- Flask
- SQLite3
- flask-jwt-extended
- python-dotenv
- gunicorn

## Setup

### 1. Clone the repository
```bash
git clone <repository_url>
cd <repository_directory>
```

### 2. Install dependencies
Ensure you have pip installed, then run:
```bash
pip install -r requirements.txt
```

### 3. Create a .env file
Create a .env file in the root directory of your project with the following variables:
```env
DB_PATH=damage_database.db
FLASK_ENV=development
KEY=your_secret_key
```

### 4. Database Setup
The database will automatically be created when the application starts, along with a table for storing damage reports.

### 5. Running the Application
You can run the application using the following command:
```bash
flask run
```
Or, for production, use Gunicorn:
```bash
gunicorn --bind 0.0.0.0:80 app:app
```

## API Endpoints

### /
- **GET:** Returns basic information about the microservice.
- **Example response:**
  ```json
  {
    "service": "Damage Service",
    "version": "1.0.0",
    "description": "A RESTful API for managing car damages"
  }
  ```

### /debug
- **GET:** Returns the JWT secret key and the database path for debugging purposes.
- **Example response:**
  ```json
  {
    "JWT_SECRET_KEY": "your_secret_key",
    "Database_Path": "damage_database.db"
  }
  ```

### /damage/add
- **POST:** Registers a new damage report for a car. Requires a valid JWT token in the Authorization header.
- **Request body:**
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
- **Example response:**
  ```json
  {
    "message": "Damage registered successfully"
  }
  ```

### /damage
- **GET:** Fetches a list of all damage reports.
- **Example response:**
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

### /damage/<car_id>
- **GET:** Fetches all damage records for a specific car by car_id.
- **Example response:**
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

### /damage/change/<damage_id>
- **PUT:** Updates an existing damage report. Requires a valid JWT token in the Authorization header.
- **Request body:**
  ```json
  {
    "engine_damage": "major",
    "tire_damage": "worn out"
  }
  ```
- **Example response:**
  ```json
  {
    "message": "Damage report 1 updated successfully"
  }
  ```

- **DELETE:** Deletes a damage report by damage_id. Requires a valid JWT token in the Authorization header.
- **Example response:**
  ```json
  {
    "message": "Damage report 1 deleted successfully"
  }
  ```

## Docker Setup

### Dockerfile
A Dockerfile is included to build and run the application in a container.
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:app"]
```

### Docker Compose
To run the application with Docker Compose, include the following docker-compose.yml file:
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "80:80"
    environment:
      - DB_PATH=damage_database.db
      - FLASK_ENV=development
      - KEY=your_secret_key
    volumes:
      - .:/app
```

## Authentication

This microservice uses JWT for authentication. To interact with the endpoints, you must first obtain a JWT token.

### Getting a JWT Token
To obtain a token, you'll need to implement a login route that returns a JWT token upon successful user authentication (this step is not implemented in the provided code).

Once authenticated, include the token in the Authorization header in the following format:
```makefile
Authorization: Bearer <your_token_here>
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
```



