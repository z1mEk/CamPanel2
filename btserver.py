from bluepy.btle import Peripheral, UUID

# Define the BLE device address and service UUID
device_address = "02:11:23:34:86:E2"  # Replace with your BLE device address
service_uuid = "0000180f-0000-1000-8000-00805f9b34fb"  # Example: Battery Service UUID

# Connect to the BLE device
peripheral = Peripheral(device_address)

# Get the service by UUID
service = peripheral.getServiceByUUID(UUID(service_uuid))

# Iterate through characteristics in the service
for characteristic in service.getCharacteristics():
    print(f"Characteristic UUID: {characteristic.uuid}")

    # Read the value of the characteristic
    value = characteristic.read()
    print(f"Characteristic Value: {value}")

# Disconnect from the BLE device
peripheral.disconnect()