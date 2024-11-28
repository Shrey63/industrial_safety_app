from django.http import request
from django.shortcuts import render, redirect
from .utils import *
from .model_runner import *
from django.http import HttpResponse
import json

glist = {'CPCBSticker',
         'Documentfolder',
         'Raingaurd',
         'efficientpowersticker',
         'doanddontsticker',
         'warningsticker',
         'phonenumber',
         'doorhandle',
         'doorstopper',
         'emergencybutton',
         'genset nameplate',
         'hinges',
         'mahindrasticker',
         'powerol_sticker',
         'shyamglobalsticker',
         }

def process(request):
    # Run Helmet Detection Model
    print("---------------------done-------------------")
    if request.method == 'POST':
        video = request.FILES.get('video_file')
        if not video:
            return render(request,"failure.html")  # Redirect to failure page if no video is provided

    folder_name = "input_data"
    try:
        folder_name = datetime.now().strftime('%d-%m-%y_%H-%M-%S')
        folder_path= os.path.join(settings.MEDIA_ROOT_CHECKPOINT, "input_data", folder_name)
        os.makedirs(folder_path, exist_ok=True)
    except FileNotFoundError as e:
         print(e)
         return render(request, "error.html")  # Handle file not found

    video_path = os.path.join(folder_path, video.name)
    with open(video_path, 'wb+') as destination:
        for chunk in video.chunks():
            destination.write(chunk)
    print(folder_path)
    extract_frames(video_path, folder_path, interval=1)

    s=run_model_on_folder(folder_path, r'..\..\pt\Checkpoints.pt')
    print(s)
    if len(s)==len(glist):
        context={
            "found": list(s)
        }
        # response = redirect('success')  # Create a redirect response
        # response.set_cookie('context', json.dumps(context))  # Store context in a cookie
        # return response
        return render(request,'success.html',context)
    else:
        diff=glist-s
        context = {
            "notfound": list(diff),
            "found":list(s)
        }
        print(glist)
        print("-------------------------------------------------------------")
        print(s)
        print("-------------------------------------------------------------")
        print(diff)
        print("-------------------------------------------------------------")
        # response = redirect('failure')  # Create a redirect response
        # response.set_cookie('context', json.dumps(context))  # Store context in a cookie
        # return response
        return render(request,"failure.html",context)
    return render(request, "index.html")

def index(request):
    return  render(request, "index.html")
def success(request):
    context = request.COOKIES.get('context', '{}')  # Retrieve the cookie
    context = json.loads(context)  # Load the context from the cookie
    print(f"failure context: {context}")
    return render(request, "success.html", context)

def failure(request):
    context = request.COOKIES.get('context', '{}')  # Retrieve the cookie
    context = json.loads(context)  # Load the context from the cookie
    print(f"failure context: {context}")
    return render(request, "failure.html", context)

def inprogress(request):
    return render(request, "loader.html")

