import random
import discord
import copy

client = discord.Client()

OBJS = {
    "Capture the Flag": ["Aquarius", "Bazaar", "Catalyst"],
    "Oddball": ["Live Fire", "Recharge", "Streets"],
    "Strongholds": ["Live Fire", "Recharge", "Streets"],
    "KOTH": ["Live Fire", "Recharge", "Streets"]
}
SLAYER = ["Aquarius", "Catalyst", "Live Fire", "Recharge", "Streets"]


def series(length):
    gts = list(OBJS)
    slayer_maps = copy.deepcopy(SLAYER)
    temp_objs = copy.deepcopy(OBJS)
    picked_gt = []
    picked_maps = []
    games = []
    cur_map = None

    for i in range(length):
        if i == 1 or i == 4 or i == 6:
            while True:  # Pick a random slayer map, but make sure the map hasn't been played in the last 2 matches
                cur_map = random.choice(list(set(slayer_maps) - {picked_maps[-1]}))
                if picked_maps.count(cur_map) < 2 and cur_map != picked_maps[-1] and (cur_map != picked_maps[-2] if (i == 4 or i == 6) else True):
                    picked_maps.append(cur_map)
                    break

            slayer_maps.remove(picked_maps[-1])
            games.append("Slayer - " + picked_maps[-1])
        elif i == 5:
            picked_gt.append(random.choice(list(set(gts) - {'Capture the Flag'})))
            while True:
                cur_map = random.choice(list(set(temp_objs[picked_gt[-1]]) - {picked_maps[-1]}))
                if picked_maps.count(cur_map) < 2 and cur_map != picked_maps[-1]:
                    picked_maps.append(cur_map)
                    break

            games.append(picked_gt[-1] + " - " + picked_maps[-1])
        elif i == 6:
            while True:
                cur_map = random.choice(list(set(slayer_maps) - {picked_maps[-1]}))
                if picked_maps.count(cur_map) < 2 and cur_map != picked_maps[-1]:
                    picked_maps.append(cur_map)
                    break

            games.append("Slayer - " + picked_maps[-1])
        else:
            picked_gt.append(random.choice(list(set(gts) - set(picked_gt))))
            while True:
                cur_map = random.choice(temp_objs[picked_gt[-1]])
                if len(picked_maps) == 0:
                    break
                elif picked_maps.count(cur_map) < 2 and cur_map != picked_maps[-1] and cur_map != picked_maps[-2]:
                    break

            picked_maps.append(cur_map)
            temp_objs[picked_gt[-1]].remove(picked_maps[-1])
            games.append(picked_gt[-1] + " - " + picked_maps[-1])

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
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.casefold() == "!bo3":
        matches = series(3)
        embed = create_embed(matches, 3)
        await message.channel.send(embed=embed)
    elif message.content.casefold() == "!bo5":
        matches = series(5)
        embed = create_embed(matches, 5)
        await message.channel.send(embed=embed)
    elif message.content.casefold() == "!bo7":
        matches = series(7)
        embed = create_embed(matches, 7)
        await message.channel.send(embed=embed)
    elif message.content.casefold() == "!coinflip":
        await message.channel.send(coinflip())
    elif message.content.casefold() == "!number":
        await message.channel.send(rand_number())
    elif message.content.casefold() == "!botservers":
        await message.channel.send("I'm in " + str(len(client.guilds)) + " servers!")


with open("token.txt") as f:
    token = f.readline().rstrip()

client.run(token)
