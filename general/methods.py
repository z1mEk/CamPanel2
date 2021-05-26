# methods of general
import asyncio

def RunAsync(proc):
    #return asyncio.ensure_future(proc)
    onceRunLoop = asyncio.new_event_loop()
    result = onceRunLoop.run_until_complete(proc)
    onceRunLoop.close()
    return result

