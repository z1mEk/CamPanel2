from bluepy.btle import Peripheral, Characteristic, Service, DefaultDelegate

class BLEServer:
    def __init__(self):
        try:
            # Utwórz obiekt Peripheral
            self.peripheral = Peripheral()

            # Utwórz usługę GATT
            service_uuid = "0000180a-0000-1000-8000-00805f9b34fb"  # Przykładowa usługa Device Information
            self.device_info_service = Service(service_uuid, 1)

            # Utwórz charakterystykę w ramach usługi
            characteristic_uuid = "00002a29-0000-1000-8000-00805f9b34fb"  # Przykładowa charakterystyka Manufacturer Name String
            self.manufacturer_name_characteristic = Characteristic(characteristic_uuid, 0x02, self.device_info_service)

            # Ustaw wartość domyślną
            self.manufacturer_name_characteristic.write("MyBLEDevice")

            # Dodaj charakterystykę do usługi
            self.device_info_service.addCharacteristic(self.manufacturer_name_characteristic)

            # Dodaj usługę do urządzenia
            self.peripheral.addService(self.device_info_service)

        except Exception as e:
            print(f"Błąd inicjalizacji serwera BLE: {e}")
            raise

    def run_server(self):
        try:
            print("Uruchomiono serwer BLE. Oczekiwanie na połączenia...")

            # Pozostań w pętli głównej, aby serwer działał ciągle
            while True:
                if self.peripheral.waitForNotifications(1.0):
                    continue

        except KeyboardInterrupt:
            print("Zatrzymano serwer BLE.")

        finally:
            self.peripheral.disconnect()

if __name__ == "__main__":
    try:
        # Utwórz instancję serwera BLE
        server = BLEServer()
        server.run_server()

    except KeyboardInterrupt:
        print("Zatrzymano program.")
