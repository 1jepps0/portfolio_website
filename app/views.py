from django.shortcuts import render
from app.models import *

# Create your views here.

def home_view(request):
    return render(request, "home.html")

def writeups_view(request):
    objects = CtfWriteup.objects.all()
    return render(request, "writeups.html", {"writeups": objects})

def contact_view(request):
    return render(request, "contact.html")

def projects_view(request):
    return render(request, "projects.html")
 
def writeup_view(request, writeup_name):
    objects = CtfWriteup.objects.all()
    context = {}
    attributes = ["name", "description", "competetion", "point_count",
                  "tags", "hints", "author", "body_text", "code_snippets", "image"]

    for object in objects:
        if writeup_name == object.name:
            for attribute in attributes:
                context[attribute] = getattr(object, attribute)
 

    return render(request, "writeup.html", context)


