import asyncio

def RunAsync(proc):
    return asyncio.ensure_future(proc)
