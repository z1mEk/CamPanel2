# methods of general
import asyncio

def RunAsync(proc):
    #return asyncio.ensure_future(proc)
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(proc)
