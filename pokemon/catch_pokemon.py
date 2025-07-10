import discord
from discord.ext import commands
import aiohttp
import random
import json
import os

POKEMON_STORAGE = "pokemon/pokemon_storage.json"


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


def get_rarity(pokemon_id):
    if pokemon_id > 800:
        return "ตำนาน (Legendary)"
    elif pokemon_id > 500:
        return "หายาก (Rare)"
    else:
        return "ธรรมดา (Common)"


def is_shiny():
    return random.randint(1, 4096) == 1


# กำหนดโอกาสจับได้ตาม rarity
def catch_chance(rarity):
    chances = {
        "ธรรมดา (Common)": 0.8,
        "หายาก (Rare)": 0.5,
        "ตำนาน (Legendary)": 0.2
    }
    return chances.get(rarity, 0.5)  # default 50%


class CatchView(discord.ui.View):

    def __init__(self, bot, ctx, pokemon):
        super().__init__(timeout=30)
        self.bot = bot
        self.ctx = ctx
        self.pokemon = pokemon
        self.caught = False

    @discord.ui.button(label="จับ", style=discord.ButtonStyle.green)
    async def catch_button(self, interaction: discord.Interaction,
                           button: discord.ui.Button):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("นี่ไม่ใช่ปุ่มของคุณ!",
                                                    ephemeral=True)
            return

        chance = catch_chance(self.pokemon["rarity"])
        success = random.random() < chance
        shiny_text = "✨ Shiny ✨" if self.pokemon["shiny"] else ""

        if success:
            added = add_pokemon_to_user(interaction.user.id, self.pokemon)
            if added:
                await interaction.response.edit_message(
                    content=
                    f"🎉 {interaction.user.mention} จับ {self.pokemon['name']} {shiny_text} ได้แล้ว! [{self.pokemon['rarity']}] 🛍️",
                    view=None)
            else:
                await interaction.response.edit_message(
                    content=
                    f"⚠️ {interaction.user.mention} มี {self.pokemon['name']} {shiny_text} ตัวนี้ในกระเป๋าแล้ว!",
                    view=None)
        else:
            await interaction.response.edit_message(
                content=
                f"😢 {interaction.user.mention} พยายามจับ {self.pokemon['name']} แต่โปเกมอนหนีไปแล้ว!",
                view=None)

        self.stop()

    @discord.ui.button(label="ไม่จับ", style=discord.ButtonStyle.red)
    async def no_catch_button(self, interaction: discord.Interaction,
                              button: discord.ui.Button):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("นี่ไม่ใช่ปุ่มของคุณ!",
                                                    ephemeral=True)
            return

        await interaction.response.edit_message(
            content=
            f"❌ {interaction.user.mention} เลือกที่จะไม่จับ {self.pokemon['name']}",
            view=None)
        self.stop()

class CatchPokemon(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def fetch_pokemon(self, identifier):
        url = f"https://pokeapi.co/api/v2/pokemon/{identifier.lower()}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    return None

    @commands.command(name="catchpokemon", help="attempt to catch a random pokemon")
    async def catchpokemon(self, ctx):
        pokemon_id = random.randint(1, 1025)
        data = await self.fetch_pokemon(str(pokemon_id))
        if not data:
            await ctx.send("ไม่พบโปเกมอนนี้!")
            return

        shiny = is_shiny()
        rarity = get_rarity(pokemon_id)
        sprite = data["sprites"]["front_shiny"] if shiny else data["sprites"][
            "front_default"]

        pokemon = {
            "name": data["name"].capitalize(),
            "id": data["id"],
            "types": ", ".join(t["type"]["name"] for t in data["types"]),
            "sprite": sprite,
            "rarity": rarity,
            "shiny": shiny
        }

        shiny_text = "✨ Shiny ✨" if shiny else ""
        embed = discord.Embed(
            title=f"พบโปเกมอน: {pokemon['name']} {shiny_text} [{rarity}]",
            description=f"ประเภท: {pokemon['types']}",
            color=discord.Color.random())
        embed.set_thumbnail(url=sprite)

        view = CatchView(self.bot, ctx, pokemon)
        await ctx.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(CatchPokemon(bot))
