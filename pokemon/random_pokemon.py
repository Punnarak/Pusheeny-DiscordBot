import random
from discord.ext import commands
import discord
import aiohttp


class RandomPokemon(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  def is_shiny(self):
    # โอกาสเจอ shiny 1 ใน 4096
    return random.randint(1, 4096) == 1

  async def get_random_pokemon(self):
    pokemon_id = random.randint(1, 1025)
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
    url2 = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}"

    async with aiohttp.ClientSession() as session:
      async with session.get(url) as resp:
        if resp.status == 200:
          data = await resp.json()
          name = data["name"].capitalize()
          shiny = self.is_shiny()
          sprite = data["sprites"]["front_shiny"] if shiny else data[
              "sprites"]["front_default"]
          types = ", ".join([t["type"]["name"] for t in data["types"]])
          stats = {
              stat['stat']['name']: stat['base_stat']
              for stat in data['stats']
          }
          info1 = {
              "name": name,
              "image": sprite,
              "types": types,
              "id": pokemon_id,
              "shiny": shiny,
              "stats": stats
          }
        else:
          info1 = dict()

    async with aiohttp.ClientSession() as session:
      async with session.get(url2) as resp:
        if resp.status == 200:
          data = await resp.json()
          cap_rate = data["capture_rate"]
          is_leg = data["is_legendary"]
          is_myth = data["is_mythical"]
          info2 = {"capture_rate": cap_rate}
          if is_leg:
            info2["is_legendary"] = "โปเกม่อนในตำนาน"
          else:
            info2["is_legendary"] = ""
          if is_myth:
            info2["is_mythical"] = "โปเกม่อนเทพนิยาย"
          else:
            info2["is_mythical"] = ""
        else:
          info2 = dict()

    if len(info1) == 0 or len(info2) == 0:
      return None
    else:
      info1.update(info2)
      return info1

  @commands.command(name="randpokemon", help="random pokemon")
  async def random_pokemon(self, ctx):
    pokemon = await self.get_random_pokemon()
    if pokemon:
      shiny_text = "✨ Shiny ✨" if pokemon["shiny"] else ""
      embed = discord.Embed(
          title=
          f"🎲 โปเกมอนสุ่มได้: {pokemon['name']} {shiny_text} (#{pokemon['id']})",
          description=
          f"ประเภท: {pokemon['types']} {pokemon['is_legendary']}{pokemon['is_mythical']}",
          color=discord.Color.random())
      embed.set_thumbnail(url=pokemon['image'])

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
