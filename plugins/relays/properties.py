from plugins.relays.modbus import Relay, State, ModbusRelays
from general import helper

class relayMeta(type):
    relay = None

    @property
    def value(self):
        return helper.RunAsync(ModbusRelays.getRelayState(relay))
        
    @value.setter
    def value(self, value:State):
        helper.RunAsync(ModbusRelays.setRelayState(relay, value))
