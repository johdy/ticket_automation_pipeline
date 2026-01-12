FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr libtesseract-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./requirements.txt

# Installer torch CPU-only + les autres dépendances
RUN pip install --no-cache-dir \
        torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip

# Copier tout ton code Flask + OCR
COPY . .

# Exposer le port Flask
EXPOSE 5000

# Lancer ton app principale (celle de ton API Flask)
CMD ["python", "app.py"]
