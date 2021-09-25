import json
import requests
from datetime import datetime

IPADDRESS = '127.0.0.1'
PORT = '8000'

#call to send vitals data to api
def send_data_to_api(datetimeStr, steps, heartRate, temperature):
    dt = datetime.strptime(datetimeStr, '%m/%d/%Y %I:%M:%S %p')
    validDt = dt.strftime('%Y-%m-%dT%H:%M:%S')
    data = {
        'datetime': validDt,
        'heartRate': heartRate,
        'steps': steps,
        'temperature': temperature
    }

    r = requests.post('http://' + IPADDRESS + ':' + PORT + '/vitalsdata/', json=data)
    print(r.json())


# example
# send_data_to_api('12/23/2000 01:13:13 PM', 12000, 500, 27)
