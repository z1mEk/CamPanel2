import asyncio
from enum import Enum
from plugins.helper import modbusCRC
from general import methods

class RelayAddress(Enum):
    RELAY0 = (0,0)
    RELAY1 = (0,1)
    RELAY2 = (0,2)
    RELAY3 = (0,3)
    RELAY4 = (0,4)
    RELAY5 = (0,5)
    RELAY6 = (0,6)
    RELAY7 = (0,7)

class relayMeta(type):
    address = None

    @property
    def val(self):
        return methods.RunAsync(self._getRelayState())
        
    @val.setter
    def val(self, value):
        methods.RunAsync(self._setRelayState(value))

    @classmethod
    async def toggle(cls):
        cls.val = 0 if cls.val == 0 else 1

    @classmethod
    async def on(cls):
        cls.val = 1

    @classmethod
    async def off(cls):
        cls.val = 0
    
    @classmethod
    async def _setRelayState(cls, value):
        cls.val = value
        await cls.onChange(value)
        # cmd = [cls.address[0], 0x05, 0, cls.address[1], 0, value if (value == 0) else 0xFF, 0, 0]
        # crc = modbusCRC.calculate(cmd[0:6])
        # cmd[6], cmd[7] = crc & 0xFF, crc >> 8
        #cls.serial.write(cmd)     

    @classmethod
    async def _getRelayState(cls):
        return cls.val
        # cmd = [cls.address[0], 0x05, 0, cls.address[1], 0xFF, 0, 0, 0]
        # crc = modbusCRC.calculate(cmd[0:6])
        # cmd[6], cmd[7] = crc & 0xFF, crc >> 8
        #cls.serial.write(cmd)
        #return cls.serial.read(cmd) 

    @classmethod
    async def onChange(cls, value):
        pass
        
class TRelay(metaclass=relayMeta):
    pass

class data:
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
    async def readData(cls, interval):
        while True:
            await asyncio.sleep(interval)  

    @classmethod
    def initialize(cls, event_loop):   
        event_loop.create_task(cls.readData(1))
