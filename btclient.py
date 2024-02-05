from bluepy.btle import Peripheral, UUID

def run_ble_client():
    # Ustawienia BLE
    service_uuid = "12345678-1234-5678-1234-56789abcdef0"
    characteristic_uuid = "12345678-1234-5678-1234-56789abcdef1"

    peripheral_address = "02:11:23:34:86:E2"  # Wstaw rzeczywisty adres MAC serwera BLE

    # Utwórz klienta BLE i nawiąż połączenie
    peripheral = Peripheral(peripheral_address)

    try:
        # Pobierz usługę i charakterystykę
        service = peripheral.getServiceByUUID(UUID(service_uuid))
        characteristic = service.getCharacteristics(UUID(characteristic_uuid))[0]

        # Wyślij zapytanie do serwera
        value = characteristic.read()
        print("Otrzymano odpowiedź od serwera:", value.decode())

    except Exception as e:
        print(f"Błąd podczas komunikacji z serwerem: {e}")

    finally:
        peripheral.disconnect()

if __name__ == "__main__":
    run_ble_client()