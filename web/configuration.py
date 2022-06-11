import sys
import websocket
import json
import time
import flask
from flask import request, jsonify, render_template
import logging
from multiprocessing import Process, Value

app = flask.Flask(__name__, static_url_path="")
# app.config["DEBUG"] = True
log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

class CamillaConfiguration:
    def __init__(self, websocket_url, configuration_file):
        self.ws = websocket.create_connection(websocket_url)
        self.configuration_file = configuration_file
        self.configuration = self.get_configuration()
        self.saved_muted = self.get_saved_configuration()
        self.muted = {}
        self.set_saved_mute(self.saved_muted)
    
    def get_saved_configuration(self):
        configuration = {}
        try:
            with open(self.configuration_file, mode='r') as configuration_file:
                try:
                    configuration = json.load(configuration_file)
                except:
                    print("{} is corrupted".format(self.configuration_file))
        except FileNotFoundError as e:
            print("{} not found, will use default configuration".format(self.configuration_file))
        print(configuration)
        return configuration

    def get_configuration(self):
        self.ws.send(json.dumps('GetConfigJson'))
        configuration = json.loads(json.loads(self.ws.recv())['GetConfigJson']['value'])
        self.timestamp = int(time.time())
        return configuration

    def set_configuration(self):
        self.ws.send(json.dumps({'SetConfigJson': json.dumps(self.configuration)}))
        #print(self.configuration)
        print(self.ws.recv())

    def set_mute(self, channel, mute):
        set_mute=True
        try:
            self.configuration['mixers']['mixer']['mapping'][channel]['mute'] = mute
        except IndexError as e:
            print("{} channel not found".format(channel))
            set_mute=False
        if set_mute:
            self.muted[channel] = mute
            self.set_configuration()
            self.save_configuration()

    def keep_alive(self, timeout):
        time_alive = int(time.time()) - self.timestamp
        if time_alive >= timeout:
            self.get_configuration()
            print("keep alive")
    
    def set_saved_mute(self, muted):
        for channel, mute in muted.items():
            self.set_mute(int(channel), mute)
    
    def save_configuration(self):
        with open(self.configuration_file, mode='w') as configuration_file:
            json.dump(self.muted, configuration_file, ensure_ascii=False, indent=4)


@app.route("/", methods=["GET"])
def get_home():
    configuration = conf.get_configuration()
    channel_mapping = configuration['mixers']['mixer']['mapping']
    mixer = []
    for channel in channel_mapping:
        print("channel: {}, mute {}".format(channel['dest'], channel['mute']))
        channel = {
            "channel": channel['dest'],
            "mute": str(not channel['mute']).lower()
        }
        mixer.append(channel)
    res = render_template('mute_template.html', mixer=mixer)
    return res

@app.route("/mute/", methods=["POST"])
def set_mute():
    data = request.json
    print(data)
    conf.set_mute(data["channel"], data["mute"])
    data["mute"] = str(not data['mute']).lower()
    return jsonify(data)  

if __name__ == "__main__":
    conf = CamillaConfiguration("ws://127.0.0.1:1234", "/home/dsp-user/web/configuration.json")
    app.run(host='0.0.0.0', port=80, threaded=True)
