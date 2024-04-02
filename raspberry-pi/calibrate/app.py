from flask import Flask, jsonify, request, render_template
from picamera2 import Picamera2, Preview
from decimal import Decimal
import urllib
import time

app = Flask(__name__)

# setup the Pi Camera to take a still image to use to calibrate the application
picam2 = Picamera2()
cameraConfig = picam2.create_still_configuration(main={"size":(1920,1080)}, lores={"size":(640,480)}, display="lores")
picam2.configure(cameraConfig)
picam2.start()

# Give the camera time to setup
time.sleep(2)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/get-image', methods = ['GET'])
def getImage():
    name = request.args.get('camera-name')
    imageFile = "../calibrate-images/{}.jpg".format(name)
    picam2.capture_file(imageFile)
    
    #data = {"image" : imageFile}
    data = {"image" : "/imgs/test.jpg"}
    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin','*')
    
    return response

@app.route('/monitor', methods = ['POST'])
def startMonitoring():
    cameraName = urllib.parse.unquote(request.args.get('camera-name'))
    distanceRatio = Decimal(urllib.parse.unquote(request.args.get('distance-ratio')))
    sampleZonePercent = Decimal(urllib.parse.unquote(request.args.get('sample-zone')))
    speedLimit = Decimal(urllib.parse.unquote(request.args.get('speed-limit')))
    print("Camera Name: {} Distance Ratio: {} Sample Zone %: {} Speed Limit: {}".format(
        cameraName,
        distanceRatio,
        sampleZonePercent,
        speedLimit))
    
    response = jsonify({"success":True})
    response.headers.add('Access-Control-Allow-Origin','*')
    response.status_code = 200
    
    return response
         
         
if __name__ == "__main__":
    app.run(host="0.0.0.0")