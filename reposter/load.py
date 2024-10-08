import json
import requests
from bs4 import BeautifulSoup


def read_file(attachment):
    response = requests.get(attachment.url)
    response.raise_for_status()

    if (messages := read_as_json_in_html(response)) is not None:
        return messages, "json"
    elif (messages := read_as_html(response)) is not None:
        return messages, "html"
    else:
        return None


def read_as_json_in_html(response):
    for line in str(response.content, encoding="utf-8").split("\n"):
        if line.strip()[:16] == "let messages = [":
            return json.loads(line.strip()[15:-1])


def read_as_html(response):
    soup = BeautifulSoup(str(response.content, encoding="utf-8"), "lxml")
    messages = soup.find_all("div", { "class": "chatlog__message-group" })
    if len(messages) > 0:
        return messages
    return None


def split_messages(messages, file_type):
    if file_type == "html":
        return list(collect_messages_html(messages))
    elif file_type == "json":
        return []
    return []


def collect_messages_html(messages):
    post = ""

    for message in messages:
        next_group, had_attachments = format_message_group(message)
        if next_group is None:
            continue

        if had_attachments:
            yield post + next_group
            post = ""
        else:
            post += next_group

    if len(post) > 0:
        yield post


def format_message_group(group):
    string = ""
    had_attachments = False
    messages = group.find_all("div", { "class": "chatlog__message" })
    header = group.find("div", { "class": "chatlog__header" })
    if header is None:
        return None, False

    author = header.find("span", { "class": "chatlog__author" })
    nickname = author.text
    timestamp = header.find("span", { "class": "chatlog__timestamp" })
    
    string += f"**{nickname} ({author['title']})** *{timestamp['title']}*\n"
    for message in messages:
        content = message.find("div", { "class": "chatlog__content chatlog__markdown" })
        if content is not None:
            string += content.text + "\n"
            emojis = content.find_all("img", { "class": "chatlog__emoji" })
            if emojis is not None and len(emojis) > 0:
                had_attachments = True
                for emoji in emojis:
                    string += f"{emoji['src']}\n"

        attachments = message.find_all("div", { "class": "chatlog__attachment" })
        if attachments is not None and len(attachments) > 0:
            had_attachments = True
            for attachment in attachments:
                if (link := attachment.find("a")) is not None:
                    string += f"{link['href']}\n"
                elif (video := attachment.find("video")) is not None:
                    string += f"{video.source['src']}\n"
    return string + "\n", had_attachments
