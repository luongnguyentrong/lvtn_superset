#!/bin/bash

# Read unit_name from command-line argument
unit_name="$1"

echo "Deploying new superset for unit $unit_name to server..."

# run new superset container
docker compose up superset_$unit_name -d
docker compose exec superset_$unit_name superset db upgrade
docker compose exec superset_$unit_name superset init

# restart nginx container
docker compose down nginx
docker compose up nginx -d