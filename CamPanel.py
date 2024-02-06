#!/usr/bin/python
import nest_asyncio
from nest_asyncio import asyncio
nest_asyncio.apply()
from general import events as generalEvents, pluginsLoader
import threading
import time
from general.logger import logging

def startCampanel():
    while True:
        logging.info("CamPanel is running...")
        event_loop = asyncio.get_event_loop()
        event_loop.create_task(generalEvents.onRun(event_loop))
        event_loop.create_task(pluginsLoader.pluginsInit(event_loop))
        event_loop.run_forever()


if __name__ == '__main__':
    daemon_thread = threading.Thread(target=startCampanel)
    daemon_thread.daemon = True
    daemon_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Main thread interrupted. Exiting...")