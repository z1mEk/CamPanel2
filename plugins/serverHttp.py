from flask import Flask, jsonify, request, render_template, send_from_directory
from threading import Thread
from plugins import waterLevel, dalyBms
from hmi import methods as hmiMethods
from general import methods as generalMethods
import os

TEMPLATES_DIR = os.path.join('plugins', 'html')
app = Flask("CamPanel", template_folder=TEMPLATES_DIR)

class plugin:

    @classmethod
    def start_flask_server(cls):
        app.run(host='0.0.0.0', port=5000)

    @classmethod
    def initialize(cls, event_loop):
        thread = Thread(target=cls.start_flask_server)
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
            "totalVoltage": dalyBms.data.totalVoltage,
            "currentAmper": dalyBms.data.currentAmper,
            "RSOC": dalyBms.data.RSOC
        }
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

@app.route('/set', methods=['GET'])
def set_rsoc():
    rsoc = request.args.get('rsoc')
    dalyBms.data.RSOC = rsoc
    return jsonify({"success": True, "message": f"RSOC set to {rsoc}", "rsoc": rsoc})

@app.route('/wakeup', methods=['GET'])
def wakeup():
    generalMethods.RunAsync(hmiMethods.wakeUp())
    return jsonify({"success": True})
