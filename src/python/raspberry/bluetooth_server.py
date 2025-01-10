import bluetooth


def main():
    # Create a Bluetooth socket
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    port = 1
    server_sock.bind(("", port))
    server_sock.listen(1)

    print("Waiting for connection on RFCOMM channel %d" % port)

    # Accept a connection
    client_sock, client_info = server_sock.accept()
    print("Accepted connection from ", client_info)

    try:
        while True:
            data = client_sock.recv(1024)
            if not data:
                break
            print("Received: %s" % data.decode())

            # Send a response
            response = "Hello from Raspberry Pi!"
            client_sock.send(response.encode())
    except OSError:
        pass

    print("Disconnected.")
    client_sock.close()
    server_sock.close()


if __name__ == "__main__":
    main()