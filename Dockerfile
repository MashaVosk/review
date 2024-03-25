# Базовый образ Python
FROM python:3.10

# Устанавливаем зависимости для приложения
COPY app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Устанавливаем зависимости для scrapy
COPY scrapy/requirements.txt /scrapy/requirements.txt
RUN pip install --no-cache-dir -r /scrapy/requirements.txt

# Копируем исходный код приложения
COPY . /app

# Указываем рабочую директорию
WORKDIR /app

# Команда для запуска main.py
CMD ["python", "main.py"]