# Lauren Cho
# LCHO6@UCI.EDU
# 91059503
#
# test_ds_message_protocol.py

"""
Tests to make sure that the direct messaging protocol is implemented correctly.
"""

import ds_protocol


def test_extract_json():
    """
    Tests the extract_json function.
    """
    # Tests JSON string
    json_str = '{"response": {"type": "ok", "message": "Success!", "token": "12345", "messages": ["Message 1", "Message 2"]}}'
    expected_tuple = ds_protocol.DataTuple('ok', 'Success!', '12345', ['Message 1', 'Message 2'])
    assert ds_protocol.extract_json(json_str) == expected_tuple

    # Tests json string without token and messages
    json_str = '{"response": {"type": "ok", "message": "Success!"}}'
    expected_tuple = ds_protocol.DataTuple('ok', 'Success!', '', [])
    assert ds_protocol.extract_json(json_str) == expected_tuple

    # Tests string that's not json
    json_str = '{"response": {"type": "ok", "message": "Success!", "token": "12345", "messages": ["Message 1", "Message 2"]}'
    assert ds_protocol.extract_json(json_str) is None


def test_join():
    """
    Tests join function.
    """
    # Tests with empty token
    join_json1 = ds_protocol.join("testuser", "abc123")
    json_expected1 = '{"join": {"username": "testuser", "password": "abc123", "token": ""}}'
    assert join_json1 == json_expected1

    # Tests with token
    join_json2 = ds_protocol.join("testagain", "please", "12345")
    json_expected2 = '{"join": {"username": "testagain", "password": "please", "token": "12345"}}'
    assert join_json2 == json_expected2


def test_directmessage():
    """
    Tests the directmessage function.
    """
    json_dm1 = ds_protocol.directmessage('user_token', 'Hello world!',
                                         'laurlaur', 1603167689.3928561)
    json_dm2 = ds_protocol.directmessage('user_token_2', 'Test!',
                                         'bippy', 1234567890)
    assert json_dm1 == '{"token": "user_token", "directmessage": {"entry": "Hello world!", "recipient": "laurlaur", "timestamp": 1603167689.3928561}}'
    assert json_dm2 == '{"token": "user_token_2", "directmessage": {"entry": "Test!", "recipient": "bippy", "timestamp": 1234567890}}'


def test_retrieve_dm():
    """
    Tests retrieve_dm function.
    """
    json_retreive = ds_protocol.retrieve_dm("12345", "This is my message.")
    json_expected = '{"token": "12345", "directmessage": "This is my message."}'
    assert json_retreive == json_expected
