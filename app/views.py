from django.shortcuts import render
from app.models import *
from collections import *
from datetime import *
from pathlib import Path
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CtfWriteupSerializer

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



            context["data"] = object
   
    return render(request, "writeup.html", context)


class WriteupUploadAPIView(APIView):
    def post(self, request):
        serializer = CtfWriteupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Writeup uploaded successfully!"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def writeup_upload(request):
    if request.method == "POST":          

        try:
            name = request.POST.get("name", "default_name")  
            category = request.POST.get("category", "No Category")
            competition = request.POST.get("competition", "Unknown")
            point_count = request.POST.get("point_count", 0)
            description = request.POST.get("description", "")
            tags = request.POST.get("tags", "")
            hints = request.POST.get("hints", "")
            author = request.POST.get("author", "Unknown")
            markdown_body = request.POST.get("markdown_body", "")

            cur_date = datetime.now().strftime("%Y-%m-%d")

            writeup = CtfWriteup.objects.create_writeup(
                name=name,
                category=category,
                competition=competition,
                point_count=point_count,
                description=description,
                tags=tags,
                hints=hints,
                date=cur_date,
                author=author,
                markdown_body=markdown_body,
            )

            context = {"message": "Writeup uploaded successfully!"}
            return render(request, "upload_response.html", context)

        except Exception as e:
            context = {"message": e}
            return render(request, "upload_response.html", context)



    context = {"message": "Wrong method"}
    return render(request, "upload_response.html", context)

