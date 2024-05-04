# Lauren Cho
# LCHO6@UCI.EDU
# 91059503
#
# test_ds_messenger.py

from ds_messenger import DirectMessenger


def test_send():
    """
    Test send function.
    """
    messenger1 = DirectMessenger(dsuserver='168.235.86.101', username="bippy111", password='bippy123')
    recipient1 = "somethingeasier"
    message1 = "I need spring break."
    assert messenger1.send(message1, recipient1) is None


def test_retrieve_new():
    """
    Test retrieve_new Function.
    """
    messenger1 = DirectMessenger(dsuserver='168.235.86.101', username="bippy111", password='bippy123')
    recipient1 = "laurlaur1"
    message1 = "I need a break."
    messenger1.send(message1, recipient1)

    messenger2 = DirectMessenger(dsuserver='168.235.86.101', username="laurlaur1", password='abc123')
    new_msg = messenger2.retrieve_new()

    assert isinstance(new_msg, list) is False
    assert len(new_msg) == 1


def test_retrieve_all():
    """
    Test retrieve_all Function.
    """
    messenger1 = DirectMessenger(dsuserver='168.235.86.101', username="bippy222", password='bippy123')
    recipient1 = "laurlaur2"
    message1 = "I don't like testing."
    messenger1.send(message1, recipient1)

    messenger2 = DirectMessenger(dsuserver='168.235.86.101', username="laurlaur2", password='abc123')
    new_msg = messenger2.retrieve_all()

    assert isinstance(new_msg, list)
    assert new_msg[0].recipient == "bippy222"
    assert new_msg[0].message == "I don't like testing."
