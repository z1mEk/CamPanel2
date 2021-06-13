import types
from plugins import bms, water, relays, updateHmi

async def pluginsInit(event_loop):
    for name, val in globals().items():
        if isinstance(val, types.ModuleType) and 'plugin' in dir(val) and 'initialize' in dir(val.plugin):
            val.plugin.initialize(event_loop)
