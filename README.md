# Discord Reposter

A simple Discord bot for reposting the contents of a chat downloaded using
DiscordChatExporter. This requires Python version 3.10 or greater.

## Usage

Create a text file named `token.txt` and paste your Discord bot token inside.
Create another text file named `allowlist.txt` and the Discord IDs of everyone
you want to allow to use the bot inside, one ID on each line. Next, use the
`requirements.txt` to download the third-party libraries used by the bot like
so:

```
$ python3 -m pip install -r requirements.txt
```

Having done all of that, you can now bring the bot online by running `main.py`
in the root of the repository.
