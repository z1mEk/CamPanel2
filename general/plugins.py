import logging
import types
from plugins import bms, waterLevel, updateHmi

async def pluginsInit():
    for name, val in globals().items():
        if isinstance(val, types.ModuleType) and 'plugin' in dir(val) and 'initialize' in dir(val.plugin):
            val.plugin.initialize()
