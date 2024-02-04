from bluepy.btle import Peripheral, UUID

def run_ble_client():
    # Ustawienia BLE
    service_uuid = "f000ffc0-0451-4000-b000-000000000000"
    characteristic_uuid = "f000ffc1-0451-4000-b000-000000000000"

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
            response_data = characteristic.read()
            print("Otrzymano odpowiedź od serwera:", response_data.decode())
        else:
            print("Przekroczono czas oczekiwania na odpowiedź od serwera.")

    except Exception as e:
        print(f"Błąd podczas komunikacji z serwerem: {e}")

    finally:
        peripheral.disconnect()

if __name__ == "__main__":
    run_ble_client()