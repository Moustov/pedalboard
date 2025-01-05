Raspberry Pi Zero - 101
===

# Unboxing
> Model: [Raspberry Pi Zero 2 W](https://wiki.52pi.com/index.php?title=ER-0031)

## Prepare the OS installation
> Since I could not have any display through the HDMI, I used the SSH connection over Wi-Fi   
* Prepare the micro SD card : https://www.youtube.com/watch?v=Hdm26W9dHK0
  * define the Wi-Fi in the OS settings while preparing the OS image on the micro SD card
  * define a local user for the Raspberry OS (_e.g._ `my_local_user`)
 
## Run the board
  * plug the Raspberry board
  * retrieve the Raspberry IP address
  * use Putty of Git Bash
    ```bash
    $ ssh my_local_user@192.168.0.40
    ```
where 
  * `my_local_user` being the user defined during OS preparation
  * `192.168.0.40` being the retrieved IP

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
> see https://deusyss.developpez.com/tutoriels/RaspberryPi/PythonEtLeGpio/ :
![GPIO](https://deusyss.developpez.com/tutoriels/RaspberryPi/PythonEtLeGpio/images/1000020100000211000001252655A6BB.png)

### Prepare the hardware
* Sold pins grid
* You may then connect a Breakout Board to prototype GPIO connections ![board](https://m.media-amazon.com/images/I/71-CenLprTL.jpg)

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



