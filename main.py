import curses
import subprocess
from keymanagers import timeToQuit, keymanagerQuit, keymanagerList, keymanagerTab 
stdscr = curses.initscr()

#raise when quitting tui

#Colors
def initColors():
    curses.init_pair(1,curses.COLOR_BLACK,curses.COLOR_WHITE)

#Takes list and displays vertical Menu, naviagate up and down through items, needs selected_row for cursor 
#TODO: make more dynamic
def menuList(selected_row,selected_win,winNum,navigation,frame=False):
    #adds padding to window if frame is included
    window = navigation[winNum][0]
    listItems = navigation[winNum][1]
    frameVar = 0
    if frame:
        frameVar = 1
    try:
        for idx,item in enumerate(listItems):
            x = 0  +frameVar
            y = 0 + idx + frameVar
            if idx == selected_row and selected_win == winNum :
                setColor(1,str(item),y,x,window)
            else:
                window.addstr(y,x,item)
    except:
        pass
    
    window.refresh()

def testBar(win):
    print("hewwo")

#draw bar across window
def drawBar(win):
    width = stdscr.getmaxyx()[1]
    for i in range(width-1):
        win.addch(0,i,"█")
    win.refresh()

#draw Frame around window, y x defined due resizing issues
def winFrame(win,height,width):
    for w in range(width-2):
        win.addch(0,w+1,"═")
        win.addch(height-1,w+1,"═")
    for h in range(height-2):
        win.addch(h+1,0,"║")
        win.addch(h+1,width-1,"║")
    win.addch(0,0,"╔")
    win.addch(0,width-1,"╗")
    win.addch(height-1,0,"╚")
    try:
        win.addch(height-1,width-1,"╝")
    except: pass
    #scuffed fix, curses tries to move curses to next line, even when there is none --> error

#don't know if this works
#is supposed to icut out some lines
def makeWin(height,width,y,x,windowList):
    id = str(windowList.len())
    name = "win"+id
    name = curses.newwin(height,width,y,x)
    windowList.append(name)


#Everything is run from here:Initiating/Updating of windows, row and soon to come focus_idx etc.
def main(stdscr):
    #list for all functions, is important
    #Init segment
    testItems = ['1','2','3','4']
    initColors()
    curses.curs_set(0)#cursor not invisible --> 0
    current_row_idx = 0 #row of window
    current_col_idx = 0 #Window
    key = 0
    
    #splash screen
    stdscr.addstr(0,0,"FUN - is fetching data")
    stdscr.refresh()
    height, width = stdscr.getmaxyx()
    itemsN = getSSID(18,True)

    #init Windows
    winyx = (20,30)
    win = curses.newwin(20,30,0,0)#height,width,y,x 
    win1 = curses.newwin(20,50,0,30)
    win2 = curses.newwin(20,30,20,0)
    navigation = [(win,itemsN),(win2,testItems)]
    #loop
    while True: 
        #Draw order
        win1.clear()
        win1.addstr(1,1,str(len(itemsN)))
        win1.addstr(2,1,str(current_row_idx))
        win1.addstr(3,1,str(current_col_idx))
        win1.addstr(4,1,str())
        winFrame(win1,20,50)
        win1.refresh()
        
        menuList(current_row_idx,current_col_idx,0,navigation,True)
        menuList(current_row_idx,current_col_idx,1,navigation,True)
        winFrame(win,winyx[0],winyx[1])
        winFrame(win2,20,30)
        win2.refresh()
        key = win.getch()#in ASCII code  
        
        #Keymanaging
        keymanagerQuit(key)
        current_row_idx = keymanagerList(key,current_col_idx,current_row_idx,navigation)
        current_col_idx,current_row_idx = keymanagerTab(key,current_col_idx,current_row_idx,navigation)
        
        #Clear
        stdscr.clear()

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

#sets color of Text
def setColor(pairName,text,y,x,win=stdscr):
    #colorpair --> name,color-foreground, color-background
    win.attron(curses.color_pair(pairName))
    win.addstr(y,x,text)
    win.attroff(curses.color_pair(pairName))  

#TODO: finish
def updateAll():
    pass

#run main() in wrapper
if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except timeToQuit:
        exit()
    #finally:    would work but to error message
    #    exit()
