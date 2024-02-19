import os
import pty
import serial
import threading

class SerialSimulator:
    def __init__(self, baudrate=9600):
        self.master, self.slave = pty.openpty()
        self.port = os.ttyname(self.slave)
        self.baudrate = baudrate
        self.serial = serial.Serial()
        self.serial.port = self.port
        self.serial.baudrate = baudrate
        self.serial.timeout = 0  # Ustaw timeout na zero, aby odbieranie danych było nieblokujące
        self.thread_stop = False
        self.received_buffer = b""  # Bufor do przechowywania odebranych danych

    def start(self):
        self.serial.open()
        print("Symulowane urządzenie dostępne pod portem:", self.port)
        self.thread = threading.Thread(target=self._listen)
        self.thread.start()

    def _listen(self):
        while not self.thread_stop:
            try:
                # Odbieranie danych od klienta
                received_data = self.serial.read(1024)  # Odbierz maksymalnie 1024 bajtów
                if received_data:
                    self.received_buffer += received_data
                    # Sprawdź, czy odebrano wystarczającą ilość danych do przetworzenia
                    while b"\n" in self.received_buffer:
                        message, self.received_buffer = self.received_buffer.split(b"\n", 1)
                        message = message.strip().decode()
                        print("Received from client:", message)
                        # Tutaj możesz dodać odpowiedź na odebraną wiadomość
                        response = "Odpowiedź na: " + message
                        self.serial.write(response.encode() + b'\n')
            except serial.SerialException:
                pass

            # Odbieranie danych od wirtualnego urządzenia
            if os.read(self.master, 1000):
                received_data = os.read(self.master, 1000).decode().strip()
                print("Received from device:", received_data)

    def stop(self):
        self.thread_stop = True
        self.thread.join()
        self.serial.close()

if __name__ == "__main__":
    sim = SerialSimulator()
    sim.start()

    try:
        while True:
            # Tutaj możesz oczekiwać na wejście z klawiatury i wysyłać je do urządzenia
            user_input = input("Wyslij wiadomosc: ")
            sim.serial.write(user_input.encode() + b'\n')
    except KeyboardInterrupt:
        sim.stop()
