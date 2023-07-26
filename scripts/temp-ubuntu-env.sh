#!/bin/bash

# Creates temporary Ubuntu container

# Function to animate hourglass while process is running
spin() {
  local -r chars="/-\|"

  while :; do
    for (( i=0; i<${#chars}; i++ )); do
      sleep 0.5
      echo -en "${chars:$i:1}" "\r"
    done
  done
}


# Function to clean up the Docker container
cleanup() {
  echo "Deleting container..."
  docker rm -f $CONTAINER_ID
  echo "Done."
}

# Create a new Docker container from the Ubuntu image and start it
CONTAINER_ID=$(docker run -d ubuntu:latest sleep infinity)

# Use trap to clean up the container when the script exits
trap cleanup EXIT

echo "Sandbox being created..."

# Start the spinner in the background
spin &
# Save its PID
SPIN_PID=$!

# Update package lists in the container, then install vim, apt-utils, and necessary dependencies for oh-my-zsh
docker exec $CONTAINER_ID bash -c "apt-get update > /dev/null 2>&1 && apt-get install -y vim curl wget git zsh apt-utils > /dev/null 2>&1"

# Install oh-my-zsh
docker exec $CONTAINER_ID bash -c "sh -c \"\$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh) > /dev/null 2>&1\" \"\" --unattended"

# Change the theme to 'random'
docker exec $CONTAINER_ID bash -c "sed -i 's/ZSH_THEME=\"robbyrussell\"/ZSH_THEME=\"random\"/' ~/.zshrc > /dev/null 2>&1"

# Kill the spinner
kill $SPIN_PID

# Print a welcome message
docker exec $CONTAINER_ID bash -c "echo 'Welcome! You are now inside your sandbox. This environment will be deleted upon exiting.' > /etc/motd"

# Open a zsh shell in the container, with the welcome message
docker exec -it $CONTAINER_ID bash -c 'zsh -c "cat /etc/motd; exec zsh"'
