#old code i want to keep in mind
'''
try:
   drawBar(winBar)
except:
   height, width = stdscr.getmaxyx()
   winBar = curses.newwin(10,width-1,height-1,0)
   winBar.refresh()
   winBar.refresh()
'''
        
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
