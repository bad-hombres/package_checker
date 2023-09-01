#!/bin/bash

#script version, update each time you release change to dockerfile
script_version="0.1"


# Check if Docker is installed
if ! [ -x "$(command -v docker)" ]; then
  echo "Docker is not installed. Please install Docker to use this script."
  exit 1
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

# Variables to store user input and flag to track whether a flag was provided
user_input=""
#flag_provided=false
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
      user_input="$OPTARG"
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
#shift $((OPTIND-1))

  

# If there are any additional arguments
#if [ $# -ne 0 ]; then
#  usage
#fi

# If user input was provided, use it in the code
if [ -n "$user_input" ]; then
  echo "User input: $user_input"
fi

# Perform the action based on the -r option
case "$r_option" in
  
  7)
    echo "Performing action R7"
    # Check if the 'rpm_module_r7:[version]' image exists and buid it if it does not
    if ! docker image inspect rpm_module_r7:$script_version > /dev/null 2>&1; then
      docker build -t rpm_module_r7:$script_version -f $CURRENT_DIR/Dockerfile_r7 $CURRENT_DIR
    fi
      echo "docker image exist"
      #Run the Docker and mount local directory onto the container
      #If user input was provided, use it in the code---------------------------------------------------------update------------------------------------------------------------
      if [ -n "$user_input" ]; then
        echo "User input: $user_input"
        docker run -v $PWD:/root -it --rm rpm_module_r7:$script_version

      fi
        docker run -v $PWD:/root -it --rm rpm_module_r7:$script_version
  

    # Replace this with the actual action you want to perform for option -r 7
    ;;
  
  8)
    echo "Performing action R8"
    # Check if the 'rpm_module_r8:[version]' image exists and buid it if it does not
    if ! docker image inspect rpm_module_r8:$script_version > /dev/null 2>&1; then
      docker build -t rpm_module_r8:$script_version -f $CURRENT_DIR/Dockerfile_r8 $CURRENT_DIR
    fi
      echo "docker image exist"
      # Run the Docker and mount local directory onto the container
      docker run -v $PWD:/root -it --rm rpm_module_r8:$script_version
    ;;
  
  9)
   
    echo "Performing action R9"
    # Check if the 'rpm_module_r9:[version]' image exists and buid it if it does not
    if ! docker image inspect rpm_module_r9:$script_version > /dev/null 2>&1; then
      docker build -t rpm_module_r9:$script_version -f $CURRENT_DIR/Dockerfile_r9 $CURRENT_DIR
    fi
      echo "docker image exist"
      # Run the Docker and mount local directory onto the container
      docker run -v $PWD:/root -it --rm rpm_module_r9:$script_version
    ;;

  *)
    ;;
esac
  
