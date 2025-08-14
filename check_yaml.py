import os
import yaml

def check_yaml():
    current_dir = os.getcwd()
    yaml_path = os.path.join(current_dir, 'dataset', 'data.yaml')
    
    # Read and print current yaml content
    with open(yaml_path, 'r') as f:
        current_content = f.read()
        print("Current YAML content:")
        print(current_content)
        print("\n")
    
    # Create updated content
    updated_content = f"""path: {current_dir}/dataset  # dataset root dir
train: train/images  # train images
val: val/images  # val images

nc: 3  # number of classes
names: ['guns', 'knife', 'shotgun']"""
    
    # Write updated content
    with open(yaml_path, 'w') as f:
        f.write(updated_content)
    
    print("Updated YAML content:")
    print(updated_content)
    print("\nYAML file has been updated with correct paths.")

if __name__ == "__main__":
    check_yaml()