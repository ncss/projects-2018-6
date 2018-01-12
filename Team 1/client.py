from quokka import *

from client_states import *

CHANNEL = 8

radio.enable()
radio.config(channel=CHANNEL)

# display = ImprovedQuokkaDisplay(display.spi)

while True:
    state_actions = {
                    CALIBRATE : calibrate,
                    CONNECT_SERVER : connect_to_server,
                    CHOOSE_POKEMON : choose_pokemon,
                    CHOOSE_MOVE: choose_move,
                    RESET : machine.soft_reset
                    }

    state = state_actions[state]()
