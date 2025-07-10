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


def save_pokemon_data(data):
    with open(POKEMON_STORAGE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_sprite_url(pokemon):
    # ลองอ่านจาก field โดยตรง
    if "sprite" in pokemon:
        return pokemon["sprite"]
    # หรือสร้างจากชื่อภาษาอังกฤษ
    name = pokemon.get("english", pokemon.get("name",
                                              "")).lower().replace(" ", "-")
    return f"https://projectpokemon.org/images/normal-sprite/{name}.gif"


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


class ReleaseView(discord.ui.View):

    def __init__(self, ctx, pokemon, index):
        super().__init__(timeout=30)
        self.ctx = ctx
        self.pokemon = pokemon
        self.index = index

    async def interaction_check(self, interaction):
        return interaction.user == self.ctx.author

    @discord.ui.button(label="ยืนยัน", style=discord.ButtonStyle.danger)
    async def confirm(self, interaction: discord.Interaction,
                      button: discord.ui.Button):
        data = load_pokemon_data()
        user_id = str(self.ctx.author.id)
        if user_id in data and 0 <= self.index < len(data[user_id]):
            released = data[user_id].pop(self.index)
            save_pokemon_data(data)
            await interaction.response.edit_message(
                content=f"🕊️ ปล่อย `{released['name']}` ออกไปเรียบร้อยแล้ว!",
                embed=None,
                view=None)
        else:
            await interaction.response.send_message(
                "ไม่พบโปเกมอนตัวนี้ในกระเป๋า!", ephemeral=True)

    @discord.ui.button(label="ยกเลิก", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction,
                     button: discord.ui.Button):
        await interaction.response.edit_message(
            content="❌ ยกเลิกการปล่อยโปเกมอนแล้ว", embed=None, view=None)


class ReleasePokemon(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="releasepokemon",help="release pokemon from your pocket\nformat: !releasepokemon <index>")
    async def release_pokemon(self, ctx, index: int = None):
        data = load_pokemon_data()
        user_id = str(ctx.author.id)
        user_pokemon = data.get(user_id, [])

        if not user_pokemon:
            await ctx.send("คุณไม่มีโปเกมอนในกระเป๋าเลย 😢")
            return

        if index is None:
            # แสดงรายการโปเกม่อนแบบน่ารัก
            embed = discord.Embed(title="🧳 รายการโปเกมอนของคุณ",
                                  color=0x00ccff)

            for i, p in enumerate(user_pokemon, start=1):
                shiny = "✨" if p.get("shiny") else ""
                emoji = get_rarity_emoji(p.get("rarity", ""))
                name_line = f"{p['name']} {shiny}"
                detail_line = f"ความหายาก: {emoji} {p.get('rarity', '-')}\nID: #{p['id']}"

                embed.add_field(name=f"{i}. {name_line}",
                                value=detail_line,
                                inline=False)

            embed.set_footer(
                text="ใช้คำสั่ง !releasepokemon <index> เพื่อปล่อยโปเกมอน")
            await ctx.send(embed=embed)
            return

        if index < 0 or index-1 >= len(user_pokemon):
            await ctx.send("❌ Index ไม่ถูกต้อง")
            return

        p = user_pokemon[index-1]
        embed = discord.Embed(
            title=f"คุณแน่ใจหรือไม่ที่จะปล่อย {p['name']}?",
            description=
            f"ประเภท: {p.get('types', '-')}\nความหายาก: {p.get('rarity', '-')}",
            color=discord.Color.orange())
        embed.set_thumbnail(url=get_sprite_url(p))
        embed.set_footer(text=f"Index: {index}")
        view = ReleaseView(ctx, p, index-1)
        await ctx.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(ReleasePokemon(bot))
