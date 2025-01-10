Raspberry Pi Zero - 101
===

# Unboxing
> Model: [Raspberry Pi Zero 2 W](https://wiki.52pi.com/index.php?title=ER-0031)

## Prepare the OS installation + start
### HDMI + keyboard solution
> FAILED : Since I could not have any display through the HDMI, I used the SSH connection over Wi-Fi   

> _NOTE_ : apparently, the fix is in the config.txt file (see [manual](https://www.raspberrypi.com/documentation/computers/config_txt.html#hdmi-mode)) 

### SSH solution
> ACHIEVED

Prepare the micro SD card : https://www.youtube.com/watch?v=Hdm26W9dHK0
* define the Wi-Fi in the OS settings while preparing the OS image on the micro SD card
* define a local user for the Raspberry OS (_e.g._ `my_local_user`)

Run the board:
  * plug the Raspberry board
  * retrieve the Raspberry IP address
  * use Putty of Git Bash
    ```bash
    $ ssh my_local_user@192.168.0.40
    ```
where 
  * `my_local_user` being the user defined during OS preparation
  * `192.168.0.40` being the retrieved IP

 
### USB OTG solution
> The otg_mode is only for Raspberry Pi 4

See https://www.raspberrypi.com/documentation/computers/config_txt.html#hdmi-mode


## Configure the OS

### raspi-config

You may use the Raspberry Pi Software Configuration Tool

to fine tune few things such as 
* _System Options_:      Configure system settings
* _Display Options_:     Configure display settings
* _Interface Options_:    Configure connections to peripherals
* _Performance Options_:  Configure performance settings
* _Localisation Options_: Configure language and regional settings
* _Advanced Options_:     Configure advanced settings
* _Update_:               Update this tool to the latest version
* _About raspi-config_:   Information about this configuration tool

> Connect with SSH and run
>
>    ```bash
>    $ sudo raspi-config
>    ```

### OS upgrade  
> Connect with SSH and run
>
>    ```bash
>    $ sudo apt update
>    $ sudo apt full-upgrade
>    ```

### Handling extra modules
#### FTP server
To upload files on the Raspberry board, you may use FTP.

Connect with SSH and run:
>
> Install the FTP service:
>    ```bash
>    $ sudo apt install vsftpd
>    ```
> Launch the service
>    ```bash
>    $ sudo service vsftpd restart
>    ```

See https://www.youtube.com/watch?v=Kf1U1bG9d2A

You may now connect to the FTP server from your workstation to upload files on the Raspberry board

```bash
$  ftp 192.168.0.40
```

#### Removing packages 
To remove a package :
> 
> ```bash
> $ sudo apt remove <package>
> ```

### Using a USB key
To upload files on the Raspberry board, you may use a USB key.
> /!\ _Storage keys should be connected on the 2nd Micro USB ports on the board since the 1st on is dedicated to power supplying_ 
> See [Raspberry board hardware upgrading](#Raspberry board hardware upgrading)
> On Linux, storage devices must be mounted to be used. Try this tutorial https://www.youtube.com/watch?v=stqVx3uTBFA

# Adding executables 
## Python code
It appears python is enabled by default in the OS:

```bash
$ python --version
Python 3.11.2
```
You may then add python scripts.

Python scripts can be run in 2 different flavors:
* as python interpreter argument:
    ```bash
    $ python test.py
    ```
* as an executable file - to enable this you must
  1. add `#!/usr/bin/python` at the very first line of the script
  2. `chmod 755 test.py`
  3. now you may run the file 
>    ```bash
>    $ ./test.py
>    ```

To use pip you must install the package:
```bash
$ sudo apt install python3-pip -y
```
However, if you install packages at system level instead of a virtual env., 
pip will encourage you to use (see [PEP 668](https://peps.python.org/pep-0668/))

```bash
$ sudo apt install python3-<package>
```


## C code
It appears GCC is enabled by default in the OS:

```bash
$ gcc --version
gcc (Debian 12.2.0-14) 12.2.0
Copyright (C) 2022 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
```
### GPIO test
To handle the GPIO interface, there is a linux service to use. You may check its status through
```bash
$ sudo systemctl status pigpiod
```
A success should display something like
```
● pigpiod.service - Daemon required to control GPIO pins via pigpio
     Loaded: loaded (/lib/systemd/system/pigpiod.service; disabled; preset: enabled)
     Active: active (running) since Fri 2025-01-10 18:47:33 CET; 2s ago
    Process: 562 ExecStart=/usr/bin/pigpiod -l -p 8889 (code=exited, status=0/SUCCESS)
   Main PID: 563 (pigpiod)
      Tasks: 4 (limit: 178)
        CPU: 286ms
     CGroup: /system.slice/pigpiod.service
             └─563 /usr/bin/pigpiod -l -p 8889

Jan 10 18:47:33 raspberrypi systemd[1]: Starting pigpiod.service - Daemon required to control GPIO pins via pigpio...
Jan 10 18:47:33 raspberrypi systemd[1]: Started pigpiod.service - Daemon required to control GPIO pins via pigpio.
```
Otherwise you should start the service:

```bash
$ sudo systemctl start pigpiod
```
or even install it 
```bash
$ sudo apt update
$ sudo apt install pigpio
```

> To change the port at which the pigpio service listens to can be configured with
> `-p` option :
> ```
> [Service]
> ExecStart=/usr/bin/pigpiod -l -p 8889
> ```

The source code that demoes a blinking LED is available in [src/c/blink.c](src/c/blink.c).
To compile it, run
```bash
$ gcc -o blink blink.c -lpigpio -lpthread
```
Then use sudo to run the code:
```bash
$ sudo blink
```


# Raspberry board hardware upgrading

Here is a view of the Raspberry connectors:
```
+--------------------------------------------------+
|   : : : : : : : : : : : : : : : : : : : : (GPIO) |
|                                                  |
|  +-----+                                +------+ | 
|  | µSD |                                |micro | |
|  +-----+                                |camera| |
|                                         +------+ |
| <micro HDMI>     <micro USB #2> <micro USB #1>   |
+--------------------------------------------------+
```

## Interacting with GPIO 
> * see https://www.raspberrypi.com/documentation/computers/config_txt.html#hdmi-mode
> * see https://deusyss.developpez.com/tutoriels/RaspberryPi/PythonEtLeGpio/ :
![GPIO](https://deusyss.developpez.com/tutoriels/RaspberryPi/PythonEtLeGpio/images/1000020100000211000001252655A6BB.png)

### Prepare the hardware
* Sold pins grid
* You may then connect a [Breakout Board](https://github.com/Freenove/Freenove_Breakout_Board_for_Raspberry_Pi) 
  to prototype GPIO connections ![board](https://m.media-amazon.com/images/I/71-CenLprTL.jpg)

> You may use a [_breadboard_](https://www.youtube.com/watch?v=6WReFkfrUIk) to prototype your project

### Python script

> /!\ As per [this tuto](https://deusyss.developpez.com/tutoriels/RaspberryPi/PythonEtLeGpio/#LIII-A), you should install the package
> `python3-RPi.GPIO`. Unfortunately, GPIO input does not work and generates a RuntimeError
> ```
> Traceback (most recent call last):
>   File "/home/chris/./push_button.py", line 23, in <module>
>     GPIO.add_event_detect(pin_number, GPIO.BOTH, callback=button_callback, bouncetime=100)
> RuntimeError: Failed to add edge detection
> ```
> The fix is explained [here](https://raspberrypi.stackexchange.com/questions/147332/rpi-gpio-runtimeerror-failed-to-add-edge-detection).
> It requires python3-rpi-lgpio :
> ```bash
> $ sudo apt update
> $ sudo apt install python3-rpi-lgpio
> ```
> This could be linked with an issue mentionned in [RPi.GPIO2](https://pypi.org/project/RPi.GPIO2/):
> > RPi.GPIO requires non-standard kernel patches that expose the GPIO registers to userspace via a character device /dev/gpiomem. As this is not supported by the mainline Linux kernel, any distribution targeting Raspberry Pi devices running the mainline kernel will not be compatible with the RPi.GPIO library. As a large number of tutorials, especially those targeted at beginners, demonstrate use of the RPi's GPIO pins by including RPi.GPIO syntax, this incompatibility limits users to distributions build on a special downstream kernel maintained by the Rapberry Pi foundation. We would like to enable beginners on any Linux distribution by allowing them to follow easily available tutorials.
> 
> Therefore **_RPi.GPIO2 should then be installed_** 
> > _NOTE : both RPi.GPIO and RPi.GPIO2 experienced some issues while installing with PyCharm_

#### PIN powering 
* Source code: code sample to activate/deactivate the pin #18: [src/python/pin18_power_up.py](src/python/pin18_power_up.py)
* Hardware: 
  * if the Breakout Board is used, the LED should be turned on and off
  * otherwise here is a possible schema:
```
    +--[LED]--+
    |         |
    R1        |
    |         |
+---|---------|------------------------------------+
|   : : : : : : : : : : : : : : : : : : : : (GPIO) |
|                                                  |
|  +-----+                                +------+ | 
|  | µSD |                                |micro | |
|  +-----+                                |camera| |
```
    * The R1 resistor (100k) is connected to GPIO pin #2 (+5V)
    * the LED is connected to R1 and GPIO pin #18

#### PIN activation
> To detect if a button has been pressed, see https://www.youtube.com/watch?v=T67VfwiJPMg
The source code is in [src/python/push_button.py](src/python/push_button.py)

```
      +--[PB]---------------------------+
      |                                 |
      R1                                |
      |                                 |
+-----|---------------------------------|----------+
|   : : : : : : : : : : : : : : : : : : : : (GPIO) |
|                                                  |
|  +-----+                                +------+ | 
|  | µSD |                                |micro | |
|  +-----+                                |camera| |
```
    * The R1 resistor (100k) is connected to GPIO pin #34 (GND)
    * the PB (push button) is connected to R1 and GPIO pin #20

### C code
To do.

## Potentiometer reading - Interacting with ADS1115 External 16 Bit ADC
The purpose of this card is to convert an analog signal into a numeric value so that the value of a potentiometer.

Here is a sample on how to make it: 
* general info: https://docs.cirkitdesigner.com/component/a31888c7-8f98-4d81-5f3b-e5a17a61923e/adafruit-ads1115-16bit-i2c-adc
* schema: https://app.cirkitdesigner.com/project/2f7ffdde-d487-4cfe-a04c-324202820c3b


## Interacting with Bluetooth
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

```python
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
```

### Bluetooth Client Example

Here’s an example of a Bluetooth client that connects to the Raspberry Pi and sends data:

```python
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