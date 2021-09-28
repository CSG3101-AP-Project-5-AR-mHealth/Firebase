import json
import requests
import urllib3
from datetime import datetime

#LAN IP where django server is running
IPADDRESS = '192.168.1.107'
PORT = '8000'

#call to send vitals data to api
def send_data_to_api(datetimeStr, steps, heartRate, temperature):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    dt = datetime.strptime(datetimeStr, '%m/%d/%Y %I:%M:%S %p')
    validDt = dt.strftime('%Y-%m-%dT%H:%M:%S')
    data = {
        'datetime': validDt,
        'heartRate': heartRate,
        'steps': steps,
        'temperature': temperature
    }

    r = requests.post('https://' + IPADDRESS + ':' + PORT + '/vitalsdata/', json=data, verify=False)
    print(r.json())


# example
send_data_to_api('12/23/2000 01:13:13 PM', 12000, 500, 27)
