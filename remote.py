import sys
import serial
import websocket
import json
import time

#stty -F /dev/ttyACM0 cs8 115200 -ignbrk -brkint -imaxbel -opost -onlcr -isig -icanon -iexten -echo -echoe -echok -echoctl -echoke noflsh -ixon -crtscts

SERIALPORT = "/dev/ttyACM0"
ser = serial.serial_for_url(SERIALPORT, timeout=1, do_not_open=True)
ser.baudrate = 115200
ser.bytesize = 8
ser.parity = "N"
ser.stopbits = 1
ser.xonxoff = False
ser.rtscts = False

configuration = {
    "RC5": {
        "0x10": {
            "0x10": "increase",
            "0x11": "decrease"
        },
        "0x18": {
            "0x11": "mute"
        }
    },
    "APPLE": {
        "0xFF": {
            "0xB":  "increase",
            "0xD": "decrease",
            "0x5E": "mute"
        }
    }
}

class CamillaVolume:
    def __init__(self, websocket_url):
        self.ws = websocket.create_connection(websocket_url)
        self.current_volume = self.get_volume()

    def get_mute(self):
        self.ws.send(json.dumps('GetMute'))
        mute = json.loads(self.ws.recv())['GetMute']['value']
        self.timestamp = int(time.time())
        return mute

    def get_volume(self):
        self.ws.send(json.dumps('GetVolume'))
        volume = json.loads(self.ws.recv())['GetVolume']['value']
        self.timestamp = int(time.time())
        print('volume: {}'.format(volume))
        return volume

    def mute(self):
        self.ws.send(json.dumps({"SetMute": True }))
        print("mute")
        return self.ws.recv()

    def unmute(self):
        self.ws.send(json.dumps({"SetMute": False }))
        print("unmute")
        return self.ws.recv()

    def switch_mute(self):
        mute = self.get_mute()
        result = ""
        if mute == False:
            result = self.mute()
        elif mute == True:
            result = self.unmute()
        return result

    def set_volume(self, volume):
        self.ws.send(json.dumps({"SetVolume": volume }))
        return self.ws.recv()

    def increase(self):
        volume = self.get_volume()
        result = ""
        if volume < 0:
            result = self.set_volume(volume + 1)
        return result

    def decrease(self):
        volume = self.get_volume()
        result = ""
        if volume > -99:
            result = self.set_volume(volume - 1)
        return result

    def keep_alive(self, timeout):
        time_alive = int(time.time()) - self.timestamp
        if time_alive >= timeout:
            self.get_volume()


try:
    ser.open()
except serial.SerialException as e:
    sys.stderr.write('Could not open serial port {}: {}'.format(ser.name, e))
    sys.exit(1)

remote = CamillaVolume("ws://127.0.0.1:1234")
remote.set_volume(-12)

while True:
    serial_data = ser.readline().decode('utf-8')
    if serial_data.startswith('Protocol'):
        protocol = ""
        address = ""
        command = ""
        for item in serial_data.split(' '):
            if item.startswith('Protocol'):
                protocol = item.split('=')[1]
            elif item.startswith('Address'):
                address = item.split('=')[1]
            elif item.startswith('Command'):
                command = item.split('=')[1]

        # print(serial_data)

        action = ""
        try:
            action = configuration[protocol][address][command]
        except KeyError as e:
            print('{} {} {} not defined'.format(protocol, address, command))
        
        if action == "mute":
            remote.switch_mute()
        elif action == "increase":
            remote.increase()
        elif action == "decrease":
            remote.decrease()
        
    remote.keep_alive(30)
