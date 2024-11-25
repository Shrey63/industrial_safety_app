from django.shortcuts import render, redirect
from .utils import *
from .model_runner import *
import time
import glob

def home(request):
    # Run Helmet Detection Model
    folder_name = "input_data"
    # files = glob.glob(os.path.join(folder_path, "*.*"))  # Match all files
    # image_path=max(files, key=os.path.getmtime) if files else None
    # try:
    image_path = get_latest_image(folder_name)
    print(f"Latest image path: {image_path}")
    # except FileNotFoundError as e:
    #     print(e)
    detection_keyword="no-helmet"
    helmet_detection = run_model(image_path, r'..\..\pt\helmet.pt', detection_keyword)
    if helmet_detection==0:
        request.session["violation_type"] = "helmet"
        request.session["detection_keyword"] = detection_keyword
        return redirect(f"/notify/")
    print(helmet_detection)
    # Run Shoes Detection Model
    # shoes_detection = run_model(r'..\..\11.jpg', r'..\..\pt\shoes.pt', "no-shoes")

    # Print the detection results
    # print(f"Helmet Detection Result: {helmet_detection}")
    # print(f"Shoes Detection Result: {shoes_detection}")
    # helmet_detection=run_helmet_model(r'..\..\12.jpg',r'..\..\pt\helmet.pt')
    # time.sleep(40)
    # shoes_detection=run_shoes_model(r'..\..\13.jpeg',r'..\..\pt\shoes.pt')


    # helmet_detection=run_yolov9_model('12.jpg', 'C:\\Users\\shrey\\PycharmProjects\\industrial_safety_app\\industrial_safety_app\\pt\\helmet.pt')

    # if helmet_detection==0:
    #     violation_type = "helmet"
    #     print(f"violation_type ={violation_type}")
    #     # Redirect to the notify view with the violation_type as a query parameter
        # return redirect(f"/notify/?violation_type={violation_type}")
    # time.sleep(40)
    # if shoes_detection == 0:
    #     violation_type = "shoes"
        # Redirect to the notify view with the violation_type as a query parameter
        # return redirect(f"/notify/?violation_type={violation_type}")

    return render(request, "index.html")

def success(request):
    return render(request, "success.html")

def failure(request):
    return render(request, "failure.html")


def notify(request):
    """
    Handles the notifier view. Sends WhatsApp, email notifications,
    and displays the notification message on the website.
    """
    violation_type = request.session.get("violation_type", "mask")
    detection_keyword = request.session.get("detection_keyword")
    folder_name = f'output_result/{detection_keyword}/'
    absolute_image_path = get_latest_image(folder_name)

    # Fetch the customized messages for the detected violation
    messages = VIOLATION_MESSAGES.get(violation_type, VIOLATION_MESSAGES["mask"])  # Fallback to "mask"

    email_subject = messages["email_subject"]
    email_message = messages["email_message"]
    whatsapp_caption = messages["whatsapp_caption"]

    # Dummy data for now, to be replaced with dynamic data later
    email_recipient = "shreya.agrawal@cumminscollege.in"
    whatsapp_group_id = "FJjIC6Bobxu5tXLub7wqiN"
    # Generate encryption key
    key = generate_key()

    # Encrypt WhatsApp group ID
    encrypted_recipient = encrypt_recipient(whatsapp_group_id, key)

    # Send Email Notification
    send_email(email_subject, email_message, email_recipient,absolute_image_path)

    # Send WhatsApp Notification
    send_whatsapp_message(encrypted_recipient, whatsapp_caption,absolute_image_path , key)

    # Prepare data for website notification
    context = {
        'message': email_message,
        'image_name': absolute_image_path ,  # Pass only the image file name
    }
    print(absolute_image_path)

    # Render the notifier page with the notification
    return render(request, "notifier.html", context)


def get_latest_image(folder_name):
    # Get all files in the folder
    folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),folder_name)
    files = glob.glob(os.path.join(folder_path, "*.*"))
    # Ensure files exist before finding the latest one
    if not files:
        raise FileNotFoundError(f"No files found in the folder: {os.path.abspath(folder_path)}")
    # Return the latest file path
    return max(files, key=os.path.getmtime)

