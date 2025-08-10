# Django + Celery + Redis + PostgreSQL Docker проект

## Технологический стек
- **Django** - основной веб-фреймворк
- **Celery** - асинхронные задачи
- **Redis** - брокер сообщений и кэш
- **PostgreSQL** - основная база данных
- **Gunicorn** - продакшн-сервер
- **Docker** - контейнеризация приложения

## 🛠 Требования
1. Docker ([установка](https://docs.docker.com/get-docker/))
2. Docker Compose ([установка](https://docs.docker.com/compose/install/))
3. Свободные порты: 8000, 5432

## 🚀 Быстрый старт

```bash
# Клонировать репозиторий
git clone https://github.com/daniel-ocean97/PythonProject5


# Создать файл окружения (на основе примера)
cp .env.sample .env

# Запустить контейнеры
docker-compose up --build -d

# Применить миграции
docker-compose exec backend python manage.py migrate

# Создать суперпользователя (опционально)
docker-compose exec backend python manage.py createsuperuser
```

🔍 Проверка сервисов
1. Django приложение
```bash
curl -I http://localhost:8000/admin/
```
Ожидаемый ответ: HTTP/1.1 200 OK или HTTP/1.1 302 Found

2. PostgreSQL
```bash
docker-compose exec db psql -U your_db_user -d your_db_name -c "\dt"
```
3. Redis
```bash
docker-compose exec redis redis-cli ping
```
Ожидаемый ответ: PONG

4. Celery Worker
```bash
docker-compose logs celery_worker | grep "ready"
```
5. Celery Beat
```bash
docker-compose logs celery_beat | grep "Scheduler"
```
⚙️ Команды
### Управление контейнерами

1. ```bash docker-compose up  -d ```	Запуск
2. ```bash docker-compose down```	Остановка
3. ```bash docker-compose ps```	Статус
4. ```docker-compose logs -f```	Логи
