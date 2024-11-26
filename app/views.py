from django.shortcuts import render
from app.models import *
from collections import *
from datetime import *
from pathlib import Path

# Create your views here.

def home_view(request):
    return render(request, "home.html")

def writeups_view(request):
    writeups = CtfWriteup.objects.all()

    organized_writeups = defaultdict(lambda: defaultdict(list))
    for writeup in writeups:
        organized_writeups[writeup.competition][writeup.category].append(writeup)


    sorted_organized_writeups = {
        competition: dict(categories)
        for competition, categories in sorted(
            organized_writeups.items(),
            key=lambda item: max(
                (writeup.date for cat in item[1].values() for writeup in cat),
                default=datetime.min
            ),
            reverse=True 
        )
    }

    organized_writeups = {k: dict(v) for k, v in sorted_organized_writeups.items()}

    return render(request, 'writeups.html', {'writeups': dict(sorted_organized_writeups)})

def contact_view(request):
    return render(request, "contact.html")

def projects_view(request):
    return render(request, "projects.html")
 
def writeup_view(request, writeup_name):
    objects = CtfWriteup.objects.all()
    context = {}

    for object in objects:
        if object.name == writeup_name:


            text = ''
            with object.markdown_body.open('r') as f:
                text = f.read()

            object.markdown_body = text
            context["data"] = object
   
    return render(request, "writeup.html", context)


