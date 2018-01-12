from quokka import *

# TODO Dummy list
pokemon_list = ['a']

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

    while msg != "server_ready":
        if msg == "confirm":
            connected = True

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

    # Draw the pokemon
    start = running_time()
    while True:
        if selection < 2:
            # button.a = A button
            # button.b = C button
            # button.c = D button
            # button.d = B button
            if buttons.a.was_pressed():
                pokemon_indices[selection]  = (pokemon_indices[selection]-1)%len(pokemon_list)
            if buttons.d.was_pressed():
                pokemon_indices[selection]  = (pokemon_indices[selection]+1)%len(pokemon_list)
            # This is actually a c button press. It's just a bug with the Quokka
            if buttons.b.was_pressed():
                selection += 1

        # TODO Draw the screen
        display.fill(1)
        if selection < 2:
            # TODO Draw pokemon
            pass
        else:
            # Draw the waiting message
            display.text('Waiting for', 20, 22, 0)
            display.text('server...', 28, 34, 0)
            pass
        # Display is 128 x 64
        display.show()

        if running_time()-start < 33:
            sleep(int(33.34-(running_time()-start)))
    return CHOOSE_POKEMON
