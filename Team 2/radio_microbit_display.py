from microbit import *
import radio
import music

radio.on()
radio.config(channel=6)

foot_sound = 'C6:6'
hand_sound = 'C4:6'

timer = 10

while True:
    msg = radio.receive()
    
    if msg:
        cmd, position = msg.split(':')
        if cmd == 'dsp_side':
            if position == 'RIGHT':
                display.show(Image.ARROW_E, wait = False)
            elif position == 'LEFT':
                display.show(Image.ARROW_W, wait = False)
        
        if cmd == 'dsp_limb':
            if position == 'HAND':
                music.play(hand_sound, wait = False)
            elif position == 'FOOT':
                music.play(foot_sound, wait = False)
            
        sleep(timer*1000)
        timer = timer*0.9