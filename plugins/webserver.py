from flask import Flask
from flask import jsonify
import json
import asyncio
from plugins import bms

class webserver:
    app = Flask('CamPanel')
        
    @app.route("/")
    def index():
        return "Hello, I'm Campanel!"

    @app.route("/dupa")
    def dupa():
        return json.dumps(bms.data.__dict__)

class plugin:
    name = 'WebServer'

    @classmethod
    def initialize(self):
        loop = asyncio.get_event_loop()  
        webserver.app.debug = True
        webserver.app.run()    
        loop.run_forever