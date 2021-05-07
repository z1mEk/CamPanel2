import asyncio

class plugin:
    name = 'PV Controler'

    @classmethod
    def initialize(self):
        loop = asyncio.get_event_loop()      
        loop.run_forever