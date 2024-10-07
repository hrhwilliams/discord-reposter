from . import auth, commands, load
import discord


def create_client():
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    with open("allowlist.txt", "r", encoding="utf-8") as file:
        for line in file.readlines():
            auth.allow(line.strip())

    @client.event
    async def on_ready():
        print(f"Logged in as {client.user}")

    @client.event
    async def on_message(message):
        if message.content.startswith("$"):
            match message.content:
                case "$ping":
                    await commands.ping(message.channel)
                case "$loadfile":
                    await commands.load_file(message)
                case "$startposting":
                    await commands.start_posting(message)
                case "$whoami":
                    await commands.whoami(message)
                case _:
                    print(f"Attempted unknown command {message.content}")

    return client
