#standard imports
import socket
import struct
import time, datetime
import numpy as np
import json
from collections import deque

#For automating Nexmon calls
import subprocess
import re
import threading

#The data structure was useful, but I bet there are better import choices
from influxdb_client import Point, WritePrecision

class RX():

    def __init__(self, mqttClient=None, log=None, poll=None):
        # Generic inits
        self.UDP_IP = "0.0.0.0"
        self.UDP_PORT = 5500
        self.SO_TIMESTAMPNS = 35
        self.SOF_TIMESTAMPING_RX_SOFTWARE = (1 << 3)
        self.fx64 = np.ones(64, dtype=bool)
        self.fx64[:6] = False
        self.fx64[64*1-5:] = False
        self.fx64[32] = False
        self.deck = deque(maxlen=100)

        # Inits useful to my specific use case, note the mqttClient Param
        self.active = False
        self.status="Initializing"
        self.MQTT_CLIENT_ID = 'wifi_sensing'
        self.client = mqttClient

        # Await wifi connection, probably on wlan1 if you are using an external USB
        while subprocess.check_output(['iwgetid','-r'])=="\n":
            print("Awaiting WIFI")
            time.sleep(1)

        # Set up Nexmon with actual correct parameters based on connected wifi
        device=subprocess.check_output(['iwgetid'])
        device=device.split()[0].decode('utf-8')
        print("Connected with " + device)
        iwInfo=subprocess.check_output(['iw', device, 'link'])
        self.CHOSEN_AP=re.search("([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})", iwInfo.decode('utf-8')).group(0)
        print("Conntected to " + self.CHOSEN_AP)
        iwRes=subprocess.check_output(['iw',device,'info']);
        channel=re.search("(channel) (.)",iwRes.decode('utf-8')).group(2)
        csiParam=subprocess.check_output(['makecsiparams', '-c', channel+'/20', '-C', '1', '-N', '1']).decode('utf-8')
        print(f"{channel} | {csiParam}")
        subprocess.call(['nexutil', '-Iwlan0', '-s500', '-b', '-l34', '-v'+csiParam])

        # Set up the reception of CSI data
        self.r = None
        r = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        r.setsockopt(socket.SOL_SOCKET, self.SO_TIMESTAMPNS, self.SOF_TIMESTAMPING_RX_SOFTWARE)
        r.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.r = r
        r.bind((self.UDP_IP, self.UDP_PORT))
        self.fd = r.fileno()
        self.prev = None
        self.send_buf = []
        self.ws_thread = threading.Thread(target=self.recv)
        self.ws_thread.daemon = True
        self.ws_thread.start()

    def recv(self):
        print("Activating wifi sensing receiver")
        cnt = 0
        while True:
            try:
                data, ancdata, _, _ = self.r.recvmsg(4096, 128)
            except socket.timeout:
                continue
            if len(data) < 18:
                print("rx: packet too small")
                continue
            s, ns = struct.unpack('LL', ancdata[0][2])
            ts = s * 10**9 + ns
            self.process(data, ts)
            cnt +=1
            if self.active==True:
                #print('# of devices detected', cnt)
                cnt = 0
                self.publish(self.send_buf)
                self.send_buf.clear()

    def process(self, raw, ts):
        self.ver, mask, rssi, fc, mac, _seq, conf, chanspec, chip = struct.unpack('<BBbB6sHHHH',raw[:18])
        seq = _seq >> 4
        mac_str = mac.hex(':')
        count = (len(raw) - 18) // 2
        data = np.frombuffer(raw, dtype='<h', count=count, offset=18).astype(np.float32).view(np.complex64)
        #appears to be 256 on newer wifi protocols, can break this
        assert len(data) == 64, f"Data of {len(data)} is not expected"
        pl = data[self.fx64]

        ######simple filter for broken chunks
        x = pl.reshape((4,-1))
        mn = np.mean(np.abs(x), axis=-1)
        msk = np.zeros(mn.shape, dtype=bool)
        msk[np.argmax(mn)] = True
        pl  = x[msk]
        pl = pl.ravel()
        v = np.abs(pl)
        maxv = np.max(v)
        if maxv != 0:
            v /= maxv

        if self.prev is not None:
            motion = (np.corrcoef(v, self.prev)[0][1])**2
            motion = -10 * motion + 10
            self.send_buf.append(dict(time=ts, motion=motion, rssi=rssi,mac=mac_str, seq=seq))
        self.prev = v

    def publish(self, buf):

        points = []
        old_rssi=0.0
        old_time=0.0
        for b in buf:
            for key in ['rssi']:
                point = Point("wifi") \
                .field(key, b[key]) \
                .tag("mac", b['mac']) \
                .time(b['time'],WritePrecision.NS)
                points.append(point)
                if b['mac']==self.CHOSEN_AP:
                    cur_rssi=max(min((100.0+2.0*(b['rssi'])+30.0)/100.0,1.0),0.0)
                    cur_time=b['time'];
                    if cur_time-old_time>1:
                        self.track(cur_rssi)

                        old_time = cur_time

    def track(self,rssi):
        #this is how the rest of my use case knows what to do, replace for your use case
        self.client.publish("wifi-sensing/rssi",rssi)

        if len(self.deck)>10:
            self.status="Active" 
        else:
            print(f'Baselining {len(self.deck)*10}% complete')
            self.status=f'Baselining {len(self.deck)*10}% complete'
        self.deck.append(rssi)


    #Helper functions for my specific use case
    def start(self):
        self.active=True
    def stop(self):
        self.active=False
    def getStatus(self):
        return self.status
    def getDeck(self):
        return self.deck
    def close(self):
        self.r.close()


if __name__ == '__main__':
    rx = RX()
    rx.recv()
