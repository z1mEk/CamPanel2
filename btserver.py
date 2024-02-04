from gatt import Device, constants

class BLEServer(Device):
    def read_by_handle(self, handle):
        print("Odebrano zapytanie o dane BLE.")
        response_data = {"nazwisko": "Gabriel Zima"}
        response_json = json.dumps(response_data)
        return bytearray(response_json.encode())

server = BLEServer(adapter_name='hci0', device_name='MyBLEServer')

try:
    server.add_service(uuid='6e400001-b5a3-f393-e0a9-e50e24dcca9e', primary=True)
    server.add_characteristic(uuid='6e400002-b5a3-f393-e0a9-e50e24dcca9e',
                              value="",
                              permissions=(constants.PERMISSION_READ |
                                           constants.PERMISSION_WRITE),
                              properties=(constants.PROPERTY_READ |
                                          constants.PROPERTY_WRITE),
                              secure=False)

    print("Oczekiwanie na połączenie...")

    server.run()
except KeyboardInterrupt:
    pass
finally:
    server.stop()