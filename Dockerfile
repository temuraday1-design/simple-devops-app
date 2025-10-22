# 1. Базалық образ
FROM python:3.13-slim

# 2. Жұмыс директориясы
WORKDIR /app

# 3. Қолданба файлдарын контейнерге көшіру
COPY . /app

# 4. Тәуелділіктерді орнату
RUN pip install --no-cache-dir flask

# 5. Портты ашу
EXPOSE 5000

# 6. Қолданбаны іске қосу
CMD ["python", "app.py"]
