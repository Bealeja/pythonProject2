from django.http import HttpResponse
from uptime import uptime
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import datetime
import json


# Create your views here.
@require_http_methods(["GET"], )
def get_current_server_time(request):
    return HttpResponse(datetime.datetime.now())


@csrf_exempt
@require_http_methods(["POST"], )
def upload_file(request):
    file = request.FILES['text']
    with open(file.name, 'wb') as dst:
        for chunk in file.chunks():
            dst.write(chunk)
        return HttpResponse(status=200)


@require_http_methods(["HEAD"])
def check_connection(request):
    response = HttpResponse(status=200)
    response['Server_Status'] = 'Up'
    response['Up_time'] = uptime()
    return response


@csrf_exempt
@require_http_methods(["PUT"])
def save_json_to_file(request):
    json.loads
    data = json.loads(request.body)
    json_object = json.dumps(data, indent=4)
    with open("JSON_Data.json", "a") as f:
        f.write(json_object)
        return HttpResponse(status=200)
