from ultralytics import YOLO
import datetime
import os

def train_model():
    # Load the model
    model = YOLO('yolov8m.pt')
    
    # Get absolute path to data.yaml
    current_dir = os.getcwd()
    data_yaml_path = os.path.join(current_dir, 'dataset', 'data.yaml')
    
    # Verify data.yaml exists
    if not os.path.exists(data_yaml_path):
        raise FileNotFoundError(f"data.yaml not found at {data_yaml_path}")
    
    # Print training configuration
    print(f"Starting training with:")
    print(f"- Data config: {data_yaml_path}")
    print(f"- Number of images: {len(os.listdir(os.path.join(current_dir, 'dataset', 'train', 'images')))} train, "
          f"{len(os.listdir(os.path.join(current_dir, 'dataset', 'val', 'images')))} val")
    
    # Training
    results = model.train(
        data=data_yaml_path,
        imgsz=640,
        epochs=20,
        batch=4,
        name=f"yolov8m_{datetime.datetime.now().strftime('%Y%m%d_%H-%M-%S')}"
    )
    
    return results

if __name__ == "__main__":
    train_model()