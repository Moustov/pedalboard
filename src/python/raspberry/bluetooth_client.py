import bluetooth

def main():
    target_name = "Your_Raspberry_Pi_Name"
    target_address = None

    # Discover devices
    nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True)

    for addr, name in nearby_devices:
        if target_name == name:
            target_address = addr
            break

    if target_address is not None:
        print("Found target Bluetooth device with address:", target_address)
    else:
        print("Could not find target Bluetooth device.")
        return

    # Create a Bluetooth socket
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    # Connect to the Raspberry Pi
    sock.connect((target_address, 1))

    try:
        message = "Hello, Raspberry Pi!"
        sock.send(message)
        print("Sent:", message)
    finally:
        sock.close()

if __name__ == "__main__":
    main()