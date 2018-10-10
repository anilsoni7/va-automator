try:

    import threading
    import requests
    import constant
    from time import sleep
    from datetime import datetime
except ImportError:
    import threading
    import requests
    import constant
    from time import sleep
    from datetime import datetime

class DirectionThread(threading.Thread):
    def __init__(self,id,name):
        threading.Thread.__init__(self)

    def getdirection(self):
        #get direcction 1/0 from somewhere
        #update the constant.direction time to time
        #update constant.time = datetime.today()
        #wait for 540 seconds/ 9 minutes
        #sleep(540)

        pass


    def run(self):
        while True:
            self.getdirection()