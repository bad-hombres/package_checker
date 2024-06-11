import os
import argparse
import subprocess
import shutil

def generate_sbom(deb_file, output_folder='sboms'):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Construct the command to run syft
    output_file = os.path.join(output_folder, f'sbom_{os.path.basename(deb_file)}.json')
    command = f'syft {deb_file} -o json > {output_file}'
    
    # Run the command
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True)
        if result.returncode == 0:
            print(f"SBOM successfully generated and saved to {output_file}")
        else:
            print(f"Failed to generate SBOM: {result.stderr.decode('utf-8')}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        return False
    
    return output_file

def find_deb_files(directory):
    deb_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.deb'):
                deb_files.append(os.path.join(root, file))
    return deb_files

def clean_sbom_folder(folder='sboms'):
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder)

def main():
    parser = argparse.ArgumentParser(description='Generate SBOM for .deb files in a folder')
    parser.add_argument('folder', metavar='FOLDER', type=str,
                        help='Path to the folder containing .deb files')
    args = parser.parse_args()

    folder_path = args.folder

    if not os.path.isdir(folder_path):
        print(f"Folder not found: {folder_path}")
        return

    # Clean the SBOM folder
    clean_sbom_folder()

    # Find all .deb files in the specified folder
    deb_files = find_deb_files(folder_path)

    if not deb_files:
        print(f"No .deb files found in {folder_path} or its subdirectories.")
        return

    # Generate SBOM for each .deb file
    for deb_file in deb_files:
        sbom_file = generate_sbom(deb_file)
        if sbom_file:
            # Scan SBOM for CVEs
            cve_report = scan_for_cves(sbom_file)
            if cve_report:
                with open(f'{sbom_file}.cve_report.txt', 'w') as report_file:
                    report_file.write(cve_report)

def scan_for_cves(sbom_file):
    # Construct the command to run grype
    command = f'grype sbom:{sbom_file}'
    
    # Run the command
    try:
        result = subprocess.run(command, shell=True, capture_output=True)
        if result.returncode == 0:
            print("CVE Scan Results:")
            print(result.stdout.decode('utf-8'))
            return result.stdout.decode('utf-8')
        else:
            print(f"Failed to scan for CVEs: {result.stderr.decode('utf-8')}")
            return None
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        return None

if __name__ == '__main__':
    main()

