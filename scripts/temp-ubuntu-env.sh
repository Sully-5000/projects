#!/bin/bash

# Creates temporary ubuntu container for testing scripts.

# Function to clean up the Docker container
cleanup() {
  echo "Cleaning up..."
  docker rm -f $CONTAINER_ID
  echo "Done."
}

# Create a new Docker container from the Ubuntu image and start it
CONTAINER_ID=$(docker run -d ubuntu:latest sleep infinity)

# Use trap to clean up the container when the script exits
trap cleanup EXIT

# Update package lists in the container, then install vim
docker exec -it $CONTAINER_ID bash -c "apt-get update && apt-get install -y vim"

# Open a bash shell in the container
docker exec -it $CONTAINER_ID bash