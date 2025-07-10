import discord
from discord.ext import commands
import json
import os

POKEMON_STORAGE = "pokemon/pokemon_storage.json"


def load_pokemon_data():
    if os.path.exists(POKEMON_STORAGE):
        with open(POKEMON_STORAGE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def get_rarity_emoji(rarity):
    emojis = {
        "ธรรมดา (Common)": "⚪",
        "Uncommon": "🟢",
        "หายาก (Rare)": "🔵",
        "Epic": "🟣",
        "ตำนาน (Legendary)": "🟡",
        "Mythical": "🌟",
        "Ultra Beast": "🔥"
    }
    return emojis.get(rarity, "❓")


def get_sprite_url(pokemon):
    return f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon['id']}.png"


class MyPokemon(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mypokemon", help="show your pokemon")
    async def mypokemon(self, ctx):
        data = load_pokemon_data()
        user_pokemon = data.get(str(ctx.author.id), [])
        if not user_pokemon:
            await ctx.send("คุณยังไม่มีโปเกมอนในกระเป๋าเลย 😢")
            return

        embed = discord.Embed(title="🧳 รายการโปเกมอนของคุณ", color=0x00ccff)

        for i, p in enumerate(user_pokemon, start=1):
            shiny = "✨" if p.get("shiny") else ""
            emoji = get_rarity_emoji(p.get("rarity", ""))
            name_line = f"{p['name']} {shiny}"
            detail_line = f"ประเภท: {p['types']}\nความหายาก: {emoji} {p.get('rarity', '-')}\nID: #{p['id']}"

            embed.add_field(name=f"{i}. {name_line}",
                            value=detail_line,
                            inline=False)

        embed.set_footer(text="อย่าลืมพาโปเกมอนไปผจญภัยนะ! 🌟")

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(MyPokemon(bot))
