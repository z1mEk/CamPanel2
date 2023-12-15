#!/usr/bin/env python3

import nest_asyncio
nest_asyncio.apply()
from general import events as generalEvents, plugins_loader
import threading
import time

def startCampanel():
    while True:
        print("CamPanel daemon is running...")
        event_loop = nest_asyncio.asyncio.get_event_loop()
        nest_asyncio.asyncio.ensure_future(generalEvents.onRun(event_loop))
        nest_asyncio.asyncio.ensure_future(plugins_loader.pluginsInit(event_loop))
        event_loop.run_forever()
        time.sleep(1)

daemon_thread = threading.Thread(target=startCampanel)
daemon_thread.daemon = True
daemon_thread.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Main thread interrupted. Exiting...")