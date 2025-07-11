import discord
from discord.ext import commands, tasks
# import aiohttp
import random
import os
from . import common_pokemon_util as cpu

from .catch_pokemon import add_pokemon_to_user  # เรียกใช้ util จากไฟล์ catch_pokemon

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
                f"🎉 {interaction.user.mention} จับ {self.pokemon['name']} {shiny_text} ได้ก่อนใคร! {self.pokemon['leg_or_myth']} 🏆",
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

    async def spawn_pokemon_event(self):
        channel_id = CHANNEL_ID
        channel = self.bot.get_channel(channel_id)
        if not channel:
            print("Channel not found")
            return
        pokemon_data = await cpu.fetch_pokemon_data()
        if not pokemon_data:
            return

        shiny_text = "✨ Shiny ✨" if pokemon_data["shiny"] else ""

        embed = discord.Embed(
            title="โปเกมอนป่าโผล่ออกมาแล้ว!",
            description=
            f"ใครจะจับได้ก่อน!?\n{pokemon_data['name']} {shiny_text} {pokemon_data['leg_or_myth']}\nประเภท: {pokemon_data['types']}",
            color=discord.Color.random())
        embed.set_thumbnail(url=pokemon_data['sprite'])
        async def dummy_callback():
            pass

        view = EventCatchView(self.bot, pokemon_data, dummy_callback)
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
