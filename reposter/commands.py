from re import finditer
from datetime import datetime
from . import auth, load, user
import discord, asyncio


# Retry parameters
RETRY_LIMIT = 10
RETRY_DELAY = 2  # Seconds to wait before retrying


async def ping(channel):
    await channel.send("pong!")


async def whoami(message):
    await message.channel.send(f"{message.author.id}")


async def load_file(message):
    if not auth.auth(message.author):
        await message.channel.send(
            "https://tenor.com/view/wait-a-minute-who-are-you-kazoo-kid-funny-gif-16933963"
        )
        return
    
    if user.get_user_is_currently_posting(message.author):
        return

    for attachment in message.attachments:
        if attachment.filename.split(".")[-1].lower() in ("htm", "html",):
            if (message_tuple := load.read_file(attachment)) is not None:
                messages, fmt = message_tuple
                user.set_user_open_file(message.author, messages, fmt)
                await message.channel.send("success")
            else:
                await message.channel.send("failed to find messages to repost.")
            break


async def send_message(channel, message):
    '''automatically formats and splits'''
    if len(message) == 0:
        return
    message = message.replace("\n", "\n> ")
    while len(message) > 1900:
        break_at = message.find(" ", 990)
        smaller_message = message[:break_at]
        await send_with_retry(channel, smaller_message)
        message = "> " + message[break_at+1:]
    await send_with_retry(channel, message)


async def send_with_retry(channel, message):
    for attempt in range(RETRY_LIMIT):
        try:
            await channel.send(message)
            return  # Successfully sent, exit the function
        except discord.HTTPException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            print(message)
            await asyncio.sleep(RETRY_DELAY)


async def start_posting(message):
    if (message_tuple := user.get_user_open_file(message.author)) is None:
        await message.channel.send("nothing to repost")
        return

    if user.get_user_is_currently_posting(message.author):
        await message.channel.send("but im already doing that!!")
        return
    
    user.set_user_is_currently_posting(message.author, True)
    messages, fmt = message_tuple

    for m in load.split_messages(messages, fmt):
        await send_message(message.channel, m)

    user.set_user_is_currently_posting(message.author, False)
    await message.channel.send("all done")

    currently_posting = False
    return
    current_timestamp = None
    message_to_send = ""
    for message in j:
        if len(message_to_send) > 1200:
            await send_message(channel, message_to_send)
            message_to_send = ""

        timestamp = datetime.fromisoformat(message["timestamp"])
        if current_timestamp is None or not (
            timestamp.day == current_timestamp.day
            and timestamp.month == current_timestamp.month
            and timestamp.year == current_timestamp.year
        ):
            message_to_send += f"# {timestamp.year}-{timestamp.month}-{timestamp.day}\n"
            current_timestamp = timestamp

        message_to_send += (
            f'> **{message["author"]["username"]}**: {message["content"]}\n\n'
        )

        if len(message["attachments"]) > 0:
            message_to_send += f'**{message["author"]["username"]}** embeds:\n'
            for attachment in message["attachments"]:
                message_to_send += f'{attachment["url"]}\n'
            await send_message(channel, message_to_send)
            message_to_send = ""
    await send_message(channel, message_to_send)
