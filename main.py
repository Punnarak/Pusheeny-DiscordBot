import discord
from discord.ext import commands
import random
from keep_alive import keep_alive
import os
import actions.random_from_list as rfl
import actions.add_to_list as atl
import actions.get_from_list as gfl
import actions.delete_from_list as dfl
import requests
from levels.level_system import get_leaderboard
from typing import Optional
from discord import Embed
# 👇 นำเข้าโมดูลจากโฟลเดอร์ levels
from levels.level_system import (add_xp, show_level, create_voice_xp_task)

TOKEN = os.environ['DISCORD_TOKEN']

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

voice_xp_task = create_voice_xp_task(bot)


@bot.event
async def on_ready():
    print(f"✅ Bot is ready: {bot.user}")
    voice_xp_task.start()


@bot.event
async def on_message(message):
    await add_xp(message.author, amount=1, context_channel=message.channel)
    if message.author.bot:
        return
    elif message.content.startswith("!hello") or message.content.startswith(
            "/hello"):
        await add_xp(message.author, amount=4, context_channel=message.channel)
        await message.channel.send("Hello from the other side!")

    elif message.content.startswith("!showtime") or message.content.startswith(
            "/showtime"):
        embedVar = discord.Embed(
            title='====== Showtime ======',
            url='https://www.instagram.com/pun_hasinanan/?utm_medium=copy_link',
            description="This is Movie Showtime",
            color=0xff0000
        ).set_image(
            url=
            'https://i.pinimg.com/originals/3c/67/e6/3c67e6d5dd463ab401cc780305af3306.jpg'
        )
        embedVar.add_field(name="4 แพร่ง", value="21:05", inline=False)
        # embedVar.add_field(name="Field2", value="hi2", inline=False)
        embedVar.set_footer(text="✨Get Ticket at the bottom of the post")
        await add_xp(message.author, amount=4, context_channel=message.channel)
        await message.channel.send(embed=embedVar)

    # คำสั่งสุ่ม
    elif message.content.startswith("!rand"):
        await add_xp(message.author, amount=4, context_channel=message.channel)
        await message.channel.send(rfl.rand_action(message.content))
    # คำสั่งเพิ่ม
    elif message.content.startswith("!add"):
        await add_xp(message.author, amount=4, context_channel=message.channel)
        await message.channel.send(atl.add_action(message.content))
    # แสดงรายการ
    elif message.content.startswith("!list"):
        await add_xp(message.author, amount=4, context_channel=message.channel)
        list = gfl.get_list_action(message.content)
        if list:
            for item in list:
                await message.channel.send(item)
        # ลบ ตามชื่อ หรือ ตามเลขลำดับ
        elif message.content.startswith("!del"):
            await add_xp(message.author,
                         amount=4,
                         context_channel=message.channel)
            await message.channel.send(dfl.delete_action(message.content))
    # Random meme from Reddit
    elif message.content.startswith("!meme"):
        await add_xp(message.author, amount=4, context_channel=message.channel)
        response = requests.get("https://meme-api.com/gimme")
        data = response.json()

        embed = discord.Embed(title=data["title"],
                              url=data["postLink"],
                              color=0xFFC0CB)
        embed.set_image(url=data["url"])
        embed.set_footer(
            text=
            f"👍 {data['ups']} | r/{data['subreddit']} | by {data['author']}")
        await message.channel.send(embed=embed)
    elif message.content.startswith("!eat r") or message.content.startswith(
            "/eat r"):
        restaurant = [
            "น้องเนยส้มตำ", "เนื้อหนัง", "เจ๊หมวย", "เรือนจำนมสด",
            "ลุงโตเกียว", "ไม่ตกไม่แตก", "นายอีฟ", "ย่างเนย", "ติดมันส์",
            "MLC", "Seoul Good", "Kaikao"
        ]  #12
        i = random.randint(0, len(restaurant) - 1)
        await add_xp(message.author, amount=4, context_channel=message.channel)
        await message.channel.send(restaurant[i])

    elif message.content.startswith("!do") or message.content.startswith(
            "/do"):
        await add_xp(message.author, amount=4, context_channel=message.channel)
        do = ["เล่นเกม", "ดูหนัง", "ดูการ์ตูน", "ไถTiktok"]  #4
        i = random.randint(0, len(do) - 1)
        if (i == 0):
            what = [
                "DOTA 2", "Genshin Impact", "OSU!", "ROV", "LOL", "Valorant"
            ]  #6
            x = random.randint(0, len(what) - 1)
            await message.channel.send(do[i] + what[x])
        elif (i == 1):
            what = [
                "Action", "Comedy", "Drama", "Fantasy", "Horror", "Mystery",
                "Romance", "Thriller"
            ]  #8
            x = random.randint(0, len(what) - 1)
            await message.channel.send(do[i] + what[x])

        else:
            await message.channel.send(do[i])
        # elif message.content.startswith("!clear") or message.content.startswith("/clear"):
    await bot.process_commands(message)


