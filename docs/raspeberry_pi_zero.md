Raspberry Pi Zero - 101
===

# Unboxing
> Model: [Raspberry Pi Zero 2 W](https://wiki.52pi.com/index.php?title=ER-0031)

## Prepare the hardware
* Sold pins grid
  > Since I could not have any display through the HDMI, I used the SSH connection over Wi-Fi   

## Prepare the OS installation
* Prepare the micro SD card : https://www.youtube.com/watch?v=Hdm26W9dHK0
  * define the Wi-Fi in the OS settings while preparing the OS image on the micro SD card
  * define a local user for the Raspberry OS
 
## Run the board
  * plug the Raspberry board
  * retrieve the Raspberry IP address
  * use Putty of Git Bash
    ```bash
    $ ssh chris@192.168.0.40
    ```
where 
  * `chris` being the user defined during OS preparation
  * `192.168.0.40` being the IP provided at OS starting (DHCP)

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

### Adding extra modules
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

### Using a USB key
To upload files on the Raspberry board, you may use a USB key.
> /!\ Storage keys should be connected on the 2nd Micro USB ports on the board since the 1st on is dedicated to power supplying 

> On Linux, storage devices must be mounted to be used. Try this tutorial https://www.youtube.com/watch?v=stqVx3uTBFA

# Adding python code
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


# Raspberry board hardware upgrading

