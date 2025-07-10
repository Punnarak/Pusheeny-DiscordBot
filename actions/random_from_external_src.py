from . import common_action_util as cau
import random
from discord.ext import commands
import discord
import requests


# คำสั่งสุ่ม external source
class RandomFromExternalSrc(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
    self.api_key = "YOUR_RAPIDAPI_KEY"  # 🔁 ใส่คีย์จาก RapidAPI
    self.api_host = "unogsng.p.rapidapi.com"

  @commands.command(name="meme", help="random meme from Reddit")
  async def random_meme_from_reddit(self, ctx):
    response = requests.get("https://meme-api.com/gimme")
    data = response.json()

    embed = discord.Embed(title=data["title"],
                          url=data["postLink"],
                          color=0xFFC0CB)
    embed.set_image(url=data["url"])
    embed.set_footer(
        text=f"👍 {data['ups']} | r/{data['subreddit']} | by {data['author']}")
    await ctx.send(embed=embed)

async def setup(bot):
  await bot.add_cog(RandomFromExternalSrc(bot))
