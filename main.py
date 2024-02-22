import random
import discord
import copy
import json
from datetime import datetime
import threading
import os
from dotenv import load_dotenv
import logging
from logging_setup import setup_logging

setup_logging()
logging.info("Logging has been set up")

load_dotenv()
token = os.environ.get("DISCORD_BOT_TOKEN")

# Initialize the intents
intents = discord.Intents.default()

# Enable guild messages to listen to messages in servers
intents.guild_messages = True

client = discord.Client(intents=intents)
OBJS = {
    "Capture the Flag": ["Aquarius", "Argyle", "Empyrean", "Forbidden"],
    "Oddball": ["Live Fire", "Recharge", "Streets"],
    "Strongholds": ["Live Fire", "Recharge", "Solitude"],
    "King of the Hill": ["Live Fire", "Recharge", "Solitude"],
}
SLAYER = ["Aquarius", "Live Fire", "Recharge", "Streets", "Solitude"]

def pick_map(available_maps, picked_maps, last_n=2):
    """
    Pick a map ensuring it wasn't picked in the last_n matches
    """
    valid_maps = list(set(available_maps) - set(picked_maps[-last_n:]))
    if valid_maps:
        return random.choice(valid_maps)
    return None

def series(length, OBJS, SLAYER):
    gts = list(OBJS)
    slayer_maps = copy.deepcopy(SLAYER)
    temp_objs = copy.deepcopy(OBJS)
    picked_gt = []
    picked_maps = []
    games = []

    for i in range(length):
        if i in [1, 4, 6]:
            cur_map = pick_map(slayer_maps, picked_maps, 2)
            if cur_map:
                picked_maps.append(cur_map)
                slayer_maps.remove(cur_map)
                games.append(f"Slayer - {cur_map}")
        elif i == 5:
            gt = random.choice(list(set(gts) - {'Capture the Flag'}))
            picked_gt.append(gt)
            cur_map = pick_map(temp_objs[gt], picked_maps, 1)
            if cur_map:
                picked_maps.append(cur_map)
                games.append(f"{gt} - {cur_map}")
        else:
            gt = random.choice(list(set(gts) - set(picked_gt)))
            picked_gt.append(gt)
            cur_map = pick_map(temp_objs[gt], picked_maps, 2)
            if cur_map:
                picked_maps.append(cur_map)
                temp_objs[gt].remove(cur_map)
                games.append(f"{gt} - {cur_map}")

    return games

def create_embed(matches, length):
    embed = discord.Embed(title="BO" + str(length) + " Series",
                          description="Maps to be played in best of " + str(length) + " series")
    embed.set_thumbnail(
        url="https://i1.wp.com/www.thexboxhub.com/wp-content/uploads/2022/02/halo-infinite-header.jpg?fit=1083%2C609&ssl=1")

    for i in range(len(matches)):
        embed.add_field(name="Game " + str(i + 1), value=matches[i], inline=False)

    return embed

def coinflip():
    percent = random.randint(0, 100);
    if percent < 50:
        return "Heads"
    elif percent > 50:
        return "Tails"
    else:
        return "You're both losers!"

def rand_number():
    return random.randint(1, 10)

@client.event
async def on_ready():
    logging.info(f"We have logged in as {client.user}")


COMMAND_LOG_COUNT = {'BO3': 0, 'BO5': 0, 'BO7': 0, 'Coinflip': 0, 'Number': 0}

def handle_bo_command(length, message):
    matches = series(length, OBJS, SLAYER)
    embed = create_embed(matches, length)
    COMMAND_LOG_COUNT[f'BO{length}'] += 1
    return embed

COMMANDS = {
    '!bo3': lambda m: handle_bo_command(3, m),
    '!bo5': lambda m: handle_bo_command(5, m),
    '!bo7': lambda m: handle_bo_command(7, m),
    '!coinflip': lambda m: coinflip(),
    '!number': lambda m: rand_number(),
    '!botservers': lambda m: f"I'm in {len(client.guilds)} servers!"
}

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    cmd_func = COMMANDS.get(message.content.casefold())
    if cmd_func:
        response = cmd_func(message)
        if isinstance(response, discord.Embed):
            await message.channel.send(embed=response)
        else:
            await message.channel.send(response)

def checkTime():
    # This function runs periodically every hour
    threading.Timer(3600, checkTime).start()

    # Log current time with format "Mon Month Day HH:MM:SS", e.g., "Thu Oct 14 15:30:45"
    logging.info(f"Current Time = {datetime.now().strftime('%a %b %d %H:%M:%S')}")
    logging.info(f"Command Log Count: {json.dumps(COMMAND_LOG_COUNT)}")


checkTime()

client.run(token)
