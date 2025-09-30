
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    wget unzip curl xvfb libnss3 libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libxkbcommon0 libxcomposite1 libxdamage1 libxrandr2 \
    libgbm1 libpangocairo-1.0-0 libgtk-3-0 libasound2 git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir playwright && playwright install chromium

COPY . .

EXPOSE 5000
CMD ["python", "server.py"]
