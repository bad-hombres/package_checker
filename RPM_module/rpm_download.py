import subprocess
import os

def main():
    package_list_file = "/root/input.txt"
    download_directory = "/root/packages-download"
    log_file = "download_log.log"

    # Read package names from the file
    with open(package_list_file, 'r', encoding='utf-8') as f:
        package_names = [line.strip() for line in f]

    # Create the download directory if it doesn't exist
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
                log.write(f"Download Status: {'Success' if result else 'Failure'}\n\n")

        print("Packages downloaded successfully to:", download_directory)

        # Scan for vulnerabilities in downloaded packages
        vulnerabilities_log = "vulnerabilities_log.log"
        scan_for_vulnerabilities(download_directory, vulnerabilities_log)
        print("Vulnerability scan completed. Check vulnerabilities_log.log for results.")

    except subprocess.CalledProcessError as e:
        print("Error executing command:")
        print(e)

def download_package(package_name, download_directory):
    # Construct the yum command to download the package
    yum_command = ["yum", "-y", "install", "--downloadonly", "--downloaddir", download_directory, package_name]

    # Execute the yum command using subprocess
    process = subprocess.Popen(yum_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    return process.returncode == 0

def scan_for_vulnerabilities(directory, vulnerabilities_log):
    with open(vulnerabilities_log, 'w', encoding='utf-8') as log:
        for filename in os.listdir(directory):
            if filename.endswith('.rpm'):
                vulnerabilities = scan_package_vulnerabilities(os.path.join(directory, filename))
                log.write(f"Package: {filename}\n")
                log.write(f"Vulnerabilities:\n{vulnerabilities}\n\n")

def scan_package_vulnerabilities(rpm_file_path):
    try:
        changelog_output = subprocess.check_output(["rpm", "-q", "--changelog", "-p", rpm_file_path], stderr=subprocess.PIPE)
        changelog_output = changelog_output.decode('utf-8')  # Decode the output to a string
        return changelog_output
    except subprocess.CalledProcessError as e:
        return "Error retrieving changelog: " + e.stderr.decode('utf-8')

if __name__ == "__main__":
    main()

