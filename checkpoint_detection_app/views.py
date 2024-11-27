from django.http import request
from django.shortcuts import render, redirect
from .utils import *
from .model_runner import *
glist = {'CPCBSticker',
         'Documentfolder',
         'Raingaurd',
         'doanddontsticker',
         'doorhandle',
         'doorstopper',
         'efficientpowersticker',
         'emergencybutton',
         'genset nameplate',
         'hinges',
         'mahindrasticker',
         'phonenumber',
         'powerol_sticker',
         'shyamglobalsticker',
         'warningsticker'}




def index(request):
    # Run Helmet Detection Model
    folder_name = "input_data"
    try:
        folder_path= get_latest_image(folder_name)
        print(f"Latest image path: {folder_path}")
    except FileNotFoundError as e:
         print(e)
         return render(request, "error.html")  # Handle file not found


    s=run_model_on_folder(folder_path, r'..\..\pt\Checkpoints.pt')
    print(s)
    if len(s)==len(glist):
        context={
            "found":s
        }
        return render(request, "success.html",context)
    else:
        diff=glist-s
        context = {
            "not-found": diff,
            "found":s
        }
        print(glist)
        print("-------------------------------------------------------------")
        print(s)
        print("-------------------------------------------------------------")
        print(diff)
        print("-------------------------------------------------------------")
        return render(request, "failure.html",context)
    # Run Shoes Detection Model
    # detection_keyword="no-shoes"
    # shoes_detection = run_model(image_path, r'..\..\pt\shoes.pt', detection_keyword)
    # if shoes_detection == 0:
    #     request.session["violation_type"] = "shoes"
    #     request.session["detection_keyword"] = detection_keyword
    #     return redirect(f"/notify/")
    # print(shoes_detection)

    return render(request, "index.html")

def success(request):
    return render(request, "success.html")

def failure(request):
    return render(request, "failure.html")

