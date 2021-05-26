import asyncio
from plugins.modbus.modbus import Relay
from plugins.modbus.properties import relayMeta

class data:
    class relay0(metaclass=relayMeta):
        relay = Relay.RELAY0
        pass

    class relay1(metaclass=relayMeta):
        relay = Relay.RELAY1
        pass

    class relay2(metaclass=relayMeta):
        relay = Relay.RELAY2
        pass

    class relay3(metaclass=relayMeta):
        relay = Relay.RELAY3
        pass

    class relay4(metaclass=relayMeta):
        relay = Relay.RELAY4
        pass

    class relay5(metaclass=relayMeta):
        relay = Relay.RELAY5
        pass

    class relay6(metaclass=relayMeta):
        relay = Relay.RELAY6
        pass

    class relay7(metaclass=relayMeta):
        relay = Relay.RELAY7
        pass

class plugin:
    @classmethod
    def readData(self, interval:int):
        pass

    @classmethod
    def initialize(self):
        loop = asyncio.get_event_loop()      
        loop.create_task(self.readData(1))
        loop.run_forever 