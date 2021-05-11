import asynctio

def RunAsync(proc):
  return asyncio.get_event_loop().run_until_complete(proc)
