import discord
from discord.ext import commands
import random
import copy
import os
from dotenv import load_dotenv
import logging
from logging_setup import setup_logging
import json
from datetime import datetime
import threading

setup_logging()

# Load environment variables
load_dotenv()
token = os.environ.get("DISCORD_BOT_TOKEN")

# Initialize the bot with intents
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Arena Mode Objectives and Slayer maps
ARENA_OBJS = {
    "Capture the Flag": ["Aquarius", "Argyle", "Empyrean", "Forbidden", "Fortress", "Inquisitor"],
    "Oddball": ["Live Fire", "Recharge", "Streets"],
    "Strongholds": ["Live Fire", "Recharge", "Solitude","Interference"],
    "King of the Hill": ["Live Fire", "Recharge", "Solitude", "Interference"],
}
ARENA_SLAYER = ["Aquarius", "Live Fire", "Recharge", "Streets", "Solitude", "Interference","Fortress","Inquisitor"]

# HCS Mode Objectives and Slayer maps

HCS_OBJS = {
    "Capture the Flag": ["Aquarius", "Argyle", "Empyrean", "Forbidden",],
    "Oddball": ["Live Fire", "Recharge", "Streets"],
    "Strongholds": ["Live Fire", "Recharge", "Solitude","Interference"],
    "King of the Hill": ["Live Fire", "Recharge", "Solitude"],
}
HCS_SLAYER = ["Aquarius", "Live Fire", "Recharge", "Streets", "Solitude"]

def pick_map(available_maps, picked_maps, last_n=2):
    """
    Pick a map ensuring it wasn't picked in the last_n matches
    """
    valid_maps = list(set(available_maps) - set(picked_maps[-last_n:]))
    if valid_maps:
        return random.choice(valid_maps)
    return None

def series(length, mode="Arena"):
    if mode == "Arena":
        gts = list(ARENA_OBJS)
        slayer_maps = copy.deepcopy(ARENA_SLAYER)
        temp_objs = copy.deepcopy(ARENA_OBJS)
    elif mode == "HCS":
        gts = list(HCS_OBJS)
        slayer_maps = copy.deepcopy(HCS_SLAYER)
        temp_objs = copy.deepcopy(HCS_OBJS)
    else:
        raise ValueError("Invalid mode. Choose 'Arena' or 'HCS'.")

    picked_gt = []
    picked_maps = []
    games = []

    for i in range(length):
        if i in [1, 4, 6]:  # Slayer rounds for certain matches
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

COMMAND_LOG_COUNT = {'bo3_arena': 0, 'bo5_arena': 0, 'bo7_arena': 0, 'bo3_hcs': 0, 'bo5_hcs': 0, 'bo7_hcs': 0, 'Coinflip': 0, 'Number': 0}

def handle_bo_command(length, message):
    matches = series(length, OBJS, SLAYER)
    embed = create_embed(matches, length)
    COMMAND_LOG_COUNT[f'BO{length}'] += 1
    return embed

COMMANDS = {
    '!bo3_arena': lambda m: handle_bo_command(3, m, mode="Arena"),
    '!bo5_arena': lambda m: handle_bo_command(5, m, mode="Arena"),
    '!bo7_arena': lambda m: handle_bo_command(7, m, mode="Arena"),
    '!bo3_hcs': lambda m: handle_bo_command(3, m, mode="HCS"),
    '!bo5_hcs': lambda m: handle_bo_command(5, m, mode="HCS"),
    '!bo7_hcs': lambda m: handle_bo_command(7, m, mode="HCS"),
    '!coinflip': lambda m: coinflip(),
    '!number': lambda m: rand_number(),
    '!botservers': lambda m: f"I'm in {len(client.guilds)} servers!"
}

class MatchCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
   
    # Arena Mode Commands
    
    @discord.app_commands.command(name="bo3_arena", description="Starts a Bo3 series for Arena")
    async def bo3_arena(self, interaction: discord.Interaction):
        matches = series(3, mode="Arena")
        embed = create_embed(matches, 3)
        await interaction.response.send_message(embed=embed)
        COMMAND_LOG_COUNT['bo3_arena'] += 1

    @discord.app_commands.command(name="bo5_arena", description="Starts a Bo5 series for Arena")
    async def bo5_arena(self, interaction: discord.Interaction):
        matches = series(5, mode="Arena")
        embed = create_embed(matches, 5)
        await interaction.response.send_message(embed=embed)
        COMMAND_LOG_COUNT['bo5_arena'] += 1

    @discord.app_commands.command(name="bo7_arena", description="Starts a Bo7 series for Arena")
    async def bo7_arena(self, interaction: discord.Interaction):
        matches = series(7, mode="Arena")
        embed = create_embed(matches, 7)
        await interaction.response.send_message(embed=embed)
        COMMAND_LOG_COUNT['bo7_arena'] += 1
    
    # HCS Mode Commands
    
    @discord.app_commands.command(name="bo3_hcs", description="Starts a Bo3 series for HCS")
    async def bo3_hcs(self, interaction: discord.Interaction):
        matches = series(3, mode="HCS")
        embed = create_embed(matches, 3)
        await interaction.response.send_message(embed=embed)
        COMMAND_LOG_COUNT['bo3_hcs'] += 1

    @discord.app_commands.command(name="bo5_hcs", description="Starts a Bo5 series for HCS")
    async def bo5_hcs(self, interaction: discord.Interaction):
        matches = series(5, mode="HCS")
        embed = create_embed(matches, 5)
        await interaction.response.send_message(embed=embed)
        COMMAND_LOG_COUNT['bo5_hcs'] += 1

    @discord.app_commands.command(name="bo7_hcs", description="Starts a Bo7 series for HCS")
    async def bo7_hcs(self, interaction: discord.Interaction):
        matches = series(7, mode="HCS")
        embed = create_embed(matches, 7)
        await interaction.response.send_message(embed=embed)
        COMMAND_LOG_COUNT['bo7_hcs'] += 1

     # Other Commands
    
    @discord.app_commands.command(name="coinflip", description="Flips a coin")
    async def coinflip(self, interaction: discord.Interaction):
        result = coinflip()  # Assuming coinflip() is defined elsewhere
        await interaction.response.send_message(result)
        COMMAND_LOG_COUNT['Coinflip'] += 1

    @discord.app_commands.command(name="number", description="Generates a random number")
    async def number(self, interaction: discord.Interaction):
        number = rand_number()  # Assuming rand_number() is defined elsewhere
        await interaction.response.send_message(str(number))
        COMMAND_LOG_COUNT['Number'] += 1

    @discord.app_commands.command(name="botservers", description="Shows the number of servers the bot is in")
    async def botservers(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"I'm in {len(self.bot.guilds)} servers!")


async def setup(bot):
    await bot.add_cog(MatchCommands(bot))
    await bot.tree.sync()

@bot.event
async def on_ready():
    await setup(bot)
    logging.info(f"We have logged in as {bot.user}")

def checkTime():
    # This function runs periodically every hour
    threading.Timer(3600, checkTime).start()

    # Log current time with format "Mon Month Day HH:MM:SS", e.g., "Thu Oct 14 15:30:45"
    logging.info(f"Current Time = {datetime.now().strftime('%a %b %d %H:%M:%S')}")
    logging.info(f"Command Log Count: {json.dumps(COMMAND_LOG_COUNT)}")


checkTime()

bot.run(token)
