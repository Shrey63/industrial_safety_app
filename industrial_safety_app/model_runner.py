import os
import subprocess
def run_model(source_image_path, weights_path, detection_keyword):
    """
    Runs the YOLOv9 model and checks for specific detection in the output.

    Args:
        source_image_path (str): Path to the input image.
        weights_path (str): Path to the YOLOv9 weights file.
        detection_keyword (str): Keyword to look for in the model output.

    Returns:
        int: Detection result (0 if keyword is found, -1 otherwise).
    """
    # Global variable to store detection status
    detection_status = 1

    # YOLOv9 script and arguments
    python_path = os.path.join(os.getcwd(), '.venv', 'Scripts', 'python')  # Adjust as needed
    command = f"{python_path} detect_dual.py --source '{source_image_path}' --img 640 --device cpu --weights '{weights_path}' --name {detection_keyword}"

    try:
        # Save the original directory
        original_dir = os.getcwd()

        # Change to the YOLOv9 directory
        yolov9_dir = os.path.join("industrial_safety_app", "ml_models", "yolov9")
        os.chdir(yolov9_dir)

        # Run the YOLOv9 model using subprocess
        process = subprocess.run(command, shell=True, capture_output=True, text=True)

        # Print the process output (for debugging)
        print(process)
        print('------------------------------')
        print(f"STDOUT:\n{process.stdout}")
        print('------------------------------')
        print(f"STDERR:\n{process.stderr}")
        print('------------------------------')

        # Check the output logs for detection results
        output = process.stdout
        if detection_keyword in output:
            detection_status = 0

        print(f"{detection_keyword} detection status: {detection_status}")

        return (detection_status)

    except Exception as e:
        print(f"Error running YOLOv9 model: {e}")
        return -1

    finally:
        # Change back to the original directory
        os.chdir(original_dir)


# Global set to store all unique detections
detected_classes = set()
def run_model_on_folder(folder_path, weights_path):
    """
    Processes all images in a folder using the YOLOv9 model and accumulates unique detections.

    Args:
        folder_path (str): Path to the folder containing images.
        weights_path (str): Path to the YOLOv9 weights file.

    Returns:
        set: A set of all unique detections found across all images.
    """
    global detected_classes

    # Ensure the folder exists
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    # Get a sorted list of all image files in the folder (oldest-first)
    image_files = sorted(
        [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))],
        key=os.path.getctime
    )

    if not image_files:
        raise FileNotFoundError(f"No image files found in folder: {folder_path}")

    # Process each image sequentially
    for image_path in image_files:
        print(f"Processing image: {image_path}")
        run_checkpoint_model(image_path, weights_path)

    return detected_classes


def run_checkpoint_model(source_image_path, weights_path):
    """
    Runs the YOLOv9 model and extracts detected classes.

    Args:
        source_image_path (str): Path to the input image.
        weights_path (str): Path to the YOLOv9 weights file.
    """
    global detected_classes

    # YOLOv9 script and arguments
    python_path = os.path.join(os.getcwd(), '.venv', 'Scripts', 'python')  # Adjust as needed
    command = f"{python_path} detect_dual.py --source '{source_image_path}' --img 640 --device cpu --weights '{weights_path}' --name outputResult"

    try:
        # Save the original directory
        original_dir = os.getcwd()

        # Change to the YOLOv9 directory
        yolov9_dir = os.path.join("industrial_safety_app", "ml_models", "yolov9")
        os.chdir(yolov9_dir)

        # Run the YOLOv9 model using subprocess
        process = subprocess.run(command, shell=True, capture_output=True, text=True)

        # Parse the process output for detected classes
        output = process.stdout
        print(f"Model Output:\n{output}")

        # Extract detected classes
        extract_detected_classes(output)

    except Exception as e:
        print(f"Error running YOLOv9 model: {e}")

    finally:
        # Change back to the original directory
        os.chdir(original_dir)


def extract_detected_classes(output):
    """
    Extracts detected classes from the model's output and updates the global set.

    Args:
        output (str): The output string from the YOLOv9 model.
    """
    global detected_classes

    # Parse the output for detected class lines
    lines = output.splitlines()
    for line in lines:
        if line.startswith("Detected:"):
            # Extract the class name from the line
            class_name = line.split("Detected:")[1].strip()
            detected_classes.add(class_name)
