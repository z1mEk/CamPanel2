from bluepy.btle import Peripheral, UUID, DefaultDelegate
import json
import time
import subprocess

class BLEDelegate(DefaultDelegate):
    def handleNotification(self, cHandle, data):
        print("Odebrano dane BLE:", data.decode())

def send_json_data(peripheral, characteristic, data):
    json_data = json.dumps(data)
    characteristic.write(json_data.encode())

def get_ble_address():
    try:
        result = subprocess.check_output(["hcitool", "dev"]).decode("utf-8")
        lines = result.split("\n")
        for line in lines:
            if "hci" in line:
                parts = line.split()
                if len(parts) == 3:
                    return parts[2]  # Adres MAC urządzenia BLE
    except Exception as e:
        print("Błąd podczas pobierania adresu BLE:", e)
    return None

def main():
    # Ustawienia BLE
    service_uuid = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"  # Przykładowa usługa Custom UART
    characteristic_uuid = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"  # Przykładowa charakterystyka TX
    print(f"adress = {get_ble_address()}")
    peripheral_address = get_ble_address()  # Wstaw rzeczywisty adres MAC
    peripheral = Peripheral()  # Utwórz obiekt Peripheral bez podawania adresu na razie
    peripheral.setDelegate(BLEDelegate())

    try:
        peripheral.connect(peripheral_address)  # Nawiązanie połączenia z podanym adresem

        # Przykładowe dane JSON
        sample_data = {"key": "value", "temperature": 25.5, "status": "OK"}

        # Pobranie usługi i charakterystyki
        service = peripheral.getServiceByUUID(UUID(service_uuid))
        characteristic = service.getCharacteristics(UUID(characteristic_uuid))[0]

        print("Oczekiwanie na dane BLE...")

        while True:
            # Wysłanie danych JSON przez Bluetooth
            send_json_data(peripheral, characteristic, sample_data)

            time.sleep(1)  # Poczekaj przed kolejnym wysłaniem

    except KeyboardInterrupt:
        pass

    finally:
        peripheral.disconnect()  # Rozłączenie po zakończeniu programu

if __name__ == "__main__":
    main()
