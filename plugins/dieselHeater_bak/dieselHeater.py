import spidev
import RPi.GPIO as GPIO
import time

class DieselHeaterRF:
    def __init__(self, pin_sck, pin_mosi, pin_miso, pin_ss, pin_gdo2):
        self._pin_sck = pin_sck
        self._pin_mosi = pin_mosi
        self._pin_miso = pin_miso
        self._pin_ss = pin_ss
        self._pin_gdo2 = pin_gdo2
        self._heater_addr = 0
        self._packet_seq = 0
        self._spi = spidev.SpiDev()
        self._initialized = False

        self.init_gpio()
        self.init_spi()

        time.sleep(0.1)

    def init_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._pin_sck, GPIO.OUT)
        GPIO.setup(self._pin_mosi, GPIO.OUT)
        GPIO.setup(self._pin_miso, GPIO.IN)
        GPIO.setup(self._pin_ss, GPIO.OUT)
        GPIO.setup(self._pin_gdo2, GPIO.IN)

        self._initialized = True

    def init_spi(self):
        self._spi.open(0, 0)
        self._spi.max_speed_hz = 1000000
        self._spi.mode = 0b00

    def begin(self, heater_addr=0):
        if not self._initialized:
            self.init_gpio()

        self._heater_addr = heater_addr
        self.set_pin_output(self._pin_ss, GPIO.LOW)
        time.sleep(0.1)
        self.init_radio()
        self.set_pin_output(self._pin_ss, GPIO.HIGH)

    def init_radio(self):
        self.write_strobe(0x30)
        time.sleep(0.1)

        self.write_reg(0x00, 0x07)
        self.write_reg(0x02, 0x06)
        self.write_reg(0x03, 0x47)
        self.write_reg(0x07, 0x04)
        self.write_reg(0x08, 0x05)
        self.write_reg(0x0A, 0x00)
        self.write_reg(0x0B, 0x06)
        self.write_reg(0x0C, 0x00)
        self.write_reg(0x0D, 0x10)
        self.write_reg(0x0E, 0xB1)
        self.write_reg(0x0F, 0x3B)
        self.write_reg(0x10, 0xF8)
        self.write_reg(0x11, 0x93)
        self.write_reg(0x12, 0x13)
        self.write_reg(0x13, 0x22)
        self.write_reg(0x14, 0xF8)
        self.write_reg(0x15, 0x26)
        self.write_reg(0x17, 0x30)
        self.write_reg(0x18, 0x18)
        self.write_reg(0x19, 0x16)
        self.write_reg(0x1A, 0x6C)
        self.write_reg(0x1B, 0x03)
        self.write_reg(0x1C, 0x40)
        self.write_reg(0x1D, 0x91)
        self.write_reg(0x20, 0xFB)
        self.write_reg(0x21, 0x56)
        self.write_reg(0x22, 0x17)
        self.write_reg(0x23, 0xE9)
        self.write_reg(0x24, 0x2A)
        self.write_reg(0x25, 0x00)
        self.write_reg(0x26, 0x1F)
        self.write_reg(0x2C, 0x81)
        self.write_reg(0x2D, 0x35)
        self.write_reg(0x2E, 0x09)
        self.write_reg(0x09, 0x00)
        self.write_reg(0x04, 0x7E)
        self.write_reg(0x05, 0x3C)

        patable = [0x00, 0x12, 0x0E, 0x34, 0x60, 0xC5, 0xC1, 0xC0]
        self.write_burst(0x7E, patable)

        self.write_strobe(0x31)
        self.write_strobe(0x36)
        self.write_strobe(0x3B)
        self.write_strobe(0x36)
        self.write_strobe(0x3A)

        time.sleep(136)

    def set_pin_output(self, pin, value):
        GPIO.output(pin, value)

    def write_reg(self, addr, val):
        self.spi_start()
        self._spi.xfer2([addr, val])
        return self.spi_end()

    def write_burst(self, addr, values):
        self.spi_start()
        self._spi.xfer2([addr] + values)
        self.spi_end()

    def write_strobe(self, addr):
        self.spi_start()
        self._spi.xfer2([addr])
        self.spi_end()

    def spi_start(self):
        self.set_pin_output(self._pin_ss, GPIO.LOW)
        while GPIO.input(self._pin_miso):
            pass

    def spi_end(self):
        self.set_pin_output(self._pin_ss, GPIO.HIGH)
        return GPIO.input(self._pin_miso)

    def crc16_2(self, buf, length):
        crc = 0xFFFF

        for pos in range(length):
            crc ^= buf[pos]
            for _ in range(8):
                if crc & 0x0001 != 0:
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1
        return crc

    def find_address(self, timeout):
        buf = [0] * 24

        if self.receive_packet(buf, timeout):
            address = self.parse_address(buf)
            return address

        return 0

    def send_command(self, cmd, addr=None, num_transmits=10):
        t = 0
        buf = [0] * 10

        if addr is None:
            addr = self._heater_addr

        buf[0] = 9
        buf[1] = cmd
        buf[2] = (addr >> 24) & 0xFF
        buf[3] = (addr >> 16) & 0xFF
        buf[4] = (addr >> 8) & 0xFF
        buf[5] = addr & 0xFF
        buf[6] = self._packet_seq
        buf[9] = 0

        crc = self.crc16_2(buf, 7)
        buf[7] = (crc >> 8) & 0xFF
        buf[8] = crc & 0xFF

        for _ in range(num_transmits):
            self.tx_burst(10, buf)
            t = time.time()
            while self.write_reg(0xF5, 0xFF) != 0x01:
                time.sleep(0.001)
                if time.time() - t > 0.1:
                    return

    def tx_burst(self, length, values):
        self.tx_flush()
        self._spi.xfer2([0x7F, length] + values)
        self.write_strobe(0x35)

    def tx_flush(self):
        self.write_strobe(0x36)
        self.write_strobe(0x3B)
        time.sleep(0.016)

    def rx_flush(self):
        self.write_strobe(0x36)
        self.write_reg(0xBF, 0xFF)
        self.write_strobe(0x3A)
        time.sleep(0.016)

    def rx_enable(self):
        self.write_strobe(0x34)

    def rx(self, length):
        return self._spi.xfer2([0xBF] * length)

    def receive_packet(self, bytes, timeout):
        t = time.time()
        rx_len = 0

        self.rx_flush()
        self.rx_enable()

        while True:
            if time.time() - t > timeout:
                return False

            while not GPIO.input(self._pin_gdo2):
                if time.time() - t > timeout:
                    return False

            rx_len = self.write_reg(0xFB, 0xFF)

            if rx_len == 24:
                break

            self.rx_flush()
            self.rx_enable()

        bytes[:rx_len] = self.rx(rx_len)

        self.rx_flush()

        crc = self.crc16_2(bytes, 19)
        if crc == (bytes[19] << 8) + bytes[20]:
            return True

        return False

    def parse_address(self, buf):
        address = 0
        address |= buf[2] << 24
        address |= buf[3] << 16
        address |= buf[4] << 8
        address |= buf[5]
        return address
    
    
# Użycie
# heater_rf = DieselHeaterRF(pin_sck=11, pin_mosi=10, pin_miso=9, pin_ss=8, pin_gdo2=7)
# found_address = heater_rf.find_address(timeout=5)  # Timeout w sekundach

# if found_address:
#     print(f"Znaleziono adres urządzenia: 0x{found_address:X}")
#     heater_rf.begin(heater_addr=found_address)
# else:
#     print("Nie udało się znaleźć adresu urządzenia.")    
