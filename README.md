# SW Checkin

This python script checks your flight reservation with Southwest and then checks you in at exactly 24 hours before your flight.  Queue up the script and it will `sleep` until the earliest possible check-in time.

## Contributors
<a href="https://github.com/ilikerolls/SouthwestCheckin_UI/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=ilikerolls/SouthwestCheckin_UI" />
</a>

## Requirements

This script can either be ran directly on your host or within Docker.

### Host

* Python (should work with 2.x or 3.x thanks to @ratabora)
* [pip](https://pypi.python.org/pypi/pip)

### Docker

* Docker (tested with 1.12.6)

## Setup

### Host

#### Install Base Package Requirements

```bash
$ pip install -r requirements.txt
```

#### Usage

```bash
$ python ./checkin.py CONFIRMATION_NUMBER FIRST_NAME LAST_NAME
```

### Windows GUI
#### Usage

```bash
Double Click SouthWest_Checkin_UI.pyw to open GUI

or from command line 

$ pythonw ./SouthWest_Checkin_UI.pyw
```

### Docker

#### Usage

```bash
$ sudo docker run -it pyro2927/southwestcheckin:latest CONFIRMATION_NUMBER FIRST_NAME LAST_NAME
```
