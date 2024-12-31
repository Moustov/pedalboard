Pedalboard project
===

# Configuration
Based on [MinGW v2.0.0](https://www.mingw-w64.org/downloads/)
* Download the [w64devkit-x64](https://github.com/skeeto/w64devkit/releases/download/v2.0.0/w64devkit-x64-2.0.0.exe)
* Run the install EXE
* Redefine the PATH to include the bin
Example with "Git Bash" and the dev kit installed under c:\w64devkit
```shell
$ PATH=$PATH:/c/w64devkit/bin
```


# How to build
To build the [helloworld.c](test/helloworld.c), run
```shell
$ /c/w64devkit/bin/cc.exe -o tests/helloworld tests/helloworld.c
```
This will create the file "helloworld.exe". You may then run `helloworld.exe`
```shell
$ helloworld.exe
```