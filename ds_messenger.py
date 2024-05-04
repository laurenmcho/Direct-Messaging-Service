# Lauren Cho
# LCHO6@UCI.EDU
# 91059503
#
# ds_messenger.py
# 168.235.86.101

"""
Contains the DirectMessenger and DirectMessage class so that
the user can actually send and retrieve messages.
"""

import socket
import time
import ds_protocol


class DirectMessage:
    """
    Direct message class that contains the recipient, message,
    and timestamp.
    """
    def __init__(self):
        self.recipient = None
        self.message = None
        self.timestamp = None


class DirectMessenger:
    """
    Direct messenger class that allows a user to send a message, retrieve new
    messages, or retrieve all messages.
    """
    def __init__(self, dsuserver=None, username=None, password=None):
        """
        The data contents about the dsuserver, username, password, and
        previous timestamp are stored here.
        """
        self.token = None
        self.dsuserver = dsuserver
        self.username = username
        self.password = password

    def send(self, message: str, recipient: str) -> bool:
        """
        Sends the direct message and returns true if the message is
        successfully sent and false if send failed.

        :param message: The message to be sent.
        :param recipient: The recipient's username.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:

            try:
                client.connect((self.dsuserver, ds_protocol.PORT))
            except ConnectionError:
                return False
            except socket.gaierror:
                return False

            sending = client.makefile('w')
            recv = client.makefile('r')

            join_msg = ds_protocol.join(self.username, self.password)

            sending.write(join_msg + '\r\n')
            sending.flush()
            resp = recv.readline()

            data_tuple = ds_protocol.extract_json(resp)
            if data_tuple.response_type == 'error':
                print(data_tuple.response_message)
                return False

            token = data_tuple.token

            dm = DirectMessage()
            dm.recipient = recipient
            dm.message = message
            dm.timestamp = time.time()

            send_dm = ds_protocol.directmessage(token, dm.message,
                                                dm.recipient, dm.timestamp)

            sending.write(send_dm + '\r\n')
            sending.flush()
            resp = recv.readline()

            data_tuple = ds_protocol.extract_json(resp)
            if data_tuple.response_type == 'error':
                print(data_tuple.response_message)
                return False

    def retrieve_new(self) -> dict:
        """
        Returns a list of DirectMessage objects that contains all
        new messages.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            try:
                client.connect((self.dsuserver, ds_protocol.PORT))
            except ConnectionError:
                return False
            except socket.gaierror:
                return False

            sending = client.makefile('w')
            recv = client.makefile('r')

            join_msg = ds_protocol.join(self.username, self.password)

            sending.write(join_msg + '\r\n')
            sending.flush()
            resp = recv.readline()

            data_tuple = ds_protocol.extract_json(resp)
            if data_tuple.response_type == 'error':
                print(data_tuple.response_message)
                return False

            self.token = data_tuple.token

            retrieve_all_dm = ds_protocol.retrieve_dm(self.token, 'new')

            sending.write(retrieve_all_dm + '\r\n')
            sending.flush()
            resp = recv.readline()

            data_tuple = ds_protocol.extract_json(resp)

            if data_tuple.response_type == 'error':
                print(data_tuple.response_message)
                return False

            new_messages = {}
            dm = DirectMessage()
            for message in data_tuple.messages:
                dm.recipient = message['from']
                dm.message = message['message']
                dm.timestamp = message['timestamp']
                new_messages[dm.recipient] = dm.message

            return new_messages

    def retrieve_all(self) -> list:
        """
        Returns a list of DirectMessage objects that contains all
        messages.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            try:
                client.connect((self.dsuserver, ds_protocol.PORT))
            except ConnectionError:
                return False
            except socket.gaierror:
                return False

            sending = client.makefile('w')
            recv = client.makefile('r')

            join_msg = ds_protocol.join(self.username, self.password)

            sending.write(join_msg + '\r\n')
            sending.flush()
            resp = recv.readline()

            data_tuple = ds_protocol.extract_json(resp)
            if data_tuple.response_type == 'error':
                print(data_tuple.response_message)
                return False

            self.token = data_tuple.token

            retrieve_all_dm = ds_protocol.retrieve_dm(self.token, 'all')

            sending.write(retrieve_all_dm + '\r\n')
            sending.flush()
            resp = recv.readline()

            data_tuple = ds_protocol.extract_json(resp)

            if data_tuple.response_type == 'error':
                print(data_tuple.response_message)
                return False

            all_messages = []
            dm = DirectMessage()
            for message in data_tuple.messages:
                dm.recipient = message['from']
                dm.message = message['message']
                dm.timestamp = message['timestamp']
                all_messages.append(dm)

            return all_messages
