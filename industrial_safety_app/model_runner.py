import os
import subprocess
# Global variable for helmet detection
helmet_detection = -1  # Default: -1 (not processed yet)


def run_yolov9_model(source_image_path, weights_path):
    """
    Runs the YOLOv9 model and updates the helmet detection status.

    Args:
        source_image_path (str): Path to the input image for the YOLOv9 model.
        weights_path (str): Path to the YOLOv9 weights file.
        save_dir (str): Directory to save the results.
        result_name (str): Custom name for the saved results folder.

    Returns:
        str: Path to the saved result.
    """

    global helmet_detection

    # YOLOv9 script and arguments
    python_path = os.path.join(os.getcwd(), '.venv', 'Scripts', 'python')
    print(weights_path)
    command = f"{python_path} detect_dual.py --source '{source_image_path}' --img 640 --device cpu --weights '{weights_path}' --name yolov9_results"
    try:
        # Change to the YOLOv9 directory
        os.chdir("industrial_safety_app/ml_models/yolov9")  # Adjust path if YOLOv9 is in another directory
        # Run the YOLOv9 model using subprocess
        process = subprocess.run(command, shell=True,capture_output=True, text=True)

        print(process)
        print(f"STDOUT:\n{process.stdout}")
        print(f"STDERR:\n{process.stderr}")
        # Check the output logs for detection results
        output = process.stdout
        print(output)
        if "no-helmet" in output:
            helmet_detection = 0
        elif "helmet" in output:
            helmet_detection = 1
        else:
            helmet_detection = -1  # No relevant detection

        print(helmet_detection)
        # Print the process output (for debugging)

        # Path to the saved result

        return helmet_detection

    except Exception as e:
        print(f"Error running YOLOv9 model: {e}")
        helmet_detection = -1
        return None

    finally:
        # Change back to the original directory
        os.chdir("..")
