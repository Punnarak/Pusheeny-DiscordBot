from discord.ext import commands
import discord
from . import common_pokemon_util as cpu


class RandomPokemon(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.command(name="randpokemon", help="random pokemon")
  async def random_pokemon(self, ctx):
    pokemon = await cpu.fetch_pokemon_data()
    if pokemon:
      shiny_text = "✨ Shiny ✨" if pokemon["shiny"] else ""
      embed = discord.Embed(
          title=
          f"🎲 โปเกมอนสุ่มได้: {pokemon['name']} {shiny_text} (#{pokemon['id']})",
          description=
          f"ประเภท: {pokemon['types']} {pokemon['leg_or_myth']}",
          color=discord.Color.random())
      embed.set_thumbnail(url=pokemon['sprite'])

      # เพิ่มฟิลด์แสดง stats
      embed.add_field(name="HP",
                      value=str(pokemon["stats"].get("hp", "N/A")),
                      inline=True)
      embed.add_field(name="Attack",
                      value=str(pokemon["stats"].get("attack", "N/A")),
                      inline=True)
      embed.add_field(name="Defense",
                      value=str(pokemon["stats"].get("defense", "N/A")),
                      inline=True)
      embed.add_field(name="Sp. Atk",
                      value=str(pokemon["stats"].get("special-attack", "N/A")),
                      inline=True)
      embed.add_field(name="Sp. Def",
                      value=str(pokemon["stats"].get("special-defense",
                                                     "N/A")),
                      inline=True)
      embed.add_field(name="Speed",
                      value=str(pokemon["stats"].get("speed", "N/A")),
                      inline=True)

      await ctx.send(embed=embed)
    else:
      await ctx.send("ไม่สามารถดึงข้อมูลโปเกมอนได้ 😢")


async def setup(bot):
  await bot.add_cog(RandomPokemon(bot))
