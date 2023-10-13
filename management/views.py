from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse

from django.shortcuts import redirect, render
from rest_framework.decorators import api_view, permission_classes

from rest_framework.response import Response
import requests

from dnd_data.models import Race, CharacterClass, Background, Alignment

from django.contrib.auth.decorators import login_required


@login_required
def get_management_tools(request):
    races = Race.objects.all()
    character_classes = CharacterClass.objects.all()
    context = {"races": races, "character_classes": character_classes}

    return render(request, "management.html", context)


@login_required
def update_races(request):
    existing_races = Race.objects.values_list("name", flat=True)
    fetch_new_data("races", existing_races, Race)


@login_required
def update_character_classes(request):
    existing_character_classes = CharacterClass.objects.values_list("name", flat=True)
    fetch_new_data("classes", existing_character_classes, CharacterClass)


@login_required
def update_backgrounds(request):
    existing_backgrounds = Background.objects.values_list("name", flat=True)
    fetch_new_data("backgrounds", existing_backgrounds, Background)


@login_required
def update_alignments(request):
    existing_alignments = Alignment.objects.values_list("name", flat=True)
    fetch_new_data("alignments", existing_alignments, Alignment)


def fetch_new_data(api_endpoint, existing_data, model):
    try:
        response = requests.get(f"https://www.dnd5eapi.co/api/{api_endpoint}")
        response.raise_for_status()

        fetched_data = response.json()["results"]

        for new_data in fetched_data:
            if new_data["name"] not in existing_data:
                model.objects.create(
                    name=new_data["name"],
                )

        return JsonResponse({"message": "success"}, status=201)

    except requests.exceptions.RequestException as e:
        return Response(
            {"message": f"Failed to fetch {api_endpoint} data: {str(e)}"}, status=500
        )
