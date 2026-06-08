import os, psutil
from camera_data import CameraData
from process_handler import ProcessHandler

class VideoHandler:
    
    def __init__(self, cameraData, videoDir=r"../calibrate-server/videos"):
        self.videoDir = videoDir
        self.pendingVideos = {}
        self.MAX_VIDEO_PROCESSING = 3
        self.cameraData = cameraData
        
    def getVideoList(self):
        return [file for file in os.listdir(self.videoDir) if os.path.isfile(os.path.join(self.videoDir, file)) and file.split(".")[-1].lower() == "h264"]
    
    def addVideoToProcess(self, video):
        if len(self.pendingVideos) < self.MAX_VIDEO_PROCESSING:
            if video not in list(self.pendingVideos.values()):
                process = subprocess.Popen(['python','./analyze_motion.py','--camera-name={}'.format(cameraData.name)
                  ,'--speed-limit={}'.format(cameraData.speedLimit), '--ratio={}'.format(cameraData.distanceRatio),
                  '--sample-zone={}'.format(cameraData.sampleZonePercent), '--video={}'.format(videoFileName)])
                
                return process

    def run(self):
        # log process id so client can kill it
        processHandler = ProcessHandler()
        processHandler.savePid(os.getpid())
        
        while(True):
            videos = self.getVideoList()
            # if the videos directory contains videos, start to process them
            if len(videos) > 0:
                video = self.getVideoList()[0]
                process = self.addVideoToProcess(video)
                self.pendingVideos[process.pid] = video
                
                # check the pending video processes to see if they are finished
                for pid in list(self.pendingVideos.keys):
                    if not psutil.pid_exists(pid):
                        del self.pendingVideos[pid]
    