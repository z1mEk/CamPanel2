from bluepy.btle import Peripheral, DefaultDelegate, UUID
import json

class BLEServerDelegate(DefaultDelegate):
    def __init__(self, peripheral):
        DefaultDelegate.__init__(self)
        self.peripheral = peripheral

    def handleNotification(self, cHandle, data):
        print(f"Odebrano dane BLE: {data.decode()}")
        response_data = {"nazwisko": "Gabriel Zima"}
        response_json = json.dumps(response_data)
        self.peripheral.writeCharacteristic(cHandle, response_json.encode(), withResponse=True)

def run_ble_server():
    # Ustawienia BLE
    service_uuid = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
    characteristic_uuid = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"

    # Utwórz serwer BLE
    peripheral = Peripheral()
    peripheral.setDelegate(BLEServerDelegate(peripheral))

    try:
        # Utwórz usługę i charakterystykę
        service = peripheral.getServiceByUUID(UUID(service_uuid))
        characteristic = service.getCharacteristics(UUID(characteristic_uuid))[0]

        print("Oczekiwanie na dane BLE...")

        while True:
            if peripheral.waitForNotifications(1.0):
                continue

    except KeyboardInterrupt:
        pass

    finally:
        peripheral.disconnect()

if __name__ == "__main__":
    run_ble_server()