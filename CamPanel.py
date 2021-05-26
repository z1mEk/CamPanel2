import asyncio
from general import events, plugins

loop = asyncio.get_event_loop()
asyncio.ensure_future(events.onRun())
asyncio.ensure_future(plugins.pluginsInit())
loop.run_forever()