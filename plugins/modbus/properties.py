from plugins.modbus.modbus import CRC
from enum import Enum
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
        # crc = CRC.calculate(cmd[0:6])
        # cmd[6], cmd[7] = crc & 0xFF, crc >> 8
        #cls.serial.write(cmd)     

    @classmethod
    async def _getRelayState(cls):
        return cls.val
        # cmd = [address, 0x05, 0, relayNumber, 0xFF, 0, 0, 0]
        # crc = CRC.calculate(cmd[0:6])
        # cmd[6], cmd[7] = crc & 0xFF, crc >> 8
        #cls.serial.write(cmd)
        #return cls.serial.read(cmd) 

    @classmethod
    async def onChange(cls, value):
        pass
        
class TRelay(metaclass=relayMeta):
    pass
