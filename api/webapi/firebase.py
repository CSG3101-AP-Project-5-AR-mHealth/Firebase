import argparse
import json
import requests

from oauth2client.service_account import ServiceAccountCredentials

PROJECT_ID = 'mhealth-app-b0e54'
BASE_URL = 'https://fcm.googleapis.com'
FCM_ENDPOINT = 'v1/projects/' + PROJECT_ID + '/messages:send'
FCM_URL = BASE_URL + '/' + FCM_ENDPOINT
SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']
REGISTRATION_TOKEN = 'cRDItj-FQb-P7at0tu5Ykq:APA91bHifI8Z9A6h1j6sejVf48RfK2XajeYgafLLKCCvGl1AYl2jNbYYhtnuSOVhn2ezwCQjkhU6ADlT08VtWMYGp9mMbjJCT58o4v2SEa1Ym3z9uSA7-6LHMg6M0ytcngtc-tFbd1Dv'

# get OAuth2 token to use with FCM service
def get_access_token():
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      'webapi/service-account.json', SCOPES)
  access_token_info = credentials.get_access_token()
  return access_token_info.access_token

# send the fcm message to fcm servers, pass in the result of build_common_message
def send_fcm_message(fcm_message):
  headers = {
    'Authorization': 'Bearer ' + get_access_token(),
    'Content-Type': 'application/json; UTF-8',
  }

  resp = requests.post(FCM_URL, data=json.dumps(fcm_message), headers=headers)

  if resp.status_code == 200:
    print('Message sent to Firebase for delivery, response:')
    print(resp.text)
  else:
    print('Unable to send message to Firebase')
    print(resp.text)

# builds the json payload for the fcm message
# pass in the registration token from the android application and the anomalous
# heart rate to send in the notification
def build_common_message(registrationToken = None, heartRate = '200'):
  return {
    'message': {
        'notification': {
            'title': 'Anomalous Vitals Detected',
            'body': 'Are you ok?'
        },
        'data': {
            'heartRate': heartRate
        },
        'token': registrationToken or REGISTRATION_TOKEN
    }
  }

def main():
  common_message = build_common_message()
  print('FCM request body for message using common notification object:')
  print(json.dumps(common_message, indent=2))
  send_fcm_message(common_message)

# uncomment main to test run from the command line, to test this way will require
# the REGISTRATION_TOKEN to be set with the fcm registration token of the android
# application
#main()
