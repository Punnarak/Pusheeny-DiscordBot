import pkgutil


async def setup(bot):
    package = __name__
    for _, module_name, is_pkg in pkgutil.iter_modules(__path__):
        if not is_pkg:
            if module_name not in ["pokemon_storage", "common_pokemon_util", "pagination_pokemon", "search_result_view"]:
                module = f"{package}.{module_name}"
                await bot.load_extension(module)
                print(f"✅ Loaded actions extension: {module}")
