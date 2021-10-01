from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import viewsets
from dietapp.models import Food, Event, Energy
from dietapp.serializers import   FoodSerializer, EventSerializer, EnergySerializer

from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from pymongo import MongoClient
import functools

dietDateFormat = '%m-%d-%Y %I:%M %p'


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

def authenticateUser(token):
    #client = MongoClient("mongodb://localhost:27017")
    import requests
    from requests.structures import CaseInsensitiveDict
    headers = CaseInsensitiveDict()
    headers["Authorization"] = token
    try:
        response = requests.get("http://localhost:3300/user/verify", headers=headers)
        success = response.json()
    except HTTPError as http_err:
        print(http_err)
    return success.get('user')

def auth_user(func):
    @functools.wraps(func)
    def validate(*args, **kwargs):
        req = args[0]
        user = authenticateUser(req.META['HTTP_AUTHORIZATION'])
        if not user:
            return Response({"error": 'user invalid'})
        args = args + (user,)
        return func(*args, **kwargs)
    return validate



@api_view(['GET','POST'])
def Config(*args):
    request = args[0]
    user = args[1]
    if request.method == 'GET':

        config = Food.objects.all()

@api_view(['GET', 'POST'])
@auth_user
def List(*args):
    request = args[0]
    user = args[1]

    if request.method == 'GET':
        allfoods = Food.objects.all()
        foods = FoodSerializer(allfoods, many=True)
        return Response(foods.data)
    if request.method == 'POST':
        data = JSONParser().parse(request)
        eatenon = data['EatenOn']
        data['EatenOn'] = datetime.strptime(eatenon, dietDateFormat )
        data['User'] = user
        #data['EatenOn'] = datetime.now()
        serializer = FoodSerializer(data=data)
        collectLog = 'start'
        if serializer.is_valid():
            collectLog = collectLog + " is valid"
            serializer.save()
            return JSONResponse("Successfully saved Food")
        else:
            collectLog = collectLog + 'failed'
            return JSONResponse("did not save "+collectLog)


@api_view(['GET', 'POST'])
def Events(request):
    if request.method == 'GET':
        allevents = Event.objects.all()
        events = EventSerializer(allevents, many=True)
        return Response(events.data)
    if request.method == 'POST':
        data = JSONParser().parse(request)
        happenedon = data['HappenedOn']
        data['HappenedOn'] = datetime.strptime(happenedon, dietDateFormat)
        serializer = EventSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        return JSONResponse("Successfully saved Event")


@api_view(['GET', 'POST'])
def Energies(request):
    if request.method == 'GET':
        allenergies = Energy.objects.all()
        energyList = EnergySerializer(allenergies, many=True)
        return Response(energyList.data)
    if request.method == 'POST':
        data = JSONParser().parse(request)
        exertedon = data['ExertedOn']
        data['ExertedOn'] = datetime.strptime(exertedon, dietDateFormat)
        serializer = EnergySerializer(data=data)
        collectLog = 'start'
        if serializer.is_valid():
            collectLog = collectLog + " is valid"
            serializer.save()
            return JSONResponse("Successfully saved Food")
        else:
            collectLog = collectLog + 'failed'
            return JSONResponse("did not save " + collectLog)