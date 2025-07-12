import discord
from . import common_pokemon_util as cpu

class PokemonPaginationView(discord.ui.View):
    def __init__(self, ctx, input_list, keyword=None):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.pokemon_list = input_list
        self.page = 0
        self.per_page = 5
        self.message = None
        self.keyword = keyword

    def get_total_pages(self):
        return (len(self.pokemon_list) - 1) // self.per_page + 1

    def generate_embed(self):
        start = self.page * self.per_page
        end = start + self.per_page
        if not self.keyword:
            title = f"🔍 ผลการค้นหา: \"{self.keyword}\""
        else:
            title = f"📦 โปเกมอนของ {self.ctx.author.display_name}"
        embed = discord.Embed(title=title,
                              description=f"หน้า {self.page + 1} / {self.get_total_pages()} 📃",
                              color=0x00ccff
                              )

        for idx, pokemon in enumerate(self.pokemon_list[start:end], start=start + 1):
            shiny = "✨" if pokemon.get("shiny") else ""
            emoji = cpu.get_rarity_emoji(pokemon['is_legendary'], pokemon['is_mythical'])
            name_line = f"{pokemon['name']} {shiny}"
            rarity = pokemon['leg_or_myth']
            detail_line = f"ประเภท: {pokemon['types']}\nความหายาก: {emoji} {rarity}\nID: #{pokemon['id']}"

            embed.add_field(name=f"{idx}. {name_line}",
                            value=detail_line,
                            inline=False
                            )
        embed.set_footer(text=f"หน้า {self.page + 1} / {self.get_total_pages()} 📃")

        return embed

    async def update(self, interaction: discord.Interaction):
        await interaction.response.edit_message(embed=self.generate_embed(), view=self)

    @discord.ui.button(label="⏮️", style=discord.ButtonStyle.grey)
    async def first(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.page = 0
        await self.update(interaction)

    @discord.ui.button(label="⏪", style=discord.ButtonStyle.grey)
    async def prev(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.page > 0:
            self.page -= 1
            await self.update(interaction)

    @discord.ui.button(label="⏩", style=discord.ButtonStyle.grey)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.page < self.get_total_pages() - 1:
            self.page += 1
            await self.update(interaction)

    @discord.ui.button(label="⏭️", style=discord.ButtonStyle.grey)
    async def last(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.page = self.get_total_pages() - 1
        await self.update(interaction)

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        if self.message:
            try:
                await self.message.edit(view=self)
            except discord.NotFound:
                pass
