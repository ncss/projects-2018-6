from quokka import *
from pokemon_img import venusaur
from improved_display import *

# TODO Dummy list
pokemon_list = ['venusaur']
# venusaur = venusaur.split('\n')
# venusaur_buffer = SpecialFrameBuffer(bytearray(392), 56, 56, framebuf.MONO_VLSB)
# venusaur_buffer.draw_image(venusaur, [0, 0])

imgs = {
        'venusaur' : venusaur.split('\n')
        }

display = ImprovedQuokkaDisplay(display.spi)

# Initialise the states
CALIBRATE = 0
CONNECT_SERVER = 1
CHOOSE_POKEMON = 2
CHOOSE_MOVE = 3
READ_ZMOVE = 4
TRANSFER_BATTLE = 5
DISPLAY_TURN = 6
RESULT_SCREEN = 7
RESET = 8

state = CALIBRATE

def calibrate():
    return CONNECT_SERVER

def connect_to_server():
    msg = radio.receive()

    return CHOOSE_POKEMON

    connected = False
    last_attempt_time = running_time()

    # While the server hasn't got all clients connected
    while msg != "server_ready":
        if msg == "confirm":
            connected = True

        # If this client hasn't connected, attempt to connect every half second
        if not connected and running_time()-last_attempt_time > 500:
            last_attempt_time = running_time()
            radio.send('connect')

        msg = radio.receive()

    return CHOOSE_POKEMON

def choose_pokemon():
    '''
    Draw the choose pokemon screen and handle the buttons
    '''
    global pokemon_list

    pokemon_indices = [0, 0]
    selection = 0

    start = running_time()
    while True:
        if selection < 2:
            # Display is 128 x 64
            # button.a = A button
            # button.d = B button
            # button.b = C button
            # button.c = D button
            if buttons.a.was_pressed():
                pokemon_indices[selection]  = (pokemon_indices[selection]-1)%len(pokemon_list)
            if buttons.d.was_pressed():
                pokemon_indices[selection]  = (pokemon_indices[selection]+1)%len(pokemon_list)
            if buttons.b.was_pressed():
                selection += 1

        # Draw the screen
        display.fill(1)
        if selection < 2:
            # Draw pokemon
            display.draw_image(imgs[pokemon_list[pokemon_indices[selection]]], [36, 4])

            # Draw the arrows and push them toward the edges if the button is held
            display.text('<', 10-5*int(buttons.a.is_pressed()), 28, 0)
            display.text('>', 110+5*int(buttons.d.is_pressed()), 28, 0)
        else:
            # Draw the waiting message
            display.text('Waiting for', 20, 22, 0)
            display.text('server...', 28, 34, 0)

            return CHOOSE_MOVE

            msg = radio.receive()
            last_attempt_time = running_time()-500
            connected = False

            while msg != "start_battle":
                if msg == "confirm":
                    connected = True

                if not connected and running_time()-last_attempt_time > 500:
                    last_attempt_time = running_time()
                    # TODO Send the required information about the pokemon to the server
                    radio.send('|'.join([str(a) for a in pokemon_indices]))

                msg = radio.receive()

            return CHOOSE_MOVE

        display.show()

        if running_time()-start < 33:
            sleep(int(33.34-(running_time()-start)))
    return CHOOSE_POKEMON

def choose_move():
    # TODO get the actual move list
    moves = ['move1', 'move2', 'move3']

    move_selector = 0

    while True:
        display.fill(1)

        # Iterate the possible moves, and draw them
        # Also draw an indicator of the current selection
        for l, line in enumerate(moves):
            y = 10+18*l
            display.text('>'*int(l == move_selector)+' '+line, 20, y, 0)

        display.show()

        # If the A button is pressed, iterate the selector
        # If the C button is pressed, make the selection
        if buttons.a.was_pressed():
            move_selector = (move_selector+1)%len(moves)
        if buttons.b.was_pressed():
            # TODO store the move choice somewhere
            return READ_ZMOVE

def read_zmove():
    # TODO get the quality of the z-move in range 1-10
    quality = 5

    return TRANSFER_BATTLE

def transfer_battle():
    # Part 1, send the info
    # TODO send the move to the server
    message = ''
    msg = radio.receive()
    last_attempt_time = running_time()-500

    while msg != "confirm":
        if running_time()-last_attempt_time > 500:
            last_attempt_time = running_time()
            # TODO Send the required information about the turn to the server
            radio.send('action:'+message)

        msg = radio.receive()

    # Part 2, receive the results back and send a confirmation
    msg = radio.receive()
    while not msg or not msg.startswith('action:'):
        msg = radio.receive()
    # TODO Store the turn information messages, then send confirmation

    radio.send('confirm')

    # TODO determine if the game is over or not
    # Set state as necessary
    return DISPLAY_TURN

def display_turn():
    # TODO display the battle actions however we want to

    return CHOOSE_MOVE

def result_screen():
    # TODO get the actual result
    result = "You Won!"

    while not buttons.c.was_pressed():
        display.fill(1)

        display.text(result, (128-8*len(result))//2, 28, 0)

        display.show()

    return RESET
