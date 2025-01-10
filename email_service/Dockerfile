# Dockerfile for scheduler_service

# Użycie obrazu z Pythonem
FROM python:3.9-slim

RUN apt-get update && apt-get install -y curl

# Ustawienie katalogu roboczego
WORKDIR /app

# Skopiowanie plików aplikacji do obrazu
COPY ./scheduler_service/ . 
COPY ./shared ./shared 

# Instalacja zależności z requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Ustawienie polecenia startowego dla kontenera
CMD ["python", "app.py"]
