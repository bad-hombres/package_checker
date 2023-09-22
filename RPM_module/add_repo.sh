#!/bin/bash

# Initialize the URL variable
repo_url=""

# Check if yum-config-manager is available
if ! command -v yum-config-manager &>/dev/null; then
  echo "yum-config-manager is not installed. installing yum-utils"
  yum install -y yum-utils
fi

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
  key="$1"

  case $key in
    -url)
      repo_url="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $key"
      exit 1
      ;;
  esac
done

# Check if the repository URL is provided
if [ -z "$repo_url" ]; then
  echo "Usage: $0 -url <repository_url>"
  exit 1
fi

# Check if the repository is already enabled
if yum-config-manager --qrepo="$repo_url" | grep -q 'enabled = 1'; then
  echo "Repository is already enabled. Exiting."
  exit 1
fi

# Add the repository using yum-config-manager
yum-config-manager --add-repo="$repo_url"

# Enable the repository
yum-config-manager --enable "$(basename "$repo_url")"

echo "Repository has been added and enabled in YUM."

