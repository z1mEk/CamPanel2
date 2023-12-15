#!/usr/bin/env python3

import nest_asyncio
nest_asyncio.apply()
from general import events as generalEvents, plugins_loader

event_loop = nest_asyncio.asyncio.get_event_loop()
nest_asyncio.asyncio.ensure_future(generalEvents.onRun(event_loop))
nest_asyncio.asyncio.ensure_future(plugins_loader.pluginsInit(event_loop))
event_loop.run_forever()
