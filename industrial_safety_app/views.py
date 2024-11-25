from django.shortcuts import render, redirect
from .utils import *
from .model_runner import *

def home(request):
    # Run Helmet Detection Model
    folder_name = "input_data"
    try:
        image_path = get_latest_image(folder_name)
        print(f"Latest image path: {image_path}")
    except FileNotFoundError as e:
         print(e)
    detection_keyword="no-helmet"
    helmet_detection = run_model(image_path, r'..\..\pt\helmet.pt', detection_keyword)
    if helmet_detection==0:
        request.session["violation_type"] = "helmet"
        request.session["detection_keyword"] = detection_keyword
        return redirect(f"/notify/")
    print(helmet_detection)

    # Run Shoes Detection Model
    detection_keyword="no-shoes"
    shoes_detection = run_model(image_path, r'..\..\pt\shoes.pt', detection_keyword)
    if shoes_detection == 0:
        request.session["violation_type"] = "shoes"
        request.session["detection_keyword"] = detection_keyword
        return redirect(f"/notify/")
    print(shoes_detection)

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

    folder_name = os.path.join(settings.MEDIA_ROOT, 'output_result', detection_keyword)
    latest_image_path = get_latest_image(folder_name)

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
    send_email(email_subject, email_message, email_recipient,latest_image_path)

    # Send WhatsApp Notification
    send_whatsapp_message(encrypted_recipient, whatsapp_caption,latest_image_path , key)

    # image_url = absolute_image_path.replace(settings.MEDIA_ROOT, settings.MEDIA_URL)
    image_url = latest_image_path.replace(settings.MEDIA_ROOT, settings.MEDIA_URL).replace("\\", "/")
    # Prepare data for website notification
    context = {
        'subject': email_subject,
        'message': email_message,
         'image_url': image_url,  # Use URL for the image
    }
    print(latest_image_path)
    # Render the notifier page with the notification
    return render(request, "notifier.html", context)