@bot.command()
async def command(message):
    embedc = discord.Embed(
        title='====== Command ======',
        url='https://www.instagram.com/pun_hasinanan/?utm_medium=copy_link',
        description="This is Pusheeny Command",
        color=0xFFC0CB
    ).set_image(
        url=
        'https://i.pinimg.com/originals/35/25/46/352546eccb66bb11200f99b9aa1268a8.gif'
    )
    embedc.add_field(name="!hello", value="hi", inline=False)
    embedc.add_field(name="!level", value="show your level", inline=False)
    embedc.add_field(name="!leaderboard",
                     value="show leaderboard of top 5",
                     inline=False)
    embedc.add_field(name="!meme",
                     value="random meme from Reddit",
                     inline=False)
    embedc.add_field(name="!showtime", value="check movie time", inline=False)
    embedc.add_field(
        name="!addfood",
        value="add food in food list for randomization\nformat: !addfood <food>",
        inline=False)
    embedc.add_field(name="!delfood",
                     value="delete food from food list\nformat: !delfood <food>",
                     inline=False)
    embedc.add_field(name="!randfood", value="random food", inline=False)
    embedc.add_field(name="!eat r", value="random restaurant", inline=False)
    embedc.add_field(name="!do", value="random event", inline=False)
    embedc.add_field(name="!command", value="show all command", inline=False)
    # embedVar.set_footer(text="✨Get Ticket at the bottom of the post")
    await add_xp(message.author, amount=4, context_channel=message.channel)
    await message.channel.send(embed=embedc)


@bot.listen("on_command")
async def on_command(ctx):
    if ctx.author.bot:
        return
    await add_xp(ctx.author, amount=-1, context_channel=ctx.channel)
    await add_xp(ctx.author, amount=5, context_channel=ctx.channel)


@bot.command()
async def level(ctx, member: Optional[discord.Member] = None):
    if member is None:
        member = ctx.author  # ตั้งค่า default เป็นผู้ใช้ที่รันคำสั่ง
    await show_level(ctx, member)


@bot.command()
async def leaderboard(ctx):
    top_users = get_leaderboard()
    if not top_users:
        await ctx.send("📉 ยังไม่มีข้อมูลเลเวลในระบบเลยค่ะ!")
        return

    medals = ["🥇", "🥈", "🥉"]

    for index, (user_id, stats) in enumerate(top_users, start=1):
        try:
            user = await bot.fetch_user(int(user_id))
            name = f"{user.mention}"  # จะ tag user
            avatar_url = user.avatar.url if user.avatar else user.default_avatar.url
        except:
            name = f"User ID {user_id}"
            avatar_url = None

        medal = medals[index - 1] if index <= 3 else f"#{index}"
        level = stats["level"]
        xp = stats["xp"]

        embed = Embed(
            title=f"{medal} อันดับที่ {index}",
            description=f"👤 {name}\n⭐ Level: `{level}` | ✨ XP: `{xp}`",
            color=discord.Color.gold())

        if avatar_url:
            embed.set_thumbnail(url=avatar_url)

        await ctx.send(embed=embed)

    await ctx.send("📊 อัปเดตทุกครั้งที่มีคนใช้บอทหรือส่งข้อความ")


keep_alive()
bot.run(TOKEN)
