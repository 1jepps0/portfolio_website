from django.shortcuts import render, redirect
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

from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from .forms import ContactForm 


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

        print("Request Data:", request.data)
        print("Request Files:", request.FILES)

        serializer = CtfWriteupSerializer(data=request.data)

        if serializer.is_valid():

            print("Serializer is valid")
            writeup = serializer.save()
            return Response(
                {"message": "Writeup uploaded successfully!"},
                status=status.HTTP_201_CREATED,
            )

        else:
            print("Serializer errors:", serializer.errors)  
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
def contact_view(request):

    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():

            name = form.cleaned_data["name"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            sender = form.cleaned_data["email"]
            true_sender = "JacobEppsWebsiteForm@gmail.com"

            recipients = ["1jepps10@gmail.com"]

            full_message = f"Name: {name}\nSubject: {subject}\nSender Email: {sender}\n\nMessage:\n{message}"
            full_subject = f"Form Message from {name} Subject: {subject}"

            send_mail(full_subject, full_message, true_sender, recipients)

            # return HttpResponseRedirect("/success")

    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})
