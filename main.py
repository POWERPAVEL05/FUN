import curses
import subprocess

stdscr = curses.initscr()

#Colors
def initColors():
    curses.init_pair(1,curses.COLOR_BLACK,curses.COLOR_WHITE)

#Takes list and displays vertical Menu, naviagate up and down through items, needs selected_row for cursor 
#TODO: make more dynamic
#TODO: account for multiple signals with same SSID
def menuSSID(selected_row,selected_win,winId,listItems,win,frame=False):
    #h, w = win.getmaxyx()
    #adds padding to window if frame is included
    frameVar = 0
    if frame:
        frameVar = 1
    try:
        for idx,item in enumerate(listItems):
            x= 0  +frameVar
            y = 0 + idx + frameVar
            if idx == selected_row and selected_win == winId :
                setColor(1,str(item),y,x,win)
            else:
                win.addstr(y,x,item)
    except:
        pass
    
    win.refresh()

#draw bar across window
def drawBar(win):
    height, width = stdscr.getmaxyx()
    for i in range(width-1):
        win.addch(0,i,"█")
    win.refresh()

#draw Frame around window, y x defined due resizing issues
def winFrame(win,y,x):
    height,width = y,x
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

#raised when quitting tui
class timeToQuit(Exception):pass

#for quitting application
def keymanagerQuit(key):
    if key == ord("q"):
            #incase of failure in other systems
        raise timeToQuit
    else:
        pass

#moving up and down focused list
def keymanagerList(key,current_col_idx,current_row_idx,navigation): 
    items = (navigation[current_col_idx])[0]
    if key == ord("k"):
        if current_row_idx == 0:
            return len(items)-1
        else:
            current_row_idx += -1
            return current_row_idx
    elif key == ord("j"):
        if current_row_idx == len(items)-1:
            return 0
        else:
            current_row_idx +=1
            return current_row_idx
    else:
        return current_row_idx

#for moving around tabs which are soon to come
def keymanagerTab(key,current_col_idx,current_row_idx,navigation):
    items = navigation
    if key == ord("h"):
        if current_col_idx == 0:
            return (len(items)-1,0)
        else:
            current_col_idx += -1
            return (current_col_idx,0)
    elif key == ord("l"):
        if current_col_idx == len(items)-1: #max
            return (0,0)
        else:
            current_col_idx += 1
            return (current_col_idx,0)
    else:
        return current_col_idx, current_row_idx

#Everything is run from here:Initiating/Updating of windows, row and soon to come focus_idx etc.
def main(stdscr):
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
    #winBar = curses.newwin(2,width-1,height-1,0)
    #win1.refresh()

    allWindows = [win,win2]

    navigation = [[itemsN],[testItems]]
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
        
        #winBar.refresh()
        '''
        try:
            drawBar(winBar)
        except:
            height, width = stdscr.getmaxyx()
            winBar = curses.newwin(10,width-1,height-1,0)
            winBar.refresh()
        winBar.refresh()
        '''
        menuSSID(current_row_idx,current_col_idx,0,itemsN,win,True)
        menuSSID(current_row_idx,current_col_idx,1,testItems,win2,True)
        winFrame(win,winyx[0],winyx[1])
        winFrame(win2,20,30)
        win2.refresh()
        key = win.getch()#in ASCII code  
        #win.addstr(20,0,str(current_row_idx))
        
        #Keymanaging
        keymanagerQuit(key)
        current_row_idx = keymanagerList(key,current_col_idx,current_row_idx,navigation)
        current_col_idx,current_row_idx = keymanagerTab(key,current_col_idx,current_row_idx,navigation)
        
        #Clear
        stdscr.clear()

#gibt Liste von SSID wieder und Laenge der Liste
#beakpoint specifies amount
#TODO: handle 'I'm unkwown' and same routers emitting multiple singnals 
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
'''

        if key == ord("q"):
            #incase of failure in other systems
            curses.curs_set(1)
            curses.nocbreak()
            stdscr.keypad(False)
            curses.echo()
            exit()#curses.endwin() does not work, my fault?
        elif key == ord("k"):
            if current_row_idx == 0:
                current_row_idx = len(itemsN)-1
            else:
                current_row_idx += -1
        elif key == ord("j"):
            if current_row_idx == len(itemsN)-1:
                current_row_idx = 0
            else:
                current_row_idx += 1
'''
'''
def main(win):
    win.nodelay(True)
    key = ""
    win.clear()
    win.addstr("Detected key:")

    prev =""
    while True:
        try:
            key = win.getkey()
            prev = str(prev)+str(key)
            win.clear()
            win.addstr("Detected key:")
            win.addstr(str(prev))
            if key == os.linesep:
                break
        except Exception:
            # No input
            pass

curses.wrapper(main)
'''
