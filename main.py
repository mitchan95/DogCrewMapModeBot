import random
import discord
import copy

client = discord.Client()

OBJS = {
    "Capture the Flag": ["Aquarius", "Bazaar"],
    "Oddball": ["Live Fire", "Recharge", "Streets"],
    "Strongholds": ["Live Fire", "Recharge", "Streets"],
    "KOTH": ["Live Fire", "Recharge", "Streets"]
}
SLAYER = ["Aquarius", "Live Fire", "Recharge", "Streets"]


def series(length):
    gts = list(OBJS)
    slayer_maps = copy.deepcopy(SLAYER)
    temp_objs = copy.deepcopy(OBJS)
    picked_gt = []
    picked_maps = []
    games = []

    for i in range(length):
        if i == 1 or i == 4:
            picked_maps.append(
                random.choice(list(set(slayer_maps) - {picked_maps[-1]})))
            slayer_maps.remove(picked_maps[-1])
            games.append("Slayer - " + picked_maps[-1])
        elif i == 5:
            picked_gt.append(random.choice(list(set(gts) - {'Capture the Flag'})))
            picked_maps.append(random.choice(list(set(temp_objs[picked_gt[-1]]) - {picked_maps[-1]})))
            games.append(picked_gt[-1] + " - " + picked_maps[-1])
        elif i == 6:
            picked_maps.append(random.choice(list(set(slayer_maps) - {picked_maps[-1]})))
            games.append("Slayer - " + picked_maps[-1])
        else:
            picked_gt.append(random.choice(list(set(gts) - set(picked_gt))))
            picked_maps.append(
                random.choice(
                    temp_objs[picked_gt[-1]]))
            temp_objs[picked_gt[-1]].remove(picked_maps[-1])
            games.append(picked_gt[-1] + " - " + picked_maps[-1])

    return games


def create_embed(matches, length):
    embed = discord.Embed(title="BO" + str(length) + " Series", description="Maps to be played in best of " + str(length) + " series")
    embed.set_thumbnail(
        url="https://i1.wp.com/www.thexboxhub.com/wp-content/uploads/2022/02/halo-infinite-header.jpg?fit=1083%2C609&ssl=1")

    for i in range(len(matches)):
        embed.add_field(name="Game " + str(i+1), value=matches[i], inline=False)

    return embed


def coinflip():
    return random.choice(["Heads", "Tails"])


def rand_number():
    return random.randint(1, 10)

'''
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

client.run('OTQxNTk1NzQxOTA5MDUzNTAw.YgYPXg.ipMivbRmXk1hm4SXfjHp3FDC5d8')'''

print(series(5))
print(series(5))
print(series(5))
print(series(5))
print(series(5))
print(series(5))
