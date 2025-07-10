import discord
from discord.ext import commands
import random
from keep_alive import keep_alive
import os
import requests
from discord import Embed
from levels.level_system import (add_xp, create_voice_xp_task
                                 )  # นำเข้าโมดูลจากโฟลเดอร์ levels

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
    await bot.load_extension("actions.random_from_list")
    await bot.load_extension("actions.random_from_external_src")
    await bot.load_extension("actions.get_from_list")
    await bot.load_extension("actions.add_to_list")
    await bot.load_extension("actions.delete_from_list")
    await bot.load_extension("actions.chat")
    await bot.load_extension("actions.loop_tasks")
    await bot.load_extension("actions.pusheeny_timer")
    await bot.load_extension("levels.level_command")
    await bot.load_extension("pokemon.random_pokemon")
    await bot.load_extension("pokemon.catch_pokemon")
    await bot.load_extension("pokemon.my_pokemon")
    await bot.load_extension("pokemon.release_pokemon")

    print(f"✅ Bot is ready: {bot.user}")
    print("📋 Registered commands:")
    for command in bot.commands:
        print(f"- {command.name}")
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

@bot.command(name="command", help="show all command")
async def command(ctx):
    embedc = discord.Embed(title="✨ คำสั่งทั้งหมดของบอท ✨",
                           description="คำสั่งที่คุณสามารถใช้ได้ในบอทนี้",
                           color=0xFFC0CB)

    for cmd in bot.commands:
        if cmd.hidden:
            continue
        name = f"!{cmd.name}"
        desc = cmd.help or "ไม่มีคำอธิบาย"
        embedc.add_field(name=name, value=desc, inline=False)

    embedc.set_footer(text="ใช้ !<ชื่อคำสั่ง> เพื่อเรียกใช้งาน")
    embedc.set_image(
        url=
        "https://i.pinimg.com/originals/35/25/46/352546eccb66bb11200f99b9aa1268a8.gif"
    )

    await ctx.send(embed=embedc)


@bot.listen("on_command")
async def on_command(ctx):
    if ctx.author.bot:
        return
    await add_xp(ctx.author, amount=5, context_channel=ctx.channel)


keep_alive()
bot.run(TOKEN)
