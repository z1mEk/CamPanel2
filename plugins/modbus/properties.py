from plugins.modbus.modbus import ModbusRelays
from enum import Enum
from general import methods

class Relay(Enum):
    RELAY0 = (0,0)
    RELAY1 = (0,1)
    RELAY2 = (0,2)
    RELAY3 = (0,3)
    RELAY4 = (0,4)
    RELAY5 = (0,5)
    RELAY6 = (0,6)
    RELAY7 = (0,7)

class State(Enum):
    OFF = 0x00
    ON = 0xFF

class relayMeta(type):
    relay:Relay = None

    @property
    def value(self):
        return methods.RunAsync(ModbusRelays.getRelayState(self.relay))
        
    @value.setter
    def value(self, value:State):
        methods.RunAsync(ModbusRelays.setRelayState(self.relay, value))
        
class TRelay(metaclass=relayMeta):
    pass
