from plugins.modbus.modbus import Relay, State, ModbusRelays
from general import helper

class relayMeta(type):
    relay = None

    @property
    def value(self):
        return helper.RunAsync(ModbusRelays.getRelayState(self.relay))
        
    @value.setter
    def value(self, value:State):
        helper.RunAsync(ModbusRelays.setRelayState(self.relay, value))
