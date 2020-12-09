from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "1st"

@app.route("/1")
def firstPage():
    return "ok"