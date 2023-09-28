#!/bin/bash

#script version, update each time you release change to dockerfile
script_version="0.2"


# Check if Docker is installed
if ! [ -x "$(command -v docker)" ]; then
  echo "Docker is not installed. Please install Docker to use this script."
  exit 1
fi

#getting grype
if ! [ -x "$(command -v grype)" ]; then
  echo "Grype is not installed. Password is required to install grype..."
  sudo curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sudo sh -s -- -b /usr/local/bin
fi

# Get the absolute path of the current directory
CURRENT_DIR=$(pwd)

# Function to display usage information
usage() {
  echo "Usage: $0 -r [7|8|9] [-u INPUT]"
  echo "  -r [7|8|9] : Download for specific RedHat (required)"
  echo "  -u INPUT : Specify additional repository to install for download."
  exit 1
}

# Variables to store user input via flag. this will be used to install new repo
new_repo_input=""
flag_provided=false
r_option=""

# Parse command-line options
while getopts "r:u:" opt; do
  case $opt in
    r)
      case "$OPTARG" in
        7|8|9)
          r_option="$OPTARG"
#          flag_provided=true
          ;;
        *)
          usage
          ;;
      esac
      ;;
    u)
      new_repo_input="$OPTARG"
      ;;
    *)
      usage
      ;;
  esac
done

# Check if the -r flag is provided
if [ -z "$r_option" ]; then
  echo "Error: The -r flag is required (must be 7, 8, or 9)."
  usage
fi

# Shift to the next argument after the options
shift $((OPTIND-1))

# Perform the action based on the -r option
case "$r_option" in
  
  7)
    echo "Performing action R7"
    #check if custom repo flag was provided
    if [ -n "$new_repo_input" ]; then
       echo "CUSTOM REPO INSTALLED: $new_repo_input"
       docker build -t rpm_module_r7:$script_version --build-arg OS_VERSION="centos:7" --build-arg ARG_REPO=$new_repo_input $CURRENT_DIR
    else
      # Check if the 'rpm_module_r7:[version]' image exists and buid it if it does not
      if ! docker image inspect rpm_module_r7:$script_version > /dev/null 2>&1; then
        docker build -t rpm_module_r7:$script_version --build-arg OS_VERSION="centos:7" $CURRENT_DIR
      fi
    fi
    # Run the Docker and mount local directory onto the container
    docker run -v $PWD:/root -it --rm rpm_module_r7:$script_version
    
    grype dir:./packages-download --distro rhel:7 -o table > vulnerablity_scan.log
    ;;
  
  8)
    echo "Performing action R8"
    #check if custom repo flag was provided
    if [ -n "$new_repo_input" ]; then
       echo "CUSTOM REPO INSTALLED: $new_repo_input"
       docker build -t rpm_module_r8:$script_version --build-arg OS_VERSION="registry.access.redhat.com/ubi8/ubi:latest" --build-arg ARG_REPO=$new_repo_input $CURRENT_DIR
    else
      # Check if the 'rpm_module_r8:[version]' image exists and buid it if it does not
      if ! docker image inspect rpm_module_r8:$script_version > /dev/null 2>&1; then
        docker build -t rpm_module_r8:$script_version --build-arg OS_VERSION="registry.access.redhat.com/ubi8/ubi:latest" $CURRENT_DIR
      fi
    fi
    # Run the Docker and mount local directory onto the container
    docker run -v $PWD:/root -it --rm rpm_module_r8:$script_version
    grype dir:./packages-download --distro rhel:8 -o table > vulnerablity_scan.log
    ;;
  
  9)
   
    echo "Performing action R9"
    #check if custom repo flag was provided
    if [ -n "$new_repo_input" ]; then
       echo "CUSTOM REPO INSTALLED: $new_repo_input"
       docker build -t rpm_module_r9:$script_version --build-arg OS_VERSION="registry.access.redhat.com/ubi9-init" --build-arg ARG_REPO=$new_repo_input $CURRENT_DIR
    else
      # Check if the 'rpm_module_r9:[version]' image exists and buid it if it does not
      if ! docker image inspect rpm_module_r9:$script_version > /dev/null 2>&1; then
        docker build -t rpm_module_r9:$script_version --build-arg OS_VERSION="registry.access.redhat.com/ubi9-init" $CURRENT_DIR
      fi
    fi
    # Run the Docker and mount local directory onto the container
    docker run -v $PWD:/root -it --rm rpm_module_r9:$script_version
    grype dir:./packages-download --distro rhel:9 -o table > vulnerablity_scan.log
    ;;

  *)
    ;;
esac 
