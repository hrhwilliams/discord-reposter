from re import finditer
from datetime import datetime
import discord, asyncio

currently_posting = False

# Retry parameters
RETRY_LIMIT = 10
RETRY_DELAY = 2  # Seconds to wait before retrying


async def ping(channel):
    await channel.send("pong!")


async def whoami(message):
    await message.channel.send(f"{message.author.id}")


async def send_message(channel, message):
    if len(message) == 0:
        return
    for attempt in range(RETRY_LIMIT):
        try:
            await channel.send(message)
            return  # Successfully sent, exit the function
        except discord.HTTPException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            print(message)
            await asyncio.sleep(RETRY_DELAY)
    print(f"Failed to send message after {RETRY_LIMIT} attempts")


async def startposting(j, channel):
    global currently_posting

    if currently_posting:
        await channel.send("but im already doing that!!")
        return

    currently_posting = True
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
