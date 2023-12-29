import math
import cv2
import numpy as np
from datetime import datetime
from operator import attrgetter

def getVector(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    dx = float(x2 - x1)
    dy = float(y2 - y1)
        
    distance = math.sqrt(dx**2 + dy**2)
        
    if dy > 0:
        angle = math.degrees(math.atan(-dx/dy))
    elif dy == 0.0:
        if dx < 0.0:
            angle = 90.0
        elif dx > 0:
            angle = -90.0
        else:
            angle = 0.0
    else:
        if dx < 0:
            angle = 180 - math.degrees(math.atan(dx/dy))
        elif dx > 0:
            angle = -180 - math.degrees(math.atan(dx/dy))
        else:
            angle = 180.0
                
    return distance, angle
    

class ProcessedObject(object):
    def __init__(self, id, dateTime):
        self.id = id
        self.dateTime = dateTime
        self.speed = None
        self.direction = None
        self.image = ""
        self.positions = []
    

class Position(object):
    def __init__(self, point, boundingBox, frameNumber):
        self.point = point
        self.boundingBox = boundingBox
        self.frameNumber = frameNumber
        self.inSampleZone = False
        self.vector = None
        
        
class SampleZone(object):
    def __init__(self, size, samplePercent):
        width, height = size
        halfPercentAmount = width * ((samplePercent / 2.0 ) / 100.0)
        self.midX = width / 2
        self.startX = self.midX - halfPercentAmount
        self.startY = 0.0
        self.endX = self.midX + halfPercentAmount
        self.endY = height
    
class MovingObject(object):
    
    def __init__(self, objectId, position, startFrame):
        self.id = objectId
        self.positions = [position]
        self.totalDistance = 0
        self.distanceFromStart = 0
        self.startFrame = startFrame
        self.midPointPosition = None
        self.sampleZonePositions = []
        self.lastFrame = -1
        self.counted = False
        self.speed = None
        
        # generates a random color
        self.color = (np.random.randint(255), np.random.randint(255), np.random.randint(255))
        
    def getPositionCount(self):
        return len(self.positions)
        
    def getLastPosition(self):
        return self.positions[-1]
    
    def addPosition(self, position, fps, midX):
        if len(self.positions) > 0:
            startPosition = self.positions[0]
            vectorFromStart = getVector(startPosition.point, position.point)
            position.vector = getVector(self.getLastPosition().point, position.point)
            self.totalDistance = self.getTotalDistance()
            self.distanceFromStart = vectorFromStart[0]
            if self.getLastPosition().point[0] < midX and position.point[0] > midX:
                self.midPointPosition = position
            if self.getLastPosition().point[0] > midX and position.point[0] < midX:
                self.midPointPosition = position
            
            #position.speed = self.getSpeed(lastPosition, position, fps)
            
        self.positions.append(position)
        self.lastFrame = position.frameNumber
        
        
    def getTotalDistance(self):
        totalDistance = 0
        for position in self.positions:
            if position.vector != None:
                distance, angle = position.vector
                totalDistance += distance
            
        return totalDistance
    
        
    def setSpeed(self, position1, position2, fps):
        frameDiff = position2.frameNumber - position1.frameNumber
        
        print("Frame Diff: {0}".format(frameDiff))
        seconds = frameDiff/fps
        
        self.speed = getVector(position1.point, position2.point)[0] / seconds
        

    def draw(self, outputImage):
        
        for position in self.positions:
            cv2.circle(outputImage, position.point, 2, self.color, 1)
            cv2.polylines(outputImage, [np.int32([obj.point for obj in self.positions])], False, self.color, 1)
            cv2.putText(outputImage, "{0}".format(self.id), position.point, cv2.FONT_HERSHEY_PLAIN, 0.7, (127, 255, 255), 1)
            
        #if self.speed:
            #cv2.putText(outputImage, ("%1.2f" % self.speed), cv2.FONT_HERSHEY_PLAIN, 0.7, (127, 255, 255), 1)
            

class MovingObjects(object):
    
    def __init__(self, fps, sampleZone, outputImage=None):
        self.fps = fps
        self.sampleZone = sampleZone
        self.MAX_MISSING_FRAMES = 10
        self.nextObjectId = 1
        self.movingObjects = []
        
    def isValidVector(self, vector):
        self.ANGLE_TOLERANCE = 15.0
        self.TRAFFIC_DIRECTION = 90.0 # abs value
        self.DISTANCE_TOLERANCE = 200.0
        
        minAngle = self.TRAFFIC_DIRECTION - self.ANGLE_TOLERANCE
        maxAngle = self.TRAFFIC_DIRECTION + self.ANGLE_TOLERANCE
        distance, angle = vector
        
        return abs(angle) > minAngle and abs(angle) < maxAngle and distance <= self.DISTANCE_TOLERANCE

    def getMidlinePosition(self, frameNumber):
        for obj in self.movingObjects:
            if obj.midPointPosition != None:
                if obj.midPointPosition.frameNumber == frameNumber:
                    return obj
            
        return None
    
    def inSampleZone(self, point):
        x = point[0]
        if x >= self.sampleZone.startX and x <= self.sampleZone.endX:
            return True
        
        return False
        
    def updateObjects(self, movingObject, matches, frameNumber):
        inZone = False
        for i, match in enumerate(matches):
            contour, centroid = match
            
            vector = getVector(movingObject.getLastPosition().point, centroid)
            distance, angle = vector
            if self.isValidVector(vector):
                position = Position(centroid, contour, frameNumber)
                prevPoint = movingObject.getLastPosition().point
                
                # if the position is in the sample zone, set in zone as well as previous point
                if self.inSampleZone(centroid):
                    position.inSampleZone = True
                    movingObject.positions[-1].inSampleZone = True
                #if position is not in the samplezone, but the previous position was, set in zone
                if not self.inSampleZone(centroid):
                    if self.inSampleZone(prevPoint):
                        position.inSampleZone = True
                # if previous position was on other side of zone, set both in zone
                if not self.inSampleZone(centroid):
                    if prevPoint[0] < self.sampleZone.startX and centroid[0] > self.sampleZone.endX:
                        position.inSampleZone = True
                        movingObject.positions[-1].inSampleZone = True                        
                    if prevPoint[0] > self.sampleZone.endX and centroid[0] < self.sampleZone.startX:
                        position.inSampleZone = True
                        movingObject.positions[-1].inSampleZone = True                          
                    
                if movingObject.positions[-1].inSampleZone and not position.inSampleZone:
                    # filters the position array to positions in the sample zone
                    sampledPoints = list(filter(lambda p: p.inSampleZone, movingObject.positions))
                    
                    # gets the positions just outside of the sample zone
                    if len(sampledPoints) > 0:
                        minFrameSampleZonePoint = min(sampledPoints, key=attrgetter('frameNumber'))
                        maxFrameSampleZonePoint = max(sampledPoints, key=attrgetter('frameNumber'))
                    
                        # sets the speed of the object
                        movingObject.setSpeed(minFrameSampleZonePoint, maxFrameSampleZonePoint, self.fps)
                    
                    
                movingObject.addPosition(position, self.fps, self.sampleZone.midX)
                # TODO: clean this up
                if movingObject.getPositionCount() > 10:
                    movingObject.counted=True
                    
                return i
            
        return None
    
    def countObjects(self, matches, frameNumber, outputImage):
        
        # Update existing objects
        for movingObject in self.movingObjects:
            i = self.updateObjects(movingObject, matches, frameNumber)
            if i is not None:
                del matches[i]
                
        # Add new moving objects
        for match in matches:
            contour, centroid = match
            position = Position(centroid, contour, frameNumber)
            newObject = MovingObject(self.nextObjectId, position, frameNumber)
            self.movingObjects.append(newObject)
            self.nextObjectId += 1
        
        # Draw Moving Objects
        if outputImage is not None:
            for movingObject in self.movingObjects:
                movingObject.draw(outputImage)
        
        # Clean-up moving objects collection
        self.movingObjects[:] = [mv for mv in self.movingObjects if frameNumber - mv.lastFrame <= self.MAX_MISSING_FRAMES or mv.counted == True]
