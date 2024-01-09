#!/usr/bin/python
import nest_asyncio
nest_asyncio.apply()
from general import events as generalEvents, plugins_loader
import threading
import time
from general.logger import logging

def startCampanel():
    while True:
        logging.info("CamPanel is running...")
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
    logging.info("Main thread interrupted. Exiting...")