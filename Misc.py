"""The below code is used to create a single.jpg image and monitor it"""
import os
import time
from PIL import Image, ImageDraw
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Function to create the initial image
def create_image(file_path):
    width, height = 200, 200
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    draw.text((10, 10), "This is a secure image", fill="black")
    image.save(file_path)
    return image

# Watchdog event handler to monitor file changes
class FileModifiedHandler(FileSystemEventHandler):
    def __init__(self, original_file, observer):
        super().__init__()
        self.original_file = original_file
        self.observer = observer

    def on_modified(self, event):
        if event.src_path == self.original_file:
            print("Image has been modified!")
            # You can perform any action here, like sending an alert or logging.
            # Here, we'll just stop monitoring the file.
            self.observer.stop()

# Main function to create and monitor the image
def main():
    image_file = "secure_image.jpg"
    
    # Create the initial image if it doesn't exist
    if not os.path.exists(image_file):
        create_image(image_file)
        print("Initial image created.")
    
    # Start monitoring for modifications
    observer = Observer()
    event_handler = FileModifiedHandler(image_file, observer)
    observer.schedule(event_handler, path=".", recursive=False)
    observer.start()
    
    try:
        while observer.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

if __name__ == "__main__":
    main()

















"""The below code is to monitor the changes to .jpg image file by calculating its hsh has changed or not"""
import time
import hashlib
import os
from PIL import Image
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Function to calculate the hash of an image
def calculate_hash(image_path):
    with open(image_path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

# Function to check if image is modified
def is_image_modified(image_path, last_hash):
    current_hash = calculate_hash(image_path)
    return current_hash != last_hash

# Event handler for file system events
class ImageChangeHandler(FileSystemEventHandler):
    def __init__(self, image_path, last_hash):
        self.image_path = image_path
        self.last_hash = last_hash

    def on_modified(self, event):
        if event.src_path == self.image_path:
            if is_image_modified(self.image_path, self.last_hash):
                print("Image has been modified!")
                # Notify user here (e.g., send email, display notification, etc.)
            self.last_hash = calculate_hash(self.image_path)

# Main function to monitor image for changes
def monitor_image(image_name):
    image_path = os.path.join(os.getcwd(), image_name)
    if not os.path.isfile(image_path):
        print("Invalid image path.")
        return
    last_hash = calculate_hash(image_path)
    event_handler = ImageChangeHandler(image_path, last_hash)
    observer = Observer()
    observer.schedule(event_handler, os.getcwd(), recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    image_name = input("Enter the name of the image to monitor (including extension): ")
    monitor_image(image_name)
