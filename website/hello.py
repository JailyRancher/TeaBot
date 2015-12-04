from flask import Flask, render_template, jsonify, request
from flask import redirect, url_for
import serial

ser = serial.Serial('/dev/ttyACM1', 9600)

app = Flask(__name__)
message = ""
time = ""


# This route is the initial main HTML page that loads up when the server is launched
# The time variable sets the clock initally to 0, which displays the clock on the page
@app.route('/')
def index():
    return render_template('index.html', time=0)


# This route will take in an input message and parse the timer from it
# Message format: B 000 C
@app.route('/send', methods=['POST'])
def send():
    temp = []
    temp = str(request.form['inputMessage'])
    strtime = temp[1:-5]
    time = int(strtime)
    temperature = request.form['inputMessage']
    print message
    ser.write(message)
    return render_template('index.html', temperature=temperature, time=time)


# Test run without the Arduino
@app.route('/timeset', methods=['POST'])
def timeset():
    temp = []
    temp = str(request.form['timeset'])
    strtime = temp[1:-5]
    time = int(strtime)
    print type(time)
    print time
    return render_template('index.html', time=time, message=message)


# AJAX Call method
# Reads in message sent from Arduino and returns it to index.html
@app.route('/arduino/')
def readArduino():
    message=ser.readline()
    d = {}
    d['val'] = message
    return jsonify(**d)

if __name__=="__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
