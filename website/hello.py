from flask import Flask, render_template, jsonify, request
from flask import redirect, url_for
import serial

#ser = serial.Serial('/dev/ttyACM0', 9600) #raspberry pi USB serial input
ser = serial.Serial('/dev/tty.usbmodem1421', 9600)

app = Flask(__name__)
message = ""
time = ""


# This route is the initial main HTML page that loads up when the server is launched
# The time variable sets the clock initally to 0, which displays the clock on the page
@app.route('/')
def index():
    return render_template('index.html', time=0, totaltime=0)


# This route will take in an input message and parse the timer from it
# Message format: B000000
# The first three numbers are boiling time
# Second three numbers are tea time 
# Serial write can only write size 1 byte at a given time
@app.route('/send', methods=['POST'])
def send():
    temp = []
    temp = str(request.form['inputMessage'])
    message = request.form['inputMessage']
    boilingtime = temp[1:-3]
    teatime = temp[4:]

    boilingtime = int(boilingtime) + 1
    teatime = int(teatime)
    cooling_time = 60
    servo_moving_time = 5
    totalTime = boilingtime + teatime + cooling_time + servo_moving_time

    for index in temp:
        ser.write(index)
    #ser.write(message)

    return render_template('index.html', time=boilingtime, message=message, totaltime=totalTime)

# For testing purposes when Arduino is not connected
# Test run without the Arduino
@app.route('/timeset', methods=['POST'])
def timeset():
    temp = []
    temp = str(request.form['timeset'])
    boilingtime = temp[1:-3]
    teatime = temp[4:]
    boilingtime = int(boilingtime)
    teatime = int(teatime)
    totalTime = boilingtime + teatime + 60 + 20
    for index in temp:
        print index
    #print boilingtime
    #print teatime
    return render_template('index.html', time=boilingtime, message=temp, totaltime=totalTime)


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
