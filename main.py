import discord
import random
from keep_alive import keep_alive
import os

TOKEN = os.environ['DISCORD_TOKEN']
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("{0.user} is online".format(client))

@client.event
async def on_message(message):
    message.content = message.content.lower()
    if message.author == client.user:
        return

    elif message.content.startswith("!hello") or message.content.startswith(
            "/hello"):
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
        await message.channel.send(embed=embedVar)

    elif message.content.startswith("!eat f") or message.content.startswith(
            "/eat f"):
        food = [
            "ข้าวกะเพราไก่กรอบ", "ข้าวกะเพราหมูกรอบ", "มาม่าผัดกะเพราหมูกรอบ",
            "ข้าวผัดหมู", "ไข่เจียว", "ข้าวมันไก่ทอด", "ข้าวมันไก่ต้ม",
            "หมูกระทะ", "ชาบู", "สลัด", "แพนเค้ก", "สเต็ก",
            "ข้าวเหนียวหมูปิ้ง", "ก๋วยเตี๋ยว", "เครป", "มาม่า", "ข้าวขาหมู",
            "บิงซู", "ฮันนี่โทส"
        ]  #19
        i = random.randint(0, 18)
        await message.channel.send(food[i])

    elif message.content.startswith("!eat r") or message.content.startswith(
            "/eat r"):
        restaurant = [
            "น้องเนยส้มตำ", "เนื้อหนัง", "เจ๊หมวย", "เรือนจำนมสด",
            "ลุงโตเกียว", "ไม่ตกไม่แตก", "นายอีฟ", "ย่างเนย", "ติดมันส์",
            "MLC", "Seoul Good", "Kaikao"
        ]  #12
        i = random.randint(0, 11)
        await message.channel.send(restaurant[i])

    elif message.content.startswith("!do") or message.content.startswith(
            "/do"):
        do = ["เล่นเกม", "ดูหนัง", "ดูการ์ตูน", "ไถTiktok"]  #4
        i = random.randint(0, 3)
        if (i == 0):
            what = [
                "DOTA 2", "Genshin Impact", "OSU!", "ROV", "LOL", "Valorant"
            ]  #6
            x = random.randint(0, 5)
            await message.channel.send(do[i] + what[x])
        elif (i == 1):
            what = [
                "Action", "Comedy", "Drama", "Fantasy", "Horror", "Mystery",
                "Romance", "Thriller"
            ]  #8
            x = random.randint(0, 7)
            await message.channel.send(do[i] + what[x])

        else:
            await message.channel.send(do[i])

    elif message.content.startswith("!command") or message.content.startswith(
            "/command"):
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
        embedc.add_field(name="!showtime",
                         value="check movie time",
                         inline=False)
        embedc.add_field(name="!eat f", value="random food", inline=False)
        embedc.add_field(name="!eat r",
                         value="random restaurant",
                         inline=False)
        embedc.add_field(name="!do", value="random event", inline=False)
        embedc.add_field(name="!command",
                         value="show all command",
                         inline=False)
        # embedVar.set_footer(text="✨Get Ticket at the bottom of the post")
        await message.channel.send(embed=embedc)

    # elif message.content.startswith("!clear") or message.content.startswith("/clear"):


keep_alive()
client.run(TOKEN)
