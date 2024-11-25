from django.shortcuts import render
from app.models import *

# Create your views here.

def home_view(request):
    return render(request, "home.html")

def writeups_view(request):
    

    comp_dict = {}
    comps = []


    for object in objects:
        obj_comp = object.Competetion

        if not obj_comp in comps:
            comps.append(obj_comp)


    for comp in comps:
        categories = {}

        
        comp_dict[comp] = categories

    return render(request, "writeups.html", {"writeups": objects, "competetions": competetions, "categories": categories})

def contact_view(request):
    return render(request, "contact.html")

def projects_view(request):
    return render(request, "projects.html")
 
def writeup_view(request, writeup_name):
    objects = CtfWriteup.objects.all()
    context = {}
    attributes = ["name", "description", "competetion", "point_count",
                  "tags", "hints", "author", "markdown_body", "image"]

    for object in objects:
        if writeup_name == object.name:
            for attribute in attributes:
                context[attribute] = getattr(object, attribute)
 

    return render(request, "writeup.html", context)


