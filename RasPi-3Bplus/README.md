**Requirements**

* A Raspberry Pi 3B+ (a 4 may also work but I haven't tested it) running Raspbian Bullseye patched wth the [Nexmon patches](https://github.com/seemoo-lab/nexmon)
* An additional USB wifi adapter to enable the RPi to be able to have internet access while the built-in wifi is set to monitor mode for wifi sensing.

**Basic Apprach**

* At boot, get the onboard wifi chip (wlan0 in the code) into monitor mode with some reasonable (although probably wrong) default configurations.  (see /miscfiles/start_nexmon.sh)
* Let NetworkManager handle connecting to whatever wifi you want to use as your baseline (wlan1 usually)
* Run this script, wait for wifi on wlan1 to work, reconfigure nexmon for that network
* Monitor chosen network on wlan0, and report findings via MQTT on wlan1 (this conveniently generates more traffic to analyze)

**Inspirations**

* [This Hackster project](https://www.hackster.io/mzakharo/wifi-sensing-via-raspberry-pi-ff1087)
* [Plotly page on data smoothing](https://plotly.com/python/smoothing)
* [Another page on data smoothing](https://pieriantraining.com/python-smoothing-data-a-comprehensive-guide)

