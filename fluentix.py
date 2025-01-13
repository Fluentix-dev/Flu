try:
    """Imports"""
    import os # operating sys stuff
    import random # random verify codes
    import zipfile # zip manager
    import urllib3 # download package
    import platform
    from fluentixengine import upload # upload package
    from fluentixengine.packages import search_package, insert_data, search_owner, delete_package, search_link, edit_package # get package
    from fluentixengine.sendmail import send_email # send package

    if platform.system() == "Windows":
        from pyreadline3 import Readline
        readline = Readline()
    else:
        import readline

    import sys # system stuff
    import shutil # delete stuff
    import re # email thing
    from colorama import Fore, Style, init # colored text baby
    import subprocess
    import time
except:
    import sys
    sys.stdout.write("[INSTALL-ERROR#1] Fluentix is incorrectly installed, refer to https://docs.fluentix.dev/install to retry.")
    sys.exit(1)

init()

# Help text for commands
help_text = """--------------------------------------------------------------
Fluentix v0.0.1 - Command Reference (https://docs.fluentix.dev/console)
│
├── General Commands: (More info at https://docs.fluentix.dev/console/commands)
│   ├── version                 : Display the current version of Fluentix.
│   ├── credits                 : Show the owner + contributors to Fluentix.
│   ├── check                   : Verify if Fluentix is installed correctly.
│   ├── help <command>          : Display detailed help for a specific command.
│   ├── exit                    : Exit the Fluentix runtime.
│   ├── clean                   : Clear the terminal/command prompt.
│   └── alias <mode> <command> <shortcut> : Create/manage shortcuts for commands.
│       ├── -show   : List all existing shortcuts.
│       └── -manage : Modify or delete shortcuts.
│   
├── Runtime:
│   └── -runtime                : Enters Fluentix's runtime.
│
├── Code Execution: (More info at https://docs.fluentix.dev/console)
│   ├── <file.flu/file.fl> <args...> : Execute a Fluentix file with optional arguments.
│   └── execute                      : Lively executes Fluentix code on console.
│
├── Package Management: (More info at https://docs.fluentix.dev/console/packages)
│   ├── installed               : List all installed packages.
│   ├── install <pkg1>, <pkg2>...: Install packages from the Fluentix library.
│   ├── uninstall <pkg1>, <pkg2>...: Uninstall packages from your computer.
│   ├── reinstall <pkg1>, <pkg2>...: Reinstall packages.
│   ├── upload <dir> <email>    : Upload a package to the Fluentix library. 
│   ├── upload-template         : Generate a package upload template.
│   └── manage-packages <email> : Manage your uploaded packages via email.
│
└── Updates: (WIP)
   └── update [version]        : Update Fluentix. Specify a version (e.g., "update 0.0.1") 
                                 or omit for the latest version.

Need Help?
Visit our FAQs: https://docs.fluentix.dev
--------------------------------------------------------------"""


# Unpack shortcuts._fluentix_
try:
    with open(os.path.dirname(os.path.realpath(__file__)) + '/fluentixdata/shortcuts._fluentix_', 'r') as f:
        shortcuts = f.read().split('\n')
except FileNotFoundError:
    shortcuts = ""

commands = ["help", "credits", "upload", "version", "installed", "update", "install", "uninstall", "reinstall", "manage-packages", "manage-package","clean", "alias", "upload-template", "check", "execute"]
subcommands = ["-runtime"]

def clean_console():
    """Clears the console output."""
    if os.name == 'nt':  # For Windows
        subprocess.run('cls')
    else:  # For Unix/Linux/Mac
        subprocess.run('clear')

def reinstall(package):
    """Reinstalls package."""
    uninstall_package(package)
    install_package(package)

    return "s"

