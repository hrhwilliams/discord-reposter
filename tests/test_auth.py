import os
import pytest
import reposter.auth as auth

class TestUser:
    def __init__(self, id):
        self.id = id

def test_auth():
    with open("tests/test_allowlist.txt", "w") as fp:
        fp.write("111222333444555666\n")
        fp.write("999888777666555444\n")

    auth.read_allowlist(filepath="tests/test_allowlist.txt")

    assert auth.auth(TestUser("111222333444555666")) == True
    assert auth.auth(TestUser("999888777666555444")) == True
    assert auth.auth(TestUser("555444333222111222")) == False
    assert auth.auth(TestUser("")) == False

    os.remove("tests/test_allowlist.txt")


def test_auth_invalid_allowlist():
    with open("tests/test_allowlist.txt", "w") as fp:
        fp.write("bad\n")
        fp.write("bad\n")

    with pytest.raises(ValueError):
        auth.read_allowlist(filepath="tests/test_allowlist.txt")
