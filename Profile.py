# Lauren Cho
# LCHO6@UCI.EDU
# 91059503
#
# Profile.py

"""
Contains the profile class needed for each user to have their own profile.
"""

import json
import time
from pathlib import Path


class DsuFileError(Exception):
    """
    DsuFileError is a custom exception handler that you should catch in your
    own code. It is raised when attempting to load or save Profile objects to
    file the system.
    """


class DsuProfileError(Exception):
    """
    DsuProfileError is a custom exception handler that you should catch in
    your own code. It is raised when attempting to deserialize a dsu file
    to a Profile object.
    """


class Timestamp:
    """
    The Timestamp class takes a string entry and stores it into a dictionary
    with the time [shigan] being the key. Shigan is time in Korean.
    """
    def __init__(self, shigan: float = 0, entry: str = None) -> None:
        """
        Initializes objects needed to get the timestamp.
        """
        self.shigan = shigan
        self.entry = entry

    def make_dict(self) -> dict:
        """
        Allows the timestamp to be stored in a dictionary with messages
        """
        store_msg = {}
        store_msg[self.shigan] = self.entry
        return store_msg


class Profile:
    """
    The Profile class exposes the properties required to join
    an ICS 32 DSU server. You will need to use this class to manage
    the information provided by each new user created within your program
    for a2. Pay close attention to the properties and functions in this
    class as you will need to make use of each of them in your program.
    """

    def __init__(self, dsuserver=None, username=None, password=None):
        """
        Initializes the objects called on for profile.
        """
        self.dsuserver = dsuserver  # REQUIRED
        self.username = username  # REQUIRED
        self.password = password  # REQUIRED
        self.contacts = {}
        if username is not None:
            self.path = './' + self.username + '.dsu'

    def add_contact(self, name: str, path) -> None:
        """
        Adds contacts to a dictionary so that it can be accessed later
        in the GUI.
        """
        self.contacts[name] = []
        self.save_profile(path)

    def add_message(self, path, name: str, message: str, its_me: bool = False):
        """
        Adds messages to the contacts list so that it can be accessed
        later in the GUI.
        """
        message = '[' + str(its_me) + ']' + ' ' + message
        timestamp_obj = Timestamp(time.time(), message)
        self.contacts[name].append(timestamp_obj.make_dict())
        self.save_profile(path)

    def save_profile(self, path: str) -> None:
        """
        save_profile accepts an existing dsu file to save the current
        instance of Profile to the file system.

        Example usage:

        profile = Profile()
        profile.save_profile('/path/to/file.dsu')

        Raises DsuFileError
        """
        the_p = Path(path)

        if the_p.exists() and the_p.suffix == '.dsu':
            try:
                with open(the_p, 'w', encoding='utf-8') as the_f:
                    json.dump(self.__dict__, the_f)
            except Exception as ex:
                raise DsuFileError("Error while attempting to process the DSU file.", ex) from ex  # pylint: disable=line-too-long
        else:
            raise DsuFileError("Invalid DSU file path or type")

    def load_profile(self, path: str) -> None:
        """
        load_profile will populate the current instance of Profile
        with data stored in a DSU file.

        Example usage:

        profile = Profile()
        profile.load_profile('/path/to/file.dsu')

        Raises DsuProfileError, DsuFileError
        """
        the_p = Path(path)

        if the_p.exists() and the_p.suffix == '.dsu':
            try:
                with open(the_p, 'r', encoding='utf-8') as the_f:
                    obj = json.load(the_f)
                    self.username = obj['username']
                    self.password = obj['password']
                    self.dsuserver = obj['dsuserver']
                    self.contacts = obj['contacts']

            except Exception as ex:
                raise DsuProfileError(ex) from ex
        else:
            raise DsuFileError()
