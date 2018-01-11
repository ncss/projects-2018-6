from quokka import *
import radio

CHANNEL = 8

radio.on()
radio.config(length=251, channel=CHANNEL)

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

def connect_to_server():
    global state

    msg = radio.receive()

    connected = False
    last_attempt_time = running_time()

    while msg != "server_ready":
        if msg == "confirm":
            connected = True

        if not connected and running_time()-last_attempt_time > 500:
            last_attempt_time = running_time()
            radio.send('connect')

        msg = radio.receive()

    state = CHOOSE_POKEMON

while True:
    if state == CALIBRATE:
        state = CONNECT_SERVER

    elif state == CONNECT_SERVER:
        connect_to_server()

    elif state == CHOOSE_POKEMON:
        pass

    elif state == CHOOSE_MOVE:
        pass

    elif state == READ_ZMOVE:
        pass

    elif state == TRANSFER_BATTLE:
        pass

    elif state == DISPLAY_TURN:
        pass

    elif state == RESULT_SCREEN:
        pass

    elif state == RESET:
        reset()
