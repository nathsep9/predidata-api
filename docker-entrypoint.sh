#!/bin/sh


if [$DB_HOST -eq ""]; then
    echo "No DB_HOST specified"
    exit 1
fi

while ! nc -z $DB_HOST 5432; do
  echo "$(date) - waiting for database to start on $DB_HOST:5432..."
  sleep 1
done

echo "DB started"

flask db upgrade

exec "$@"