import asyncio

class plugin:

    @classmethod
    def initialize(self):
        loop = asyncio.get_event_loop()      
        loop.run_forever