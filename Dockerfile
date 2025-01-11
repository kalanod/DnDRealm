# Используем базовый образ с Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY src/ /app

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Указываем команду для запуска приложения
CMD ["python", "main.py"]

