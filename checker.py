import os
import sys
import argparse


sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

def load_module(module_name):
    try:
        module = __import__(module_name)
        return module
    except ImportError as e:
        print(f"Error loading module '{module_name}': {e}")
        return None


def main(file_name, architecture, pkg_type):
    if architecture:
        arch_msg = f" using architecture '{architecture}'"
    else:
        arch_msg = " using the default architecture"

    if pkg_type:
        pkg_msg = f" and packaging type '{pkg_type}'"
    else:
        pkg_msg = ""

    loaded_module = load_module(pkg_type)
    if loaded_module:
        print(f"Module '{pkg_type}' loaded successfully!")
        print(loaded_module.init(file_name, architecture))

    print(f"Processing file '{file_name}'{arch_msg}{pkg_msg}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a file with optional architecture and packaging type")

    parser.add_argument("file", type=str, help="Path to the file to process")
    parser.add_argument("--arch", type=str, choices=["x86", "x64", "arm"], help="Architecture to use (x86, x64, arm)")
    parser.add_argument("--pkg_type", type=str, help="Packaging type to use (zip, tar, exe)")

    args = parser.parse_args()

    main(args.file, args.arch, args.pkg_type)

