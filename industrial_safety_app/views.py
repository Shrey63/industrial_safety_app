from django.shortcuts import render

def home(request):
    return render(request, "notifier.html")

def success(request):
    return render(request, "success.html")

def failure(request):
    return render(request, "failure.html")

def notify(request):
    return render(request, "notifier.html")
