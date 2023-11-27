# methods of general
import nest_asyncio
nest_asyncio.apply()

def RunAsync(proc):
    loop = nest_asyncio.asyncio.get_event_loop()
    ret = loop.run_until_complete(proc)
    return ret

