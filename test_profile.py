# Lauren Cho
# lcho6@uci.edu
# 91059503
#
# test_profile.py

import pytest
from pathlib import Path
from Profile import DsuFileError
from Profile import DsuProfileError
from Profile import Timestamp
from Profile import Profile


def test_timestamp():
    time = Timestamp(123.456, "test entry")
    dictionary = time.make_dict()
    assert isinstance(dictionary, dict)
    assert len(dictionary) == 1
    assert 123.456 in dictionary
    assert dictionary[123.456] == "test entry"


def test_profile_init():
    profile = Profile("123", "test", "password")
    assert profile.dsuserver == "123"
    assert profile.username == "test"
    assert profile.password == "password"
    assert isinstance(profile.contacts, dict)


def test_profile_add_contact(name, path):

    profile = Profile("123", "test", "password")
    name = 'contact1'
    path = './test.dsu'
    profile.add_contact(name, path)
    assert 'contact1' in profile.contacts.keys()
    assert len(profile.contacts["contact1"]) == 0
    # profile.add_contact(name, 'the_path')
    # assert "contact1" in profile.contacts
    # assert len(profile.contacts["contact1"]) == 0   


def test_profile_add_message(path, name, message, b_val):
    profile = Profile("123", "test", "password")
    path = './test.dsu'
    name = 'contact1'
    message = 'test message'
    b_val = True
    profile.add_contact(name, path)

    profile.add_message(path, name, message, b_val)
    assert len(profile.contacts["contact1"]) == 1
    assert isinstance(profile.contacts["contact1"][0], dict)
    assert "test message" in profile.contacts["contact1"][0][list(profile.contacts["contact1"][0])[0]]


def test_profile_save_load(path=None):
    path = "./test.dsu"
    profile_1 = Profile("123", "test", "password")
    profile_1.add_contact("contact1", path)
    profile_1.add_message(path, "contact1",
                          "test message",
                          True)

    profile_2 = Profile()
    with pytest.raises(DsuFileError):
        profile_2.load_profile("./nonexistent.dsu")

    with pytest.raises(DsuFileError):
        profile_2.load_profile("./test.txt")

    with pytest.raises(DsuProfileError):
        profile_2.load_profile("./invalid.dsu")

    profile_1.save_profile(path)
    profile_2.load_profile(path)

    assert profile_1.dsuserver == profile_2.dsuserver
    assert profile_1.username == profile_2.username
    assert profile_1.password == profile_2.password
    assert profile_1.contacts == profile_2.contacts
