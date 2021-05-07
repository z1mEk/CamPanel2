import asyncio
from general import events, tasks

loop = asyncio.get_event_loop()
asyncio.ensure_future(events.onRun())

for t in dir(tasks):
    if t.startswith('periodic_'):
        loop.create_task(getattr(tasks, t)())

loop.run_forever()
