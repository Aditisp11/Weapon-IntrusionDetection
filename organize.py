import os
import shutil
import random

def organize_dataset():
    # Create dataset structure
    dataset_root = "dataset"
    for split in ['train', 'val']:
        for folder in ['images', 'labels']:
            os.makedirs(os.path.join(dataset_root, split, folder), exist_ok=True)
    
    # Source directories
    source_dirs = ['simple_images/guns', 'simple_images/knife', 'simple_images/shotgun']
    
    # Collect all image and label pairs
    all_files = []
    for source_dir in source_dirs:
        image_files = [f for f in os.listdir(source_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
        for img_file in image_files:
            base_name = os.path.splitext(img_file)[0]
            txt_file = base_name + '.txt'
            if os.path.exists(os.path.join(source_dir, txt_file)):
                all_files.append((source_dir, base_name))
    
    # Split into train/val (80/20 split)
    random.shuffle(all_files)
    split_idx = int(len(all_files) * 0.8)
    train_files = all_files[:split_idx]
    val_files = all_files[split_idx:]
    
    # Copy files to new structure
    def copy_files(files, split):
        for source_dir, base_name in files:
            # Copy image
            for ext in ['.jpg', '.jpeg', '.png']:
                if os.path.exists(os.path.join(source_dir, base_name + ext)):
                    shutil.copy2(
                        os.path.join(source_dir, base_name + ext),
                        os.path.join(dataset_root, split, 'images', base_name + ext)
                    )
                    break
            
            # Copy label
            shutil.copy2(
                os.path.join(source_dir, base_name + '.txt'),
                os.path.join(dataset_root, split, 'labels', base_name + '.txt')
            )
    
    copy_files(train_files, 'train')
    copy_files(val_files, 'val')
    
    # Create data.yaml
    yaml_content = """path: ./dataset
train: train/images
val: val/images

nc: 3  # number of classes
names: ['knife', 'gun', 'shotgun']  # class names"""

    with open(os.path.join(dataset_root, 'data.yaml'), 'w') as f:
        f.write(yaml_content)
    
    print(f"Dataset organized with {len(train_files)} training and {len(val_files)} validation images")

if __name__ == "__main__":
    organize_dataset()