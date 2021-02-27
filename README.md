# RadioClub EIT - Automated Weather Satellite Ground Station GNURadio

Based on [wx-ground-station](https://git.radio.clubs.etsit.upm.es/Meteor-automated/wx-ground-station) but now it uses GNURadio for signal processing.

*Automated Weather Satelite Ground Station*. Automates the reception of weather satellites on Linux using [GNURadio](https://www.gnuradio.org/). It uses [SoapyRemote](https://github.com/pothosware/SoapyRemote/wiki) in order to connect to a remote SDR.

Features:
* Powered by bash, python3, [GNURadio](https://www.gnuradio.org/), [orbit-predictor](https://github.com/satellogic/orbit-predictor), [wxtoimg](https://wxtoimgrestored.xyz), [meteor_decoder](https://github.com/artlav/meteor_decoder), [SoapyRemote](https://github.com/pothosware/SoapyRemote/wiki), [gr-doppler](https://github.com/acien101/gr-doppler), [gr-satellites](https://github.com/daniestevez/gr-satellites) and Linux (Ubuntu and Debian tested).
* Works with **NOAA 18**, **NOAA 19**, **NOAA 15** and **METEOR-M 2**
* Doppler correction
* Radio reception through [SoapyRemote](https://github.com/pothosware/SoapyRemote/wiki). Allows to multiple users to use the sdr at the same time.
* Upload wav, iq and images to a **FTP** Server.

## Dependencies (Mainly for Linux)

### Some linux dependencies

```
$ sudo apt-get install autoconf
$ sudo apt-get install cmake
$ sudo apt-get install sox
$ sudo apt-get install at
$ sudo apt-get install libncurses5-dev libncursesw5-dev
$ sudo apt-get install imagemagick
$ sudo apt-get install telnet
```

### GNURadio

[Here a guide of how to install GNURadio](https://wiki.gnuradio.org/index.php/InstallingGR)

### SoapyRemote

[Here a guide of how to install SoapyRemote](https://github.com/pothosware/SoapyRemote/wiki)

### gr-satellites

[Here the docs of how to install gr-satellites](https://gr-satellites.readthedocs.io/en/latest/installation_intro.html)

### gr-doppler

```bash
$ pip install orbit-predictor
$ git clone https://github.com/acien101/gr-doppler.git
$ cd gr-doppler
$ mkdir build
$ cd build
$ cmake ../
$ make
$ sudo make install
```

### Wxtoimg

[Link](https://wxtoimgrestored.xyz)

```
$ wget https://wxtoimgrestored.xyz/beta/wxtoimg-amd64-2.11.2-beta.deb
$ sudo dpkg -i wxtoimg-amd64-2.11.2-beta.deb
```

### meteor_decoder

[Link](https://github.com/artlav/meteor_decoder)

```
$ sudo apt-get fpc
$ git clone https://github.com/artlav/meteor_decoder
$ cd meteor_decoder
$ source build_medet.sh
$ sudo cp medet /usr/bin
```

### orbit_predictor

[Link](https://github.com/satellogic/orbit-predictor)

This project calculate satellite orbit with python3 using [orbit-predictor](https://github.com/satellogic/orbit-predictor). You can create a virtualenv (recommended) or use python3 with pip3.

```
sudo apt-get install python3-pip
pip3 install orbit-predictor
```

## Install

### Setup environment variables
Complete environment variables on `.venv` with your station data. Export them or put it on `~/.bashrc` for example. Make environment variables efective with `source ~/.bashrc`

### Configure wxtoimg

Write the next variables under ` ~/.wxtoimgrc`. Here is an example `.wxtoimgrc`.

```
Latitude: 40.438
Longitude: -3.708
Altitude: 666.0
```

### Configure project

Execute `configure.sh`. The `configure.sh` script sets the installation directory in the scripts and schedules a cron job to run the satellite pass scheduler job at midnight every night.


## How it works

Powered by **bash** this program calculate the satellites orbit with python3 and [orbit-predictor](https://github.com/satellogic/orbit-predictor). It schedules the radio record and the antenna positioning when its passing with `schedule_all.sh`. On `receive_satellite.sh` it is executed the GNURadio flowchart for the signal demodulation. Then the signal is decoded with [wxtoimg](https://wxtoimgrestored.xyz) and upload the results to a *FTP Server*.


Everyday the next pipeline is executed:
* `schedule_all.sh` Starts the pipeline with the supported satellites. Calculate when the pass is starting and finishing and then it schedule `receive_satellite.sh` passing the timeout in args.
* `receive_satellite.sh` Connect to soapyremote server the amount time specified on arg (timeout). The GNURadio flowchart is executed for demodulation and signal process. Then `decode_satellite.sh` is executed.
* `decode_satellite.sh` Use [wxtoimg](https://wxtoimgrestored.xyz) to decode NOAA images. Then `upload.sh` is executed
* `upload.sh` Upload the results to a FTP Server.
