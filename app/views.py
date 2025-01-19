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

import ast
import os


def home_view(request):
    return render(request, "home.html")

def writeups_view(request):
    writeups = CtfWriteup.objects.all()

    # get unique categories to use for the filter
    unique_cats = list({writeup.category for writeup in writeups})
    competitions = list({writeup.competition for writeup in writeups})

    # get selected comp based on filter
    selected_competition = request.GET.get('competition-filter', 'all')
    selected_category = request.GET.get('category-filter', 'all')

    # Filter writeups based on the selected competition and category
    if selected_competition != 'all':
        writeups = writeups.filter(competition=selected_competition)
    if selected_category != 'all':
        writeups = writeups.filter(category=selected_category)

    
    # organize writeups based on competition:category
    organized_writeups = defaultdict(lambda: defaultdict(list))
    url_name = ""
    for writeup in writeups:
        setattr(writeup, "tags", ast.literal_eval(writeup.tags))
        url_name = slugify(writeup.name).replace("-", "%20")
        organized_writeups[writeup.competition][writeup.category].append(writeup)

    # sort the writeups by date so the most recent ones appear on top
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

    



    context = {
        'writeups': dict(sorted_organized_writeups),
        'selected_competition': selected_competition,
        'selected_category': selected_category,
        'unique_categories': unique_cats,
        'unique_competitions': competitions,
    }

    return render(request, 'writeups.html', context)

def projects_view(request):
    return render(request, "projects.html")

def portfolio_website_view(request):
    return render(request, "portfolio_website.html")
 
def writeup_view(request, writeup_name):
    objects = CtfWriteup.objects.all()
    context = {}

    for object in objects:
        if object.name == writeup_name:
            tag_list = ast.literal_eval(object.tags)
            context["tags"] = tag_list
            context["data"] = object
   
    print(context["tags"])
    return render(request, "writeup.html", context)




class WriteupUploadAPIView(APIView):

    password = os.getenv("WRITEUP_PASSWORD") 

    def post(self, request):
        sent_password = request.data.get("password")

        if sent_password != self.password:
            return Response(
                {"message": "Invalid Password"},
                status=status.HTTP_403_FORBIDDEN,
            )

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
            true_sender = os.getenv("EMAIL_USER")

            recipients = ["1jepps10@gmail.com"]

            full_message = f"Name: {name}\nSubject: {subject}\nSender Email: {sender}\n\nMessage:\n{message}"
            full_subject = f"Form Message from {name} Subject: {subject}"

            send_mail(full_subject, full_message, true_sender, recipients)

            return HttpResponseRedirect("/success")

    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})

def success_view(request):
    return render(request, "success.html")

