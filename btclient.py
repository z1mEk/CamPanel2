from bluepy.btle import Peripheral, UUID

def run_ble_client():
    # Ustawienia BLE
    service_uuid = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
    characteristic_uuid = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"

    peripheral_address = "02:11:23:34:86:E2"  # Wstaw rzeczywisty adres MAC serwera BLE

    # Utwórz klienta BLE i nawiąż połączenie
    peripheral = Peripheral(peripheral_address)

    try:
        # Pobierz usługę i charakterystykę
        service = peripheral.getServiceByUUID(UUID(service_uuid))
        characteristic = service.getCharacteristics(UUID(characteristic_uuid))[0]

        # Wyślij zapytanie do serwera
        characteristic.write(b"Pytanie")

        # Czekaj na odpowiedź od serwera
        if peripheral.waitForNotifications(10.0):
            print("Otrzymano odpowiedź od serwera.")
        else:
            print("Przekroczono czas oczekiwania na odpowiedź od serwera.")

    except Exception as e:
        print(f"Błąd podczas komunikacji z serwerem: {e}")

    finally:
        peripheral.disconnect()

if __name__ == "__main__":
    run_ble_client()