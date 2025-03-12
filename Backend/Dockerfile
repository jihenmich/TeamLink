# Basis-Image
FROM python:3.10

# Arbeitsverzeichnis setzen
WORKDIR /app

# Abhängigkeiten installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App-Code kopieren
COPY . .

# Port für FastAPI
EXPOSE 8000

# Startbefehl
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
