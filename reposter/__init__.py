from . import auth, commands, load
import discord


def create_client():
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    with open('allowlist.txt', 'r', encoding='utf-8') as file:
        for line in file.readlines():
            auth.allow(line.strip())

    @client.event
    async def on_ready():
        print(f'Logged in as {client.user}')

    @client.event
    async def on_message(message):
        if message.content.startswith('$'):
            match message.content:
                case '$ping':
                    await commands.ping(message.channel)
                case '$loadfile':
                    if not auth.auth(message.author):
                        await message.channel.send('https://tenor.com/view/wait-a-minute-who-are-you-kazoo-kid-funny-gif-16933963')
                    else:
                        for attachment in message.attachments:
                            if attachment.filename.split('.')[-1].lower() in ('htm', 'html'):
                                load.set_current_file(attachment)
                                await message.channel.send("success")
                                break
                case '$startposting':
                    if not auth.auth(message.author):
                        await message.channel.send('https://tenor.com/view/wait-a-minute-who-are-you-kazoo-kid-funny-gif-16933963')
                    elif (current_file := load.get_current_file()) is not None:
                        await commands.startposting(current_file, message.channel)
                    else:
                        await message.channel.send('no file loaded.')
                case '$whoami':
                    await commands.whoami(message)
                case _:
                    print(f'Attempted unknown command {message.content}')

    return client
