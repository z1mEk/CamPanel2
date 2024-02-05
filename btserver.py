import asyncio
from bleak import BleakServer, BleakCharacteristic, BleakAdvertisingData

CHARACTERISTIC_UUID = "f000ffc1-0451-4000-b000-000000000000"

async def send_data(characteristic):
    count = 0
    while True:
        data = f"Dane od serwera: {count}"
        await asyncio.sleep(1)  # Emulacja pracy serwera
        await characteristic.write_value(data.encode())
        count += 1

async def run_ble_server():
    # Utwórz serwer BLE
    server = BleakServer()

    # Utwórz charakterystykę
    characteristic = BleakCharacteristic(
        uuid=CHARACTERISTIC_UUID,
        description="Custom Characteristic",
        notify=True,
        write=False,
    )

    # Dodaj charakterystykę do serwera
    await server.add_characteristic(characteristic)

    # Uruchom wątek wysyłający dane
    asyncio.create_task(send_data(characteristic))

    # Skonfiguruj dane reklamowe
    advertising_data = BleakAdvertisingData(service_uuids=[CHARACTERISTIC_UUID])

    # Uruchom serwer z danymi reklamowymi
    await server.start(advertising_data=advertising_data)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_ble_server())
