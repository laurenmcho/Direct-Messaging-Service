# Lauren Cho
# LCHO6@UCI.EDU
# 91059503
#
# ds_protocol.py

"""
Creates protocols for the server by using JSON
to find information.
"""

import json
from collections import namedtuple

# Namedtuple to hold the values retrieved from json messages.
DataTuple = namedtuple('DataTuple', ['response_type', 'response_message',
                                     'token', 'messages'])
PORT = 3021


def extract_json(json_msg: str) -> DataTuple:
    '''
    Call the json.loads function on a json string and convert
    it to a DataTuple object.
    '''

    try:
        json_obj = json.loads(json_msg)
        response_type = json_obj['response']['type']
        response_message = json_obj['response'].get('message', None)

        if 'token' in json_obj['response']:
            token = json_obj['response']['token']
        else:
            token = ''

        if 'messages' in json_obj['response']:
            messages = json_obj['response']['messages']
        else:
            messages = []

    except json.JSONDecodeError:
        print("Json cannot be decoded.")
        return None

    return DataTuple(response_type, response_message, token, messages)


def join(username, password, token=""):
    """
    Returns a JSON string that contains the username, password, and token.
    """
    return json.dumps({"join": {"username": username, "password": password,
                                "token": token}})


def directmessage(token, message, recipient, timestamp):
    """
    Returns a JSON string that contains the token and entry. The entry
    contains the message, recipient, and timestamp for the direct message.
    """
    return json.dumps({"token": token, "directmessage":
                       {"entry": message,
                        "recipient": recipient,
                        "timestamp": timestamp}})


def retrieve_dm(token, direct_message):
    """
    Returns a JSON string that contains the token and message
    to retrieve the direct message.
    """
    return json.dumps({"token": token, "directmessage": direct_message})
