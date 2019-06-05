#!/bin/sh -e

echo "Creating database..."

DATABASE=postgres://$POSTGRES_USER:$POSTGRES_PASSWORD@pg:$POSTGRES_PORT
echo "CREATE DATABASE $POSTGRES_DB "| psql $DATABASE?sslmode=disable

echo "Creating schemas..."
psql $DATABASE?sslmode=disable < /migrations/schema.sql

echo "Creating store procedures..."
psql  $DATABASE?sslmode=disable < /migrations/stores.sql

echo "Populating tables..."
psql  $DATABASE?sslmode=disable < /migrations/populate.sql