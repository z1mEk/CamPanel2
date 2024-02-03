# bluetooth_server.py
import bluetooth

server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

port = 1
server_socket.bind(("", port))
server_socket.listen(1)

print("Waiting for connection on RFCOMM channel", port)

client_socket, client_info = server_socket.accept()
print("Accepted connection from", client_info)

while True:
    data = client_socket.recv(1024)
    if not data:
        break
    print("Received:", data.decode("utf-8"))

client_socket.close()
server_socket.close()