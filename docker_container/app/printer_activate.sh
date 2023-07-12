#usr/bin/bash

command=$1

port=$2

sudo echo $command > /sys/bus/usb/drivers/usb/$port/authorized