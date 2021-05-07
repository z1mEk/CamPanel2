import asyncio

class data:
    class pv:
        voltage = 0
        current = 0
        power = 0
        status = 0

    class battery:
        voltage = 0
        current = 0
        temperature = 0
        status = 0
        chargingStatus = 0

    class load:
        voltage = 0
        current = 0
        power = 0
        status = 0

class plugin:
    name = 'PV Controler'

    @classmethod
    def initialize(self):
        loop = asyncio.get_event_loop()      
        loop.run_forever