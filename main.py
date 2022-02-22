import random
import discord
import copy

client = discord.Client()

OBJS = {
    "Capture the Flag": ["Aquarius", "Bazaar"],
    "Oddball": ["Live Fire", "Recharge", "Streets"],
    "Strongholds": ["Live Fire", "Recharge", "Streets"]
}
SLAYER = ["Aquarius", "Bazaar", "Live Fire", "Recharge", "Streets"]


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
                random.choice(list(set(slayer_maps) - set(picked_maps))))
            slayer_maps.remove(picked_maps[-1])
            games.append("Slayer - " + picked_maps[-1])
        elif i == 5:
            picked_gt.append(random.choice(list(set(gts) - set(['Capture the Flag']))))
            picked_maps.append(random.choice(list(set(temp_objs[picked_gt[-1]]) - set([picked_maps[-1]]))))
            games.append(picked_gt[-1] + " - " + picked_maps[-1])
        elif i == 6:
            picked_maps.append(random.choice(list(set(slayer_maps) - set([picked_maps[-1]]))))
            games.append("Slayer - " + picked_maps[-1])
        else:
            picked_gt.append(random.choice(list(set(gts) - set(picked_gt))))
            picked_maps.append(
                random.choice(
                    list(set(temp_objs[picked_gt[-1]]) - set(picked_maps))))
            temp_objs[picked_gt[-1]].remove(picked_maps[-1])
            games.append(picked_gt[-1] + " - " + picked_maps[-1])

    return games


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == "!bo3":
        matches = series(3)
        embed = discord.Embed(title="BO3 Series", description="Maps to be played in best of 3 series")
        embed.add_field(name="Game 1", value=matches[0], inline=False)
        embed.add_field(name="Game 2", value=matches[1], inline=False)
        embed.add_field(name="Game 3", value=matches[2], inline=False)
        embed.set_thumbnail(url="https://i1.wp.com/www.thexboxhub.com/wp-content/uploads/2022/02/halo-infinite-header.jpg?fit=1083%2C609&ssl=1")
        await message.channel.send(embed=embed)
    elif message.content == "!bo5":
        matches = series(5)
        embed = discord.Embed(title="BO5 Series", description="Maps to be played in best of 5 series")
        embed.set_thumbnail(url="https://i1.wp.com/www.thexboxhub.com/wp-content/uploads/2022/02/halo-infinite-header.jpg?fit=1083%2C609&ssl=1")
        embed.add_field(name="Game 1", value=matches[0], inline=False)
        embed.add_field(name="Game 2", value=matches[1], inline=False)
        embed.add_field(name="Game 3", value=matches[2], inline=False)
        embed.add_field(name="Game 4", value=matches[3], inline=False)
        embed.add_field(name="Game 5", value=matches[4], inline=False)
        await message.channel.send(embed=embed)


client.run('OTQxNTk1NzQxOTA5MDUzNTAw.YgYPXg.ipMivbRmXk1hm4SXfjHp3FDC5d8')