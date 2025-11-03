# Используем официальный образ Python
FROM python:3.11-slim-bullseye

# Устанавливаем зависимости включая nginx
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Создаем и переходим в рабочую директорию
WORKDIR /app

# Просто копируем nginx конфиг в основную директорию конфигов
COPY nginx.conf /etc/nginx/nginx.conf

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

# Открываем порт
EXPOSE 80

# Запускаем и nginx и Django
CMD nginx && python manage.py runserver 0.0.0.0:8000