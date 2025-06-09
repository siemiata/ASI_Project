FROM python:3.10.11-slim

# Instalacja systemowych zależności
RUN apt-get update && apt-get install -y --fix-missing \
    build-essential \
    tesseract-ocr \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Ustawienie katalogu roboczego
WORKDIR /app

# Skopiowanie projektu do kontenera
COPY . /app

# Instalacja zależności
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Otwarcie portu na potrzeby streamlit
EXPOSE 8501

# Domyślna komenda uruchamiająca Streamlit z app.py
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
