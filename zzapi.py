# from sinchsms import SinchSMS
# import time
# from time import sleep


# def sendSMS():

#     # enter all the details
#     # get app_key and app_secret by registering
#     # a app on sinchSMS
#     number = '447520651139'
#     app_key = '21d042c387334abdb8555ecc83c36faa'
#     app_secret = '3b8ae4caffbd43d99d7868e146af7d7a'

#     # enter the message to be sent
#     message = 'Hello Message!!!'

#     client = SinchSMS(app_key, app_secret)
#     print("Sending '%s' to %s" % (message, number))

#     response = client.send_message(number, message)
#     message_id = response['messageId']
#     response = client.check_status(message_id)

#     # keep trying unless the status returned is Successful
#     while response['status'] != 'Successful':
#         print(response['status'])
#         time.sleep(1)
#         response = client.check_status(message_id)

#     print(response['status'])


# if __name__ == "__main__":
#     sendSMS()

import requests
import json

# resp =
#
# print(resp.status_code, resp.text)
