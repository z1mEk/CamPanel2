'''
pip3 install flask
'''
import os
import nest_asyncio
nest_asyncio.apply()
from flask import Flask, jsonify, render_template, send_from_directory
from threading import Thread
from plugins import waterLevel, dalyBms, epeverTracer, relays, temperatures
from general.configLoader import config
import logging
import logging.handlers

TEMPLATES_DIR = os.path.join('plugins', 'html')
app = Flask("CamPanel", template_folder=TEMPLATES_DIR)

handler = logging.handlers.RotatingFileHandler(config.httpServer.filelog,
                                               maxBytes=config.httpServer.LogmaxBytes,
                                               backupCount=config.httpServer.backupCount)

logging.getLogger('werkzeug').setLevel(logging.INFO)
logging.getLogger('werkzeug').addHandler(handler)
app.logger.setLevel(logging.WARNING)
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
def getData():
    response = {
        "success": True,
        "waterLevel": 
        {
            "whiteWaterLevel": waterLevel.data.whiteWaterLevel,
            "greyWaterLevel": waterLevel.data.greyWaterLevel,
        },
        "bms":
        {
            "totalVoltage": dalyBms.data.totalVoltage,
            "currentMiliamper": dalyBms.data.currentMiliAmper,
            "currentFlex": dalyBms.data.currentFlex,
            "currentFlexUnit": dalyBms.data.currentFlexUnit,
            "currenFlexWithUnit": (
                '{:.0f}mA'.format(dalyBms.data.currentFlex) if abs(dalyBms.data.currentMiliAmper) < 1000 else
                '{:.2f}A'.format(dalyBms.data.currentFlex) if abs(dalyBms.data.currentMiliAmper) < 10000 else
                '{:.1f}A'.format(dalyBms.data.currentFlex) if abs(dalyBms.data.currentMiliAmper) < 100000 else
                '{:.0f}A'.format(dalyBms.data.currentFlex)
            ),
            "RSOC": dalyBms.data.RSOC,
        },
        "solar":
        {
            "pvVoltage": '{:.1f}V'.format(epeverTracer.pv.voltage),
            "pvCurrent": '{:.1f}A'.format(epeverTracer.pv.current),
            "pvPower": '{:.0f}W'.format(epeverTracer.pv.power)
        },
        "temperature":
        {
            "inTemp": '{:.0f}'.format(temperatures.data.inTemp),
            "outTemp": '{:.0f}'.format(temperatures.data.outTemp),
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