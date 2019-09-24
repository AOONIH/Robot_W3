
def control_motor(con, red_center, green_center, window_size):
    #only chase green
    if green_center is None:
        con.write(b"S")
    elif green_center[0] < window_size * 0.45:
        con.write(b"L")
    elif green_center[0] > window_size * 0.55:
        con.write(b"R")
    else:
        con.write(b"F")
