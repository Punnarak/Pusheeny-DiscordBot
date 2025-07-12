from discord.ext import commands
from . import common_pokemon_util as cpu
from . import pagination_pokemon as pagi


class SearchPokemon(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="searchpokemon", help="search from your pokemon list")
    async def searchpokemon(self, ctx, *, keyword: str):
        keyword_lower = keyword.lower()
        data = cpu.load_pokemon_data()
        all_pokemon = data.get(str(ctx.author.id), [])

        if not all_pokemon:
            await ctx.send("คุณยังไม่มีโปเกมอนเลยนะ!")
            return

        results = [p for p in all_pokemon if keyword_lower in p["name"].lower()]

        if not results:
            await ctx.send(f"ไม่พบโปเกมอนที่มีคำว่า \"{keyword}\"")
            return

        view = pagi.PokemonPaginationView(ctx, results, keyword)
        embed = view.generate_embed()
        message = await ctx.send(embed=embed, view=view)
        view.message = message

async def setup(bot):
    await bot.add_cog(SearchPokemon(bot))
