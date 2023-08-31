#!/bin/bash

# Check if Docker is installed
if ! [ -x "$(command -v docker)" ]; then
  echo "Docker is not installed. Please install Docker to use this script."
  exit 1
fi

# Get the absolute path of the current directory
CURRENT_DIR=$(pwd)

# Check if the 'rpm_module:0.1' image exists and buid it if it does not
if ! docker image inspect rpm_module:0.1 > /dev/null 2>&1; then
  docker build -t rpm_module:0.1 $CURRENT_DIR
fi
  echo "docker image exist"
  # Run the Docker and mount local directory onto the container
  docker run -v $PWD:/root -it --rm rpm_module:0.1
  