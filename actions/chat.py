from discord.ext import commands
import requests
# คำสั่งสนทนา (หา api ใหม่ก่อน)
class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def call_thai_gpt_api(self, prompt):
        try:
            response = requests.post(
                "https://api-inference.huggingface.co/models/Fawass/aibeacon-thai-chatbot",
                json={"data": [prompt]},
                timeout=30
            )
            result = response.json()
            return result["data"][0]
        except Exception as e:
            return f"❌ เกิดข้อผิดพลาด: {e}"

    @commands.command(name="ai",help="chat with Pusheeny\nformat: !ai <message>")
    async def ai_command(self, ctx, *, message: str):
        await ctx.send("🤖 กำลังคิด...")
        reply = self.call_thai_gpt_api(message)
        await ctx.send(reply)

async def setup(bot):
    await bot.add_cog(Chat(bot))
