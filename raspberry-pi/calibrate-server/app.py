from flask import Flask, jsonify, request, render_template
from picamera2 import Picamera2, Preview
from decimal import Decimal
import urllib, subprocess, os, signal, time, sys

app = Flask(__name__)



@app.route("/")
def index():
    return render_template("index.html")

@app.route('/get-image', methods = ['GET'])
def getImage():
    # setup the Pi Camera to take a still image to use to calibrate the application
    picam2 = Picamera2()
    cameraConfig = picam2.create_still_configuration(main={"size":(1920,1080)}, lores={"size":(640,480)}, display="lores")
    picam2.configure(cameraConfig)
    picam2.start()

    # Give the camera time to setup
    time.sleep(2)

    name = request.args.get('camera-name')
    imageFile = "../calibrate-images/{}.jpg".format(name)
    picam2.capture_file(imageFile)
    picam2.close()
    
    #data = {"image" : imageFile}
    data = {"image" : "/imgs/test.jpg"}
    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin','*')
    
    return response

@app.route('/monitor', methods = ['POST'])
def startStopMonitoring():
    stop = False
    
    if request.args.get('camera-name') is not None:
        cameraName = urllib.parse.unquote(request.args.get('camera-name'))
    
    if request.args.get('distance-ratio') is not None:
        distanceRatio = Decimal(urllib.parse.unquote(request.args.get('distance-ratio')))
    
    if request.args.get('sample-zone') is not None:
        sampleZonePercent = Decimal(urllib.parse.unquote(request.args.get('sample-zone')))
    
    if request.args.get('sample-zone') is not None:
        speedLimit = Decimal(urllib.parse.unquote(request.args.get('speed-limit')))
    
    if request.args.get('stop') is not None:
        stop = bool(urllib.parse.unquote(request.args.get('stop')).title())
    
    if not stop:
        if not [var for var in (cameraName, distanceRatio, sampleZonePercent, speedLimit) if var is None]:
            
            response = jsonify({"success":True})
            response.headers.add('Access-Control-Allow-Origin','*')
            response.status_code = 200
            subprocess.Popen(['python','./process/motion_record.py','--camera-name={}'.format(cameraName),'--speed-limit={}'.format(speedLimit),'--ratio'.format(distanceRatio),'--sample-zone'.format(sampleZonePercent)])
        else:
            response = jsonify({"success":False})
            response.headers.add('Access-Control-Allow-Origin','*')
            response.status_code = 400
    else:
        pid = 0
        
        # read the python process id
        pidDoc = open('.pid', 'r')
        pid = int(pidDoc.read())
        
        # stop the python process
        os.kill(pid, signal.SIGTERM)
        pidDoc.close()
            
        response = jsonify({"success":True})
        response.headers.add('Access-Control-Allow-Origin','*')
        response.status_code = 200
    
    return response
         
         
if __name__ == "__main__":
    app.run(host="0.0.0.0")