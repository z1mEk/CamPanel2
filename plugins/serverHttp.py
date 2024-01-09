'''
pip3 install flask
'''
import os
import nest_asyncio
nest_asyncio.apply()
from flask import Flask, jsonify, render_template, send_from_directory
from threading import Thread
from plugins import waterLevel, dalyBms, relays
from general.configLoader import config
import logging
import logging.handlers

TEMPLATES_DIR = os.path.join('plugins', 'html')
app = Flask("CamPanel", template_folder=TEMPLATES_DIR)

handler = logging.handlers.RotatingFileHandler('flask.log', maxBytes=10*1024*1024, backupCount=5)
logging.getLogger('werkzeug').setLevel(logging.INFO)
logging.getLogger('werkzeug').addHandler(handler)
app.logger.setLevel(logging.INFO)
app.logger.addHandler(handler)

class plugin:

    @classmethod
    def start_flask_server(cls):
        host = config.httpServer.host
        port = config.httpServer.port
        app.run(host=host, port=port)

    @classmethod
    async def initialize(cls, event_loop):
        await nest_asyncio.asyncio.sleep(5)
        thread = Thread(target=cls.start_flask_server)
        thread.daemon = True
        thread.start()

@app.route('/getData')
def get_waterLevel():
    response = {
        "waterLevel": 
        {
            "whiteWaterLevel": waterLevel.data.whiteWaterLevel,
            "greyWaterLevel": waterLevel.data.greyWaterLevel,
        },
        "bms":
        {
            "totalVoltageDisplay": dalyBms.data.totalVoltageDisplay,
            "currentDisplay": dalyBms.data.currentDisplay,
            "RSOC": dalyBms.data.RSOC,
        },
        "relays": relays.data.relaysState
    }
    return jsonify(response)

@app.route('/')
def getIndex():
    return render_template('index.html')

@app.route('/css/<file_name>')
def getCss(file_name):
    return send_from_directory(os.path.join(TEMPLATES_DIR, 'css'), file_name)

@app.route('/js/<file_name>')
def getJs(file_name):
    return send_from_directory(os.path.join(TEMPLATES_DIR, 'js'), file_name)

@app.route('/fonts/<file_name>')
def getFonts(file_name):
    return send_from_directory(os.path.join(TEMPLATES_DIR, 'fonts'), file_name)

@app.route('/setrelay/relay<relay>/toggle')
def set_relay(relay):
    relays.data.relays[int(relay)].toggle()
    return jsonify({"success": True})