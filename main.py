import curses
from keymanagers import timeToQuit,keymanagerQuit,keymanagerList,keymanagerTab,keymanagerSelect,keymanagerStatus,keymanagerRefresh
from netTools import getSSID,connect
stdscr = curses.initscr()
#41,147

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
    win.addstr(0,2,"win")
    #scuffed fix, curses tries to move curses to next line, even when there is none --> error

#don't know if this works
#is supposed to icut out some lines
def makeWin(height,width,y,x,windowList):
    id = str(windowList.len())
    name = "win"+id
    name = curses.newwin(height,width,y,x)
    windowList.append(name)

def refreshWin(win):
    win.refresh()
#Everything is run from here:Initiating/Updating of windows, row and soon to come focus_idx etc.
def main(stdscr):
    #Init segment
    testItems = ['1','2','3','4']
    initColors()
    curses.curs_set(0)#cursor not invisible --> 0
    current_row_idx = 0 #row of window
    current_col_idx = 0 #Window
    key = 0
    command = ""
    wifiState = True #TODO: set based on nmcli
    interactiveMode = True
    enterText = ""
    saveCommand = ""
    
    #splash screen
    height, width = stdscr.getmaxyx()
    stdscr.addstr(0,0,"FUN - is fetching data")
    stdscr.refresh()
    netList = getSSID(18,True)

    #init Windows
    winyx = (20,30)
    win = curses.newwin(20,30,0,0)#height,width,y,x 
    win1 = curses.newwin(20,35,0,60)
    win2 = curses.newwin(20,30,0,30)
    win3 = curses.newwin(5,45,30,0)
    navigation = [(win,netList),(win2,testItems)]
    #loop
    while True: 
        #Draw order
        win1.clear()
        #add stuff to win1
        #win1.addstr(1,1,str(len(netList)))
        win1.addstr(2,1,str(current_row_idx))
        win1.addstr(3,1,str(current_col_idx))
        infoTemp ="height,width:"+str((height,width))
        win1.addstr(4,1,infoTemp)
        statusTemp = ("Wifi on:"+str(wifiState))
        win1.addstr(5,1,statusTemp)
        try:
            win1.addstr(6,1,chr(key)+str(key))
        except:
            win1.addstr(6,1,"")
        win1.addstr(7,1,str(interactiveMode))
        win1.addstr(8,1,enterText)
        winFrame(win1,20,35)
        win1.refresh()
        
        winFrame(win,winyx[0],winyx[1])
        winFrame(win2,20,30)
        menuList(current_row_idx,current_col_idx,0,navigation,True)#win
        menuList(current_row_idx,current_col_idx,1,navigation,True)#win2
        
        win3.clear()
        win3.addstr(1,0,str(command))
        win3.addstr(2,0,str(saveCommand)+" Password: "+str(enterText))
        win3.refresh()
        
        #Keymanaging/Update states etc
        key = win.getch()#in ASCII code  
        keymanagerQuit(key)
        if(interactiveMode):
            current_row_idx = keymanagerList(key,current_col_idx,current_row_idx,navigation)
            current_col_idx,current_row_idx = keymanagerTab(key,current_col_idx,current_row_idx,navigation)
            command = keymanagerSelect(key,current_col_idx,current_row_idx,navigation)
            wifiState = keymanagerStatus(key,wifiState)
            netList = keymanagerRefresh(key,netList)
            if key == ord("i"):
                interactiveMode = False
        #enter text mode
        else:
            #press ESC to leave text mode
            if key == 27:
                enterText = ""
                command = False
                interactiveMode = True
            #backspace
            elif key == 127:
                enterText = enterText[:-1]
            #enter to connect
            elif key == ord("\n"):
                interactiveMode = True
                command = "loading"
                win3.refresh()
                connect(str(saveCommand),str(enterText))
                command = False
                enterText = "done"
                saveCommand = ""
            else:
                #set limit
                if len(enterText)<=30:
                    enterText = enterText + chr(key)
                else:
                    pass
        #Press enter in menuList containing List of network names
        if command!=False and navigation[current_col_idx][1] == netList:
            saveCommand = command
            command = False
            interactiveMode = False
        else:
            pass
        #Clear
        stdscr.clear()

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
