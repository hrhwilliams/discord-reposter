# Discord Reposter

A simple Discord bot for reposting the contents of a chat downloaded using
DiscordChatExporter. This requires Python version 3.10 or greater.

## Setup

Create a text file named `token.txt` and paste your Discord bot token inside.
Create another text file named `allowlist.txt` and the Discord IDs of everyone
you want to allow to use the bot inside, one ID on each line. Next, use the
`requirements.txt` to download the third-party libraries used by the bot like
so:

```
$ python -m pip install -r requirements.txt
```

Having done all of that, you can now bring the bot online by running:

```
$ python main.py
```

## Usage

Upload the file you want to repost along with the command `$loadfile` to have
the bot open and parse a chat export. To begin reposting, send the message
`$startposting` in the channel you wish to have the bot repost in.

There is no way to tell the bot to stop once it has begun reposting other
than to forcefully shut the bot down by pressing Ctrl-C in the terminal
the bot is running in.
