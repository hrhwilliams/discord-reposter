import json
import requests

from datetime import datetime


current_file = None


def set_current_file(attachment):
    global current_file
    response = requests.get(attachment.url)
    response.raise_for_status()

    for line in str(response.content, encoding='utf-8').split('\n'):
        if line.strip()[:16] == 'let messages = [':
            current_file = json.loads(line.strip()[15:-1])
            break


def get_current_file():
    global current_file
    return current_file
