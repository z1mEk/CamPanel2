import asyncio
from plugins.modbus.properties import TRelay, RelayAddress

class relay0(TRelay):
    address = RelayAddress.RELAY0

    @classmethod
    async def onChange(cls, value):
        print("onChange")

class relay1(TRelay):
    address = RelayAddress.RELAY1
    pass

class relay2(TRelay):
    address = RelayAddress.RELAY2
    pass

class relay3(TRelay):
    address = RelayAddress.RELAY3
    pass

class relay4(TRelay):
    address = RelayAddress.RELAY4
    pass

class relay5(TRelay):
    address = RelayAddress.RELAY5
    pass

class relay6(TRelay):
    address = RelayAddress.RELAY6
    pass

class relay7(TRelay):
    address = RelayAddress.RELAY7
    pass

class plugin:
    @classmethod
    def readData(cls, interval:int):
        pass

    @classmethod
    def initialize(cls, event_loop):   
        event_loop.create_task(cls.readData(1))
