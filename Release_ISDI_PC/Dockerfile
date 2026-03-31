FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libgtk-3-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt pyinstaller

COPY src/ ./src/

CMD pyinstaller --noconfirm --windowed --onedir --name "ISDI-PC" --paths src --add-data "src:src" src/main.py && cp -r dist /app/out/
