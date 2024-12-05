# Official Python runtime
FROM python:3.9-slim

# Установка зависимостей системы
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Рабочая директория приложения
WORKDIR /usr/src/app

# Копируем зависимости в контейнер
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект в контейнер
COPY . .

# Собираем статические файлы
RUN python manage.py collectstatic --noinput

# Открываем порт для приложения
EXPOSE 8000

# Команда для запуска Gunicorn
CMD ["gunicorn", "eventcalendar.wsgi:application", "--bind", "0.0.0.0:8000"]
