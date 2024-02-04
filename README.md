# Command to run PostgreSQL in Docker:

docker run --name fastapi-postgres -p 5432:5432 -e POSTGRES_PASSWORD=admin -e POSTGRES_DB=fastapi_db -d postgres