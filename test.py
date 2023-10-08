import random
import copy

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


OBJS = {
    "Capture the Flag": ["Aquarius", "Argyle", "Empyrean"],
    "Oddball": ["Live Fire", "Recharge", "Streets"],
    "Strongholds": ["Live Fire", "Recharge", "Solitude"],
    "King of the Hill": ["Live Fire", "Recharge", "Solitude"]
}
SLAYER = ["Aquarius", "Live Fire", "Recharge", "Streets", "Solitude"]


print(series(5, OBJS, SLAYER))
print(series(5, OBJS, SLAYER))
print(series(5, OBJS, SLAYER))
print(series(5, OBJS, SLAYER))
print(series(5, OBJS, SLAYER))
print(series(5, OBJS, SLAYER))

print(series(3, OBJS, SLAYER))
print(series(3, OBJS, SLAYER))
print(series(3, OBJS, SLAYER))
print(series(3, OBJS, SLAYER))
print(series(3, OBJS, SLAYER))

print(series(7, OBJS, SLAYER))
print(series(7, OBJS, SLAYER))
print(series(7, OBJS, SLAYER))
print(series(7, OBJS, SLAYER))
print(series(7, OBJS, SLAYER))
