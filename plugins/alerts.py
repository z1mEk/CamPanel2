import asyncio

class plugin:
    name = 'Alerts'

    @classmethod
    def initialize(self):
        loop = asyncio.get_event_loop()      
        loop.run_forever