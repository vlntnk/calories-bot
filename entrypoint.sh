#!/bin/bash
# Ждём, пока БД станет доступной
echo "Жду базу данных..."
while ! nc -z postgres 5432; do
  sleep 1
done

# Применяем миграции
#alembic revision --autogenerate -m 'migrate'
alembic upgrade head

# Запускаем приложение (то, что было в CMD)
exec "$@"
