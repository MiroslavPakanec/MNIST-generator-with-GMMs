#!/bin/bash

# Create Docker network
docker network create --driver bridge --opt com.docker.network.bridge.name=bc-net bc-net

# Navigate to the client directory and run the shell script
cd client
./restart_linux.sh

# Navigate back to the root directory
cd ..

# Navigate to the service directory and run the shell script
cd service
./restart_linux.sh

# Navigate back to the root directory
cd ..