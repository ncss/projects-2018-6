from microbit import *

import radio
current_score = 0
radio.on()
radio.config(channel=6)
prefix = 'tw:scr:9'

while True:
    
    msg = radio.receive()
    
    if msg:
        print(msg)
        try:
            game, scr, score = msg.split(':')
        except ValueError:
            continue
        if game == 'tw' and scr == 'scr':
            current_score = int(score)
            if current_score == -1:
                display.scroll('Game Over')
                display.show(Image.NO)
            else:
                display.scroll(str(current_score))
    elif current_score == 0:
        display.show('0')
    else:  
        display.scroll(str(current_score))

        