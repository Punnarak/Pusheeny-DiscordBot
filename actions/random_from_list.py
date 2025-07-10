from . import common_action_util as cau
import random
from discord.ext import commands

# คำสั่งสุ่ม
class RandAction(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def random_item_from_list(self, ctx, type):
        temp_list = cau.read_item_list(cau.info_dict[type][0])
        if not temp_list:
            await ctx.send("ยังไม่มีเมนูอาหารในรายการเลย ลองเพิ่มก่อนสิ!")
        else:
            temp = random.choice(temp_list)
            await ctx.send(f"สุ่มได้{cau.info_dict[type][2][0]}: **{temp}** {cau.info_dict[type][2][1]}")

    @commands.command(name="randfood", help="random food from list")
    async def random_food_from_list(self, ctx):
        await self.random_item_from_list(ctx, "food")

    @commands.command(name="randrestaurant", help="random restaurant from list")
    async def random_restaurant_from_list(self, ctx):
        await self.random_item_from_list(ctx, "restaurant")
            


async def setup(bot):
    await bot.add_cog(RandAction(bot))
