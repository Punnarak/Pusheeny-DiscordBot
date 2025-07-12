import pkgutil

async def setup(bot):
    package = __name__  # "actions"
    for _, module_name, is_pkg in pkgutil.iter_modules(__path__):
        if not is_pkg:
            if module_name not in ["common_action_util", "pagination_from_list"]:
                module = f"{package}.{module_name}"
                await bot.load_extension(module)
                print(f"✅ Loaded actions extension: {module}")
            
    
