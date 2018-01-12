from microbit import *
import radio
radio.on()
radio.config(length=251, channel=3)
counter = 0
display.show(str(counter))

while True:
    msg = radio.receive()
    if msg:
        if msg == "Left_1":
            counter += 1
            display.show(str(counter))
            print (counter)
