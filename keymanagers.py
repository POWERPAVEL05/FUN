class timeToQuit(Exception):pass
#for quitting application
def keymanagerQuit(key):
    if key == ord("q"):
        raise timeToQuit
    else:
        pass
def keymanagerSelect(key,current_col_idx,current_row,navigation):
    items = (navigation[current_col_idx][1])
    win = (navigation[current_col_idx][0])
    if key == ord("\n"):
        return str(items[current_row])
    else:
        return "Nothing selected"

#moving up and down focused list
def keymanagerList(key,current_col_idx,current_row_idx,navigation): 
    items = (navigation[current_col_idx][1])
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
#switch between focusable(in navigation) windows
def keymanagerTab(key,current_col_idx,current_row_idx,navigation):
    tabs = navigation
    if key == ord("h"):
        if current_col_idx == 0:
            return (len(tabs)-1,0)
        else:
            current_col_idx += -1
            return (current_col_idx,0)
    elif key == ord("l"):
        if current_col_idx == len(tabs)-1: #max
            return (0,0)
        else:
            current_col_idx += 1
            return (current_col_idx,0)
    else:
        return current_col_idx, current_row_idx

