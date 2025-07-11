import discord
from discord.ext import commands
import random
from . import common_pokemon_util as cpu


def add_pokemon_to_user(user_id, pokemon):
    data = cpu.load_pokemon_data()
    user_pokemon = data.get(str(user_id), [])
    # ป้องกันซ้ำแบบ shiny + id เท่านั้น
    if any(p['id'] == pokemon['id'] and p['shiny'] == pokemon['shiny']
           for p in user_pokemon):
        return False
    user_pokemon.append(pokemon)
    data[str(user_id)] = user_pokemon
    cpu.save_pokemon_data(data)
    return True


class CatchView(discord.ui.View):

    def __init__(self, bot, ctx, pokemon):
        super().__init__(timeout=30)
        self.bot = bot
        self.ctx = ctx
        self.pokemon = pokemon
        self.caught = False

    @discord.ui.button(label="จับ", style=discord.ButtonStyle.green)
    async def catch_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("นี่ไม่ใช่ปุ่มของคุณ!", ephemeral=True)
            return

        chance = cpu.catch_chance(self.pokemon["capture_rate"])
        success = random.random() < chance
        shiny_text = "✨ Shiny ✨" if self.pokemon["shiny"] else ""

        if success:
            added = add_pokemon_to_user(interaction.user.id, self.pokemon)
            if added:
                await interaction.response.edit_message(
                    content=
                    f"🎉 {interaction.user.mention} จับ {self.pokemon['name']} {shiny_text} ได้แล้ว! {self.pokemon['leg_or_myth']} 🛍️",
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
    async def no_catch_button(self,
                              interaction: discord.Interaction,
                              button: discord.ui.Button):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("นี่ไม่ใช่ปุ่มของคุณ!", ephemeral=True)
            return

        await interaction.response.edit_message(
            content=
            f"❌ {interaction.user.mention} เลือกที่จะไม่จับ {self.pokemon['name']}",
            view=None)
        self.stop()


class CatchPokemon(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="catchpokemon",
                      help="attempt to catch a random pokemon")
    async def catchpokemon(self, ctx):
        pokemon_data = await cpu.fetch_pokemon_data()
        # keys: name, id, types, sprite, stats, shiny, capture_rate, is_legendary, is_mythical, leg_or_myth
        if not pokemon_data:
            await ctx.send("ไม่พบโปเกมอนนี้!")
            return

        shiny_text = "✨ Shiny ✨ " if pokemon_data["shiny"] else ""
        
        embed = discord.Embed(
            title=f"พบโปเกมอน: {pokemon_data['name']} {shiny_text}{pokemon_data['leg_or_myth']}",
            description=f"ประเภท: {pokemon_data['types']}",
            color=discord.Color.random())
        embed.set_thumbnail(url=pokemon_data['sprite'])

        view = CatchView(self.bot, ctx, pokemon_data)
        await ctx.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(CatchPokemon(bot))
