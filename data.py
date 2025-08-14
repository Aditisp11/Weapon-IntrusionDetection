# First, let's create a proper dataset structure
import os
import shutil
from sklearn.model_selection import train_test_split

def organize_dataset():
    # Create dataset directory structure
    dataset_dir = "dataset"
    os.makedirs(dataset_dir, exist_ok=True)
    os.makedirs(os.path.join(dataset_dir, "train", "images"), exist_ok=True)
    os.makedirs(os.path.join(dataset_dir, "train", "labels"), exist_ok=True)
    os.makedirs(os.path.join(dataset_dir, "val", "images"), exist_ok=True)
    os.makedirs(os.path.join(dataset_dir, "val", "labels"), exist_ok=True)
    
    # Define classes
    classes = ["guns", "knife", "shotgun"]
    
    # Create data.yaml
    yaml_content = f"""
path: {os.path.abspath(dataset_dir)}  # dataset root dir
train: train/images  # train images (relative to 'path')
val: val/images  # val images (relative to 'path')

# Classes
names:
  0: guns
  1: knife
  2: shotgun
    """
    
    with open(os.path.join(dataset_dir, "data.yaml"), "w") as f:
        f.write(yaml_content)
    
    return dataset_dir, classes

# Create the dataset structure and yaml file
dataset_dir, classes = organize_dataset()

print("Dataset structure created!")
print("Now you need to:")
print("1. Create annotation labels for your images using a tool like LabelImg")
print("2. Put your images in dataset/train/images and dataset/val/images")
print("3. Put corresponding label files in dataset/train/labels and dataset/val/labels")