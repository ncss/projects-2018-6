from microbit import *
import radio

radio.on()
radio.config(channel=6)

display.scroll('Ready?')
while True:
    msg = radio.receive()
    
    if msg and msg.s  tartswith('tw:dsp:'):
        print(msg)
        protocol, cmd, position = msg.split(':')
        if position == 'LHAND':
            display.show(Image.ARROW_NW)
        elif position == 'RHAND':
            display.show(Image.ARROW_NE)
        elif position == 'RFOOT':
            display.show(Image.ARROW_SE)
        elif position == 'LFOOT':
            display.show(Image.ARROW_SW)
            
        #sleep(timer*1000)
        #timer = timer*0.9