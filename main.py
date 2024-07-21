import curses
import subprocess

menuItems = ["Start","Options","Help","Quit"]
stdscr = curses.initscr()

#Colors
def initColors():
    curses.init_pair(1,curses.COLOR_BLACK,curses.COLOR_WHITE)

#Takes list and displays vertical Menu, naviagate up and down through items, needs selected_row for cursor 
#TODO: make more dynamic
#TODO: account for multiple signals with same SSID
def menuSSID(selected_row,listItems,win,frame=False):
    #h, w = win.getmaxyx()
    #adds padding to window if frame is included
    frameVar = 0
    if frame:
        frameVar = 1
    try:
        for idx,item in enumerate(listItems):
            x= 0  +frameVar
            y = 0 + idx + frameVar + 1
            #if idx > 15: break
            if idx == selected_row:
                setColor(1,str(item),y,x,win)
            else:
                win.addstr(y,x,item)
    except:
        pass #list to long -->  TODO: add error log?
    
    win.refresh()

#draw frame around border of window
def winFrame(win):
    height,width = win.getmaxyx()
    for w in range(width-2):
        win.addstr(0,w+1,"═")
        win.addstr(height-1,w+1,"═")
    for h in range(height-2):
        win.addstr(h+1,0,"║")
        win.addstr(h+1,width-2,"║")

def keymanagerQuit(key):
    if key == ord("q"):
            #incase of failure in other systems
            curses.curs_set(1)
            curses.nocbreak()
            stdscr.keypad(False)
            curses.echo()
            exit()#curses.endwin() does not work, my fault?
    else:
        pass

def keymanagerList(key,current_row_idx,items): 
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

def keymanagerTab(key,current_col_idx,items):
    if key == ord("l"):
        if current_col_idx == 0:
            return len(items)
        else:
            current_col_idx -= 1
            return current_col_idx
    elif key == ord("h"):
        if current_col_idx == len(items): #max
            current_col_idx = 0 
        else:
            current_col_idx += 1

#Everything is run from here:Initiating/Updating of windows, row and soon to come focus_idx etc.
def main(stdscr):
    #Init segment
    initColors()
    curses.curs_set(0)#cursor invisible
    current_row_idx = 0
    current_col_idx = 0 #Window
    key = 0
    
    #splash screen
    stdscr.addstr(0,0,"FUN - is fetching data")
    stdscr.refresh()
    itemsN = getSSID(17)
    win = curses.newwin(30,30,0,0)#height,width,y,x
    win1 = curses.newwin(20,30,0,30)
    win1.refresh()
    
    #loop
    while True: 
        #Draw order
        #winFrame(win)
        win1.addstr(0,0,str(len(itemsN)))
        win1.addstr(1,0,str(current_row_idx))
        win1.refresh()
        
        menuSSID(current_row_idx,itemsN,win,True)
        key = win.getch()#in ASCII code  
        #win.addstr(20,0,str(current_row_idx))
        #Keymanaging
        keymanagerQuit(key)
        win1.clear()
        current_row_idx = keymanagerList(key,current_row_idx,itemsN)
        current_col_idx = 0 #keymanagerTab(key,current_col_idx,itemsN)
        
        #Clear
        stdscr.clear()

#gibt Liste von SSID wieder und Laenge der Liste
#beakpoint specifies amount
#TODO: handle 'I'm unkwown' and same routers emitting multiple singnals 
def getSSID(breakpoint = None):
    ssid = subprocess.run(["nmcli","-f" ,"SSID","-c","no","-t","d","w"],text=True,capture_output=True)
    nameList = str(ssid.stdout).split("\n")
    if breakpoint == None:
        return nameList
    else:
        return nameList[:breakpoint]

def setColor(pairName,text,y,x,win=stdscr):
    #colorpair --> name,color-foreground, color-background
    win.attron(curses.color_pair(pairName))
    win.addstr(y,x,text)
    win.attroff(curses.color_pair(pairName))  

def updateAll():
    pass

if __name__ == "__main__":
    curses.wrapper(main)

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
