import random
from discord.ext import commands
import discord
import aiohttp


class RandomPokemon(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  def get_rarity(self, pokemon_id):
    if pokemon_id > 800:
      return "ตำนาน (Legendary)"
    elif pokemon_id > 500:
      return "หายาก (Rare)"
    else:
      return "ธรรมดา (Common)"

  def is_shiny(self):
    # โอกาสเจอ shiny 1 ใน 4096
    return random.randint(1, 4096) == 1

  async def get_random_pokemon(self):
    pokemon_id = random.randint(1, 1025)
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"

    async with aiohttp.ClientSession() as session:
      async with session.get(url) as resp:
        if resp.status == 200:
          data = await resp.json()
          name = data["name"].capitalize()
          shiny = self.is_shiny()
          sprite = data["sprites"]["front_shiny"] if shiny else data[
              "sprites"]["front_default"]
          types = ", ".join([t["type"]["name"] for t in data["types"]])
          rarity = self.get_rarity(pokemon_id)
          stats = {
              stat['stat']['name']: stat['base_stat']
              for stat in data['stats']
          }
          return {
              "name": name,
              "image": sprite,
              "types": types,
              "id": pokemon_id,
              "rarity": rarity,
              "shiny": shiny,
              "stats": stats
          }
        else:
          return None

  @commands.command(name="randpokemon", help="random pokemon")
  async def random_pokemon(self, ctx):
    pokemon = await self.get_random_pokemon()
    if pokemon:
      shiny_text = "✨ Shiny ✨" if pokemon["shiny"] else ""
      embed = discord.Embed(
          title=
          f"🎲 โปเกมอนสุ่มได้: {pokemon['name']} {shiny_text} (#{pokemon['id']})",
          description=
          f"ประเภท: {pokemon['types']}\nความหายาก: {pokemon['rarity']}",
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
