
# OpenFDBM
#### An Open Source FDBM Project

OpenFDBM is an project that is an Open Source project that is aimed for developing Frequency Domain Binaural Model (FDBM) which everyone could contribute and make a improvement to the existing model and application.

OpenFDBM runs on python3 and uses flask as the package for webserver , the webserve is used to serve API to control the FDBM state on the system.
Mobile application to control the FDBM is also provided, albeit still in the early development stage

Table of contents
=================

<!--ts-->
   * [Table of contents](#table-of-contents)
   * [Getting Started](#getting-started)
   * [Prerequisites](#prerequisites)
      * [Hardware List](#hardware-list)
      * [Software List](#software-list)
   * [Installation](#installation)
   * [Dependency](#dependency)
<!--te-->


## Getting Started

Thi instruction wlll help you to assemble the component (both software and hardware) needed to get the application up and running. All setup is based on the submitted paper titled *Open-Source Raspberry Pi Hearing Assistance Device with Consumer Hardware*

## Prerequisites
Please make sure you have met the minimum requirement to run OpenFDBM as listed below:

- Running Raspbian on the Raspberry pi zero (at the time of writing , the latest release is [raspbian stretch](
https://www.raspberrypi.org/downloads/raspbian/)).
- If using mobile application, minimum of android version 6.0
- Both Raspberry pi zero and Mobile Phone is connected to the same network.

Below is the list of Hardware and Software used in the project,

### Hardware list

Below is the hardware used in this Project:

-   [Andrea Binaural Microphone (25.82$)](https://www.amazon.com/Andrea-Communications-Surround-Recording-SB-205B/dp/B005GAW69M/ref=sr_1_1?ie=UTF8&qid=1526779842&sr=8-1&keywords=andrea+binaural+microphone)
-   [Raspberry Pi Zero W (10.00$)](https://www.adafruit.com/product/3400)
-   [8gb sd card (11.99$)](https://www.amazon.com/SanDisk-MicroSDHC-Standard-Packaging-SDSDQUAN-008G-G4A/dp/B00M55C0VU/ref=sr_1_3?s=electronics&ie=UTF8&qid=1527100932&sr=1-3&keywords=sandisk+micro+sd+card+8gb+class+10)
-   [LiPo Shim, Step-Up DC-DC Converter (9.95$)](https://www.adafruit.com/product/3196)
-   [Lithium Polymer Battery (3.7V; 1300mAh) (7.99$)](https://www.aliexpress.com/item/3-7V-1200mah-902360-Lithium-Polymer-LiPo-Rechargeable-Battery-For-Mp3-MP4-MP5-DVD-PAD-mobile/32295854525.html?spm=a2g0s.9042311.0.0.27424c4dwYLysm)
-   [lipoly charger (6.95$)](https://www.adafruit.com/product/1905)

The total cost of all the hardwqare used is around **72.7$ USD**.

![enter image description here](https://raw.githubusercontent.com/shiinoandra/OpenFDBM/master/hardwares.png)

Please do note that the above hardware is not compulsory, meaning that you can replace it with alternative hardware as long as it have the same specification and/or function.
the hardware listed above is merely a reference of the hardware that we used in the project as written in the paper.

### Software List



The requirement of the application and package to run OpenFDBM is as listed below :
-	alsaaudio package
-	sounddevice package
-	portaudio19 package
- Python 3
- Python 3 NumPy Package
- Python 3 SciPy Package
- Python 3 Matplotlib Pacakge
- Python 3 Flask Package

## Installation
Below is the detailed instruction how to setup your system and get it running.

### Installing Raspbian
1. Download the raspbian image from link below :
	[Raspbian Image Download](https://www.raspberrypi.org/downloads/raspbian/)
	Choose Raspbian Stretch Lite:  Minimal image based on Debian Stretch.

2.	On the host computer, insert microsd card and copy the raspbian image into the sdcard using the dd command

	```
    sudo dd bs=4MB if=./<name of the img>.img of=/dev/sdb
    ```
3. Unplug the microsd and plug it into the Raspberry pi zero, turn on the power of the raspberry pi zero

### Connecting to The Raspberry Pi
1. On the host computer  try to connect to the raspberry using ssh
	```
	ssh pi@<raspberry pi IP address>
	```
	the default password is "raspberry" without quote.
	if you have problem detecting the Ip address of the newly connected raspberry pi you could use nmap utilitiy 					on linux to search for its ip address
	```
	nmap -p 22 <your hostname>
2.	Once you are connected to the raspberry pi update the package list to ensure that it has the newest package list
	```
	sudo apt-get update
	sudo apt-get upgrade
	```

### Installing the Required Application and Package
1.	Using apt ,, install all the required package with the command below :
	```
	sudo apt-get install python3-pip python-pip
	sudo apt-get install python3-numpy python-numpy
	sudo apt-get install python3-scipy python-scipy
	sudo apt-get install python3-matplotlib python-matplotlib
	sudo apt-get install python3-flask
	sudo pip3 install --upgrade pip
	sudo pip install --upgrade pip
	sudo apt-get install portaudio19-dev
	sudo apt-get install python3-cffi python-cffi
	sudo pip3 install sounddevice
	sudo pip install sounddevice
	sudo pip3 install pyalsaaudio
	sudo apt-get install python-alsaaudio
	```
2.	Optionally you could also install tmux to enable the program run in a different terminal simulaneously

	```
	sudo apt-get install tmux
	```

### Checking the Sound Device
To ensure that the audio device works correctly, check the soundcard with the following command:
```
python3 -m sounddevice
```
it will give you the status of the input and output used by the soundcard as the example below:
```
0 bcm2835 ALSA: - (hw:0,0), ALSA (0 in, 2 out)

1 bcm2835 ALSA: IEC958/HDMI (hw:0,1), ALSA (0 in, 2 out)

> 2 Andrea SuperBeam USB Headset: Audio (hw:1,0), ALSA (2 in, 2 out)

3 sysdefault, ALSA (0 in, 128 out)

< 4 default, ALSA (0 in, 128 out)

5 dmix, ALSA (0 in, 2 out)
````
In the example above the Andrea SuperBeam USB Headset is being used as the input device where the default ALSA driver is being used as the output device.

## Running The System

To run the system simply use the python command to run the online_FDBM.py file
```
python3 online_FDBM.py
```

when the application is running it will display a message like below:
```
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```
the defauit port for the application is 5000 which you could freely change in the code.

the next step is to plug into the input and output port of the andrea USB dac, the sound from the input will be then fed into the FDBM system.


## Web API

The underlying control for the OpenFDBM is all based on http communication to the Flask server on the application. The http API allows users to create their own application and expand the application of the OpenFDBM to be more flexible.

The command list for the Web API is listed below:

### Checking Connection
This command is used to check whether the server is accessible or not
```
http://<ip address>:<port>/test_connection
```
If the connection is successful the server will return JSON data with ok status
```
{"status": "ok"}
```
### Changing to Front Direction

This command is used to change the FDBM operation mode to front mode, in this mode the FDBM will pick up the sound from the front direction

```
http://<ip address>:<port>/front
```

### Changing to Left Direction

This command is used to change the FDBM operation mode to left mode, in this mode the FDBM will pick up the sound from the left direction

```
http://<ip address>:<port>/left
```

### Changing to Right Direction

This command is used to change the FDBM operation mode to right mode, in this mode the FDBM will pick up the sound from the right direction

```
http://<ip address>:<port>/right
```
## Android Application

We have build and android application to control the OpenFDBM system from the mobile phone.
As for now the application is ony available for android platform. You can also find the source code for it in the "Andoid Application"  folder.

 The application is build using ionic framework and angularJS.

If you want to directly install the application just simply download the **openfdbm.apk** and install it.
if you want to build it yourself from the source code, there is several prerequisites that you must install prior building it. below is the list of the required application.

 - NodeJS
 - npm
 - Ionic
 - Cordova



Please refer to the below link for the guide on how to install each application as it is outside the scope of  the current article.

[Installing NodeJS and npm](https://nodejs.org/en/download/package-manager)
[Installing Ionic (and Cordova)](https://ionicframework.com/docs/v1/guide/installation.html)

Once you have installed all the prerequisites , you could build the application using command below from terminal:
```
ionic cordova build --release android
```
don't forget to sign the output apk after building. For more information, please refer to the link below:
[Publishing Ionic App](https://ionicframework.com/docs/v1/guide/publishing.html)



## Authors

 - Irwansyah
 - Muhammad Bagus Andra
 - Tsuyoshi Usagawa

Human Interface Cybernetic Computation Lab.
Kumamoto University

## License
The OpenFDBM is Licensed under Apache 2.0 License, please refer to the LICENSE.md for more information

## Acknowledgments

if you use a part or the whole system in your work please cite our work below

> Irwansyah, Muhammad Bagus Andra, Tsuyoshi Usagawa, "Open-Source
> Raspberry Pi Hearing Assistance Device with Consumer Hardware, in
> submission process, 2018)
