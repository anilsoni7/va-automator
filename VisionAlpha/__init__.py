try:

    from hashlib import sha512
    from VisionAlpha.Thread import Thread
    from requests import post
    from json import loads
    from time import sleep
    import pickle
    from os import path,unlink
    from platform import system
    from datetime import datetime
    from VisionAlpha.DirectionThread import DirectionThread



except ImportError:

    from hashlib import sha512
    from VisionAlpha.Thread import Thread
    from requests import post
    from json import loads
    from time import sleep
    import pickle
    from os import path,unlink
    from platform import system
    from datetime import datetime


class VisionAlpha:
    def __init__(self,id,username,password,direction,acesstoken):
        self.id = id
        self.username = username
        self.password = password
        self.access_token = acesstoken
        self.token_type = 'Bearer'
        self.direction = direction  # 0 as down and 1 as up


def main(usr):
    if type(usr) is not type(list()):
        browser_instance = int(input("How many account you want to open :: "))
        usr = []
        for i in range(browser_instance):
            usr.append([])
            usr[i].append(i)
            usr[i].append(input("Enter Username for Account " + str(i + 1) + " :: "))
            usr[i].append(input("Enter Password for Account " + str(i + 1) + " :: "))
            usr[i].append(int(input("Enter up/down as 1/0 for Account " + str(i + 1) + " :: ")))

    # API_ENDPOINT = "https://visionalpha.000webhostapp.com/"
    #
    # for i in range(len(usr)):
    #
    #     data = {'username': usr[i][1],
    #             'password': sha512(str(usr[i][2]).encode('utf-8')).hexdigest()}
    #     req = post(url=API_ENDPOINT, data=data)
    #     j = loads(req.text)
    #
    #     if j == 0:
    #         print("There was error verifying username %s" % usr[i][1])
    #         exit()
    #     #if int(j) < len(usr):
    #     #    print("You are only allowed to login with %s id" % j)
    #     #   exit()
    #
    #     print("%d - %s username verified " %(usr[i][0],usr[i][1]))
    #     sleep(2)


    tok =[]

    thread = []
    va = []

    if path.isfile('data.pickle'):

        if system() == 'Windows':
            date = path.getctime('data.pickle')
        else:
            date = path.getmtime('data.pickle')

        ct = datetime.fromtimestamp(date)
        tt = datetime.today()
        z = tt - ct

        if z.days > 2:
            unlink('data.pickle')
        else :

            with open("data.pickle","rb") as f:
                tok = pickle.load(f)
            f.close()
        if len(usr) != len(tok):
            print("There was error verifying users ")
            print("To continute please delete data.pickle file and start again")
            exit()

        for i in range(len(usr)):
            va.append(VisionAlpha(usr[i][0], usr[i][1], usr[i][2], usr[i][3],tok[i]))
            thread.append(Thread(usr[i][0], usr[i][1], va[i]))

    else :
        for i in range(len(usr)):
            va.append(VisionAlpha(usr[i][0], usr[i][1], usr[i][2], usr[i][3],""))
            thread.append(Thread(usr[i][0], usr[i][1], va[i]))


    # directionThread = DirectionThread(1,'DirectionThread')
    # directionThread.start()

    acesst = []
    for t in thread:
        t.start()
        while(t.va.access_token =="" and t.authcount != 3):
            pass
        if len(tok) == 0 :
            if(t .authcount == 3 and t.va.access_token=="" ):
                acesst.append("")
            else:
                acesst.append(t.va.access_token)
    #
    if not path.isfile('data.pickle') or len(tok) == 0:
        with open("data.pickle", "wb") as f:
                pickle.dump(acesst,f)
        f.close()






if __name__ == "__main__":
   main(usr="")
