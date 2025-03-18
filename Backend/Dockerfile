# Basis-Image (Python 3.12, kannst aber auch 3.10 verwenden, wenn du möchtest)
FROM python:3.12

# Arbeitsverzeichnis setzen
WORKDIR /app

# Umgebungsvariable für den PYTHONPATH setzen, damit Docker die Module richtig erkennt
ENV PYTHONPATH=/app

# Abhängigkeiten installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App-Code kopieren
COPY . .

# Port für FastAPI
EXPOSE 8000

# Startbefehl
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
