from . import common_action_util as cau
from discord.ext import commands


# ลบ ตามชื่อ หรือ ตามเลขลำดับ
class DeleteAction(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def delete_item_from_list(self, ctx, type):
        temp = ctx.message.content
        temp = temp.split(' ')
        new_temp = temp[1]
        if len(temp) > 2:
            for i in range(2, len(temp)):
                new_temp = new_temp + ' ' + temp[i]
        temp = new_temp
        temp_list = cau.read_item_list(cau.info_dict[type][0])
        if not temp_list:
            await ctx.send("ยังไม่มี{cau.info_dict[type][2][0]}ในรายการเลย")

        # ลบตามเลขลำดับ
        if temp.isdigit():
            index = int(temp) - 1
            if 0 <= index < len(temp_list):
                removed = temp_list.pop(index)
                cau.save_item_list(cau.info_dict[type][0],
                                   temp_list)  # ← ใช้ฟังก์ชันใหม่
                await ctx.send(
                    f"ลบ{cau.info_dict[type][2][0]}ลำดับ {index+1}: **{removed}** เรียบร้อยแล้ว"
                )
            else:
                await ctx.send("เลขลำดับไม่ถูกต้อง")
        else:
            # ลบตามชื่อ
            if temp in temp_list:
                temp_list.remove(temp)
                cau.save_item_list(cau.info_dict[type][0],
                                   temp_list)  # ← ใช้ฟังก์ชันใหม่
                await ctx.send(
                    f"ลบ{cau.info_dict[type][2][0]}: **{temp}** เรียบร้อยแล้ว")
            else:
                await ctx.send(
                    f"ไม่พบ{cau.info_dict[type][2][0]}ชื่อ \"{temp}\"")

    @commands.command(
        name="delfood",
        help="delete food from food list\nformat: !delfood <food>")
    async def delete_food(self, ctx):
        await self.delete_item_from_list(ctx, "food")

    @commands.command(
        name="delrestaurant",
        help=
        "delete restaurant from restaurant list\nformat: !delrestaurant <restaurant>"
    )
    async def delete_restaurant(self, ctx):
        await self.delete_item_from_list(ctx, "restaurant")

    @commands.command(
        name="delmovie",
        help="delete movie from movie list\nformat: !delmovie <movie>")
    async def delete_movie(self, ctx):
        await self.delete_item_from_list(ctx, "movie")


async def setup(bot):
    await bot.add_cog(DeleteAction(bot))
