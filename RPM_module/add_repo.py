import argparse
import subprocess

# Function to check if yum-utils is installed
def is_yum_utils_installed():
    try:
        subprocess.check_call(['yum', 'list', 'installed', 'yum-utils'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

# Function to install yum-utils
def install_yum_utils():
    if not is_yum_utils_installed():
        try:
            subprocess.check_call(['yum', 'install', '-y', 'yum-utils'])
        except subprocess.CalledProcessError as e:
            print(f"Error: Failed to install yum-utils - {e}")
    else:
        print("yum-utils is already installed.")

# Function to install a YUM repository using a URL
def install_yum_repository(url):
    try:
        subprocess.check_call(['yum-config-manager', '--add-repo', url])
        print(f"Repository '{url}' has been added successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to add repository '{url}' - {e}")

def main():
    parser = argparse.ArgumentParser(description="Install a YUM repository using a URL.")
    parser.add_argument('-url', required=True, help="The URL of the YUM repository to install.")

    args = parser.parse_args()

    repository_url = args.url

    # Check if yum-utils is installed; if not, install it
    install_yum_utils()

    # Call the function to install the YUM repository
    install_yum_repository(repository_url)
if __name__ == "__main__":
    main()

