from . import common_action_util as cau
from discord.ext import commands


def write_to_file(file, item):
  with open(file, "a", encoding="utf-8") as f:
    f.write(item.strip() + "\n")


# คำสั่งเพิ่มใส่รายการ
class AddAction(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  async def add_item_to_list(self, ctx, type):
    pass
    temp = ctx.message.content
    temp = temp.split(' ')
    new_temp = temp[1]
    if len(temp) > 2:
      for i in range(2, len(temp)):
        new_temp = new_temp + ' ' + temp[i]
    temp = new_temp
    if temp:
      temp_list = cau.read_item_list(cau.info_dict[type][0])
      if temp in temp_list:
        await ctx.send(
            f"มี{cau.info_dict[type][2][0]} **{temp}** อยู่ในรายการแล้ว!")
      else:
        write_to_file(cau.info_dict[type][0], temp)
        await ctx.send(
            f"เพิ่ม{cau.info_dict[type][2][0]}: **{temp}** เรียบร้อยแล้ว!")
    else:
      await ctx.send(
          f"โปรดระบุชื่อ{cau.info_dict[type][2][0]} เช่น \"!add{type} Ratatouille\""
      )

  @commands.command(
      name="addfood",
      help="add food in food list for randomization\nformat: !addfood <food>")
  async def add_food(self, ctx):
    await self.add_item_to_list(ctx, "food")
    
  @commands.command(
    name="addrestaurant",
    help="add restaurant in restaurant list for randomization\nformat: !addrestaurant <restaurant>")
  async def add_restaurant(self, ctx):
    await self.add_item_to_list(ctx, "restaurant")

  @commands.command(
      name="addmovie",
      help=
      "add movie in movie list for randomization\nformat: !addmovie <movie>")
  async def add_movie(self, ctx):
    await self.add_item_to_list(ctx, "movie")


async def setup(bot):
  await bot.add_cog(AddAction(bot))
