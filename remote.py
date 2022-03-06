import sys
import getopt
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

DEFAULT_CONFIGURATION = {
    "websocket_api": "ws://127.0.0.1:1234",
    "remote": {
        "APPLE": {
            "0xFF": {
                "0xB":  "increase",
                "0xD": "decrease",
                "0x5E": "mute"
            }
        }
    },
    "volume": -12,
    "mute": False
}

class CamillaVolume:
    def __init__(self, configuration_file, default_configuration):
        self.configuration_file = configuration_file
        self.configuration = self.get_configuration(default_configuration)
        self.ws = websocket.create_connection(self.configuration["websocket_api"])
        self.remote_mapping =  self.configuration["remote"]

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

    def set_mute(self, mute):
        self.ws.send(json.dumps({"SetMute": mute }))
        self.configuration["mute"] = mute
        self.timestamp = int(time.time())
        print("mute: {}".format(mute))
        return self.ws.recv()

    def switch_mute(self):
        mute = self.get_mute()
        result = ""
        if mute == False:
            result = self.set_mute(True)
        elif mute == True:
            result = self.set_mute(False)
        return result

    def set_volume(self, volume):
        self.ws.send(json.dumps({"SetVolume": volume }))
        self.configuration["volume"] = volume
        self.timestamp = int(time.time())
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
            self.save_configuration()

    def get_configuration(self, default_configuration):
        configuration = ""
        try:
            with open(self.configuration_file, mode='r') as configuration_file:
                try:
                    configuration = json.load(configuration_file)
                except:
                    print("{} is corrupted".format(self.configuration_file))
                    configuration = default_configuration
        except FileNotFoundError as e:
            print("{} not found, will use default configuration".format(self.configuration_file))
            configuration = default_configuration
        print(configuration)
        return configuration

    def save_configuration(self):
        with open(self.configuration_file, mode='w') as configuration_file:
            json.dump(self.configuration, configuration_file, ensure_ascii=False, indent=4)


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:", ["help", "conf="])
    except getopt.GetoptError as err:
        print(err)
        print("remote.py -c <conf>")
        sys.exit(2)
    configuration = ""
    verbose = False
    for o, a in opts:
        if o in ("-h", "--help"):
            print("remote.py -c <conf>")
            sys.exit()
        elif o in ("-c", "--conf"):
            configuration = a
        else:
            assert False, "unhandled option"

    # start serial
    try:
        ser.open()
    except serial.SerialException as e:
        sys.stderr.write('Could not open serial port {}: {}'.format(ser.name, e))
        sys.exit(1)

    # web socket connection
    remote = CamillaVolume(configuration, DEFAULT_CONFIGURATION)

    # set last saved mute & volume
    remote.set_mute(remote.configuration["mute"])
    remote.set_volume(remote.configuration["volume"])

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
                action = remote.remote_mapping[protocol][address][command]
            except KeyError as e:
                print('{} {} {} not defined'.format(protocol, address, command))
            
            if action == "mute":
                remote.switch_mute()
            elif action == "increase":
                remote.increase()
            elif action == "decrease":
                remote.decrease()
            
        remote.keep_alive(10)


if __name__ == "__main__":
    main()
