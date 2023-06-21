import curses
import serial
import time

arduino = serial.Serial('COM9',9600,timeout=1)
#time.sleep(0.02)

screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)

try:
    while True:
        char = screen.getch()
        if char == ord('q'):
            break
        elif char == curses.KEY_UP:
            arduino.write(b'f')
        elif char == curses.KEY_DOWN:
            arduino.write(b'b')
        elif char == curses.KEY_RIGHT:
            arduino.write(b'r')
        elif char == curses.KEY_LEFT:
            arduino.write(b'l')
        elif char == ord(' '):
            arduino.write(b's')
        else:
            arduino.write(b's')
finally:
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()


