import importlib
from general.configLoader import config
from general.logger import logging

async def pluginsInit(event_loop):

    plugin_files = config.plugins

    logging.info(f"Plugins initialize: {plugin_files}")

    for module_name in plugin_files:
        if module_name in plugin_files:
            try:
                module = importlib.import_module(f"plugins.{module_name}")
                await module.plugin.initialize(event_loop)
                logging.info(f"Loaded: {module}")
            except Exception as e:
                logging.error(f"Plugins loader: {e}")

