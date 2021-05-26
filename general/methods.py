# methods of general
import asyncio
from general import loop

def RunAsync(proc):
    #return asyncio.ensure_future(proc)
    #loop = asyncio.new_event_loop()
    #asyncio.set_event_loop(loop)
    return loop.loop.run_until_complete(proc)
