import os
import importlib
import types

async def pluginsInit(event_loop):
    # Directory where files with classes are located
    plugin_directory = "../plugins"

    # Fetching a list of files in the directory.
    plugin_files = [f[:-3] for f in os.listdir(plugin_directory) if f.endswith(".py") and not f.startswith("__")]

    # Import classes
    for plugin_file in plugin_files:
        module_name = f"plugins.{plugin_file}"
        module = importlib.import_module(module_name)

        # Iterating through the attributes of the module (classes) and adding them to the current module.
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj):
                globals()[name] = obj

    # Initialization of plugins.
    for name, val in globals().items():
        if isinstance(val, types.ModuleType) and 'plugin' in dir(val) and 'initialize' in dir(val.plugin):
            val.plugin.initialize(event_loop)

''' old wersion
import types
from plugins import bms, water, relays, updateHmi

async def pluginsInit(event_loop):
    for name, val in globals().items():
        if isinstance(val, types.ModuleType) and 'plugin' in dir(val) and 'initialize' in dir(val.plugin):
            val.plugin.initialize(event_loop)
'''
