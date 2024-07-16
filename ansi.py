import termios, sys, tty
stdin = sys.stdin.fileno()
termios_old = termios.tcgetattr(stdin)


def reset_console():
    global termios_old, stdin
    try:
        termios.tcsetattr(stdin, termios.TCSANOW, termios_old)
        return True
    finally:
        return False

def setup_console():
    global termios_old, stdin
    new = termios.tcgetattr(stdin)
    new[3] = new[3] & ~(termios.ECHO|termios.ICANON)          # lflags
    try:
        termios.tcsetattr(stdin, termios.TCSANOW, new)
        tty.setraw(stdin)
        return True
    finally:
        termios.tcsetattr(stdin, termios.TCSANOW, termios_old)
        return False
def readchar():
    tty.setraw(sys.stdin.fileno())
    return sys.stdin.read(1)

def print_raw(string):
        print(string, end='', flush=True)

print_raw("\033[4mName: ")
while True:
    c = readchar()
    if c=="\n" or c=="q":
        print("\n OKKKK!")
        break
    else:
        print_raw(" "+c)
reset_console()

