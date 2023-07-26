#!/bin/bash

# Creates temporary ubuntu container

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

# Update package lists in the container, then install vim and necessary dependencies for oh-my-zsh
docker exec -it $CONTAINER_ID bash -c "apt-get update && apt-get install -y vim curl wget git zsh"

# Install oh-my-zsh
docker exec -it $CONTAINER_ID bash -c "sh -c \"\$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)\" \"\" --unattended"

# Change the theme to 'dst'
docker exec -it $CONTAINER_ID bash -c "sed -i 's/ZSH_THEME=\"robbyrussell\"/ZSH_THEME=\"random\"/' ~/.zshrc"

# Open a bash shell in the container
docker exec -it $CONTAINER_ID zsh