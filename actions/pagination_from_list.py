import discord
from . import common_action_util as cau

class ListPaginationView(discord.ui.View):
    def __init__(self, ctx, item_list, listtype):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.item_list = item_list
        self.page = 0
        self.per_page = 15
        self.message = None
        self.listtype = listtype

    def get_total_pages(self):
        return (len(self.item_list) - 1) // self.per_page + 1

    def generate_embed(self):
        start = self.page * self.per_page
        end = start + self.per_page
        embed = discord.Embed(title=f"{cau.info_dict[self.listtype][1]}",
                              description=f"หน้า {self.page + 1} / {self.get_total_pages()} 📃",
                              color=discord.Color.green()
                              )

        for idx, item in enumerate(self.item_list[start:end], start=start + 1):
            embed.add_field(name=f"{idx}. {item}",
                            value=f"",
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
