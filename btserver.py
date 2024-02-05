from gatt import Device, Service, Characteristic, Application

class MyCharacteristic(Characteristic):
    def __init__(self, service):
        Characteristic.__init__(
            self,
            service,
            uuid="6e400002-b5a3-f393-e0a9-e50e24dcca9e",
            properties=["notify", "write"]
        )
        self.addDescriptor(MyDescriptor(self))

    def WriteValue(self, value, options):
        print("WriteValue:", value)
        return True

class MyDescriptor(Descriptor):
    def __init__(self, characteristic):
        Descriptor.__init__(
            self,
            characteristic,
            uuid="2901",
            value="My Custom Characteristic"
        )

class MyService(Service):
    def __init__(self, application):
        Service.__init__(self, application=application, uuid="6e400001-b5a3-f393-e0a9-e50e24dcca9e")
        self.addCharacteristic(MyCharacteristic(self))

class MyApp(Application):
    def __init__(self):
        Application.__init__(self)

    def start(self):
        super().start()

app = MyApp()
app.addService(MyService(app))
app.start()
