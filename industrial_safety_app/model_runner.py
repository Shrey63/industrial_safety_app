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
        print(f"STDOUT:\n{process.stdout}")
        print(f"STDERR:\n{process.stderr}")

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

