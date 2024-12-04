# Brug en officiel Python-billedbase
FROM python:3.10-slim

# Indstil arbejdsmappen i containeren
WORKDIR /app

# Kopiér alle filer fra det lokale bibliotek til containeren
COPY . .

# Installer Flask
RUN pip install flask

# Eksponér port 5000 (den port Flask bruger)
EXPOSE 5000

# Kommando til at starte Flask-applikationen
CMD ["python", "app.py"]
