#!/bin/bash

docker run --rm -d --name postgres -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=mypassword -p 5432:5432 postgres

sleep 2

docker exec -it postgres psql -U myuser -c 'CREATE DATABASE restaurant_checkout;'

cd server

docker build --progress=plain -t server .

docker run -d -e PYTHONUNBUFFERED=1 --rm -p 8000:80 server

cd ..

cd client

docker build --progress=plain -t client .

docker run -d --rm -p 5173:5173 client

