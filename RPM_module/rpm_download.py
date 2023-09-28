import subprocess
import shutil
import os

def main():
    package_list_file = "/root/input.txt"
    download_directory = "/root/packages-download"
    log_file = "download_log.log"

    # Read package names from the file
    with open(package_list_file, 'r', encoding='utf-8') as f:
        package_names = [line.strip() for line in f]

    # check if the download directory exist and if it is delete it. then create new directory. this is so we get rid of old packages
    if os.path.exists(download_directory):
        shutil.rmtree(download_directory)

    os.makedirs(download_directory, exist_ok=True)

    try:
        download_status = {}

        for package_name in package_names:
            download_result = download_package(package_name, download_directory)
            download_status[package_name] = download_result

        # create Log file
        with open(log_file, 'w', encoding='utf-8') as log:
            for package_name, result in download_status.items():
                log.write(f"Package: {package_name}\n")
                log.write(f"Download Status: {'Success' if result[0] else 'Failure'}\n")
                if not result[0]:
                    log.write(f"Download Error: {result[1]}\n")
                log.write("\n")

        print("Packages downloaded successfully to:", download_directory)
        cleanup_download_dir(download_directory)

    except subprocess.CalledProcessError as e:
        print("Error executing command:")
        print(e)

def download_package(package_name, download_directory): 
    specific_package_directory  = download_directory + "/" + package_name
    # Construct the yum command to download the package
    yum_command = ["yum", "-y", "install", "--downloadonly", "--downloaddir", specific_package_directory, package_name]

    # Execute the yum command using subprocess
    process = subprocess.Popen(yum_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode == 0:
        return True, None
    else:
        error_message = stderr.decode('utf-8').strip() if stderr else "Unknown error"
        return False, f"Download failed for '{package_name}': {error_message}"



# Go throught the files in download directory and delete the empty ones. this is because yum creates directory even if the download is unsuccessful
def cleanup_download_dir(directory):
    for dirpath, dirnames, filenames in os.walk(directory, topdown=False):
        for dirname in dirnames:
            dir_to_check = os.path.join(dirpath, dirname)
            if not os.listdir(dir_to_check):
                os.rmdir(dir_to_check)
                print(f"Deleted empty directory: {dir_to_check}")

if __name__ == "__main__":
    main()

