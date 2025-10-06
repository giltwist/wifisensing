#!/bin/bash

sudo ip link set wlan1 down
sudo iw wlan1 set monitor none
sudo ip link set wlan1 up
