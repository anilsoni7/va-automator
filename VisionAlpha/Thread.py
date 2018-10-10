try:
    import threading
    from time import sleep
    from requests import post
    from requests import get
    from requests import codes
    from json import loads
    from sys import exit
    from time import sleep
    from json import dumps
    from datetime import datetime
    import VisionAlpha.constant as constant
    from importlib import reload

except ImportError:
    from requests import post
    from requests import get
    from requests import codes
    from json import loads
    from json import dumps
    from sys import exit
    import threading
    from datetime import datetime
    from time import sleep
    import VisionAlpha.constant


client ={
    'id' : 'HippoRiceBowl_frontend',
    'secret' : '9HRoucDGLLpvcvICRpfV'
}

#API_ENDPOINT.va_secret is depriciated
API_ENDPOINT ={
    'va_secret' : 'http://visionalpha.000webhostapp.com/client.php',
    'hippo' : 'https://hippo-ricebowl-backend.azurewebsites.net/',
    'access_token' : 'accesstoken',
    'store_result' : 'insights/storeTraderInsight',
    'current_state' : 'insights/getCurrentState',
    'current_balance' : 'insights/getCurrentBalance',
    'past_session' : ''
}
fix_header ={
    'Accept' : 'application/json, text/plain, */*',
    'Origin': 'http://visionalpha.com',
    'Referer': 'http://visionalpha.com/'
}

class Thread(threading.Thread):
    def __init__(self,id,name,vaObject):
        threading.Thread.__init__(self)
        self.id = id
        self.name = name
        self.va = vaObject
        self.authcount =0

    def run(self):
        print("consuming process ", str(self.id))
        self.startthread()
        print("ended process ", str(self.id))

    def startthread(self):

        if self.va.access_token == "":
            self.auth()
        while True:
            self.getstate()

    # def getbalance(self):
    #     global API_ENDPOINT
    #     global fix_header
    #     header = {
    #         'Authorization': 'Bearer ' + str(self.va.access_token),
    #         'Accept': str(fix_header['Accept']),
    #         'Origin': str(fix_header['Origin']),
    #         'Referer' : str(fix_header['Referer'])
    #
    #     }
    #     r = get(str(API_ENDPOINT['hippo']) + str(API_ENDPOINT['current_balance']), headers=header)
    #     print(str(self.name) + " balance is " + str(r.text))
    #
    # def getsession(self):
    #     global API_ENDPOINT
    #     global fix_header
    #     header = {
    #         'Authorization': 'Bearer ' + str(self.va.access_token),
    #         'Accept': str(fix_header['Accept']),
    #         'Origin': str(fix_header['Origin']),
    #         'Referer' : str(fix_header['Referer'])
    #     }
    #     r = get(str(API_ENDPOINT['hippo']) + str(API_ENDPOINT['past_session']), headers=header)

    def getstate(self):
        global API_ENDPOINT
        global fix_header
        header = {
            'Authorization': 'Bearer '+str(self.va.access_token),
            'Accept': str(fix_header['Accept']),
            'Origin': str(fix_header['Origin']),
            'Referer' : str(fix_header['Referer'])
        }
        r = get(str(API_ENDPOINT['hippo']) + str(API_ENDPOINT['current_state']), headers=header)
        if r.status_code == codes.ok:
            j = loads(r.text)
            #print(j)
            if j['CanSubmit'] == True :
                #print(j)
                self.storetraderinsight( j['Segment'],datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT'))
                sleep(5)
                self.getstate()

            # r = get(str(API_ENDPOINT['hippo']) + str(API_ENDPOINT['current_state']), headers=header)
            # j = loads(r.text)
            wait = int(j['SecondsToNextSegment'])
            if wait < 151 :
                print( str(self.va.username) + " waiting for " + str(600) + " -=")
                sleep(600)
            # elif wait >150 and wait < 301:
            #     #self.storetraderinsight( j['Segment'],datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT'))
            #     sleep(wait-150)
            else:
                print( str(self.va.username) + " waiting for " + str(wait-150) )
                sleep(wait-150)

        else :
            print(r.text)
            rj = loads(r.text)
            if rj['Message'] :
                self.auth()

    def storetraderinsight(self,segment,time):
        global API_ENDPOINT
        global fix_header
        global direction
        header = {
            'Content-Type' : 'application/json',
            'Accept': str(fix_header['Accept']),
            'Authorization': "Bearer " + str(self.va.access_token),
            'Origin': str(fix_header['Origin']),
            'Referer' : str(fix_header['Referer'])
        }
        # if we get direction then self.va.direction
        # should be changed to constant.constant().direction

        #reload(constant)
        #current_time = datetime.utcnow()
        #if constant.constant.time.hour != current_time.hour or constant.constant.time.minute < current_time.minute - 2 :

        #   constant.constant.direction = input("Enter the direction for segment "+ str(segment) + " :: ")

        #direc = "buy" if constant.constant.direction else "sell"
        direc = "buy" if self.va.direction else "sell"
        payload = {
            'direction': str(direc),
            'segment' : int(segment),
            'submit_time': str(time)
        }
        # print(payload)
        # print("for user " + str(self.name))
        # print("json")
        # print(dumps(payload))
        r = post( str(API_ENDPOINT['hippo'])+str(API_ENDPOINT['store_result']), json=payload, headers=header)
        if r.status_code == codes.ok :
            print(loads(r.text) + " for " + str(self.va.username) + "  " + str(payload['direction']) + "  " + str(datetime.today().strftime('%d %H:%M:%S')))
        else:
            print("error submitting alpha for ", self.va.username)
            print(r.text)
            print(payload)

    def auth(self):
        global client
        while client['secret'] == '':
            client['secret'] = str(self.clientsecret())

        payload = {
            'client_id': 'HippoRiceBowl_frontend',
            'client_secret': client['secret'],
            'grant_type': 'password',
            'password': str(self.va.password),
            'username': str(self.va.username)
        }
        header = {
            'Accept' : 'application/json, text/plain, */*',
            'Content-Type' : 'application/x-www-form-urlencoded',
            'Origin': str(fix_header['Origin']),
            'Referer' : str(fix_header['Referer'])
        }
        sleep(2)
        if client['secret'] != "" :
            r = post( str(API_ENDPOINT['hippo']) + str(API_ENDPOINT['access_token']), data=payload, headers=header )
            if r.status_code == codes.ok :
                _ = loads(r.text)
                self.va.access_token = _['access_token']
                self.va.token_type = _['token_type']
            else :
                print("There was error obtaining Autharization for " + str(self.name))
                if(self.authcount == 3):
                    print("we were unable to login for account " + str(self.va.username))
                    print("Tried Attempt " + str(self.authcount))
                    exit()

                print(r.status_code)
                self.authcount += 1
                self.auth()

    def clientsecret(self):
        global API_ENDPOINT
        r = get(API_ENDPOINT['va_secret'])
        if r.status_code == codes.ok:
            j = loads(r.text)
            return str(j)
        else:
            return ""

    def marketcondition(self):
        pass