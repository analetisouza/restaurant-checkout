#!/bin/sh

until pg_isready -h db -U myuser; do
  echo "Waiting for database to be ready..."
  sleep 1
done
echo "Database is ready"
exec "$@"
