import curses
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
def menu(selected_row):
    h, w = stdscr.getmaxyx()
    curses.init_pair(1,curses.COLOR_BLACK,curses.COLOR_WHITE)
    for idx,item in enumerate(menuItems):
        x=w//2 - len(item)//2
        y=h//2 - len(menuItems)+idx
        if idx == selected_row:
            setColor(1,item,y,x)
        else:
            stdscr.addstr(y,x,item)
    stdscr.refresh()

def main(stdscr):
    #cursor invisible
    curses.curs_set(0)
    current_row_idx = 0
    #colorpair --> name,color-foreground, color-background
    #curses.init_pair(1,curses.COLOR_RED,curses.COLOR_BLUE)
    while True:
        menu(current_row_idx)
        key = stdscr.getch()
        stdscr.addstr(0,0,str(key))
        stdscr.refresh()
        if key == 113:
            exit()
        elif key == 107:
            if current_row_idx == 0:
                current_row_idx = len(menuItems)-1
            else:
                current_row_idx += -1
        elif key == 106:
            if current_row_idx == len(menuItems)-1:
                current_row_idx = 0
            else:
                current_row_idx += 1
        stdscr.clear()
        stdscr.addstr(0,0,"Up")

def setColor(pairName,text,y,x):
    stdscr.attron(curses.color_pair(pairName))
    stdscr.addstr(y,x,text)
    stdscr.attroff(curses.color_pair(pairName))

if __name__ == "__main__":
    curses.wrapper(main)

