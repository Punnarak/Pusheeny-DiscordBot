import discord
from discord.ext import commands, tasks
import requests
import datetime
import os
from requests.structures import CaseInsensitiveDict

TOKEN = os.getenv('GOLD_API_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))


class GoldPriceNotifier(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.gold_alert.start()

    def cog_unload(self):
        self.gold_alert.cancel()

    @tasks.loop(time=[
        datetime.time(hour=8, tzinfo=datetime.timezone(datetime.timedelta(hours=7))),
        datetime.time(hour=12, tzinfo=datetime.timezone(datetime.timedelta(hours=7))),
        datetime.time(hour=17, tzinfo=datetime.timezone(datetime.timedelta(hours=7)))
    ])
    async def gold_alert(self):
        channel_id = CHANNEL_ID  # แทนด้วย ID ช่องจริง
        channel = self.bot.get_channel(channel_id)
        if not channel:
            return
        try:
            url = f"https://api.metals.dev/v1/latest?api_key={TOKEN}&currency=USD&unit=toz&base=USD&symbols=XAU"
            headers = CaseInsensitiveDict()
            headers["Accept"] = "application/json"
            response = requests.get(url, headers=headers)
            data = response.json()

            if "metals" in data and "gold" in data["metals"]:
                gold_price = data["metals"]["gold"]
                thb_rate = data.get("currencies", {}).get("THB")

                desc = f"**1 XAU = {gold_price:,.2f} USD**"
                if thb_rate:
                    thb = 1/thb_rate
                    desc += f"\n💵 **1 USD = {thb:,.2f} บาท**"

                embed = discord.Embed(title="📈 ราคาทองคำ XAU/USD และค่าเงินบาท",
                                      description=desc,
                                      color=0xFFD700,
                                      timestamp=datetime.datetime.utcnow())
                embed.set_footer(text="ข้อมูลจาก metals.dev")
                await channel.send(embed=embed)

            else:
                await channel.send("❌ ไม่พบข้อมูลราคาทองคำจาก API")

        except Exception as e:
            await channel.send(f"❌ ไม่สามารถดึงราคาทองได้: `{e}`")


async def setup(bot):
    await bot.add_cog(GoldPriceNotifier(bot))
