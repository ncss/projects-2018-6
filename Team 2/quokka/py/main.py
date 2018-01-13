import quokka
import random

r = 0
g = 0
b = 0

colours =  ['RED', 'GREEN', 'YELLOW', 'BLUE']
sides = ['L', 'R']
limbs = ['HAND', 'FOOT']
colours_dict = {"GREEN":0, "YELLOW":1, "BLUE":2, "RED":3}

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

#send limb and side to MB display
def body_show(current_side, current_limb):
    quokka.radio.send('tw:dsp:'+ current_side + current_limb)

#reset the turn - screen, timer, colours, neopixels
def turn_reset():
    r = 0
    g = 0
    b = 0
    quokka.display.fill(1)
    quokka.display.show()
    quokka.neopixels.clear()
    quokka.neopixels.show()
    #timer = timer*0.9
    #quokka.sleep(500)
    #return timer

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
    points = 0

    # start screen
    started = False
    if quokka.buttons.a.was_pressed():

        start_sequence()

        #Twister

        while lives > 0:
            prev_sum = [0]*4
            #control turns by button pressed
            if quokka.buttons.b.was_pressed() or started:
                started = True
                quokka.radio.send('tw:scr:' + str(points))
            #Gameplay positions

                # colour show and select
                current_colour = random.choice(colours)
                colour_show(current_colour, r, g, b)

                #temporary body:
                current_limb = random.choice(limbs)
                current_side = random.choice(sides)
                body_show(current_side, current_limb)

                start_time = quokka.running_time()
                elapse_time = quokka.running_time() - start_time


                while elapse_time < 5000:
                    msg = quokka.radio.receive()
                    if current_colour == "RED":
                        quokka.sleep(2000)
                        points += 1
                        break

                    if msg:
                        try:
                            protocol, cmd, array = msg.split(":")
                            if protocol == "tw" and cmd=="btn":
                                buttons = []
                                for line in array.split(';'):
                                    buttons.append(line.split(","))
                        except ValueError:
                            continue

                        # list of integers, showing num of buttons pressed in each row
                        #if current_colour
                        curr_sum = sum(map(bool, buttons[colours_dict[current_colour]]))


                        if prev_sum[colours_dict[current_colour]] != curr_sum:
                        #colour_pressed = any(buttons[colours_dict[current_colour]])
                        #if colour_pressed:
                            prev_sum[colours_dict[current_colour]] = curr_sum
                            points += 1
                            break

                    elapse_time = quokka.running_time() - start_time

                turn_reset()



            if quokka.buttons.c.was_pressed():
                quokka.radio.send('tw:scr:-1')

                #timer = turn_reset(timer)


                #lives overide for incorrect move - decrease score by 1

            #Gameover Sequence

'''
                turn_over = False
                while not turn_over:
                    msg = quokka.radio.receive()


                        delta = []

                        # if decrease in one that isnt the correct colour, lose life

                        # elif increase in correct one, turn_over = True
                        # else do nothing
                        current_colour
        '''
