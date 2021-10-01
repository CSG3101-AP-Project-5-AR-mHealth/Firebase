from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from webapi.models import InputData, Registration
from webapi.serializers import InputDataSerializer, RegistrationSerializer
from .firebase import send_fcm_message, build_common_message
from timeseries_model.run_model import predict_anomaly


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
        print(serializer.errors)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def inputdata_adddata(request):
    if request.method == 'GET':
        return HttpResponse(status=404)

    if request.method == 'POST':
        data = JSONParser().parse(request)      
        serializer = InputDataSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()

            process_model_on_recent_data(serializer.data)

            return JsonResponse(serializer.data, status=201, safe=False)
        return JsonResponse(serializer.errors, status=400)

def process_model_on_recent_data(data):
    # call model here
    anomalies = predict_anomaly(data)
    if anomalies[0].size:
        print("Anomaly detected at: ", data[anomalies[0][0]])
        fcm_token = Registration.objects.all().order_by('-id')[:1]
        print("Sending Notification")
        #send_fcm_message(build_common_message(fcm_token))

