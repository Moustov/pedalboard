Bluetooth on Raspberry Pi Zero 2W
===

To configure Bluetooth and share information with a Raspberry Pi Zero 2 W using Python, you'll typically use the **BlueZ** stack along with the **pybluez** library. Below are the steps to set up Bluetooth and share data.

### Prerequisites

1. **Update Your System**:
   ```bash
   sudo apt update
   sudo apt upgrade
   ```

2. **Install Required Packages**:
   ```bash
   sudo apt install python3-pip bluez python3-bluez
   pip3 install pybluez
   ```

### Setting Up Bluetooth

1. **Enable Bluetooth**:
   Make sure Bluetooth is enabled on your Raspberry Pi. You can check this using:
   ```bash
   sudo systemctl status bluetooth
   ```

> Here is a possible output
> ```
> $ sudo systemctl status bluetooth
> ● bluetooth.service - Bluetooth service
>      Loaded: loaded (/lib/systemd/system/bluetooth.service; enabled; preset: enabled)
>      Active: active (running) since Fri 2025-01-10 19:36:12 CET; 2h 3min ago
>        Docs: man:bluetoothd(8)
>    Main PID: 414 (bluetoothd)
>      Status: "Running"
>       Tasks: 1 (limit: 178)
>         CPU: 200ms
>      CGroup: /system.slice/bluetooth.service
>              └─414 /usr/libexec/bluetooth/bluetoothd
> 
> Jan 10 19:36:12 raspberrypi bluetoothd[414]: Starting SDP server
> Jan 10 19:36:12 raspberrypi bluetoothd[414]: profiles/audio/vcp.c:vcp_init() D-Bus experimental not enabled
> Jan 10 19:36:12 raspberrypi bluetoothd[414]: src/plugin.c:plugin_init() Failed to init vcp plugin
> Jan 10 19:36:12 raspberrypi bluetoothd[414]: profiles/audio/mcp.c:mcp_init() D-Bus experimental not enabled
> Jan 10 19:36:12 raspberrypi bluetoothd[414]: src/plugin.c:plugin_init() Failed to init mcp plugin
> Jan 10 19:36:12 raspberrypi bluetoothd[414]: profiles/audio/bap.c:bap_init() D-Bus experimental not enabled
> Jan 10 19:36:12 raspberrypi bluetoothd[414]: src/plugin.c:plugin_init() Failed to init bap plugin
> Jan 10 19:36:13 raspberrypi bluetoothd[414]: Bluetooth management interface 1.22 initialized
> Jan 10 19:36:13 raspberrypi bluetoothd[414]: profiles/sap/server.c:sap_server_register() Sap driver initialization failed.
> Jan 10 19:36:13 raspberrypi bluetoothd[414]: sap-server: Operation not permitted (1)
> ```
> The output shows that the Bluetooth service is active and running on your Raspberry Pi Zero 2 W, which is a good sign
> 
> Understanding the Messages:
> * D-Bus Experimental Not Enabled:
>        This indicates that certain Bluetooth profiles (like audio profiles) are not enabled because the D-Bus experimental feature is not turned on. This might not affect basic Bluetooth functionality, such as connecting devices and exchanging data.
> * Failed to Init Plugins:
>        The messages about failing to initialize plugins like vcp, mcp, and bap suggest that certain advanced features (like audio profiles) are not available due to the missing D-Bus support. Again, this may be irrelevant if you're primarily using Bluetooth for data transfer.>
> * Sap Driver Initialization Failed:
>        The sap-server message indicates that the SIM Access Profile (SAP) driver could not initialize, which is typically used for connecting to SIM cards over Bluetooth. This is generally not needed for most common Bluetooth applications.



   If it’s not running, start it with:
   ```bash
   sudo systemctl start bluetooth
   ```

2. **Pairing Devices**:
   You can pair your Raspberry Pi with another Bluetooth device using the Bluetooth manager or the command line.

   To use the command line:
   ```bash
   bluetoothctl
   ```

   Inside the `bluetoothctl` prompt, you can use commands like:
   - `power on` to turn on the Bluetooth.
   - `scan on` to start scanning for devices.
   - `pair <MAC_ADDRESS>` to pair with a device.
   - `connect <MAC_ADDRESS>` to connect.

### Python Script Example

Here’s a simple example to create a Bluetooth server that listens for connections and sends a message:

#### Bluetooth Server (Raspberry Pi)
See [src/python/raspberry/bluetooth_server.py](src/python/raspberry/bluetooth_server.py)

### Bluetooth Client Example
Here’s an example of a Bluetooth client that connects to the Raspberry Pi and sends data:
See [src/python/raspberry/bluetooth_client.py](src/python/raspberry/bluetooth_client.py)
```

### Running the Scripts

1. **Run the Server**:
   - Save the server code on your Raspberry Pi and run it:
   ```bash
   python3 bluetooth_server.py
   ```

2. **Run the Client**:
   - Save the client code on another device (like a laptop or smartphone) and run it after the server is running.

### Conclusion

These examples demonstrate how to set up Bluetooth communication between a Raspberry Pi Zero 2 W and another device. You can modify the scripts to handle more complex data exchanges as needed. If you have any questions or need further assistance, feel free to ask!