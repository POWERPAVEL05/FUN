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
def menuSSID(selected_row,listItems,win):
    #h, w = win.getmaxyx()
    try:
        for idx,item in enumerate(listItems):
            x= 1
            y = 0 + idx
            if idx > 15: break
            if idx == selected_row:
                setColor(1,str(item),y,x,win)
            else:
                win.addstr(y,x,item)
    except:
        pass #list to long -->  TODO: add error log?
    win.refresh()

#Everything is run from here:Initiating/Updating of windows, row and soon to come focus_idx etc.
def main(stdscr):
    #Init segment
    initColors()
    curses.curs_set(0)#cursor invisible
    current_row_idx = 0
    key = 0
    #splash screen
    stdscr.addstr(0,0,"FUN - is fetching data")
    stdscr.refresh()
    itemsN = getSSID(15)
    win = curses.newwin(20,30,0,0)
    win.refresh()
    while True: 
        #Draw order
        menuSSID(current_row_idx,itemsN,win)
        key = win.getch() 
        #Keymanager
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
        #Clear
        stdscr.clear()

#gibt Liste von SSID wieder und Laenge der Liste
#beakpoint specifies amount

#TODO: handle 'I'm unkwown' and same routres emitting multiple singnals 
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

def init():
    curses.curs_set(0)

def updateAll():
    pass

if __name__ == "__main__":
    curses.wrapper(main)

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
