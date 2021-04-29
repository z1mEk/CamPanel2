import asyncio
from general import events, tasks

loop = asyncio.get_event_loop()
asyncio.ensure_future(events.onRun())
runTasks = [loop.create_task(getattr(tasks, t)()) for t in dir(tasks) if t.startswith('periodic_')]
loop.run_forever()
loop.close()