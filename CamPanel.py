import asyncio
from general import events as generalEvents, plugins_loader

event_loop = asyncio.get_event_loop()
asyncio.ensure_future(generalEvents.onRun(event_loop))
asyncio.ensure_future(plugins_loader.pluginsInit(event_loop))
event_loop.run_forever()
