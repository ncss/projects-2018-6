from microbit import *

import radio

radio.on()
radio.config(channel = 6)
prefix = 'tw:scr'

while True:
    
    score = radio.receive()
    
    if score:
        if score.startswith(prefix):
                display.show(score)