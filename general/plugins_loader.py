import os
import importlib

async def pluginsInit(event_loop):
    plugin_directory = "./plugins"
    plugin_files = [f[:-3] for f in os.listdir(plugin_directory) if f.endswith(".py") and not f.startswith("__")]

    print(f"Available plugins: {plugin_files}")
    print(f"Plugins initialize: ")

    for plugin_file in plugin_files:
        module_name = plugin_file
        if module_name in plugin_files:
            module = importlib.import_module(f"plugins.{module_name}")
            module.plugin.initialize(event_loop)
            print(f"Loaded: {module}")
