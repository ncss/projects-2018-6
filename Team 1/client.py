from quokka import *

from improved_display import *
from client_states import *

CHANNEL = 8

radio.enable()
radio.config(channel=CHANNEL)

display = ImprovedQuokkaDisplay(display.spi)

while True:
    state_actions = {
                    CALIBRATE : calibrate,
                    CONNECT_SERVER : connect_to_server,
                    CHOOSE_POKEMON : choose_pokemon,
                    RESET : machine.soft_reset
                    }

    state = state_actions[state]()
    # if state == CALIBRATE:
    #     calibrate()
    #     print(state)
    #
    # elif state == CONNECT_SERVER:
    #     connect_to_server()
    #
    # elif state == CHOOSE_POKEMON:
    #     choose_pokemon()
    #
    # elif state == CHOOSE_MOVE:
    #     pass
    #
    # elif state == READ_ZMOVE:
    #     state = TRANSFER_BATTLE
    #
    # elif state == TRANSFER_BATTLE:
    #     pass
    #
    # elif state == DISPLAY_TURN:
    #     pass
    #
    # elif state == RESULT_SCREEN:
    #     pass
    #
    # elif state == RESET:
    #     reset()
