import os, time

pidFile = open('.pid','w')
pidFile.write("{}".format(os.getpid()))
pidFile.close()



for x in range(100):
    print(x)
    time.sleep(10)