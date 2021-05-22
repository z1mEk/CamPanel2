import asyncio

def RunAsync(proc):
  #return asyncio.ensure_future(proc)
  return asyncio.get_event_loop().run_until_complete(proc)
