# Create your views here.


import datetime
import json
import os

from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from uptime import uptime

from django.views.decorators.csrf import csrf_exempt

"""
Function: get_current_server_time
...
Attributes
----------
request : JSON
    a formatted JSON response from the server which outputs the current date and time the request was posted by the user
"""


# Remove-item alias:curl

# http://127.0.0.1:8000/our_endpoints/server_time/
@require_http_methods(["GET"], )
def get_current_server_time(request):
    return HttpResponse(datetime.datetime.now())


"""
Function: upload_file 
... 
Attributes 
---------- 
request : JSON a formatted JSON response from the server which 
searches for 'text' and output a file with that associated naming convention 
to the endpoint and returns status 200 if successful
"""


# curl -X POST -F "text=@test.txt" http://127.0.0.1:8000/our_endpoints/upload_file/ (not working)
@csrf_exempt
@require_http_methods(["POST"], )
def upload_file(request):
    file = request.FILES['text']
    with open(file.name, 'wb') as dst:
        for chunk in file.chunks():
            dst.write(chunk)
        return HttpResponse(status=200)


"""
Function: check_connection
... 
Attributes 
---------- 
request : JSON, a formatted JSON response from the server returns
returns 200 status to indicate the server is functioning and the current 
server status and up time
"""


# curl -I --head http://127.0.0.1:8000/our_endpoints/check_connection/ (working)
@require_http_methods(["HEAD"])
def check_connection(request):
    response = HttpResponse(status=200)
    response['Server_Status'] = 'Up'
    response['Up_time'] = uptime()
    return response


"""
Function: save_json_to_file
... 
Attributes 
---------- 
request : JSON 
A formatted JSON response from the server 
prints body of request to a JSON file which is saved
to the end point and returns a status of 200
"""


# curl -X PUT -H "Content-Type: application/json" -d '{\"test01\": \"11011101\"}'
# http://127.0.0.1:8000/our_endpoints/save_json_to_file/ (working)
@csrf_exempt
@require_http_methods(["PUT"])
def save_json_to_file(request):
    # print('This is the returned request: ', request.body)
    data = json.loads(request.body)
    json_object = json.dumps(data, indent=4)
    with open("JSON_Data.json", "a") as f:
        f.write(json_object)
        return HttpResponse(status=200)


"""
Function: delete_file
... 
Attributes 
---------- 
request : JSON 
A formatted JSON response from the server 
returns an OS remove function which deletes the file matching 'file name'
from the request and returns a status of 200 when the file has been removed
"""


# curl -X DELETE -d "@My_Files/test02" http://127.0.0.1:8000/our_endpoints/delete_file/
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_file(request):
    py_json = json.loads(request.body)
    # print('This is py_json: ', py_json)
    try:
        os.remove('My_Files/' + py_json['file_name'])
        return HttpResponse(status=200)
    except OSError:
        return HttpResponse(status=500)


"""
Function: update_file
... 
Attributes 
---------- 
request : JSON 
A formatted JSON response from the server 
returns the body of the request as a new file which
overwrites the data of the selected file
"""


@csrf_exempt
@require_http_methods(["PATCH"])
def update_file(request):
    data = json.loads(request.body)
    with open('records.txt', 'a') as f:
        f.write(data['updates'])
        return HttpResponse(status=200)
