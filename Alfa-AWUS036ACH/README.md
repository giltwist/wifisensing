**About:**

My previous explorations with the Raspberry Pi 3B+ had some limitations:

* The hardware required a kernel patch to do monitor mode
* The hardware had only a single antenna
* The software was strongly tied to an IoT device I made for a class

This exploration is, consequently, about:

* Using a device that can do monitor mode mostly out-of-the box.  Note that you may need to install an appropriate driver (such as https://github.com/lwfinger/rtw88 or https://github.com/aircrack-ng/rtl8812au.git ... see also https://store.rokland.com/pages/alfa-wireless-adapters-monitor-mode-help-linux)
* Using a device with two antennas to do basic direction and possibly range inference.  Note that this setup is not built to handle reflections/echos let alone intentional obfuscation.

Ideally, I'd like to put this code on a little ROS-powered robot that I have for fox-hunting purposes.

**More Reading on CSI Obfuscation:**

* https://www.sciencedirect.com/science/article/abs/pii/S0140366421004916
* https://www.sciencedirect.com/science/article/abs/pii/S1389128625001768
