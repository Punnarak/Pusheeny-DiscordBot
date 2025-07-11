import os
import json
import aiohttp
import random

POKEMON_STORAGE = "pokemon/pokemon_storage.json"
CHANNEL_ID = int(os.environ['CHANNEL_ID'])


def load_pokemon_data():
    if os.path.exists(POKEMON_STORAGE):
        with open(POKEMON_STORAGE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_pokemon_data(data):
    with open(POKEMON_STORAGE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_pokemon_to_user(user_id, pokemon):
    data = load_pokemon_data()
    user_pokemon = data.get(str(user_id), [])
    # ป้องกันซ้ำแบบ shiny + id เท่านั้น
    if any(p['id'] == pokemon['id'] and p['shiny'] == pokemon['shiny']
           for p in user_pokemon):
        return False
    user_pokemon.append(pokemon)
    data[str(user_id)] = user_pokemon
    save_pokemon_data(data)
    return True

def is_shiny():
    return random.randint(1, 4096) == 1

def catch_chance(cap_rate): # กำหนดโอกาสจับได้ตาม cap_rate
    chances = ((cap_rate - 255) / 255) + 1
    return chances

def get_rarity_emoji(legendary, mythical):
    emojis = {
        "ธรรมดา (Common)": "⚪",
        "Uncommon": "🟢",
        "หายาก (Rare)": "🔵",
        "Epic": "🟣",
        "ตำนาน (Legendary)": "🟡",
        "Mythical": "🌟",
        "Ultra Beast": "🔥",
        "other": "❓"
    }
    temp = ""
    if legendary or mythical:
        if legendary:
            temp += emojis["ตำนาน (Legendary)"]
        if mythical:
            temp += emojis["Mythical"]
    else:
        temp = emojis["ธรรมดา (Common)"]
    return temp

async def fetch_pokemon_data_with_api(identifier, url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                return None
            

async def fetch_pokemon_data():
    pokemon_id = random.randint(1, 1025)    #random pokemon id
    # fetch pokemon data part1
    url = f"https://pokeapi.co/api/v2/pokemon/{str(pokemon_id)}"
    data = await fetch_pokemon_data_with_api(str(pokemon_id), url)
    if not data:
        return None

    shiny = is_shiny()
    sprite = data['sprites']['front_shiny'] if shiny else data['sprites']['front_default']
    stats = {
      stat['stat']['name']: stat['base_stat']
      for stat in data['stats']
    }
    pokemon = {
        "name": data["name"].capitalize(),
        "id": data["id"],
        "types": ", ".join(t["type"]["name"] for t in data["types"]),
        "sprite": sprite,
        "shiny": shiny,
        "stats": stats
    }
    # fetch pokemon data part2
    url2 = f"https://pokeapi.co/api/v2/pokemon-species/{str(pokemon_id)}"
    data2 = await fetch_pokemon_data_with_api(str(pokemon_id), url2)
    if not data2:
        return None
    cap_rate = data2["capture_rate"]
    pokemon["capture_rate"] = cap_rate
    pokemon["is_legendary"] = data2["is_legendary"]
    pokemon["is_mythical"] = data2["is_mythical"]
    # check legendary or mythical
    if data2["is_legendary"]:
        leg = "โปเกม่อนในตำนาน"
    else:
        leg = ""
    if data2["is_mythical"]:
        myth = "โปเกม่อนเทพนิยาย"
    else:
        myth = ""
    if data2["is_legendary"] or data2["is_mythical"]:
        leg_or_myth = f"[{leg}{myth}]"
    else:
        leg_or_myth = ""
    pokemon["leg_or_myth"] = leg_or_myth

    return pokemon    # keys: name, id, types, sprite, shiny, stats, capture_rate, is_legendary, is_mythical, leg_or_myth