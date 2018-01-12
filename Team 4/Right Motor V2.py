from microbit import *
import radio
radio.on()

radio.config(length=251, channel=3)
display.show("R")
threshold = 1900
status = None

while True:
    x = accelerometer.get_x()
    if status:
        if status == True:
            if x < -threshold:
                status = False
                radio.send("Right_1")
        elif status == False:
            if x > threshold:
                status = True
                radio.send("Right_1")
    else:
        if x < -threshold:
                status = False
                radio.send("Right_1")
        if x > threshold:
                status = True
                radio.send("Right_1")