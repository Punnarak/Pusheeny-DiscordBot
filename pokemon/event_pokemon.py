import discord
from discord.ext import commands, tasks
import aiohttp
import random
import os

from .catch_pokemon import add_pokemon_to_user, is_shiny  # เรียกใช้ util จากไฟล์ catch_pokemon

CHANNEL_ID = int(os.environ['CHANNEL_ID'])


class EventCatchView(discord.ui.View):

    def __init__(self, bot, pokemon, on_catch_callback):
        super().__init__(timeout=60)
        self.bot = bot
        self.pokemon = pokemon
        self.caught = False
        self.on_catch_callback = on_catch_callback

    @discord.ui.button(label="จับก่อนใคร!", style=discord.ButtonStyle.green)
    async def catch_first(self, interaction: discord.Interaction,
                          button: discord.ui.Button):
        if self.caught:
            await interaction.response.send_message("⛔ มีคนจับโปเกมอนไปแล้ว!",
                                                    ephemeral=True)
            return

        added = add_pokemon_to_user(interaction.user.id, self.pokemon)
        shiny_text = "✨ Shiny ✨" if self.pokemon['shiny'] else ""

        if added:
            self.caught = True
            
            await interaction.response.edit_message(
                content=
                f"🎉 {interaction.user.mention} จับ {self.pokemon['name']} {shiny_text} ได้ก่อนใคร! {self.pokemon['is_legendary']}{self.pokemon['is_mythical']} 🏆",
                view=None)
            await self.on_catch_callback()
        else:
            await interaction.response.send_message(
                "📦 คุณมีโปเกมอนตัวนี้แล้ว!", ephemeral=True)

        self.stop()


class EventPokemon(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.spawn_loop.start()

    async def fetch_pokemon(self, identifier, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    return None

    async def spawn_pokemon_event(self):
        channel_id = CHANNEL_ID
        channel = self.bot.get_channel(channel_id)
        if not channel:
            print("Channel not found")
            return
        pokemon_id = random.randint(1, 1025)
        url = f"https://pokeapi.co/api/v2/pokemon/{str(pokemon_id)}"
        data = await self.fetch_pokemon(str(pokemon_id), url)
        if not data:
            return

        shiny = is_shiny()
        sprite = data['sprites']['front_shiny'] if shiny else data['sprites'][
            'front_default']

        pokemon = {
            "name": data["name"].capitalize(),
            "id": data["id"],
            "types": ", ".join(t["type"]["name"] for t in data["types"]),
            "sprite": sprite,
            "shiny": shiny
        }
        url2 = f"https://pokeapi.co/api/v2/pokemon-species/{str(pokemon_id)}"
        data2 = await self.fetch_pokemon(str(pokemon_id), url2)
        if not data2:
            return
        cap_rate = data2["capture_rate"]
        pokemon["capture_rate"] = cap_rate
        if data2["is_legendary"]:
            pokemon["is_legendary"] = "โปเกม่อนในตำนาน"
        else:
            pokemon["is_legendary"] = ""
        if data2["is_mythical"]:
            pokemon["is_mythical"] = "โปเกม่อนเทพนิยาย"
        else:
            pokemon["is_mythical"] = ""
        if data2["is_legendary"] or data2["is_mythical"]:
            leg = pokemon["is_legendary"]
            myth = pokemon["is_mythical"]
            leg_or_myth = f"[{leg}{myth}]"
        else:
            leg_or_myth = ""

        shiny_text = "✨ Shiny ✨" if shiny else ""

        embed = discord.Embed(
            title="โปเกมอนป่าโผล่ออกมาแล้ว!",
            description=
            f"ใครจะจับได้ก่อน!?\n{pokemon['name']} {shiny_text} {shiny_text}{leg_or_myth}\nประเภท: {pokemon['types']}",
            color=discord.Color.random())
        embed.set_thumbnail(url=sprite)
        async def dummy_callback():
            pass

        view = EventCatchView(self.bot, pokemon, dummy_callback)
        await channel.send(embed=embed, view=view)

    @tasks.loop(minutes=1)
    async def spawn_loop(self):
        # สุ่ม 50% ว่าจะปล่อยหรือไม่ในรอบนั้น
        rand = random.random()
        # print(f"Random value: {rand}")
        if rand < 0.5:
            await self.spawn_pokemon_event()

    @spawn_loop.before_loop
    async def before_loop(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(EventPokemon(bot))
