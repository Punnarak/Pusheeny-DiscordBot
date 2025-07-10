from discord.ext import commands
import discord
import requests


# คำสั่งสุ่ม external source
class RandomFromExternalSrc(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

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

  @commands.command(name="joke", help="random joke from JokeAPI")
  async def random_joke_from_api(self, ctx):
    response = requests.get("https://v2.jokeapi.dev/joke/Any")
    data = response.json()

    if data["type"] == "single":
      # มุกแบบบรรทัดเดียว
      joke = data["joke"]
    else:
      # มุกแบบ 2 ส่วน (setup + delivery)
      joke = f"{data['setup']}\n||{data['delivery']}||"

    embed = discord.Embed(title="Here's a joke for you!",
                        description=joke,
                        color=0x00FFFF)
    embed.set_footer(text=f"Category: {data['category']}")
    await ctx.send(embed=embed)

  @commands.command(name="askyn", help="สุ่มตอบ Yes/No/Maybe พร้อม gif จากคำถามที่ถาม")
  async def ask_yes_no(self, ctx, *, question: str = None):
    try:
        # ดึงคำตอบจาก YesNo API
        response = requests.get("https://yesno.wtf/api", timeout=5)
        if response.status_code != 200:
            raise Exception("API response error")

        data = response.json()
        answer = data.get("answer", "unknown").capitalize()  # Yes / No / Maybe
        image_url = data.get("image")

        if not question:
            question = "คำถามอะไรบางอย่าง..."

        # สร้าง Embed
        embed = discord.Embed(
            title=f"ถามว่า: {question}",
            description=f"🎲 คำตอบ: **{answer}**",
            color=0x85edda
        )
        embed.set_image(url=image_url)
        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"❌ เกิดข้อผิดพลาด: `{e}`")



async def setup(bot):
  await bot.add_cog(RandomFromExternalSrc(bot))
