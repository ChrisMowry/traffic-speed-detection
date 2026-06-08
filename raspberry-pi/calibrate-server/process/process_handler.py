import os, signal
import psutil

class ProcessHandler:
    def __init__(self, pidFileName=r"../calibrate-server/.pid"):
        self.pidFileName = pidFileName
        self.pids = []
        if os.path.exists(pidFileName):
            self.getPids()
            
    def deleteFile(self):
        if os.path.exists(self.pidFileName): 
            os.remove(self.pidFileName)
    
    def savePid(self, pid):
        with open(self.pidFileName, "a") as pidFile:
            pidFile.write("{}\n".format(pid))
        self.getPids()
        
    def removePid(self, pid):
        self.getPids()
        self.pids.remove(pid)
        with open(self.pidFileName, "w") as pidFile:
            for pid in self.pids:
                pidFile.write("{}\n".format(pid))
        
    def getPids(self):
        if os.path.exists(self.pidFileName):
            with open(self.pidFileName, "r") as pidFile:
                for line in pidFile:
                    if len(line.strip()) >= 1:
                        self.pids.append(int(line))
    
    def stopProcess(self, pid):
        self.getPids()
        if pid in self.pids:
            os.kill(pid, signal.SIGTERM)
            self.pids.remove(pid)
            with open(self.pidFileName, "w") as pidFile:
                for pid in self.pids:
                    pidFile.write("{}\n".format(pid))
        
    def stopAllProcesses(self):
        self.getPids()
        if len(self.pids) > 0:
            for pid in set(self.pids):
                try:
                    process = psutil.Process(pid)
                    print("Stopping {}".format(process.cmdline()))
                    os.kill(pid, signal.SIGTERM)
                except:
                    pass
            with open(self.pidFileName, "w") as pidFile:
                pidFile.write("")
            
