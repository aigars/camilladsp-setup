import sys
import websocket
import json
import time
import flask
from flask import request, jsonify, render_template
import logging

app = flask.Flask(__name__, static_url_path="")
# app.config["DEBUG"] = True
log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

class CamillaConfiguration:
    def __init__(self, websocket_url):
        self.ws = websocket.create_connection(websocket_url)
        self.configuration = self.get_configuration()
    
    def get_configuration(self):
        self.ws.send(json.dumps('GetConfigJson'))
        configuration = json.loads(json.loads(self.ws.recv())['GetConfigJson']['value'])
        self.timestamp = int(time.time())
        return configuration

    def set_configuration(self):
        self.ws.send(json.dumps({'SetConfigJson': json.dumps(self.configuration)}))
        print(self.ws.recv())
        #print(self.configuration)

    def set_mute(self, channel, mute):
        self.configuration['mixers']['mixer']['mapping'][channel]['mute'] = mute
        self.set_configuration()


@app.route("/", methods=["GET"])
def get_home():
    configuration = remote.get_configuration()
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
    remote.set_mute(data["channel"], data["mute"])
    data["mute"] = str(not data['mute']).lower()
    return jsonify(data)


if __name__ == "__main__":
    remote = CamillaConfiguration("ws://127.0.0.1:1234")
    app.run(host='0.0.0.0', port=8080)
