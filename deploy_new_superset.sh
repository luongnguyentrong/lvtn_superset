#!/bin/bash

# Read unit_name from command-line argument
unit_name="$1"

echo "Deploying new superset for unit $unit_name to server..."

# run new superset container
docker compose up $unit_name -d

# restart nginx container
docker compose down nginx
docker compose up nginx -d