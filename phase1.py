"""
This code accomplishes the following 
1) fork a new child process and print its id
2) stores in the current directory as the base directory
3) keeps a detailed track of everything that happens in the base directory as well as in the sub-directories like creation of new files/directories, deletion of existing files/directories and any modifications that take place to the files/directories
4) create random files of different extensions like .pdf, .jpg, .txt etc etc along with one .jpg image as mandatory - make these files hidden, these files should as act honey pots so keep a track of them like you can create a text files and store the details about these files created so that some other process can keep a track of these 
5) make sure to deploy these honeypot files in all the directories, and if a new directory is created the script should new honeypot in this too 
6) overall keep this process always active and monitoring and make changes and print logs wherever necessary 
7) make this suitable for windows platform
8) put extensive logging i.e., printing on console like if found any new file/directory, deletion, created honeypot file etc.,
9) make sure you create exactly one .jpg and another random file in every directory
"""

import os
import random
import string
import time
import logging
import csv
from multiprocessing import Process
from PIL import Image, ImageDraw

# Setup logging
logging.basicConfig(filename='monitor.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def fork_child_process():
    """Fork a new child process and print its ID."""
    child_process = Process(target=monitor_directories)
    child_process.start()
    print(f"Child process ID: {child_process.pid}")
    logging.info(f"Child process ID: {child_process.pid}")

def monitor_directory_changes(root_dir):
    """Monitor changes in the specified directory."""
    # Keep track of initial file and directory structure
    initial_structure = get_directory_structure(root_dir)
    
    # Monitor for changes
    while True:
        current_structure = get_directory_structure(root_dir)
        
        # Check for newly created files/directories
        new_items = compare_directory_structure(initial_structure, current_structure)
        if new_items:
            logging.info(f"New items detected: {new_items}")
            print(f"New items detected: {new_items}")
            for item in new_items:
                if os.path.isdir(os.path.join(root_dir, item)):
                    create_honeypot(os.path.join(root_dir, item))

        # Check for deleted files/directories
        deleted_items = compare_directory_structure(current_structure, initial_structure)
        if deleted_items:
            logging.info(f"Deleted items detected: {deleted_items}")
            print(f"Deleted items detected: {deleted_items}")
            remove_deleted_folders_from_csv(deleted_items)
        
        # Update initial structure
        initial_structure = current_structure
        
        # Sleep for some time before checking again
        time.sleep(5)

def get_directory_structure(root_dir):
    """Get the directory structure as a dictionary."""
    dir_structure = {}
    for dirpath, dirnames, filenames in os.walk(root_dir):
        relative_path = os.path.relpath(dirpath, root_dir)
        dir_structure[relative_path] = {
            'directories': dirnames,
            'files': filenames
        }
    return dir_structure

def compare_directory_structure(old_structure, new_structure):
    """Compare two directory structures and return the differences."""
    differences = []
    for path, data in new_structure.items():
        if path not in old_structure:
            differences.append(path)
        else:
            old_files = set(old_structure[path]['files'])
            new_files = set(data['files'])
            new_items = new_files - old_files
            if new_items:
                differences.extend([os.path.join(path, item) for item in new_items])
    return differences

def create_honeypot(directory):
    """Create hidden honey pot files in the specified directory."""
    # Create .jpg images only
    filename = generate_random_filename()
    filenameWithExt = filename + '.jpg'
    filepath = os.path.join(directory, filenameWithExt)
    create_image(filepath)
    add_file_info_to_csv(filename, '.jpg', directory)

def generate_random_filename():
    """Generate a random filename with the specified extension."""
    adjectives = ['funny', 'silly', 'wacky', 'goofy', 'crazy', 'quirky', 'whimsical']
    nouns = ['banana', 'kangaroo', 'unicorn', 'penguin', 'squirrel', 'pickle', 'robot']
    adjective = random.choice(adjectives)
    noun = random.choice(nouns)
    return f"{adjective}_{noun}_hpot"

def monitor_directories():
    """Monitor the base directory and its sub-directories."""
    base_dir = os.getcwd()
    logging.info(f"Monitoring directory: {base_dir}")
    print(f"Monitoring directory: {base_dir}")
    monitor_directory_changes(base_dir)

def add_file_info_to_csv(file_name, extension, directory):
    csv_file = "file_info.csv"
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([file_name, extension, directory])

def remove_deleted_folders_from_csv(deleted_folders):
    csv_file = "file_info.csv"
    updated_rows = []
    base_dir = os.getcwd()
    for i in range(len(deleted_folders)):
        deleted_folders[i] = os.path.join(base_dir, deleted_folders[i])

    with open(csv_file, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[2] not in deleted_folders:
                updated_rows.append(row)

    # Write updated rows back to the CSV file
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(updated_rows)

def create_image(file_path):
    """Create an image with text."""
    width, height = 200, 200
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    draw.text((10, 10), "This is a secure image", fill="black")
    image.save(file_path)

if __name__ == "__main__":
    # Fork a child process
    fork_child_process()



# import os
# import random
# import string
# import time
# import ctypes
# import logging
# import csv
# from multiprocessing import Process
# from PIL import Image, ImageDraw

# # Setup logging
# logging.basicConfig(filename='monitor.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# def fork_child_process():
#     """Fork a new child process and print its ID."""
#     child_process = Process(target=monitor_directories)
#     child_process.start()
#     print(f"Child process ID: {child_process.pid}")
#     logging.info(f"Child process ID: {child_process.pid}")

# def monitor_directory_changes(root_dir):
#     """Monitor changes in the specified directory."""
#     # Keep track of initial file and directory structure
#     initial_structure = get_directory_structure(root_dir)
    
#     # Monitor for changes
#     while True:
#         current_structure = get_directory_structure(root_dir)
        
#         # Check for newly created files/directories
#         new_items = compare_directory_structure(initial_structure, current_structure)
#         if new_items:
#             logging.info(f"New items detected: {new_items}")
#             print(f"New items detected: {new_items}")
#             for item in new_items:
#                 if os.path.isdir(os.path.join(root_dir, item)):
#                     create_honeypot(os.path.join(root_dir, item))

#         # Check for deleted files/directories
#         deleted_items = compare_directory_structure(current_structure, initial_structure)
#         if deleted_items:
#             logging.info(f"Deleted items detected: {deleted_items}")
#             print(f"Deleted items detected: {deleted_items}")
#             remove_deleted_folders_from_csv(deleted_items)
        
#         # Update initial structure
#         initial_structure = current_structure
        
#         # Sleep for some time before checking again
#         time.sleep(5)

# def get_directory_structure(root_dir):
#     """Get the directory structure as a dictionary."""
#     dir_structure = {}
#     for dirpath, dirnames, filenames in os.walk(root_dir):
#         relative_path = os.path.relpath(dirpath, root_dir)
#         dir_structure[relative_path] = {
#             'directories': dirnames,
#             'files': filenames
#         }
#     return dir_structure

# def compare_directory_structure(old_structure, new_structure):
#     """Compare two directory structures and return the differences."""
#     differences = []
#     for path, data in new_structure.items():
#         if path not in old_structure:
#             differences.append(path)
#         else:
#             old_files = set(old_structure[path]['files'])
#             new_files = set(data['files'])
#             new_items = new_files - old_files
#             if new_items:
#                 differences.extend([os.path.join(path, item) for item in new_items])
#     return differences

# def create_honeypot(directory):
#     """Create hidden honey pot files in the specified directory."""
#     # Create .jpg images only
#     filename = generate_random_filename()
#     filenameWithExt = filename + '.jpg'
#     filepath = os.path.join(directory, filenameWithExt)
#     create_image(filepath)
#     add_file_info_to_csv(filename, '.jpg', directory)
#     # Hide file (works on Windows)
#     # if os.name == 'nt':
#     #     ctypes.windll.kernel32.SetFileAttributesW(filepath, 2)  # 2 means hidden attribute

# def generate_random_filename():
#     """Generate a random filename with the specified extension."""
#     adjectives = ['funny', 'silly', 'wacky', 'goofy', 'crazy', 'quirky', 'whimsical']
#     nouns = ['banana', 'kangaroo', 'unicorn', 'penguin', 'squirrel', 'pickle', 'robot']
#     adjective = random.choice(adjectives)
#     noun = random.choice(nouns)
#     return f"{adjective}_{noun}_hpot"

# def monitor_directories():
#     """Monitor the base directory and its sub-directories."""
#     base_dir = os.getcwd()
#     logging.info(f"Monitoring directory: {base_dir}")
#     print(f"Monitoring directory: {base_dir}")
#     monitor_directory_changes(base_dir)

# def add_file_info_to_csv(file_name, extension, directory):
#     csv_file = "file_info.csv"
#     with open(csv_file, mode='a', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow([file_name, extension, directory])

# def remove_deleted_folders_from_csv(deleted_folders):
#     csv_file = "file_info.csv"
#     updated_rows = []
#     base_dir = os.getcwd()
#     print("----------------------")
#     # Adding base_dir to every directory present in deleted_folders
#     for i in range(len(deleted_folders)):
#         deleted_folders[i] = base_dir + '\\' + deleted_folders[i]
#         print(deleted_folders[i])

#     with open(csv_file, mode='r', newline='') as file:
#         reader = csv.reader(file)
#         for row in reader:
#             if row[2] not in deleted_folders:
#                 updated_rows.append(row)

#     # Write updated rows back to the CSV file
#     with open(csv_file, mode='w', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerows(updated_rows)

# def create_image(file_path):
#     """Create an image with text."""
#     width, height = 200, 200
#     image = Image.new("RGB", (width, height), "white")
#     draw = ImageDraw.Draw(image)
#     draw.text((10, 10), "This is a secure image", fill="black")
#     image.save(file_path)

# if __name__ == "__main__":
#     # Fork a child process
#     fork_child_process()



# import os
# import random
# import string
# import time
# import logging
# import csv
# from multiprocessing import Process
# from PIL import Image, ImageDraw

# # Setup logging
# logging.basicConfig(filename='monitor.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# def fork_child_process():
#     """Fork a new child process and print its ID."""
#     child_process = Process(target=monitor_directories)
#     child_process.start()
#     print(f"Child process ID: {child_process.pid}")
#     logging.info(f"Child process ID: {child_process.pid}")

# def monitor_directory_changes(root_dir):
#     """Monitor changes in the specified directory."""
#     # Keep track of initial file and directory structure
#     initial_structure = get_directory_structure(root_dir)
    
#     # Monitor for changes
#     while True:
#         current_structure = get_directory_structure(root_dir)
        
#         # Check for newly created files/directories
#         new_items = compare_directory_structure(initial_structure, current_structure)
#         if new_items:
#             logging.info(f"New items detected: {new_items}")
#             print(f"New items detected: {new_items}")
#             for item in new_items:
#                 if os.path.isdir(os.path.join(root_dir, item)):
#                     create_honeypot(os.path.join(root_dir, item))

#         # Check for deleted files/directories
#         deleted_items = compare_directory_structure(current_structure, initial_structure)
#         if deleted_items:
#             logging.info(f"Deleted items detected: {deleted_items}")
#             print(f"Deleted items detected: {deleted_items}")
#             remove_deleted_folders_from_csv(deleted_items)
        
#         # Update initial structure
#         initial_structure = current_structure
        
#         # Sleep for some time before checking again
#         time.sleep(5)

# def get_directory_structure(root_dir):
#     """Get the directory structure as a dictionary."""
#     dir_structure = {}
#     for dirpath, dirnames, filenames in os.walk(root_dir):
#         relative_path = os.path.relpath(dirpath, root_dir)
#         dir_structure[relative_path] = {
#             'directories': dirnames,
#             'files': filenames
#         }
#     return dir_structure

# def compare_directory_structure(old_structure, new_structure):
#     """Compare two directory structures and return the differences."""
#     differences = []
#     for path, data in new_structure.items():
#         if path not in old_structure:
#             differences.append(path)
#         else:
#             old_files = set(old_structure[path]['files'])
#             new_files = set(data['files'])
#             new_items = new_files - old_files
#             if new_items:
#                 differences.extend([os.path.join(path, item) for item in new_items])
#     return differences

# def create_honeypot(directory):
#     """Create hidden honey pot files in the specified directory."""
#     # Create .jpg images only
#     filename = generate_random_filename()
#     filenameWithExt = filename + '.jpg'
#     filepath = os.path.join(directory, filenameWithExt)
#     create_image(filepath)
#     add_file_info_to_csv(filename, '.jpg', directory)

# def generate_random_filename():
#     """Generate a random filename with the specified extension."""
#     adjectives = ['funny', 'silly', 'wacky', 'goofy', 'crazy', 'quirky', 'whimsical']
#     nouns = ['banana', 'kangaroo', 'unicorn', 'penguin', 'squirrel', 'pickle', 'robot']
#     adjective = random.choice(adjectives)
#     noun = random.choice(nouns)
#     return f"{adjective}_{noun}_hpot"

# def monitor_directories():
#     """Monitor the base directory and its sub-directories."""
#     base_dir = os.getcwd()
#     logging.info(f"Monitoring directory: {base_dir}")
#     print(f"Monitoring directory: {base_dir}")
#     monitor_directory_changes(base_dir)

# def add_file_info_to_csv(file_name, extension, directory):
#     csv_file = "file_info.csv"
#     with open(csv_file, mode='a', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow([file_name, extension, directory])

# def remove_deleted_folders_from_csv(deleted_folders):
#     csv_file = "file_info.csv"
#     updated_rows = []
#     base_dir = os.getcwd()

#     with open(csv_file, mode='r', newline='') as file:
#         reader = csv.reader(file)
#         for row in reader:
#             if row[2] not in deleted_folders:
#                 updated_rows.append(row)

#     # Write updated rows back to the CSV file
#     with open(csv_file, mode='w', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerows(updated_rows)

# def create_image(file_path):
#     """Create an image with text."""
#     width, height = 200, 200
#     image = Image.new("RGB", (width, height), "white")
#     draw = ImageDraw.Draw(image)
#     draw.text((10, 10), "This is a secure image", fill="black")
#     image.save(file_path)

# if __name__ == "__main__":
#     # Fork a child process
#     fork_child_process()
# ``



#old versions

# import os
# import random
# import string
# import time
# import ctypes
# import logging
# import csv
# from multiprocessing import Process

# # Setup logging
# logging.basicConfig(filename='monitor.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# def fork_child_process():
#     """Fork a new child process and print its ID."""
#     child_process = Process(target=monitor_directories)
#     child_process.start()
#     print(f"Child process ID: {child_process.pid}")
#     logging.info(f"Child process ID: {child_process.pid}")

# def monitor_directory_changes(root_dir):
#     """Monitor changes in the specified directory."""
#     # Keep track of initial file and directory structure
#     initial_structure = get_directory_structure(root_dir)
    
#     # Monitor for changes
#     while True:
#         current_structure = get_directory_structure(root_dir)
        
#         # Check for newly created files/directories
#         new_items = compare_directory_structure(initial_structure, current_structure)
#         if new_items:
#             logging.info(f"New items detected: {new_items}")
#             print(f"New items detected: {new_items}")
#             for item in new_items:
#                 if os.path.isdir(os.path.join(root_dir, item)):
#                     create_honeypot(os.path.join(root_dir, item))

#         # Check for deleted files/directories
#         deleted_items = compare_directory_structure(current_structure, initial_structure)
#         if deleted_items:
#             logging.info(f"Deleted items detected: {deleted_items}")
#             print(f"Deleted items detected: {deleted_items}")
#             remove_deleted_folders_from_csv(deleted_items)
        
#         # Update initial structure
#         initial_structure = current_structure
        
#         # Sleep for some time before checking again
#         time.sleep(5)

# def get_directory_structure(root_dir):
#     """Get the directory structure as a dictionary."""
#     dir_structure = {}
#     for dirpath, dirnames, filenames in os.walk(root_dir):
#         relative_path = os.path.relpath(dirpath, root_dir)
#         dir_structure[relative_path] = {
#             'directories': dirnames,
#             'files': filenames
#         }
#     return dir_structure

# def compare_directory_structure(old_structure, new_structure):
#     """Compare two directory structures and return the differences."""
#     differences = []
#     for path, data in new_structure.items():
#         if path not in old_structure:
#             differences.append(path)
#         else:
#             old_files = set(old_structure[path]['files'])
#             new_files = set(data['files'])
#             new_items = new_files - old_files
#             if new_items:
#                 differences.extend([os.path.join(path, item) for item in new_items])
#     return differences

# def create_honeypot(directory):
#     """Create hidden honey pot files in the specified directory."""
#     extensions = ['.jpg']  # Add more extensions if needed
#     for ext in extensions:
#         filename = generate_random_filename()
#         filenameWithExt = filename+ext
#         filepath = os.path.join(directory, filenameWithExt)
#         with open(filepath, 'wb') as f:
#             # Generate random binary data
#             binary_data = bytes([random.randint(0, 255) for _ in range(1024)])
#             f.write(binary_data)
#             add_file_info_to_csv(filename, ext, directory)
#         # Hide file (works on Windows)
#         if os.name == 'nt':
#             ctypes.windll.kernel32.SetFileAttributesW(filepath, 2)  # 2 means hidden attribute

# def generate_random_filename():
#     """Generate a random filename with the specified extension."""
#     adjectives = ['funny', 'silly', 'wacky', 'goofy', 'crazy', 'quirky', 'whimsical']
#     nouns = ['banana', 'kangaroo', 'unicorn', 'penguin', 'squirrel', 'pickle', 'robot']
#     adjective = random.choice(adjectives)
#     noun = random.choice(nouns)
#     return f"{adjective}_{noun}_hpot"

# def monitor_directories():
#     """Monitor the base directory and its sub-directories."""
#     base_dir = os.getcwd()
#     logging.info(f"Monitoring directory: {base_dir}")
#     print(f"Monitoring directory: {base_dir}")
#     monitor_directory_changes(base_dir)

# def add_file_info_to_csv(file_name, extension, directory):
#     csv_file = "file_info.csv"
#     with open(csv_file, mode='a', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow([file_name, extension, directory])

# def remove_deleted_folders_from_csv(deleted_folders):
#     csv_file = "file_info.csv"
#     updated_rows = []
#     base_dir = os.getcwd()
#     print("----------------------")
#     #adding base_dir to every directory present in deleted_folders
#     for i in range(len(deleted_folders)):
#         deleted_folders[i] = base_dir + '\\' + deleted_folders[i]
#         print(deleted_folders[i])

#     with open(csv_file, mode='r', newline='') as file:
#         reader = csv.reader(file)
#         for row in reader:
#             if row[2] not in deleted_folders:
#                 updated_rows.append(row)

#     # Write updated rows back to the CSV file
#     with open(csv_file, mode='w', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerows(updated_rows)

# if __name__ == "__main__":
#     # Fork a child process
#     fork_child_process()

