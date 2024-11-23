from django.shortcuts import render, redirect
from .utils import *
from .model_runner import run_yolov9_model,helmet_detection
def home(request):
    helmet_detection=run_yolov9_model(r'..\..\input_data\1.jpg',r'..\..\pt\helmet.pt')
    # helmet_detection=run_yolov9_model('1.jpg', 'C:\\Users\\shrey\\PycharmProjects\\industrial_safety_app\\industrial_safety_app\\pt\\helmet.pt')
    print(f"Result saved at: {helmet_detection}")
    if helmet_detection==0:
        violation_type = "helmet"
        # Redirect to the notify view with the violation_type as a query parameter
        return redirect(f"/notify/?violation_type={violation_type}")
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
    violation_type = request.GET.get("violation_type", "mask")  # Default to "mask" if not provided

    # Fetch the customized messages for the detected violation
    messages = VIOLATION_MESSAGES.get(violation_type, VIOLATION_MESSAGES["mask"])  # Fallback to "mask"

    email_subject = messages["email_subject"]
    email_message = messages["email_message"]
    whatsapp_caption = messages["whatsapp_caption"]

    # Dummy data for now, to be replaced with dynamic data later
    email_recipient = "shreya.agrawal@cumminscollege.in"
    whatsapp_group_id = "FJjIC6Bobxu5tXLub7wqiN"
    image_filename = "no-mask.jpg"

    # Generate encryption key
    key = generate_key()

    # Encrypt WhatsApp group ID
    encrypted_recipient = encrypt_recipient(whatsapp_group_id, key)

    # Send Email Notification
    send_email(email_subject, email_message, email_recipient)

    # Send WhatsApp Notification
    send_whatsapp_message(encrypted_recipient, whatsapp_caption, image_filename, key)

    # Prepare data for website notification
    context = {
        'message': email_message,
        'image_name': image_filename,  # Pass only the image file name
    }

    # Render the notifier page with the notification
    return render(request, "notifier.html", context)


