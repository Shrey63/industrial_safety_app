from django.http import request
from django.shortcuts import render, redirect
from .utils import *
from .model_runner import *
from django.http import request
from django.shortcuts import render, redirect
from .utils import *
from .model_runner import *
from django.http import HttpResponse
import json


# Function to run model and check for violation
def run_detection_model(image_path, model_path, detection_keyword, session_key):
    detection_result = run_model(image_path, model_path, detection_keyword)
    if detection_result == 0:  # Violation detected
        request.session["violation_type"] = session_key
        request.session["detection_keyword"] = detection_keyword
        return True
    return False

def home(request):
    # Run Helmet Detection Model
    folder_name = "input_data"
    try:
        image_path = get_latest_image(folder_name)
        print(f"Latest image path: {image_path}")
    except FileNotFoundError as e:
         print(e)
         return render(request, "error.html")  # Handle file not found

    detection_keyword="no-helmet"
    helmet_detection = run_model(image_path, r'..\..\pt\helmet.pt', detection_keyword)
    if helmet_detection==0:
        request.session["violation_type"] = "no-helmet"
        request.session["detection_keyword"] = detection_keyword
    print(helmet_detection)
    notify(request)
    # Run Shoes Detection Model
    # detection_keyword="no-shoes"
    # shoes_detection = run_model(image_path, r'..\..\pt\shoes.pt', detection_keyword)
    # if shoes_detection == 0:
    #     request.session["violation_type"] = "shoes"
    #     request.session["detection_keyword"] = detection_keyword
    #     return redirect(f"/notify/")
    # print(shoes_detection)

    return render(request, "index.html")


def notify(request):
    """
    Handles the notifier view. Sends WhatsApp, email notifications,
    and displays the notification message on the website.
    """
    violation_type = request.session.get("violation_type", "no-mask")
    detection_keyword = request.session.get("detection_keyword")

    folder_name = os.path.join(settings.MEDIA_ROOT, 'output_result', detection_keyword)
    latest_image_path = get_latest_image(folder_name)

    # Fetch the customized messages for the detected violation
    messages = VIOLATION_MESSAGES.get(violation_type, VIOLATION_MESSAGES["no-mask"])  # Fallback to "mask"

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
    # context = {
    #     'subject': email_subject,
    #     'message': email_message,
    #      'image_url': image_url,  # Use URL for the image
    # }
    print(latest_image_path)
    # Render the notifier page with the notification
    # return render(request, "notifier.html", context)
    return


#CHECKPOINT VIEWS
def process(request):
    # Run Helmet Detection Model
    print("---------------------done-------------------")
    if request.method == 'POST':
        video = request.FILES.get('video_file')
        person_name= request.get('person_name')
        if not video:
            return render(request,"failure.html")  # Redirect to failure page if no video is provided

    try:
        folder_name = datetime.now().strftime('%d-%m-%y_%H-%M-%S')
        folder_path= os.path.join(settings.MEDIA_ROOT,"video_input_data", folder_name)
        os.makedirs(folder_path, exist_ok=True)
    except FileNotFoundError as e:
         print(e)
         return render(request, "error.html")  # Handle file not found

    video_path = os.path.join(folder_path, video.name)
    with open(video_path, 'wb+') as destination:
        for chunk in video.chunks():
            destination.write(chunk)
    print(folder_path)
    extract_frames(video_path, folder_path, interval=2)

    s=run_model_on_folder(folder_path, r'..\..\pt\Checkpoints.pt')
    print(s)
    print(f'video name {video.name}')
    if len(s)==len(glist):
        context={
            "dg_no": os.path.splitext(video.name)[0],
            "found": list(s),
            "uploaded_by":person_name
        }
        request.session['context'] = context  # Store context in the session
        return redirect('success')
        # return render(request,'success.html',context)
    else:
        diff=glist-s
        context = {
            "notfound": list(diff),
            "found":list(s),
            "dg_no": os.path.splitext(video.name)[0],
            "uploaded_by":person_name
        }
        print(glist)
        print("-------------------------------------------------------------")
        print(s)
        print("-------------------------------------------------------------")
        print(diff)
        print("-------------------------------------------------------------")
        request.session['context'] = context  # Store context in the session
        return redirect('failure')
        # return render(request,"failure.html",context)
    return render(request, "index.html")

def index(request):
    return  render(request, "index.html")
def success(request):
    context = request.session.get('context', {})  # Retrieve the context from the session
    print(f"Success context: {context}")
    return render(request, "success.html", context)


def failure(request):
    context = request.session.get('context', {})  # Retrieve the context from the session
    print(f"Failure context: {context}")
    return render(request, "failure.html", context)

def inprogress(request):
    return render(request, "loader.html")

