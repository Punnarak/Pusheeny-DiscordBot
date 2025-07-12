from . import common_action_util as cau
from discord.ext import commands

# แสดงรายการ
class GetListAction(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def output_list(self, input_list, ctx, type):
        msg = "\n".join(f"{i+1}. {item}" for i, item in enumerate(input_list))
        # ถ้าข้อความยาวเกินไป อาจต้องแบ่งส่งหลายข้อความ
        if len(msg) > 1900:
            temp_output_list = list()
            for i in range(0, len(msg), 1900):
                temp_output_list.append(f"```{msg[i:i+1900]}```")

            if temp_output_list:
                for item in temp_output_list:
                    await ctx.send(temp_output_list)
        else:
            await ctx.send("{}:\n```{}```".format(cau.info_dict[type][1], msg))

    @commands.command(name="listfood", help="show food list")
    async def get_food_from_list(self, ctx):
        food_list = cau.read_item_list(cau.info_dict["food"][0])
        if not food_list:
            await ctx.send("ยังไม่มีเมนูอาหารในรายการเลย 🍕")
        else:
            await self.output_list(food_list, ctx, "food")

    @commands.command(name="listrestaurant", help="show restaurant list")
    async def get_restaurant_from_list(self, ctx):
        restaurant_list = cau.read_item_list(cau.info_dict["restaurant"][0])
        if not restaurant_list:
            await ctx.send("ยังไม่มีร้านอาหารในรายการเลย 🍽️")
        else:
            await self.output_list(restaurant_list, ctx, "restaurant")

    @commands.command(name="listmovie", help="show movie list")
    async def get_movie_from_list(self, ctx):
        movie_list = cau.read_item_list(cau.info_dict["movie"][0])
        if not movie_list:
            await ctx.send("ยังไม่มีรายการหนังในรายการเลย 📽️")
        else:
            await self.output_list(movie_list, ctx, "movie")


async def setup(bot):
    await bot.add_cog(GetListAction(bot))
