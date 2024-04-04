def av():
    global t
    global x
    global y
    global ly
    if ly == 4:
        if t == 1:
            x = 4
            y = 0
        elif t == 9:
            x = 0
            y = 4
        elif t == 10:
            x = -4
            y = 0
        elif t == 19:
            x = 0
            y = -4
        elif t == 28:
            x = 4
            y = 0
            t = 0
            ly = 0
        elif t == 29:
            x = 4
            y = 0
            t = 0
            ly = 0
    elif t == 1:
        x = 4
        y = 0
    elif t == 9:
        x = 0
        y = 4
    elif t == 10:
        x = -4
        y = 0
    elif t == 18:
        x = 0
        y = 4
        t = 0
        ly += 1
