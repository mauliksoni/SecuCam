#!/bin/sh
# dirwatchlauncher.sh
# navigate to home directory then to the directory then execute python script then back home

cd /
cd home/pi/PiCam/secucam
sudo python FileWalk.py
cd /
