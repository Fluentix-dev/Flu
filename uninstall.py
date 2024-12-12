import os
import sys
import platform
import subprocess

def uninstall_requirements():
    """Uninstall the required packages specified in requirements.txt."""
    try:
        # Uninstall the required packages listed in requirements.txt
        subprocess.check_call([sys.executable, '-m', 'pip', 'uninstall', '-r', 'requirements.txt', '--yes'])
        print("[SUCCESS] Successfully uninstalled required packages.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to uninstall packages: {e}")
        sys.exit(1)

def remove_batch_file():
    """Remove the Windows batch file (fluentix.bat) if it exists."""
    batch_file_path = os.path.join(os.environ['USERPROFILE'], 'flu.bat')
    batch_file_path2 = os.path.join(os.environ['USERPROFILE'], 'fl.bat')

    if os.path.isfile(batch_file_path):
        os.remove(batch_file_path)
    else:
        print('[WARNING] No batch file found to remove.')

    if os.path.isfile(batch_file_path2):
        os.remove(batch_file_path2)
    else:
        print('[WARNING] No batch file found to remove.')
    
    print('[SUCCESS] Batch file removed.')

def remove_shell_script():
    """Remove the shell script (fluentix) in /usr/local/bin if it exists."""
    shell_script_path = '/usr/local/bin/fluentix'
    if os.path.isfile(shell_script_path):
        os.remove(shell_script_path)
        print('[SUCCESS] Shell script removed.')
    else:
        print('[WARNING] No shell script found to remove.')

def main():
    """Main function to orchestrate the uninstallation process."""
    # Uninstall requirements
    uninstall_requirements()

    # Detect the operating system
    os_type = platform.system()

    if os_type == 'Windows':
        remove_batch_file()
    elif os_type in ['Linux', 'Darwin']:  # Darwin is for macOS
        remove_shell_script()
    else:
        print("[ERROR] Unsupported operating system. This script only supports Windows, macOS, and Linux.")

if __name__ == "__main__":
    main()
