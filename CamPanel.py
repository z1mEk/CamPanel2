import asyncio
from general import events

loop = asyncio.get_event_loop()
asyncio.ensure_future(events.onRun())
loop.run_forever()
