FROM python:3.9-slim

# Ustawienie katalogu roboczego
WORKDIR /app

# Kopiowanie zależności i ich instalacja
COPY push_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiowanie plików aplikacji
COPY push_service/ .

# Uruchomienie aplikacji Flask
CMD ["python", "app.py"]
