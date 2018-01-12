from microbit import *
import radio
radio.on()
threshold = 1900
radio.config(length=251, channel=3)
display.show("L")

status = None

while True:
    x = accelerometer.get_x()
    if status:
        if status == True:
            if x < -threshold:
                status = False
                radio.send("Left_1")
        elif status == False:
            if x > threshold:
                status = True
                radio.send("Left_1")
    else:
        if x < -threshold:
                status = False
                radio.send("Left_1")
        if x > threshold:
                status = True
                radio.send("Left_1")