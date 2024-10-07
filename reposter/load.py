import json
import requests
from bs4 import BeautifulSoup


current_file = None


def set_current_file(attachment):
    global current_file
    response = requests.get(attachment.url)
    response.raise_for_status()

    for line in str(response.content, encoding="utf-8").split("\n"):
        if line.strip()[:16] == "let messages = [":
            current_file = json.loads(line.strip()[15:-1])
            return True
    return False


def set_current_file2(attachment):
    global current_file
    response = requests.get(attachment.url)
    response.raise_for_status()

    soup = BeautifulSoup(str(response.content, encoding="utf-8"), 'html.parser')
    # div class="chatlog__message-group"

def get_current_file():
    global current_file
    return current_file
