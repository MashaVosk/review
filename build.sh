#!/bin/bash

# Сборка Docker-образов
docker-compose build

# Запуск контейнеров
docker-compose up -p -d 5000:5000

echo "Приложение запущено."
docker-compose ps