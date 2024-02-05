import asyncio
from bleak import BleakServer, BleakCharacteristic, BleakAdvertisingData

CHARACTERISTIC_UUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"

async def handle_write(sender: int, data: bytearray):
    print(f"Received data: {data.decode()}")

async def run_ble_server():
    # Utwórz serwer BLE
    server = BleakServer()

    # Utwórz charakterystykę
    characteristic = BleakCharacteristic(
        uuid=CHARACTERISTIC_UUID,
        description="Custom Characteristic",
        notify=True,
        write=True,
        write_callback=handle_write,
    )

    # Dodaj charakterystykę do serwera
    await server.add_characteristic(characteristic)

    # Skonfiguruj dane reklamowe
    advertising_data = BleakAdvertisingData(service_uuids=[CHARACTERISTIC_UUID])

    # Uruchom serwer z danymi reklamowymi
    await server.start(advertising_data=advertising_data)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_ble_server())
