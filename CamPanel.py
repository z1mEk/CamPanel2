import asyncio
from general import events, plugins

event_loop = asyncio.get_event_loop()
asyncio.ensure_future(events.onRun(event_loop))
asyncio.ensure_future(plugins.pluginsInit(event_loop))
event_loop.run_forever()