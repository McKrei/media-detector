FROM python:3.13-slim

WORKDIR /app

# Опционально: чтобы не упасть на проблемах с сетью
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Сначала зависимости (для кеша)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Потом код
COPY . .

# Один запуск main.py
CMD ["python", "main.py"]
