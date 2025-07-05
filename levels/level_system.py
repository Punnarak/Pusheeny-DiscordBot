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
                            await channel.send(
                                f"🎧 {member.display_name} เลเวลอัปเป็น **Level {new_level}** จากการอยู่ VC!"
                            )

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
            await context_channel.send(
                f"🎉 {member.mention} อัปเลเวลเป็น **Level {new_level}** แล้ว!")

    save_levels(data)


# 📊 คำสั่งแสดงเลเวล
async def show_level(ctx, member: Optional[discord.Member] = None):
    member = member or ctx.author
    user_id = str(member.id)
    data = load_levels()

    if user_id not in data:
        await ctx.send(f"{member.display_name} ยังไม่มีข้อมูลเลเวลเลยนะ!")
        return

    xp = data[user_id]["xp"]
    level = data[user_id]["level"]
    next_xp = (level + 1) * 100

    await ctx.send(
        f"📊 {member.display_name} | Level: **{level}**, XP: **{xp}/{next_xp}**"
    )


def get_leaderboard(top=5):
    data = load_levels()
    sorted_users = sorted(data.items(),
                          key=lambda x: (x[1]['level'], x[1]['xp']),
                          reverse=True)
    return sorted_users[:top]
