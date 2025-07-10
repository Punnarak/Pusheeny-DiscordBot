from . import common_action_util as cau
import random
from discord.ext import commands

# คำสั่งสุ่ม
class RandAction(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # async def random_item_from_list(self, ctx, type):
    #     temp_list = cau.read_item_list(cau.info_dict["food"][0])
    #     if not food_list:
    #         await ctx.send("ยังไม่มีเมนูอาหารในรายการเลย ลองเพิ่มก่อนสิ!")
    #     else:
    #         food = random.choice(food_list)
    #         await ctx.send(f"สุ่มได้เมนู: **{food}** 🍽️")

    @commands.command(name="randfood", help="random food from list")
    async def random_food_from_list(self, ctx):
        food_list = cau.read_item_list(cau.info_dict["food"][0])
        if not food_list:
            await ctx.send("ยังไม่มีเมนูอาหารในรายการเลย ลองเพิ่มก่อนสิ!")
        else:
            food = random.choice(food_list)
            await ctx.send(f"สุ่มได้เมนู: **{food}** 🍽️")


async def setup(bot):
    await bot.add_cog(RandAction(bot))
