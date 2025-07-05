import discord
from discord.ext import tasks
import json
import os
import random
from typing import Optional

LEVEL_FILE = "levels/levels.json"


def load_levels():
    if not os.path.exists(LEVEL_FILE):
        with open(LEVEL_FILE, "w") as f:
            json.dump({}, f)
    try:
        with open(LEVEL_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("⚠️ levels.json พังหรือว่าง กำลังรีเซ็ต...")
        with open(LEVEL_FILE, "w") as f:
            json.dump({}, f)
        return {}


def save_levels(data):
    with open(LEVEL_FILE, "w") as f:
        json.dump(data, f, indent=4)


def calculate_level(xp):
    level = 0
    while xp >= (level + 1) * 100:
        level += 1
    return level


# 🎧 Task: Add XP if users are in VC
def create_voice_xp_task(bot):

    @tasks.loop(minutes=1)
    async def voice_xp_task():
        data = load_levels()
        for guild in bot.guilds:
            for vc in guild.voice_channels:
                for member in vc.members:
                    if member.bot:
                        continue
                    user_id = str(member.id)

                    if user_id not in data:
                        data[user_id] = {"xp": 0, "level": 0}

                    data[user_id]["xp"] += 0.1

                    new_level = calculate_level(data[user_id]["xp"])
                    if new_level > data[user_id]["level"]:
                        data[user_id]["level"] = new_level
                        channel = next(
                            (c for c in guild.text_channels
                             if c.permissions_for(guild.me).send_messages),
                            None)
                        if channel:
                            embed = Embed(
                                title="🎧 LEVEL UP ใน VC! 🎧",
                                description=
                                f"**{member.mention}** เลเวลอัปเป็น **Level {new_level}** จากการอยู่ใน Voice Channel! 🚀",
                                color=discord.Color.blue())
                            embed.set_thumbnail(
                                url=member.avatar.url if member.
                                avatar else member.default_avatar.url)
                            embed.set_footer(
                                text="อยู่ใน VC ก็ได้เลเวล! เก่งมาก 👍")
                            await channel.send(embed=embed)

        save_levels(data)

    return voice_xp_task


# ✨ เพิ่ม XP จากการส่งข้อความ/ใช้คำสั่ง
async def add_xp(member, amount, context_channel=None):
    user_id = str(member.id)
    data = load_levels()

    if user_id not in data:
        data[user_id] = {"xp": 0, "level": 0}

    data[user_id]["xp"] += amount
    new_level = calculate_level(data[user_id]["xp"])

    if new_level > data[user_id]["level"]:
        data[user_id]["level"] = new_level
        if context_channel:
            embed = discord.Embed(
                title="🎉 LEVEL UP! 🎉",
                description=
                f"**{member.mention}** ได้อัปเลเวลเป็น\n**Level {new_level}**\nเยี่ยมมาก! 🚀✨",
                color=discord.Color.gold())
            embed.set_thumbnail(url=member.avatar.url if member.
                                avatar else member.default_avatar.url)
            embed.set_footer(text="เก่งมาก! Keep going! 💪")
            await context_channel.send(embed=embed)

    save_levels(data)


# 📊 คำสั่งแสดงเลเวล
async def show_level(ctx, member: Optional[discord.Member] = None):
    member = member or ctx.author
    user_id = str(member.id)
    data = load_levels()

    if user_id not in data:
        await ctx.send(f"❌ {member.display_name} ยังไม่มีข้อมูลเลเวลเลยนะ!")
        return

    xp = data[user_id]["xp"]
    level = data[user_id]["level"]
    next_xp = (level + 1) * 100
    progress = xp / next_xp  # ค่า progress เป็น 0-1

    # สร้าง progress bar แบบง่ายด้วยตัวอักษร
    bar_length = 20  # ความยาว progress bar
    filled_length = int(bar_length * progress)
    empty_length = bar_length - filled_length
    bar = "█" * filled_length + "░" * empty_length
    percent = int(progress * 100)

    embed = discord.Embed(
        title=f"📊 เลเวลของ {member.display_name}",
        description=
        f"⭐ **Level:** {level}\n✨ **XP:** {xp} / {next_xp} ({percent}%)",
        color=0xFFC0CB)

    embed.set_thumbnail(
        url=member.avatar.url if member.avatar else member.default_avatar.url)

    embed.add_field(name="ความคืบหน้าของ XP", value=f"`{bar}`", inline=False)

    embed.set_footer(text="ขยันเก็บ XP เพื่ออัปเลเวลเร็วๆ นะ!")

    await ctx.send(embed=embed)


def get_leaderboard(top=5):
    data = load_levels()
    sorted_users = sorted(data.items(),
                          key=lambda x: (x[1]['level'], x[1]['xp']),
                          reverse=True)
    return sorted_users[:top]
