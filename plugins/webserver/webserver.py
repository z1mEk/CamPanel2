from flask import Flask

app = Flask(__name__)
        
@app.route("/")
def index():
    return "Hello, I'm Campanel!"

@app.route("/dupa")
def dupa():
    return {}

app.debug = True
app.run()    
