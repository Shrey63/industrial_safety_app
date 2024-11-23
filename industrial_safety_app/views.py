from django.shortcuts import render, redirect
from .utils import *
from .model_runner import *
import time
def home(request):
    # Run Helmet Detection Model
    image_path=r'..\..\1.jpg'
    helmet_detection = run_model(image_path, r'..\..\pt\helmet.pt', "no-helmet")
    if helmet_detection==0:
        request.session["violation_type"] = "helmet"
        request.session["image_path"] = f"industrial_safety_app\\output_result\\no-helmet\\{os.path.basename(os.path.normpath(image_path))}"
        return redirect(f"/notify/")

    # Run Shoes Detection Model
    # shoes_detection = run_model(r'..\..\11.jpg', r'..\..\pt\shoes.pt', "no-shoes")

    # Print the detection results
    # print(f"Helmet Detection Result: {helmet_detection}")
    # print(f"Shoes Detection Result: {shoes_detection}")
    # helmet_detection=run_helmet_model(r'..\..\1.jpg',r'..\..\pt\helmet.pt')
    # time.sleep(40)
    # shoes_detection=run_shoes_model(r'..\..\13.jpeg',r'..\..\pt\shoes.pt')


    # helmet_detection=run_yolov9_model('1.jpg', 'C:\\Users\\shrey\\PycharmProjects\\industrial_safety_app\\industrial_safety_app\\pt\\helmet.pt')

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
    image_filename = request.session.get("image_path")
    absolute_image_path = os.path.join(settings.BASE_DIR, image_filename)

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


