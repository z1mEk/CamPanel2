import nest_asyncio
nest_asyncio.apply()
from general.logger import logging

def RunAsync(proc):
    event_loop = nest_asyncio.asyncio.get_event_loop()
    ret = event_loop.run_until_complete(proc)
    logging.debug(f"RunAsync({proc}) -> {ret}")
    return ret
