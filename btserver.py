import pygatt
import time

def handle_data(handle, value):
    print("Received data:", value.decode())

adapter = pygatt.GATTToolBackend()

try:
    adapter.start()

    # Utwórz serwer GATT
    server = adapter.add_service(uuid="6e400001-b5a3-f393-e0a9-e50e24dcca9e")

    # Utwórz charakterystykę w ramach usługi
    characteristic = server.add_characteristic(
        uuid="6e400002-b5a3-f393-e0a9-e50e24dcca9e",
        properties=["notify", "write"]
    )

    characteristic.on_write = handle_data

    print("BLE server started. Waiting for connections...")

    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("BLE server stopped.")

finally:
    adapter.stop()