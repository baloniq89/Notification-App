FROM python:3.9-slim

# Ustawienie katalogu roboczego
WORKDIR /app

# Kopiowanie zależności i ich instalacja
COPY scheduler_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiowanie plików aplikacji
COPY scheduler_service/ .
COPY shared/ ./shared/

# Uruchomienie aplikacji Flask
CMD ["python", "app.py"]
