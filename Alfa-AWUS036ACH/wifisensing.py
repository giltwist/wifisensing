# Adapted from https://github.com/cb-314/scapy-rssi/tree/master

import scapy.all as sca
from scapy.all import sniff
import struct
import datetime

def packet_callback(pkt):

    radiotap_formats = {"TSFT":"Q", "Flags":"B", "Rate":"B",
      "Channel":"HH", "FHSS":"BB", "dBm_AntSignal":"b", "dBm_AntNoise":"b",
      "Lock_Quality":"H", "TX_Attenuation":"H", "dB_TX_Attenuation":"H",
      "dBm_TX_Power":"b", "Antenna":"B",  "dB_AntSignal":"B",
      "dB_AntNoise":"B", "b14":"H", "b15":"B", "b16":"B", "b17":"B", "b18":"B",
      "b19":"BBB", "b20":"LHBB", "b21":"HBBBBBH", "b22":"B", "b23":"B",
      "b24":"B", "b25":"B", "b26":"B", "b27":"B", "b28":"B", "b29":"B",
      "b30":"B", "Ext":"B"}

    #print(pkt.layers)
    
        # check available Radiotap fields
    report="-----\n"
    #print(f"Available Radiotap fields: {pkt.present.flagrepr().split('+')}")
    if pkt.haslayer(sca.Dot11Beacon):
        if pkt['Dot11Beacon'].timestamp is not None:
                report+=f"Sent: {pkt['Dot11Beacon'].timestamp}\n"
                report+=f"Received: {pkt.time}\n"
    
    if pkt.haslayer(sca.Dot11):
        if pkt.addr2 is not None:
                report+=f"MAC: {pkt.addr2} "
    if pkt.haslayer(sca.Dot11Elt):
        if pkt['Dot11Elt'].info is not None and pkt['Dot11Elt'].info != b'':
            report+= f"({pkt['Dot11Elt'].info.decode("utf-8")}) "
    if pkt.haslayer(sca.RadioTap):
        if pkt.dBm_AntSignal is not None:
                report+=f"RSSI: {pkt.dBm_AntSignal} \n"
    report+=f"Antenna Readings: {struct.unpack('<bbbb',pkt.notdecoded)}"
    print(report)

# Start sniffing packets
sniff(prn=packet_callback, count=1, iface="wlan1")
