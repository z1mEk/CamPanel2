import asyncio

loop = None

def start():
    loop = asyncio.get_event_loop()
    loop.run_forever()
    
def createTask(task):
    loop.create_task(task)