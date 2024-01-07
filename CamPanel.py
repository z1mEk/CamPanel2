#!/usr/bin/python

import nest_asyncio
nest_asyncio.apply()
from general import events as generalEvents, plugins_loader
import threading
import time

def startCampanel():
    while True:
        print("CamPanel daemon is running...")
        event_loop = nest_asyncio.asyncio.get_event_loop()
        event_loop.create_task(generalEvents.onRun(event_loop))
        event_loop.create_task(plugins_loader.pluginsInit(event_loop))
        event_loop.run_forever()

daemon_thread = threading.Thread(target=startCampanel)
daemon_thread.daemon = True
daemon_thread.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Main thread interrupted. Exiting...")