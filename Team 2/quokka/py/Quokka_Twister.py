import quokka
import random

r = 0
g = 0
b = 0

colours =  ['RED', 'GREEN', 'YELLOW', 'BLUE']
sides = ['LEFT', 'RIGHT']
limbs = ['HAND', 'FOOT']

start_statements = ['Ready?', '3' , '2', '1']

quokka.radio.enable()
quokka.radio.config(channel=6)

#show colour on neopixels
def colour_show(current_colour, r, g, b):
    if current_colour == 'RED':
        r = 255
    if current_colour == 'GREEN':
        g = 255
    if current_colour == 'YELLOW':
        r =255
        g =150
    if current_colour == 'BLUE':
        b =255
    quokka.neopixels.clear()
    for i in range(8):
        quokka.neopixels.set_pixel(i, r, g, b)
        quokka.neopixels.show()
        quokka.sleep(5)

#show side on microbit display
def side_show(current_side):
    quokka.radio.send('dsp_side:'+ current_side)

#temporary limb and side
def limb_show(current_limb):
    quokka.radio.send('dsp_limb:'+ current_limb)

#reset the turn - screen, timer, colours, neopixels
def turn_reset(timer):
    quokka.sleep(int(timer*1000))
    r = 0
    g = 0
    b = 0
    quokka.display.fill(1)
    quokka.display.show()
    quokka.neopixels.clear()
    quokka.neopixels.show()
    timer = timer*0.9
    quokka.sleep(500)
    return timer

#Start Repeating countdown
def start_sequence():
    for word in start_statements:
        quokka.display.fill(1)
        quokka.display.text(word, 5, 5, 0)
        quokka.display.show()
        quokka.sleep(1000)
    quokka.display.fill(1)
    quokka.display.show()

quokka.neopixels.clear()
quokka.neopixels.show()
quokka.display.fill(0)
quokka.display.show()

while True:

    timer = 10
    lives = 2

    # start screen

    if quokka.buttons.a.was_pressed():
        start_sequence()

        #Twister

        while lives > 0:

        #Gameplay positions

            # colour show and select
            current_colour = random.choice(colours)
            colour_show(current_colour, r, g, b)


            #temporary body:
            current_limb = random.choice(limbs)
            current_side = random.choice(sides)
            limb_show(current_limb)
            side_show(current_side)

            print(current_colour + ' ' + current_side + ' ' + current_limb)
            timer = turn_reset(timer)


        #Gameover Sequence
