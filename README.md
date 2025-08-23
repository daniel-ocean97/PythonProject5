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


Настройка удаленного сервера для деплоя
1. Подготовка сервера
Создайте виртуальную машину с Ubuntu 20.04/22.04 на любом облачном провайдере (AWS, DigitalOcean, Vultr и т.д.).

2. Настройка сервера
Подключитесь к серверу (51.250.37.202 (при подключении на мой YandexCloud сервер)) по SSH и выполните следующие команды:

bash
# Обновление системы
```sudo apt update && sudo apt upgrade -y```

# Установка Docker
```sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io
```
```
# Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
```
# Добавление пользователя в группу docker
sudo usermod -aG docker $USER
newgrp docker
```

## Настройка GitHub Actions для автоматического деплоя
1. Подготовка секретов
В настройках вашего GitHub репозитория (Settings -> Secrets and variables -> Actions) добавьте следующие секреты:

SSH_KEY: Приватный SSH-ключ для доступа к серверу

SERVER_IP: "51.250.37.202" (IP моего сервера на Yandex Cloud)

SSH_USER: Имя пользователя для SSH (обычно root или ubuntu)

DOCKERHUB_USERNAME: Ваш логин на Docker Hub (если используете)

DOCKERHUB_TOKEN: Токен доступа к Docker Hub (если используете)

DEPLOY_DIR: Путь для деплоя на сервере (например, /opt/myapp)

2. Генерация SSH-ключа
Сгенерируйте SSH-ключ на вашем локальном компьютере, если у вас его еще нет:

```
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

Добавьте публичный ключ на сервер:

```
ssh-copy-id youruser@yourserverip
```
Приватный ключ добавьте в секреты GitHub как SSH_KEY.

3. Настройка workflow
Ваш файл GitHub Actions workflow (.github/workflows/django.yml) уже настроен для автоматического деплоя. При каждом пуше в ветку main или master будет выполняться:

Тестирование приложения

Сборка Docker-образов

Деплой на сервер

4. Первоначальный деплой
Перед первым автоматическим деплоем выполните на сервере вручную:

```
# Создайте директорию для приложения
sudo mkdir -p /opt/myapp
sudo chown $USER:$USER /opt/myapp
```

# Создайте файл .env.production с настройками для production
nano /opt/myapp/.env.production
Заполните файл .env.production необходимыми production-настройками (секретный ключ, настройки БД и т.д.).
