from django.http import request
from django.shortcuts import render, redirect
from .utils import *
from .model_runner import *


def index(request):
    # Run Helmet Detection Model
    folder_name = "input_data"
    try:
        image_path = get_latest_image(folder_name)
        print(f"Latest image path: {image_path}")
    except FileNotFoundError as e:
         print(e)
         return render(request, "error.html")  # Handle file not found


    run_model(image_path, r'..\..\pt\Checkpoints.pt')

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

