import curses
import subprocess
import sys
import time
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

stdscr = curses.initscr()
menuItems = ["Start","Options","Help","Quit"]
def menu(selected_row,listItems):
    h, w = stdscr.getmaxyx()
    curses.init_pair(1,curses.COLOR_BLACK,curses.COLOR_WHITE)
    for idx,item in enumerate(listItems):
        x=w//2 - len(item)//2
        #y=h//2 - len(listItems)+idx
        y = 0 + idx
        if idx == selected_row:
            setColor(1,str(item),y,x)
        else:
            stdscr.addstr(y,x,item)
    #stdscr.refresh()

def main(stdscr):
    #cursor invisible
    curses.curs_set(0)
    current_row_idx = 0
    #colorpair --> name,color-foreground, color-background
    #curses.init_pair(1,curses.COLOR_RED,curses.COLOR_BLUE)
    #stdscr.nodelay(True)
    #timeTemp = time.time()
    key = 0
    itemsN = getSSID()
    print(menuItems)
    print(itemsN)
    while True: 
        menu(current_row_idx,itemsN)
        #test = str(info)
        #stdscr.addstr(0,0,test)
        key = stdscr.getch()
        stdscr.refresh()
        if key == 113:
            exit()
        elif key == 107:
            if current_row_idx == 0:
                current_row_idx = len(itemsN)-1
            else:
                current_row_idx += -1
        elif key == 106:
            if current_row_idx == len(itemsN)-1:
                current_row_idx = 0
            else:
                current_row_idx += 1
        stdscr.refresh()
        stdscr.clear()

#gibt Liste von SSID wieder und Laenge der Liste
def getSSID():
    ssid = subprocess.run(["nmcli","-f" ,"SSID","-c","no","-t","d","w"],text=True,capture_output=True)
    nameList = str(ssid.stdout).split()
    return nameList


def setColor(pairName,text,y,x):
    stdscr.attron(curses.color_pair(pairName))
    stdscr.addstr(y,x,text)
    stdscr.attroff(curses.color_pair(pairName))
    
if __name__ == "__main__":
    curses.wrapper(main)

