"""Arrow-key menu selector."""
import sys

def pick(opts: list, hdr: str = "") -> int:
    """Arrow-key picker. Up/down to navigate, Enter to select."""
    if len(opts) < 2: return -1
    import termios, tty
    sel = 0
    nlines = len(opts) + 1
    print()
    while True:
        sys.stdout.write("\033[" + str(nlines) + "A\033[J")
        print("  " + hdr + ":")
        for i, o in enumerate(opts):
            print(("  > " if i == sel else "    ") + o)
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch == '\x1b':
                ch += sys.stdin.read(2)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        if ch in ('\r', '\n'):
            break
        if ch == '\x1b[A':
            sel = (sel - 1) % len(opts)
        elif ch == '\x1b[B':
            sel = (sel + 1) % len(opts)
        elif ch in ('\x1b', '\x03'):
            sys.stdout.write("\033[J")
            return -1
    return sel
