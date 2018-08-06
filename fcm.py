import pyfcm
import os
import json
import secret

TOKEN_FILE = os.path.join(os.path.dirname(__file__), 'tokens.json')


class FCM:

    __service = None
    __tokens = []

    def __init__(self):
        self.__service = pyfcm.FCMNotification(api_key=secret.API_KEY)
        if os.path.isfile(TOKEN_FILE):
            self.__tokens = json.load(open(TOKEN_FILE, "r"))
        else:
            with open(TOKEN_FILE, "wb") as f:
                f.write(bytes("[]".encode("utf-8")))

    def send_message(self, title, message, params=None):
        if params is None:
            params = {}
        data_message = {
            "title": title,
            "message": message
        }
        data_message.update(params)
        print(self.__service.notify_multiple_devices(
            registration_ids=self.__tokens,
            data_message=data_message
        ))

    def add_token(self, token):
        self.__tokens.append(token)
        json.dump(self.__tokens, open(TOKEN_FILE, "w"))
