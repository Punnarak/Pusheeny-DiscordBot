from discord.ext import commands
import discord
from typing import Optional
from discord import Embed
from levels.level_system import ( show_level )  # นำเข้าโมดูลจากโฟลเดอร์ levels
from levels.level_system import get_leaderboard

# คำสั่งเกี่ยวกับ level
class LevelCommand(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @commands.command(name="level", help="show your level")
  async def level(self, ctx, member: Optional[discord.Member] = None):
    if member is None:
      member = ctx.author  # ตั้งค่า default เป็นผู้ใช้ที่รันคำสั่ง
    await show_level(ctx, member)

  @commands.command(name="leaderboard", help="show leaderboard of top 5")
  async def leaderboard(self, ctx):
    top_users = get_leaderboard()
    if not top_users:
      await ctx.send("📉 ยังไม่มีข้อมูลเลเวลในระบบเลยค่ะ!")
      return

    medals = ["🥇", "🥈", "🥉"]

    for index, (user_id, stats) in enumerate(top_users, start=1):
      try:
        user = await self.bot.fetch_user(int(user_id))
        name = f"{user.mention}"  # จะ tag user
        avatar_url = user.avatar.url if user.avatar else user.default_avatar.url
      except:
        name = f"User ID {user_id}"
        avatar_url = None

      medal = medals[index - 1] if index <= 3 else f"#{index}"
      level = stats["level"]
      xp = stats["xp"]

      embed = Embed(title=f"{medal} อันดับที่ {index}",
                    description=f"👤 {name}\n⭐ Level: `{level}` | ✨ XP: `{xp}`",
                    color=discord.Color.gold())

      if avatar_url:
        embed.set_thumbnail(url=avatar_url)

      await ctx.send(embed=embed)

    await ctx.send("📊 อัปเดตทุกครั้งที่มีคนใช้บอทหรือส่งข้อความ")


async def setup(bot):
  await bot.add_cog(LevelCommand(bot))
