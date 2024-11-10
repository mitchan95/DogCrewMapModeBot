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
arena_OBJS = {
    "Capture the Flag": ["Aquarius", "Empyrean", "Forbidden", "Fortress", "Inquisitor"],
    "Oddball": ["Live Fire", "Recharge", "Streets"],
    "Strongholds": ["Live Fire", "Recharge"],
    "King of the Hill": ["Live Fire", "Recharge", "Solitude"],
}
arena_SLAYER = ["Aquarius", "Live Fire", "Recharge", "Streets", "Solitude", "Fortress", "Inquisitor"]

# HCS Mode Objectives and Slayer maps
hcs_OBJS = {
    "Capture the Flag": ["Aquarius", "Empyrean", "Forbidden"],
    "Oddball": ["Live Fire", "Recharge", "Streets"],
    "Strongholds": ["Live Fire", "Recharge"],
    "King of the Hill": ["Live Fire", "Recharge", "Solitude"],
}
hcs_SLAYER = ["Aquarius", "Live Fire", "Recharge", "Streets", "Solitude"]

# Legacy Mode Objectives and Slayer maps
legacy_OBJS = {
    "Capture the Flag": ["Aquarius", "Argyle", "Empyrean", "Forbidden", "Fortress", "Inquisitor", "Catalyst", "Starboard"],
    "Oddball": ["Live Fire", "Recharge", "Streets"],
    "Strongholds": ["Live Fire", "Recharge", "Interference", "Solitude"],
    "King of the Hill": ["Live Fire", "Recharge", "Solitude", "Interference"],
}
legacy_SLAYER = ["Aquarius", "Live Fire", "Recharge", "Streets", "Solitude", "Fortress", "Inquisitor", "Interference", "Starboard"]

def pick_map(available_maps, picked_maps, last_n=2):
    valid_maps = list(set(available_maps) - set(picked_maps[-last_n:]))
    if valid_maps:
        return random.choice(valid_maps)
    return None

def series(length, mode="Arena"):
    if mode == "Arena":
        gts = list(arena_OBJS)
        slayer_maps = copy.deepcopy(arena_SLAYER)
        temp_objs = copy.deepcopy(arena_OBJS)
    elif mode == "HCS":
        gts = list(hcs_OBJS)
        slayer_maps = copy.deepcopy(hcs_SLAYER)
        temp_objs = copy.deepcopy(hcs_OBJS)
    elif mode == "Legacy":
        gts = list(legacy_OBJS)
        slayer_maps = copy.deepcopy(legacy_SLAYER)
        temp_objs = copy.deepcopy(legacy_OBJS)
    else:
        raise ValueError("Invalid mode. Choose 'Arena', 'HCS', or 'Legacy'.")

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

def create_embed(matches, length, mode):
    embed = discord.Embed(
        title=f"{mode} Bo{length} Series",
        description=f"{mode} maps - best of {length}"
    )
    embed.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRQBygbA4-Ry2hYeY4S4cYU1iljNRD7e2_1WQ&s")
    for i, match in enumerate(matches):
        embed.add_field(name=f"Game {i + 1}", value=match, inline=False)
    return embed

def coinflip():
    return "Heads" if random.randint(0, 100) < 50 else "Tails"

def rand_number():
    return random.randint(1, 10)

COMMAND_LOG_COUNT = {
    'bo3_arena': 0, 'bo5_arena': 0, 'bo7_arena': 0,
    'bo3_hcs': 0, 'bo5_hcs': 0, 'bo7_hcs': 0,
    'bo3_legacy': 0, 'bo5_legacy': 0, 'bo7_legacy': 0,
    'Coinflip': 0, 'Number': 0
}

class MatchCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="bo3_arena", description="Starts a Bo3 series for Arena")
    async def bo3_arena(self, interaction):
        matches = series(3, mode="Arena")
        await interaction.response.send_message(embed=create_embed(matches, 3, "Arena"))
        COMMAND_LOG_COUNT['bo3_arena'] += 1

    @discord.app_commands.command(name="bo5_hcs", description="Starts a Bo5 series for HCS")
    async def bo5_hcs(self, interaction):
        matches = series(5, mode="HCS")
        await interaction.response.send_message(embed=create_embed(matches, 5, "HCS"))
        COMMAND_LOG_COUNT['bo5_hcs'] += 1

    @discord.app_commands.command(name="bo7_legacy", description="Starts a Bo7 series for Legacy")
    async def bo7_legacy(self, interaction):
        matches = series(7, mode="Legacy")
        await interaction.response.send_message(embed=create_embed(matches, 7, "Legacy"))
        COMMAND_LOG_COUNT['bo7_legacy'] += 1

    @discord.app_commands.command(name="coinflip", description="Flips a coin")
    async def coinflip(self, interaction):
        await interaction.response.send_message(coinflip())

    @discord.app_commands.command(name="number", description="Generates a random number")
    async def number(self, interaction):
        await interaction.response.send_message(rand_number())

async def setup(bot):
    await bot.add_cog(MatchCommands(bot))
    await bot.tree.sync()

@bot.event
async def on_ready():
    await setup(bot)
    logging.info(f"Logged in as {bot.user}")

bot.run(token)
