#! /usr/bin/python

import bluetooth
import uuid

server_socket = bluetooth.BluetoothSocket( bluetooth.RFCOMM )

port = 1
server_socket.bind(("",port))
server_socket.listen(1)

uuID = 99

bluetooth.advertise_service( server_socket, "test", service_id=uuID )

client_socket, client_address = server_socket.accept()
print(client_socket)
print(client_address)