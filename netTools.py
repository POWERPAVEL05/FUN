import subprocess
#gibt Liste von SSID wieder und Laenge der Liste
#beakpoint specifies amount
#TODO: handle 'I'm unkwown'
def getSSID(breakpoint = None,duplicateRemove=False)-> list:
    ssid = subprocess.run(["nmcli","-f" ,"SSID","-c","no","-t","d","w"],text=True,capture_output=True)
    nameList = str(ssid.stdout).split("\n")
    try:
        for _ in nameList:
            nameList.remove("")
    except:
        pass #no empty item
    if duplicateRemove:
        nameList = list(set(nameList))#remove duplicates
    if breakpoint == None:
        return nameList
    else:
        return nameList[:breakpoint]

def connect(name,password):
    if password == "":
        subprocess.run(["nmcli","d","w","connect",str(name)])
    else:
        subprocess.run(["nmcli","d","w","connect",str(name),"password",str(password)])

def wifiOff():
    subprocess.run(["nmcli","radio","wifi","off"])
    return 0

def wifiOn():
    subprocess.run(["nmcli","radio","wifi","on"])
    return 1
