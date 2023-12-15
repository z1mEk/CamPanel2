#!/usr/bin/env python3

import nest_asyncio
nest_asyncio.apply()
from general import events as generalEvents, plugins_loader
import threading

def startCampanel():
    while True:
        print("CamPanel daemon is running...")
        event_loop = nest_asyncio.asyncio.get_event_loop()
        nest_asyncio.asyncio.ensure_future(generalEvents.onRun(event_loop))
        nest_asyncio.asyncio.ensure_future(plugins_loader.pluginsInit(event_loop))
        event_loop.run_forever()
        nest_asyncio.asyncio.sleep(1)  # Adjust the sleep duration as needed

# Create a daemon thread
daemon_thread = threading.Thread(target=startCampanel)
daemon_thread.daemon = True

# Start the daemon thread
daemon_thread.start()

# Main thread can continue with other tasks or wait for the daemon to finish
try:
    while True:
        nest_asyncio.asyncio.sleep(1)
except KeyboardInterrupt:
    print("Main thread interrupted. Exiting...")