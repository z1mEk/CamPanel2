import asyncio
from plugins.modbus.modbus import Relay
from plugins.modbus.properties import TRelay

class data:
    class relay0(TRelay):
        relay = Relay.RELAY0
        pass

    class relay1(TRelay):
        relay = Relay.RELAY1
        pass

    class relay2(TRelay):
        relay = Relay.RELAY2
        pass

    class relay3(TRelay):
        relay = Relay.RELAY3
        pass

    class relay4(TRelay):
        relay = Relay.RELAY4
        pass

    class relay5(TRelay):
        relay = Relay.RELAY5
        pass

    class relay6(TRelay):
        relay = Relay.RELAY6
        pass

    class relay7(TRelay):
        relay = Relay.RELAY7
        pass

class plugin:
    @classmethod
    def readData(cls, interval:int):
        pass

    @classmethod
    def initialize(cls):
        loop = asyncio.get_event_loop()      
        loop.create_task(cls.readData(1))
        #loop.run_forever 