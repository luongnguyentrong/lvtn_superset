#!/bin/bash

# Check if the unit name argument is provided
if [ -z "$1" ]; then
  echo "Please provide the unit name as the first argument."
  exit 1
fi

# Get the unit name from the first command-line argument
unit_name=$1

# Set the Docker context as the unit name folder
docker_context="./$unit_name"

# Construct the Docker repository URL
docker_repository="ducluongvn/superset_$unit_name"

# Build the Docker image
docker build -t $docker_repository "$docker_context"

# Log in to the Docker repository using access token from environment variable
echo "$DOCKER_TOKEN" | docker login --username ducluongvn --password-stdin

# Push the Docker image to the repository
docker push "$docker_repository"
