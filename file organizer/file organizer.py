import os
import shutil

folder_path = input("Enter the folder path to organize: ")

if not os.path.exists(folder_path):
    print("The folder does not exist!")
    exit()

file_types = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".pptx"],
    "Videos": [".mp4", ".mkv", ".avi"],
    "Music": [".mp3", ".wav"],
    "Others": []
}

def create_folder(folder_name):
    folder_location = os.path.join(folder_path, folder_name)
    if not os.path.exists(folder_location):
        os.makedirs(folder_location)

for file in os.listdir(folder_path):
    file_location = os.path.join(folder_path, file)

    if os.path.isdir(file_location):
        continue

    file_extension = os.path.splitext(file)[1].lower()

    moved = False

    for category, extensions in file_types.items():
        if file_extension in extensions:
            create_folder(category)
            destination = os.path.join(folder_path, category, file)
            shutil.move(file_location, destination)
            print(f"Moved {file} to {category}")
            moved = True
            break

    if not moved:
        create_folder("Others")
        destination = os.path.join(folder_path, "Others", file)
        shutil.move(file_location, destination)
        print(f"Moved {file} to Others")

print("File organization completed!")