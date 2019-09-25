def control_motor(con, red_center, green_center, window_width):
    #only chase green
    if green_center is None:
        con.write(b"S")
    elif green_center[0] < window_width * 0.3:
        con.write(b"L")
    elif green_center[0] > window_width * 0.7:
        con.write(b"R")
    else:
        con.write(b"F")
