# Flask_API

sudo docker run --name catalog_db -e POSTGRES_PASSWORD=123456 -e POSTGRES_DB=gregdb -p 5432:5432 -d postgres

sudo docker build -t flask_catalog:latest .

sudo  docker run --link catalog_db:postgres -d -p 5002:5000 flask_catalog