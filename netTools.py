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
    con = subprocess.run(["nmcli","d","w",name,"password",password],capture_output=True)
    return str(con.stdout)
