import discord
import json
import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))
BLACKLIST_FILE = "blacklist.json"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def add_to_blacklist(date_str):
    try:
        with open(BLACKLIST_FILE, "r") as f:
            blacklist = json.load(f)
    except FileNotFoundError:
        blacklist = []

    if date_str not in blacklist:
        blacklist.append(date_str)
        with open(BLACKLIST_FILE, "w") as f:
            json.dump(blacklist, f, indent=2)
        return True
    return False

@client.event
async def on_ready():
    print(f"🤖 Bot is connected as {client.user}")

@client.event
async def on_message(message):
    print(f"📩 Message received: {message.content} in channel {message.channel.id}")

    if message.channel.id != CHANNEL_ID:
        print("⛔ Wrong channel, ignoring.")
        return

    # REJECT
    if message.content.startswith("!reject "):
        date_str = message.content.split(" ", 1)[1].strip()
        if add_to_blacklist(date_str):
            await message.channel.send(f"🛑 Got it. `{date_str}` will be ignored from now on.")
        else:
            await message.channel.send(f"⚠️ `{date_str}` is already blacklisted.")

    # BLACKLIST QUERY
    elif message.content.strip() == "!blacklist":
        try:
            with open(BLACKLIST_FILE, "r") as f:
                blacklist = json.load(f)
        except FileNotFoundError:
            blacklist = []

        if blacklist:
            dates = "\n".join(f"- `{d}`" for d in sorted(blacklist))
            await message.channel.send(f"📋 Currently blacklisted dates: (to restore one use `!unrecejt YYYY-MM-DD`) \n{dates}")
        else:
            await message.channel.send("✅ No dates are currently blacklisted.")
          
          # UNREJECT
    elif message.content.startswith("!unreject "):
        date_str = message.content.split(" ", 1)[1].strip()
        try:
            with open(BLACKLIST_FILE, "r") as f:
                blacklist = json.load(f)
        except FileNotFoundError:
            blacklist = []

        if date_str in blacklist:
            blacklist.remove(date_str)
            with open(BLACKLIST_FILE, "w") as f:
                json.dump(blacklist, f, indent=2)
            await message.channel.send(f"✅ `{date_str}` has been removed from the blacklist.")
        else:
            await message.channel.send(f"⚠️ `{date_str}` was not in the blacklist.")

client.run(TOKEN)
