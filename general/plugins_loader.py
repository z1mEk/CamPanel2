import importlib
from general.config_loader import config

async def pluginsInit(event_loop):

    plugin_files = config.plugins

    print(f"Plugins initialize: {plugin_files}")

    for module_name in plugin_files:
        if module_name in plugin_files:
            module = importlib.import_module(f"plugins.{module_name}")
            await module.plugin.initialize(event_loop)
            print(f"Loaded: {module}")
