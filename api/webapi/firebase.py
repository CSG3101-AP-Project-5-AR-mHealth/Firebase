import argparse
import json
import requests

from oauth2client.service_account import ServiceAccountCredentials

PROJECT_ID = 'mheathtest'
BASE_URL = 'https://fcm.googleapis.com'
FCM_ENDPOINT = 'v1/projects/' + PROJECT_ID + '/messages:send'
FCM_URL = BASE_URL + '/' + FCM_ENDPOINT
SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']
REGISTRATION_TOKEN = 'cW_lKsfmRiydbo0EA-7Nde:APA91bGCtHTnyIhKQ-Stx6Y6TrCwI2zCI2RLnV2vSmLD2a05FaL2OiySO2uCs8cuxWQjGScgZPOptgo-ec_9LB5xEKMPcSIPTJpMQm3966dggn33RNCGRvBUgmlCCmFXBoyepAXzgQza'

# [START retrieve_access_token]
def get_access_token():
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      'service-account.json', SCOPES)
  access_token_info = credentials.get_access_token()
  return access_token_info.access_token
# [END retrieve_access_token]

def send_fcm_message(fcm_message, registration_token = None):
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

def build_common_message(registrationToken = None):
  return {
    'message': {
      'notification': {
        'title': 'API Test Notification',
        'body': 'Test Successful!'
      },
      'token': registrationToken or REGISTRATION_TOKEN
    }
  }

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
