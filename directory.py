import os

def check_and_fix_dataset():
    # Get current working directory
    current_dir = os.getcwd()
    
    # Define the correct paths
    dataset_dir = os.path.join(current_dir, "dataset")
    
    # Create proper directory structure
    for split in ['train', 'val']:
        for folder in ['images', 'labels']:
            dir_path = os.path.join(dataset_dir, split, folder)
            os.makedirs(dir_path, exist_ok=True)
    
    # Create updated data.yaml with absolute path
    yaml_content = f"""path: {dataset_dir}  # dataset root dir
train: train/images  # train images
val: val/images  # val images

nc: 3  # number of classes
names: ['knife', 'gun', 'shotgun']"""

    # Write the yaml file
    yaml_path = os.path.join(dataset_dir, "data.yaml")
    with open(yaml_path, 'w') as f:
        f.write(yaml_content)
    
    # Print directory structure for verification
    print("\nCurrent directory structure:")
    for root, dirs, files in os.walk(dataset_dir):
        level = root.replace(dataset_dir, '').count(os.sep)
        indent = ' ' * 4 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print(f"{subindent}{f}")

if __name__ == "__main__":
    check_and_fix_dataset()
    print("\nDataset structure has been checked and fixed.")
    print("Please verify that your images and labels are in the correct directories.")