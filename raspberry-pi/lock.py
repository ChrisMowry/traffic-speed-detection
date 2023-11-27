import os

LOCKFILE_NAME = ".lock"

def lock(file):
    """
    Creates a text file with video file names that are currently
    being written.
    """
    dir = os.path.dirname(file)
    with open(os.path.join(dir, LOCKFILE_NAME), "a") as lockFile:
        # writes the filename to the lock file
        lockFile.write("{0}\n".format(os.path.basename(file.strip())))
        
def unlock(file):
    """
    Removes file name from the lock file when function is called
    """
    dir = os.path.dirname(file)
    lockfile = os.path.join(dir, LOCKFILE_NAME)
    lockedfileNames = []
    if os.path.isfile(lockfile):
        # Create list of files in lock file
        with open(lockfile, "r") as lockfileReader:
            lockedfileNames = lockfileReader.read().split("\n")
            
        # Remove empty strings
        lockedfileNames = list(filter(None, lockedfileNames))
        
        # Remove file to unlock from list
        lockedfileNames = list(filter(lambda name: name != os.path.basename(file), lockedfileNames))
        
        # if list of locked file names is empty, delete lock file, otherwise write all file names except
        # the unlocked file name
        if len(lockedfileNames) > 0:
            with open(lockfile, "w") as lockfileWriter:
                for lockfileName in lockedFileNames:
                    lockfileWriter.write("{0}\n".format(lockfileName))
        else:
            os.remove(lockfile)
            
def isLocked(file):
    dir = os.path.dirname(file)
    lockfile = os.path.join(dir, LOCKFILE_NAME)
    
    if not os.path.isfile(lockfile):
        return False
    
    lockedfileNames = []
    with open(os.path.join(dir, LOCKFILE_NAME), "r" ) as lockFileReader:
        lockedfileNames = lockFileReader.read().split("\n")
        
    return os.path.basename(file).strip() in lockedfileNames
    

                    
            
            
            