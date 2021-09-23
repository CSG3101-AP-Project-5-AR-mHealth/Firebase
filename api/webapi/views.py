from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from webapi.models import InputData, Registration
from webapi.serializers import InputDataSerializer, RegistrationSerializer

@csrf_exempt
def registration_addtoken(request):
    if request.method == 'GET':
        return HttpResposne(status=404)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = RegistrationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def inputdata_adddata(request):
    if request.method == 'GET':
        return HttpResposne(status=404)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = InputDataSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