def print_progress_bar(iteration, total, length=50):
    """Print a progress bar to the console."""
    percent = (iteration / total) * 100
    filled_length = int(length * iteration // total)
    bar = '*' * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r[PROGRESS] |{bar}| {percent:.2f}%')
    sys.stdout.flush()

def zip_folder(folder_path, zip_file_path):
    """Zip a directory for upload."""
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        total_files = sum(len(files) for _, _, files in os.walk(folder_path))
        current_file = 0
        
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(file_path, os.path.relpath(file_path, folder_path))
                current_file += 1
                print_progress_bar(current_file, total_files)  # Update progress bar
    
    print()  # New line after progress bar completion
    return f"[INFO] Folder '{folder_path}' has been zipped into '{zip_file_path}'."

def is_valid_email(email):
    """Validate the email address using a regex pattern."""
    # Ensure the input is a string
    if not isinstance(email, str):
        return False
    
    # Define the regex pattern for a valid email
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # Use re.match to check if the email matches the pattern
    return re.match(pattern, email) is not None

def unzip_file(zip_file_path, destination):
    """Unzips the downloaded zip file into the destination directory."""
    try:
        os.makedirs(destination, exist_ok=True)
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(destination)
        return f"[INFO] Unzipped package to {destination}"
    except Exception as e:
        return Fore.RED + f"[ZIP-ERROR] An error occurred while unzipping: {e}\nThe module might have some problem with it's zip, please contact the dev at " + Fore.YELLOW + search_package(os.path.splitext(os.path.basename(zip_file_path))[0])
    
def download_file(name, url, zip_path=os.path.dirname(os.path.realpath(__file__))+"packages/my_package.zip"):
    """Downloads a file from a URL and unzips it."""
    # Ensure name is used correctly
    package_name = name  # Assuming name is the package name directly
    zip_dir = os.path.dirname(zip_path)
    os.makedirs(zip_dir, exist_ok=True)
    temp_file_path = f'{package_name}.zip'  # Use package_name directly

    http = urllib3.PoolManager()
    try:
        response = http.request('GET', url)
        if response.status == 200:
            with open(temp_file_path, 'wb') as f:
                f.write(response.data)
            sys.stdout.write(f"[INFO] Downloaded data from {url} to {temp_file_path}\n")
            sys.stdout.write(unzip_file(temp_file_path, package_name) + "\n")  # Unzip with the correct name
            shutil.move(package_name, 'packages')
            return Fore.GREEN + f"[SUCCESS] Downloading proccess completed."
        else:
            sys.stdout.write(Fore.YELLOW + f"[WARNING] Failed to download file. HTTP Status: {response.status}\n")

    except Exception as e:
        sys.stdout.write(Fore.RED + f"[ERROR] An error occurred: {e}\n")

def verify_email(email):
    """Handle email verification process."""
    if email is None:
        email = input("Enter your email: ")
        if email.lower() == 'x':
            return False
    
    attempt = 0
    clean_console()
    sys.stdout.write("--------------------------------------------------------------\n")
    sys.stdout.write("VERIFY YOUR EMAIL TO CONTINUE")

    try:
        answer_code = random.randint(100000, 999999)
        sys.stdout.write(send_email(email, answer_code) + "\n")
    except Exception as e:
        sys.stdout.write(Fore.RED + "[EMAIL-ERROR#1] Error occurred while sending email, please check your email address validation and try again\n")
        return verify_email(None) # Return the result of the recursive call

    sys.stdout.write(Fore.GREEN + "[SUCCESS] " + Fore.WHITE + "A six-digit code was sent to your email, " + Fore.YELLOW + "remember to check your spam.\n")
    sys.stdout.write(Fore.WHITE + "[INFO] Type '-1' to re-enter email address, 'x' to cancel.\n")

    while True:
        code = input(Fore.WHITE + "[INPUT] Enter the 6-digit verification code: ")
        if code == "-1":
            sys.stdout.write(Fore.WHITE + "[INFO] Re-enter your email\n")
            return verify_email(email=None)  # Return the result of the recursive call
        elif code == str(answer_code):
            sys.stdout.write(Fore.GREEN + "[SUCCESS]" + Fore.YELLOW + " Authentication complete.\n" + Fore.WHITE)
            return email
        elif code.lower() == 'x':
            return
        elif attempt == 5:
            sys.stdout.write(Fore.YELLOW + "[WARNING] Maximum of 5 attempts reached. Stopping..." + Fore.WHITE)
        else:
            sys.stdout.write(Fore.YELLOW + "[WARNING] Wrong code, try again!\n" + Fore.WHITE)
            attempt += 1

def manage_selected_package(package, email):
    """Manage the selected package."""
    package_name = package[1]
    package_version = package[2]
    package_description = package[3]
    package_owner = package[4] 

    o = True

    while True:

        if o == True:
            if os.name == 'nt':  # For Windows
                os.system('cls')
            else:  # For Unix/Linux/Mac
                os.system('clear')

        if o == False:
            break

        sys.stdout.write("--------------------------------------------------------------\n")
        sys.stdout.write(f"Managing {package_name} (Version {package_version}):\n")
        sys.stdout.write("[U] - Update: Use this option if you've updated this package and want to publish a new version of it.\n")
        sys.stdout.write("[I] - Information: Edit its information and ownership.\n")
        sys.stdout.write("[D] - Delete: Delete the package from the database as well as unpublish it.\n")
        sys.stdout.write("[C] - Copy: Get a copy of the zip of this package.\n")
        sys.stdout.write("[X] - Exit: Exit this menu.\n")
        option = input("Enter your option: ").strip().upper()
        
        if option == 'U':
            clean_console()
            sys.stdout.write("--------------------------------------------------------------\n")
            c = input("Enter path of your package: ")
            upload_package(c, email, check=False)
            delete_package(package_name, email)
            sys.stdout.write("Updating Completed")
            clean_console()
            
        elif option == 'I':

            changes = False

            while True:
                clean_console()
                sys.stdout.write("--------------------------------------------------------------\n")
                sys.stdout.write(f"Editing information for package: {package_name}...\n")
                sys.stdout.write(f"[1] Package Name: {package_name}\n")
                sys.stdout.write(f"[2] Package Version: {package_version}\n")
                sys.stdout.write(f"[3] Package Description: {package_description}\n")
                sys.stdout.write(f"[4] Package Ownership: {package_owner}\n")
                if not changes:
                    sys.stdout.write("[S] Save: Save changes and exit.\n")
                else:
                    sys.stdout.write("[S] Save: Save changes and exit (UNSAVED CHANGES).\n")

                sys.stdout.write("[X] Exit: Exit without saving.\n")
                
                edit_option = input("Select an option to edit or save: ").strip().upper()
                
                if edit_option == '1':
                    clean_console()
                    sys.stdout.write("--------------------------------------------------------------\n")
                    sys.stdout.write("[INFO] Type '_X_' to discard changes\n")
                    new_name = input("Enter new package name: ")
                    if new_name.lower() != '_x_':
                        package_name = new_name  # Update the variable to reflect the change
                        changes = True
                        clean_console()
                    else:
                        clean_console()
                elif edit_option == '2':
                    sys.stdout.write("--------------------------------------------------------------\n")
                    clean_console()
                    sys.stdout.write("[INFO] Type '_X_' to discard changes\n")
                    new_version = input("Enter new package version: ")
                    if new_version.lower() != '_x_':
                        package_version = new_version  # Update the variable to reflect the change
                        changes = True
                        clean_console()
                    else:
                        clean_console()
                elif edit_option == '3':
                    sys.stdout.write("--------------------------------------------------------------\n")
                    clean_console()
                    sys.stdout.write("[INFO] Type '_X_' to discard changes\n")
                    new_description = input("[INPUT] Enter new package brief description: ")
                    if new_description.lower() != '_x_':     
                        changes = True
                        package_description = new_description  # Update the variable to reflect the change
                        clean_console()
                    else:
                        clean_console()
                elif edit_option == '4':
                    clean_console()
                    sys.stdout.write("--------------------------------------------------------------\n")
                    sys.stdout.write("[INFO] Type '_X_' to discard changes\n")
                    new_owner = input("Enter new package owner: ")
                    if new_owner.lower() != '_x_':
                        changes = True
                        package_owner = new_owner  # Update the variable to reflect the change
                        clean_console()
                    else:
                        clean_console()
                elif edit_option == 'S' or edit_option == "s":
                    # Save changes to the database
                    if len(package_name) < 30 and len(package_version.split('.')) <= 4 and len(package_description[2]) < 300:
                        edit_package(package[1], package_name, package_version, package_description, package_owner)
                        clean_console()
                        sys.stdout.write(Fore.GREEN + "[SUCCESS] Saved changes.")
                        break  # Exit editing menu
                elif edit_option.lower() == 'x':
                    if changes:
                        option = input("Are you sure? (y/n): ")
                        if option == "Y" or option == "y":
                            sys.stdout.write("[INFO] Exiting without saving changes.\n")
                        else:
                            clean_console()
                            continue
                    break  # Exit editing menu
                else: 
                    sys.stdout.write("Invalid option. Please select a valid option.\n")
        
        elif option == 'D':
            confirm = input("Are you sure you want to delete this package? (Y/N): ")
            if confirm in ("y", "Y"):
                try:
                    link = search_package(package_name)[0][0]
                    upload.delete(link)
                    delete_package(package_name)
                except TypeError:
                    sys.stdout.write(Fore.RED + "[ERROR] Package does not exists.\nMaybe new data about that package was updated from database, type 'n' and retry.\n")
                    time.sleep(1)
                    clean_console()
                    return
                
            else:
                i = input("Continue to stay in this dialog? (Y/N): ")
                if i == "N" or i == "n":
                    o = True
                    break

        elif option == 'C':
            clean_console()
            sys.stdout.write("--------------------------------------------------------------\n")
            install_package(package_name)
            clean_console()
        elif option == 'X':
            sys.stdout.write("[INFO] Exiting management menu.\n")
            return "exit"
        else:
            sys.stdout.write(Fore.YELLOW + "[WARNING] Invalid option. Please enter a valid option.\n")
    
    return "quit"

def manage_uploads(email):
    """Manage uploaded packages by email."""
    email = verify_email(email)
    if not email:
        return 
    
    have_packages = search_owner(email)
    
    if not have_packages:
        return Fore.YELLOW + f"[WARNING] No packages found inside mail {email}. Either re-enter mail by typing 'manage-uploads <mail>' or upload a package by typing 'upload <dir>'. More info on http://docs.fluentix.dev/upload/no-package-mail"

    sys.stdout.write("--------------------------------------------------------------\n")
    sys.stdout.write(f"Owner: {email}\n")
    sys.stdout.write("Uploaded packages: \n")
    
    def printi():
        for index, package in enumerate(have_packages, start=1):
            package_name = package[1]  # The name of the package
            package_version = package[2]  # The version of the package
            sys.stdout.write(f"[{index}] {package_name}: {package_version}\n")
        sys.stdout.write(f"[X] Close\n")
        choice = input("Type the number of the desired package to manage it: ")
        return choice

    # Prompt user to select a package by number
    choice = printi()
    
    while True:
        if choice == "x" or choice == "X":
            clean_console()
            return ""
        try:
            choice_index = int(choice) - 1
            if 0 <= choice_index < len(have_packages):
                selected_package = have_packages[choice_index]
                stop = manage_selected_package(selected_package, email)
                if stop == "quit" or stop == "exit":
                    clean_console()
                    break

        except ValueError:
            sys.stdout.write(Fore.YELLOW + "[WARNING] Invalid option, try again.\n" + Fore.WHITE)
            time.sleep(1)
            clean_console()
            choice = printi()

def upload_template(dir):
    if dir == None:
        dir = os.getcwd()
    try:
        shutil.copytree(os.path.dirname(os.path.abspath(__file__))+"/template", dir, symlinks=False, ignore=None, ignore_dangling_symlinks=False, dirs_exist_ok=True)
        sys.stdout.write(Fore.GREEN + f"[SUCCESS] Upload template has successfully copied to {dir} !")
    except NotADirectoryError:
        sys.stdout.write(Fore.RED + "[NOT-A-DIR-ERROR] Not a directory, please double check the sent path.\n" + Fore.WHITE + "More info at: " + Fore.BLUE + "http://docs.fluentix.dev/not-a-dir")
        return

def upload_package(dir, email, check=True):
    """Uploads a package after verifying ownership."""
    if check == True:
        email = verify_email(email)
        if not email:
            return 
    
    try:
        with open(os.path.join(dir, "details.fluentix-package"), "r") as f:
            info = f.read().split('\n')  # Corrected to split by newline
    except FileNotFoundError:
        sys.stdout.write(Fore.RED + f"[UPLOAD-ERROR#1] Error, no 'details.fluentix-package' found in dir {Fore.YELLOW + dir + Fore.RED}, try again. Run 'flu upload-template' for upload template.\n")
        sys.stdout.write(Fore.WHITE + f"More info on " + Fore.BLUE + "http://docs.fluentix.dev/upload/no-fluentix-package-file\n")
        exit(1)

    data = [line.split() for line in info]
    data[2] = ' '.join(data[2][1:])  # Clean up description

    package_name = ' '.join(data[0][1:])
    if search_package(package_name):
        return Fore.YELLOW + f"[WARNING] Package with name '{package_name}' already exists. Please choose a different name.\n"

    # Ensure the zip file is named correctly
    zip_file_path = os.path.join(dir, f"{package_name}.zip")  # Use package_name for the zip file
    zip_folder(dir, zip_file_path)  # Pass the correct zip file path
    download_link = upload.main(zip_file_path)  # Use the correct zip file path
    # Check of package_name, package_version, package_description length be4 upload
    if len(package_name) < 30 and len(data[1][1].split('.')) <= 4 and len(data[2]) < 300:
        insert_data(download_link, package_name, data[1][1], data[2], email)
        os.remove(zip_file_path)
        return Fore.GREEN + "[SUCCESS] Upload completed!\nYou can verify if your package if live by visiting " + Fore.CYAN + "https://search.fluentix.dev" + Fore.WHITE
    else:
        return Fore.RED + """[UPLOAD-ERROR#3] Rejected upload, make sure the 'details.fluentix-package' has satisfied the requirements.
More info at """ + Fore.CYAN + "http://docs.fluentix.dev/rejected-upload"

def install_package(package):
    """Installs a package by retrieving its link from the database."""
    package_info = search_package(package)
    if not package_info:
        return Fore.RED + f"[INSTALL-ERROR#1] Package '{package}' not found in the database.\nSearch for packages in " + Fore.CYAN + "http://lib.fluentix.dev/"

    name = package
    with open(os.path.dirname(os.path.realpath(__file__)) + '/fluentixdata/installed._fluentix_', 'r') as f:
        installed = f.read().splitlines()
        
    if name in installed:
        return Fore.YELLOW + f"[WARNING] Package '{name}' already installed. To update, type: 'update {name}'."

    package_link = package_info[0][0]
    sys.stdout.write(f"[INFO] Downloading package from {package_link}...\n")
    result = download_file(package, package_link)
    
    if result is None:
        return Fore.RED + f"[INSTALL-ERROR#1] Failed to install package '{package}'."
    else:
        with open(os.path.dirname(os.path.realpath(__file__)) + '/fluentixdata/installed._fluentix_', 'a') as f:
            f.write(name + '\n')
        
    return Fore.GREEN + f"[SUCCESS] Installation of package {name} is successfully completed."

def uninstall_package(package_name):
    """Uninstalls a package by removing it from the database and filesystem."""
    # First, check if the package is installed
    sets = os.path.dirname(os.path.realpath(__file__))
    with open(sets + '/fluentixdata/installed._fluentix_', 'r') as f:
        installed = f.read().splitlines()

    if package_name not in installed:
        return Fore.YELLOW + f"[WARNING] Package '{package_name}' is not installed.\nSee installed packages: 'flu installed'.\n"

    option = input("Are you sure (y/n): ")
    if option == "Y" or option == "y":
        # Remove the package entry from the installed list
        installed.remove(package_name)
        with open(sets + '/fluentixdata/installed._fluentix_', 'w') as f:
            f.write('\n'.join(installed) + "\n")

        # Remove the package files from the filesystem
        package_path = os.path.join(sets + "/packages", package_name)  # Assuming packages are stored in a 'packages' directory
        if os.path.exists(package_path):
            try:
                shutil.rmtree(package_path)  # Use shutil.rmtree to remove the directory and its contents
                return Fore.GREEN + f"[SUCCESS] " + Fore.YELLOW + f"Package '{package_name}' has been uninstalled successfully."
            except Exception as e:
                return Fore.RED + f"[UNINSTALL-ERROR#1] Error removing package files: {e}"
        else:
            return Fore.YELLOW + f"[WARNING] No files found for package '{package_name}'."
    else:
        return ""

def alias_options(option):
    """Manage alias options."""
    have_shortcuts = False
    with open(os.path.dirname(os.path.realpath(__file__)) + '/fluentixdata/shortcuts._fluentix_', 'r') as f:
        list_functions = f.read().strip().split('\n')
        if len(list_functions) >= 2:
            have_shortcuts = True

    def display_shortcuts(manage=True):
        """Display the available shortcuts."""
        if manage:
            clean_console()
        sys.stdout.write(Fore.WHITE+ "Available shortcuts:\n")
        for i in range(0, len(list_functions), 2):
            sys.stdout.write(f"[{round((i/2)+1)}] {list_functions[i]}: {list_functions[i+1]}\n")
        if manage:
            sys.stdout.write("[X] Cancel.\n")

    if option == '-show':
        if have_shortcuts:
            display_shortcuts(manage=False)
        else:
            sys.stdout.write(Fore.YELLOW + "[ERROR-ALIAS#4] No shortcuts available.\nMore info at http://docs.fluentix.dev/console/alias#error-alias4\n")
        return

    elif option == '-manage':
        if have_shortcuts:
            display_shortcuts()
        else:
            sys.stdout.write(Fore.YELLOW + "[ERROR-ALIAS#4] No shortcuts available.\nMore info at http://docs.fluentix.dev/console/alias#error-alias4\n")
            return
        while have_shortcuts:
            if have_shortcuts:
                display_shortcuts()
            else:
                return Fore.YELLOW + "[WARNING] No shortcuts created.\nMore info at http://docsfluentix.dev/alias"
            selection = input("Enter your selection: ")
            if selection.lower() == "x":
                break
            try:
                selection = int(selection) - 1
                if selection * 2 < len(list_functions):
                    current_shortcut = list_functions[selection * 2]
                    current_command = list_functions[selection * 2 + 1]

                    while True:
                        clean_console()
                        sys.stdout.write(Fore.WHITE + "Managing shortcut: {}\n".format(current_shortcut))
                        sys.stdout.write(f"[S] Edit shortcut's name (current: {current_shortcut})\n")
                        sys.stdout.write(f"[C] Edit command (current: {current_command})\n")
                        sys.stdout.write("[D] Delete this shortcut.\n")
                        sys.stdout.write("[A] Apply changes.\n")
                        sys.stdout.write("[X] Close.\n")
                        op = input("Enter your option: ")

                        if op.lower() == "d":
                            confirm = input("Are you sure you want to delete this shortcut? (y/n): ")
                            if confirm.lower() == "y":
                                del list_functions[selection * 2:selection * 2 + 2]
                                with open(os.path.dirname(os.path.realpath(__file__)) + '/fluentixdata/shortcuts._fluentix_', 'w') as f:
                                    f.write('\n'.join(list_functions))
                                    f.write('\n')

                                sys.stdout.write(Fore.GREEN + "[SUCCESS] Shortcut deleted.\n")
                                break  # Exit the inner loop to refresh the outer loop

                        elif op.lower() == "s":
                            new_name = input("Enter new shortcut name: ")
                            list_functions[selection * 2] = new_name
                            sys.stdout.write(Fore.GREEN + f"[SUCCESS] Shortcut name updated to '{new_name}'.\n")
                            current_shortcut = new_name  # Update the current shortcut variable
                            time.sleep(1)

                        elif op.lower() == "c":
                            new_command = input("Enter new command: ")
                            list_functions[selection * 2 + 1] = new_command
                            sys.stdout.write(Fore.GREEN + f"Command updated to '{new_command}'.\n")
                            current_command = new_command  # Update the current command variable

                        elif op.lower() == "a":
                            with open(os.path.dirname(os.path.realpath(__file__)) + '/fluentixdata/shortcuts._fluentix_', 'w') as f:
                                f.write('\n'.join(list_functions) + "\n")
                            sys.stdout.write(Fore.GREEN + "Changes applied.\n")
                            break  # Exit the inner loop to refresh the outer loop

                        elif op.lower() == "x":
                            sys.stdout.write("Exiting management menu.\n")
                            break

                        # Display updated values immediately
                        clean_console()
                        sys.stdout.write("Managing shortcut: {}\n".format(current_shortcut))
                        sys.stdout.write(f"[S] Edit shortcut's name (current: {current_shortcut})\n")
                        sys.stdout.write(f"[C] Edit command (current: {current_command})\n")
                        sys.stdout.write("[D] Delete this shortcut.\n")
                        sys.stdout.write("[A] Apply changes.\n")
                        sys.stdout.write("[X] Close.\n")

                else:
                    sys.stdout.write(Fore.RED + "[ERROR] Invalid selection. Try again.\n")
                    time.sleep(1)
            except (ValueError, IndexError):
                sys.stdout.write(Fore.RED + "[ERROR] Invalid input. Please enter a valid option.\n")
                time.sleep(1)

def alias(shortcut, command):
    """Creates a shortcut via 'key' and do command when pressed."""
    
    subcommands = ["-show", "-manage"]
    try:
        with open(os.path.dirname(os.path.realpath(__file__)) + '/fluentixdata/shortcuts._fluentix_', 'r') as f:
            list_functions = f.read().split('\n')

    except:
        list_functions = ""

    if shortcut in subcommands:
        alias_options(shortcut)
        return ""

    if command is None or command == "":
        return Fore.RED + "[ERROR-ALIAS#2] No command assigned, try again.\nMore info at http://docs.fluentix.dev/console/alias#error-alias2"
    
    if shortcut is None or shortcut == "":
        return Fore.RED + "[ERROR-ALIAS#2] No command assigned, try again.\nMore info at http://docs.fluentix.dev/console/alias#error-alias2"

    if shortcut in commands or shortcut in list_functions:
        return Fore.RED + f"[ERROR-ALIAS#3] '{shortcut}' is already used. Try again with a different name.\nOr run it by typing 'flu {shortcut}'\nMore info at http://docs.fluentix.dev/alias/error3"

    with open(os.path.dirname(os.path.realpath(__file__)) + '/fluentixdata/shortcuts._fluentix_', 'a') as f:
        f.write(f"{shortcut}\n{command}\n")


    return Fore.GREEN + f"[SUCCESS] Successfully added command '{command}' with shortcut '{shortcut}'!"

def better_help(command):
    
    #commands = ["help", "credits", "upload", "version", "installed", "update", "install", "uninstall", "reinstall", "manage-packages", "manage-package","clean", "alias"]

    functions = {
        "version" : "Command version shows current Fluentix version.\nUsage: flu version\nGet new releases at http://fluentix.dev",
        "credits" : "Shows the developers and contributors of Fluentix.\nUsage: flu credits\nContribute at http://fluentix.dev/contribute",
        "alias" : "Creates shortcut for a command. Best used if command is long.\nUsage: flu alias <shortcut/mode> <command>\nDetailed guide at http://docs.fluentix.dev/alias",
        "installed" : "Shows installed packages.\nUsage: flu installed\nMore info at http://docs.fluentix.dev/installed",
        "check" : "Checks if you have installed Fluentix correctly.\nUsage: flu check\nIf it returns an error, try again at https://docs.fluentix.dev/install",
        "upload" : "(Web version coming soon) Uploads a package from your computer to the database.\nUsage: flu upload <package-directory> <email>\nHow to upload: http://docs.fluentix.dev/upload",
        "update" : "Update packages/Fluentix (if new version found).\nUsage: flu update <fluentix/package1> <package2> ...\nMore info at: http://docs.fluentix.dev/update",
        "install" : "Install packages (if multi packages were given) from Fluentix's database.\nUsage: flu install <package1> <package2> ... \nYou can easily search for packages at http://lib.fluentix.dev",
        "reinstall" : "Reinstall packages (if multi packages were given). That package should be existed on your computer else it can't be performed.\nUsage: flu reinstall <package1> <package2> ...",
        "uninstall" : "Uninstall packages (if multi packages were given). That package should be existed on your computer else it can't be performed.\nUsage: flu uninstall <package1> <package2> ...",
        "manage-packages" : "(Web version coming soon) A place to manage your packages.\nUsage: flu manage-packages <email>\nMore info can be found at: http://docs.fluentix.dev/manage-package",
        "manage-package" : "(Web version coming soon) A place to manage your packages.\nUsage: flu manage-packages <email>\nMore info can be found at: http://docs.fluentix.dev/manage-package",
        "clean" : "Clears out the terminal.\nUsage: flu clean\nMore info can be found at: http://docs.fluentix.dev/clean",
        "exit" : "Exits runtime (only works when using fluentix runtime).\nUsage: (only in fluentix runtime) exit\nMore info: " + Fore.BLUE + "http://docs.fluentix.dev/exit",
        "execute" : "Executes Fluentix code inside cmd/terminal.\nUsage: flu execute\nMore info can be found at http://docs.fluentix.dev/execute#terminal"
    }

    if command in functions:
        return f"""--------------------------------------------------------------
{functions[command]}
--------------------------------------------------------------"""
    
    return None
    
def do_alias(shortcut, command):
    sys.stdout.write(Fore.CYAN + f"[ALIAS] Executing shortcut command '{shortcut}'...\n" + Fore.WHITE)
    cmd = ['flu']
    for command in shortcuts[shortcuts.index(command)].split():
        cmd.append(command)
    result = subprocess.run(cmd, encoding=str)
    try:
        sys.stdout.write(result)
    except TypeError:
        # done
        pass
    
    if "returncode=1" in str(result):
        sys.stdout.write(Fore.RED + f"[ALIAS-ERROR#1] Error occured while running shortcut command '{shortcut}'. \nRefer above to see error, this problem is likely not a problem with 'alias'.\nhttps://docs.fluentix.dev/console/alias#error-alias1")
        return
    else:
        return

def check():
    """Check if fluentix is installed correctly"""
    sys.stdout.write("--------------------------------------------------------------\n")
    point = 0
    sys.stdout.write("[INFO] Running check...\n[INFO] Checking for required modules...\n")
    time.sleep(1)
    try:
        import pymysql
        import urllib3
        import colorama
    except:
        return "[INSTALLATION-ERROR] Modules aren't installed/initialzied correctly.\nRefer to https://docs.fluentix.dev/install for more info.\n"
    # success check
    try:
        sys.stdout.write(Fore.GREEN + "[SUCCESS] Modules installed correctly.\n")
        point += 1
        sys.stdout.write("[INFO] Checking for internet...\n")
        time.sleep(1)
        # checks for internet
        internet = True
        url = 'https://google.com'
        http = urllib3.PoolManager()
        response = http.request('GET', url)
        sys.stdout.write(Fore.GREEN + "[SUCCESS] Internet connection is valid!\n")
        point += 1
    except:
        sys.stdout.write(Fore.YELLOW + "[WARNING] Limited or no internet connection, packages function is restricted.\n")
        internet = False
    # checks for fluentix state
    if internet:
        sys.stdout.write("[INFO] Checking Fluentix's database availability...\n")
        try:
            search_owner("ppthanh216@gmail.com")
            sys.stdout.write(Fore.GREEN + "[SUCCESS] Fluentix's database is good.\n[SUCCESS] Functions related to packages can be used.\n")
            point += 1
        except:
            sys.stdout.write(Fore.RED + "[ERROR] Fluentix's database is temporary down (or maintaince), you can double check your internet or wait a moment.\n")
    else:
        sys.stdout.write("[INFO] Skipping checking Fluentix's database because internet is not available.\n")

    if point == 3:
        sys.stdout.write(Fore.GREEN + "[SUCCESS] Fluentix is successfully installed on your device.\n")
    
    elif point == 0:
        sys.stdout.write(Fore.RED + "[FAILED] Fluentix is not correctly installed on your computer.\nRefer to https://docs.fluentix.dev/install for more info.\n")
    
    else:
        sys.stdout.write(Fore.YELLOW + "[WARNING] Fluentix is partially installed on your computer, but it is limited, try connect to a valid internet.\n")

    sys.stdout.write("[RESULT] Checked and satisfied " + str(point) + "/3 conditions.\n")
    sys.stdout.write("--------------------------------------------------------------\n")
    

def do_func(mode, arguments, cmd):
    """Execute commands based on user input."""
    if mode == "version":
        return "Current version: Fluentix - v0.0.1 Beta"
    
    elif mode == "credits":
        return "Fluentix: Made by @Lam and @iaminfinityiq"
    
    elif mode == "installed":
        # do installed
        try:
            with open(os.path.dirname(os.path.realpath(__file__)) + '/fluentixdata/installed._fluentix_', 'r') as f:
                installed = f.readlines()
            if not installed:
                return Fore.YELLOW + "[NOTICE] No packages installed right now, how about installing one?"
            
            if installed[0] != "\n":
                return "Installed packages: " + "\n".join(pkg.strip() for pkg in installed)
            
            else:
                return "[NOTICE] No packages have been installed yet."

        except FileNotFoundError:
            return "[NOTICE] No packages have been installed yet."
        
    elif mode == "install":
        # do install
        if not arguments or not cmd:
            return "Usage: flu install <package1> <package2> ...\nMore info by typing 'fluentix help install'."
        cmd = cmd.split(',')
        for arg in cmd:
            arg = ' '.join(map(str, arg.split()))
            sys.stdout.write(install_package(arg))
        return
    
    elif mode == "uninstall":
        # do uninstall
        if not arguments or not cmd:
            return "Usage: flu install <package1> <package2> ...\nMore info by typing 'flu help install'."
        cmd = cmd.split(',')
        for arg in cmd:
            sys.stdout.write(uninstall_package(arg))
        return
    
    elif mode == "upload":
        # do upload
        try:
            return upload_package(os.getcwd() + "/" + arguments[0], arguments[1] if len(arguments) > 1 else None)
        except IndexError:
            return Fore.RED + "[UPLOAD-ERROR#1] Directory argument is missing.\nMore information at http://docs.fluentix.dev/upload/no-file\n"
        
    elif mode == "upload-template":
        # do upload-template
        try:
            return upload_template(arguments[0])
        except IndexError:
            return upload_template(None)
        
    elif mode == "manage-packages" or mode == "manage-package":
        return manage_uploads(arguments[0] if arguments else None)
    elif mode == "clean":
        clean_console()
    elif mode == "reinstall":
        if not arguments or not cmd:
            return "Usage: flu install <package1> <package2> ...\nMore info by typing 'flu help install'."
        cmd = cmd.split(',')
        for arg in cmd:
            arg = arg.split()
            sys.stdout.write(reinstall(arg))
        return
    elif mode == "alias":
        try:
            shortcut = arguments[0]
            command = ' '.join(arguments[1:])
            return alias(shortcut, command)  # Ensure alias returns a string
        except IndexError:
            return "[TIP] Usage: flu alias <shortcut> <command>"
    elif mode == "help":
        try:
            command = arguments[0]
            if command == '' or command == '-all':
                sys.stdout.write(help_text + "\n")
                return
            if better_help(command) != None:
                sys.stdout.write("--------------------------------------------------------------\n")
                sys.stdout.write(f"Prompt: {command}\n")
                return better_help(command)
            else:
                return Fore.RED + "[HELP-ERROR] Invalid command, find the list of commands at " + Fore.CYAN + "http://docs.fluentix.dev/commands"
        except IndexError:
            return help_text
    elif mode == "check":
        # checks if installed correctly
        return check()
    
    elif mode == "execute":
        sys.stdout.write("[INFO] Entered Fluentix's live code execution.\n")
        import flu
        return flu.execute_cmd() 
    


def do_sub(command, arg=None, source=False):
    """Do subcommands"""
    if command == "-runtime" and source == False:
        return main()

def main():
    command_history = []
    sys.stdout.write("[INFO] Entered fluentix runtime.\n")
    while True:
        try:
            fluentix = input("flu> ")
            try:
                fluentix.split('.')[1]
                run_file = fluentix
            except IndexError:
                run_file = None
            # Add the command to history
            command_history.append(fluentix)
            readline.add_history(fluentix)  # Add to readline history

            args = fluentix.split()
            if not args:
                sys.stdout.write(help_text + "\n")
                continue

            fluentix_command = args[0]
            del args[0]

            if fluentix_command == "exit":
                break
            
            elif fluentix_command in commands:
                s = do_func(fluentix_command, args, fluentix)
                if s:
                    sys.stdout.write(s + "\n")

            elif "fl" in fluentix_command:
                if fluentix_command.count('.flu') != 0 or fluentix_command.count('.fl') != 0:
                    try:
                        import flu
                        with open(fluentix) as file:
                            flu.execute_code(file.read(), run_file[1].lower())
                    except FileNotFoundError:
                        sys.stdout.write(Fore.RED + f"[EXECUTE-ERROR#1] File not found for '{sys.argv[1]}' in dir {os.getcwd()}\nMore info at http://docs.fluentix.dev/faq/file/error1")
                        exit()
                else:
                    sys.stdout.write(Fore.YELLOW + f"[WARNING] Please type 'exit' to include 'flu' in the start or start typing without 'fluentix' in start.\n")

            elif fluentix_command in shortcuts:
                if shortcuts.index(fluentix_command) % 2 == 0:
                    do_alias(shortcut=shortcuts[shortcuts.index(fluentix_command)], command=shortcuts[shortcuts.index(fluentix_command)+1])
                elif fluentix_command.count('.flu') == 0 or fluentix_command.count('.fl') == 0:
                    sys.stdout.write(Fore.RED + f"[TERMINAL-ERROR#1] Unknown command '{fluentix_command}'.\n" + Fore.CYAN + "More info at http://docs.fluentix.dev/unknown-command\n")
                else:
                    # run file functionality
                    try:
                        import flu
                        with open(fluentix) as file:
                            flu.execute_code(file.read(), run_file[1].lower())
                    except FileNotFoundError:
                        sys.stdout.write(Fore.RED + f"[EXECUTE-ERROR#1] File not found for '{sys.argv[1]}' in dir {os.getcwd()}\nMore info at http://docs.fluentix.dev/file/error1\n")

            elif fluentix_command in subcommands:
                if args:
                    do_sub(fluentix_command, arg=args)
                do_sub(fluentix_command)

            elif fluentix_command.count('.flu') == 0 or fluentix_command.count('.fl') == 0:
                sys.stdout.write(Fore.RED + f"[TERMINAL-ERROR#1] Unknown command '{fluentix_command}'.\n" + Fore.CYAN + "More info at http://docs.fluentix.dev/faq/unknown-command\n")
                
            elif fluentix != None:
                # run file functionality
                try:
                    import flu
                    if fluentix_command[1] == "-runtime":
                        fluentix_command[1] = fluentix_command[2]

                    with open(fluentix_command[1]) as file:
                        flu.execute_code(file.read(), run_file[1].lower())
                except FileNotFoundError:
                    sys.stdout.write(Fore.RED + f"[EXECUTE-ERROR#1] File not found for '{fluentix_command[1]}' in dir {os.getcwd()}\nMore info at http://docs.fluentix.dev/file/error1\n")

        except KeyboardInterrupt:
            sys.stdout.write("\n[NOTICE] Force Quitting terminal...\n")
            sys.exit(1)

def prase():
    try:
        args = sys.argv[1:]

        if not args:
            sys.stdout.write(help_text + "\n")

        fluentix_command = args[0]
        del args[0]

        if fluentix_command in commands:
            s = do_func(fluentix_command, args, ' '.join(map(str, args)))
            if s:
                sys.stdout.write(s + "\n")

        elif fluentix_command in subcommands:
            do_sub(fluentix_command)

        elif fluentix_command in shortcuts:
            if shortcuts.index(fluentix_command) % 2 == 0:
                do_alias(shortcut=shortcuts[shortcuts.index(fluentix_command)], command=shortcuts[shortcuts.index(fluentix_command)+1])
            elif fluentix_command.count('.flu') == 0 or fluentix_command.count('.fl') == 0:
                sys.stdout.write(Fore.RED + f"[TERMINAL-ERROR#1] Unknown command '{fluentix_command}'.\n" + Fore.CYAN + "More info at http://docs.fluentix.dev/unknown-command\n")
            else:
                # run file functionality
                try:
                    import flu
                    with open(sys.argv[1]) as file:
                        flu.execute_code(file.read(), run_file[1].lower())
                except FileNotFoundError:
                    sys.stdout.write(Fore.RED + f"[EXECUTE-ERROR#1] File not found for '{Fore.YELLOW + sys.argv[1] + Fore.RED}' in dir '{Fore.YELLOW + os.getcwd() + Fore.RED}'\n" + Fore.WHITE + "More info at " + Fore.BLUE + "http://docs.fluentix.dev/file/error1\n")
                    exit(1)

        elif fluentix_command.count('.flu') == 0 or fluentix_command.count('fl') == 0:
            sys.stdout.write(Fore.RED + f"[TERMINAL-ERROR#1] Unknown command '{fluentix_command}'.\n" + Fore.WHITE + "More info at " + Fore.BLUE + "http://docs.fluentix.dev/unknown-command\n")
            return

    except KeyboardInterrupt:
        sys.stdout.write("\n[INFO] Force Quitting terminal...\n")
        sys.exit(1)

if __name__ == '__main__':
    try:
        try:
            sys.argv[1].split('.')[1]
            run_file = sys.argv[1].split('.')
            if run_file[1].lower() in ("flu", "fl"):
                # run file functionality
                try:
                    import flu
                    with open(sys.argv[1]) as file:
                        flu.execute_code(file.read(), run_file[1].lower())
                except FileNotFoundError:
                    sys.stdout.write(Fore.RED + f"[EXECUTE-ERROR#1] File not found for '{Fore.YELLOW + sys.argv[1] + Fore.RED}' in dir '{Fore.YELLOW + os.getcwd() + Fore.RED}'\n" + Fore.WHITE + "More info at " + Fore.BLUE + "http://docs.fluentix.dev/file/error1\n")
                    exit(1)
            else:
                sys.stdout.write(Fore.RED + f"[EXECUTE-ERROR#2] Enter a valid extension, got '{Fore.YELLOW + run_file[1] + Fore.RED}'.\n" + Fore.WHITE + "More info at " + Fore.BLUE + "http://docs.fluentix.dev/file/error2\n")
                exit(1)
        except IndexError:
            prase()
    except IndexError:
        exit()
