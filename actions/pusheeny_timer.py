from discord.ext import commands
import discord
import asyncio

class TimerCommand(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="timer", help="ตั้งเวลา เช่น !timer 1 หรือ !timer 0.20 ข้อความ")
    async def timer(self, ctx, time_arg: str, *, custom_message: str = None):
        try:
            if '.' in time_arg:
                minutes, seconds = map(int, time_arg.split('.'))
                total_seconds = minutes * 60 + seconds
            else:
                minutes = int(time_arg)
                total_seconds = minutes * 60
        except:
            await ctx.send("❌ รูปแบบเวลาผิดนะ ใช้แบบ `!timer 1` หรือ `!timer 0.20 ข้อความ`")
            return

        # ส่งข้อความเริ่มต้น
        countdown_msg = await ctx.send(f"⏳ เริ่มนับถอยหลัง {total_seconds} วินาที...")

        # แสดง countdown ทุก 5 วิ
        for remaining in range(total_seconds, 0, -1):
            if remaining % 5 == 0 or remaining <= 5:
                await countdown_msg.edit(content=f"⏳ เหลือเวลา {remaining} วินาที...")
            await asyncio.sleep(1)

        # เตรียมข้อความเมื่อหมดเวลา
        final_message = custom_message if custom_message else f"หมดเวลา {total_seconds} วินาทีแล้วว!"
        embed = discord.Embed(title="⏰ หมดเวลาแล้ว!!",
                              description=f"🎉 {final_message} 🎉",
                              color=0xe64747
                              )
        embed.set_image(
            url="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExdDhlYWd3aGlqMGpkM2g5YjI0andweWw0bG1jeGNrMDlpdGdmb3pyaSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/fUwOs80ja3sTPpjndh/giphy.gif"
        )
        embed.set_footer(text="⏳ Timer Completed!")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(TimerCommand(bot))
