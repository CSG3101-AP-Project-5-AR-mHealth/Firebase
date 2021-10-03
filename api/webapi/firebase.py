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

# [START retrieve_access_token]
def get_access_token():
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      'service-account.json', SCOPES)
  access_token_info = credentials.get_access_token()
  return access_token_info.access_token
# [END retrieve_access_token]

def send_fcm_message(fcm_message):
  # [START use_access_token]
  headers = {
    'Authorization': 'Bearer ' + get_access_token(),
    'Content-Type': 'application/json; UTF-8',
  }
  # [END use_access_token]
  resp = requests.post(FCM_URL, data=json.dumps(fcm_message), headers=headers)

  if resp.status_code == 200:
    print('Message sent to Firebase for delivery, response:')
    print(resp.text)
  else:
    print('Unable to send message to Firebase')
    print(resp.text)

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
  '''{
    'message': {
      'notification': {
        'title': 'API Test Notification',
        'body': 'Test Successful!'
      },
      'token': registrationToken or REGISTRATION_TOKEN
    }
  }'''

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--message')
  args = parser.parse_args()
  if args.message and args.message == 'common-message':
    common_message = build_common_message()
    print('FCM request body for message using common notification object:')
    print(json.dumps(common_message, indent=2))
    send_fcm_message(common_message)
  else:
    print('''Invalid command. Please use one of the following commands:
python messaging.py --message=common-message''')


#main()
