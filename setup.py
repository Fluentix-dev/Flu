import os
import sys
import platform
import subprocess
import time


def install_requirements():
    """Install the required packages from requirements.txt."""
    try:
        # Install the required packages from requirements.txt
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt', '--user'])
        print("Successfully installed required packages.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install packages: {e}")
        sys.exit(1)

def create_batch_file(fluentix_path):
    """Create a batch file for Windows."""
    # Check if Python is installed
    try:
        subprocess.check_call(['python', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("[ERROR] Python is not installed or not found in your PATH.")
        print("Please install Python from https://www.python.org/downloads/ and ensure it's added to your PATH.")
        sys.exit(1)

    # Create the batch file content
    batch_file_content = f'@echo off\npy "{fluentix_path}" %*\n'
    batch_file_path = os.path.join(os.environ['USERPROFILE'], 'flu.bat')
    batch_file_path2 = os.path.join(os.environ['USERPROFILE'], 'fl.bat')

    # Write the batch file
    with open(batch_file_path, 'w') as f:
        f.write(batch_file_content)

    with open(batch_file_path2, 'w') as f:
        f.write(batch_file_content)

    # Add the directory to the system's PATH
    user_profile_dir = os.environ['USERPROFILE']
    path_variable = os.environ['PATH']
    if user_profile_dir not in path_variable:
        new_path_variable = f"{user_profile_dir};{path_variable}"
        os.environ['PATH'] = new_path_variable
        print(f"Added {user_profile_dir} to the system's PATH.")

    print(f'[INFO] Batch file created at: {batch_file_path}')
    print('[SUCCESS] You can run Fluentix by typing `flu` or `fl` in your command prompt.')


def create_shell_script(fluentix_path):
    """Create a shell script for Linux or macOS."""
    print("[NOTICE] MAKE SURE THIS SCRIPT IS RAN VIA `sudo` else it won't work.")
    time.sleep(1)
    try:
        subprocess.check_call(['python', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("[ERROR] Python is not installed or not found in your PATH.")
        print("Please install Python from https://www.python.org/downloads/ and ensure it's added to your PATH.")
        sys.exit(1)

    shell_script_content = f'#!/bin/bash\npython "{fluentix_path}" "$@"\n'
    shell_script_path2 = '/usr/local/bin/flu'
    shell_script_path3 = '/usr/local/bin/fl'
    
    with open(shell_script_path2, 'w') as f:
        f.write(shell_script_content)

    with open(shell_script_path3, 'w') as f:
        f.write(shell_script_content)

    os.chmod(shell_script_path2, 0o755)
    os.chmod(shell_script_path3, 0o755)
    
    print('[SUCCESS] You can run it by typing `flu` or `fl` in your terminal.')


def main():
    """Main function to orchestrate the setup process."""
    # Path to the fluentix.py file
    fluentix_path = os.path.abspath("fluentix.py")

    if not os.path.isfile(fluentix_path):
        print("[ERROR] The fluentix.py file does not exist in the current directory.")
        sys.exit(1)

    # Install requirements
    install_requirements()

    # Detect the operating system
    os_type = platform.system()

    if os_type == 'Windows':
        create_batch_file(fluentix_path)
    elif os_type in ['Linux', 'Darwin']:  # Darwin is for macOS
        create_shell_script(fluentix_path)
    else:
        print("Unsupported operating system. This script only supports Windows, macOS, and Linux.")


if __name__ == "__main__":
    main()
